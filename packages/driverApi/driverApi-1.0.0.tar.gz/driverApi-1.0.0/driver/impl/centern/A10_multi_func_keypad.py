import ctypes
import platform
from abc import ABCMeta
from ctypes import create_string_buffer, byref

from common import get_absolute_path, global_constants
from device.device_config import DeviceConfig
from device.port import PortType
from device.status import DeviceStatus
from device.status.device_status import DeviceStatusType
from driver.keypad import KeyPadInfo
from driver.multi_func_keypad import MultiFuncKeyPad
from logger.device_logger import logger


class A10MultiFuncKeyPad(MultiFuncKeyPad, metaclass=ABCMeta):
    """ A10多功能密码键盘驱动实现类 """

    def __init__(self):
        super().__init__()
        self.port_id = 0
        """ 端口号 0-USB,1-COM1,2-COM2……"""

        self.outTime = 30
        """ 等待超时时间 """

        self.baudRate = None
        """ 串口波特率，当为串口时有效 """

        self.extendPort = None
        """ BP 口 ,取值为”A”、 ”B”、 ”C”、 ”K”分别为 A、B、C、K 口,取值 NULL 或””表示不连接BP口"""

        self.dll_GWQ = None
        """ 柜外清驱动实例 """

        self.device_cfg = None

        if platform.system() == 'Windows':
            self.dll_GWQ = ctypes.WinDLL(get_absolute_path("dll/A10/Windows/CENT_GWQ.dll"))
        elif platform.system() == 'Linux':
            self.dll_GWQ = ctypes.CDLL(get_absolute_path("dll/A10/Linux/libcent_gwq.so"))

    def read_pwd(self, flag: int) -> KeyPadInfo:
        """ 由于继承关系，需重写方法，不做具体实现 """
        pass

    def set_master_key(self, old_key: str, new_key: str) -> int:
        """ 由于继承关系，需重写方法，不做具体实现 """
        pass

    def set_work_key(self, work_key: str) -> int:
        """ 由于继承关系，需重写方法，不做具体实现 """
        pass

    def init(self, device_cfg: DeviceConfig) -> int:
        super().init(device_cfg)
        self.device_cfg = device_cfg
        devParam = device_cfg.device_model_param
        if devParam:
            try:
                self.outTime = int(devParam.get(global_constants.OUT_TIME))
            except Exception as e:
                logger.error(e)
        port_type = device_cfg.port.get_port_type()
        if port_type == PortType.USB:
            self.port_id = 0
        elif port_type == PortType.COM:
            self.port_id = device_cfg.port.port_id[3:]
            self.baudRate = device_cfg.port.get_port_param("baudRate")
        return 0

    def read_tel_no(self) -> KeyPadInfo:
        logger.info("读取电话号码")
        info = KeyPadInfo()
        iDisplayResult = create_string_buffer(32)
        numType = 1  # 1-手机号
        read_status = self.dll_GWQ.GWQ_StartKeyboard(self.port_id, self.extendPort, self.baudRate,
                                                     self.outTime, numType, byref(iDisplayResult))
        info.error_code = read_status
        if read_status == 0:
            tel_no = iDisplayResult.value.decode("gbk")
            info.data = tel_no
        return info

    def read_auth_code(self) -> KeyPadInfo:
        info = KeyPadInfo()
        logger.info("读取验证码")
        iDisplayResult = create_string_buffer(32)
        numType = 5  # 1-验证码
        read_status = self.dll_GWQ.GWQ_StartKeyboard(self.port_id, self.extendPort, self.baudRate,
                                                     self.outTime, numType, byref(iDisplayResult))
        info.error_code = read_status
        if read_status == 0:
            auth_code = iDisplayResult.value.decode("gbk")
            info.data = auth_code
        return info

    # def get_status(self) -> DeviceStatus:
    #     szDevice = ctypes.create_string_buffer(32)
    #     online_status = self.dll_GWQ.GWQ_CheckOnline(self.port_id, self.extendPort, self.baudRate, szDevice)
    #     status = super().get_status()
    #     if status.status_type == DeviceStatusType.DEV_READY:
    #         if online_status >= 0:
    #             return DeviceStatus(DeviceStatusType.DEV_READY, self.device_cfg)
    #         else:
    #             return DeviceStatus(DeviceStatusType.DEV_NOT_ONLINE, self.device_cfg)
    #     else:
    #         return super().get_status()


if __name__ == '__main__':
    # TODO linux没有读取验证码
    fun = A10MultiFuncKeyPad()
    tel = fun.read_tel_no()
    print(tel.__dict__)
