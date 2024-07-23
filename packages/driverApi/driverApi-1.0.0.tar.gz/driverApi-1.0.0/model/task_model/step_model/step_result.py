# author: haoliqing
# date: 2023/9/15 14:05
# desc:

from enum import Enum, unique


@unique
class StepStatus(Enum):
    """ 任务状态枚举类 """
    SUCCESS = 0  # 执行成功，如果步骤中包含对设备的调用，则在步骤中要确认设备成功执行完毕，该步骤才能返回成功
    FAIL = 1  # 执行失败
    REPEAT = 2  # 步骤执行成功，但需要重复执行，例如打印多张凭证


class StepResult(object):

    def __init__(self, step_id: str):
        self.__step_id = step_id  # 步骤ID
        self.__status = StepStatus.SUCCESS  # 步骤执行后的状态
        self.__code = None  # 步骤执行后的状态码
        self.__data = None  # 状态信息中的参数

    @property
    def step_id(self):
        return self.__step_id

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status: StepStatus):
        self.__status = status

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code: str):
        self.__code = code

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data: str):
        self.__data = data
