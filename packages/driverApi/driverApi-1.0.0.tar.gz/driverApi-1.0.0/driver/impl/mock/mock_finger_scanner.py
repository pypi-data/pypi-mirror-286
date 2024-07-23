# author: haoliqing
# date: 2024/1/4 16:13
# desc:
from typing import List

from driver.finger_scanner import FingerScanner, TemplatesInfo
from logger.device_logger import logger


class MockFingerScanner(FingerScanner):
    """模拟指纹仪驱动实现类"""
    def get_finger_template(self, finger_num: int) -> TemplatesInfo:
        logger.info("收到的需要采集的指纹模板数量：{}".format(finger_num))
        info = TemplatesInfo()
        templates = []
        counter = 0
        while counter < finger_num:
            counter += 1
            templates.append("第{}个指纹模板".format(counter))
        info.data = templates
        return info

    def get_finger_feature(self) -> str:
        return "MockFingerFeature:1111111111111333333333"

    def verify_finger(self, template_list: List[str]) -> int:
        logger.info("收到的指纹模板列表：{}".format(template_list))
        return 0
