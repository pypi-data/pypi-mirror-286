# author: haoliqing
# date: 2023/8/31 10:14
# desc:
from queue import Queue
from threading import Thread, Event

from exception.device_exception import DeviceException
from logger.device_logger import logger
from model.task_model.base_task import Task, TaskStatus, TaskStatusListener
from task.container.task_register import TaskRegister
from task.handler import TaskHandler


class TaskContainer(object):
    """任务容器基类"""
    task_register: TaskRegister = TaskRegister()

    def __init__(self, container_id: str, task_handler: TaskHandler):
        self.__task_queue = Queue(maxsize=10)  # 先进先出队列
        self.__status_task_queue = Queue(maxsize=10)  # 先进先出队列
        self.__container_id = container_id
        self.__task_handler = task_handler
        self.__monitor = TaskContainerMonitor(container_id + "_monitor", task_handler, self)

    def add_task(self, task: Task):
        self.__monitor.pause()  # 添加任务时暂停任务监听线程，避免添加逻辑未执行完，任务已被get
        if self.__task_queue.full():
            device_exception = DeviceException('E01004', self.__container_id)
            logger.error(str(device_exception))
            raise device_exception
        else:
            # common_utils.send_socket_msg(task.request_context.socket, "接收消息")
            self.__task_queue.put(task)
            self.task_register.add_task(task)
            self.__monitor.resume()  # 执行完添加逻辑运行监听线程

    def add_status_task(self, task: Task):
        self.__monitor.resume()  # 先让线程运行起来
        if not self.__status_task_queue.full():
            """对于状态查询任务，放不下就忽略"""
            self.__status_task_queue.put(task)

    def remove_task(self, task_id: str):
        self.task_register.remove_task(task_id)

    def start(self, ) -> bool:
        self.__monitor.start()
        return self.__monitor.is_alive()

    def cancel(self) -> bool:
        return self.__monitor.cancel()

    def clear_task(self):
        while not self.__task_queue.empty():
            task = self.__task_queue.get()
            self.remove_task(task.id)

    def get_task(self):
        """获取队列中的下一个任务"""
        task = None
        if not self.__task_queue.empty():
            task = self.__task_queue.get()  # 获取不到任务则等待一秒钟,获取任务的同时任务已经从队列移除
        return task

    def get_status_task(self):
        """获取状态查询任务"""
        task = None
        if not self.__status_task_queue.empty():
            task = self.__status_task_queue.get()  # 获取不到任务则等待一秒钟,获取任务的同时任务已经从队列移除
        return task


class DeviceTaskStatusListener(TaskStatusListener):

    def __init__(self, task_handler: TaskHandler, container: TaskContainer):
        self.__task_handler = task_handler
        self.__container = container

    def on_status_change(self, task_id: str, status: TaskStatus):
        if status == TaskStatus.SUCCESS or status == TaskStatus.FAIL or status == TaskStatus.TERMINATE:
            # 任务执行成功或失败的情况下移除任务
            self.__container.remove_task(task_id)
            self.__task_handler.clean_current_task()


class TaskContainerMonitor(Thread):
    """任务容器监听器，主要用于从任务容器中获取任务并扔给任务执行器执行"""

    def __init__(self, thread_name, task_handler: TaskHandler, container: TaskContainer):
        Thread.__init__(self)  # 调用父类初始化函数
        self.__thread_name = thread_name
        self.__task_handler = task_handler
        self.__run_flag = True
        self.__container = container
        self.__pause_flag = Event()  # 用于暂停线程的标识

    def cancel(self) -> bool:
        self.__run_flag = False
        self.join()
        return True

    def pause(self):
        self.__pause_flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__pause_flag.set()  # 设置为True, 让线程停止阻塞

    def run(self) -> None:
        while self.__run_flag:
            self.__pause_flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回, 以此来实现线程等待，释放CPU时间
            if not self.__task_handler.get_current_task():
                # 没有任务在执行，才获取新任务
                # 优先执行设备调用任务
                task = self.__container.get_task()
                if task:
                    if task.status == TaskStatus.CANCEL:  # 如果是已取消任务，从注册器中删除任务，结束
                        self.__container.remove_task(task.id)
                        continue
                    else:
                        task.status = TaskStatus.RUN
                        self.__container.task_register.send_task_signal.emit("U", task)
                else:
                    task = self.__container.get_status_task()

                if task:
                    task.add_status_listener(DeviceTaskStatusListener(self.__task_handler, self.__container))
                    self.__task_handler.execute(task)
                else:
                    self.pause()  # 暂停线程，直到有任务加入

            else:
                # 有任务则执行该任务
                self.__task_handler.execute(self.__task_handler.get_current_task())
