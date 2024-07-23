# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.evaluator import Evaluator, EvaluateInfo


class GetEvaluateResultStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        evaluator: Evaluator = context.get_device()
        if not evaluator:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        teller_id = context.get_request_param_data("tellerID")
        teller_name = context.get_request_param_data("tellerName")
        teller_photo = context.get_request_param_data("tellerPhoto")
        star_level = context.get_request_param_data("starLevel")
        if not star_level:
            star_level = 5
        eva_info: EvaluateInfo = evaluator.get_evaluate_result(teller_id, teller_name, teller_photo, int(star_level))
        if eva_info and eva_info.err_code >= 0:
            self.__set_ret_value(context, "levelID", eva_info.level)
            self.__set_ret_value(context, "messageID", eva_info.message)
            context.get_response().ret_code = eva_info.err_code
            result.status = StepStatus.SUCCESS
        else:
            result.status = StepStatus.FAIL
            result.data = "读取评价信息失败"
            result.code = eva_info.err_code
            return

    def __set_ret_value(self, context: DeviceRequestContext, param_id, value):
        if context.get_request_param_data(param_id):
            context.get_response().add_response_value(context.get_request_param_data(param_id), value)

