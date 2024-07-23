# author: haoliqing
# date: 2023/8/17 14:08
# desc: 响应，设备功能或系统功能执行后完成的结果
from enum import Enum, unique


@unique
class ResponseState(Enum):
    SUCCESS = 'SUCCESS'  # 成功
    FAIL = 'FAIL'  # 失败
    EXCEPTION = 'EXCEPTION'  # 发生异常
    NA = 'NA'  # 未知


class Response(object):

    def __init__(self):
        self.__response_values = {}  # 创建空字典
        self.__response_state = ResponseState.NA  # 初始状态为未知
        self.__ret_code = ""
        self.__ret_msg = ""

    @property
    def state(self):
        return self.__response_state

    @state.setter
    def state(self, state: ResponseState):
        self.__response_state = state

    @property
    def ret_code(self):
        return self.__ret_code

    @ret_code.setter
    def ret_code(self, ret_code):
        self.__ret_code = ret_code

    @property
    def ret_msg(self):
        return self.__ret_msg

    @ret_msg.setter
    def ret_msg(self, ret_msg):
        self.__ret_msg = ret_msg

    @property
    def response_values(self):
        return self.__response_values

    def get_response_value(self, data_id):
        return self.__response_values.get(data_id)

    def add_response_value(self, data_id, data_value):
        self.__response_values[data_id] = data_value
