# author: haoliqing
# date: 2023/8/31 16:44
# desc:


class TaskHandler(object):
    """任务执行器基类"""

    def __init__(self):
        self._current_task = None

    def execute(self, task):
        """任务未执行完成（非完成/失败/取消状态）的情况下，handler始终持有任务"""
        self._current_task = task
        self.__execute_task(task)

    def get_current_task(self):
        return self._current_task

    def __execute_task(self, task):
        task.execute()

    def clean_current_task(self):
        self._current_task = None





