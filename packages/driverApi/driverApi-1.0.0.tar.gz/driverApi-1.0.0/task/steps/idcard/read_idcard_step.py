# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.id_card_reader import IDCardReader, IDInfo


class ReadIDCardStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        id_reader: IDCardReader = context.get_device()
        if not id_reader:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        id_info: IDInfo = id_reader.read()
        if id_info and id_info.err_code == 0:
            self.__set_ret_value(context, "peopleIDID", id_info.id)
            self.__set_ret_value(context, "nameID", id_info.cnName)
            self.__set_ret_value(context, "sexID", id_info.sex)
            self.__set_ret_value(context, "nationID", id_info.nation)
            self.__set_ret_value(context, "birthdayID", id_info.birthday)
            self.__set_ret_value(context, "addressID", id_info.address)
            self.__set_ret_value(context, "policeID", id_info.dep)
            self.__set_ret_value(context, "validStartID", id_info.begin)
            self.__set_ret_value(context, "validEndID", id_info.end)
            self.__set_ret_value(context, "imageInfoID", id_info.image_info)
            context.get_response().ret_code = id_info.err_code
            result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.code = id_info.err_code
            result.data = "读取二代身份证信息失败"
            return

    def __set_ret_value(self, context: DeviceRequestContext, param_id, value):
        if context.get_request_param_data(param_id):
            context.get_response().add_response_value(context.get_request_param_data(param_id), value)
