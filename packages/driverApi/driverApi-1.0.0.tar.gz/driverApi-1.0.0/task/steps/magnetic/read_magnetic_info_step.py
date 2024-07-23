# author: haoliqing
# date: 2023/9/22 16:33
# desc:
from model.task_model.step_model import Step, StepStatus, StepResult
from model.task_model.context.device_request_context import DeviceRequestContext
from driver.magnetic_strip_rwer import MagneticStripRWer, MagneticStripInfo


class ReadMagneticInfoStep(Step):
    def execute(self, context: DeviceRequestContext, result: StepResult):
        magnetic_reader: MagneticStripRWer = context.get_device()
        if not magnetic_reader:
            result.status = StepStatus.FAIL
            result.data = "无法获取到设备驱动"
            return

        mag_info: MagneticStripInfo = magnetic_reader.read()
        result.code = mag_info.err_code
        if mag_info and mag_info.err_code == 0:
            self.__set_ret_value(context, "numID", mag_info.card_no)
            self.__set_ret_value(context, "track1ID", mag_info.stack1_info)
            self.__set_ret_value(context, "track2ID", mag_info.stack2_info)
            self.__set_ret_value(context, "track3ID", mag_info.stack3_info)
            result.status = StepStatus.SUCCESS
            context.get_response().ret_code = mag_info.err_code
        else:
            result.status = StepStatus.FAIL
            result.code = mag_info.err_code
            result.data = "读取磁条信息失败"
            return

    def __set_ret_value(self, context: DeviceRequestContext, param_id, value):
        if context.get_request_param_data(param_id):
            context.get_response().add_response_value(context.get_request_param_data(param_id), value)
