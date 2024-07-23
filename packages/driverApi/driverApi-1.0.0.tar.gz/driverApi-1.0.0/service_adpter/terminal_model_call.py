from abc import abstractmethod, ABCMeta
from typing import Dict


class TerminalModelCall(metaclass=ABCMeta):
    @abstractmethod
    def getTerminalModels(self) -> Dict:
        """
        获取所有终端型号
        @return:
        """
