# author: haoliqing
# date: 2023/9/15 10:33
# desc:

from abc import abstractmethod
from model.task_model.step_model.step_result import StepResult
from model.task_model.context.device_request_context import DeviceRequestContext


class Step(object):

    def __init__(self, step_id: str):
        self.__id = step_id
        self.__hint = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, _id: str):
        self.__id = _id

    @property
    def hint(self):
        return self.__hint

    @hint.setter
    def hint(self, hint: str):
        self.__hint = hint

    @abstractmethod
    def execute(self, context: DeviceRequestContext, result: StepResult):
        pass
