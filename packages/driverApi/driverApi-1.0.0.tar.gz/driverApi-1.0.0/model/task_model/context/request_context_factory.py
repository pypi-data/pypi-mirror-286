# author: haoliqing
# date: 2023/8/21 21:00
# desc: 请求上下文工厂
from common import Singleton
from model.task_model.context.request_context import RequestContext
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.context.system_request_context import SystemRequestContext
from common import global_constants
from model.global_param_manager import GlobalParamManager
import threading
from logger.device_logger import logger
from exception.device_exception import DeviceException


@Singleton
class RequestContextFactory(object):
    global_param_manager: GlobalParamManager = GlobalParamManager()
    lock = threading.RLock()

    def get_request_context(self, request_id: str, request_data, socket) -> RequestContext:
        func_name = request_data[global_constants.FUNCTION_NAME]
        context = None

        if self.global_param_manager.get_device_func_cfg(func_name):
            return DeviceRequestContext(request_id, request_data,
                                        self.global_param_manager.get_device_func_cfg(func_name), socket)
        elif self.global_param_manager.get_system_func_cfg(func_name):
            return SystemRequestContext(request_id, request_data,
                                        self.global_param_manager.get_system_func_cfg(func_name), socket)
        else:
            device_exception = DeviceException('E01002', func_name)
            logger.error(str(device_exception))
            raise device_exception
