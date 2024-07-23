# author: haoliqing
# date: 2023/9/5 16:21
# desc:
import time

from PySide2.QtCore import QEventLoop

from common import Singleton
from device.device_config import DeviceConfig
from driver.magnetic_strip_rwer import MagneticStripRWer, MagneticStripInfo
from view.signal.read_signal import ReadSignal


@Singleton
class MockMagnetIC(MagneticStripRWer):
    """模拟磁条读写器驱动实现类"""
    signal = ReadSignal()
    magneticInfo = None

    def init(self, device_cfg: DeviceConfig) -> int:
        super().init(device_cfg)
        return 0

    def read(self) -> MagneticStripInfo:
        """TODO 弹出模拟外设读卡，读取磁条信息并返回"""
        self.signal.magnetic_read_signal.emit(MagneticStripInfo())
        self.event_loop = QEventLoop()
        self.event_loop.exec_()
        return self.magneticInfo

    def read_finished(self, magneticInfo):
        print(magneticInfo)
        if self.event_loop and self.event_loop.isRunning():
            self.event_loop.quit()
        self.magneticInfo = magneticInfo

    def write(self, stack1_info: str, stack2_info: str, stack3_info: str) -> int:
        time.sleep(1)  # 等待1秒
        return 0

    def open(self) -> int:
        super().open()
        return 0

    def close(self) -> int:
        super().close()
        return 0


if __name__ == '__main__':
    ic = MockMagnetIC()
    data = ic.read()
    print(data)
