# author: haoliqing
# date: 2023/9/4 15:13
# desc:
from common.singleton import Singleton
from model.task_model.device_task import DeviceTask
from model.task_model.system_task import SystemTask
from model.global_param_manager import GlobalParamManager
from model.task_model.step_model.default_reset_step import DefaultResetStep
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.context.system_request_context import SystemRequestContext
import threading

globalTaskID: int = 1


@Singleton
class TaskFactory(object):
    """设备调用任务工厂类"""
    global_param_manager: GlobalParamManager = GlobalParamManager()
    lock = threading.RLock()

    def create_device_task(self, func_name, dev_request_context: DeviceRequestContext) -> DeviceTask:
        """根据功能名称创建设备调用任务"""
        device_func = self.global_param_manager.get_device_func_cfg(func_name)
        device_task: DeviceTask = device_func.get_task(dev_request_context.request_id, dev_request_context)  # 任务编号与请求编号保持一致
        if device_task:
            # 添加默认的重置步骤
            device_task.reset_step = DefaultResetStep("default")
            next_cfg = self.global_param_manager.get_device_func_next(func_name)
            if next_cfg:
                device_task.next_cfg = next_cfg
        return device_task

    def create_system_task(self, func_name, sys_request_context: SystemRequestContext) -> SystemTask:
        """根据功能名称创建系统功能任务"""
        sys_func = self.global_param_manager.get_system_func_cfg(func_name)
        sys_task = sys_func.get_task(sys_request_context.request_id, sys_request_context)  # 任务编号与请求编号保持一致
        return sys_task

    def __get_task_id(self) -> int:
        global globalTaskID
        self.lock.acquire()
        try:
            if globalTaskID >= 9999999:
                globalTaskID = 0
            globalTaskID += 1
            return globalTaskID
        finally:
            # 修改完成，释放锁
            self.lock.release()
