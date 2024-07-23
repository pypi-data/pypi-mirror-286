from tkinter import *
from tkinter.ttk import *
from typing import List

from driver.magnetic_strip_rwer import MagneticStripInfo


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.label1 = self.label1(self)
        self.label2 = self.label2(self)
        self.label3 = self.label3(self)
        self.label4 = self.label4(self)
        self.card_no = self.card_no(self)
        self.stack1_info = self.stack1_info(self)
        self.stack2_info = self.stack2_info(self)
        self.stack3_info = self.stack3_info(self)
        self.commit = self.commit(self)
        self.cancel = self.cancel(self)

    def __win(self):
        self.title("Tkinter布局助手")
        # 设置窗口大小、居中
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        width = int(screenwidth / 2.5)
        height = int(screenheight / 2.5)
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.minsize(width=width, height=height)

    @staticmethod
    def label1(parent):
        label = Label(parent, text="卡号", anchor="e", )
        label.place(relx=0.07393715341959335, rely=0.10498687664041995, relwidth=0.18484288354898337,
                    relheight=0.07874015748031496)
        return label

    @staticmethod
    def label2(parent):
        label = Label(parent, text="一磁道数据", anchor="e", )
        label.place(relx=0.07393715341959335, rely=0.3087139107611549, relwidth=0.18484288354898337,
                    relheight=0.07874015748031496)
        return label

    @staticmethod
    def label3(parent):
        label = Label(parent, text="二磁道数据 ", anchor="e", )
        label.place(relx=0.07393715341959335, rely=0.4961942257217848, relwidth=0.18484288354898337,
                    relheight=0.07874015748031496)
        return label

    @staticmethod
    def label4(parent):
        label = Label(parent, text="三磁道数据", anchor="e", )
        label.place(relx=0.07393715341959335, rely=0.6899212598425197, relwidth=0.18484288354898337,
                    relheight=0.07874015748031496)
        return label

    @staticmethod
    def card_no(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "6217998340006985046")
        entry.place(relx=0.27726432532347506, rely=0.10498687664041995, relwidth=0.609981515711645,
                    relheight=0.07874015748031496)
        return entry

    @staticmethod
    def stack1_info(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "")
        entry.place(relx=0.27726432532347506, rely=0.26246719160104987, relwidth=0.609981515711645,
                    relheight=0.10874015748031496)
        return entry

    @staticmethod
    def stack2_info(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "6217998340006985046=28092200200600000")
        entry.place(relx=0.27726432532347506, rely=0.4461942257217848, relwidth=0.609981515711645,
                    relheight=0.10874015748031496)
        return entry

    @staticmethod
    def stack3_info(parent):
        entry = Entry(parent)
        entry.insert(INSERT,
                     "996217998340006985046=1561560000000000000003000000114000028091=000000000000=000000000000=000000002006000")
        entry.place(relx=0.27726432532347506, rely=0.6499212598425197, relwidth=0.609981515711645,
                    relheight=0.10874015748031496)
        return entry

    @staticmethod
    def cancel(parent):
        btn = Button(parent, text="取消", takefocus=False, )
        btn.place(relx=0.33271719038817005, rely=0.8198950131233596, relwidth=0.16635859519408502,
                  relheight=0.09874015748031496)
        return btn

    @staticmethod
    def commit(parent):
        btn = Button(parent, text="确认", takefocus=False, )
        btn.place(relx=0.5914972273567468, rely=0.8198950131233596, relwidth=0.16635859519408502,
                  relheight=0.09874015748031496)
        return btn


class Win(WinGUI):
    def __init__(self, title, items: List[str]):
        """
        :param title: 窗口标题
        :param items: 输入项列表
        """
        super().__init__()
        self.title(title)
        self.__result = None
        self.__items = items
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.__event_bind()

    def on_closing(self):
        pass

    def commit_click(self):
        self.__result = MagneticStripInfo()
        for item in self.__items:
            text = getattr(self, item)
            value_str = text.get()
            setattr(self.__result, item, f"{value_str}")
        self.withdraw()
        self.quit()

    def cancel_click(self):
        self.withdraw()
        self.quit()

    def getResult(self):
        return self.__result

    def __event_bind(self):
        self.commit.config(command=self.commit_click)
        self.cancel.config(command=self.cancel_click)


if __name__ == "__main__":
    win = Win(None, "测试", [])
    win.mainloop()
