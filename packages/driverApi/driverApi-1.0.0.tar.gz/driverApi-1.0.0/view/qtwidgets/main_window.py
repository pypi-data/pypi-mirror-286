# coding:utf-8
import os

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon, QScreen
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QAction
from qfluentwidgets import NavigationItemPosition, SplitFluentWindow, FluentIcon, SystemTrayMenu, SplashScreen, \
    setThemeColor, setTheme, Theme

from driver.impl import MockKeypad, MockIDCardReader, MockMagnetIC, MockFinanceIcCard
from logger.device_logger import logger
from view.icon import app_icon
from .device_interface import DeviceInterface
from .state_interface import StateInterface
from .task_interface import TaskInterface
from view.mockdialog.ic_card_dialog import FinanceIcCardView
from view.mockdialog.id_card_dialog import IdCardView
from view.mockdialog.keypad_dialog import KeyPadView
from view.mockdialog.magnetic_dialog import MagneticView


class MainWindow(SplitFluentWindow):

    def __init__(self, conn):
        super().__init__()
        self.initWindow()
        self.conn = conn
        # 创建子接口
        # self.homeInterface = HomeInterface(self)
        self.deviceInterface = DeviceInterface(self)
        self.stateInterface = StateInterface(self)
        self.taskInterface = TaskInterface(self)
        # 将项目添加到导航界面
        self.initNavigation()
        # 创建系统托盘
        self.initTrayWin()
        # self.setWindowGeometry()
        # 初始化模拟界面以及信号绑定
        self.init_mock_view()
        self.splashScreen.finish()
        setThemeColor('#36A2FC')
        setTheme(Theme.LIGHT)

    def init_mock_view(self):
        self.mock_keypad = MockKeypad()
        self.mock_idcard = MockIDCardReader()
        self.mock_magnetc = MockMagnetIC()
        self.mock_iccard = MockFinanceIcCard()
        self.mock_keypad.signal.keypad_read_signal.connect(self.showKeypadDialog)
        self.mock_idcard.signal.idcard_read_signal.connect(self.showIDCardDialog)
        self.mock_magnetc.signal.magnetic_read_signal.connect(self.showMagneticDialog)
        self.mock_iccard.signal.iccard_read_signal.connect(self.showIcCardDialog)

    def showKeypadDialog(self, prompt):
        self.keypad_dialog = KeyPadView(prompt)
        self.keypad_dialog.finished.connect(self.mock_keypad.read_finished)
        self.keypad_dialog.exec_()

    def showIDCardDialog(self, idcardInfo):
        self.idcard_dialog = IdCardView(idcardInfo)
        self.idcard_dialog.finished.connect(self.mock_idcard.read_finished)
        self.idcard_dialog.exec_()

    def showMagneticDialog(self, magneticInfo):
        self.magnetic_dialog = MagneticView(magneticInfo)
        self.magnetic_dialog.finished.connect(self.mock_magnetc.read_finished)
        self.magnetic_dialog.exec_()

    def showIcCardDialog(self, financeICInfo):
        self.iccard_dialog = FinanceIcCardView(financeICInfo)
        self.iccard_dialog.finished.connect(self.mock_iccard.read_finished)
        self.iccard_dialog.exec_()

    def initNavigation(self):
        self.navigationInterface.setExpandWidth(200)
        # self.addSubInterface(self.homeInterface, FluentIcon.HOME, '首页')
        # self.navigationInterface.addSeparator()
        pos = NavigationItemPosition.TOP
        self.addSubInterface(self.deviceInterface, FluentIcon.APPLICATION, '设备配置', pos)
        self.addSubInterface(self.stateInterface, FluentIcon.SPEED_HIGH, '设备状态', pos)
        self.addSubInterface(self.taskInterface, FluentIcon.LIBRARY, '任务列表', pos)

    def initWindow(self):
        self.resize(1000, 700)
        logger.info(app_icon)
        self.setWindowIcon(QIcon(":/icon.ico"))
        self.setWindowTitle('外设工具')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
        self.show()

        QApplication.processEvents()

    def initTrayWin(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon(":/icon.ico"))
        self.trayMenu = SystemTrayMenu(self)
        self.trayMenu.addAction(QAction("主界面", self, triggered=self.showMainWin))
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(QAction("重启", self, triggered=self.restart))
        self.trayMenu.addAction(QAction("退出", self, triggered=self.quit))
        self.tray.activated.connect(self.on_tray_icon_clicked)
        self.tray.setContextMenu(self.trayMenu)
        self.tray.show()

    def setWindowGeometry(self):
        self.resize(1000, 700)
        self.setWindowIcon(QIcon(":/icon.ico"))
        self.setWindowTitle('外设工具')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def on_tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def initCfgData(self):
        # 初始化设备配置信息
        self.deviceInterface.deviceFrame.init()
        # # 初始化任务列表
        self.taskInterface.taskFrame.init()

    def showMainWin(self):
        self.show()

    def restart(self):
        self.deviceInterface.deviceFrame.saveAndRestart()

    def quit(self):
        QApplication.quit()
        self.conn.send("terminate")  # 发送终止信号到主进程
        self.conn.close()
        os._exit(0)

    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())
