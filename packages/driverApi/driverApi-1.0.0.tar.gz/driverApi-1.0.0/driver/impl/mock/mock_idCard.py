from PySide2.QtCore import QEventLoop

from common import Singleton
from device.device_config import DeviceConfig
from driver.id_card_reader import IDCardReader, IDInfo
from view.signal.read_signal import ReadSignal


@Singleton
class MockIDCardReader(IDCardReader):
    """身份证阅读器适配器基类"""
    signal = ReadSignal()
    data = None

    def init(self, device_cfg: DeviceConfig) -> int:
        super().init(device_cfg)
        return 0

    def read(self) -> IDInfo:
        """
        读取二代证信息 TODO 模拟读取身份证
        :return: 读取到的二代证信息，若返回值为None，则获取失败，否则读卡的成功与失败由IDInfo.errorCode来决定，
        若该值小于0，则认为读卡失败，否则为读卡成功，该值需要在驱动实现中自行设置，默认为0
        """
        self.signal.idcard_read_signal.emit(IDInfo())
        self.event_loop = QEventLoop()
        self.event_loop.exec_()
        return self.data

    def read_finished(self, idInfo):
        if self.event_loop and self.event_loop.isRunning():
            self.event_loop.quit()
        self.data = idInfo

    def open(self) -> int:
        super().open()
        return 0

    def close(self) -> int:
        super().close()
        return 0


if __name__ == '__main__':
    idCard = MockIDCardReader()
    data = idCard.read()
    print(data)
