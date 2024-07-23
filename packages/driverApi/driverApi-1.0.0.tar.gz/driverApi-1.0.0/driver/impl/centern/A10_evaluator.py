# author: haoliqing
# date: 2024/1/4 16:26
# desc:
import ctypes
from ctypes import c_int, byref
import platform

from common import get_absolute_path, global_constants
from device.device_config import DeviceConfig
from device.port import PortType
from device.status import DeviceStatus
from device.status.device_status import DeviceStatusType
from driver.evaluator import Evaluator, EvaluateInfo
from logger.device_logger import logger


class A10Evaluator(Evaluator):
    """A10评价器驱动实现类"""

    def __init__(self):
        super().__init__()
        self.port_id = None
        """ 端口号 0-USB,1-COM1,2-COM2……"""

        self.outTime = 30
        """ 等待超时时间 """

        self.baudRate = 9600
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
        except Exception as e:
            logger.error(e)
            return -1
        return 0

    def get_evaluate_result(self, teller_id: str, teller_name: str, teller_photo: str, star_level: int) -> EvaluateInfo:
        logger.info("收到的请求信息：teller_id:{0}, teller_name:{1}, teller_photo:{2}, star_level:{3}"
                    .format(teller_id, teller_name, teller_photo, star_level))
        eva_info = EvaluateInfo()
        evalValue = c_int(0)
        evaluator_status = self.dll_GWQ.GWQ_StartEvaluator(self.port_id, self.baudRate, self.baudRate,
                                                           bytes(teller_name, "gbk"),
                                                           bytes(teller_id, "gbk"), star_level,
                                                           bytes(teller_photo, "gbk"),
                                                           self.outTime,
                                                           byref(evalValue))
        print(evaluator_status)
        print(evalValue.value)
        if evaluator_status == 0:
            eva_info.level = evalValue.value
            match evalValue.value:
                case 1:
                    eva_info.message = '满意'
                case 2:
                    eva_info.message = '一般'
                case 3:
                    eva_info.message = '不满意'
                case 4:
                    eva_info.err_code = -1
        else:  # 4-等待超时，返回-1
            eva_info.err_code = evaluator_status
        return eva_info

    def update_teller_photo(self, file_path: str) -> int:
        logger.info("收到的请求信息：file_path:{0}".format(file_path))
        imgType = 2  # 0-广告图片，1-视频文件，2-柜员头像，3-语音文件，4-升级包
        return self.dll_GWQ.GWQ_DownLoadFile(self.port_id, self.baudRate, self.baudRate, imgType,
                                             bytes(file_path, "gbk"))

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

    def is_cancel(self) -> bool:
        return True

    def cancel(self) -> int:
        return self.dll_GWQ.GWQ_CancelRead(self.port_id, self.extendPort, self.baudRate)


if __name__ == '__main__':
    eval = A10Evaluator()
    # result = eval.get_evaluate_result("100001", "王五", "photo.jpg", 5)
    # result = eval.update_teller_photo("/home/msm/Desktop/photo.png")
    eval.get_status()
    # print(result)
