# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.keypad import KeyPad


class ReadPwdStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        keypad: KeyPad = context.get_device()
        if not keypad:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        pwd = keypad.read_pwd(0)
        if pwd.error_code >= 0:
            context.get_response().add_response_value(context.get_request_param_data("pwdID"), pwd.data)
            context.get_response().ret_code = pwd.error_code
            result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.code = pwd.error_code
            result.data = "读取密码失败"
            return
