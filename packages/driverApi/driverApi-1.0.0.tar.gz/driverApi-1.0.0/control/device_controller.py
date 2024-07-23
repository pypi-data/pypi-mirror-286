# author: haoliqing
# date: 2023/8/21 16:52
# desc: 设备访问控制器
import json
import traceback

from common.singleton import Singleton
from model.task_model.context.device_request_context import DeviceRequestContext
from model.task_model.context.system_request_context import SystemRequestContext
from model.task_model.context.request_context_factory import RequestContextFactory
from service_adpter import TerminalInfoCallImpl
from task.container import TaskRegister
from task.manager import DeviceTaskManager, SystemTaskManager
from control.sparepart.sparepart_factory import SparePartFactory
from common import global_constants, common_utils, send_socket_msg
import time
from logger.device_logger import logger
from exception.device_exception import DeviceException


@Singleton
class DeviceController(object):

    def __init__(self):
        """初始化"""
        self.__device_task_manager = DeviceTaskManager()
        self.__system_task_manager = SystemTaskManager()
        self.task_register: TaskRegister = TaskRegister()

    def execute(self, req_data: str, socket):
        """执行请求"""
        try:
            request_data = json.loads(req_data)
            if global_constants.OPTION == request_data[global_constants.REQ_TYPE].lower():
                self.__handle_option(request_data)
            elif global_constants.REQUEST == request_data[global_constants.REQ_TYPE].lower():
                self.__handle_request(request_data, socket)
            else:
                # self.__handle_getstatus(request_data, socket)
                pass  # 改变查询状态为主动推送
        except Exception as e:
            logger.error("执行设备调用请求{0}时发生异常: {1}, 异常信息：{2}"
                         .format(request_data[global_constants.FUNCTION_NAME], str(e), traceback.format_exc()))

    def __handle_option(self, request_data):
        flag = request_data['data']
        task = self.task_register.get_task(request_data[global_constants.REQUEST_ID])
        if task:
            if flag == 'yes':
                task.restart_task()
            else:
                task.finish_task()

    def __handle_request(self, request_data, socket):
        try:
            request_id = str(int(time.time() * 1000))  # 毫秒时间戳
            logger.info("DeviceController接收到请求数据：{0}，请求ID：{1}".format(request_data, request_id))
            msg = json.dumps({"state": "RECEIVE", "function": request_data[global_constants.FUNCTION_NAME],
                              "request_id": request_id})
            common_utils.send_socket_msg(socket, msg)

            start = time.time()
            if request_data[global_constants.FUNCTION_NAME] == "GetMac":
                mac_value = TerminalInfoCallImpl().getMacAddr()
                macField = request_data[global_constants.REQ_PARAM]["MacId"]
                msg = json.dumps(
                    {"state": "SUCCESS", "function": request_data[global_constants.FUNCTION_NAME],
                     "data": {macField: mac_value}, "code": 0, "msg": "执行成功", "request_id": request_id},
                    ensure_ascii=False)
                send_socket_msg(socket, msg)
                return
            spare_part = SparePartFactory().get_spare_part(request_data[global_constants.FUNCTION_NAME])
            if spare_part:
                spare_part.update(request_data)  # 更新请求数据，填充内容
            request_context = RequestContextFactory().get_request_context(request_id, request_data, socket)
            end = time.time()
            logger.info("构建请求上下文耗时" + str(end - start) + "秒")
            if isinstance(request_context, DeviceRequestContext):
                self.__device_task_manager.execute(request_context)
            elif isinstance(request_context, SystemRequestContext):
                self.__system_task_manager.execute(request_context)
            else:
                device_exception = DeviceException('E01001', request_context)
                logger.error(str(device_exception))
                raise device_exception

        except Exception as e:
            msg = json.dumps({"state": "FAIL", "function": request_data[global_constants.FUNCTION_NAME], "msg": str(e),
                              "request_id": request_id}, ensure_ascii=False)
            logger.error("执行设备调用请求{0}时发生异常: {1}, 异常信息：{2}"
                         .format(request_data["function"], str(e), traceback.format_exc()))
            common_utils.send_socket_msg(socket, msg)


if __name__ == '__main__':
    start_req_data = '{"function":"SystemStart","param":{}}'
    control: DeviceController = DeviceController()
    control.execute(json.loads(start_req_data))

    kpd_req_data = '{"function" : "ReadKpdPwd",type: "request", "param" :{"pwdID":"PASSWORD"}}'
    control.execute(json.loads(kpd_req_data))
