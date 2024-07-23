# author: haoliqing
# date: 2024/5/8 14:24
# desc:
import mimetypes
import os
import shutil
from typing import List

from common.file_convert_utils import html_to_pdf, pdf_to_images
from device.device_config import DeviceConfig
from driver.file_printer import FilePrinter, MultiFilePrintResult, SingleFilePrintResult
from logger.device_logger import logger


class LinuxPrinter(FilePrinter):
    def __init__(self):
        from cups import Connection
        super().__init__()
        self.prt_name = None
        self.conn = Connection()

    def init(self, device_cfg: DeviceConfig) -> int:
        super().__init__()
        if self.conn is None:
            logger.error("连接打印机服务异常！")
            return -1
        printers = self.conn.getPrinters()
        print(printers)
        try:
            devParam = device_cfg.device_model_param
            actual_printer_name = None
            if devParam:
                printer_name = devParam['printer_name']
                if printer_name and printer_name.strip() != "":
                    logger.info("配置的打印机名称为" + printer_name)
                    printers = self.conn.getPrinters()
                    print(printers)
                    for name in printers.keys():
                        if printer_name == name:
                            actual_printer_name = printer_name
                            break
                    if not actual_printer_name:
                        logger.warning("未获取到名为{0}的打印机，获取默认打印机".format(printer_name))
                        actual_printer_name = self.conn.getDefault()
                else:
                    logger.info("未指定打印机名称，获取默认打印机")
                    actual_printer_name = self.conn.getDefault()
            else:
                actual_printer_name = self.conn.getDefault()
            if not actual_printer_name:
                logger.error("未获取到任何打印机驱动")
                return -1
            else:
                self.prt_name = actual_printer_name
                return 0
        except Exception as e:
            logger.error(e)
            return -1

    def print_single_file(self, file_path: str) -> SingleFilePrintResult:
        result = SingleFilePrintResult()
        file_type = self.get_file_type_by_mime(file_path)
        if file_type:
            if file_type == "application/pdf":
                self.print_pdf(file_path)
            elif file_type == "text/plain":
                self.print_text(file_path)
            elif file_type.startswith("image"):
                self.print_image(file_path)
            else:
                result.error_code = -1
                result.error_msg = "不支持的文件类型{0}".format(file_type)
                logger.error(result.error_msg)
        else:
            result.error_code = -1
            result.error_msg = "无法识别文件{0}的类型".format(file_path)
            logger.error(result.error_msg)
        return result

    def print_multi_file(self, file_path_list: List[str]) -> MultiFilePrintResult:
        pass

    def print_html_data(self, html_info: str):
        pdf_path = html_to_pdf(html_info)
        self.print_single_file(pdf_path)

    def print_image(self, file_path: str):
        # TODO 这里需要根据打印文件设置纸张方向
        print_options = {
            'media': 'A5',
            'landscape': 'portrait',
            'fit-to-page': 'true'
        }
        """
        'media':纸张大小，A4，A5，Letter ...
        'landscape': 布局方向：横向（landscape）纵向（portrait）
        'scaling':缩放比例，将内容按比例缩小或放大
        'page-top','page-bottom','page-left','page-right':设置页面页边距
        
        """

        self.conn.printFile(self.prt_name, file_path, "Print Image Job", print_options)

    def print_pdf(self, file_path: str):
        """
        静默打印pdf
        :param file_path: pdf 文件绝对路径
        :return:
        """
        images = pdf_to_images(file_path)
        try:
            if len(images) > 0:
                for image_path in images:
                    self.print_image(image_path)
        except Exception as e:
            logger.error("Print Image Exception：{0}".format(e.with_traceback(None)))
        finally:
            logger.info("清理临时文件")
            if len(images) > 0:
                for image in images:
                    if os.path.exists(image):
                        os.remove(image)
                dirname = os.path.dirname(images[0])
                if os.path.exists(dirname):
                    shutil.rmtree(dirname)

    def print_text(self, file_path: str):
        pass

    def read_file(self, file_path: str):
        pass

    @staticmethod
    def get_file_type_by_mime(filename):
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type


if __name__ == '__main__':
    cfg_info = {'devClassDesc': '激光打印机', 'devClassName': 'LaserPrinter', 'devModelDesc': '系统打印机',
                'devModelName': 'SystemPrinter', "devParam": {"printer_name": "NPI82F456"},
                'port': {'commPort': 'COM1', 'commTypeName': 'COM'}, 'status': '1',
                'termId': 'term1'}
    # NPI82F456
    dev_cfg = DeviceConfig(cfg_info)
    printer = LinuxPrinter()
    printer.init(dev_cfg)
    printer.print_image("/home/msm/Desktop/hzbank/hzbank0.jpg")
    # printer.print_single_file("/home/msm/Desktop/hzbank.pdf")
