# author: haoliqing
# date: 2023/8/21 16:55
# desc: 设备调用任务管理器
import traceback

from common.singleton import Singleton
from exception.device_exception import DeviceException
from model.task_model.context.device_request_context import DeviceRequestContext
from device.device_config_manager import DeviceConfigManager
from model.global_param_manager import GlobalParamManager
from task.task_factory import TaskFactory
from model.task_model.device_task import DeviceTask
from common import global_constants
from typing import Dict
from task.container.task_container import TaskContainer
from task.handler.task_handler import TaskHandler
from logger.device_logger import logger
import time


@Singleton
class DeviceTaskManager(object):
    device_config_manager: DeviceConfigManager = DeviceConfigManager()
    global_param_manager: GlobalParamManager = GlobalParamManager()
    task_containers: Dict[str, TaskContainer] = {}
    is_start = False

    def start(self) -> bool:
        if self.is_start:
            logger.warn("外设调用任务管理器已启动，不再重复启动")
        port_list: set[str] = self.device_config_manager.get_all_ports()
        try:
            for port_id in port_list:
                task_container = TaskContainer("container_" + port_id, TaskHandler())
                self.task_containers[port_id] = task_container
                task_container.start()
            self.is_start = True
            return True
        except Exception as e:
            logger.error("初始化设备任务管理器发生异常: {0}, 异常信息：{1}".format(str(e), traceback.format_exc()))
            for task_container in self.task_containers.values():
                task_container.cancel()
            return False

    def stop(self) -> bool:
        try:
            for task_container in self.task_containers.values():
                flag = task_container.cancel()
                if not flag:
                    return flag
                else:
                    task_container.clear_task()
            self.is_start = False
            return True
        except Exception as e:
            logger.error("停止设备任务管理器发生异常: {0}, 异常信息：{1}".format(str(e), traceback.format_exc()))
            # TODO 重启任务队列
            return False

    def execute(self, dev_request_context: DeviceRequestContext):
        start = time.time()
        function_name = dev_request_context.function_name
        class_list = self.global_param_manager.get_func_class(function_name)
        device_cfgs = self.device_config_manager.get_device_cfgs_by_classes(class_list.split("|"))
        if device_cfgs:
            # 传参时若指定了设备型号，则查找对应的设备
            device_model = dev_request_context.get_request_param_data("deviceMOD")
            device_cfg = None
            if not device_model:
                device_cfg = device_cfgs[0]
            else:
                for device_item in device_cfgs:
                    if device_item.device_model == device_model:
                        device_cfg = device_item
                        break
                else:
                    device_exception = DeviceException('E01003', function_name)
                    logger.error(str(device_exception))
                    raise device_exception
            dev_request_context.set_device_cfg(device_cfg)
            task: DeviceTask = TaskFactory().create_device_task(function_name, dev_request_context)
            end = time.time()
            logger.info("构建外设调用任务耗时" + str(end - start) + "秒")
            self.task_containers[device_cfg.port.port_id].add_task(task)

        else:
            device_exception = DeviceException('E01003', function_name)
            logger.error(str(device_exception))
            raise device_exception

    def execute_inner_status_query(self, dev_request_context: DeviceRequestContext):
        function_name = dev_request_context.function_name
        task: DeviceTask = TaskFactory().create_device_task(function_name, dev_request_context)
        device_cfg = dev_request_context.device_cfg
        isExist = self.task_containers.get(device_cfg.port.port_id, None)
        if isExist:
            self.task_containers[device_cfg.port.port_id].add_status_task(task)
        else:
            pass
