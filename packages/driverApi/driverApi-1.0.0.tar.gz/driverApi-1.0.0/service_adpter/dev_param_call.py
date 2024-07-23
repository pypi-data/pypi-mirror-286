from abc import abstractmethod, ABCMeta
from typing import Dict, List


class DevParamCall(metaclass=ABCMeta):

    @abstractmethod
    def addDevRunParam(self, data):
        """
        添加设备运行时参数
        @param parent:
        @param data:
        @return:
        """

    @abstractmethod
    def deleteDevRunParam(self, bindId, devParamId):
        """
        根据绑定Id 和设备参数Id 精确删除设备运行时参数
        @param parent: 弹窗父窗口对象
        @param bindId:
        @param devParamId:
        @return:
        """

    @abstractmethod
    def updateRunDevParam(self, data) -> bool:
        """
        更新设备运行时参数
        @param data:
        @return:
        """

    @abstractmethod
    def getDevParamByDevModelId(self, devModelId) -> List:
        """
        根据设备型号查询该设备的可选参数,详情表格中显示列表下拉框
        @param devModelId:
        @return: options
        """

    @abstractmethod
    def getDevRunParamByBindId(self, bindId) -> List:
        """
        根据绑定Id获取设备运行时参数,用于详情表格中显示已配置的运行时参数
        @param bindId:
        @return:
        """
    @abstractmethod
    def getDevParam(self, devModelId, bindId) -> List:
        """
        根据绑定Id和设备id查询设备默认参数以及自定义参数,用于程序启动时组装应用上下文
        @param devModelId:
        @param bindId:
        @return:
        """

