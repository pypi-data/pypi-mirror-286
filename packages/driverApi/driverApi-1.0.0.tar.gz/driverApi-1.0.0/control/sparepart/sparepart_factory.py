# author: haoliqing
# date: 2023/9/19 17:02
# desc:

from typing import Dict
from control.sparepart.abstract_sparepart import AbstractSparePart
from common import Singleton
from control.sparepart.impl.system_start import SystemStart
from control.sparepart.impl.receipt_print import ReceiptPrint
from control.sparepart.impl.read_kpd_pwd import ReadKpdPwd
from control.sparepart.impl.read_pboc_ic import ReadPbocIC


@Singleton
class SparePartFactory(object):
    """请求数据零配件工厂"""

    spare_part_cfg: Dict[str, AbstractSparePart] = {}
    """ 零配件定义 {功能名称:零配件实现}"""

    def __init__(self):
        self.spare_part_cfg['SystemStart'] = SystemStart()
        self.spare_part_cfg['SystemRestart'] = SystemStart()
        self.spare_part_cfg['ReadKpdPwd'] = ReadKpdPwd()
        self.spare_part_cfg['ReadKpdCfmPwd'] = ReadKpdPwd()
        self.spare_part_cfg['ReceiptPrint'] = ReceiptPrint()
        self.spare_part_cfg['PrintView'] = ReceiptPrint()
        self.spare_part_cfg['JournalPrint'] = ReceiptPrint()
        self.spare_part_cfg['LaserPrint'] = ReceiptPrint()
        self.spare_part_cfg['ReadPBOCICCard'] = ReadPbocIC()
        self.spare_part_cfg['TranReadPBOCICCard'] = ReadPbocIC()

    def get_spare_part(self, func_name: str):
        return self.spare_part_cfg.get(func_name, None)


if __name__ == '__main__':
    factory1 = SparePartFactory()
    factory2 = SparePartFactory()
    print(factory1 == factory2)
    print(id(factory1))
    print(id(factory2))
