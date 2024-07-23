# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.magnetic_strip_rwer import MagneticStripRWer, MagneticStripInfo


class WriteMagneticInfoStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        magnetic_writer: MagneticStripRWer = context.get_device()
        if not magnetic_writer:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        stack1_info = context.get_request_param_data("stack1_info")
        stack2_info = context.get_request_param_data("stack2_info")
        stack3_info = context.get_request_param_data("stack3_info")
        flag = magnetic_writer.write(stack1_info, stack2_info, stack3_info)
        result.code = flag
        if flag < 0:
            result.status = StepStatus.FAIL
            result.data = "写入磁条卡失败"
            return
        result.status = StepStatus.SUCCESS
