# author: haoliqing
# date: 2023/8/29 15:58
# desc:
from model.function.function_config import FunctionConfig
from model.task_model.context.system_request_context import SystemRequestContext
from model.task_model.system_task import SystemTask
from typing import List, Dict
from common import common_utils


class SystemFunction(FunctionConfig):
    """系统功能定义"""

    def __init__(self, func_cfg: dict):
        super().__init__(func_cfg)

    def get_task(self, task_id: str, sys_request_context: SystemRequestContext) -> SystemTask:

        sys_task: SystemTask = self.__create_task(task_id, sys_request_context)
        return sys_task

    def __create_task(self, task_id: str, sys_request_context: SystemRequestContext) -> SystemTask:
        class_path = self.__get_action_cfg()
        sys_task: SystemTask = common_utils.create_obj_by_cls_path(class_path, task_id, sys_request_context)
        sys_task.param_cfg = self.__get_param_cfg()
        return sys_task

    def __get_param_cfg(self) -> List[Dict]:
        return self.function_conf.get(self.PARAMS_NODE, None)

    def __get_action_cfg(self) -> str:
        return self.function_conf.get(self.FUNC_NODE_ACTION, None)
