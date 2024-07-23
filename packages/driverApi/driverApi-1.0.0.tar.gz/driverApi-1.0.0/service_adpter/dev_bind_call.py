from abc import ABCMeta, abstractmethod
from typing import Dict, List


class DevBindCall(metaclass=ABCMeta):
    """ 设备绑定信息基类 """

    @abstractmethod
    def getBindDev(self, termId, pageIndex=1, pageSize=10) -> Dict | None:
        """
        获取本终端绑定的设备,页面显示数据调用
        @param termId: 本终端Id
        @param pageIndex: 当前页
        @param pageSize: 页大小
        @return: retData
        """

    @abstractmethod
    def getBindDevAsOtherInfo(self, termId) -> Dict | None:
        """
        获取本终端绑定的设备以及其他信息，系统启动组装配置信息调用
        @param termId: 本终端Id
        @return: retData
        """

    @abstractmethod
    def getBindDetailByBindId(self, bindId) -> Dict:
        """
        获取绑定详情
        @param bindId:
        @return:
        """

    @abstractmethod
    def addBindDev(self, data):
        """
        新增绑定信息
        @param parent: 窗口对象
        @param data: 绑定数据
        @return:
        """

    @abstractmethod
    def deleteBindDev(self, bindId):
        """
        根据bindId删除数据
        @param parent: 父窗口对象
        @param bindId: id
        @return:
        """

    @abstractmethod
    def updateBindDev(self, data) -> bool:
        """
        根据bindId更新数据
        @param data: 要更新的数据
        @return:
        """

    @abstractmethod
    def batchUpdateBindDev(self, dataList: List) -> bool:
        """
        根据bindId更新数据
        @param dataList: 要更新的数据列表
        @return:
        """

    @abstractmethod
    def getStatus(self) -> List:
        """
        获取绑定状态
        @return:
        """
