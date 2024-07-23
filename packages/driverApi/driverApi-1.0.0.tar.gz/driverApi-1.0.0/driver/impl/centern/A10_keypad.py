# author: haoliqing
# date: 2023/9/5 15:43
# desc:
import ctypes
import platform
from ctypes import *

from common import get_absolute_path, global_constants
from device.device_config import DeviceConfig
from device.port import PortType
from driver.keypad import KeyPadInfo
from driver.multi_func_keypad import MultiFuncKeyPad
from logger.device_logger import logger
from device.status.device_status import DeviceStatus, DeviceStatusType


class A10Keypad(MultiFuncKeyPad):
    """A10密码键盘驱动实现类"""

    def __init__(self):
        super().__init__()

        self.port_id = None
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

    def init(self, device_cfg: DeviceConfig) -> int:
        super().init(device_cfg)
        try:
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
            self.dll_GWQ.GWQ_ResetKey(0, None, 1000)
        except Exception as e:
            logger.error(e)
            return -1
        return 0

    def read_pwd(self, flag: int) -> KeyPadInfo:
        logger.info("输入密码")
        iPinMode = 0  # 0-表示集中发送 1-表示即按即发
        outPwd = create_string_buffer(32)
        outPwdSize = 32  # 数组 Pin 的大小
        # 设置是否显示倒数计时
        self.setShowCountDown()
        read_status = self.dll_GWQ.GWQ_ReadPin(self.port_id, self.extendPort, self.baudRate, iPinMode, flag,
                                               self.outTime, outPwd,
                                               outPwdSize)
        info = KeyPadInfo()
        info.error_code = read_status
        if read_status == 0:
            info.data = outPwd.value.decode('utf-8')
        elif read_status == -2:
            info.error_code = -1
        elif read_status == -1:
            info.error_code = -2
        else:
            info.error_code = read_status
        return info

    def setShowCountDown(self, iPinDISP=1):
        self.dll_GWQ.GWQ_ReadPin(self.port_id, self.extendPort, self.baudRate, iPinDISP)

    def set_master_key(self, old_key: str, new_key: str) -> int:
        c_old_key = bytes(old_key, "utf-8")
        c_new_key = bytes(new_key, "utf-8")
        MKeyIndex = 1  # 主密钥号0~15
        status = self.dll_GWQ.GWQ_UpdateMKey(self.port_id, self.extendPort, self.baudRate, MKeyIndex, c_new_key,
                                             c_old_key)
        if status == -2:
            return -1
        elif status == -1:
            return -2
        return status

    def set_work_key(self, work_key) -> int:
        """下载工作密钥 并 激活"""
        MKeyIndex = 0  # 主密钥索引号：0~15
        WKeyIndex = 0  # 工作密钥索引号：0~15
        download_result = self.dll_GWQ.GWQ_DownLoadWKey(self.port_id, None, self.baudRate,
                                                        MKeyIndex, WKeyIndex, bytes(work_key, 'utf-8'))
        if download_result == 0:
            return self.dll_GWQ.GWQ_ActiveWKey(self.port_id, self.extendPort, self.baudRate, MKeyIndex, WKeyIndex)
        elif download_result == -2:
            return -1
        elif download_result == -1:
            return -2
        return download_result

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
        elif read_status == -2:
            info.error_code = -1
        elif read_status == -1:
            info.error_code = -2
        else:
            info.error_code = read_status
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
        elif read_status == -2:
            info.error_code = -1
        elif read_status == -1:
            info.error_code = -2
        else:
            info.error_code = read_status
        return info

    def open(self) -> int:
        super().open()
        return 0

    def cancel(self) -> int:
        return self.dll_GWQ.GWQ_CancelRead(self.port_id, self.extendPort, self.baudRate)

    def is_cancel(self) -> bool:
        return True

    def get_status(self) -> DeviceStatus:
        szDevice = ctypes.create_string_buffer(32)
        online_status = self.dll_GWQ.GWQ_CheckOnline(self.port_id, self.extendPort, self.baudRate, szDevice)
        status = super().get_status()
        if status.status_type == DeviceStatusType.DEV_READY:
            if online_status >= 0:
                return DeviceStatus(DeviceStatusType.DEV_READY, self.device_cfg)
            else:
                return DeviceStatus(DeviceStatusType.DEV_NOT_ONLINE, self.device_cfg)
        else:
            return super().get_status()


if __name__ == "__main__":
    keypad = A10Keypad()
    # i = keypad.init()
    # r = keypad.read_pwd(0)
    r = keypad.set_master_key("3838383838383838", "3131313131313131")  # false
    # r = keypad.set_work_key("3030303030303030")
    # print(r)
