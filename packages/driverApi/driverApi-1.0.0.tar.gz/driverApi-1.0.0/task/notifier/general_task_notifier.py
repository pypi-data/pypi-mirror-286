# author: haoliqing
# date: 2023/10/9 20:21
# desc:
import json
import tkinter as tk
from tkinter import messagebox

from common import common_utils, get_absolute_path
from logger.device_logger import logger
from model import init_config
from model.task_model.context.request_context import RequestContext
from model.task_model.response.task_notifier import TaskNotifier
from task.container.task_register import TaskRegister


class GeneralTaskNotifier(TaskNotifier):
    task_register: TaskRegister = TaskRegister()

    def on_start(self, ctx: RequestContext):
        pass

    def on_success(self, ctx: RequestContext):
        msg = json.dumps({"state": ctx.get_response().state.value, "function": ctx.function_name,
                          "data": ctx.get_response().response_values, "code": ctx.get_response().ret_code,
                          "msg": "执行成功", "request_id": ctx.request_id}, ensure_ascii=False)
        common_utils.send_socket_msg(ctx.socket, msg)

    def on_fail(self, ctx: RequestContext):
        msg = json.dumps({"state": ctx.get_response().state.value, "function": ctx.function_name,
                          "data": {}, "code": ctx.get_response().ret_code,
                          "msg": ctx.get_response().ret_msg, "request_id": ctx.request_id}, ensure_ascii=False)
        common_utils.send_socket_msg(ctx.socket, msg)

    def on_retry(self, ctx: RequestContext):
        pass

    def on_repeat(self, ctx: RequestContext):
        pass

    def on_halt(self, ctx: RequestContext):
        if init_config.show_message():
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            root.attributes('-topmost', True)  # 确保弹框会在顶层
            flag = messagebox.askokcancel("重试提示", "{}执行失败，是否重试？".format(ctx.function_name))
            task = self.task_register.get_task(ctx.request_id)
            if flag:
                task.restart_task()
            else:
                task.finish_task()
        else:
            msg = json.dumps({"state": "OPTION", "function": ctx.function_name,
                              "data": {"yes": "是", "no": "否"}, "code": ctx.get_response().ret_code,
                              "msg": "{}执行失败，是否重试？".format(ctx.function_name), "request_id": ctx.request_id},
                             ensure_ascii=False)
            common_utils.send_socket_msg(ctx.socket, msg)
