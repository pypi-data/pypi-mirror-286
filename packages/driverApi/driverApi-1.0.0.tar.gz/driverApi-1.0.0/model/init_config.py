# author: haoliqing
# date: 2023/10/19 17:12
# desc:

import configparser
from typing import List

from common import common_utils

conf = configparser.ConfigParser()  # 类的实例化
conf.read(common_utils.get_absolute_path('config/device_service.ini'), encoding='utf-8')


def is_local_run() -> bool:
    """是否本地运行模式"""
    str_flag = conf.get('common', 'local_run')
    if "true" == str_flag.lower():
        return True
    else:
        return False


def show_message() -> bool:
    """是否本地展示提示信息"""
    mode = conf.get('common', 'message_model')
    if 'LOCAL' == mode.upper():
        return True
    else:
        return False


def get_remote_base_url() -> str:
    """ 远程服务基本路径 """
    ip = conf.get('remote', 'ip')
    port = conf.get('remote', 'port')
    path = conf.get('remote', 'path')
    baseUrl = f"http://{ip}:{port}{path}"
    return baseUrl


def get_network_card_name() -> List:
    """ 获取配置文件中的所有网卡名称 """
    netCardNames = []
    options = conf.options('network_card')
    for option in options:
        value = conf.get('network_card', option)
        netCardNames.append(value)
    return netCardNames


def is_start_push() -> bool:
    str_flag = conf.get('common', 'start_push')
    if "true" == str_flag.lower():
        return True
    else:
        return False


if __name__ == '__main__':
    print(get_network_card_name())
