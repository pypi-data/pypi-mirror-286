# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.multi_func_screen import MultiFuncScreen, SignInfo


class RequestSignStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        screen: MultiFuncScreen = context.get_device()
        if not screen:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        file_path = context.get_request_param_data("filePath")
        param = context.get_request_param_data("param")
        if not param:
            param = '{}'
        sign_info: SignInfo = screen.request_sign(file_path, param)
        if sign_info and sign_info.err_code == 0:
            self.__set_ret_value(context, "signDataID", sign_info.sign_data)
            self.__set_ret_value(context, "signImageBase64ID", sign_info.sign_image_base64)
            context.get_response().ret_code = sign_info.err_code
            result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.code = sign_info.err_code
            result.data = "请求签名失败"
            return

    def __set_ret_value(self, context: DeviceRequestContext, param_id, value):
        if context.get_request_param_data(param_id):
            context.get_response().add_response_value(context.get_request_param_data(param_id), value)
