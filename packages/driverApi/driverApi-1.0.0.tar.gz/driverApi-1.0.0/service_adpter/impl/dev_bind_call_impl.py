import json
from typing import Dict, List

from common import common_utils, global_constants
from common.singleton import Singleton
from model import init_config
from service_adpter.api.device_api import APIEndpoint
from service_adpter.dev_bind_call import DevBindCall
from service_adpter.send_request import send


@Singleton
class DevBindCallImpl(DevBindCall):

    def getBindDev(self, termId, pageIndex=1, pageSize=5, parent=None) -> Dict | None:
        retData: dict = {}
        if init_config.is_local_run():
            path = common_utils.get_absolute_path('config/device_config.json')
            file_data = common_utils.read_file(path)
            dev_cfg: Dict = json.loads(file_data)
            dev_models: List = dev_cfg['device_models']
            dev_model_class_dict = {}
            for dev_model in dev_models:
                dev_model_class_dict[dev_model["dev_id"]] = dev_model["dev_class"]
            term_dev_cfg: List = dev_cfg['term_dev_cfg']
            data: list = []
            for item in term_dev_cfg:
                devClassId = dev_model_class_dict.get(item["dev_id"])
                if "|" in devClassId:
                    devClassId = global_constants.COMP_DEVICE
                bindInfo = [0, devClassId, item["dev_id"], item["port"],
                            item["status"]]
                data.append(bindInfo)
            start_index = (pageIndex - 1) * pageSize
            end_index = start_index + pageSize
            retData["data"] = data[start_index:end_index]
            retData["total"] = len(term_dev_cfg)
            return retData
        else:
            params = {
                "termId": termId,
                "pageIndex": pageIndex,
                "pageSize": pageSize
            }
            respBody = send(APIEndpoint.get_bind_dev, params=params)
            if respBody and respBody.get(global_constants.SUCCESS, None):
                respData: list = respBody["data"]
                data: list = []
                for item in respData:
                    bindInfo = [item["bindId"], item["devClassId"], item["devModelId"], item["commPort"],
                                item["status"]]
                    data.append(bindInfo)
                retData["data"] = data
                retData["total"] = respBody["totalCount"]
                return retData
        return None

    def getBindDevAsOtherInfo(self, termId) -> List | None:
        params = {
            "termId": termId
        }
        respBody = send(APIEndpoint.get_bind_dev_as_other_info, params=params)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            respData: list = respBody["data"]
            return respData
        return None

    def getBindDetailByBindId(self, bindId) -> Dict:
        params = {
            "bindId": bindId
        }
        respBody = send(APIEndpoint.get_bind_detail_by_bindId, params=params)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            return respBody["data"]

    def addBindDev(self, data):
        return send(APIEndpoint.add_bind_dev, data=data)

    def deleteBindDev(self, bindId):
        params = {
            "bindId": bindId
        }
        return send(APIEndpoint.delete_bind_dev, params=params)

    def updateBindDev(self, data) -> bool:
        respBody = send(APIEndpoint.update_bind_dev, data=data)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            return True
        return False

    def batchUpdateBindDev(self, dataList: List) -> bool:
        respBody = send(APIEndpoint.batch_update_bind_dev, data=dataList)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            return True
        return False

    def getStatus(self) -> List:
        return [("1-启用", "1",), ("2-禁用", "2",), ("3-备选", "3")]


if __name__ == '__main__':
    call = DevBindCallImpl()
    # print(call.getBindDev("D4E98A9C81D1"))
    # print(call.getCommType(None, "TermA0001"))
    print(call.getBindDevAsOtherInfo("TermA0001"))
