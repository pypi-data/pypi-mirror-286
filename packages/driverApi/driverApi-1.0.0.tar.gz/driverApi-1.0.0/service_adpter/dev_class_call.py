from abc import ABCMeta, abstractmethod
from typing import List


class DevClassCall(metaclass=ABCMeta):

    @abstractmethod
    def getDevClass(self) -> List | None:
        """
        获取设备类型下拉框数据
        @return: 设备类型列表
        """
