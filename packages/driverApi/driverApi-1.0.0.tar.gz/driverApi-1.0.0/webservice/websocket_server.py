# author: haoliqing
# date: 2023/10/10 10:26
# desc:

import asyncio
import threading

import websockets
from control.device_controller import DeviceController
from model.init_config import conf

device_ctl: DeviceController = DeviceController()

websocket_users = set()


# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_user_msg(websocket):
    while True:
        recv_text = await websocket.recv()
        device_ctl.execute(recv_text, websocket)
        # await websocket.send(response_text)


async def send_msg(websocket, resp_msg):
    await websocket.send(resp_msg)


# 服务器端主逻辑
async def run(websocket, path):
    while True:
        try:
            websocket_users.add(websocket)
            await recv_user_msg(websocket)
        except websockets.ConnectionClosed:
            print("ConnectionClosed...", path)  # 链接断开
            print("websocket_users old:", websocket_users)
            websocket_users.remove(websocket)
            print("websocket_users new:", websocket_users)
            break
        except websockets.InvalidState:
            print("InvalidState...")  # 无效状态
            break
        except Exception as e:
            print("Exception:", e)


def start():
    # 启动WebSocket服务器
    start_socket_server = websockets.serve(run, 'localhost', 8765)

    # 运行事件循环
    asyncio.get_event_loop().run_until_complete(start_socket_server)
    asyncio.get_event_loop().run_forever()
    print("websocket服务启动成功")


# 启动服务器
async def run_server():
    async with websockets.serve(run, 'localhost', conf.get('websocket', 'port')):
        await asyncio.Future()  # run forever


# 多协程模式，防止阻塞主线程无法做其他事情
def web_socket_server():
    asyncio.run(run_server())


# 多线程启动
def start_server():
    # 多线程启动，否则会堵塞
    thread = threading.Thread(target=web_socket_server)
    thread.start()


if __name__ == '__main__':
    start()
