# author: haoliqing
# date: 2023/9/5 15:43
# desc:

from PySide2.QtCore import QEventLoop

from common import Singleton
from device.device_config import DeviceConfig
from driver.keypad import KeyPadInfo
from driver.multi_func_keypad import MultiFuncKeyPad
from logger.device_logger import logger
from view.signal.read_signal import ReadSignal


@Singleton
class MockKeypad(MultiFuncKeyPad):
    """模拟密码键盘驱动实现类"""
    signal = ReadSignal()
    data = None

    def init(self, device_cfg: DeviceConfig) -> int:
        super().init(device_cfg)
        return 0

    def read_pwd(self, flag: int) -> KeyPadInfo:
        """TODO 弹出模拟外设输入界面，输入密码并返回"""
        logger.info("输入密码")
        keyPadInfo = KeyPadInfo()
        if flag == 0:
            self.signal.keypad_read_signal.emit("请输入密码")
        else:
            self.signal.keypad_read_signal.emit("请确认密码")
        self.event_loop = QEventLoop()
        self.event_loop.exec_()
        keyPadInfo.data = self.data
        return keyPadInfo

    def read_finished(self, password):
        if self.event_loop and self.event_loop.isRunning():
            self.event_loop.quit()
        self.data = password

    def set_master_key(self, old_key: str, new_key: str) -> int:
        return 0

    def set_work_key(self, work_key: str) -> int:
        return 0

    def open(self) -> int:
        super().open()
        return 0

    def close(self) -> int:
        super().close()
        return 0

    def read_tel_no(self) -> KeyPadInfo:
        logger.info("输入手机号")
        self.signal.keypad_read_signal.emit("请输入手机号")
        self.event_loop = QEventLoop()
        self.event_loop.exec_()
        keyPadInfo = KeyPadInfo()
        keyPadInfo.data = self.data
        return keyPadInfo

    def read_auth_code(self) -> KeyPadInfo:
        logger.info("输入手机号")
        self.signal.keypad_read_signal.emit("请输入验证码")
        self.event_loop = QEventLoop()
        self.event_loop.exec_()
        keyPadInfo = KeyPadInfo()
        keyPadInfo.data = self.data
        return keyPadInfo


if __name__ == "__main__":
    keypad = MockKeypad()
    pwd = keypad.read_pwd(flag=1)
    print(pwd)
