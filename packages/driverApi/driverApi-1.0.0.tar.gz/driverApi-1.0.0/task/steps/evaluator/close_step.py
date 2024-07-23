# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.evaluator import Evaluator


class CloseStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        print(context.last_step_result.__dict__)
        evaluator: Evaluator = context.get_device()
        if not evaluator:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return
        flag = evaluator.close()
        if flag < 0:
            result.status = StepStatus.FAIL
            result.data = "关闭设备失败"
            return
        result.code = context.last_step_result
        result.status = StepStatus.SUCCESS
