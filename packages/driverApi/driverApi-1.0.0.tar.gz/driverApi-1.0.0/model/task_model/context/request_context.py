# author: haoliqing
# date: 2023/8/17 19:39
# desc: 请求上下文基类，设备功能请求上下文和系统功能请求上下文都基于此基类

from abc import ABCMeta, abstractmethod
from model.task_model.response import Response
from common import global_constants
from typing import Dict


class RequestContext(object, metaclass=ABCMeta):

    def __init__(self, request_id, request_data, function_cfg, socket):
        self.__response: Response = self.create_response()
        self.__request_id: str = request_id
        self.__request_data: Dict = request_data
        self.__function_cfg = function_cfg
        self.__socket = socket
        self.__request_id = request_id

    @property
    def request_id(self):
        return self.__request_id

    @property
    def function_name(self):
        return self.__request_data[global_constants.FUNCTION_NAME]

    @property
    def request_data(self):
        return self.__request_data

    def get_request_data(self, data_id: str):
        return self.__request_data.get(data_id, None)

    def get_request_param_data(self, data_id: str):
        data = None
        param: dict = self.__request_data.get("param", None)
        if param:
            data = param.get(data_id, None)
        return data

    @property
    def function_cfg(self):
        return self.__function_cfg

    @abstractmethod
    def create_response(self):
        """ 创建空的响应数据 """
        pass

    """ 设置响应数据 """

    def set_response(self, response: Response):
        self.__response = response

    def get_response(self) -> Response:
        return self.__response

    @property
    def socket(self):
        return self.__socket

