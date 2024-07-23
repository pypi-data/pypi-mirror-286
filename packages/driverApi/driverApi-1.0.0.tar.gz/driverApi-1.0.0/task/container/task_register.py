# author: haoliqing
# date: 2023/8/30 17:38
# desc: 任务登记类,该对象可能会被多个线程操作，故对数据的修改需要加锁
import threading

from PySide2.QtCore import QObject, Signal

from common.singleton import Singleton

from model.task_model.base_task import Task


@Singleton
class TaskRegister(QObject):
    """任务登记类"""

    task_cache = {}
    lock = threading.RLock()
    send_task_signal = Signal(str, object)
    finished = Signal()  # 表示任务结束信号

    def __init__(self):
        super().__init__()

    def add_task(self, task: Task):
        """登记任务"""
        # 加锁
        self.lock.acquire()
        try:
            self.task_cache[task.id] = task
            self.send_task_signal.emit("A", task)
        finally:
            # 修改完成，释放锁
            self.lock.release()

    def get_task(self, task_id):
        """根据任务id获取任务"""
        return self.task_cache.get(task_id, None)

    def remove_task(self, task_id):
        """删除登记的任务"""
        # 加锁
        self.lock.acquire()
        try:
            if task_id in self.task_cache:
                self.send_task_signal.emit("D", self.task_cache[task_id])
                self.finished.emit()
                del self.task_cache[task_id]
        finally:
            # 修改完成，释放锁
            self.lock.release()

    def bind_signal(self, view):
        self.send_task_signal.connect(view.receive_add_data)

    def get_task_num(self):
        """获取任务个数"""
        return len(self.task_cache)
