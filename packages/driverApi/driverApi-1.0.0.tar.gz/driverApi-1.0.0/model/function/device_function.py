# author: haoliqing
# date: 2023/8/29 15:55
# desc:
from hashlib import new

from model.function.function_config import FunctionConfig
from model.task_model.base_task import TaskRetryType
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.device_task import DeviceTask
from typing import List, Dict
from model.task_model.step_model import Step
from common import common_utils
from model.task_model.response.task_notifier_factory import TaskNotifierFactory


class DeviceFunction(FunctionConfig):
    """设备功能定义"""

    def __init__(self, func_cfg: dict):
        super().__init__(func_cfg)

    def get_task(self, task_id: str, dev_request_context: DeviceRequestContext) -> DeviceTask:
        dev_task: DeviceTask = self.__create_task(task_id, dev_request_context)
        return dev_task

    def __create_task(self, task_id: str, dev_request_context: DeviceRequestContext) -> DeviceTask:
        class_path = self.get_task_class_name()
        dev_task: DeviceTask = common_utils.create_obj_by_cls_path(class_path, task_id, dev_request_context)
        dev_task.retry_type = self.get_task_retry_type()
        dev_task.auto_retry_num = self.get_task_auto_retry_num()
        dev_task.param_cfg = self.get_param_cfg()
        dev_task.task_notifier = TaskNotifierFactory().get_task_notifier(self.get_task_notifier_name())
        dev_task.task_desc = self.function_conf.get(self.FUNC_NODE_DESC)
        steps = self.get_step_cfg()
        if steps:
            for step_cfg in steps:
                step: Step = self.__create_step(step_cfg)
                if step:
                    dev_task.add_step(step)
        return dev_task

    def get_step_cfg(self) -> List[Dict]:
        return self.get_task_param(self.STEPS_NODE)

    def get_param_cfg(self) -> List[Dict]:
        return self.function_conf.get(self.PARAMS_NODE, None)

    def get_task_class_name(self) -> str:
        return self.get_task_param(self.TASK_NODE_CLASS)

    def get_task_notifier_name(self) -> str:
        return self.get_task_param(self.TASK_NODE_NOTIFIER)

    def get_task_retry_type(self) -> str:
        retry = self.get_task_param(self.TASK_NODE_RETRY)
        if retry:
            if retry == 'M':
                return TaskRetryType.MANUAL
            elif retry == 'A':
                return TaskRetryType.AUTO
            else:
                return TaskRetryType.NOT
        else:
            return TaskRetryType.NOT

    def get_task_auto_retry_num(self) -> int:
        num = self.get_task_param(self.TASK_NODE_NUMBER)
        if num:
            return num
        else:
            return 0

    def get_task_param(self, param_id: str):
        task_cfg = self.function_conf.get(self.TASK_NODE, None)
        if task_cfg:
            return task_cfg.get(param_id, None)
        else:
            return None

    def __create_step(self, step_cfg: Dict) -> Step:
        step_id = step_cfg[FunctionConfig.STEP_NODE_ID]
        step_class = step_cfg[FunctionConfig.STEP_NODE_CLASS]
        step_hint = step_cfg[FunctionConfig.STEP_NODE_HINT]
        step: Step = None
        if step_class:
            step = common_utils.create_obj_by_cls_path(step_class, step_id)
            step.hint = step_hint
        return step
