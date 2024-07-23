from PySide2 import QtCore
from PySide2.QtGui import QCloseEvent
from PySide2.QtCore import QRegularExpression, Qt, Signal
from PySide2.QtGui import QRegularExpressionValidator
from PySide2.QtWidgets import QDialog, QApplication

from driver.id_card_reader import IDInfo
from view.mockdialog.ui import idCard


class IdCardView(QDialog):
    """
    读取身份证实例窗口实现类
    """
    finished = Signal(IDInfo)

    def __init__(self, idInfo):
        super().__init__()
        self.idInfo = idInfo
        self.ui = idCard.Ui_Form()
        self.setWindowTitle("模拟二代身份证阅读器")
        self.ui.setupUi(self)
        self.ui.confirm.clicked.connect(self.btnClick)
        self.setValidator()

    def setValidator(self):
        expression = QRegularExpression("[0-9]{17,18}")
        validator = QRegularExpressionValidator(expression)
        self.ui.id.setValidator(validator)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

    def btnClick(self):
        self.idInfo.cnName = self.ui.cnName.text()
        self.idInfo.sex = self.ui.sex.text()
        self.idInfo.nation = self.ui.nation.text()
        self.idInfo.birthday = self.ui.birthday.text()
        self.idInfo.address = self.ui.address.text()
        self.idInfo.id = self.ui.id.text()
        self.idInfo.dep = self.ui.dep.text()
        self.idInfo.begin = self.ui.beginDate.text()
        self.idInfo.end = self.ui.endDate.text()
        self.idInfo.image_path = self.ui.imagePath.text()
        self.idInfo.image_info = self.ui.imageInfo.text()
        self.close()

    def closeEvent(self, event: QCloseEvent):
        self.finished.emit(self.idInfo)
        event.accept()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    window = IdCardView([])
    window.show()
    app.exec_()
