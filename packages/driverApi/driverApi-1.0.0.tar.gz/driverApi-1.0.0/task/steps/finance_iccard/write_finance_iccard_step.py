# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from driver.finance_ic_card_rwer import FinanceICCardRWer, WriteICResult
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext


class WriteFinanceICCardStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        ic_writer: FinanceICCardRWer = context.get_device()
        if not ic_writer:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        arpc = context.get_request_param_data("arpc")
        script = context.get_request_param_data("script")
        """
        写IC卡时，写入卡中的数据符合PBOC2.0规范的55域数据
        一般格式为“910A xx xx xx xx xx xx xx xx 3030 写卡脚本”
        写卡脚本格式为71(72)xx xx xx xx
        开放给交易的接口有两个输入字段 arpc 和 writeCardScript
        一般来说，后台返回的写卡数据可能有以下几种情况
        1、返回完整的符合55域规范数据（这种情况输入的ARPC长度一定大于20，且writeCardScript为空）
        2、返回单独的arpc和writeCardScript，且arpc长度为16位
        3、返回单独的arpc和writeCardScript，且arpc长度为20位
        如遇到其他情况，还需扩展
        """

        input_data = self.__create_input_data(arpc, script)
        writeResult: WriteICResult = ic_writer.write_finance_ic_info(input_data)
        if writeResult and writeResult.err_code >= 0:
            self.__set_ret_value(context, "scriptResultID", writeResult.script_result)
            self.__set_ret_value(context, "tranCertID", writeResult.tc)
            context.get_response().ret_code = str(writeResult.err_code)
            result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.code = writeResult.err_code
            result.data = "写入IC卡信息失败"
            return

    def __create_input_data(self, arqc: str, script: str) -> str:
        """
        生成写卡的输入数据
        :param arqc: 应用输入的ARPC数据
        :param script: 应用输入的写卡脚本
        :return: 生成的写卡数据
        """
        input_data = None
        if not arqc or arqc.isspace() or len(arqc) < 16:
            return input_data

        if len(arqc) > 20:
            return arqc

        if len(arqc) == 20:
            input_data = '910A' + arqc
        elif len(arqc) == 16:
            input_data = '910A' + arqc + '3030'
        else:
            return input_data

        if script and not script.isspace():
            input_data = input_data + script

        return input_data

    def __set_ret_value(self, context: DeviceRequestContext, param_id, value):
        if context.get_request_param_data(param_id):
            context.get_response().add_response_value(context.get_request_param_data(param_id), value)
