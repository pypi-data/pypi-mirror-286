from PySide2.QtCore import QModelIndex, Qt
from PySide2.QtGui import QPalette, QColor
from PySide2.QtWidgets import QWidget, QStyleOptionViewItem, QStyledItemDelegate
from qfluentwidgets import TableItemDelegate


class MTableItemDelegate(TableItemDelegate):
    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        rect = option.rect
        y = rect.y() + (rect.height() - editor.height()) // 2
        x, w = max(0, rect.x()), rect.width()
        if index.column() == 0:
            pass

        editor.setGeometry(x, y, w, rect.height())


class ValueDelegate(QStyledItemDelegate):
    def __init__(self, column, parent=None):
        super().__init__(parent)
        self.column = column
        self.textDict = {
            "0": "就绪",
            "1": "初始化",
            "2": "忙碌",
            "3": "错误",
            "4": "未安装",
            "5": "未知",
            "6": "离线",
        }

    def paint(self, painter, option, index):
        value = index.data(Qt.DisplayRole)
        if index.column() == self.column:
            if value == "0":
                option.palette.setColor(QPalette.Text, QColor("green"))
            else:
                option.palette.setColor(QPalette.Text, QColor("red"))
        super().paint(painter, option, index)

    def displayText(self, value, locale):
        # 根据值进行文本渲染
        if self.column == 2:
            return self.textDict.get(value)
