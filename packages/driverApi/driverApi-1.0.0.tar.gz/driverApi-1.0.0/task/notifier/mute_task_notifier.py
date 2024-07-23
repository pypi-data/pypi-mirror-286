# author: haoliqing
# date: 2023/10/9 20:21
# desc:


from model.task_model.context.request_context import RequestContext
from model.task_model.response.task_notifier import TaskNotifier


class MuteTaskNotifier(TaskNotifier):
    """静默任务通知器，不做任何事情"""

    def on_start(self, ctx: RequestContext):
        pass

    def on_success(self, ctx: RequestContext):
        pass

    def on_fail(self, ctx: RequestContext):
        pass

    def on_retry(self, ctx: RequestContext):
        pass

    def on_repeat(self, ctx: RequestContext):
        pass

    def on_halt(self, ctx: RequestContext):
        pass
