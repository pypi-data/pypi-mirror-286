from tkinter import Tk, font, END
from tkinter.ttk import Entry, Label, Button


class WinGUI(Tk):
    def __init__(self, flag):
        super().__init__()
        self.__win()
        self.label = self.label(self, flag)
        if flag == 0 or flag == 1:
            self.password = self.password(self, show='●')
        else:
            self.password = self.password(self)
        self.commit = self.commit(self)
        self.cancel = self.cancel(self)

    def __win(self):
        # 设置窗口大小、居中
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        width = int(screenwidth / 3)
        height = int(screenheight / 5)
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.minsize(width=width, height=height)

    @staticmethod
    def label(parent, flag):
        text = "请输入密码"
        if flag == 1:
            text = "请确认密码"
        elif flag == 2:
            text = "请输入手机号"
        elif flag == 3:
            text = "请输入验证码"
        label = Label(parent, text=text, anchor="e", font=font.Font(size=12))
        label.place(relx=0.10909090909090909, rely=0.1932367149758454, relwidth=0.19636363636363635,
                    relheight=0.1932367149758454)
        return label

    @staticmethod
    def password(parent, show=None):
        entry = Entry(parent, font=font.Font(size=8), show=show)
        entry.place(relx=0.3090909090909091, rely=0.2032367149758454, relwidth=0.5618181818181818,
                    relheight=0.1532367149758454)
        return entry

    @staticmethod
    def commit(parent):
        btn = Button(parent, text="确认", takefocus=False, )
        btn.place(relx=0.7090909090909091, rely=0.5797101449275363, relwidth=0.16, relheight=0.18840579710144928)
        return btn

    @staticmethod
    def cancel(parent):
        btn = Button(parent, text="清空", takefocus=False, )
        btn.place(relx=0.4727272727272727, rely=0.5797101449275363, relwidth=0.17636363636363636,
                  relheight=0.18357487922705315)
        return btn


class Win(WinGUI):
    def __init__(self, title, flag):
        """
       :param title: 窗口标题
       """
        super().__init__(flag)
        self.title(title)
        self.__result = None
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.__event_bind()

    def on_closing(self):
        self.withdraw()
        self.quit()

    def commit_click(self):
        entry = getattr(self, "password")
        val = entry.get()
        self.__result = val
        self.withdraw()
        self.quit()

    def cancel_click(self):
        self.password.delete(0, END)

    def getResult(self):
        return self.__result

    def __event_bind(self):
        self.commit.config(command=self.commit_click)
        self.cancel.config(command=self.cancel_click)


if __name__ == "__main__":
    win = Win('模拟密码键盘', 1)
    win.mainloop()
    print(win.getResult())
