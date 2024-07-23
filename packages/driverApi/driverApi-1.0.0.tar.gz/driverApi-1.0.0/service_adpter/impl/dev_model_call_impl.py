import json
from typing import Dict

from common import Singleton, common_utils, global_constants
from model import init_config
from service_adpter.api.device_api import APIEndpoint
from service_adpter.dev_model_call import DevModelCall
from service_adpter.send_request import send


@Singleton
class DevModelCallImpl(DevModelCall):

    def getDevModelByDevClass(self, devClassIds: list) -> Dict | None:
        retData = {}
        if init_config.is_local_run():
            path = common_utils.get_absolute_path('config/device_config.json')
            file_data = common_utils.read_file(path)
            dev_cfg: Dict = json.loads(file_data)
            dev_model_cfg = dev_cfg['device_models']
            compDev: list = []
            for devClassId in devClassIds:
                devModels: list = []
                for model in dev_model_cfg:
                    if devClassId == global_constants.COMP_DEVICE and "|" in model.get('dev_class'):
                        compDev.append((model["dev_id"] + "-" + model["dev_desc"], model["dev_id"],))
                    if devClassId in model.get('dev_class'):
                        devModels.append((model["dev_id"] + "-" + model["dev_desc"], model["dev_id"],))
                retData[devClassId] = devModels
            retData[global_constants.COMP_DEVICE] = compDev
            return retData
        else:
            for devClassId in devClassIds:
                params = {
                    "devClassId": devClassId
                }
                respBody = send(APIEndpoint.get_dev_model_by_dev_class, params=params)
                if respBody and respBody.get(global_constants.SUCCESS, None):
                    data: list = respBody["data"]
                    devModels: list = []
                    for item in data:
                        devModels.append((item["devModelId"] + "-" + item["devModelDesc"], item["devModelId"],))
                    retData[devClassId] = devModels

        return retData
