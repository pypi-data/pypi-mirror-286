from abc import ABCMeta, abstractmethod
from typing import Dict


class DevModelCall(metaclass=ABCMeta):

    @abstractmethod
    def getDevModelByDevClass(self, devClassIds: list) -> Dict | None:
        """
        根据设备类型列表获取每个设备类型的可选设备型号
        @param devClassIds: 设备类型列表
        @return: key:设备类型，val:设备型号列表|None
        """
