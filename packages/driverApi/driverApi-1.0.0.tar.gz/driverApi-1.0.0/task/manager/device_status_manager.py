# author: haoliqing
# date: 2023/10/27 14:43
# desc:
import copy
import json
import time
from queue import Queue
from threading import Thread
from typing import List, Dict

import model.init_config as init_config
from common import Singleton
from common.common_utils import send_socket_msg
from device.device_config import DeviceConfig
from device.status.device_status import DeviceStatus, DeviceStatusType
from device.status.device_status_receiver import DeviceStatusReceiver, DeviceStatusListener
from logger.device_logger import logger
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.context.request_context_factory import RequestContextFactory
from task.manager.device_task_manager import DeviceTaskManager
from webservice.wsserver import Clients, lock


@Singleton
class DeviceStatusManager(object):
    status_cache: Dict[str, DeviceStatus] = {}
    device_task_manager = DeviceTaskManager()
    is_start = False

    def __init__(self):
        self.__status_receiver: DeviceStatusReceiver = DeviceStatusReceiver()
        self.__status_receiver.add_status_listener(InnerStatusListener(self))
        self.__push_status_queue = Queue(maxsize=10)  # 先进先出队列
        self.__dev_cfgs = None
        self.__collector = None
        self.__pushStatus = None

    def start(self, dev_cfgs: List[DeviceConfig]) -> bool:
        if self.is_start:
            logger.warn("设备状态查询任务管理器已启动，不再重复启动")
        self.__dev_cfgs = dev_cfgs
        for cfg in dev_cfgs:
            status: DeviceStatus = DeviceStatus(DeviceStatusType.DEV_UNKNOWN, cfg)
            self.status_cache[status.dev_class + "_" + status.dev_model] = status
        self.__collector = DeviceStatusCollector(dev_cfgs, self)
        self.__collector.start()
        if init_config.is_start_push():
            self.__pushStatus = DeviceStatusPush()
            self.__pushStatus.start()
        self.is_start = True
        return self.__collector.is_alive()

    def add_status(self, status: DeviceStatus):
        if not self.__push_status_queue.full():
            self.__push_status_queue.put(status)
        self.status_cache[status.dev_class + "_" + status.dev_model] = status
        # logger.info("更新设备状态：设备类型{0}， 设备型号{1}，状态{2}".format(status.dev_class, status.dev_model, status.status_type))

    def get_status(self, dev_class, dev_model) -> DeviceStatus:
        return self.status_cache.get(dev_class + "_" + dev_model, None)

    def get_all_status(self) -> List[DeviceStatus]:
        return self.status_cache.values()

    def get_push_status(self) -> DeviceStatus:
        """ 从队列中获取要推送的状态 """
        status = None
        if not self.__push_status_queue.empty():
            status = self.__push_status_queue.get()
        return status

    def stop(self) -> bool:
        self.is_start = False
        self.__dev_cfgs = None
        self.status_cache.clear()
        return self.__collector.cancel()


class DeviceStatusCollector(Thread):

    def __init__(self, dev_cfgs: List[DeviceConfig], status_manager: DeviceStatusManager):
        Thread.__init__(self)  # 调用父类初始化函数
        self.__run_flag = True
        self.__cfg_list = dev_cfgs
        self.__status_manager = status_manager

    def cancel(self) -> bool:
        self.__run_flag = False
        self.join()
        return True

    def run(self) -> None:
        while self.__run_flag:
            time.sleep(1)
            for cfg in self.__cfg_list:
                request_id = str(int(time.time() * 1000))  # 毫秒时间戳
                status = self.__status_manager.get_status(cfg.device_class, cfg.device_model)
                if status and status.is_valid():
                    # 状态未过期则不重复检查
                    continue
                request_data = json.loads('{"function" : "QueryStatus","type": "request", "param" :{}}')
                request_context: DeviceRequestContext = RequestContextFactory().get_request_context(request_id,
                                                                                                    request_data, None)
                request_context.set_device_cfg(cfg)
                # 内部的状态查询任务交给DeviceTaskManager执行，防止多个任务同时调用设备导致冲突
                self.__status_manager.device_task_manager.execute_inner_status_query(request_context)


class InnerStatusListener(DeviceStatusListener):

    def __init__(self, status_manager: DeviceStatusManager):
        self.__status_manager = status_manager

    def on_status_change(self, status: DeviceStatus):
        self.__status_manager.add_status(status)


class DeviceStatusPush(Thread):
    """ 定时（每隔5s）向客户端推送状态的线程 """

    def __init__(self):
        super().__init__()
        self.__device_status_manager: DeviceStatusManager = DeviceStatusManager()

    def run(self) -> None:
        while True:
            time.sleep(1)
            status = self.__device_status_manager.get_push_status()
            lock.acquire()
            try:
                if status and Clients:
                    statusInfo = copy.deepcopy(status)
                    statusInfo.status_type = statusInfo.status_type.value
                    msg = json.dumps(
                        {"state": "success", "function": "StateChange",
                         "data": {"status_type": statusInfo.status_type,
                                  "dev_class": statusInfo.dev_class,
                                  "dev_class_desc": statusInfo.dev_class_desc,
                                  "dev_model": statusInfo.dev_model,
                                  "dev_model_desc": statusInfo.dev_model_desc}}, ensure_ascii=False)

                    for socket in Clients.values():
                        send_socket_msg(socket, msg)
            finally:
                lock.release()
