# author: haoliqing
# date: 2023/10/25 14:19
# desc:
import tkinter
from typing import List


class ViewItem(object):

    def __init__(self, text: str, attr_name: str, def_value: str = None):
        """
        用于构建界面输入项的属性
        :param text: Label描述
        :param attr_name:  结果属性ID
        :param def_value:  默认值
        """

        self.text = text
        self.attr_name = attr_name
        self.def_value = def_value


class MockDevicePanel(object):

    def __init__(self, result, title, items: List[ViewItem]):
        """
        :param result: 需要返回的结果对象
        :param title: 窗口标题
        :param items: 输入项列表
        """
        self.__result = result
        self.__items = items
        self.id_window = tkinter.Tk()
        self.id_window.protocol('WM_DELETE_WINDOW', self.on_window_x_close)
        self.id_window.title(title)
        self.id_window.geometry('1068x681+10+10')
        row_num = 0
        for item in items:
            label = tkinter.Label(self.id_window, text=item.text)
            label.grid(row=row_num, column=0)
            text = tkinter.Text(self.id_window, width=50, height=1, undo=True, autoseparators=False)
            text.grid(row=row_num, column=1)
            if item.def_value:
                text.insert(tkinter.INSERT, item.def_value)
            setattr(self, "label" + str(row_num), label)
            setattr(self, "text" + str(row_num), text)
            row_num += 1

        self.commit_button = tkinter.Button(self.id_window, text="确定", bg="lightblue", width=10,
                                            command=self.commit_click)  # 调用内部方法  加()为直接调用
        self.commit_button.grid(row=row_num, column=0)
        self.cancel_button = tkinter.Button(self.id_window, text="取消", bg="lightblue", width=10,
                                            command=self.cancel_click)  # 调用内部方法  加()为直接调用
        self.cancel_button.grid(row=row_num, column=1)
        self.id_window.mainloop()

    def commit_click(self):
        index = 0
        for item in self.__items:
            text = getattr(self, "text" + str(index))
            value_str = text.get(1.0, tkinter.END)
            setattr(self.__result, item.attr_name, value_str)
        self.id_window.destroy()

    def cancel_click(self):
        self.__result = None
        self.id_window.destroy()

    def get_result(self):
        return self.__result

    def on_window_x_close(self):
        self.__result = None
        self.id_window.destroy()


