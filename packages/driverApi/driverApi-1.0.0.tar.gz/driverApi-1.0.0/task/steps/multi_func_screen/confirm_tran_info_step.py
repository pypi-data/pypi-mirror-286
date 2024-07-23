# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.multi_func_screen import MultiFuncScreen


class ConfirmTranInfoStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        screen: MultiFuncScreen = context.get_device()
        if not screen:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        info = context.get_request_param_data("info")
        param = context.get_request_param_data("param")
        if not param:
            param = '{}'

        flag = screen.confirm_tran_info(info, param)
        if flag == 0:
            self.__set_ret_value(context, "resultID", flag)
            context.get_response().ret_code = flag
            result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.data = "确认交易信息失败"
            result.code = flag
            return

    def __set_ret_value(self, context: DeviceRequestContext, param_id, value):
        if context.get_request_param_data(param_id):
            context.get_response().add_response_value(context.get_request_param_data(param_id), value)
