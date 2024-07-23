# author: haoliqing
# date: 2023/8/21 16:58
# desc: 设备功能请求上下文定义
from model.task_model.context.request_context import RequestContext
from driver.cache.cache import DriverCache
from enum import Enum, unique
from model.task_model.response import DeviceResponse
from device.base_device import Device, DeviceConfig


@unique
class RequestType(Enum):
    FIRST_RUN = 0  # 成功
    FAIL = 1  # 失败
    EXCEPTION = 2  # 发生异常
    NA = 3  # 未知


class DeviceRequestContext(RequestContext):
    driver_cache: DriverCache = DriverCache()

    def __init__(self, request_id, request_data, function_cfg, socket):
        super().__init__(request_id, request_data, function_cfg, socket)
        self.__device_class: str = None
        self.__device_model: str = None
        self.__device_cfg: DeviceConfig = None
        self.__driver_key: str = None
        self.__last_step_result = None

    @property
    def device_class(self) -> str:
        return self.__device_class

    @property
    def driver_key(self) -> str:
        return self.__driver_key

    @property
    def device_model(self) -> str:
        return self.__device_model

    def create_response(self) -> DeviceResponse:
        return DeviceResponse()

    def get_device(self) -> Device:
        return self.driver_cache.get_driver(self.__driver_key)

    def set_device(self, device: Device):
        if not self.get_device():
            self.driver_cache.cache_driver(self.__driver_key, device)

    def set_device_cfg(self, device_cfg: DeviceConfig):
        self.__device_cfg = device_cfg
        self.__device_class = device_cfg.device_class
        self.__device_model = device_cfg.device_model
        self.__driver_key = self.__device_class + self.__device_model

    @property
    def device_cfg(self):
        return self.__device_cfg

    def unset_device(self):
        self.driver_cache.clean_driver(self.__driver_key)

    @property
    def device_class(self):
        return self.__device_class

    @property
    def device_model(self):
        return self.__device_model

    @property
    def last_step_result(self):
        return self.__last_step_result

    @last_step_result.setter
    def last_step_result(self, step_result):
        self.__last_step_result = step_result
