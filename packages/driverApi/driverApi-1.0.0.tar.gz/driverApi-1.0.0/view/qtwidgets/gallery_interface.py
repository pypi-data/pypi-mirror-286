from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout
from qfluentwidgets import TitleLabel, TransparentToolButton, FluentIcon, toggleTheme


class ToolBar(QWidget):

    def __init__(self, title, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)
        self.hBoxLayout = QHBoxLayout(self)
        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(70)
        self.themeButton = TransparentToolButton(FluentIcon.CONSTRACT, self)
        self.themeButton.clicked.connect(toggleTheme)
        self.hBoxLayout.setContentsMargins(20, 40, 40, 0)
        self.hBoxLayout.addWidget(self.titleLabel)
        self.hBoxLayout.addWidget(self.themeButton)


class GalleryInterface(QFrame):
    """ Gallery interface """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.toolBar = ToolBar(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.toolBar)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.setObjectName('view')

    # def scrollToCard(self, index: int):
    #     w = self.vBoxLayout.itemAt(index).widget()
    #     self.verticalScrollBar().setValue(w.y())
    #
    # def resizeEvent(self, e):
    #     super().resizeEvent(e)
    #     self.toolBar.resize(self.width(), self.toolBar.height())
