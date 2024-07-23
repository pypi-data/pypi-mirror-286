# author: haoliqing
# date: 2023/9/19 17:06
# desc:
import json
from tkinter import messagebox
from typing import List, Dict

import model.init_config as init_config
from common import common_utils, global_constants
from control.sparepart.abstract_sparepart import AbstractSparePart
from logger.device_logger import logger
from model.global_param_manager import GlobalParamManager
from service_adpter import TerminalInfoCallImpl
from service_adpter.system_start_call_server import SystemStartCallServer


class SystemStart(AbstractSparePart):
    """系统启动零配件"""

    global_param_manager: GlobalParamManager = GlobalParamManager()

    def __init__(self):

        self.dev_class: Dict[str, str] = {}
        """本地配置的设备类型列表"""

        self.dev_model: Dict = {}
        """本地配置的设备型号列表"""

        self.bind_info: List[Dict] = []
        """本地的设备配置"""

        self.dev_cfg: Dict[str, List[Dict]] = {}
        """设备配置数据"""

        self.systemStartCallServer: SystemStartCallServer = SystemStartCallServer()
        self.terminalInfoCall: TerminalInfoCallImpl = TerminalInfoCallImpl()

        if init_config.is_local_run():
            self.__load_local_dev_cls_cfg(common_utils.get_absolute_path('config/device_class_config.json'))
            self.__load_local_dev_cfg(common_utils.get_absolute_path('config/device_config.json'))
            self.__convert_data()

    def update(self, request_data):
        if init_config.is_local_run():
            request_data[global_constants.DEVICE_CONFIG] = self.dev_cfg
        else:
            mac_addr = self.terminalInfoCall.getMacAddr()
            # 获取不到mac地址
            if mac_addr is None:
                logger.error("查询本机mac地址失败，请检查配置！")
                messagebox.showerror("异常", "查询本机mac地址失败，请检查配置！")
                request_data[global_constants.DEVICE_CONFIG] = {}
            else:
                remote_cfg = self.systemStartCallServer.get_dev_cfg(mac_addr)
                request_data[global_constants.DEVICE_CONFIG] = remote_cfg

    def __load_local_dev_cfg(self, path):
        file_data = common_utils.read_file(path)
        dev_cfg: Dict = json.loads(file_data)
        dev_model_cfg = dev_cfg['device_models']
        for model in dev_model_cfg:
            self.dev_model[model['dev_id']] = model
        self.bind_info = dev_cfg['term_dev_cfg']

    def __load_local_dev_cls_cfg(self, path):
        file_data = common_utils.read_file(path)
        self.dev_class = json.loads(file_data)

    def __convert_data(self):
        for info in self.bind_info:
            dev_id = info['dev_id']
            model = self.dev_model.get(dev_id, None)
            if not model:
                logger.warn('本地设备配置中不存在ID为 %s 的设备型号' % dev_id)
            else:
                model_clss = model['dev_class'].split('|')
                for model_cls in model_clss:
                    cls = self.dev_class.get(model_cls, None)
                    if not cls:
                        logger.warn('本地设备配置中不存在ID为 %s 的设备类型定义' % model_cls)
                    else:
                        if not self.dev_cfg.get(model_cls, None):
                            self.dev_cfg[model_cls] = []
                        self.dev_cfg[model_cls].append(self.__build_dev_cfg_data(model_cls, model, info))

    def __build_dev_cfg_data(self, model_cls, model, bind_info):
        cfg_data = {}
        cfg_data[global_constants.TERM_ID] = bind_info.get('term_id', None)
        cfg_data[global_constants.DEV_STATUS] = bind_info.get('status', None)
        cfg_data[global_constants.DEV_CLASS_NAME] = model_cls
        cfg_data[global_constants.DEV_CLASS_DESC] = self.dev_class.get(model_cls, None)
        cfg_data[global_constants.DEV_MODEL_NAME] = model.get('dev_name', None)
        cfg_data[global_constants.DEV_MODEL_DESC] = model.get('dev_desc', None)
        port_cfg = {}
        port_cfg[global_constants.COMM_TYPE_NAME] = bind_info.get('port_type', None)
        port_cfg[global_constants.COMM_PORT] = bind_info.get('port', None)
        cfg_data[global_constants.PORT] = port_cfg
        return cfg_data


if __name__ == '__main__':
    sys_start: SystemStart = SystemStart()
    print('dev_class:', sys_start.dev_class)
    print('dev_model:', sys_start.dev_model)
    print('bind_info:', sys_start.bind_info)
    print('dev_config:', sys_start.dev_cfg)
