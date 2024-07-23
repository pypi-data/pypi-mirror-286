# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.keypad import KeyPad


class SetSecKeyStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        keypad: KeyPad = context.get_device()
        if not keypad:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return
        if context.get_request_data("newMasterSecKey") and context.get_request_data("oldMasterSecKey"):
            flag = keypad.set_master_key(context.get_request_data("oldMasterSecKey"),
                                         context.get_request_data("newMasterSecKey"))
            if flag < 0:
                result.status = StepStatus.FAIL
                result.data = "设置主密钥失败"
                return
        if context.get_request_data("workSecKey"):
            flag = keypad.set_work_key(context.get_request_data("workSecKey"))
            if flag < 0:
                result.status = StepStatus.FAIL
                result.data = "设置工作密钥失败"
                return

        result.status = StepStatus.SUCCESS
