# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from device.base_device import Device
from driver.driver_factory import DriverFactory
from driver.file_printer import FilePrinter


class InitStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        device: Device = context.get_device()
        if not device:
            device = DriverFactory().get_device(context.device_cfg)
        if not device:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return
        if isinstance(device, FilePrinter):
            context.set_device(device)
            flag = device.init(context.device_cfg)
            if flag < 0:
                result.status = StepStatus.FAIL
                result.data = "初始化设备驱动失败"
            else:
                flag = device.open()
                if flag < 0:
                    result.status = StepStatus.FAIL
                    result.data = "打开设备失败"
                else:
                    result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.data = "获取到的设备驱动类型不匹配"


