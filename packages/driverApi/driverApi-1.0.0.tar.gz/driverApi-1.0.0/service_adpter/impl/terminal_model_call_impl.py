import json
from typing import Dict

from common import global_constants
from service_adpter.api.device_api import APIEndpoint
from service_adpter.send_request import send
from service_adpter.terminal_model_call import TerminalModelCall
from model import init_config


class TerminalModelCallImpl(TerminalModelCall):
    def getTerminalModels(self) -> Dict:
        if init_config.is_local_run():
            return {"TM00": "TM00-通用终端"}
        else:
            respBody = send(APIEndpoint.get_terminal_models)
            if respBody and respBody.get(global_constants.SUCCESS, []):
                respData: list = respBody.get("data", [])
                if respData and len(respData) > 0:
                    return {item["termModelId"]: f"{item['termModelId']}-{item['termModelDesc']}" for item in
                            respData}


if __name__ == '__main__':
    impl = TerminalModelCallImpl()
    models = impl.getTerminalModels()
    print(models)
