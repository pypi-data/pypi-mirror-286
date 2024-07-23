# author: haoliqing
# date: 2023/9/5 9:40
# desc:
import os
import platform

from common import Singleton
from device.base_device import Device
from device.device_config import DeviceConfig
from driver.impl import *
from logger.device_logger import logger
import importlib


@Singleton
class DriverFactory(object):
    """设备驱动工厂"""

    KEYPAD = 'Keypad'  # 数字键盘
    MAGNET_IC = 'MagnetIC'  # 磁条读写器
    FINGER = 'FingerScanner'  # 指纹仪
    PBOCICCard = 'PBOCICCard'  # IC卡
    ID_CARD = 'IDCard'  # 身份证识别器
    QR_CODE = 'QRCode'  # 二维码扫描仪
    PRINTER = 'Printer'  # 针式打印机
    LASER_PRINTER = 'LaserPrinter'  # 激光打印机
    JOURNAL_PRINTER = 'JournalPrinter'  # 流水打印机
    EVALUATOR = 'Evaluator'  # 评价器
    MULTI_FUNC_SCREEN = 'MultiFuncScreen'  # 多功能屏幕

    def __init__(self):
        pass
        # 导入外部文件
        # module_path = os.path.join(os.getcwd(), 'mock_keypad.py')
        # self.mock_keypad_module = importlib.import_module('mock_keypad', module_path)

    def get_device(self, device_cfg: DeviceConfig) -> Device:
        """根据设备配置获取设备驱动"""
        device_class: str = device_cfg.device_class
        device_model: str = device_cfg.device_model
        device = None
        if device_class == self.KEYPAD:
            device = self.get_keypad_driver(device_model)
        elif device_class == self.MAGNET_IC:
            device = self.get_magnet_ic_driver(device_model)
        elif device_class == self.ID_CARD:
            device = self.get_id_card_driver(device_model)
        elif device_class == self.PBOCICCard:
            device = self.get_pboc_ic_driver(device_model)
        elif device_class == self.EVALUATOR:
            device = self.get_evaluator_driver(device_model)
        elif device_class == self.FINGER:
            device = self.get_finger_scanner_driver(device_model)
        elif device_class == self.MULTI_FUNC_SCREEN:
            device = self.get_multi_func_screen_driver(device_model)
        elif device_class == self.LASER_PRINTER:
            device = self.get_laser_printer_driver(device_model)
        else:
            logger.error("不支持的设备类型{0}".format(device_class))
        return device

    def get_keypad_driver(self, device_model: str) -> Device:
        """获取数字键盘驱动"""
        device = None
        if device_model == 'MockKeypad':
            device = MockKeypad()
        elif device_model == 'CenternA10':
            device = A10Keypad()
        else:
            logger.error("未获取到型号为{0}的{1}驱动".format(device_model, self.KEYPAD))
        return device

    def get_magnet_ic_driver(self, device_model: str) -> Device:
        """获取磁条卡刷卡器驱动"""
        device = None
        if device_model == 'MockMagnetic':
            device = MockMagnetIC()
        elif device_model == 'CenternMK500':
            if platform.system() == 'Windows':
                device = MK500MagnetIC()
            elif platform.system() == 'Linux':
                device = MK500MagnetICLinux()
        else:
            logger.error("未获取到型号为{0}的{1}驱动".format(device_model, self.MAGNET_IC))
        return device

    def get_id_card_driver(self, device_model: str) -> Device:
        """获取身份证阅读器驱动"""
        device = None
        if device_model == 'MockIDCard':
            device = MockIDCardReader()
        elif device_model == 'CenternMK500':
            if platform.system() == 'Windows':
                device = MK500IDCardReader()
            elif platform.system() == 'Linux':
                device = MK500IDCardReaderLinux()
        else:
            logger.error("未获取到型号为{0}的{1}驱动".format(device_model, self.ID_CARD))
        return device

    def get_pboc_ic_driver(self, device_model: str) -> Device:
        """获取金融IC卡驱动"""
        device = None
        if device_model == 'MockICCard':
            device = MockFinanceIcCard()
        elif device_model == 'CenternMK500':
            if platform.system() == 'Windows':
                device = MK500FinanceIcCard()
            elif platform.system() == 'Linux':
                device = MK500FinanceIcCardLinux()
        else:
            logger.error("未获取到型号为{0}的{1}驱动".format(device_model, self.PBOCICCard))
        return device

    def get_evaluator_driver(self, device_model: str) -> Device:
        """获取评价器驱动"""
        device = None
        if device_model == 'MockEvaluator':
            device = MockEvaluator()
        elif device_model == 'CenternA10':
            device = A10Evaluator()
        else:
            logger.error("未获取到型号为{0}的{1}驱动".format(device_model, self.EVALUATOR))
        return device

    def get_finger_scanner_driver(self, device_model: str) -> Device:
        """获取指纹仪驱动"""
        device = None
        if device_model == 'MockFingerScanner':
            device = MockFingerScanner()
        elif device_model == 'CenternMK500':
            if platform.system() == 'Windows':
                device = MK500FingerScanner()
            elif platform.system() == 'Linux':
                pass  # TODO
        else:
            logger.error("未获取到型号为{0}的{1}驱动".format(device_model, self.FINGER))
        return device

    def get_multi_func_screen_driver(self, device_model: str) -> Device:
        """获取多功能屏幕驱动"""
        device = None
        if device_model == 'MockMultiFuncScreen':
            device = MockMultiFuncScreen()
        elif device_model == 'CenternA10':
            device = A10MultiFuncScreen()
        else:
            logger.error("未获取到型号为{0}的{1}驱动".format(device_model, self.MULTI_FUNC_SCREEN))
        return device

    def get_laser_printer_driver(self, device_model: str) -> Device:
        """获取激光打印机驱动"""
        device = None
        if platform.system() == 'Windows':
            device = WindowsPrinter()
        elif platform.system() == 'Linux':
            device = LinuxPrinter()
        else:
            logger.error("未获取到型号为{0}的{1}驱动".format(device_model, self.LASER_PRINTER))
        return device
