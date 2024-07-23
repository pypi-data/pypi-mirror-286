# author: haoliqing
# date: 2023/9/18 14:06
# desc:
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.step_model.base_step import Step
from model.task_model.step_model.step_result import StepResult
from device.base_device import Device


class DefaultResetStep(Step):
    """默认的重置步骤，该步骤用于设备调用失败后，重置设备驱动"""

    def execute(self, context: DeviceRequestContext, result: StepResult):
        device: Device = context.get_device()
        if device:
            device.close()
