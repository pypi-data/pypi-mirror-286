from typing import List, Dict

from common import Singleton, global_constants
from service_adpter.api.device_api import APIEndpoint
from service_adpter.dev_param_call import DevParamCall
from service_adpter.send_request import send


@Singleton
class DevParamCallImpl(DevParamCall):

    def addDevRunParam(self,  data):
        return send(APIEndpoint.add_dev_run_param, data=data)

    def deleteDevRunParam(self, bindId, devParamId):
        params = {
            "bindId": bindId,
            "devParamId": devParamId
        }
        respBody = send(APIEndpoint.delete_dev_run_param, params=params)
        return respBody and respBody.get(global_constants.SUCCESS, None)

    def updateRunDevParam(self, data) -> bool:
        respBody = send(APIEndpoint.update_run_dev_param, data=data)
        return respBody and respBody.get(global_constants.SUCCESS, None)

    def getDevParamByDevModelId(self, devModelId) -> List:
        params = {
            "devModelId": devModelId
        }
        respBody = send(APIEndpoint.get_dev_param_by_dev_model_id, params=params)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            return respBody['data']

    def getDevRunParamByBindId(self, bindId) -> List:
        params = {
            "bindId": {bindId}
        }
        retData: list = []
        respBody = send(APIEndpoint.get_dev_run_param_by_bind_id, params=params)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            retData = [[item['devParamId'], item['runValue'], item['devParamName']] for item in respBody['data']]
        return retData

    def getDevParam(self, devModelId, bindId) -> Dict:
        params = {
            "devModelId": devModelId,
            "bindId": bindId
        }
        respBody = send(APIEndpoint.get_dev_param, params=params)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            return {item['devParamName']: item['defaultValue'] for item in respBody['data']}


if __name__ == '__main__':
    call = DevParamCallImpl()
    # print(call.getDevDefaultParamByDevModelId("201"))
