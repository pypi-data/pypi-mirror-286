# author: haoliqing
# date: 2023/9/19 17:08
# desc:

from abc import ABCMeta, abstractmethod


class AbstractSparePart(object, metaclass=ABCMeta):
    """请求数据装配器接口"""

    @abstractmethod
    def update(self, request_data):
        pass
