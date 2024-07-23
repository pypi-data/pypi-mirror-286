from typing import Dict, List

import psutil

from common import Singleton, global_constants
from model import init_config
from service_adpter.api.device_api import APIEndpoint
from service_adpter.send_request import send
from service_adpter.terminal_info_call import TerminalInfoCall


@Singleton
class TerminalInfoCallImpl(TerminalInfoCall):

    def addTerminalInfo(self, data):
        return send(APIEndpoint.add_terminal_info, data=data)

    def updateTerminalInfo(self, data):
        send(APIEndpoint.update_terminal_info, data=data)

    def getTerminalInfoByMac(self, macAddr) -> Dict | None:
        if macAddr is None:
            return None
        elif init_config.is_local_run():
            return {"termModelId": "TM00", "termId": "00000000", "termDesc": "本地运行终端"}
        params = {
            "termFeature": macAddr
        }
        respBody = send(APIEndpoint.get_terminal_info_by_mac, params=params)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            respData: list = respBody.get("data", [])
            if respData and len(respData) > 0:
                return respData[0]
            else:
                return None

    def getMacAddr(self) -> str | None:
        # 查询到所有网卡名称
        netCardNames = init_config.get_network_card_name()
        # 依次查找mac地址
        for netCardName in netCardNames:
            interfaces = psutil.net_if_addrs()
            if netCardName in interfaces:
                nic = interfaces[netCardName]
                for address in nic:
                    if address.family == psutil.AF_LINK:
                        return address.address.replace("-", "")
        return None

    def getCommType(self, termModelId) -> List | None:
        if init_config.is_local_run():
            return [('LPT', 'LPT', 'LPT'), ('USB', 'USB', 'USB'), ('COM1', 'COM1', 'COM'), ('COM2', 'COM2', 'COM')]
        retData: list = []
        params = {
            "termModelId": termModelId
        }
        respBody = send(APIEndpoint.get_comm_type, params=params)
        if respBody and respBody.get(global_constants.SUCCESS, None):
            data: list = respBody["data"]
            for index, item in enumerate(data):
                retData.append((f"{item.get('commTypeId')}-{item.get('commPort')}", item.get("commPort"),
                                item.get("commTypeId")))
            return retData
        return None


if __name__ == '__main__':
    call = TerminalInfoCallImpl()
    print(call.getMacAddr())
