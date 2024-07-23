from PySide2 import QtCore
from PySide2.QtGui import QCloseEvent
from PySide2.QtCore import Signal, Qt, QSize
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QLineEdit

from common import common_utils, Singleton
from driver.finance_ic_card_rwer import FinanceICInfo, PBOCVersion
from view.mockdialog.ui import finaceIc


class FinanceIcCardView(QDialog):
    """
    模拟读取金融卡信息
    """
    finished = Signal(object)

    def __init__(self, financeICInfo):
        super().__init__()
        self.icInfo = financeICInfo
        self.ui = finaceIc.Ui_Form()
        self.setWindowTitle("模拟金融IC卡阅读器")
        self.ui.setupUi(self)
        self.ui.confirm.clicked.connect(self.btnClick)
        for label in self.findChildren(QLabel):
            label.setFixedSize(100, 25)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        for lineEdit in self.findChildren(QLineEdit):
            lineEdit.setMinimumSize(QSize(100, 25))

    def btnClick(self):
        """确认按钮，用来校验数据，保存数据,如果对数据有特殊，可在获取数据时加校验"""
        self.icInfo.arqc = self.ui.arqc.text()
        self.icInfo.cert_type = self.ui.cert_type.text()
        self.icInfo.cert_no = self.ui.cert_no.text()
        self.icInfo.card_no = self.ui.card_no.text()
        self.icInfo.card_serial_no = self.ui.card_serial_no.text()
        self.icInfo.owner_name = self.ui.owner_name.text()
        self.icInfo.balance = self.ui.balance.text()
        self.icInfo.ccy = self.ui.ccy.text()
        """交易日志信息，从表格获取"""
        # tran_detail = self.ui.tran_detail.text()
        self.icInfo.issue_branch_data = self.ui.issue_branch_data.text()
        self.icInfo.aid = self.ui.aid.text()
        self.icInfo.arqc_source = self.ui.arqc_source.text()
        self.icInfo.tran_counter = self.ui.tran_counter.text()
        self.icInfo.balance_limit = self.ui.balance_limit.text()
        self.icInfo.single_limit = self.ui.single_limit.text()
        self.icInfo.verify_result = self.ui.verify_result.text()
        self.icInfo.arqc_only = self.ui.arqc_only.text()
        self.icInfo.effective_date = self.ui.effective_date.text()
        self.icInfo.overdue_date = self.ui.overdue_date.text()
        self.icInfo.track2Data = self.ui.track2Data.text()
        self.icInfo.pboc_ver = PBOCVersion.PBOC_VER_20
        self.icInfo.contact_mode = self.ui.contact_mode.text()
        self.close()

    def closeEvent(self, event: QCloseEvent):
        self.finished.emit(self.icInfo)
        event.accept()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication([])
    window = FinanceIcCardView([])
    window.show()
    app.exec_()
