# author: haoliqing
# date: 2023/8/16 14:30
# desc: 设备功能调用任务实现类
from abc import ABCMeta, abstractmethod
from model.task_model.base_task import Task
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.context.request_context import RequestContext
from model.task_model.step_model.base_step import Step
from model.function.device_fucntion_next import DeviceFunctionNext
from typing import List, Dict
from model.function.function_config import FunctionConfig
from model.task_model.response.task_notifier import TaskNotifier
from logger.device_logger import logger


class ValidateResult(object):

    def __init__(self):
        self.validate_flag: bool = False
        self.validate_msg = None


class DeviceTask(Task, metaclass=ABCMeta):

    def __init__(self, task_id: int, context: RequestContext):
        super().__init__(task_id, context)
        self.__reset_step: Step = None
        self.__next_cfg: DeviceFunctionNext = None
        self.__param_cfg: List[Dict] = None
        self.__steps: List[Step] = []
        self.__notifier: TaskNotifier = None
        self.__task_desc: str = None

    @abstractmethod
    def execute(self):
        pass

    def validate(self) -> ValidateResult:
        """根据设备功能定义参数配置校验请求上下文中请求参数是否正确"""
        result: ValidateResult = ValidateResult()
        flag = True
        msg = "请求参数校验不通过:"
        request_data = self.__request_context.request_data
        if self.__param_cfg:
            for param in self.__param_cfg:
                name = param[FunctionConfig.PARAM_NODE_NAME]
                require = param[FunctionConfig.PARAM_NODE_CHECK_REQUIRE]
                desc = param[FunctionConfig.PARAM_NODE_DESC]
                if require == 'Y':
                    if not request_data or not request_data[name]:
                        flag = False
                        msg = msg + '必输项 %s [%s] 没有值,' % (desc, name)
        result.validate_flag = flag
        if not flag:
            result.validate_msg = msg[:-1]
        return result

    @property
    def reset_step(self) -> Step:
        return self.__reset_step

    @reset_step.setter
    def reset_step(self, step: Step):
        self.__reset_step = step

    @property
    def next_cfg(self):
        return self.__next_cfg

    @next_cfg.setter
    def next_cfg(self, next_cfg: DeviceFunctionNext):
        self.__next_cfg = next_cfg

    @property
    def param_cfg(self):
        return self.__param_cfg

    @param_cfg.setter
    def param_cfg(self, param_cfg: List[Dict]):
        self.__param_cfg = param_cfg

    def add_step(self, step: Step):
        self.__steps.append(step)

    @property
    def steps(self):
        return self.__steps

    @property
    def task_notifier(self):
        return self.__notifier

    @task_notifier.setter
    def task_notifier(self, notifier: TaskNotifier):
        self.__notifier = notifier

    @property
    def task_desc(self):
        return self.__task_desc

    @task_desc.setter
    def task_desc(self, task_desc: str):
        self.__task_desc = task_desc

    @abstractmethod
    def restart_task(self):
        pass

    @abstractmethod
    def finish_task(self):
        pass
