# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.file_printer import FilePrinter


class PrintSingleFileStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        printer: FilePrinter = context.get_device()
        if not printer:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return
        file_path = context.get_request_param_data("filePath")
        print_result = printer.print_single_file(file_path)
        if print_result.error_code >= 0:
            context.get_response().ret_code = print_result.error_code
            context.get_response().ret_msg = print_result.error_msg
            result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.code = print_result.error_code
            result.data = print_result.error_msg
            return
