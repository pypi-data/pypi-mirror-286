# author: haoliqing
# date: 2023/9/22 10:11
# desc:
import traceback

import exception
from device.base_device import Device
from driver.driver_factory import DriverFactory
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.device_task import DeviceTask
from model.task_model.base_task import TaskStatus, TaskRetryType
from task.manager.device_status_manager import DeviceStatusManager
from device.status.device_status import DeviceStatus, DeviceStatusType
from logger.device_logger import logger


class QueryDeviceStatusTask(DeviceTask):
    status_manager: DeviceStatusManager = DeviceStatusManager()

    def execute(self):
        try:
            context: DeviceRequestContext = self.request_context
            device: Device = context.get_device()
            if not device:
                device = DriverFactory().get_device(context.device_cfg)
            if not device:
                self.__notify_status(DeviceStatusType.DEV_UNINSTALL)
                return
            flag = device.init(context.device_cfg)
            if flag < 0:
                self.__notify_status(DeviceStatusType.DEV_ERROR)
            else:
                status = device.get_status()
                if status:
                    self.status_manager.add_status(status)
                else:
                    self.__notify_status(DeviceStatusType.DEV_UNKNOWN)
        except exception as e:
            logger.error("执行设备状态查询任务时发生异常: {0}, 异常信息：{1}"
                         .format(str(e), traceback.format_exc()))
            self.__notify_status(DeviceStatusType.DEV_UNKNOWN)
        finally:
            # 无论状态查询任务是否执行成功，都改为成功状态以释放当前任务句柄
            self.status = TaskStatus.SUCCESS

    def __notify_status(self, status_type: DeviceStatusType):
        status = DeviceStatus(status_type, self.request_context.device_cfg)
        self.status_manager.add_status(status)

    def restart_task(self):
        self.status = TaskStatus.RUN

    def finish_task(self):
        self.__on_task_fail()
