import ctypes
from ctypes import *
from typing import List

from common import get_absolute_path
from device.device_config import DeviceConfig
from device.port import PortType
from device.status import DeviceStatus
from device.status.device_status import DeviceStatusType
from driver.finger_scanner import FingerScanner, TemplatesInfo
from logger.device_logger import logger


class MK500FingerScanner(FingerScanner):

    def __init__(self):
        super().__init__()

        self.nPort: int = 0

        self.pszComNo = b"1001"

        self.device_cfg = None

        self.dll_FingerScanner = ctypes.WinDLL(get_absolute_path("dll/MK500/Windows/TesoLive.dll"))
        """ 加载读IC卡驱动为了判断设备在线状态 """
        self.dll_ICReader = ctypes.WinDLL(get_absolute_path("dll/MK500/Windows/CENT_Reader.dll"))

    def init(self, device_cfg: DeviceConfig) -> int:
        super().init(device_cfg)
        try:
            self.device_cfg = device_cfg
            port_type = device_cfg.port.get_port_type()
            if port_type == PortType.USB:
                self.nPort = 0
                self.pszComNo = b"1001"
            elif port_type == PortType.COM:
                self.nPort = device_cfg.port.port_id[3:]
                self.pszComNo = bytes(device_cfg.port.port_id, "gbk")
        except Exception as e:
            logger.error(e)
            return -1
        return 0

    def get_finger_template(self, finger_num: int) -> TemplatesInfo:
        info = TemplatesInfo()
        template_list: [str] = []
        while len(template_list) < finger_num:
            template = create_string_buffer(513)
            data_len = c_int(1000)
            error_msg = create_string_buffer(64)
            read_status = self.dll_FingerScanner.FPIGetTemplate(self.nPort, template, byref(data_len), error_msg)
            info.error_code = read_status
            print("error_code:", read_status)
            if read_status >= 0:
                template = template.value.decode("gbk")
                template_list.append(template)
            elif read_status == -17:
                break
        info.data = template_list
        return info

    def get_finger_feature(self) -> str:
        feature = create_string_buffer(513)
        data_len = c_int(1000)
        error_msg = create_string_buffer(64)
        read_status = self.dll_FingerScanner.FPIGetFeature(self.nPort, feature, byref(data_len), error_msg)
        if read_status >= 0:  # -17 取消操作    -13 超时操作
            return feature.value.decode("gbk")
        return ""

    def verify_finger(self, template_list: List[str]) -> int:
        finger_feature = self.get_finger_feature()
        result = -1
        for finger_template in template_list:
            verify_result = self.dll_FingerScanner.FPIMatch(bytes(finger_template, "gbk"), bytes(finger_feature, "gbk"),
                                                            3)
            if verify_result >= 0:
                return verify_result
            else:
                result = verify_result
        return result

    def get_status(self) -> DeviceStatus | None:
        online_status = self.dll_ICReader.CT_ChkDevPresent(self.pszComNo, b"")
        status = super().get_status()
        if status.status_type == DeviceStatusType.DEV_READY:
            if online_status >= 0:
                return DeviceStatus(DeviceStatusType.DEV_READY, self.device_cfg)
            else:
                return DeviceStatus(DeviceStatusType.DEV_NOT_ONLINE, self.device_cfg)
        else:
            return super().get_status()

    def is_cancel(self) -> bool:
        return False


if __name__ == '__main__':
    scanner = MK500FingerScanner()
    feature = scanner.get_status()
    print(feature)
