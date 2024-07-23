import json
import tkinter as tk
from tkinter import messagebox
from typing import Dict

import requests
from requests import RequestException, Timeout

import model.init_config as init_config
from logger.device_logger import logger
from service_adpter.api.device_api import APIEndpoint

baseUrl = init_config.get_remote_base_url()

isTimeOut = False


def send(apiPath: APIEndpoint, params=None, data=None) -> Dict | None:
    global isTimeOut
    method = apiPath.value[1].value
    url = baseUrl + apiPath.value[0]
    if isTimeOut:
        return
    response = None
    try:
        if method == 'GET':
            response = requests.get(url, params=params, timeout=5)
        elif method == 'POST':
            response = requests.post(url, params=params, json=data, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, params=params, json=data, timeout=5)
        elif method == 'DELETE':
            response = requests.delete(url, params=params, timeout=5)
        else:
            raise ValueError("Unsupported HTTP method")
        if response and response.status_code == 200:
            return json.loads(response.text)
        else:
            return None
    except Timeout as e:
        logger.error(f"{e}")
        showMessage(f"{baseUrl}请求超时，请检查网络后在设备助手页面点击【保存重启】刷新数据", timeout=10000)
        if response:
            logger.error(response.headers.__dict__)
        isTimeOut = True
        return None
    except RequestException as e:
        logger.error(f"{e}")
        showMessage(f"{e}", timeout=10000)
        if response:
            logger.error(response.headers.__dict__)
        isTimeOut = True
        return None


def showMessage(message, timeout=2500):
    root = tk.Tk()
    root.withdraw()
    try:
        root.after(timeout, root.destroy)
        messagebox.showwarning('网络异常', message, master=root)
    except:
        pass
