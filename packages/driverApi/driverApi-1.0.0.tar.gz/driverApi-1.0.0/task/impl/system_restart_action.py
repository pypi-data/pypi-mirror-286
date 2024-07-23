import json
import traceback

from common import send_socket_msg
from device.device_config_manager import DeviceConfigManager
from driver.cache.cache import DriverCache
from logger.device_logger import logger
from model.task_model.base_task import TaskStatus
from model.task_model.system_task import SystemTask
from task.manager import DeviceTaskManager
from task.manager.device_status_manager import DeviceStatusManager
from webservice.wsserver import Clients


class SystemRestartAction(SystemTask):

    def action(self):
        """ 能点击重启按钮，则系统已经重启 不用再判断是否启动"""

        try:
            self.__restart()
        except Exception as e:
            logger.error("重启外设框架时发生异常: {0}, 异常信息：{1}".format(str(e), traceback.format_exc()))

    def __restart(self):
        context = self.request_context
        device_cfg = context.request_data['deviceConfig']
        if len(device_cfg) == 0:
            raise Exception("读取配置信息失败！")
        """ 执行重启controller里面会返回系统启动零配件类，会重新请求数据 """
        dev_manager: DeviceConfigManager = DeviceConfigManager()
        """ 初始化会clear原有的数据，重新装配"""
        if not dev_manager.init_dev_cfg(device_cfg):
            self.status = TaskStatus.FAIL
            self.message = "初始化设备配置失败"
            logger.error("初始化设备配置失败")
            return
        else:
            logger.info("初始化设备配置成功")

        """ 清空驱动缓存 """
        driverCache: DriverCache = DriverCache()
        driverCache.clean_driver()

        """ 设备任务管理器，先stop，在重启"""
        deviceTaskManager: DeviceTaskManager = DeviceTaskManager()
        deviceTaskManager.stop()
        if not deviceTaskManager.start():
            self.status = TaskStatus.FAIL
            self.message = "启动设备调用任务管理器失败"
            logger.error("启动设备调用任务管理器失败")
            return
        else:
            logger.info("启动设备调用任务管理器成功")

        """设备状态管理器，先stop，在重启"""
        deviceStatusManager: DeviceStatusManager = DeviceStatusManager()
        deviceStatusManager.stop()
        if not deviceStatusManager.start(dev_manager.get_cfgs_list()):
            self.status = TaskStatus.FAIL
            self.message = "启动设备状态管理器失败"
            logger.error("启动设备状态管理器失败")
            return
        else:
            logger.info("启动设备状态管理器成功")
        self.status = TaskStatus.SUCCESS
        self.message = "重启成功"

        data: dict = {}
        for item in device_cfg:
            data[item] = device_cfg[item][0]["devClassDesc"]
        msg = json.dumps({"state": "success", "function": "CfgChange", "data": data}, ensure_ascii=False)
        if Clients:
            for socket in Clients.values():
                send_socket_msg(socket, msg)
