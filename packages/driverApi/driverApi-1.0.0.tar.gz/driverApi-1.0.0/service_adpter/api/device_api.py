from enum import Enum


class APIMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class APIEndpoint(Enum):
    """ 设备绑定信息路径枚举 """
    get_bind_dev = ("/terminal-device-bind-v1/page", APIMethod.GET)
    get_bind_dev_as_other_info = ("/terminal-device-bind-v1/search", APIMethod.GET)
    get_bind_detail_by_bindId = ("/terminal-device-bind-v1/detail", APIMethod.GET)
    add_bind_dev = ("/terminal-device-bind-v1/add", APIMethod.POST)
    delete_bind_dev = ("/terminal-device-bind-v1/delete", APIMethod.DELETE)
    update_bind_dev = ("/terminal-device-bind-v1/update", APIMethod.PUT)
    batch_update_bind_dev = ("/terminal-device-bind-v1/updateBatch", APIMethod.PUT)
    get_dev_class = ("/device-class-v1/page", APIMethod.GET)

    add_dev_run_comm_param = ("/device-run-communication-param-v1/add", APIMethod.POST)
    delete_dev_run_comm_param = ("/device-run-communication-param-v1/delete/precise", APIMethod.DELETE)
    update_dev_run_comm_param = ("/device-run-communication-param-v1/update", APIMethod.PUT)
    get_comm_param_by_comm_type_id = ("/device-communication-param-v1/page", APIMethod.GET)
    get_dev_run_comm_param_by_bind_id = ("/device-run-communication-param-v1/page", APIMethod.GET)
    get_comm_port_param = ("/device-communication-param-v1/allParam", APIMethod.GET)

    get_dev_model_by_dev_class = ("/device-model-class-v1/page", APIMethod.GET)

    add_dev_run_param = ("/device-run-param-v1/add", APIMethod.POST)
    delete_dev_run_param = ("/device-run-param-v1/delete/precise", APIMethod.DELETE)
    update_run_dev_param = ("/device-run-param-v1/update", APIMethod.PUT)
    get_dev_param_by_dev_model_id = ("/device-model-param-v1/page", APIMethod.GET)
    get_dev_run_param_by_bind_id = ("/device-run-param-v1/page", APIMethod.GET)
    get_dev_param = ("/device-model-param-v1/allParams", APIMethod.GET)

    add_terminal_info = ("/terminal-info-v1/add", APIMethod.POST)
    update_terminal_info = ("/terminal-info-v1/update", APIMethod.PUT)
    get_terminal_info_by_mac = ("/terminal-info-v1/page", APIMethod.GET)
    get_comm_type = ("/terminal-communication-param-v1/page", APIMethod.GET)

    get_terminal_models = ("/terminal-model-v1/page", APIMethod.GET)
