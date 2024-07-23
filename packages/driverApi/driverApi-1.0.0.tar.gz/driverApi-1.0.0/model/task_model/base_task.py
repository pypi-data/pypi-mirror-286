from abc import ABCMeta, abstractmethod
from enum import Enum, unique
from typing import List
from model.task_model.context.request_context import RequestContext


@unique
class TaskStatus(Enum):
    """ 任务状态枚举类 """
    SUCCESS = 0  # 任务已经成功执行完毕
    FAIL = 1  # 任务执行失败
    READY = 2  # 任务等待执行
    RUN = 3  # 任务正在执行
    HALT = 4  # 任务暂停执行，可以被恢复为READY
    TERMINATE = 5  # 任务已经被终止，即将被清除
    CANCEL = 6  # 任务被取消


@unique
class TaskRetryType(Enum):
    """ 任务重试类型枚举类 """
    NOT = 0  # 不重试
    MANUAL = 1  # 手动重试
    AUTO = 2  # 自动重试


class TaskStatusListener(object, metaclass=ABCMeta):

    @abstractmethod
    def on_status_change(self, task_id: str, status: TaskStatus):
        pass


class Task(object, metaclass=ABCMeta):

    def __init__(self, task_id, context: RequestContext):
        """初始化方法"""
        # 默认READY状态
        self.__status = TaskStatus.READY
        self.__status_code = None
        self.__message = None
        self.__retry_type = TaskRetryType.NOT
        self.__id = task_id
        self.__auto_retry_num = 0
        self.__status_listeners: List[TaskStatusListener] = []
        self.__request_context = context

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status: TaskStatus):
        self.__status = status
        for listener in self.__status_listeners:
            listener.on_status_change(self.id, status)

    @property
    def status_code(self):
        return self.__status_code

    @status_code.setter
    def status_code(self, code: str):
        self.__status_code = code

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, msg: str):
        self.__message = msg

    @property
    def id(self):
        return self.__id

    @property
    def retry_type(self):
        return self.__retry_type

    @retry_type.setter
    def retry_type(self, retry_type: TaskRetryType):
        self.__retry_type = retry_type

    @property
    def auto_retry_num(self):
        return self.__auto_retry_num

    @auto_retry_num.setter
    def auto_retry_num(self, num: int):
        self.__auto_retry_num = num

    @property
    def request_context(self):
        return self.__request_context

    @request_context.setter
    def request_context(self, context: RequestContext):
        self.__request_context = context

    def is_manual_retry_on_halt(self):
        """任务挂起时是否手动重试"""
        # 在自动重试的情况下，重试次数使用完要转为手动重试
        if self.status == TaskStatus.CANCEL:
            return False
        return self.__retry_type == TaskRetryType.MANUAL or self.__retry_type == TaskRetryType.AUTO

    def is_auto_retry_on_halt(self):
        """任务挂起时是否自动重试"""
        return self.__retry_type == TaskRetryType.AUTO

    def add_status_listener(self, listener: TaskStatusListener):
        self.__status_listeners.append(listener)
