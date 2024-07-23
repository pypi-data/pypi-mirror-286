# author: haoliqing
# date: 2023/9/22 16:33
# desc:
import json

from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.multi_func_screen import MultiFuncScreen, FileType


class DeleteFileStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        screen: MultiFuncScreen = context.get_device()
        if not screen:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        file_path: str = context.get_request_param_data("fileName")
        file_type: str = context.get_request_param_data("fileType")
        flag = screen.delete_file(FileType(int(file_type)), file_path)
        if flag >= 0:
            result.status = StepStatus.SUCCESS
            context.get_response().ret_code = str(flag)
        else:
            result.status = StepStatus.FAIL
            result.code = flag
            result.data = "删除文件失败"
            return

