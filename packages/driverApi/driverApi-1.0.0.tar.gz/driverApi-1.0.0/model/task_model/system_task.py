# author: haoliqing
# date: 2023/9/21 20:55
# desc:

from abc import ABCMeta, abstractmethod
from model.task_model.base_task import Task
from typing import List, Dict
from model.task_model.context.system_request_context import SystemRequestContext
from model.task_model.context.request_context import RequestContext


class SystemTask(Task, metaclass=ABCMeta):

    def __init__(self, task_id, context: RequestContext):
        super().__init__(task_id, context)
        self.__param_cfg: List[Dict] = None

    @abstractmethod
    def action(self):
        pass

    @property
    def param_cfg(self):
        return self.__param_cfg

    @param_cfg.setter
    def param_cfg(self, param_cfg: List[Dict]):
        self.__param_cfg = param_cfg


