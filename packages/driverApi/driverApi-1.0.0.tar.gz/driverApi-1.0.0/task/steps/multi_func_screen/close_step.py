# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.multi_func_screen import MultiFuncScreen


class CloseStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        screen: MultiFuncScreen = context.get_device()
        if not screen:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return
        flag = screen.close()
        if flag < 0:
            result.status = StepStatus.FAIL
            result.data = "关闭设备失败"
            return
        result.status = StepStatus.SUCCESS
