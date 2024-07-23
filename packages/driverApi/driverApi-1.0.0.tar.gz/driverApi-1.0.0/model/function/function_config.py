# author: haoliqing
# date: 2023/8/17 19:54
# desc: 功能定义基类，设备功能定义和系统功能定义都基于此类扩展
from abc import ABCMeta, abstractmethod


class FunctionConfig(object, metaclass=ABCMeta):
    FUNCS_NODE = "functions"

    FUNC_NODE_NAME = "name"
    FUNC_NODE_HINT = "hint"
    FUNC_NODE_DESC = "desc"
    PARAMS_NODE = "params"
    FUNC_NODE_ACTION = "action"
    PARAM_NODE_NAME = "name"
    PARAM_NODE_CLASS = "class"
    PARAM_NODE_CHECK_REQUIRE = "require"
    PARAM_NODE_DESC = "desc"
    PARAM_NODE_RETURN_VALUE = "return"
    TASK_NODE = "task"
    TASK_NODE_CLASS = "class"
    TASK_NODE_NOTIFIER = "notifier"
    TASK_NODE_TIMEOUT = "timeout"
    TASK_NODE_PERIOD = "period"
    TASK_NODE_NUMBER = "number"
    TASK_NODE_RETRY = "retry"
    TASK_NODE_LOOP = "loop"
    STEPS_NODE = "steps"
    TASK_NODE_RESET = "reset"
    STEP_NODE_CLASS = "class"
    STEP_NODE_ID = "id"
    STEP_NODE_HINT = "hint"
    STEP_NODE_RETRY = "retry"
    STEP_NODE_ASYNCHRONOUS = "asynchronous"

    def __init__(self, func_cfg: dict):
        """
        初始化设备功能定义
        :param func_cfg: 设备功能定义的json对象
        """
        self.__func_cfg = func_cfg
        self.__func_name = func_cfg[self.FUNC_NODE_NAME]
        self.__func_desc = func_cfg.get(self.FUNC_NODE_DESC,None)

    @property
    def function_name(self) -> str:
        return self.__func_name

    @property
    def function_desc(self) -> str:
        return self.__func_desc

    @property
    def function_conf(self) -> dict:
        return self.__func_cfg

    @abstractmethod
    def get_task(self, task_id):
        pass
