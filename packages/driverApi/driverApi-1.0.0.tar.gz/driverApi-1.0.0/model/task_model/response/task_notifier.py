# author: haoliqing
# date: 2023/10/9 19:41
# desc:
from abc import ABCMeta, abstractmethod
from model.task_model.context.request_context import RequestContext


class TaskNotifier(object, metaclass=ABCMeta):
    """任务通知器基类"""

    @abstractmethod
    def on_start(self, ctx: RequestContext):
        """任务开始时调用"""
        pass

    @abstractmethod
    def on_success(self, ctx: RequestContext):
        """任务成功时调用"""
        pass

    @abstractmethod
    def on_fail(self, ctx: RequestContext):
        """任务失败时调用"""
        pass

    @abstractmethod
    def on_retry(self, ctx: RequestContext):
        """任务重试时调用"""
        pass

    @abstractmethod
    def on_repeat(self, ctx: RequestContext):
        """任务重复执行时调用"""
        pass

    @abstractmethod
    def on_halt(self, ctx: RequestContext):
        """任务挂起，需要手动干预"""
        pass
