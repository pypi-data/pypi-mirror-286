import json
from typing import List

from common import common_utils, global_constants
from model import init_config
from service_adpter.api.device_api import APIEndpoint
from service_adpter.dev_class_call import DevClassCall
from service_adpter.send_request import send
from common.singleton import Singleton


@Singleton
class DevClassCallImpl(DevClassCall):

    def getDevClass(self) -> List | None:
        """
        获取设备类型下拉框数据
        @return: 设备类型列表
        """
        retData = []
        if init_config.is_local_run():
            path = common_utils.get_absolute_path('config/device_class_config.json')
            file_data = common_utils.read_file(path)
            dev_class = json.loads(file_data)
            for key in dev_class.keys():
                retData.append((dev_class.get(key), key,))
            return retData
        else:
            respBody = send(APIEndpoint.get_dev_class)
            if respBody and respBody.get(global_constants.SUCCESS, None):
                data: list = respBody["data"]
                for item in data:
                    retData.append((item["devClassId"] + "-" + item["devClassDesc"], item["devClassId"],))
                return retData
        return None


if __name__ == '__main__':
    call = DevClassCallImpl()
    print(call.getDevClass())
