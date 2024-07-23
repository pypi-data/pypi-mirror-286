import time

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QSizePolicy, \
    QSpacerItem


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 450)
        self.vBoxLayout = QVBoxLayout(Form)
        self.vBoxLayout.setContentsMargins(40, 30, 40, 20)
        self.hBoxLayout = QHBoxLayout()
        self.label1 = QLabel(text="卡    号", parent=Form)
        self.card = QLineEdit(parent=Form)
        self.card.setMinimumSize(QSize(0, 40))
        self.card.setText("6217998340006985046")
        self.hBoxLayout.addWidget(self.label1)
        self.hBoxLayout.addWidget(self.card)

        self.hBoxLayout2 = QHBoxLayout()
        self.label2 = QLabel(text="第一磁道", parent=Form)
        self.first_track = QLineEdit(parent=Form)
        self.first_track.setText("")
        self.first_track.setMinimumSize(QSize(0, 40))
        self.hBoxLayout2.addWidget(self.label2)
        self.hBoxLayout2.addWidget(self.first_track)

        self.hBoxLayout3 = QHBoxLayout()
        self.label3 = QLabel(text="第二磁道", parent=Form)
        self.second_track = QLineEdit(parent=Form)
        self.second_track.setText("6217998340006985046=28092200200600000")
        self.second_track.setMinimumSize(QSize(0, 40))
        self.hBoxLayout3.addWidget(self.label3)
        self.hBoxLayout3.addWidget(self.second_track)

        self.hBoxLayout4 = QHBoxLayout()
        self.label4 = QLabel(text="第三磁道", parent=Form)
        self.third_track = QLineEdit(parent=Form)
        self.third_track.setMinimumSize(QSize(0, 40))
        self.third_track.setText(
            "996217998340006985046=1561560000000000000003000000114000028091=000000000000=000000000000=000000002006000")
        self.hBoxLayout4.addWidget(self.label4)
        self.hBoxLayout4.addWidget(self.third_track)

        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addLayout(self.hBoxLayout2)
        self.vBoxLayout.addLayout(self.hBoxLayout3)
        self.vBoxLayout.addLayout(self.hBoxLayout4)

        self.hBoxLayout5 = QHBoxLayout()
        spacerItem = QSpacerItem(58, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.hBoxLayout5.addItem(spacerItem)
        self.label5 = QLabel(text="信息读取成功，点击\"确认\"关闭此窗口", parent=Form)
        self.readBtn = QPushButton(text="确定", parent=Form)
        self.readBtn.setMinimumSize(QtCore.QSize(90, 35))
        self.readBtn.setStyleSheet("background-color: rgb(225, 241, 255);")
        self.hBoxLayout5.addWidget(self.label5)
        self.hBoxLayout5.addWidget(self.readBtn)
        self.vBoxLayout.addLayout(self.hBoxLayout5)
