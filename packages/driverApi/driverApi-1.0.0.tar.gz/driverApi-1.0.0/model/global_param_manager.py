# author: haoliqing
# date: 2023/8/29 14:36
# desc: 全局参数管理类
from common import Singleton
from typing import Dict
import json
from common import common_utils
from model.function.device_function import DeviceFunction
from model.function.system_function import SystemFunction
from model.function.function_config import FunctionConfig
from model.function.device_fucntion_next import DeviceFunctionNext
from logger.device_logger import logger

SUB_FILES = "sub_files"
FILE_NAME = "file_name"
FILE_DESC = "file_desc"


@Singleton
class GlobalParamManager(object):
    """全局参数管理器"""

    global_cfg: Dict = {}
    """全局参数配置"""

    device_func_cfgs: Dict[str, DeviceFunction] = {}
    """ 设备功能定义 {功能名称:功能定义}"""

    system_func_cfgs: Dict[str, SystemFunction] = {}
    """ 系统功能定义 {功能名称:功能定义} """

    func_class_cfgs: Dict[str, str] = {}
    """ 设备功能与设备类型关联关系 {功能名称:设备类型} """

    func_next_step_cfgs: Dict[str, DeviceFunctionNext] = {}
    """ 设备功能下一步操作定义 {功能名称:下一步配置}"""

    def __init__(self):
        # 公共配置放到 device_service.ini中
        # self.__load_global_cfg(common_utils.get_absolute_path('config/global_config.json'))
        self.__load_device_func_conf(common_utils.get_absolute_path('config/function/device_function.json'))
        self.__load_system_func_conf(common_utils.get_absolute_path('config/function/system_function.json'))
        self.__load_func_class_conf(common_utils.get_absolute_path('config/function_class/function_class.json'))
        self.__load_func_next_conf(common_utils.get_absolute_path('config/function_next/function_next_step.json'))

    def get_device_func_cfg(self, func_name: str) -> DeviceFunction:
        """根据功能名称获取设备功能定义"""
        return self.device_func_cfgs.get(func_name, None)

    def get_system_func_cfg(self, func_name: str) -> SystemFunction:
        """根据功能名称获取系统功能定义"""
        return self.system_func_cfgs.get(func_name, None)

    def get_func_class(self, func_name: str) -> str:
        """根据功能名称获取对应的设备类型"""
        return self.func_class_cfgs.get(func_name, None)

    def get_device_func_next(self, func_name: str) -> DeviceFunctionNext:
        """根据功能名称获取对应的下一步操作配置"""
        return self.func_next_step_cfgs.get(func_name, None)

    def __load_device_func_conf(self, path):
        """加载设备功能定义配置"""
        file_data = common_utils.read_file(path)
        device_func_cfg: dict = json.loads(file_data)
        subfiles: list = device_func_cfg.get(SUB_FILES, None)
        if subfiles:
            for f in subfiles:
                self.__load_device_func_conf(common_utils.get_absolute_path(f[FILE_NAME]))
                logger.info("加载配置文件" + f[FILE_DESC])

        functions: list = device_func_cfg.get(FunctionConfig.FUNCS_NODE, None)
        if functions:
            for func in functions:
                self.device_func_cfgs[func[FunctionConfig.FUNC_NODE_NAME]] = DeviceFunction(func)

    def __load_system_func_conf(self, path):
        """加载系统功能定义配置"""
        file_data = common_utils.read_file(path)
        sys_func_cfg: dict = json.loads(file_data)
        subfiles: list = sys_func_cfg.get(SUB_FILES, None)
        if subfiles:
            for f in subfiles:
                self.__load_system_func_conf(common_utils.get_absolute_path(f[FILE_NAME]))
                logger.info("加载配置文件" + f[FILE_DESC])

        functions: list = sys_func_cfg.get(FunctionConfig.FUNCS_NODE, None)
        if functions:
            for func in functions:
                self.system_func_cfgs[func[FunctionConfig.FUNC_NODE_NAME]] = SystemFunction(func)

    def __load_func_class_conf(self, path):
        """加载设备功能与设备类型对应关系"""
        file_data = common_utils.read_file(path)
        func_class_cfg: dict = json.loads(file_data)
        subfiles: list = func_class_cfg.get(SUB_FILES, None)
        if subfiles:
            for f in subfiles:
                self.__load_func_class_conf(common_utils.get_absolute_path(f[FILE_NAME]))
                logger.info("加载配置文件" + f[FILE_DESC])

        functions: list = func_class_cfg.get('functions', None)
        if functions:
            for func in functions:
                self.func_class_cfgs[func['name']] = func['class']

    def __load_func_next_conf(self, path):
        """加载设备功能下一步操作配置"""
        file_data = common_utils.read_file(path)
        func_next_cfg: dict = json.loads(file_data)
        functions: list = func_next_cfg.get('functions', None)
        if functions:
            for func in functions:
                self.func_next_step_cfgs[func['name']] = DeviceFunctionNext(func)

    def __load_global_cfg(self, path):
        file_data = common_utils.read_file(path)
        self.global_cfg = json.loads(file_data)


"""
if __name__ == '__main__':
    manager: GlobalParamManager = GlobalParamManager()
    print(manager.device_func_cfgs)
    print(manager.system_func_cfgs)
    print(manager.func_class_cfgs)
    print(manager.func_next_step_cfgs)
"""





