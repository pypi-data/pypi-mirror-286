from abc import ABCMeta, abstractmethod
from typing import Dict


class DevCommParamCall(metaclass=ABCMeta):
    @abstractmethod
    def addDevRunCommParam(self, data):
        """
        添加设备运行时通讯参数
        @param parent:
        @param data:
        @return:
        """

    @abstractmethod
    def deleteDevRunCommParam(self, bindId, commPort, devCommParamId):
        """
        精确删除设备运行时通讯参数
        @param parent: 弹窗的父窗口
        @param bindId: 绑定id
        @param commPort: 通讯端口
        @param devCommParamId: 设备通讯参数id
        @return:
        """

    @abstractmethod
    def updateDevRunCommParam(self, data) -> bool:
        """
        更新设备运行时通讯参数
        @param data:
        @return:
        """

    @abstractmethod
    def getCommParamByCommTypeId(self, commTypeId: str) -> list:
        """
        根据端口类型查询该端口的可选参数，用于详情表格中显示下拉框数据
        @param commTypeId:
        @return:
        """

    @abstractmethod
    def getDevRunCommParamByBindId(self, bindId, commPort) -> list:
        """
        根据绑定id和端口号 查询运行时通讯端口参数，用于详情表格中显示已配置的运行时参数值
        @return:
        """

    def getCommPortParam(self, info) -> Dict:
        """
        根据绑定信息查询设备通讯参数默认参数以及运行时参数，用于程序启动时组装应用上下文
        @param info: 绑定信息
        @return:
        """
