# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from driver.multi_func_keypad import MultiFuncKeyPad
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.step_model import Step, StepStatus, StepResult


class ReadAuthCodeStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        keypad: MultiFuncKeyPad = context.get_device()
        if not keypad:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        if not isinstance(keypad, MultiFuncKeyPad):
            result.status = StepStatus.FAIL
            result.data = "该设备不支持读取验证码"
            return

        pwd = keypad.read_auth_code()
        result.code = pwd.error_code
        if pwd.error_code == 0:
            context.get_response().add_response_value(context.get_request_param_data("authCodeID"), pwd.data)
            context.get_response().ret_code = pwd.error_code
            result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.code = pwd.error_code
            result.data = "读取验证码失败"
            return
