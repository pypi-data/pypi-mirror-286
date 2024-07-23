from typing import List, Dict

from PySide2 import QtCore
from PySide2.QtCore import (Qt, QFile)
from PySide2.QtGui import (QCursor, QFont, QScreen)
from PySide2.QtWidgets import (QHBoxLayout, QSizePolicy, QSpacerItem,
                               QVBoxLayout, QApplication, QTableWidgetItem,
                               QHeaderView, QComboBox)
from qfluentwidgets import InfoBar, MessageBox, CaptionLabel, LineEdit, TableWidget, \
    TransparentPushButton, PushButton, ComboBox, isDarkTheme, SubtitleLabel
from qframelesswindow import FramelessWindow

from logger.device_logger import logger
from service_adpter import DevBindCallImpl, DevCommParamCallImpl, DevParamCallImpl
from view.qtwidgets.custom_delegate import MTableItemDelegate
from view.qss import app_theme


class DetailWindow(FramelessWindow):
    """ 绑定详情窗口 """

    def __init__(self, bindId: str, termId: str, commPortOps: List, devStatusDict: Dict):
        super().__init__()
        # 服务实例
        self.setWindowModality(Qt.ApplicationModal)
        self.devBindCall = DevBindCallImpl()
        self.devCommParamCall = DevCommParamCallImpl()
        self.devParamCall = DevParamCallImpl()
        # 本条数据的绑定id、终端id、端口类型-端口、启用状态字典
        self.bindId: str = bindId
        self.termId: str = termId
        self.commPortOps = commPortOps
        self.devStatusDict = devStatusDict

        self.table1Data: List = []
        self.table2Data: List = []
        self.commParamOps: list = []
        self.devParamOps: list = []
        # 基础绑定信息
        self.baseBindInfo: dict = {}

        # 初始化窗口
        self.initWindow()
        # 设置基本数据
        self.setBaseInfo()
        # 查询下拉框选项值
        self.initCommParamOps()
        self.initDevParamOps()
        # 根据bindId查询两个表格数据并渲染表格
        self.initTable(self.table1, ["通讯参数名称", "通讯参数值", "操作", "新增标志"])
        self.initTable(self.table2, ["设备参数名称", "设备参数值", "操作", "新增标识"])

    def setBaseInfo(self):
        """ 点击详情按钮拿到绑定id并查询基本信息 """
        self.baseBindInfo = self.devBindCall.getBindDetailByBindId(self.bindId)
        if self.baseBindInfo:
            detail = self.baseBindInfo
            self.devClass.setText(f"{detail.get('devClassId')}-{detail.get('devClassDesc')}")
            self.devModel.setText(f"{detail.get('devModelId')}-{detail.get('devModelDesc')}")
            self.commPort.setText(f"{detail.get('commPort')}")
            self.enabled.setText(self.devStatusDict.get(detail.get("status")))

    def initCommParamOps(self):
        """
        根据基本信息中的”端口类型“ 获取端口通讯参数选项
        @return:
        """
        if self.baseBindInfo:
            commPort = self.baseBindInfo.get("commPort")
            commPortType = None
            for item in self.commPortOps:
                if commPort == item[1]:
                    commPortType = item[2]
            self.commParamOps = self.devCommParamCall.getCommParamByCommTypeId(commPortType)

    def initDevParamOps(self):
        """ 根据 ”设备类型“ 获取设备类型参数选项 """
        if self.baseBindInfo:
            self.devParamOps: list = []
            data = self.devParamCall.getDevParamByDevModelId(self.baseBindInfo.get("devModelId"))
            for index, item in enumerate(data):
                option: tuple = (f"{index + 1}-{item['devParamDesc']}", item['devParamId'],)
                self.devParamOps.append(option)

    def initTable(self, tableWidget: TableWidget, titleList: List):
        tableWidget.setColumnCount(4)
        # ["通讯参数名称", "通讯参数值", "操作", "新增标志"]
        tableWidget.setHorizontalHeaderLabels(titleList)
        tableWidget.setBorderVisible(False)
        tableWidget.setBorderRadius(8)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.showGrid()
        tableWidget.setItemDelegate(MTableItemDelegate(self.table1))
        tableWidget.setColumnHidden(3, True)
        # 设置表格数据
        if tableWidget is self.table1:
            self.setTable1Data()
        elif tableWidget is self.table2:
            self.setTable2Data()

    def setTable1Data(self):
        """
        渲染表格1数据
        @return:
        """
        if self.baseBindInfo:
            commPort = self.baseBindInfo.get("commPort")
            self.table1Data = self.devCommParamCall.getDevRunCommParamByBindId(self.bindId, commPort)
            self.table1.setRowCount(len(self.table1Data))
            for rowIndex, row in enumerate(self.table1Data):
                for colIndex, cell_data in enumerate(row):
                    if colIndex == 0:
                        self.setComboBox(self.table1, self.commParamOps, rowIndex, colIndex, cell_data)
                    elif colIndex == 1:
                        self.table1.setItem(rowIndex, colIndex, QTableWidgetItem(cell_data))
                self.setDeleteButton(self.table1, rowIndex, "No")
            # 初始化完数据之后删除已有的下拉框选项值，避免重复添加
            removeList = []
            for item in self.table1Data:
                removeList.append(item[0])
            self.commParamOps = [tup for tup in self.commParamOps if tup[1] not in removeList]

    def insertCommParam(self):
        """
        表1新增一行数据，并设置下拉框的值
        @return:
        """
        totalCount = len(self.table1Data)
        rowCount = self.table1.rowCount()  # 新行的下标为总行数
        if rowCount - totalCount > 0:
            InfoBar.warning(title="提示", content="请先保存后添加！", parent=self)
            return
        self.table1.insertRow(rowCount)
        self.setComboBox(self.table1, self.commParamOps, rowCount, 0, None)
        self.setDeleteButton(self.table1, rowCount, "YES")

    def saveAndUpdateTable1Data(self):
        """
        保存或更新数据表1数据
        @return:
        """
        reqCount = len(self.table1Data)
        updateNum = 0
        updateFlag: bool = True
        for row in range(self.table1.rowCount()):
            rowObj = DevRunCommParam()
            rowObj.bindId = self.bindId
            rowObj.commPort = self.baseBindInfo.get("commPort")
            for column in range(self.table1.columnCount()):
                if column == 0:
                    item: QComboBox = self.table1.cellWidget(row, column)
                    userData = item.currentData()
                    rowObj.devCommParamId = userData
                elif column == 1:
                    item = self.table1.item(row, column)
                    if item is not None:
                        rowObj.runValue = item.text()
                    else:
                        rowObj.runValue = item
                elif column == 3:
                    rowObj.addFlag = self.table1.item(row, column).text()
            # 新增标识为YES并且参数有值 调用新增接口
            if rowObj.addFlag == "YES" and rowObj.runValue is not None and len(rowObj.runValue) > 0:
                respBody = self.devCommParamCall.addDevRunCommParam(rowObj.__dict__)
                if respBody and respBody.get("success", None):
                    InfoBar.success("提示", "通讯参数新增成功!", parent=self)
                else:
                    InfoBar.error("提示", f"{respBody['errCode']}:{respBody['errMessage']}！",
                                  parent=self)
                self.initCommParamOps()
                self.setTable1Data()
            elif row < reqCount and rowObj.runValue != self.table1Data[row][1]:
                updateFlag = self.devCommParamCall.updateDevRunCommParam(rowObj.__dict__)
                updateNum += 1
        if updateNum > 0:
            if updateFlag:
                InfoBar.success("提示", f"{updateNum}条通讯参数已更新成功！", parent=self)
            else:
                InfoBar.error("提示", "更新失败！", parent=self)
            self.initCommParamOps()
            self.setTable1Data()

    def setTable2Data(self):
        """
        渲染表格2数据
        @return:
        """
        if self.baseBindInfo:
            bindId = self.baseBindInfo.get("bindId")
            self.table2Data = self.devParamCall.getDevRunParamByBindId(bindId)
            self.table2.setRowCount(len(self.table2Data))
            for rowIndex, row in enumerate(self.table2Data):
                for colIndex, cel_data in enumerate(row):
                    if colIndex == 0:
                        self.setComboBox(self.table2, self.devParamOps, rowIndex, colIndex, cel_data)
                    elif colIndex == 1:
                        self.table2.setItem(rowIndex, colIndex, QTableWidgetItem(cel_data))
                self.setDeleteButton(self.table2, rowIndex, "No")
            # 初始化完数据之后删除已有的下拉框选项值，避免重复添加
            removeList = []
            for item in self.table2Data:
                removeList.append(item[0])
            self.devParamOps = [tup for tup in self.devParamOps if tup[1] not in removeList]

    def insertDevParam(self):
        """
        表2新增一行数据，并设置下拉框的值
        @return:
        """
        totalCount = len(self.table2Data)
        rowCount = self.table2.rowCount()
        if rowCount - totalCount > 0:
            InfoBar.warning(title="提示", content="请先保存后添加！", parent=self)
            return
        self.table2.insertRow(rowCount)
        self.setComboBox(self.table2, self.devParamOps, rowCount, 0, None)
        self.setDeleteButton(self.table2, rowCount, "YES")

    @staticmethod
    def setComboBox(tableWidget: TableWidget, comboBoxData: List, rowIndex: int, columnIndex: int, data):
        combobox = ComboBox()
        combobox.setMaximumHeight(28)
        combobox.setFont(QFont("仿宋", 10))
        for item in comboBoxData:
            combobox.addItem(item[0], userData=item[1])
            if data:
                index = combobox.findData(data)
                combobox.setCurrentIndex(index)
                combobox.setEnabled(False)
        tableWidget.setCellWidget(rowIndex, columnIndex, combobox)

    def setDeleteButton(self, tableWidget: TableWidget, rowIndex: int, flag: str):
        delete_button = TransparentPushButton(tableWidget)
        delete_button.setText("删除")
        delete_button.setMaximumHeight(25)
        delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        delete_button.clicked.connect(self.removeRow)
        tableWidget.setCellWidget(rowIndex, 2, delete_button)
        tableWidget.setItem(rowIndex, 3, QTableWidgetItem(flag))

    def removeRow(self):
        sender = self.sender()  # 获取发送信号的按钮对象
        if isinstance(sender, TransparentPushButton):
            if sender in self.table1.findChildren(TransparentPushButton):
                btnPos = self.table1.indexAt(sender.pos())
                if btnPos.isValid():
                    row = btnPos.row()
                    messageBox = MessageBox("删除提示", "是否删除当前数据?", self)
                    messageBox.yesButton.setText("删除")
                    messageBox.cancelButton.setText("取消")
                    if messageBox.exec():
                        bindId = self.bindId
                        commPort = self.baseBindInfo.get("commPort")
                        devCommParamId = self.table1.cellWidget(row, 0).currentData()
                        respBody = self.devCommParamCall.deleteDevRunCommParam(bindId, commPort, devCommParamId)
                        if respBody and respBody.get("success", None):
                            InfoBar.success(title="提示", content="删除成功！", parent=self)
                        self.initCommParamOps()
                        self.setTable1Data()
            elif sender in self.table2.findChildren(TransparentPushButton):
                btnPos = self.table2.indexAt(sender.pos())
                if btnPos.isValid():
                    row = btnPos.row()
                    messageBox = MessageBox("删除提示", "是否删除当前数据?", self)
                    messageBox.yesButton.setText("删除")
                    messageBox.cancelButton.setText("取消")
                    if messageBox.exec():
                        bindId = self.bindId
                        devCommParamId = self.table2.cellWidget(row, 0).currentData()
                        flag = self.devParamCall.deleteDevRunParam(bindId, devCommParamId)
                        if flag:
                            InfoBar.success("提示", "删除成功！", parent=self)
                        self.initDevParamOps()
                        self.setTable2Data()

    def saveAndUpdateTable2Data(self):
        """
        保存或更新数据表2数据
        @return:
        """
        reqCount = len(self.table2Data)
        updateNum = 0
        updateFlag: bool = True
        for row in range(self.table2.rowCount()):
            rowObj = DevRunParam()
            rowObj.bindId = self.bindId
            for column in range(self.table2.columnCount()):
                if column == 0:
                    item: QComboBox = self.table2.cellWidget(row, column)
                    userData = item.currentData()
                    rowObj.devParamId = userData
                elif column == 1:
                    item = self.table2.item(row, column)
                    if item is not None:
                        rowObj.runValue = (item.text())
                    else:
                        rowObj.runValue = item
                elif column == 3:
                    rowObj.addFlag = self.table2.item(row, column).text()
            # 新增标识为YES并且参数有值 调用新增接口
            if rowObj.addFlag == "YES" and rowObj.runValue is not None:
                respBody = self.devParamCall.addDevRunParam(rowObj.__dict__)
                if respBody and respBody.get("success", None):
                    InfoBar.success("提示", "设备参数新增成功", parent=self)
                else:
                    InfoBar.error("提示", f"{respBody['errCode']}:{respBody['errMessage']}！",
                                  parent=self)
                self.initDevParamOps()
                self.setTable2Data()
            elif row < reqCount and rowObj.runValue != self.table2Data[row][1]:
                updateFlag = self.devParamCall.updateRunDevParam(rowObj.__dict__)
                updateNum += 1
        if updateNum > 0:
            if updateFlag:
                InfoBar.success("提示", f"{updateNum}条设备参数已更新成功！", parent=self)
            else:
                InfoBar.error("提示", "更新失败！", parent=self)
            self.initDevParamOps()
            self.setTable2Data()

    def submit(self):
        self.saveAndUpdateTable1Data()
        self.saveAndUpdateTable2Data()

    def initWindow(self):
        self.resize(900, 600)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
        self.globalLayout = QVBoxLayout(self)
        self.globalLayout.setContentsMargins(20, 0, 20, 20)
        self.titleLayout = QHBoxLayout(self)
        self.titleLayout.setContentsMargins(10, 10, 150, 20)
        self.title = SubtitleLabel(self)
        self.title.setText("绑定详情")
        self.titleLayout.addWidget(self.title)
        self.globalLayout.addLayout(self.titleLayout)

        self.horLayoutRow1 = QHBoxLayout()
        self.devClass_label = CaptionLabel(self)
        self.devClass_label.setText("设备类型")
        self.devClass_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.devClass = LineEdit(self)
        self.devClass.setEnabled(False)
        self.devClass.setMaximumHeight(30)
        self.devClass.setFixedHeight(30)
        self.commPort_label = CaptionLabel(self)
        self.commPort_label.setText("通讯端口")
        self.commPort_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.commPort = LineEdit(self)
        self.commPort.setEnabled(False)
        self.commPort.setMaximumHeight(30)
        self.commPort.setFixedHeight(30)
        self.spacer1 = QSpacerItem(60, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horLayoutRow1.addWidget(self.devClass_label)
        self.horLayoutRow1.addWidget(self.devClass)
        self.horLayoutRow1.addWidget(self.commPort_label)
        self.horLayoutRow1.addWidget(self.commPort)
        self.horLayoutRow1.addItem(self.spacer1)

        self.horLayoutRow2 = QHBoxLayout()
        self.devModel_label = CaptionLabel(self)
        self.devModel_label.setText("设备型号")
        self.devModel_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.devModel = LineEdit(self)
        self.devModel.setEnabled(False)
        self.devModel.setMaximumHeight(30)
        self.devModel.setFixedHeight(30)
        self.enabled_label = CaptionLabel(self)
        self.enabled_label.setText("是否启用")
        self.enabled_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.enabled = LineEdit(self)
        self.enabled.setEnabled(False)
        self.enabled.setMaximumHeight(30)
        self.enabled.setFixedHeight(30)
        self.spacer2 = QSpacerItem(60, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horLayoutRow2.addWidget(self.devModel_label)
        self.horLayoutRow2.addWidget(self.devModel)
        self.horLayoutRow2.addWidget(self.enabled_label)
        self.horLayoutRow2.addWidget(self.enabled)
        self.horLayoutRow2.addItem(self.spacer2)

        self.horLayoutRow3 = QHBoxLayout()
        self.add_comm_param = PushButton(self)
        self.add_comm_param.setText("新增通讯参数")
        self.add_comm_param.setMaximumSize(150, 30)
        self.add_comm_param.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_comm_param.clicked.connect(self.insertCommParam)
        self.spacer3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horLayoutRow3.addWidget(self.add_comm_param)
        self.horLayoutRow3.addItem(self.spacer3)

        self.table1 = TableWidget(self)

        self.horLayoutRow4 = QHBoxLayout()
        self.add_dev_param = PushButton(self)
        self.add_dev_param.setText("增加设备参数")
        self.add_dev_param.setMaximumSize(150, 30)
        self.add_dev_param.setCursor(QCursor(Qt.PointingHandCursor))
        self.add_dev_param.clicked.connect(self.insertDevParam)
        self.spacer4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horLayoutRow4.addWidget(self.add_dev_param)
        self.horLayoutRow4.addItem(self.spacer4)

        self.table2 = TableWidget(self)

        self.horLayoutRow5 = QHBoxLayout()
        self.spacer5 = QSpacerItem(258, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.save = PushButton(self)
        self.save.setText("保存")
        self.save.setMaximumSize(150, 30)
        self.save.setMinimumWidth(100)
        self.save.clicked.connect(self.submit)
        self.save.setCursor(QCursor(Qt.PointingHandCursor))
        self.horLayoutRow5.addItem(self.spacer5)
        self.horLayoutRow5.addWidget(self.save)

        self.globalLayout.addLayout(self.horLayoutRow1)
        self.globalLayout.addLayout(self.horLayoutRow2)
        self.globalLayout.addLayout(self.horLayoutRow3)
        self.globalLayout.addWidget(self.table1)
        self.globalLayout.addLayout(self.horLayoutRow4)
        self.globalLayout.addWidget(self.table2)
        self.globalLayout.addLayout(self.horLayoutRow5)

        self.setQss()

    def setQss(self):
        logger.info(app_theme)
        color = 'dark' if isDarkTheme() else 'light'
        style_file = QFile(f":/{color}.qss")
        style_file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = style_file.readAll().data().decode("utf-8")
        self.setStyleSheet(stylesheet)


class DevRunCommParam:
    def __init__(self):
        self.bindId = None
        """终端设备绑定ID"""
        self.commPort = None
        """绑定端口号"""
        self.devCommParamId = None
        """通讯参数ID"""
        self.runValue = None
        """参数值"""
        self.addFlag = None
        """新增标识"""


class DevRunParam:
    def __init__(self):
        self.bindId: str = None
        """ 终端设备绑定ID """
        self.devParamId: str = None
        """ 设备参数ID """
        self.runValue: str = None
        """ 参数值 """
        self.addFlag: str = None
        """新增标识"""


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 设置qt界面大小与原设计界面比例相同

    app = QApplication()
    # app.setStyle(QStyleFactory.create('Fusion'))
    self = DetailWindow(1, 1, [], {})
    self.show()
    app.exec_()
