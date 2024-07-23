# author: haoliqing
# date: 2023/9/22 14:22
# desc:
import json
import time
import traceback
from threading import Thread

from common import send_socket_msg
from model.task_model.system_task import SystemTask
from model.task_model.base_task import TaskStatus
import common.global_constants
from device.device_config_manager import DeviceConfigManager
import sys
from task.manager.device_task_manager import DeviceTaskManager
from task.manager.device_status_manager import DeviceStatusManager
from logger.device_logger import logger
from webservice.wsserver import Clients

isStarted = False


class SystemStartAction(SystemTask):

    def action(self):
        global isStarted
        if isStarted:
            self.status = TaskStatus.SUCCESS
        else:
            try:
                self.__start()
            except Exception as e:
                logger.error("启动外设框架时发生异常: {0}, 异常信息：{1}".format(str(e), traceback.format_exc()))
            finally:
                if not self.status == TaskStatus.SUCCESS:
                    isStarted = False
                else:
                    isStarted = True

    def __start(self):
        context = self.request_context
        device_cfg = context.request_data['deviceConfig']
        if len(device_cfg) == 0:
            self.status = TaskStatus.FAIL
            raise Exception("读取配置信息失败！")
        dev_manager: DeviceConfigManager = DeviceConfigManager()
        if not dev_manager.init_dev_cfg(device_cfg):
            self.status = TaskStatus.FAIL
            self.message = "初始化设备配置失败"
            logger.error("初始化设备配置失败")
            return
        else:
            logger.info("初始化设备配置成功")

        if not DeviceTaskManager().start():
            self.status = TaskStatus.FAIL
            self.message = "启动设备调用任务管理器失败"
            logger.error("启动设备调用任务管理器失败")
            return
        else:
            logger.info("启动设备调用任务管理器成功")

        if not DeviceStatusManager().start(dev_manager.get_cfgs_list()):
            self.status = TaskStatus.FAIL
            self.message = "启动设备状态管理器失败"
            logger.error("启动设备状态管理器失败")
            return
        else:
            logger.info("启动设备状态管理器成功")

        self.status = TaskStatus.SUCCESS
        self.message = "启动成功"

        device_config_push = DeviceConfigPush(device_cfg)
        device_config_push.start()


class DeviceConfigPush(Thread):
    """ 当检测到有新socket连接时，推送设备配置信息 """

    def __init__(self, device_config):
        super().__init__()
        self.device_config = device_config
        self.previous_state = dict(Clients)
        logger.info("socket连接检测已开启")

    def run(self) -> None:
        while True:
            time.sleep(1)
            if Clients != self.previous_state:
                data: dict = {}
                for item in self.device_config:
                    data[item] = self.device_config[item][0]["devClassDesc"]
                msg = json.dumps({"state": "success", "function": "CfgChange", "data": data}, ensure_ascii=False)
                self.previous_state = dict(Clients)
                for socket in Clients.values():
                    send_socket_msg(socket, msg)
