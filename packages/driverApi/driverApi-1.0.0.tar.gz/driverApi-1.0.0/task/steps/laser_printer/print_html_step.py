from driver.file_printer import FilePrinter
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.step_model import Step, StepResult, StepStatus


class PrintHtmlStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        printer: FilePrinter = context.get_device()
        if not printer:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return
        html_info = context.get_request_param_data("htmlInfo")
        print_result = printer.print_html_data(html_info)
        if print_result.error_code >= 0:
            context.get_response().ret_code = print_result.error_code
            context.get_response().ret_msg = print_result.error_msg
            result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.code = print_result.error_code
            result.data = print_result.error_msg
            return