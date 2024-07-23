# author: haoliqing
# date: 2023/8/21 17:00
# desc: 系统功能请求上下文
from model.task_model.context.request_context import RequestContext
from model.task_model.response.system_response import SystemResponse


class SystemRequestContext(RequestContext):

    def __init__(self, request_id, request_data, function_cfg, socket):
        super().__init__(request_id, request_data, function_cfg, socket)

    def create_response(self):
        return SystemResponse()
