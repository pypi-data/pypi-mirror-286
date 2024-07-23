from PySide2.QtCore import QObject, Signal

from common import Singleton


@Singleton
class ReadSignal(QObject):
    keypad_read_signal = Signal(str)
    idcard_read_signal = Signal(object)
    magnetic_read_signal = Signal(object)
    iccard_read_signal = Signal(object)
