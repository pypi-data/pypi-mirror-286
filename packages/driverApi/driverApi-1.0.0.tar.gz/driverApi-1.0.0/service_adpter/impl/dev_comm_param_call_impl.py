from typing import Dict, List

from qfluentwidgets import InfoBar

from common import Singleton, global_constants
from service_adpter.api.device_api import APIEndpoint
from service_adpter.dev_comm_param_call import DevCommParamCall
from service_adpter.send_request import send


@Singleton
class DevCommParamCallImpl(DevCommParamCall):

    def addDevRunCommParam(self, data):
        return send(APIEndpoint.add_dev_run_comm_param, data=data)

    def deleteDevRunCommParam(self,  bindId, commPort, devCommParamId):
        params = {
            "bindId": bindId,
            "commPort": commPort,
            "devCommParamId": devCommParamId
        }
        return send(APIEndpoint.delete_dev_run_comm_param, params=params)

    def updateDevRunCommParam(self, data) -> bool:
        respBody = send(APIEndpoint.update_dev_run_comm_param, data=data)
        return respBody and respBody.get(global_constants.SUCCESS, None)

    def getCommParamByCommTypeId(self, commTypeId: str) -> List:
        options: List = []
        params = {
            "commTypeId": commTypeId
        }
        respBody = send(APIEndpoint.get_comm_param_by_comm_type_id, params=params)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            for index, item in enumerate(respBody['data']):
                option: tuple = (f"{index + 1}-{item['devCommParamDesc']}", item['devCommParamId'],)
                options.append(option)
        return options

    def getDevRunCommParamByBindId(self, bindId, commPort) -> List:
        param = {
            "bindId": bindId,
            "commPort": commPort
        }
        retData = []
        respBody = send(APIEndpoint.get_dev_run_comm_param_by_bind_id, params=param)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            for index, item in enumerate(respBody['data']):
                custParam = [item['devCommParamId'], item['runValue'], item["devCommParamName"]]
                retData.append(custParam)
            return retData
        return retData

    def getCommPortParam(self, info) -> Dict:
        params = {
            "commTypeId": info["commTypeId"],
            "bindId": info["bindId"],
            "commPort": info["commPort"]
        }
        respBody = send(APIEndpoint.get_comm_port_param, params=params)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            data = respBody["data"]
            return {item["devCommParamName"]: item["defaultValue"] for item in data}


if __name__ == '__main__':
    call = DevCommParamCallImpl()
    # print(call.getDevCommTypeByCommPort("TM01", "COM1"))
    # print(call.getCommPortDefaultValue("COM"))
    # print(call.getDevRunCommParamByBindId("1771108120984514562", "COM1"))
