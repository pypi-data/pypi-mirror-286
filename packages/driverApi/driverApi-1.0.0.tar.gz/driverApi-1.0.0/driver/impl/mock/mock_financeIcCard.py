import time

from PySide2.QtCore import QEventLoop

from common import Singleton
from device.device_config import DeviceConfig
from driver.finance_ic_card_rwer import FinanceICCardRWer, FinanceICInfo, TranInfo
from view.signal.read_signal import ReadSignal


@Singleton
class MockFinanceIcCard(FinanceICCardRWer):
    signal = ReadSignal()
    financeICInfo = None

    def power_on(self) -> int:
        time.sleep(1)  # 等待1秒
        return 0

    def power_off(self) -> int:
        time.sleep(1)  # 等待1秒
        return 0

    def read_finance_ic_info(self, tran_info: TranInfo) -> FinanceICInfo:
        self.signal.iccard_read_signal.emit(FinanceICInfo())
        self.event_loop = QEventLoop()
        self.event_loop.exec_()
        return self.financeICInfo

    def read_finished(self, financeICInfo):
        if self.event_loop and self.event_loop.isRunning():
            self.event_loop.quit()
        self.financeICInfo = financeICInfo

    def init(self, device_cfg: DeviceConfig) -> int:
        super().init(device_cfg)
        return 0

    def open(self) -> int:
        super().open()
        return 0

    def close(self) -> int:
        super().close()
        return 0


if __name__ == '__main__':
    idCard = MockFinanceIcCard()
    data = idCard.read_finance_ic_info(TranInfo())
    print(data)
