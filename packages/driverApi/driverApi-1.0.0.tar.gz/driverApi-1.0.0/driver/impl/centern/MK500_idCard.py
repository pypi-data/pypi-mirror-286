import ctypes
import os.path
from ctypes import *

from common import global_constants
from common.common_utils import image_to_base64, get_absolute_path, get_save_pdir
from device.device_config import DeviceConfig
from device.port import PortType
from device.status import DeviceStatus
from device.status.device_status import DeviceStatusType
from driver.id_card_reader import IDCardReader, IDInfo
from logger.device_logger import logger


class PERSONINFO(Structure):
    _fields_ = [
        ('name', c_char * 80),
        ('EngName', c_char * 120),
        ('version', c_char * 10),
        ('govCode', c_char * 10),
        ('cardType', c_char * 10),
        ('otherData', c_char * 10),
        ('sex', c_char * 10),
        ('nation', c_char * 50),
        ('birthday', c_char * 30),
        ('address', c_char * 180),
        ('cardId', c_char * 50),
        ('police', c_char * 80),
        ('validStart', c_char * 30),
        ('validEnd', c_char * 30),
        ('sexCode', c_char * 10),
        ('nationCode', c_char * 10),
        ('appendMsg', c_char * 180),
        ('iFlag', c_int)
    ]

    def __str__(self):
        return f'name: {self.name.decode("gbk")}\n' \
               f'EngName: {self.EngName.decode("gbk")}\n' \
               f'version: {self.version.decode("gbk")}\n' \
               f'govCode: {self.govCode.decode("gbk")}\n' \
               f'cardType: {self.cardType.decode("gbk")}\n' \
               f'otherData: {self.otherData.decode("gbk")}\n' \
               f'sex: {self.sex.decode("gbk")}\n' \
               f'nation: {self.nation.decode("gbk")}\n' \
               f'birthday: {self.birthday.decode("gbk")}\n' \
               f'address: {self.address.decode("gbk")}\n' \
               f'cardId: {self.cardId.decode("gbk")}\n' \
               f'police: {self.police.decode("gbk")}\n' \
               f'validStart: {self.validStart.decode("gbk")}\n' \
               f'validEnd: {self.validEnd.decode("gbk")}\n' \
               f'sexCode: {self.sexCode.decode("gbk")}\n' \
               f'nationCode: {self.nationCode.decode("gbk")}\n' \
               f'appendMsg: {self.appendMsg.decode("gbk")}\n' \
               f'iFlag: {self.iFlag}'


class MK500IDCardReader(IDCardReader):
    """身份证阅读器适配器基类"""

    def __init__(self):
        super().__init__()
        self.port_id = b"HID"
        """ U 口取值为 HID，SDT,串口取值为 COM1,COM2,COM3。。。"""

        self.pszComNo = b"1001"

        self.baudRate = 9600
        """ 串口波特率，当为辅口或串口时有效。 """

        self.BpNo = None
        """ BP 口，取值为”A”、 ”B”、 ”C”、 ”K”分别为 A、B、C、K 口，取值 NULL 或””表示不连接 BP 口。"""

        self.outTime = 10
        """ 寻卡超时时间，单位为秒。"""

        self.device_cfg = None

        self.dll_IDCard = ctypes.WinDLL(get_absolute_path("dll/MK500/Windows/CENT_IDCard.dll"))

        self.dll_ICReader = ctypes.WinDLL(get_absolute_path("dll/MK500/Windows/CENT_Reader.dll"))

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
                self.pszComNo = b"1001"
            elif port_type == PortType.COM:
                self.port_id = bytes(device_cfg.port.port_id[3:], "gbk")
                self.pszComNo = bytes(device_cfg.port.port_id, "gbk")
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
        status, result, imagePath = self.read_card()
        if status == 0:
            id_info.cnName = result.name.decode("gbk")
            id_info.sex = result.sexCode.decode("gbk")
            id_info.nation = result.nationCode.decode("gbk")
            id_info.birthday = result.birthday.decode("gbk")
            id_info.address = result.address.decode("gbk")
            id_info.id = result.cardId.decode("gbk")
            id_info.dep = result.police.decode("gbk")
            id_info.begin = result.validStart.decode("gbk")
            id_info.end = result.validEnd.decode("gbk")
            id_info.image_path = imagePath
            id_info.image_info = image_to_base64(imagePath)
        elif status == -5:
            id_info.err_code = -1
        elif status == -1:
            id_info.err_code = -5
        else:
            id_info.err_code = status
        return id_info

    def saveHeadImg(self, imageType: int, saveDir: str, bMakeLogo: bool = False) -> str:
        """
        保存图片
        @param imageType: 图片类型：0—头像图片 1—正面图片 2—反面图片 3—完整图片（正反面）
        @param saveDir: 保存目录
        @param bMakeLogo: 是否制作 logo
        @return:
        """
        status, idCardInfo, imagePath = self.read_card()
        saveDir = create_string_buffer(bytes(saveDir, 'gbk'), 1024)
        if status < 0:
            return f"未检测到身份信息"
        save_status = self.dll_IDCard.CT_SaveImg(imageType, bMakeLogo, byref(idCardInfo), saveDir)
        logger.info(f"保存图片状态：{save_status}")
        if save_status < 0:
            return f"{save_status} 保存失败"
        saveImgPath = ""
        try:
            saveImgPath = saveDir.value.decode('gbk')
        except Exception as e:
            logger.error(e)
        return f"保存图片成功！\n 图片保存位置： \n {saveImgPath} "

    def read_card(self) -> ():
        """
        读取身份证信息
        @return: 读取状态，读取数据 , 头像保存路径
        """
        person_info = PERSONINFO()
        head_path = os.path.join(get_save_pdir(), "*.png")
        ImagePath = create_string_buffer(bytes(head_path, 'gbk'), 1024)
        read_status = self.dll_IDCard.CT_ReadIDCard(self.port_id, self.BpNo, self.baudRate, self.outTime, ImagePath,
                                                    byref(person_info))
        print(read_status)
        imagePath = ImagePath.value.decode("gbk")
        logger.info(f"读取二代身份证状态：{read_status}")
        return read_status, person_info, imagePath

    def open(self) -> int:
        super().open()
        return 0

    def close(self) -> int:
        super().close()
        return 0

    def is_cancel(self) -> bool:
        return True

    def cancel(self) -> int:
        """取消读取身份证"""
        return self.dll_IDCard.CT_CancelReadIDCard()

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


if __name__ == '__main__':
    # data = "None"
    idCard = MK500IDCardReader()
    # card = idCard.read()
    # data = idCard.saveHeadImg(3, "C:\\Users\\maosh\\deviceTemp\\20240329\\", bMakeLogo=True)
    data = idCard.get_status()
    print(data)
