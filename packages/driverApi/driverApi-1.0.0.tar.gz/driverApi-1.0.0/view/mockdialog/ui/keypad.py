from PySide2 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(515, 167)
        Form.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(35, -1, 35, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pwd = QtWidgets.QLineEdit(parent=Form)
        self.pwd.setMinimumSize(QtCore.QSize(0, 28))
        self.pwd.setClearButtonEnabled(True)
        self.horizontalLayout.addWidget(self.pwd)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 11)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(168, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.btn = QtWidgets.QPushButton("确认", parent=Form)
        self.btn.setMinimumSize(QtCore.QSize(89, 35))
        self.btn.setObjectName("btn")
        self.btn.setStyleSheet("background-color: rgb(225, 241, 255);")
        self.horizontalLayout_3.addWidget(self.btn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

