import ctypes
import json
import shutil
import os

from common import global_constants
from device.device_config import DeviceConfig
from device.port import PortType
from driver.id_card_reader import IDCardReader, IDInfo
from common.common_utils import image_to_base64, get_absolute_path, get_save_pdir_linux
from common.global_constants import BASE64_PREFIX
from ctypes import *

from logger.device_logger import logger


class MK500IDCardReaderLinux(IDCardReader):
    """身份证阅读器适配器基类"""

    def __init__(self):
        super().__init__()
        self.szDevice = b"HID"

        self.outTime = 30

        self.device_cfg = None

        self.baudRate = 9600

        self.dll_IDCard = ctypes.CDLL(get_absolute_path("dll/MK500/Linux/TY_IDC_Linux.so"))

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
                self.szDevice = b"HID"
            elif port_type == PortType.COM:
                self.szDevice = bytes(device_cfg.port.port_id[3:], "gbk")
                self.baudRate = device_cfg.port.get_port_param("baudRate")
        except Exception as e:
            logger.error(e)
            return -1
        return 0

    def read(self) -> IDInfo:
        """
        读取二代证信息
        :return: 读取到的二代证信息，若返回值为None，则获取失败，否则读卡的成功与失败由IDInfo.errorCode来决定，
        若该值小于0，则认为读卡失败，否则为读卡成功，该值需要在驱动实现中自行设置，默认为0
        """
        id_info = IDInfo()
        result: dict = self.read_card()
        status = result.get("status")
        if status < 0:
            id_info.err_code = status
            return id_info
        else:
            idCardInfo = result.get("idCardInfo")
            result_obj = json.loads(idCardInfo)
            id_info.cnName = result_obj["ChinaName"]
            id_info.sex = result_obj["Sex"]
            id_info.nation = result_obj["NationCode"]
            id_info.birthday = result_obj["Birth"]
            id_info.address = result_obj["Address"]
            id_info.id = result_obj["IDNumber"]
            id_info.dep = result_obj["Signatory"]
            id_info.begin = result_obj["CardActivityStart"]
            id_info.end = result_obj["CardActivityExp"]
            id_info.image_path = result.get("headImgSaveAbsPath")
            id_info.image_info = image_to_base64(id_info.image_path)
        return id_info

    def read_card(self) -> dict:
        """
        读取身份证信息
        @return: 读取状态，读取数据 , 头像保存路径
        """
        self.dll_IDCard.Linux_CT_ID_ReadCollectCardInfo.argtypes = [ctypes.c_char_p, ctypes.c_long, ctypes.c_long,
                                                                    ctypes.c_int,
                                                                    ctypes.c_char_p, ctypes.c_char_p]

        self.dll_IDCard.Linux_CT_ID_ReadCollectCardInfo.restype = ctypes.c_long

        szHeadDirs = create_string_buffer(bytes("./*.bmp", 'gbk'), 1024)
        person_info = create_string_buffer(2048)
        nType = 0  # 0-读取二代身份证（不带指纹信息） 1-读取三带身份证（带指纹信息）
        read_status = self.dll_IDCard.Linux_CT_ID_ReadCollectCardInfo(self.szDevice, self.baudRate, self.outTime, nType,
                                                                      szHeadDirs,
                                                                      person_info)

        logger.info(f"读取二代身份证状态：{read_status}")
        ret = {"status": read_status}
        if read_status >= 0:
            # 获取身份证号
            person_info = person_info.value.decode("utf-8")
            ret["idCardInfo"] = person_info
            idCardNum = json.loads(person_info)["IDNumber"]
            ret["idCardNum"] = idCardNum
            # 构建相对路径
            relativePath = f"./{idCardNum}-head.bmp"
            ret["relativePath"] = relativePath
            # 将保存的头像图片剪切到 /tmp/deviceTemp/当前日期8位数字/ 目录
            try:
                headImgSaveAbsPath = os.path.join(get_save_pdir_linux(), relativePath)
                if os.path.exists(headImgSaveAbsPath):
                    os.remove(headImgSaveAbsPath)
                shutil.move(relativePath, get_save_pdir_linux())
                ret["headImgSaveAbsPath"] = headImgSaveAbsPath
            except shutil.Error as e:
                # 如果移动失败，则
                logger.error(f"保存头像异常:{e}")
            return ret
        return ret

    def saveHeadImg(self, imageType: int, saveDir: str, szLogoInfo: str = "") -> str:
        """
        保存图片
        @param imageType: 图片类型：1—正面 2—反面 4—正反竖排 5—正反横排
        @param saveDir: 保存目录
        @param szLogoInfo: 是否制作 logo
        @return:
        """
        result = self.read_card()
        szHeadDir = bytes(result.get("headImgSaveAbsPath"), "gbk")  # 头像图片保存路径
        if result.get("status") >= 0:
            idCardNum = result.get("idCardNum")
            fileName = ""
            if imageType == 1:
                fileName = idCardNum + '-front.bmp'
            elif imageType == 2:
                fileName = idCardNum + '-back.bmp'
            elif imageType == 4:
                fileName = idCardNum + '-vert.bmp'
            elif imageType == 5:
                fileName = idCardNum + '-hori.bmp'
            savePath = os.path.join(saveDir, fileName)
            szImgDir = bytes(savePath, 'gbk')  # 合成图片输出路径
            idCardInfo = bytes(result.get("idCardInfo"), "utf-8")
            save_status = self.dll_IDCard.Linux_CT_ID_SaveCollectCardImg(imageType, szHeadDir, idCardInfo,
                                                                         bytes(szLogoInfo, "gbk"),
                                                                         szImgDir)
            logger.info(f"身份证图片保存状态：{save_status}")
            if save_status < 0:
                return f"{save_status}：保存失败"
            else:
                return f"保存图片成功!\n图片保存位置:\t{savePath} "
        return "读取身份证信息失败！"

    def cancelRead(self):
        """取消读取身份证"""
        self.dll_IDCard.CT_CancelReadIDCard()

    def open(self) -> int:
        super().open()
        return 0

    def close(self) -> int:
        super().close()
        return 0

    def is_cancel(self) -> bool:
        return False


if __name__ == '__main__':
    # data = "None"
    idCard = MK500IDCardReaderLinux()
    # data = idCard.read()
    data = idCard.saveHeadImg(5, os.path.join(get_save_pdir_linux(), "*.bmp"), "")
    # data = idCard.saveHeadImg(2, getSavePDirLinux(), "中电金信")
    # data = idCard.read()
    print(data)
