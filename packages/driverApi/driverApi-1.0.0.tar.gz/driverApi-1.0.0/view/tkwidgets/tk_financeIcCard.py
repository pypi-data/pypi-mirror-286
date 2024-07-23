from tkinter import Tk, Label, INSERT
from tkinter.ttk import Entry, Button
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
        self.label6 = self.label6(self)
        self.label7 = self.label7(self)
        self.label8 = self.label8(self)
        self.label9 = self.label9(self)
        self.label10 = self.label10(self)
        self.label11 = self.label11(self)
        self.label12 = self.label12(self)
        self.label13 = self.label13(self)
        self.label14 = self.label14(self)
        self.label15 = self.label15(self)
        self.label16 = self.label16(self)
        self.label17 = self.label17(self)
        self.label18 = self.label18(self)
        self.label19 = self.label19(self)
        self.label20 = self.label20(self)
        self.label21 = self.label21(self)

        self.owner_name = self.owner_name(self)
        self.arqc = self.arqc(self)
        self.cert_type = self.cert_type(self)
        self.card_serial_no = self.card_serial_no(self)
        self.ccy = self.ccy(self)
        self.balance = self.balance(self)
        self.cert_no = self.cert_no(self)
        self.card_no = self.card_no(self)
        self.issue_branch_data = self.issue_branch_data(self)
        self.single_limit = self.single_limit(self)
        self.aid = self.aid(self)
        self.balance_limit = self.balance_limit(self)
        self.tran_counter = self.tran_counter(self)
        self.effective_date = self.effective_date(self)
        self.verify_result = self.verify_result(self)
        self.overdue_date = self.overdue_date(self)
        self.pboc_ver = self.pboc_ver(self)
        self.contact_mode = self.contact_mode(self)
        self.arqc_source = self.arqc_source(self)
        self.track2Data = self.track2Data(self)
        self.arqc_only = self.arqc_only(self)

        self.commit = self.commit(self)
        self.cancel = self.cancel(self)

    def __win(self):
        # 设置窗口大小、居中
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        width = int(screenwidth / 2)
        height = int(screenheight / 2)
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.minsize(width=width, height=height)

    @staticmethod
    def label1(parent):
        label = Label(parent, text="持卡人姓名", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.045351473922902494, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label2(parent):
        label = Label(parent, text="原始ARQ ", anchor="e", )
        label.place(relx=0.5285118219749653, rely=0.045351473922902494, relwidth=0.13630041724617525,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label3(parent):
        label = Label(parent, text="证件类型", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.11337868480725624, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label4(parent):
        label = Label(parent, text="证件号 ", anchor="e", )
        label.place(relx=0.5285118219749653, rely=0.11337868480725624, relwidth=0.13630041724617525,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label5(parent):
        label = Label(parent, text="卡序号", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.18140589569160998, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label6(parent):
        label = Label(parent, text="卡号", anchor="e", )
        label.place(relx=0.5285118219749653, rely=0.18140589569160998, relwidth=0.13630041724617525,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label7(parent):
        label = Label(parent, text="币种", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.2494331065759637, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label8(parent):
        label = Label(parent, text="电子现金余额", anchor="e", )
        label.place(relx=0.5285118219749653, rely=0.2494331065759637, relwidth=0.13630041724617525,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label9(parent):
        label = Label(parent, text="发卡行应用数据 ", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.31746031746031744, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label10(parent):
        label = Label(parent, text="应用标识", anchor="e", )
        label.place(relx=0.5285118219749653, rely=0.31746031746031744, relwidth=0.13630041724617525,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label11(parent):
        label = Label(parent, text="余额上限", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.3854875283446712, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label12(parent):
        label = Label(parent, text="单笔金额上限", anchor="e", )
        label.place(relx=0.5285118219749653, rely=0.3854875283446712, relwidth=0.13630041724617525,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label13(parent):
        label = Label(parent, text="应用交易计数器", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.45351473922902497, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label14(parent):
        label = Label(parent, text="终端验证结果", anchor="e", )
        label.place(relx=0.5285118219749653, rely=0.45351473922902497, relwidth=0.13630041724617525,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label15(parent):
        label = Label(parent, text="应用生效日期", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.5215419501133787, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label16(parent):
        label = Label(parent, text="应用失效日期", anchor="e", )
        label.place(relx=0.5285118219749653, rely=0.5215419501133787, relwidth=0.13630041724617525,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label17(parent):
        label = Label(parent, text="支持PBOC版本", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.5895691609977324, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label18(parent):
        label = Label(parent, text="IC卡接触方式", anchor="e", )
        label.place(relx=0.5285118219749653, rely=0.5895691609977324, relwidth=0.13630041724617525,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label19(parent):
        label = Label(parent, text="加密AROC", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.6575963718820862, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def label20(parent):
        entry = Label(parent, text="AROC源数据", anchor="e", )
        entry.place(relx=0.055632823365785816, rely=0.7256235827664399, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def label21(parent):
        label = Label(parent, text="二磁道等效数据", anchor="e", )
        label.place(relx=0.055632823365785816, rely=0.7936507936507936, relwidth=0.13908205841446453,
                    relheight=0.05668934240362812)
        return label

    @staticmethod
    def owner_name(parent):
        """持卡人姓名"""
        entry = Entry(parent)
        entry.insert(INSERT, "李小龙")
        entry.place(relx=0.19471488178025034, rely=0.045351473922902494, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def arqc(parent):
        """读取到的原始arqc，格式：3位arqc长度+arqc内容"""
        entry = Entry(parent)
        entry.insert(INSERT, "123918mx2309mx238r829r")
        entry.place(relx=0.6675938803894298, rely=0.045351473922902494, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def cert_type(parent):
        """证件类型"""
        entry = Entry(parent)
        entry.insert(INSERT, "居民身份证")
        entry.place(relx=0.19471488178025034, rely=0.11337868480725624, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def cert_no(parent):
        """证件号"""
        entry = Entry(parent)
        entry.insert(INSERT, "633276200128232826")
        entry.place(relx=0.6675938803894298, rely=0.11337868480725624, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def card_serial_no(parent):
        """卡序号"""

        entry = Entry(parent)
        entry.insert(INSERT, "01")

        entry.place(relx=0.19471488178025034, rely=0.18140589569160998, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def card_no(parent):
        """卡号"""
        entry = Entry(parent)
        entry.insert(INSERT, "92873912471938913")
        entry.place(relx=0.6675938803894298, rely=0.18140589569160998, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def ccy(parent):
        """币种"""
        entry = Entry(parent)
        entry.insert(INSERT, "人民币")
        entry.place(relx=0.19471488178025034, rely=0.2494331065759637, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def balance(parent):
        """电子现金余额"""
        entry = Entry(parent)
        entry.insert(INSERT, "10000.00")
        entry.place(relx=0.6675938803894298, rely=0.2494331065759637, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def issue_branch_data(parent):
        """发卡行应用数据"""

        entry = Entry(parent)
        entry.insert(INSERT, "1312")
        entry.place(relx=0.19471488178025034, rely=0.31746031746031744, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def aid(parent):
        """应用标识,有的驱动中获取不到，给定A000000333010101"""
        entry = Entry(parent)
        entry.insert(INSERT, "A000000333010101")
        entry.place(relx=0.6675938803894298, rely=0.31746031746031744, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def balance_limit(parent):
        """余额上限"""

        entry = Entry(parent)
        entry.insert(INSERT, "10000.00")
        entry.place(relx=0.19471488178025034, rely=0.3854875283446712, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def single_limit(parent):
        """单笔金额上限"""
        entry = Entry(parent)
        entry.insert(INSERT, "5000.00")
        entry.place(relx=0.6675938803894298, rely=0.3854875283446712, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def tran_counter(parent):
        """应用交易计数器"""
        entry = Entry(parent)
        entry.insert(INSERT, "1")
        entry.place(relx=0.19471488178025034, rely=0.45351473922902497, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def verify_result(parent):
        """终端验证结果"""
        entry = Entry(parent)
        entry.insert(INSERT, "1")
        entry.place(relx=0.6675938803894298, rely=0.45351473922902497, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def effective_date(parent):
        """应用生效日期"""
        entry = Entry(parent)
        entry.insert(INSERT, "2000/1/1")
        entry.place(relx=0.19471488178025034, rely=0.5215419501133787, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def overdue_date(parent):
        """应用失效日期"""
        entry = Entry(parent)
        entry.insert(INSERT, "2010/12/30")
        entry.place(relx=0.6675938803894298, rely=0.5215419501133787, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def pboc_ver(parent):
        """卡支持的PBOC版本 ： 2.0 或者 3.0"""
        entry = Entry(parent)
        entry.insert(INSERT, "0-2.0")
        entry.place(relx=0.19471488178025034, rely=0.5895691609977324, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def contact_mode(parent):
        """当前IC卡卡片操作使用的接触方式"""
        entry = Entry(parent)
        entry.insert(INSERT, "0-接触式")
        entry.place(relx=0.6675938803894298, rely=0.5895691609977324, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def arqc_only(parent):
        """6位arqc数据，arqc密文，16位，符合PBOC规范"""
        entry = Entry(parent)
        entry.insert(INSERT, "abcdefghijklmn12345")
        entry.place(relx=0.19471488178025034, rely=0.6575963718820862, relwidth=0.27816411682892905,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def arqc_source(parent):
        """ARQC源数据"""
        entry = Entry(parent)
        entry.insert(INSERT, "1234567890")
        entry.place(relx=0.19471488178025034, rely=0.7256235827664399, relwidth=0.7496522948539638,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def track2Data(parent):
        """二磁道等效数据"""
        entry = Entry(parent)
        entry.insert(INSERT, "jcioyfogrehdninc98392ryhnc9c78cx8xyn8m")
        entry.place(relx=0.19471488178025034, rely=0.7936507936507936, relwidth=0.7496522948539638,
                    relheight=0.05668934240362812)
        return entry

    @staticmethod
    def cancel(parent):
        btn = Button(parent, text="取消", takefocus=False, )
        btn.place(relx=0.3337969401947149, rely=0.8843537414965986, relwidth=0.13908205841446453,
                  relheight=0.07936507936507936)
        return btn

    @staticmethod
    def commit(parent):
        btn = Button(parent, text="确认", takefocus=False, )
        btn.place(relx=0.5285118219749653, rely=0.8843537414965986, relwidth=0.13908205841446453,
                  relheight=0.07936507936507936)
        return btn


class Win(WinGUI):
    def __init__(self, result, title, items: List[str]):
        super().__init__()
        self.title(title)
        self.__result = result
        self.__items = items
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.__event_bind()

    def on_closing(self):
        """ 阻止右上角关闭按钮，防止误杀线程 """
        pass

    def commit_click(self):
        for item in self.__items:
            entry = getattr(self, item)
            value_str = entry.get()
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


if __name__ == "__main__":
    win = Win(None, "测试窗口", [])
    win.mainloop()
