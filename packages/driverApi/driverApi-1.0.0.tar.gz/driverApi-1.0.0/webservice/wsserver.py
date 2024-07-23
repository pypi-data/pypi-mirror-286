# author: haoliqing
# date: 2023/10/10 17:46
# desc:
import asyncio
import os
import sys

import websockets
import time
import json
import threading
from control.device_controller import DeviceController
from logger.device_logger import logger
from model.init_config import conf
from tkinter import messagebox

device_ctl: DeviceController = DeviceController()


# 功能模块
class OutputHandler():
    async def run(self, message, send_ms, websocket):
        # 用户发信息
        await send_ms(message, websocket)
        # 单发消息
        # await send_ms(message, websocket)
        # 群发消息
        # await s('hi起来')


# 存储所有的客户端
Clients = {}

lock = threading.Lock()


# 服务端
class WsServer():
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = conf.get('websocket', 'port')

    # 回调函数(发消息给客户端)
    async def callback_send(self, msg, websocket=None):
        await self.send_msg(msg, websocket)

    # 发送消息
    async def send_msg(self, msg, websocket):
        # websocket不为空，单发，为空，群发消息
        if websocket is not None:
            await websocket.send(msg)

        # 避免被卡线程
        await asyncio.sleep(0.2)

    # 针对不同的信息进行请求，可以考虑json文本
    async def run_case_x(self, json_msg, websocket):
        print('runCase')
        op = OutputHandler()
        # 参数：消息、方法、socket
        await op.run(json_msg, self.callback_send, websocket)

    # 连接一个客户端，起一个循环监听
    async def socket_handler(self, websocket, path):
        # 添加到客户端列表
        lock.acquire()
        try:
            Clients[websocket.id] = websocket
        finally:
            lock.release()
        # 握手
        # await websocket.send(json.dumps({"type": "handshake"}))
        # 循环监听
        while True:
            # 接受信息
            try:
                # 接受文本
                recv_text = await websocket.recv()
                # message = "Get message: {}".format(recv_text)
                # 返回客户端信息
                # await websocket.send(message)
                device_ctl.execute(recv_text, websocket)

                # 对message进行解析，跳进不同功能区
                # await self.runCaseX(jsonMsg=data,websocket=websocket)
            # 链接断开
            except websockets.ConnectionClosed:
                print("ConnectionClosed...", path)
                lock.acquire()
                try:
                    Clients.pop(websocket.id)
                finally:
                    lock.release()
                break
            # 无效状态
            except websockets.InvalidState:
                print("InvalidState...")
                # del Clients
                break
            # 报错
            except Exception as e:
                print("ws连接报错", e)
                # del Clients
                break

    # 启动服务器
    async def run_server(self, conn):
        try:
            async with websockets.serve(self.socket_handler, self.ip, self.port):
                await asyncio.Future()  # run forever
        except OSError as err:
            messagebox.showinfo("提示", "外设服务已启动，不再重复启动！")
            conn.send("terminate")  # 发送终止信号到主进程
            conn.close()
            os._exit(0)

    # 多协程模式，防止阻塞主线程无法做其他事情
    def web_socket_server(self, conn):
        asyncio.run(self.run_server(conn))

    # 多线程启动
    def start_server(self, conn):
        # 多线程启动，否则会堵塞,conn是管道连接对象，用于向主进程发送信号
        thread = threading.Thread(target=self.web_socket_server, args=(conn,))
        thread.start()
        logger.info("启动websocket服务成功")
        # thread.join()


if __name__ == '__main__':
    print("server")
    s = WsServer()
    s.start_server()
