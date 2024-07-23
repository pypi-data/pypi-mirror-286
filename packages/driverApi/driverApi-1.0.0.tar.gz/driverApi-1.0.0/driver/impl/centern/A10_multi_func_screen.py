# author: haoliqing
# date: 2024/1/4 16:31
# desc:
import ctypes
import platform
from ctypes import c_int, byref

from common import *
from device.device_config import DeviceConfig
from device.port import PortType
from device.status import DeviceStatus
from device.status.device_status import DeviceStatusType
from driver.multi_func_screen import MultiFuncScreen, FileType, SignInfo
from logger.device_logger import logger


class A10MultiFuncScreen(MultiFuncScreen):
    """模拟多功能屏幕驱动实现类"""

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
            self.dll_GWQ = ctypes.CDLL(get_absolute_path("dll/A10/Linux/libcent_gwq.so"), mode=os.RTLD_LAZY)

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

    def show_tran_info(self, info: str, param: str) -> int:
        logger.info("收到的请求信息：info:{0}, param:{1}".format(info, param))
        read_status = self.dll_GWQ.GWQ_ShowInfo(self.port_id, self.extendPort, self.baudRate, self.outTime,
                                                bytes(info, "gbk"))
        return read_status

    def confirm_tran_info(self, info: str, param: str) -> int:
        logger.info("收到的请求信息：info:{0}, param:{1}".format(info, param))
        iDisplayResult = c_int(0)
        confirm_status = self.dll_GWQ.GWQ_StartInfo(self.port_id, self.extendPort, self.baudRate, self.outTime,
                                                    bytes(info, "gbk"), byref(iDisplayResult))
        if confirm_status == 0:
            if iDisplayResult.value == 0:
                return 0
            elif iDisplayResult.value == 1:
                return 1
            elif iDisplayResult.value == 3:
                return -1
        return iDisplayResult.value

    def request_sign(self, file_path: str, param: str) -> SignInfo:
        logger.info("收到的请求信息：file_path:{0}, param:{1}".format(file_path, param))
        sign_info = SignInfo()
        # 参数说明：设备连接端口 ,BP口 ,波特率 ,超时时间 ,电子凭证路径 ,签名图片本地保存路径 ,签名轨迹数据本地保存路径
        signPath = ""
        XmlPath = ""
        if platform.system() == "Windows":
            # 存储路径为 用户目录+deviceTemp+8位当前日期+文件名(时间戳).*
            signPath = get_save_pdir() + get_time_stamp() + ".png"
            XmlPath = get_save_pdir() + get_time_stamp() + ".xml"
        elif platform.system() == "Linux":
            # 存储路径为 /tmp/deviceTemp/8位当前日期/文件名(时间戳).*
            signPath = get_save_pdir_linux() + get_time_stamp() + ".png"
            XmlPath = get_save_pdir_linux() + get_time_stamp() + ".xml"
        sign_status = self.dll_GWQ.GWQ_StartSign(self.port_id, self.extendPort, self.baudRate, self.outTime,
                                                 bytes(file_path, "gbk"),
                                                 bytes(signPath, "gbk"),
                                                 bytes(XmlPath, "gbk"))
        print(sign_status)
        if sign_status == 0:
            sign_info.sign_data = read_file(XmlPath)  # 模拟签名轨迹数据
            sign_info.sign_image_base64 = image_to_base64(signPath)  # 签名base64数据
        elif sign_status == -2:
            # 超时
            sign_info.err_code = -1
        elif sign_status == -1:
            # 参数错误
            sign_info.err_code = -2
        elif sign_status == -7:
            # 取消操作
            sign_info.err_code = 1
        else:
            sign_info.err_code = sign_status
        return sign_info

    def confirm_sign(self, file_path: str, param: str) -> int:
        # TODO
        # logger.info("收到的请求信息：file_path:{0}, param:{1}".format(file_path, param))
        iDisplayResult = c_int(10)
        file_path = "D:\\hwBack.pdf"
        confirmFlag = 1  # 是否确认标志0 - 显示,1 - 确认
        port = 0
        extendPort = None
        iBaudRate = 9600
        outTime = 10
        read_status = self.dll_GWQ.GWQ_ShowPdfEx(port, extendPort, iBaudRate, outTime,
                                                 bytes(file_path, "gbk"), confirmFlag,
                                                 byref(iDisplayResult))
        print(read_status)
        if read_status == 0:
            return iDisplayResult.value
        return read_status

    def download_file(self, file_type: FileType, file_path: str) -> int:
        logger.info("收到的请求信息：file_path:{0}, file_type:{1}".format(file_path, file_type))
        fileType = file_type.value
        return self.dll_GWQ.GWQ_DownLoadFile(self.port_id, self.extendPort, self.baudRate, fileType,
                                             bytes(file_path, "gbk"))

    def delete_file(self, file_type: FileType, file_name: str) -> int:
        logger.info("收到的请求信息：file_name:{0}, file_type:{1}".format(file_name, file_type))
        fileType = file_type.value
        return self.dll_GWQ.GWQ_DeleteFile(self.port_id, self.extendPort, self.baudRate, fileType,
                                           bytes(file_name, "gbk"))

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

    def cancel(self) -> int:
        return self.dll_GWQ.GWQ_CancelRead(self.port_id, self.extendPort, self.baudRate)

    def is_cancel(self) -> bool:
        return True


if __name__ == '__main__':
    # A10MultiFuncScreen().request_sign("D://DeviceFile/Interface_GWQ_MUL_V1.0.0.2_B2018040801_TY(dll)/bin/hwBack.pdf",
    #                                   "")
    """
    linux 没有"展示信息"和"确认签署"函数
    """
    A10 = A10MultiFuncScreen()
    re = A10.confirm_sign(
        "D:\\DeviceFile\\柜外清\\Interface_GWQ_MUL_V1.0.0.2_B2018040801_TY(dll)（通用版）\\bin\\hwBack.pdf", None)
