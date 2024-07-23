# author: haoliqing
# date: 2023/8/21 17:11
# desc: 系统任务管理器

from common.singleton import Singleton
from model.task_model.context.system_request_context import SystemRequestContext
from model.task_model.system_task import SystemTask
from task.task_factory import TaskFactory


@Singleton
class SystemTaskManager(object):

    def execute(self, sys_request_context: SystemRequestContext):
        function_name = sys_request_context.function_name
        task: SystemTask = TaskFactory().create_system_task(function_name, sys_request_context)
        task.action()
