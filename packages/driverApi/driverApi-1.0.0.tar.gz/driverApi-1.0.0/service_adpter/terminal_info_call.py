from abc import abstractmethod, ABCMeta
from typing import Dict, List


class TerminalInfoCall(metaclass=ABCMeta):
    @abstractmethod
    def addTerminalInfo(self, data):
        """
        添加终端信息
        @param parent:
        @param data:
        @return:
        """

    def updateTerminalInfo(self, data):
        """
        更新终端信息
        @param data:
        @param parent:
        @return:
        """

    @abstractmethod
    def getTerminalInfoByMac(self, macAddr) -> Dict:
        """
        查询终端信息
        @param macAddr: mac终端地址
        @return:
        """

    @abstractmethod
    def getMacAddr(self) -> str | None:
        """
        获取mac地址
        @return:
        """

    @abstractmethod
    def getCommType(self, termModelId) -> List | None:
        """
        根据终端型号Id获取该类型终端有哪些通讯端口
        @return: retData
        """
