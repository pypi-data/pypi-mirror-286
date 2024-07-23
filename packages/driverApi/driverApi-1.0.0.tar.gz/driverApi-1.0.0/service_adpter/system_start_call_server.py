import json
from typing import Any, List, Dict

from common.global_constants import *
from service_adpter import DevBindCallImpl, DevCommParamCallImpl, DevParamCallImpl
from service_adpter.impl import TerminalInfoCallImpl


class SystemStartCallServer:

    def __init__(self):
        self.termId = ""
        """ 终端Id """

        self.bind_info: List[Dict] = []
        """ 服务端的设备配置 """

        self.dev_cfg: Dict[str, List[Dict]] = {}
        """ 设备配置数据 """

        self.comm_port_type: Dict = {}
        self.terminalInfoCall = TerminalInfoCallImpl()
        self.devBindCall = DevBindCallImpl()
        self.devCommParamCall = DevCommParamCallImpl()
        self.devParamCall = DevParamCallImpl()

    def get_dev_cfg(self, macAddr) -> Any:
        """
        外设服务启动时，根据本终端的mac地址查询绑定信息
        @param macAddr: 终端mac地址
        @return:
        """
        self.bind_info.clear()
        self.dev_cfg.clear()
        # 根据终端mac地址查询本终端在数据库中的终端id
        terminalInfo = self.terminalInfoCall.getTerminalInfoByMac(macAddr)
        if terminalInfo:
            # 数据库能查到本终端信息
            self.termId = terminalInfo.get("termId")
            termModelId = terminalInfo.get("termModelId")
            commTypeList: List = self.terminalInfoCall.getCommType(termModelId)
            for item in commTypeList:
                self.comm_port_type[item[1]] = item[2]
            # 根据终端id查询绑定信息
            self.bind_info = self.devBindCall.getBindDevAsOtherInfo(self.termId)
            for bindInfo in self.bind_info:
                # self.devClassList.append(bindInfo.get("devClassName"))
                self.dev_cfg[bindInfo.get("devClassName")] = []
            for item in self.bind_info:
                dev_class_name = item["devClassName"]
                if dev_class_name in self.dev_cfg:
                    childDict: Dict = {TERM_ID: self.termId,
                                       DEV_STATUS: item.get("status"),
                                       DEV_CLASS_NAME: item.get("devClassName"),
                                       DEV_CLASS_DESC: item.get("devClassDesc"),
                                       DEV_MODEL_NAME: item.get("devModelName"),
                                       DEV_MODEL_DESC: item.get("devModelDesc")}
                    devParam = self.getDevModelParam(item)
                    if devParam and len(devParam) > 0:
                        childDict[DEV_PARAM] = devParam
                    childDict[PORT] = self.getPortParam(item)
                    self.dev_cfg[dev_class_name].append(childDict)
        return self.dev_cfg

    def getDevModelParam(self, info) -> Dict:
        # 查询设备参数
        return self.devParamCall.getDevParam(info.get("devModelId"), info.get("bindId"))

    def getPortParam(self, info) -> Dict:
        commTypeName = self.comm_port_type.get(info.get("commPort"))
        info["commTypeId"] = commTypeName
        portDict = {COMM_TYPE_NAME: commTypeName, COMM_PORT: info.get("commPort")}
        # 查询默认参数
        value = self.devCommParamCall.getCommPortParam(info)
        portDict[COMM_PORT_PARAM] = value
        return portDict


if __name__ == '__main__':
    call = SystemStartCallServer()
    # print()
    cfg = call.get_dev_cfg("D4E98A9C81D1")
    print(json.dumps(cfg, ensure_ascii=False))
