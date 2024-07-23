# author: haoliqing
# date: 2023/9/22 16:33
# desc:
import json

from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.evaluator import Evaluator


class UpdateTellerPhotoStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        evaluator: Evaluator = context.get_device()
        if not evaluator:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        file_path: str = context.get_request_param_data("filePath")
        flag = evaluator.update_teller_photo(file_path)
        if flag >= 0:
            result.status = StepStatus.SUCCESS
            context.get_response().ret_code = flag
        else:
            result.status = StepStatus.FAIL
            result.code = flag
            result.data = "更新柜员头像失败"
            return
