import math
import time
from functools import partial
from typing import Dict, List

from PySide2 import QtCore
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QCursor, QFont
from PySide2.QtWidgets import (QComboBox, QGroupBox, QHBoxLayout,
                               QSizePolicy, QSpacerItem, QTableWidgetItem,
                               QVBoxLayout, QHeaderView, QApplication)
from PySide2.QtWidgets import QFrame
from qfluentwidgets import LineEdit, TableWidget, ComboBox, TransparentPushButton, PrimaryPushButton, InfoBar, \
    MessageBox, TransparentToolButton, FluentIcon, CaptionLabel, Dialog

from control import DeviceController
from logger.device_logger import logger
from model import init_config
from service_adpter import DevBindCallImpl, DevClassCallImpl, DevModelCallImpl, send_request, TerminalModelCallImpl
from service_adpter.impl.terminal_info_call_impl import TerminalInfoCallImpl
from task.container import TaskRegister
from task.manager import DeviceTaskManager
from view.qtwidgets.custom_delegate import MTableItemDelegate
from view.qtwidgets.detail_window import DetailWindow
from view.qtwidgets.gallery_interface import GalleryInterface
from view.qtwidgets.task_interface import TaskFrame


# 初始化外层界面布局
class DeviceInterface(GalleryInterface):
    def __init__(self, parent=None):
        super().__init__(title="设备管理", parent=parent)
        self.parent = parent
        self.setObjectName('DeviceInterface')
        self.deviceFrame = DeviceFrame(self.parent)
        self.vBoxLayout.addWidget(self.deviceFrame)


class TerminalDeviceBind:
    def __init__(self, bindId, termId, devModelId, commPort, status):
        self.bindId = bindId
        """ 设备绑定ID;uuid"""

        self.termId = termId
        """ 终端mac地址 """

        self.commPort = commPort
        """ 通讯端口 """

        self.devModelId = devModelId
        """ 设备型号 """

        self.status = status
        """ 启用状态"""


class DeviceFrame(QFrame):
    """
    设备绑定窗口
    """
    pageIndex = 1
    pageSize = 5
    totalPage = 1
    MFont = QFont("仿宋", 11)

    def __init__(self, parent=None):
        super().__init__()
        # 父窗口
        self.parent = parent

        self.restart_flag = False
        # 服务实例
        self.devBindCall = DevBindCallImpl()
        self.devClassCall = DevClassCallImpl()
        self.devModelCall = DevModelCallImpl()
        self.terminalInfoCall = TerminalInfoCallImpl()
        self.terminalModelCall = TerminalModelCallImpl()

        # 表格下拉框数据
        self.devClassOps: list[(str, str)] = []
        self.devStatusOps: list[(str, str)] = []
        self.devStatusDict: Dict = {}
        self.commPortOps: list[(str, str)] = []
        self.devModelOps: list[(str, str)] = []
        # 记录每一个类型设备的可选设备型号,用于动态设置下拉框{"Keypad": [('2-模拟密码键盘', '2'), ('201-电子签名柜外清', '201')]}
        self.devClassModelDict: dict = {}
        # 终端绑定信息列表
        self.bindInfoList: list = []
        # 终端绑定信息及总条数缓存
        self.bindInfoCache: Dict = None
        self.detailWin = None
        # 设置窗口基本信息
        self.initWindow()
        # 设置本机mac地址
        # 设置本机mac地址
        self.termMac.setText(self.terminalInfoCall.getMacAddr())
        self.initTable()
        self.totalPage = 0

    def updateCommPorts(self, index):
        termModelId = self.termModel.itemData(index)
        self.commPortOps = self.terminalInfoCall.getCommType(termModelId)
        self.setTableData()

    def init(self):
        self.restart_flag = False
        self.initTerminalInfo()
        self.initOptionData()
        self.setTableData()

    def initTerminalInfo(self):
        """
        根据本终端MAC地址查询  本终端信息
        @return:
        """
        # 设置终端型号下拉框
        termModels = self.terminalModelCall.getTerminalModels()
        if termModels:
            for key in termModels.keys():
                self.termModel.addItem(termModels[key], userData=key)
        self.termModel.currentIndexChanged.connect(partial(self.updateCommPorts))

        terminalInfo = self.terminalInfoCall.getTerminalInfoByMac(self.termMac.text())
        if terminalInfo:
            index = self.termModel.findData(terminalInfo.get("termModelId"))
            self.termModel.setCurrentIndex(index)
            self.termName.setText(terminalInfo.get("termDesc"))
            self.termId.setText(terminalInfo.get("termId"))

    def initOptionData(self):
        """
        初始化所有下拉框数据,查询表格数据
        @return:
        """
        self.devClassOps = self.devClassCall.getDevClass()
        if self.devClassOps:
            devClassIds: list = []
            for item in self.devClassOps:
                devClassIds.append(item[1])
            self.devClassModelDict = self.devModelCall.getDevModelByDevClass(devClassIds)
        self.commPortOps = self.terminalInfoCall.getCommType(self.termModel.currentData())
        self.devStatusOps = self.devBindCall.getStatus()
        for statusTuple in self.devStatusOps:
            self.devStatusDict[statusTuple[1]] = statusTuple[0]
        self.getBindInfo()

    def getBindInfo(self):
        termId = self.termId.text()
        if termId and termId != "":
            self.bindInfoCache = self.devBindCall.getBindDev(termId, self.pageIndex, self.pageSize)
        else:
            self.bindInfoCache = {"data": "", "total": 0}

    def initTable(self):
        """
        初始化表头
        @return:
        """
        self.table.setColumnCount(7)
        # 设置水平表头并隐藏垂直表头
        self.table.setHorizontalHeaderLabels(["ID", "设备类型", "设备型号", "通讯端口", "是否启用", "绑定详情", "操作"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(TableWidget.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.table.setItemDelegate(MTableItemDelegate(self.table))
        self.table.setColumnHidden(0, True)

    def setTableData(self):
        """ 渲染/刷新表格 """
        if self.bindInfoCache is None:
            return
        self.bindInfoList = self.bindInfoCache["data"]
        totalInfo = self.bindInfoCache["total"]
        self.setPageInfo(totalInfo)
        self.table.setRowCount(len(self.bindInfoList))
        for rowIndex, row in enumerate(self.bindInfoList):
            for colIndex, cel_data in enumerate(row):
                if colIndex == 0:
                    self.table.setItem(rowIndex, colIndex, QTableWidgetItem(cel_data))
                elif colIndex == 1:
                    comboBox = self.setCellComboBox(self.devClassOps, rowIndex, colIndex, cel_data)
                    comboBox.currentIndexChanged.connect(partial(self.changeDevModelItem, rowIndex))
                elif colIndex == 2:
                    self.setCellComboBox(self.devClassModelDict.get(row[1]), rowIndex, colIndex, cel_data)
                elif colIndex == 3:
                    self.setCellComboBox(self.commPortOps, rowIndex, colIndex, cel_data)
                elif colIndex == 4:
                    self.setCellComboBox(self.devStatusOps, rowIndex, colIndex, cel_data)
            self.setRowDetailBtn(rowIndex, 5)
            self.setRowDeleteBtn(rowIndex, 6)

    def setPageInfo(self, total: int):
        """
        设置分页信息
        @param total: 数据总条数
        @return:
        """
        self.totalPage = math.ceil(total / self.pageSize)
        if self.pageIndex == 1:
            self.prePage.setEnabled(False)
        if self.totalPage == 1:
            self.nextPage.setEnabled(False)
        else:
            self.nextPage.setEnabled(True)
        self.pageLabel.setText(f"共{total}条   页数{self.pageIndex}/{self.totalPage}")

    def addRow(self):
        """
        新增一行数据，并设置下拉框的值
        @return:
        """
        if init_config.is_local_run():
            InfoBar.error("提示", "本地运行，不可绑定设备信息！", parent=self.parent)
            return
        totalCount = len(self.bindInfoList)
        rowCount = self.table.rowCount()
        if rowCount - totalCount > 0:
            InfoBar.warning(title="提示", content="请先保存后添加！", parent=self.parent)
            return
        self.table.insertRow(rowCount)
        for colIndex in range(self.table.columnCount()):  # 为每一列设置下拉框
            if colIndex == 1:
                box = self.setCellComboBox(self.devClassOps, rowCount, colIndex, None)
                box.currentIndexChanged.connect(partial(self.changeDevModelItem, rowCount))
            elif colIndex == 2:
                self.setCellComboBox(self.devModelOps, rowCount, colIndex, None)
            elif colIndex == 3:
                self.setCellComboBox(self.commPortOps, rowCount, colIndex, None)
            elif colIndex == 4:
                self.setCellComboBox(self.devStatusOps, rowCount, colIndex, None)
            elif colIndex == 6:
                self.setRowDeleteBtn(rowCount, colIndex)

    def setCellComboBox(self, result, rowIndex, colIndex, celData) -> ComboBox:
        """
        给指定单元格设置下拉框组件
        @param result: 下拉框待选项
        @param rowIndex: 行索引
        @param colIndex: 列索引
        @param celData: 已有值
        @return: 下拉框对象
        """
        combo_box = ComboBox()
        combo_box.setMaximumSize(200, 30)
        combo_box.setMinimumSize(20, 30)
        combo_box.setFont(self.MFont)
        combo_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        if result:
            for item in result:
                combo_box.addItem(item[0], userData=item[1])
                index = combo_box.findData(celData)
                combo_box.setCurrentIndex(index)
        self.table.setCellWidget(rowIndex, colIndex, combo_box)
        return combo_box

    def setRowDetailBtn(self, rowIndex, colIndex):
        """
        添加行内详情按钮
        @param rowIndex: 行索引
        @param colIndex: 列索引
        @return:
        """
        details_button = TransparentPushButton(self.table)
        details_button.setText("绑定详情")
        details_button.setMaximumHeight(30)
        details_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        details_button.setFont(self.MFont)
        details_button.setCursor(QCursor(Qt.PointingHandCursor))
        details_button.clicked.connect(self.openDetailPage)
        self.table.setCellWidget(rowIndex, colIndex, details_button)

    def setRowDeleteBtn(self, rowIndex, colIndex):
        """
        添加行内删除按钮
        @param rowIndex: 行索引
        @param colIndex: 列索引
        @return:
        """
        delete_button = TransparentPushButton(self.table)
        delete_button.setText("删除")
        delete_button.setMaximumHeight(30)
        delete_button.setFont(self.MFont)
        delete_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        delete_button.clicked.connect(self.removeRow)
        self.table.setCellWidget(rowIndex, colIndex, delete_button)

    def changeDevModelItem(self, row, index):
        """
        根据设备类型变化动态修改设备型号
        @param row: 行号
        @param index: 选中设备类型在选项中的索引
        @return:
        """
        # 选中项对应的元组值 eg: ('101-数字键盘', '101')
        dev_cls = self.devClassOps[index]
        # 根据设备类型id 获取对应的设备型号 选项列表
        dev_model_item: list = self.devClassModelDict[dev_cls[1]]
        # 获取第二列单元格的下拉框对象
        colIndex = 2
        cell_widget: ComboBox = self.table.cellWidget(row, colIndex)
        # 清空原有选项
        cell_widget.clear()
        # 将新的选项添加到设备型号下拉框
        for item in dev_model_item:
            cell_widget.addItem(item[0], userData=item[1])

    def openDetailPage(self):
        """
        展示详情
        @return:
        """
        if init_config.is_local_run():
            InfoBar.error("提示", "本地运行，无详情信息！", parent=self.parent)
            return
        sender = self.sender()  # 获取发送信号的按钮对象
        index = self.table.indexAt(sender.pos())  # 获取按钮所在的单元格索引
        row = index.row()  # 获取按钮所在的行号
        bindId = self.table.item(row, 0).text()

        if self.detailWin:
            self.detailWin.close()
            self.detailWin = None
        self.detailWin = DetailWindow(bindId, self.termId.text(), self.commPortOps, self.devStatusDict)
        self.detailWin.show()

    def removeRow(self):
        """
        删除一行
        @return:
        """
        if init_config.is_local_run():
            InfoBar.error("提示", "本地运行，无法删除配置信息！", parent=self.parent)
            return
        sender = self.sender()  # 获取发送信号的按钮对象
        index = self.table.indexAt(sender.pos())  # 获取按钮所在的单元格索引
        row = index.row()  # 获取按钮所在的行号
        messageBox = MessageBox("删除提示", "是否删除当前数据?", self.parent)
        messageBox.yesButton.setText("删除")
        messageBox.cancelButton.setText("取消")
        if messageBox.exec():
            if self.table.item(row, 0) is None:
                self.table.removeRow(row)
            else:
                bindId = self.table.item(row, 0).text()
                respBody = self.devBindCall.deleteBindDev(bindId)
                if respBody.get("success", None):
                    InfoBar.success("提示", "删除成功！", parent=self.parent)
                self.refurbishData()

    def refurbishData(self):
        """刷新表格及下拉框数据"""
        self.pageIndex = 1
        self.getBindInfo()
        self.setTableData()

    def saveUpdate(self):
        """ 保存 """
        if init_config.is_local_run():
            return
        self.saveOrUpdateTerminalInfo()
        self.saveOrUpdateBindInfo()

    def saveOrUpdateTerminalInfo(self):
        """保存或更新终端信息"""
        term_info = {"termModelId": self.termModel.currentData(),
                     "termFeature": self.termMac.text(),
                     "termDesc": self.termName.text()}
        if self.termId.text() == "":
            respBody = self.terminalInfoCall.addTerminalInfo(term_info)
            if respBody and respBody.get("success", []):
                self.initTerminalInfo()
                InfoBar.success("提示", "保存终端信息成功！", parent=self.parent)
            elif respBody:
                InfoBar.error("提示", f"{respBody['errCode']}:{respBody['errMessage']}!", parent=self.parent)
        else:
            term_info["termId"] = self.termId.text()
            self.terminalInfoCall.updateTerminalInfo(term_info)

    def saveOrUpdateBindInfo(self):
        """ 保存或更新绑定数据 """
        rowCount = self.table.rowCount()  # 点击保存时数据条数
        reqCount = len(self.bindInfoList)  # 请求到的数据条数
        updateCmdList: List[Dict] = []
        for row in range(rowCount):
            row_data = []
            for column in range(self.table.columnCount()):
                if column >= 5:
                    break
                if column == 0:
                    item = self.table.item(row, column)
                    if item:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                else:
                    item: QComboBox = self.table.cellWidget(row, column)
                    userData = item.currentData()
                    row_data.append(userData)
            if row < reqCount and row_data != self.bindInfoList[row]:
                bindInfo = TerminalDeviceBind(row_data[0], self.termId.text(), row_data[2], row_data[3], row_data[4])
                if bindInfo.commPort is None or bindInfo.commPort == "":
                    InfoBar.warning("提示", "通讯端口应有值！", parent=self.parent)
                    return
                else:
                    updateCmdList.append(bindInfo.__dict__)
            elif row_data[0] == "":
                # 没有bindId则调新增接口
                bindInfo = TerminalDeviceBind(row_data[0], self.termId.text(), row_data[2], row_data[3], row_data[4])
                respBody = self.devBindCall.addBindDev(bindInfo.__dict__)
                if respBody and respBody.get("success", None):
                    InfoBar.success("提示", "新增成功！", parent=self.parent)
                else:
                    InfoBar.error("提示", f"{respBody['errCode']}:{respBody['errMessage']}！",
                                  parent=self.parent)
                self.refurbishData()
        if len(updateCmdList) > 0:
            success = self.devBindCall.batchUpdateBindDev(updateCmdList)
            if success:
                InfoBar.success("提示", f"{len(updateCmdList)}条绑定信息已更新成功！", parent=self.parent)
            else:
                InfoBar.error("提示", "更新失败！", duration=3000, parent=self.parent)
            self.refurbishData()

    def saveAndRestart(self):
        """ 保存并重启服务"""
        # w = Dialog(title, content, self.window())
        register: TaskRegister = TaskRegister()
        task_manager: DeviceTaskManager = DeviceTaskManager()
        register.finished.connect(self.task_finished)

        if len(register.task_cache) > 0:
            messageBox = MessageBox("重启提示", "重启将清空当前所有任务，确认重启？", self.parent)
            messageBox.yesButton.setText("确认")
            messageBox.cancelButton.setText("稍后")
            if messageBox.exec():
                # 确认之后清空就绪任务
                for task_container in task_manager.task_containers.values():
                    task_container.clear_task()
                self.restart_flag = True
                messageBox = MessageBox("", "当前任务结束后将自动重启", self.parent)
                messageBox.cancelButton.hide()
                messageBox.yesButton.setText("好的")
                if messageBox.exec():
                    pass
                # if not self.task_finished:
                #     messageBox = MessageBox("", "当前任务结束后将自动重启", self.parent)
                #     messageBox.yesButton.setText("好的")
                # while True:
                #     print(self.task_finished)
                # self.restart()
        else:
            self.restart()

    def task_finished(self):
        if self.restart_flag:
            self.restart()

    def restart(self):
        self.parent.close()
        start = time.time()
        self.saveUpdate()
        send_request.isTimeOut = False
        reset_req_data = '{"function":"SystemRestart","type":"request","param":{}}'
        controller = DeviceController()
        controller.execute(reset_req_data, None)
        self.init()
        end = time.time()
        logger.info("重启应用耗时" + str(end - start) + "秒")
        self.parent.show()

    def toPrePage(self):
        """ 上一页按钮点击事件 """
        if self.totalPage != 0:
            self.pageIndex -= 1
            self.getBindInfo()
            self.setTableData()
            self.nextPage.setEnabled(True)
            if self.pageIndex == 1:
                self.prePage.setEnabled(False)

    def toNextPage(self):
        """ 下一页按钮点击事件 """
        if self.totalPage != 0:
            self.pageIndex += 1
            self.getBindInfo()
            self.setTableData()
            self.prePage.setEnabled(True)
            if self.pageIndex == self.totalPage:
                self.nextPage.setEnabled(False)

    def initWindow(self):
        """
        初始化窗口
        @return:
        """
        stretch_ratios = [2, 3, 1, 2, 3]
        self.globalLayout = QVBoxLayout(self)
        self.section1Layout = QHBoxLayout()
        self.group1 = QGroupBox(title="本终端信息")
        self.group1.setContentsMargins(0, 0, 50, 0)
        # 设置分组为垂直布局
        self.group1Layout = QVBoxLayout()
        self.group1.setLayout(self.group1Layout)
        self.row1Layout = QHBoxLayout()
        # 第一组第一行
        self.termMac_label = CaptionLabel(self.group1)
        self.termMac_label.setText("本终端MAC地址")
        self.termMac_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.termMac = LineEdit(self.group1)
        self.termMac.setReadOnly(True)
        self.termMac.setMaximumHeight(30)
        self.spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.termId_label = CaptionLabel(self.group1)
        self.termId_label.setText("本终端id")
        self.termId_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.termId = LineEdit(self.group1)
        self.termId.setReadOnly(True)
        self.termId.setMaximumHeight(30)
        self.row1Layout.addWidget(self.termMac_label)
        self.row1Layout.addWidget(self.termMac)
        self.row1Layout.addItem(self.spacer2)
        self.row1Layout.addWidget(self.termId_label)
        self.row1Layout.addWidget(self.termId)
        for index, ratio in enumerate(stretch_ratios):
            self.row1Layout.setStretch(index, ratio)

        # 第一组第二行内容
        self.row2Layout = QHBoxLayout()
        self.termModel_label = CaptionLabel(self.group1)
        self.termModel_label.setText("本终端型号")
        self.termModel_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.termModel = ComboBox(self.group1)
        self.termModel.setFont(self.MFont)
        self.termModel.setMaximumHeight(30)
        self.spacer3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.termName_label = CaptionLabel(self.group1)
        self.termName_label.setText("本终端名称")
        self.termName_label.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.termName = LineEdit(self.group1)
        self.termName.setFont(self.MFont)
        self.termName.setMaximumHeight(30)
        self.row2Layout.addWidget(self.termModel_label)
        self.row2Layout.addWidget(self.termModel)
        self.row2Layout.addItem(self.spacer3)
        self.row2Layout.addWidget(self.termName_label)
        self.row2Layout.addWidget(self.termName)
        for index, ratio in enumerate(stretch_ratios):
            self.row2Layout.setStretch(index, ratio)

        self.group1Layout.addLayout(self.row1Layout)
        self.group1Layout.addLayout(self.row2Layout)
        self.spacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.section1Layout.addWidget(self.group1)
        self.section1Layout.addItem(self.spacer1)
        self.section1Layout.setStretch(0, 4)
        self.section1Layout.setStretch(1, 1)
        # 将第一组布局添加至全局布局
        self.globalLayout.addLayout(self.section1Layout)
        # 第二组内容

        self.group2 = QGroupBox("本终端设备")
        self.group2layout = QVBoxLayout()
        self.group2.setLayout(self.group2layout)
        # 第二组第一行
        self.group2row1 = QHBoxLayout()
        self.addBtn = PrimaryPushButton(self.group2)
        self.addBtn.setText("新增")
        self.addBtn.setMinimumSize(100, 25)
        self.addBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.addBtn.clicked.connect(self.addRow)

        self.useTempBtn = PrimaryPushButton(self.group2)
        self.useTempBtn.setText("使用模板")
        self.useTempBtn.setMinimumSize(QSize(100, 25))
        self.useTempBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.spacer4 = QSpacerItem(600, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.refurbish = TransparentToolButton(FluentIcon.SYNC, self.group2)
        self.refurbish.setMinimumSize(QSize(25, 25))
        self.refurbish.setCursor(QCursor(Qt.PointingHandCursor))
        self.refurbish.clicked.connect(self.refurbishData)

        self.group2row1.addWidget(self.addBtn)
        self.group2row1.addWidget(self.useTempBtn)
        self.group2row1.addItem(self.spacer4)
        self.group2row1.addWidget(self.refurbish)
        self.group2layout.addLayout(self.group2row1)
        # 第二组表格
        self.table = TableWidget(self.group2)
        self.group2layout.addWidget(self.table)
        # 自定义分页组件
        self.pageLayout = QHBoxLayout()

        self.spacerLeft = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.pageLayout.addItem(self.spacerLeft)
        self.prePage = TransparentToolButton(FluentIcon.PAGE_LEFT, self.group2)
        self.prePage.setCursor(QCursor(Qt.PointingHandCursor))
        self.prePage.clicked.connect(self.toPrePage)
        self.pageLayout.addWidget(self.prePage)

        self.pageLabel = CaptionLabel(self.group2)
        self.pageLabel.setText('总条数 0  页数0/0 ')
        self.pageLabel.setTabletTracking(False)
        self.pageLabel.setContextMenuPolicy(Qt.NoContextMenu)
        self.pageLabel.setAlignment(Qt.AlignCenter)
        self.pageLayout.addWidget(self.pageLabel)

        self.nextPage = TransparentToolButton(FluentIcon.PAGE_RIGHT, self.group2)
        self.nextPage.setCursor(QCursor(Qt.PointingHandCursor))
        self.nextPage.clicked.connect(self.toNextPage)
        self.pageLayout.addWidget(self.nextPage)

        self.spacerRight = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.pageLayout.addItem(self.spacerRight)
        self.group2layout.addLayout(self.pageLayout)

        # 将第二组内容添加至全局布局
        self.globalLayout.addWidget(self.group2)
        # 底部操作按钮行
        self.horLayoutBottom = QHBoxLayout()
        self.spacer5 = QSpacerItem(258, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horLayoutBottom.addItem(self.spacer5)

        self.save = PrimaryPushButton(self)
        self.save.setText("保存")
        self.save.setMinimumSize(100, 25)
        self.save.setCursor(QCursor(Qt.PointingHandCursor))
        self.save.clicked.connect(self.saveUpdate)
        self.horLayoutBottom.addWidget(self.save)

        self.saveRestart = PrimaryPushButton(self)
        self.saveRestart.setText("保存并重启")
        self.saveRestart.setMinimumSize(100, 25)
        self.saveRestart.setCursor(QCursor(Qt.PointingHandCursor))
        self.saveRestart.clicked.connect(self.saveAndRestart)
        self.horLayoutBottom.addWidget(self.saveRestart)

        # 将底部操作按钮添加至全局布局
        self.globalLayout.addLayout(self.horLayoutBottom)

        self.globalLayout.setStretch(0, 1)
        self.globalLayout.setStretch(1, 4)
        self.globalLayout.setStretch(2, 1)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 设置qt界面大小与原设计界面比例相同

    app = QApplication()
    # app.setStyle(QStyleFactory.create('Fusion'))
    self = DeviceInterface()
    self.show()
    app.exec_()
