# author: haoliqing
# date: 2023/9/22 16:33
# desc:
import json

from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.finger_scanner import FingerScanner
from typing import List


class VerifyStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        finger: FingerScanner = context.get_device()
        if not finger:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        templates: List = context.get_request_param_data("templates")
        flag = finger.verify_finger(templates)
        if flag >= 0:
            result.status = StepStatus.SUCCESS
            context.get_response().ret_code = str(flag)
        else:
            result.status = StepStatus.FAIL
            result.code = flag
            result.data = "验证指纹失败"
            return


