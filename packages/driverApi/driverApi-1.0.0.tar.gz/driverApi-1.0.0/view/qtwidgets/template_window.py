from PySide2.QtCore import (QMetaObject, QSize, Qt)
from PySide2.QtGui import (QCursor, QFont)
from PySide2.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem,
                               QTableWidget, QVBoxLayout, QWidget, QTableWidgetItem, QHeaderView)


class TempWin(QWidget):
    def __init__(self):
        super().__init__()
        self.save = None
        self.cancel = None
        self.search = None
        self.table = None
        self.term_mod_val = None
        self.term_mod_lab = None
        self.term_cls_val = None
        self.term_cls_lab = None

        self.setWindowTitle("使用模板")
        size = self.screen().size()
        self.setFixedSize((size.width()) / 2, (size.height()) / 4)
        self.btnStyle = "background-color: rgb(0, 85, 255);color: rgb(255, 255, 255);"
        self.initWindow()
        self.initTable()

    def initWindow(self):
        self.globalLayout = QVBoxLayout(self)
        self.globalLayout.setContentsMargins(15, 0, 15, 0)
        self.layout1 = QHBoxLayout()
        self.layout1.setContentsMargins(0, 15, 50, 15)

        self.term_cls_lab = QLabel(self, text="终端类型")
        self.layout1.addWidget(self.term_cls_lab)

        self.term_cls_val = QComboBox(self)
        self.term_cls_val.addItem("windows", 0)
        self.term_cls_val.addItem("linux", 1)
        self.term_cls_val.setMinimumSize(QSize(0, 30))
        self.term_cls_val.setMaximumSize(QSize(200, 16777215))
        self.layout1.addWidget(self.term_cls_val)

        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout1.addItem(self.spacer1)

        self.term_mod_lab = QLabel(self, text="终端型号")
        self.layout1.addWidget(self.term_mod_lab)

        self.term_mod_val = QComboBox(self)
        self.term_mod_val.setMinimumSize(QSize(0, 30))
        self.term_mod_val.setMaximumSize(QSize(200, 16777215))

        self.layout1.addWidget(self.term_mod_val)

        self.search = QPushButton(self, text="查询")
        self.search.setMinimumSize(QSize(0, 25))
        self.search.setStyleSheet(self.btnStyle)

        self.layout1.addWidget(self.search)

        self.layout1.setStretch(0, 1)
        self.layout1.setStretch(1, 2)
        self.layout1.setStretch(2, 1)
        self.layout1.setStretch(3, 1)
        self.layout1.setStretch(4, 2)
        self.layout1.setStretch(5, 1)

        self.globalLayout.addLayout(self.layout1)

        self.table = QTableWidget(self)

        self.globalLayout.addWidget(self.table)
        self.layout2 = QHBoxLayout()
        self.layout2.setSpacing(12)
        self.layout2.setContentsMargins(10, 10, 0, 10)
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout2.addItem(self.spacer)

        self.cancel = QPushButton(self, text="取消")
        self.cancel.setMinimumSize(QSize(0, 25))
        self.cancel.setCursor(QCursor(Qt.PointingHandCursor))
        self.cancel.setStyleSheet(self.btnStyle)
        self.cancel.clicked.connect(self.close)
        self.layout2.addWidget(self.cancel)

        self.save = QPushButton(self, text="保存")
        self.save.setMinimumSize(QSize(0, 25))
        self.save.setCursor(QCursor(Qt.PointingHandCursor))
        self.save.setStyleSheet(self.btnStyle)
        self.layout2.addWidget(self.save)

        self.globalLayout.addLayout(self.layout2)
        QMetaObject.connectSlotsByName(self)

    def initTable(self):
        self.table.setColumnCount(2)
        title: list = ["模板编号", "模板名称"]
        for i in range(0, 2):
            item = QTableWidgetItem()
            self.table.setHorizontalHeaderItem(i, item)
            self.table.horizontalHeaderItem(i).setText(title[i])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()
