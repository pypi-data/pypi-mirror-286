from tkinter import Tk, INSERT
from tkinter.ttk import Entry, Button, Label
from typing import List


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.label1 = self.label1(self)
        self.label2 = self.label2(self)
        self.label3 = self.label3(self)
        self.label4 = self.label4(self)
        self.label5 = self.label5(self)
        self.label11 = self.label11(self)
        self.label7 = self.label7(self)
        self.label8 = self.label8(self)
        self.label9 = self.label9(self)
        self.label10 = self.label10(self)
        self.cnName = self.cnName(self)
        self.sex = self.sex(self)
        self.nation = self.nation(self)
        self.birthday = self.birthday(self)
        self.address = self.address(self)
        self.dep = self.dep(self)
        self.begin = self.begin(self)
        self.end = self.end(self)
        self.image_path = self.image_path(self)
        self.image_info = self.image_info(self)
        self.cancel = self.cancel(self)
        self.commit = self.commit(self)
        self.label6 = self.label6(self)
        self.id = self.id(self)

    def __win(self):
        # 设置窗口大小、居中

        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        width = int(screenwidth / 2 - 50)
        height = int(screenheight / 2 - 20)
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.minsize(width=width, height=height)

    @staticmethod
    def label1(parent):
        label = Label(parent, text="姓     名", anchor="center", )
        label.place(relx=0.03333333333333333, rely=0.04926108374384237, relwidth=0.13333333333333333,
                    relheight=0.07389162561576355)
        return label

    @staticmethod
    def label2(parent):
        label = Label(parent, text="性      别", anchor="center", )
        label.place(relx=0.5, rely=0.04926108374384237, relwidth=0.13333333333333333, relheight=0.07389162561576355)
        return label

    @staticmethod
    def label3(parent):
        label = Label(parent, text="名     族", anchor="center", )
        label.place(relx=0.03333333333333333, rely=0.1477832512315271, relwidth=0.13333333333333333,
                    relheight=0.07389162561576355)
        return label

    @staticmethod
    def label4(parent):
        label = Label(parent, text="出生日期", anchor="center", )
        label.place(relx=0.5, rely=0.1477832512315271, relwidth=0.13333333333333333, relheight=0.07389162561576355)
        return label

    @staticmethod
    def label5(parent):
        label = Label(parent, text=" 居住地址", anchor="center", )
        label.place(relx=0.03333333333333333, rely=0.24630541871921183, relwidth=0.13333333333333333,
                    relheight=0.07389162561576355)
        return label

    @staticmethod
    def label6(parent):
        label = Label(parent, text=" 身份证号", anchor="center", )
        label.place(relx=0.03333333333333333, rely=0.3448275862068966, relwidth=0.13333333333333333,
                    relheight=0.07389162561576355)
        return label

    @staticmethod
    def label7(parent):
        label = Label(parent, text=" 发证机关", anchor="center", )
        label.place(relx=0.03333333333333333, rely=0.4433497536945813, relwidth=0.13, relheight=0.07389162561576355)
        return label

    @staticmethod
    def label8(parent):
        label = Label(parent, text=" 生效日期", anchor="center", )
        label.place(relx=0.03333333333333333, rely=0.541871921182266, relwidth=0.13333333333333333,
                    relheight=0.07389162561576355)
        return label

    @staticmethod
    def label9(parent):
        label = Label(parent, text="失效日期", anchor="center", )
        label.place(relx=0.5, rely=0.541871921182266, relwidth=0.13333333333333333, relheight=0.07389162561576355)
        return label

    @staticmethod
    def label10(parent):
        label = Label(parent, text="身份证头像存储绝对路径", anchor="center", )
        label.place(relx=0.040, rely=0.6403940886699507, relwidth=0.24666666666666667, relheight=0.07389162561576355)
        return label

    @staticmethod
    def label11(parent):
        label = Label(parent, text="身份证头像BASE64数据", anchor="center", )
        label.place(relx=0.039, rely=0.7389162561576355, relwidth=0.24666666666666667,
                    relheight=0.07389162561576355)
        return label

    @staticmethod
    def cnName(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "李小龙")
        entry.place(relx=0.16666666666666666, rely=0.04926108374384237, relwidth=0.3, relheight=0.07389162561576355)
        return entry

    @staticmethod
    def sex(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "男")
        entry.place(relx=0.6333333333333333, rely=0.04926108374384237, relwidth=0.3, relheight=0.07389162561576355)
        return entry

    @staticmethod
    def nation(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "汉")
        entry.place(relx=0.16666666666666666, rely=0.1477832512315271, relwidth=0.3, relheight=0.07389162561576355)
        return entry

    @staticmethod
    def birthday(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "2000-01-01")
        entry.place(relx=0.6333333333333333, rely=0.1477832512315271, relwidth=0.3, relheight=0.07389162561576355)
        return entry

    @staticmethod
    def address(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "陕西省西安市雁塔区鱼化寨街道高档小区8号楼1101")
        entry.place(relx=0.16666666666666666, rely=0.24630541871921183, relwidth=0.7666666666666667,
                    relheight=0.07389162561576355)
        return entry

    @staticmethod
    def id(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "622654200808082379")
        entry.place(relx=0.16666666666666666, rely=0.3448275862068966, relwidth=0.7666666666666667,
                    relheight=0.07389162561576355)
        return entry

    @staticmethod
    def dep(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "陕西省西安市公安局")
        entry.place(relx=0.16666666666666666, rely=0.4433497536945813, relwidth=0.7666666666666667,
                    relheight=0.07389162561576355)
        return entry

    @staticmethod
    def begin(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "2005-01-01")
        entry.place(relx=0.16666666666666666, rely=0.541871921182266, relwidth=0.3, relheight=0.07389162561576355)
        return entry

    @staticmethod
    def end(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "2015-12-30")
        entry.place(relx=0.6333333333333333, rely=0.541871921182266, relwidth=0.3, relheight=0.07389162561576355)
        return entry

    @staticmethod
    def image_path(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "E://Temp/file")
        entry.place(relx=0.27333333333333334, rely=0.6403940886699507, relwidth=0.658, relheight=0.07389162561576355)

        return entry

    @staticmethod
    def image_info(parent):
        entry = Entry(parent)
        entry.insert(INSERT, "nc808ryocg8yrnx3hnx839xnxz983x9cn348cy9")
        entry.place(relx=0.27333333333333334, rely=0.7389162561576355, relwidth=0.658, relheight=0.07389162561576355)
        return entry

    @staticmethod
    def cancel(parent):
        btn = Button(parent, text="取消", takefocus=False, )
        btn.place(relx=0.3333333333333333, rely=0.8620689655172413, relwidth=0.15, relheight=0.08620689655172414)
        return btn

    @staticmethod
    def commit(parent):
        btn = Button(parent, text="确认", takefocus=False, )
        btn.place(relx=0.5833333333333334, rely=0.8620689655172413, relwidth=0.15, relheight=0.08620689655172414)
        return btn


class Win(WinGUI):
    def __init__(self, result, title, items: List[str]):
        """
        :param result: 需要返回的结果对象
        :param title: 窗口标题
        :param items: 输入项列表
        """
        super().__init__()
        self.title(title)
        self.__result = result
        self.__items = items
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.__event_bind()

    def on_closing(self):
        pass

    def commit_click(self):
        for item in self.__items:
            text = getattr(self, item)
            value_str = text.get()
            setattr(self.__result, item, f"{value_str}")
        self.withdraw()
        self.quit()

    def cancel_click(self):
        self.__result = None
        self.withdraw()
        self.quit()

    def getResult(self):
        return self.__result

    def __event_bind(self):
        self.commit.config(command=self.commit_click)
        self.cancel.config(command=self.cancel_click)
