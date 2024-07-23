from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QFrame
from qfluentwidgets import TitleLabel

from view.qtwidgets.gallery_interface import GalleryInterface


class HomeInterface(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('homeInterface')
        self.vBox = QVBoxLayout(self)
        self.vBox.setContentsMargins(10, 40, 10, 10)
        self.vBox.setSpacing(0)
        self.vBox.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)
        self.titleLabel = TitleLabel('外设工具', self)
        self.vBox.addWidget(self.titleLabel)
