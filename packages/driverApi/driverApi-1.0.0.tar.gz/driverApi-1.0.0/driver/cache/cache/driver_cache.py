# author: haoliqing
# date: 2023/9/5 16:32
# desc
from common import Singleton
from typing import Dict, TypeVar, Generic
from device.base_device import Device
import threading


@Singleton
class DriverCache(object):
    _driver_cache: Dict[str, Device] = {}
    lock = threading.RLock()

    def cache_driver(self, key: str, driver: Device):
        """缓存驱动实例"""
        # 加锁
        self.lock.acquire()
        try:
            self._driver_cache[key] = driver
        finally:
            # 修改完成，释放锁
            self.lock.release()

    def clean_driver(self, key: str):
        """删除缓存的驱动实例"""
        # 加锁
        self.lock.acquire()
        try:
            del self._driver_cache[key]
        finally:
            # 修改完成，释放锁
            self.lock.release()

    def clean_driver(self):
        """删除缓存的驱动实例"""
        # 加锁
        self.lock.acquire()
        try:
            self._driver_cache.clear()
        finally:
            # 修改完成，释放锁
            self.lock.release()

    def get_driver(self, key: str) -> Device:
        """获取缓存的驱动实例"""
        return self._driver_cache.get(key)
