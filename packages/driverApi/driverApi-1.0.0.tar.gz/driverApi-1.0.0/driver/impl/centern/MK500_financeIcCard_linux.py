import ctypes
from ctypes import *

from common import get_absolute_path
from device.device_config import DeviceConfig
from device.port import PortType
from driver.finance_ic_card_rwer import FinanceICCardRWer, FinanceICInfo, TranInfo, DetailInfo, WriteICResult, \
    CreditInfo
from logger.device_logger import logger


class MK500FinanceIcCardLinux(FinanceICCardRWer):
    def __init__(self):
        super().__init__()
        """ 公共参数 """
        self.szDevice = b"HID"
        self.nBaud = 9600
        self.szIcFlag = b"3"
        self.pszTxData = None
        self.outTime = 0
        self.dll_ICReader = ctypes.CDLL(get_absolute_path("dll/MK500/Linux/TY_ICC_Linux.so"))

    def init(self, device_cfg: DeviceConfig) -> int:
        super().init(device_cfg)
        try:
            port_type = device_cfg.port.get_port_type()
            if port_type == PortType.USB:
                self.szDevice = b"HID"
            elif port_type == PortType.COM:
                self.szDevice = bytes(device_cfg.port.port_id, "gbk")
            if self.szIcFlag != b"3":
                self.outTime = 30
        except Exception as e:
            logger.error(e)
            return -1
        return 0

    def power_on(self) -> int:
        pATRLen = c_int(1024)
        szATR = create_string_buffer(1024)
        on_status = self.dll_ICReader.Linux_CT_IC_PowerOn(self.szDevice, self.nBaud, self.szIcFlag, self.outTime,
                                                          pATRLen,
                                                          szATR)
        #  这里返回的on_status就是szATR的实际有效长度（API未作说明）
        atrData = szATR[:on_status]  # 返回的 ATR 数据
        atrData16 = ''.join([hex(num)[2:].zfill(2).upper() for num in atrData])  # 返回的 ATR 数据转化为16进制
        logger.info(f"上电成功,状态：{on_status}")
        logger.info(f"上电返回数据：{atrData16}")
        return on_status

    def power_off(self) -> int:
        status = self.dll_ICReader.Linux_CT_IC_PowerOff(self.szDevice, self.nBaud, self.szIcFlag)
        return status

    def read_finance_ic_info(self, tran_info: TranInfo) -> FinanceICInfo:
        """
        读IC卡
        @param tran_info:
        @return:
        """
        financeICInfo = FinanceICInfo()
        if tran_info is None:
            financeICInfo.err_code = -1
            return financeICInfo
        authAmount = self.getattr(tran_info, "tran_amt", "000000000000")  # 授权金额 （不带小数点，单位为分）
        tranCcy = self.getattr(tran_info, "tran_ccy", "0516")  # 交易货币代码 （常量0x01 0x56，表示人民币）
        tranType = self.getattr(tran_info, "tran_type", "96")  # 交易类型
        orgName = self.getattr(tran_info, "org_name", "柜面")  # 商户名称
        inputAid = self.getattr(tran_info, "inputAid", "A000000333010101")  # 交易使用的Aid
        tranDate = tran_info.tran_date  # 交易日期
        tranTime = tran_info.tran_time  # 交易时间
        self.pszTxData = (
            f"P{self.fbz(authAmount)}{authAmount}R{self.fbz(tranCcy)}{tranCcy}S{self.fbz(tranDate)}{tranDate}"
            f"T{self.fbz(tranType)}{tranType}U{self.fbz(tranTime)}{tranTime}W{self.fbz(orgName)}{orgName}")
        pszAidList: bytes = bytes(inputAid, "gbk")
        flag = self.getICInfo(financeICInfo, pszAidList)
        if flag < 0:
            financeICInfo.err_code = flag
            return financeICInfo
        flag = self.getARQC(financeICInfo, tranDate, authAmount)
        if flag < 0:
            financeICInfo.err_code = flag
            return financeICInfo
        self.getTranDetail(financeICInfo, pszAidList)
        self.getCreditLoadLog(financeICInfo, pszAidList)
        return financeICInfo

    def getICInfo(self, financeICInfo: FinanceICInfo) -> int:
        """
        读取基本卡信息
        @param financeICInfo: 结果存储对象
        @return:
        """
        pszTaglist = b"ABCDEFGHIJKMNOPQST"
        pszUserInfo = create_string_buffer(1024)
        """ 参数说明  连接端口，串口波特率，接触方式"""
        # 设置函数参数类型
        self.dll_ICReader.Linux_CT_IC_GetIccInfo.argtypes = [c_char_p, c_long, c_char_p, c_long, c_char_p, c_char_p,
                                                             c_char_p, c_long, c_char_p]
        # 设置函数返回类型
        self.dll_ICReader.Linux_CT_IC_GetIccInfo.restype = c_long
        read_card_status = self.dll_ICReader.Linux_CT_IC_GetIccInfo(self.szDevice, self.nBaud, self.szIcFlag,
                                                                    self.outTime,
                                                                    None,  # 应用AID,传Null自动选择
                                                                    pszTaglist,  # 应用标签列表
                                                                    None,  # 交易信息，读卡时传Null
                                                                    1024,  # 缓冲区
                                                                    pszUserInfo)  # 输出信息
        logger.info(f"读取IC卡结果：{read_card_status}")
        if read_card_status < 0:
            return read_card_status
        try:
            result = pszUserInfo.value.decode("gbk")[:read_card_status]
            logger.info(f"读取IC卡返回数据：{result}")
            self.analysisUerInfo(financeICInfo, result)
        except Exception as e:
            logger.error(e)
        return read_card_status

    def getARQC(self, financeICInfo: FinanceICInfo, tranDate: str, authAmount: str) -> int:
        """
        获取ARQC
        @param authAmount:
        @param tranDate:
        @param financeICInfo: 结果存储对象
        @return:
        """
        pszARQC = create_string_buffer(1024)
        logger.info(f"读取ARQC输入交易数据是: {self.pszTxData}")
        read_arqc_status = self.dll_ICReader.Linux_CT_IC_GenerateARQC(self.szDevice, self.nBaud, self.szIcFlag,
                                                                      bytes(self.pszTxData, "gbk"),
                                                                      1024,
                                                                      pszARQC)
        logger.info(f"读取ARQC结果：{read_arqc_status}")
        if read_arqc_status < 0:
            return read_arqc_status
        try:
            result = pszARQC.value.decode("gbk")[0:read_arqc_status]
            logger.info(f"读取ARQC返回数据：{result}")
            financeICInfo.arqc = str(read_arqc_status).zfill(3) + result
            self.getArqcSource(financeICInfo, result, tranDate, authAmount)
        except Exception as e:
            logger.error(e)
        return read_arqc_status

    @staticmethod
    def getArqcSource(financeICInfo: FinanceICInfo, arqc: str, tranAmt: str, tranDate: str):
        """
        解析Arqc数据，获取ArqcSource，为financeICInfo设置值
        @param financeICInfo:
        @param arqc:
        @param tranAmt:
        @param tranDate:
        @return:
        """
        appEncodeText = arqc[arqc.index("9F26") + 6:arqc.index("9F26") + 22]  # 9F26: 应用密文 （8 字节）
        financeICInfo.arqc_only = appEncodeText
        encodeTextData = arqc[arqc.index("9F27") + 6:arqc.index("9F27") + 8]  # 9F27: 密文信息数据 （1 字节）
        issueBranchDataStr = arqc[arqc.index("9F10") + 6:arqc.index("9F10") + 44]  # 9F10: 发卡行应用数据 （38位）
        financeICInfo.issue_branch_data = issueBranchDataStr
        CVRStr = issueBranchDataStr[6:14]  # 卡片验证结果（CVR）（4 字节）
        otherData = arqc[arqc.index("9F37") + 6:arqc.index("9F37") + 14]  # 9F37: 随机数(4 字节)
        ATC = arqc[arqc.index("9F37") + 6:arqc.index("9F37") + 10]  # 9F36: ATC （2 字节）
        terminalCheckResult = arqc[arqc.index("95") + 4:arqc.index("95") + 14]  # 95: 终端验证结果 （5 字节）
        financeICInfo.verify_result = terminalCheckResult
        tranDateTemp = tranDate[2]
        tranType = arqc[arqc.index("9C") + 4:arqc.index("9C") + 6]  # 9C: 交易类型 （1 字节）
        tranAmtTemp = arqc[arqc.index("9F02") + 6:arqc.index("9F02") + 18]  # 9F02: 授权金额 （6 字节）
        tranCcyCode = arqc[arqc.index("5F2A") + 6:arqc.index("5F2A") + 10]  # 5F2A: 交易货币代码 （2 字节）
        aipStr = arqc[arqc.index("82") + 4:arqc.index("82") + 8]  # 82: 应用交互特征 （2 字节）
        countryCode = arqc[arqc.index("9F1A") + 6:arqc.index("9F1A") + 10]  # 9F1A: 终端国家代码 （2 字节）
        otherAmt = arqc[arqc.index("9F03") + 6:arqc.index("9F03") + 18]  # 9F03: 其它金额 （6 字节）
        termPorperty = arqc[arqc.index("9F33") + 6:arqc.index("9F33") + 12]  # 9F33: 终端性能 （3 字节）

        # ARQC源数据  授权金额（12位）+其它金额（12位）+终端国家代码（4位）+终端验证结果（10位）+交易货币代码（4位）+交易日期（6位）+交易类型（2位）+不可预知数（8位）+应用交互特征（AIP）（4
        # 位）+应用交易计数器（ATC）（4位）+卡片验证结果（CVR）（8位）
        arqcSourceTemp = tranAmt + "000000000000" + countryCode + terminalCheckResult + "0156" + tranDateTemp + tranType + otherData + aipStr + financeICInfo.tran_counter + CVRStr
        financeICInfo.arqc_source = arqcSourceTemp

    def getTranDetail(self, financeICInfo: FinanceICInfo, pszAidList: bytes) -> int:
        """
        获取交易明细信息
        @param pszAidList:
        @param financeICInfo:
        @return:
        """
        pnTxDetailLen = c_int(1024)
        detail = create_string_buffer(2048)
        read_detail_status = self.dll_ICReader.Linux_CT_IC_GetTransActionLog(self.szDevice, self.nBaud, self.szIcFlag,
                                                                             pszAidList,
                                                                             byref(pnTxDetailLen),
                                                                             detail)
        logger.info(f"读取交易明细结果：{read_detail_status}")
        if read_detail_status < 0:
            return read_detail_status
        try:
            result = detail.value.decode("gbk")
            logger.info(f"读取交易明细返回数据：{result}")
            financeICInfo.tran_detail = self.analysisDetailInfo(result)
        except Exception as e:
            logger.error(e)
        return read_detail_status

    def getCreditLoadLog(self, financeICInfo: FinanceICInfo, pszAidList: bytes) -> int:
        """
        获取圈存明细信息
        @param pszAidList:
        @param financeICInfo:
        @return:
        """
        pnTxDetailLen = c_int(1024)
        txDetail = create_string_buffer(1024)
        read_credit_result = self.dll_ICReader.Linux_CT_IC_GetCreditLoadLog(self.szDevice, self.nBaud, self.szIcFlag,
                                                                            pszAidList,
                                                                            byref(pnTxDetailLen),
                                                                            txDetail)
        logger.info(f"读取圈存明细结果：{read_credit_result}")
        if read_credit_result < 0:
            return read_credit_result
        try:
            result = txDetail.value.decode("gbk")
            logger.info(f"读取圈存明细返回数据：{result}")
            financeICInfo.credit_detail = self.analysisCreditLoadLog(result)
        except Exception as e:
            logger.error(e)
        return read_credit_result

    @staticmethod
    def analysisDetailInfo(transDetail: str) -> list[DetailInfo] | None:
        """ 将读取到的数据解析为列表"""
        if len(transDetail) <= 0 or transDetail is None:
            return None
        dataNum = transDetail[0:2]  # 返回交易明细总条数
        if int(dataNum) == 0:
            return None
        everyDataLen: int = int(transDetail[2:5])  # 每条数据的总长度
        data: str = transDetail[5:]  # 去掉前五位数字
        dataList: [] = [data[i:i + everyDataLen] for i in range(0, len(data), everyDataLen)]  # 将数据截取为列表
        resultList: [DetailInfo] = []
        for item in dataList:
            detailInfo = DetailInfo()
            authAmt = item[item.index("P012") + 4:item.index("P012") + 16]
            detailInfo.auth_amt = f"{int(authAmt) / 100:.2f}"
            otherAmt = item[item.index("Q012") + 4:item.index("Q012") + 16]
            detailInfo.other_amt = f"{int(otherAmt) / 100:.2f}"
            detailInfo.ccy = item[item.index("R004") + 4:item.index("R004") + 8]
            detailInfo.tran_date = item[item.index("S006") + 4:item.index("S006") + 10]
            detailInfo.tran_type = item[item.index("T002") + 4:item.index("T002") + 6]
            detailInfo.tran_time = item[item.index("U006") + 4:item.index("U006") + 10]
            detailInfo.country = item[item.index("V004") + 4:item.index("V004") + 8]
            ACT = item[item.index("X004") + 4:item.index("X004") + 8]
            detailInfo.counter_app = ACT
            item = item.replace(f"X004{ACT}", "")
            detailInfo.org_name = item[item.index("W020") + 4:].strip()
            resultList.append(detailInfo)
        return resultList

    @staticmethod
    def analysisUerInfo(financeICInfo: FinanceICInfo, baseCardInfo: dict) -> FinanceICInfo:
        resultDict = {}  # 存储解析后的卡信息数据
        i = 0
        while i < len(baseCardInfo):
            if baseCardInfo[i].isupper():
                current_key = baseCardInfo[i]
                i += 1
                data_len = int(baseCardInfo[i:i + 3])
                i += 3
                resultDict[current_key] = baseCardInfo[i:i + data_len]
                i += data_len
            else:
                i += 1
        financeICInfo.card_no = resultDict.get("A")
        financeICInfo.track2Data = resultDict.get("B")
        financeICInfo.balance = resultDict.get("C")
        financeICInfo.balance_limit = resultDict.get("D")
        financeICInfo.overdue_date = resultDict.get("E")
        financeICInfo.single_limit = resultDict.get("F")
        financeICInfo.card_serial_no = resultDict.get("G")
        financeICInfo.tran_counter = resultDict.get("H")
        financeICInfo.cert_no = resultDict.get("I")
        financeICInfo.cert_type = resultDict.get("J")
        financeICInfo.owner_name = resultDict.get("K")
        financeICInfo.effective_date = resultDict.get("M")
        financeICInfo.ccy = resultDict.get("S")
        return financeICInfo

    @staticmethod
    def analysisCreditLoadLog(creditLoadLog: str) -> list[CreditInfo] | None:
        if len(creditLoadLog) <= 0 or creditLoadLog is None:
            return None
        dataNum = creditLoadLog[0:2]  # 返回圈存明细总条数
        if int(dataNum) == 0:
            return None
        everyDataLen: int = int(creditLoadLog[2:5])  # 每条数据的总长度
        data: str = creditLoadLog[5:]  # 去掉前五位数字
        dataList: [] = [data[i:i + everyDataLen] for i in range(0, len(data), everyDataLen)]  # 将数据截取为列表
        resultList: [CreditInfo] = []
        for item in dataList:
            creditInfo = CreditInfo()
            beforeAmt = item[item.index("P012") + 4:item.index("P012") + 16]
            creditInfo.before_amt = f"{int(beforeAmt) / 100:.2f}"
            afterAmt = item[item.index("Q012") + 4:item.index("Q012") + 16]
            creditInfo.after_amt = f"{int(afterAmt) / 100:.2f}"
            creditInfo.tran_date = item[item.index("S006") + 4:item.index("S006") + 10]
            creditInfo.tran_time = item[item.index("U006") + 4:item.index("U006") + 10]
            creditInfo.country = item[item.index("V004") + 4:item.index("V004") + 8]
            ACT = item[item.index("X004") + 4:item.index("X004") + 8]
            creditInfo.counter_app = ACT
            item = item.replace(f"X004{ACT}", "")
            creditInfo.org_name = item[item.index("W020") + 4:].strip()
            resultList.append(creditInfo)
        return resultList

    @staticmethod
    def fbz(param) -> str:
        """
        获取输入参数的长度转化为3位长度的字符串，示例：in:"1056" -> out:"004"
        """
        if param is not None:
            paramBytesLen: int = 0
            try:
                paramBytesLen = len(bytes(param, "gbk"))
            except UnicodeEncodeError as e:
                logger.error(e)
            return str(paramBytesLen).zfill(3)
        else:
            return "000"

    @staticmethod
    def getattr(obj: object, name: str, default=None):
        """
        根据传入的对象和属性名，判断是否有该属性，如果有该属性且不为None，则返回已有的值，
        如果是None或者没有这个属性，则返回接收到的默认值。
        """
        if hasattr(obj, name):
            attr_value = getattr(obj, name)
            if attr_value is not None:
                return attr_value
        return default

    def write_finance_ic_info(self, data: str) -> WriteICResult:
        """
        写IC卡
        @param data:
        @return:
        """
        writeRet = WriteICResult()
        pszTC = create_string_buffer(512)
        pszScriptResult = create_string_buffer(1024)
        write_status = self.dll_ICReader.Linux_CT_IC_CloseTransAction(self.szDevice,
                                                                      self.nBaud,
                                                                      self.szIcFlag,
                                                                      bytes(self.pszTxData, "gbk"),
                                                                      bytes(data, "gbk"),
                                                                      byref(c_int(1024)),
                                                                      pszTC,
                                                                      pszScriptResult)
        logger.info(f"写卡，结果是{write_status}")
        logger.info(f"写卡，输入的交易数据是{self.pszTxData}")
        logger.info(f"写卡，输入的写卡脚本是{data}")
        if write_status < 0:
            writeRet.err_code = write_status
            return write_status
        try:
            TC = pszTC.value.decode("gbk")
            writeRet.tc = TC
            scriptResult = pszScriptResult.value.decode("gbk")
            writeRet.script_result = scriptResult
        except Exception as e:
            logger.error(e)
        return writeRet

    def open(self) -> int:
        super().open()
        return 0

    def close(self) -> int:
        super().close()
        return 0
    def is_cancel(self) -> bool:
        return False

if __name__ == '__main__':
    transInfo = TranInfo()
    transInfo.tran_amt = "18000000"
    transInfo.tran_ccy = "156"  # 交易货币代码 （常量0x01 0x56，表示人民币）
    transInfo.tran_type = "31"  # 交易类型
    transInfo.org_name = "china"  # 商户名称
    transInfo.inputAid = "A000000333010101"  # 交易使用的Aid
    transInfo.tran_date = "20231218"  # 交易日期
    transInfo.tran_time = "193421"  # 交易时间
    icCard = MK500FinanceIcCardLinux()
    info = icCard.read_finance_ic_info(transInfo)
    # data = idCard.power_off()
    print(info)
