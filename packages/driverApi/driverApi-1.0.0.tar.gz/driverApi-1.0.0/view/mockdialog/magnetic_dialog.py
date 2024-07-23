from PySide2 import QtCore
from PySide2.QtCore import Signal, Qt
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import QDialog, QApplication

from view.mockdialog.ui import magneticIC


class MagneticView(QDialog):
    """
    读取磁条卡信息显示窗口
    """
    finished = Signal(object)

    def __init__(self, magneticInfo):
        super().__init__()
        self.data = magneticInfo
        self.ui = magneticIC.Ui_Form()
        self.setWindowTitle("模拟磁条卡阅读器")
        self.ui.setupUi(self)
        self.ui.readBtn.clicked.connect(self.btnClick)

    def btnClick(self):
        """点击'确认'获取信息，存储到data，等待调用"""
        self.data.card_no = self.ui.card.text()
        self.data.stack1_info = self.ui.first_track.text()
        self.data.stack2_info = self.ui.second_track.text()
        self.data.stack3_info = self.ui.third_track.text()
        self.close()

    def closeEvent(self, event: QCloseEvent):
        self.finished.emit(self.data)
        event.accept()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    window = MagneticView([])
    window.show()
    app.exec_()
