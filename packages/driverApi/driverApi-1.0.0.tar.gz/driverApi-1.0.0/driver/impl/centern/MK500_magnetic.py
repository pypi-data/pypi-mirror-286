# author: haoliqing
# date: 2023/9/5 16:21
# desc:
import ctypes
from ctypes import *

from common import get_absolute_path, global_constants
from device.device_config import DeviceConfig
from device.port import PortType
from device.status import DeviceStatus
from device.status.device_status import DeviceStatusType
from driver.magnetic_strip_rwer import MagneticStripRWer, MagneticStripInfo
from logger.device_logger import logger


class MK500MagnetIC(MagneticStripRWer):
    """升腾磁条读写器驱动实现类"""

    def __init__(self):
        super().__init__()
        self.port_id = b"HID"
        """ U 口取值为 HID，SDT,串口取值为 COM1,COM2,COM3。。。"""

        self.pszComNo = b"1001"

        self.baudRate = None
        """ 串口波特率，当为辅口或串口时有效。 """

        self.BpNo = None
        """ BP 口，取值为”A”、 ”B”、 ”C”、 ”K”分别为 A、B、C、K 口，取值 NULL 或””表示不连接 BP 口。"""

        self.outTime = 10
        """ 寻卡超时时间，单位为秒。"""

        self.device_cfg = None

        self.dll_MagCard = ctypes.WinDLL(get_absolute_path("dll/MK500/Windows/CENT_MsgCard.dll"))

        self.dll_ICReader = ctypes.WinDLL(get_absolute_path("dll/MK500/Windows/CENT_Reader.dll"))

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
                self.port_id = b"HID"
                self.pszComNo = b"1001"
            elif port_type == PortType.COM:
                self.port_id = bytes(device_cfg.port.port_id, "gbk")
                self.baudRate = device_cfg.port.get_port_param("baudRate")
        except Exception as e:
            logger.error(e)
            return -1
        return 0

    def read(self) -> MagneticStripInfo:
        szTrack1 = create_string_buffer(1024)
        szTrack2 = create_string_buffer(1024)
        szTrack3 = create_string_buffer(1024)
        nCharset = 0  # 0-ISO 格式，1-IBM 格式, 2-ISO 格式(德卡)，3-IBM 格式(德卡)
        """ 连接端口 ,波特率, BP 口, 磁道格式, 寻卡超时时间, szTrack1取值, szTrack1长度,...... """
        read_status = self.dll_MagCard.CT_ReadMsgCard(self.port_id, self.baudRate, self.BpNo, nCharset, self.outTime,
                                                      szTrack1, 79,
                                                      szTrack2, 40,
                                                      szTrack3, 107)
        msInfo = MagneticStripInfo()
        if read_status == 0:
            msInfo.stack1_info = szTrack1.value.decode("gbk")
            szTrack2Val: str = szTrack2.value.decode("gbk")
            msInfo.card_no = szTrack2Val.split("=")[0]
            msInfo.stack2_info = szTrack2Val
            msInfo.stack3_info = szTrack3.value.decode("gbk")
        elif read_status == -8:
            msInfo.err_code = -1
        elif read_status == -1:
            msInfo.err_code = -8
        else:
            msInfo.err_code = read_status
        return msInfo

    def write(self, stack1_info: str, stack2_info: str, stack3_info: str) -> int:
        szTrack1 = None
        szTrack2 = None
        szTrack3 = None
        if stack1_info:
            szTrack1 = bytes(stack1_info, "utf-8")
        if stack2_info:
            szTrack2 = bytes(stack2_info, "utf-8")
        if stack3_info:
            szTrack3 = bytes(stack3_info, "utf-8")
        nCharset = 0  # 0-ISO 格式，1-IBM 格式, 2-ISO 格式(德卡)，3-IBM 格式(德卡)
        return self.dll_MagCard.CT_WriteMsgCard(self.port_id, self.baudRate, self.BpNo, nCharset, self.outTime,
                                                szTrack1, szTrack2, szTrack3)

    def open(self) -> int:
        super().open()
        return 0

    def close(self) -> int:
        super().close()
        return 0

    def get_status(self) -> DeviceStatus | None:
        online_status = self.dll_ICReader.CT_ChkDevPresent(self.pszComNo, self.BpNo)
        status = super().get_status()
        if status.status_type == DeviceStatusType.DEV_READY:
            if online_status >= 0:
                return DeviceStatus(DeviceStatusType.DEV_READY, self.device_cfg)
            else:
                return DeviceStatus(DeviceStatusType.DEV_NOT_ONLINE, self.device_cfg)
        else:
            return super().get_status()

    def is_cancel(self) -> bool:
        return True

    def cancel(self) -> int:
        return self.dll_MagCard.CT_CancelReadMsgCard()


if __name__ == '__main__':
    ic = MK500MagnetIC()
    # data = ic.read()
    ic.get_status()
    # print(data)
