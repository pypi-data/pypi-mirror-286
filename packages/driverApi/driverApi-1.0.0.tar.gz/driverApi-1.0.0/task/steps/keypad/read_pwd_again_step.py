# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.keypad import KeyPad


class ReadPwdAgainStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        keypad: KeyPad = context.get_device()
        if not keypad:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        cfm_pwd = keypad.read_pwd(1)
        if cfm_pwd.error_code >= 0:
            if context.get_response().get_response_value(context.get_request_param_data("pwdID")) == cfm_pwd.data:
                if context.get_request_param_data("cfmPwdID"):
                    context.get_response().add_response_value(context.get_request_param_data("cfmPwdID"), cfm_pwd.data)
                result.status = StepStatus.SUCCESS
                context.get_response().ret_code = cfm_pwd.error_code
            else:
                result.status = StepStatus.FAIL
                result.code = -2
                result.data = "两次密码输入不一致"
        else:
            result.status = StepStatus.FAIL
            result.data = "读取确认密码失败"
            result.code = cfm_pwd.error_code
            return
