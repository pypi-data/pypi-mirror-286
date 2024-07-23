# author: haoliqing
# date: 2024/5/8 14:24
# desc:
import mimetypes
import os
import platform
import shutil
from typing import List

import win32con
import win32ui
from PIL import Image, ImageWin

from common import html_to_pdf, common_utils, pdf_to_images

if platform.system() == 'Windows':
    import win32print
from device.device_config import DeviceConfig
from driver.file_printer import FilePrinter, MultiFilePrintResult, SingleFilePrintResult
from logger.device_logger import logger


class WindowsPrinter(FilePrinter):

    def __init__(self):
        super().__init__()
        self.prt_name = None

    def init(self, device_cfg: DeviceConfig) -> int:
        super().init(device_cfg)
        try:
            devParam = device_cfg.device_model_param
            actual_printer_name = None
            if devParam:
                printer_name = devParam['printer_name']
                if printer_name and printer_name.strip() != "":
                    logger.info("配置的打印机名称为" + printer_name)
                    printers = win32print.EnumPrinters(
                        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
                    for printer in printers:
                        if printer_name == printer[2]:
                            actual_printer_name = printer_name
                            break
                    if not actual_printer_name:
                        logger.warn("未获取到名为{0}的打印机，获取默认打印机".format(printer_name))
                        actual_printer_name = win32print.GetDefaultPrinter()
                else:
                    logger.info("未指定打印机名称，获取默认打印机")
                    actual_printer_name = win32print.GetDefaultPrinter()
            else:
                actual_printer_name = win32print.GetDefaultPrinter()

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

    def get_file_type_by_mime(self, filename):
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type

    def print_html_data(self, html_info: str):
        pdf_path = html_to_pdf(html_info)
        self.print_single_file(pdf_path)

    def print_image(self, file_path: str):
        """
        打印图片
        :param file_path:  图片文件绝对路径
        :return:
        """
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(self.prt_name)
        printable_area = hDC.GetDeviceCaps(win32con.HORZRES), hDC.GetDeviceCaps(win32con.VERTRES)
        printer_size = hDC.GetDeviceCaps(win32con.PHYSICALWIDTH), hDC.GetDeviceCaps(win32con.PHYSICALHEIGHT)
        printer_margins = hDC.GetDeviceCaps(win32con.PHYSICALOFFSETX), hDC.GetDeviceCaps(win32con.PHYSICALOFFSETY)

        '''
        # 获取设备的可打印区域水平分辨率（像素点） 如 4761
        horz_res = hDC.GetDeviceCaps(win32con.HORZRES)
        # 获取设备的可打印区域垂直分辨率（像素点） 如 6816
        vert_res = hDC.GetDeviceCaps(win32con.VERTRES)
        # 获取设备可打印区域横向宽度（mm） 如 202
        horz_size = hDC.GetDeviceCaps(win32con.HORZSIZE)
        # 获取设备可打印区域纵向高度（mm） 如 289
        vert_size = hDC.GetDeviceCaps(win32con.VERTSIZE)
        # 获取设备的水平分辨率（像素点） 如 4961
        physical_width = hDC.GetDeviceCaps(win32con.PHYSICALWIDTH)
        # 获取设备的垂直分辨率（像素点） 如 7016
        physical_height = hDC.GetDeviceCaps(win32con.PHYSICALHEIGHT)
        # 获取设备的横向边距（像素点） 如 100
        physical_offsetx = hDC.GetDeviceCaps(win32con.PHYSICALOFFSETX)
        # 获取设备的纵向边距（像素点） 如 100
        physical_offsety = hDC.GetDeviceCaps(win32con.PHYSICALOFFSETY)
        # 水平缩放因子  0  显示器适用
        scaling_factorx = hDC.GetDeviceCaps(win32con.SCALINGFACTORX)
        # 垂直缩放因子 0  显示器适用
        scaling_factory = hDC.GetDeviceCaps(win32con.SCALINGFACTORY)
        # 水平方向dpi  600
        dpi_x = hDC.GetDeviceCaps(win32con.LOGPIXELSX)
        # 垂直方向dpi   600
        dpi_y = hDC.GetDeviceCaps(win32con.LOGPIXELSY)

        # 输出获取的信息
        print("Horizontal Resolution:", horz_res)
        print("Vertical Resolution:", vert_res)
        print("Horizontal Size (mm):", horz_size)
        print("Vertical Size (mm):", vert_size)
        print("physical_width:", physical_width)
        print("physical_height:", physical_height)
        print("physical_offsetx:", physical_offsetx)
        print("physical_offsety:", physical_offsety)
        print("scaling_factorx:", scaling_factorx)
        print("scaling_factory:", scaling_factory)
        print("dpi_x:", dpi_x)
        print("dpi_y:", dpi_y)
        '''

        bmp = Image.open(file_path)

        # 如果图片宽度比高度大的话，旋转90度，以保证最大限度铺满打印区域
        # if bmp.size[0] > bmp.size[1]:
        #     bmp = bmp.rotate(90)

        ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        scale = min(ratios)

        hDC.StartDoc(file_path)
        hDC.StartPage()

        dib = ImageWin.Dib(bmp)
        scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
        x1 = int((printer_size[0] - scaled_width) / 2)
        y1 = int((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width
        y2 = scaled_height
        dib.draw(hDC.GetHandleOutput(), (x1, 0, x2, y2))

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()

    def print_pdf(self, file_path: str):
        """
        静默打印pdf
        :param file_path: pdf 文件绝对路径
        :return:
        """
        # 黑白打印
        # win32api.ShellExecute(0, 'open', self.gsprint_path,
        #                       '-ghostscript "' + self.ghostscript_path + '" -printer "' + self.prt_name + '" "' +
        #                       file_path + '"', '.', 0)
        # '''
        # # 彩色打印
        # win32api.ShellExecute(0, 'open', self.gsprint_path,
        #                       '-color -q -ghostscript "' + self.ghostscript_path + '" -printer "' + self.prt_name + '" "' +
        #                       file_path + '"', '.', 0)
        # '''
        # return 0
        images = pdf_to_images(file_path)
        try:
            if len(images) > 0:
                for image_path in images:
                    self.print_image(image_path)
        except Exception as e:
            logger.error("Print Image Exception：{}".format(e))
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
        content = self.read_file(file_path)
        print_content = content.decode("gbk")
        printer_dc = win32ui.CreateDC()
        printer_dc.CreatePrinterDC(self.prt_name)

        printer_dc.StartDoc(file_path)
        printer_dc.StartPage()

        printer_dc.TextOut(0, 0, print_content)  # 在 0，0 位置开始打印

        printer_dc.EndPage()
        printer_dc.EndDoc()
        printer_dc.DeleteDC()

    def read_file(self, file_path: str):
        """根据文件路径读取文件并返回文件内容"""
        file_data = None
        try:
            with open(file_path, 'rb') as file_data:
                return file_data.read()
        except FileNotFoundError:
            logger.error('读取文件[{0}]时发生异常：无法打开指定的文件!'.format(file_path))
        except LookupError:
            logger.error('读取文件[{0}]时发生异常：指定了未知的编码!'.format(file_path))
        except UnicodeDecodeError:
            logger.error('读取文件[{0}]时发生异常：读取文件时解码错误!'.format(file_path))


if __name__ == '__main__':
    cfg_info = {'devClassDesc': '激光打印机', 'devClassName': 'LaserPrinter', 'devModelDesc': '系统打印机',
                'devModelName': 'SystemPrinter', "devParam": {"printer_name": "NPI82F456 (HP LaserJet M1536dnf MFP)"},
                'port': {'commPort': 'COM1', 'commTypeName': 'COM'}, 'status': '1',
                'termId': 'term1'}
    dev_cfg = DeviceConfig(cfg_info)
    printer = WindowsPrinter()
    printer.init(dev_cfg)
    printer.print_single_file("D:/hzbank.pdf")
    # printer.print_single_file("D:\\MyPicture\\png矢量图\\玩球的猫.png")
    # with open("D:\\hiprint_test\\A5.html", "r", encoding="UTF-8") as file:
    #     htmlContent = file.read()
    # printer.print_html_data(htmlContent)
    # CITIC OKI
    # NPI82F456 (HP LaserJet M1536dnf MFP)
    # Microsoft Print to PDF
    '''
    win32api.ShellExecute(0, "print", "D://test.pdf", None, ".", 0)
    printer_name = win32print.GetDefaultPrinter()
    win32api.ShellExecute(0, "print", "D://test.pdf", '/d:"%s"' % printer_name, ".", 0)
    '''
