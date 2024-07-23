# author: haoliqing
# date: 2024/1/4 16:26
# desc:
from driver.evaluator import Evaluator, EvaluateInfo
from logger.device_logger import logger


class MockEvaluator(Evaluator):
    """模拟评价器驱动实现类"""
    def get_evaluate_result(self, teller_id: str, teller_name: str, teller_photo: str, star_level: int) -> EvaluateInfo:
        logger.info("收到的请求信息：teller_id:{0}, teller_name:{1}, teller_photo:{2}, star_level:{3}"
                    .format(teller_id, teller_name, teller_photo, star_level))
        eva_info = EvaluateInfo()
        eva_info.level = 1
        eva_info.message = '满意'
        return eva_info

    def update_teller_photo(self, file_path: str) -> int:
        logger.info("收到的请求信息：file_path:{0}".format(file_path))
        return 0
