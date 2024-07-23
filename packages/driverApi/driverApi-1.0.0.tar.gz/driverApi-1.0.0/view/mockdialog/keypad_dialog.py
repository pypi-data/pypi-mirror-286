from PySide2 import QtCore
from PySide2.QtCore import QRegularExpression, Qt, Signal
from PySide2.QtGui import QRegularExpressionValidator, QCloseEvent
from PySide2.QtWidgets import QMessageBox, QDialog, QApplication

from view.mockdialog.ui import keypad


class KeyPadView(QDialog):
    """
    密码键盘实例窗口实现
    """
    finished = Signal(str)

    def __init__(self, prompt):
        super().__init__()
        self.data: str = None
        self.ui = keypad.Ui_Form()
        self.setWindowTitle("模拟密码键盘")
        self.ui.setupUi(self)
        self.ui.label.setText(prompt)
        self.ui.btn.clicked.connect(self.btnClick)

    def btnClick(self):
        flag: bool = True
        pwd = self.ui.pwd.text()
        if len(pwd) < 6:
            QMessageBox.information(self, "提示", "密码格式不正确,请重新输入！")
            QMessageBox().setWindowFlags(Qt.WindowStaysOnTopHint)
            self.ui.pwd.setText("")
            flag = False
        else:
            self.data = pwd
        if flag:
            self.close()

    def closeEvent(self, event: QCloseEvent):
        self.finished.emit(self.data)
        event.accept()

    def getData(self) -> str:
        return self.data


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    window = KeyPadView(1)
    window.show()
    app.exec_()
