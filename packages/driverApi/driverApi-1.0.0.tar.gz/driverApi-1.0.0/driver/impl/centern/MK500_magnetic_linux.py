# author: haoliqing
# date: 2023/9/5 16:21
# desc:
import ctypes
from ctypes import *

from common import get_absolute_path, global_constants
from device.device_config import DeviceConfig
from device.port import PortType
from driver.magnetic_strip_rwer import MagneticStripRWer, MagneticStripInfo
from logger.device_logger import logger


class MK500MagnetICLinux(MagneticStripRWer):
    """升腾磁条读写器驱动实现类"""

    def __init__(self):
        super().__init__()

        self.port_id = b"HID"

        self.outTime = 30

        self.device_cfg = None

        self.baudRate = 9600

        self.dll_MagCard = ctypes.CDLL(get_absolute_path("dll/MK500/Linux/TY_MSG_Linux.so"))

    def init(self, device_cfg: DeviceConfig) -> int:
        super().init(device_cfg)
        try:
            self.device_cfg = device_cfg
            devParam = device_cfg.device_model_param
            if devParam:
                try:
                    # 避免类型转换异常
                    self.outTime = int(devParam.get(global_constants.OUT_TIME))
                except Exception as e:
                    logger.error(e)
            port_type = device_cfg.port.get_port_type()
            if port_type == PortType.USB:
                self.port_id = b"HID"
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
        """ 连接端口 ,波特率, 磁道格式(0:ISO，1:IBM), 寻卡超时时间, szTrack1取值, szTrack1长度,...... """
        nCharset = 0  # 0-ISO 1-IBM 默认0
        read_status = self.dll_MagCard.Linux_CT_ReadMsgCard(self.port_id, self.baudRate, nCharset, self.outTime,
                                                            szTrack1, 512,
                                                            szTrack2, 512,
                                                            szTrack3, 512)
        msInfo = MagneticStripInfo()
        if read_status == 0:
            msInfo.stack1_info = szTrack1.value.decode("gbk")
            szTrack2Val: str = szTrack2.value.decode("gbk")
            msInfo.card_no = szTrack2Val.split("=")[0]
            msInfo.stack2_info = szTrack2Val
            msInfo.stack3_info = szTrack3.value.decode("gbk")

        return msInfo

    def write(self, stack1_info: str, stack2_info: str, stack3_info: str) -> int:
        szTrack1 = None
        szTrack2 = None
        szTrack3 = None
        nCharset = 0  # 0-ISO 1-IBM 默认0
        if stack1_info:
            szTrack1 = bytes(stack1_info, "utf-8")
        if stack2_info:
            szTrack2 = bytes(stack2_info, "utf-8")
        if stack3_info:
            szTrack3 = bytes(stack3_info, "utf-8")
        return self.dll_MagCard.Linux_CT_WriteMsgCard(self.port_id, self.baudRate, nCharset, self.outTime,
                                                      szTrack1, szTrack2, szTrack3)

    def open(self) -> int:
        super().open()
        return 0

    def close(self) -> int:
        super().close()
        return 0

    def is_cancel(self) -> bool:
        return False


if __name__ == '__main__':
    ic = MK500MagnetICLinux()
    data = ic.read()
    print(data)
