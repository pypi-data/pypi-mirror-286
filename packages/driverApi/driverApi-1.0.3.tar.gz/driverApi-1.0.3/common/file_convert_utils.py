import os
import platform
import re  # 正则
import tempfile
from typing import Dict, Any

import fitz  # PyMuPDF
import pdfkit  # 将html转为pdf
from PIL import Image, ImageFilter
from bs4 import BeautifulSoup
from reportlab.lib import pagesizes
from reportlab.pdfgen import canvas

from common import get_absolute_path
from logger.device_logger import logger


def image_to_pdf(img_path, center: bool = True, margin: int = 0, rate=1) -> str:
    page_margin = margin  # 页边距设置为30
    page_gravity = center  # 是否居中

    temp_folder = tempfile.mkdtemp()
    file_name = os.path.basename(img_path)[:-4]
    img = Image.open(img_path)
    # 计算图片在A4纸张中的位置和大小
    img_width, img_height = img.size
    page_width, page_height = pagesizes.A4
    # 计算图片在PDF中的位置和大小
    if img_width >= img_height:
        # 横向图片
        pdf_img_width = (page_width - 2 * page_margin) * rate
        pdf_img_height = (img_height / img_width * pdf_img_width)
    else:
        # 竖向图片
        pdf_img_height = (page_height - 2 * page_margin) * rate
        pdf_img_width = (img_width / img_height * pdf_img_height)
    # 创建一个PDF文件
    pdf_path = os.path.join(temp_folder, f'{file_name}.pdf')
    c = canvas.Canvas(pdf_path, pagesize=pagesizes.A4)
    c.setLineWidth(1)
    c.setStrokeColorRGB(0, 0, 0)
    # 计算图像在页面中的偏移位置
    if page_gravity:
        x_offset = (page_width - pdf_img_width) / 2
        y_offset = (page_height - pdf_img_height) / 2
    else:
        x_offset = page_margin
        y_offset = page_height - page_margin - pdf_img_height
    # 将图片绘制到PDF中
    c.drawInlineImage(img_path, x_offset, y_offset, pdf_img_width, pdf_img_height)
    c.save()
    logger.info(f"图片转换完成！pdf保存至{pdf_path}")
    return pdf_path


def pdf_to_images(pdf_path: str, resolution=300) -> Any | list:
    """
       将pdf转换为图片
       @param pdf_path: pdf文件路径
       @param resolution: 图片分辨率
       @return:
       """
    if len(pdf_path) == 0 or ".pdf" != pdf_path[-4:]:
        logger.error("无效的pdf文件")
        return
    elif not os.path.exists(pdf_path):
        logger.error("{0}不存在".format(pdf_path))
        return
    else:
        dir_name = os.path.dirname(pdf_path)
        base_name = os.path.basename(pdf_path)[:-4]
        save_dir = os.path.join(dir_name, base_name)
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
    image_path_list = []
    pdf_document = fitz.open(pdf_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        # 绘制图片的宽高分辨率
        zoom_x = resolution / 72.0  # 1 point is 1/72 inch
        zoom_y = resolution / 72.0
        mat = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        save_path = os.path.join(save_dir, "{0}{1}.jpg".format(base_name, page_num))
        img.save(save_path)
        image_path = __enhance_image(save_path)
        image_path_list.append(image_path)
    return image_path_list


def __enhance_image(image_path):
    """
    增强图片
    @param image_path:
    @return:
    """
    # 使用opencv锐化图片,转为灰度图片，根据阈值转化为黑白图片,opencv+numpy太大，放弃
    # opencv-python==3.4.16.59
    # numpy==1.26.3
    # cv_img = cv2.imread(image_path)
    # kernel = numpy.array([[-1, -1, -1], [-1, 10, -1], [-1, -1, -1]])
    # cv_img = cv2.filter2D(cv_img, -1, kernel)
    # cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    # ret, cv_img = cv2.threshold(cv_img, 175, 255, cv2.THRESH_BINARY)
    # cv2.imwrite(image_path, cv_img)

    img = Image.open(image_path)
    custom_kernel = ImageFilter.Kernel(size=(3, 3), kernel=[-1, -1, -1, -1, 12, -1, -1, -1, -1], scale=None, offset=0)
    img = img.filter(custom_kernel)
    img = img.convert("L")
    img = img.point(lambda p: p > 120 and 255)
    img.save(image_path)
    return image_path


def html_to_pdf(html_info) -> str:
    # 将html内容临时写入html文件中
    html_info = __set_page_image(html_info)
    temp_folder = tempfile.mkdtemp()
    html_file_path = tempfile.mkstemp(".html", "", temp_folder, True)[1]
    with open(html_file_path, "w+t", encoding="UTF-8") as f:
        f.write(html_info)
    pdf_output_path = tempfile.mkstemp(".pdf", "", temp_folder, True)[1]
    # 默认样式文件路径
    css1_path = get_absolute_path("common/css/hiprint.css")
    css2_path = get_absolute_path("common/css/print-lock.css")
    css = [css1_path, css2_path]
    # 设置参数
    global_options: Dict = {
        'enable-local-file-access': '--enable-local-file-access',
        'enable-smart-shrinking': '--disable-smart-shrinking',
        'user-style-sheet': '--user-style-sheet',
    }
    page_property = __set_page_property(html_info)
    global_options.update(page_property)
    try:
        pdfkit.from_file(html_file_path, pdf_output_path, css=css, configuration=__MyConfiguration(),
                         options=global_options)
        # 去除pdf空白页
        file_name, file_extension = os.path.splitext(pdf_output_path)
        dst_file = f"{file_name}_copy{file_extension}"
        __remove_blank_pages(pdf_output_path, dst_file)
        logger.info(f"html转换完成!pdf保存至{dst_file}")
        return dst_file
    except IOError as e:
        logger.error(e)


def __set_page_property(html_info) -> Dict:
    """
    设置页面参数
    @param html_info: html内容
    @return: 属性字典
    """
    options: Dict = {}
    soup = BeautifulSoup(html_info, 'html.parser')
    style = soup.find("style")
    # 如果有样式
    if style:
        css_text = style.get_text()
        # 获取margin
        pattern = r'margin:\s*([^;]+)'
        matches = re.findall(pattern, css_text)
        if matches:
            margins = re.split(r'\s+', matches[0].strip())  # 使用一个或多个空格分割匹配的 margin 属性值
            match len(margins):
                case 1:  # margin为1个时，margin: 上 = 右 = 下 = 左;
                    options['margin-top'] = margins[0]
                    options['margin-right'] = margins[0]
                    options['margin-bottom'] = margins[0]
                    options['margin-left'] = margins[0]
                case 2:  # margin为2个时，margin: 上 = 下 左 = 右;
                    options['margin-top'] = margins[0]
                    options['margin-right'] = margins[1]
                    options['margin-bottom'] = margins[0]
                    options['margin-left'] = margins[1]
                case 3:  # margin为3个时，margin:上   左=右   下;
                    options['margin-top'] = margins[0]
                    options['margin-right'] = margins[1]
                    options['margin-bottom'] = margins[2]
                    options['margin-left'] = margins[0]
                case 4:  # margin为4个时，margin:上  右  下  左;（为顺时针方向）
                    options['margin-top'] = margins[0]
                    options['margin-right'] = margins[1]
                    options['margin-bottom'] = margins[2]
                    options['margin-left'] = margins[3]
        # 获取纸张大小
        pattern = r'size:\s*([^;]+)'
        matches = re.findall(pattern, css_text)
        if matches:
            size = matches[0].strip()
            if size[0].isdigit():
                width, height = size.split()
                options["page-width"] = width
                options["page-height"] = height
            else:
                page_size = size.split()
                options["page-size"] = page_size[0]
                if len(page_size) > 1:
                    options["orientation"] = page_size[1]
    return options


def __remove_blank_pages(input_pdf_path, output_pdf_path):
    """
    去除pdf空白页
    @param input_pdf_path:
    @param output_pdf_path:
    @return:
    """
    doc = fitz.open(input_pdf_path)
    pages_to_delete = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        images = page.get_images(full=True)
        # 检测页面文本为空或只包含空白字符 并且 没有图片信息才算是空白页
        if not text.strip() and len(images) == 0:
            pages_to_delete.append(page_num)
    # 从后向前删除页，避免页码错乱
    for page_num in reversed(pages_to_delete):
        doc.delete_page(page_num)
    doc.save(output_pdf_path)
    doc.close()


def __set_page_image(html_info: str) -> str:
    soup = BeautifulSoup(html_info, 'html.parser')
    img_tags = soup.find_all("img")
    for img_tag in img_tags:
        # TODO 根据具体情况对src属性进行修改
        img_tag["src"] = get_absolute_path("./common/css/image/hi.png")
    return str(soup)


class __MyConfiguration:
    def __init__(self, wkhtmltopdf='', meta_tag_prefix='pdfkit-', environ=''):
        self.meta_tag_prefix = meta_tag_prefix
        self.wkhtmltopdf = wkhtmltopdf
        try:
            if not self.wkhtmltopdf:
                if platform.system() == "Windows":
                    self.wkhtmltopdf = get_absolute_path("dll/wkhtmltox/Windows//binary/wkhtmltopdf.exe")
                elif platform.system() == "Linux":
                    self.wkhtmltopdf = get_absolute_path("dll/wkhtmltox/Linux/binary/wkhtmltopdf")
            lines = self.wkhtmltopdf.splitlines()
            if len(lines) > 0:
                self.wkhtmltopdf = lines[0].strip()
            with open(self.wkhtmltopdf) as f:
                pass
        except (IOError, FileNotFoundError) as e:
            raise IOError('No wkhtmltopdf executable found: "%s"\n'
                          'If this file exists please check that this process can '
                          'read it or you can pass path to it manually in method call, '
                          'check README. Otherwise please install wkhtmltopdf - '
                          'https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf' % self.wkhtmltopdf)

        self.environ = environ

        if not self.environ:
            self.environ = os.environ

        for key in self.environ.keys():
            if not isinstance(self.environ[key], str):
                self.environ[key] = str(self.environ[key])


if __name__ == '__main__':
    # with open("D:/Gientech/hiprint_test/A4.html", "r", encoding="UTF-8") as file:
    #     htmlContent = file.read()
    # html_to_pdf(htmlContent)
    image = pdf_to_images("D:/hzbank.pdf")
    print(image)
    # image_to_pdf("D:\\hzbank\\hzbank0.jpg", False)
    # set_page_image(htmlContent)
    # remove_blank_pages("C:\\Users\\maosh\\AppData\\Local\\Temp\\tmpoj675i5b\\la5zxq6k.pdf", "D:/TempFile/OK.pdf")
