from typing import List, Dict

from PySide2.QtCore import Qt, Slot, Signal
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QFrame, QVBoxLayout, QHeaderView, QTableWidgetItem, QSizePolicy
from qfluentwidgets import TableWidget, TransparentPushButton, InfoBar, InfoBarPosition

import logger.device_logger
from device.base_device import Device
from driver.cache.cache import DriverCache
from driver.driver_factory import DriverFactory
from logger.device_logger import logger
from model.task_model.base_task import Task, TaskStatus
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.device_task import DeviceTask
from task.container import TaskRegister
from view.qtwidgets.gallery_interface import GalleryInterface


class TaskInterface(GalleryInterface):
    def __init__(self, parent=None):
        super().__init__("任务列表", parent)
        self.parent = parent
        self.setObjectName('TaskInterface')
        self.taskFrame = TaskFrame(self.parent)
        self.vBoxLayout.addWidget(self.taskFrame)


class TaskFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__()
        # 父窗口
        self.parent = parent
        self.initVew()
        self.task_dict: Dict[str, List] = {}
        self.driver_key_dict: Dict[str, str] = {}

    def init(self):
        self.task_register: TaskRegister = TaskRegister()
        self.driver_cache: DriverCache = DriverCache()
        self.task_register.send_task_signal.connect(self.receive_add_data)

    def initVew(self):
        layout = QVBoxLayout(self)  # 使用垂直布局管理器
        self.table = TableWidget(self)
        self.table.setBorderVisible(True)
        self.table.setBorderRadius(8)
        self.table.setColumnCount(7)
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(TableWidget.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(['任务id', '任务名称', '设备类型', '设备型号', '端口', '任务状态', '操作'])
        # 设置表格的大小策略，使其可以水平和垂直扩展到父容器的尺寸
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 设置每列根据内容自适应宽度
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.table)

    @Slot(str, object)
    def receive_add_data(self, flag: str, task: Task):
        if "A" == flag:
            logger.info("添加任务:{0}".format(task.id))
            task_info = self.parse_task(task)
            self.task_dict[task.id] = task_info
            self.update_table(list(self.task_dict.values()))
        elif "D" == flag:
            logger.info("结束任务:{0}".format(task.id))
            if self.task_dict.get(task.id, None):
                del self.task_dict[task.id]
                self.update_table(list(self.task_dict.values()))
        elif "U" == flag:
            logger.info("执行任务:{0}".format(task.id))
            if self.task_dict.get(task.id, None):
                self.task_dict[task.id][5] = TaskStatus.RUN.name
                self.update_table(list(self.task_dict.values()))

    def parse_task(self, task: Task):
        if isinstance(task, DeviceTask):
            context = task.request_context
            task_desc = task.task_desc
            if isinstance(context, DeviceRequestContext):
                request_id = context.request_id
                driver_key = context.driver_key
                cfg = context.device_cfg
                port = cfg.port.port_id
                device_class = cfg.device_class + "-" + cfg.device_class_desc
                device_model = cfg.device_model + "-" + cfg.device_model_desc
                status = task.status.name
                self.driver_key_dict[request_id] = driver_key
                return [request_id, task_desc, device_class, device_model, port, status]

    def update_table(self, tasks: List[List]):
        rowCount = len(tasks)
        self.table.setRowCount(rowCount)
        for rowIndex, row in enumerate(tasks):
            for columnIndex, cell_data in enumerate(row):
                item = QTableWidgetItem(cell_data)
                self.table.setItem(rowIndex, columnIndex, item)
            cancel_btn = TransparentPushButton(self.table)
            cancel_btn.setText("取消任务")
            cancel_btn.setMaximumHeight(30)
            cancel_btn.setCursor(QCursor(Qt.PointingHandCursor))
            cancel_btn.clicked.connect(self.cancel_task)
            self.table.setCellWidget(rowIndex, 6, cancel_btn)

    def cancel_task(self):
        sender = self.sender()
        rowIndex = self.table.indexAt(sender.pos()).row()
        request_id = self.table.item(rowIndex, 0).text()
        task = self.task_register.get_task(request_id)
        driver_key = self.driver_key_dict.get(request_id)
        device: Device = self.driver_cache.get_driver(driver_key)
        # 如果是正在执行的任务，拿到设备驱动调用设备的取消，完了之后设置任务状态为取消
        if self.table.item(rowIndex, 5).text() == TaskStatus.RUN.name:
            if not device:
                if isinstance(task, DeviceTask):
                    context = task.request_context
                    if isinstance(context, DeviceRequestContext):
                        device = DriverFactory().get_device(context.device_cfg)
            flag = device.is_cancel()
            if flag:
                cancel = device.cancel()
                if cancel == 0:
                    logger.info('取消任务{0}'.format(task.id))
                    task.status = TaskStatus.CANCEL
                    InfoBar.success("提示", f"任务{request_id}已取消", InfoBarPosition.TOP,
                                    parent=self.parent)
            else:
                InfoBar.warning("提示", "该设备不支持取消任务！", InfoBarPosition.TOP,
                                parent=self.parent)
        else:
            task.status = TaskStatus.CANCEL
            del self.task_dict[request_id]
            self.table.removeRow(rowIndex)
            InfoBar.success("提示", f"任务{request_id}已取消", InfoBarPosition.TOP,
                            parent=self.parent)
