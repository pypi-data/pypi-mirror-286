import threading
import time
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QHeaderView, QFrame, QTableWidgetItem
from qfluentwidgets import TableWidget

from device.status import DeviceStatus
from task.manager.device_status_manager import DeviceStatusManager
from view.qtwidgets.custom_delegate import ValueDelegate
from view.qtwidgets.gallery_interface import GalleryInterface


# 初始化外层界面布局
class StateInterface(GalleryInterface):
    def __init__(self, parent=None):
        super().__init__("设备状态", parent)
        self.setObjectName('StateInterface')
        self.stateFrame = StateFrame()
        self.vBoxLayout.addWidget(self.stateFrame)


class StateFrame(QFrame):
    """ 设备状态窗口 """

    def __init__(self):
        super().__init__()

        self.initView()
        self.manager = DeviceStatusManager()
        self.start_timer()

    def initView(self):
        layout = QVBoxLayout(self)  # 使用垂直布局管理器
        self.table = TableWidget(self)
        layout.addWidget(self.table)

        # 启用边框并设置圆角
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(TableWidget.NoEditTriggers)
        self.table.setWordWrap(False)
        self.table.setColumnCount(3)

        delegate = ValueDelegate(2, self.table)
        self.table.setItemDelegateForColumn(2, delegate)

        # 设置水平表头并隐藏垂直表头
        self.table.setHorizontalHeaderLabels(['设备类型', '设备型号', '设备状态'])
        self.table.verticalHeader().hide()

    def start_timer(self):
        thread = threading.Thread(target=self.setData)
        thread.name = "刷新表格线程"
        thread.daemon = True
        thread.start()

    def setData(self):
        while True:
            time.sleep(3)
            statusList: list[DeviceStatus] = self.manager.get_all_status()
            statusList = self.transferData(statusList)

            # 检查当前表格行数是否与新的数据行数相同
            if self.table.rowCount() != len(statusList):
                self.table.setRowCount(len(statusList))

            self.table.setColumnCount(3)
            for rowIndex, rowData in enumerate(statusList):
                for columnIndex, item in enumerate(rowData):
                    # 检查当前行是否存在 QTableWidgetItem
                    if self.table.item(rowIndex, columnIndex) is None:
                        tableItem = QTableWidgetItem(item)
                        self.table.setItem(rowIndex, columnIndex, tableItem)
                    else:
                        # 如果 QTableWidgetItem 已存在，则更新文本内容
                        self.table.item(rowIndex, columnIndex).setText(item)
                    # 设置 QTableWidgetItem 的属性
                    if columnIndex == 2:
                        self.table.item(rowIndex, columnIndex).setTextAlignment(Qt.AlignCenter)

    @staticmethod
    def transferData(data: List[DeviceStatus]) -> List:
        retInfo = []
        for deviceStatus in data:
            statusInfo = []
            statusDict = deviceStatus.__dict__
            statusInfo.append(f"{statusDict['dev_class']}-{statusDict['dev_class_desc']}")
            statusInfo.append(f"{statusDict['dev_model']}-{statusDict['dev_model_desc']}")
            statusInfo.append(str(statusDict['status_type'].value))
            retInfo.append(statusInfo)
        return retInfo
