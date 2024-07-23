# author: haoliqing
# date: 2023/10/9 20:27
# desc:
from common import Singleton, common_utils
from model.task_model.response.task_notifier import TaskNotifier
from typing import Dict


@Singleton
class TaskNotifierFactory(object):
    notifiers: Dict[str, TaskNotifier] = {}

    def get_task_notifier(self, cls_path: str):
        notifier = self.notifiers.get(cls_path, None)
        if not notifier:
            notifier = common_utils.create_obj_by_cls_path(cls_path)
            self.notifiers[cls_path] = notifier
        return notifier
