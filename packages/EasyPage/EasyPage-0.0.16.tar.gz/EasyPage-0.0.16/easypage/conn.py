"""
    使用了 EventEmitter 作为事件管理

    # 创建事件监听案例
    async def intercept(kwargs) -> None:
        print(kwargs)
        interception_id = kwargs["interceptionId"]

        await page_conn.send(
            method="Network.continueInterceptedRequest",
            params={"interceptionId": interception_id},
        )

    page_conn.on("Network.requestIntercepted", lambda event: loop.create_task(intercept(event)))

    异步这里代码结构有问题，仅针对 send 方法
        事件监听，监听到事件之后将会触发 loop.run_until_complete 操作
        同时同步程序也会有 loop.run_until_complete 就会造成报错：This event loop is already running
        需要对代码结构做处理，如有统一的事件发送地址，或者使用类似队列的结构
"""
import json
import time
import typing
import asyncio
import threading
import traceback
import websocket
import websockets
from threading import Lock
from easypage import errors, settings
from pyee import EventEmitter
from easypage.logger import logger
from queue import SimpleQueue, Empty
from websockets.legacy import client

TYPE_PAGE = "page"
TYPE_BROWSER = "browser"

DRIVER_TYPE = typing.Union[
    TYPE_BROWSER,
    TYPE_PAGE
]


class Conn(EventEmitter):

    def __init__(self, address: str, driver_type: DRIVER_TYPE, driver_id: str, timeout: int = None):
        """
        # 页面连接
        ws://127.0.0.1:9223/devtools/page/87B827CF2CAF710C997699F858467545

        # 浏览器连接
        ws://127.0.0.1:9223/devtools/browser/0909caac-09eb-4f48-a481-5de5decb3583

        :param address: 连接地址，如：127.0.0.1:9223
        :param driver_type: 控制类型，如：TYPE_PAGE
        :param driver_id: 对应 id，如：87B827CF2CAF710C997699F858467545
        :param timeout: 配置的超时时间
        """
        super().__init__()
        self.address = address
        self.driver_id = driver_id
        self.driver_type = driver_type
        self.driver_url = f"ws://{address}/devtools/{driver_type}/{driver_id}"
        self.timeout = timeout or settings.TIMEOUT

        self.__lock = threading.Lock()
        self.__id: int = 0
        self.__stop: bool = False
        self.__ws: WebSocket = None  # type:ignore
        self.__result_monitor = {}  # 存储结果
        self.__new_conn()

    def __new_conn(self):
        """
        与浏览器建立连接

        :return:
        """
        self.__ws = websocket.create_connection(
            url=self.driver_url,
            enable_multithread=False,
            suppress_origin=True
        )
        threading.Thread(target=self.__recv_result, daemon=True).start()

    def send(
            self,
            method: str,
            params: dict = None,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> typing.Tuple[bool, dict]:
        """
        同步发送消息

        使用：status, value = send(method="", raise_err=False, params={})

        返回的结果是有两个值：
            - status 表示当前消息是否有错误发生（raise_err 为 True 时直接抛出）
            - value 是对应浏览器返回的消息，是一个 dict

        :param method:
        :param params:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return
        """
        # 判断连接是否正常
        if self.closed():
            return False, dict()

        # 发送消息
        status, msg = self.__send(
            method=method,
            params=params,
            need_callback=need_callback
        )

        if not status:
            return False, dict()
        elif not need_callback:
            return True, msg

        # 等待信息接收
        start_time = time.time()
        while not self.__stop:
            if self.closed():
                break

            try:
                recv_msg = self.__result_monitor[msg["id"]].get(timeout=0.1)  # 短等待，避免有问题卡着
                if "result" in recv_msg:
                    return True, recv_msg["result"]
                elif "error" in recv_msg:
                    if raise_err:
                        raise errors.CDPRecvErrorMsg(recv_msg["error"])
                    return False, recv_msg["error"]

                logger.warning("没有结果：{}", recv_msg)
            except Empty:
                if time.time() - start_time >= self.timeout:
                    self.__remove_result(msg_id=msg["id"])
                    if raise_err:
                        raise errors.CDPRecvTimeout(msg)
                    logger.warning("接收超时：{}", msg)
                    break

        return False, dict()

    def __send(
            self,
            method: str,
            params: dict = None,
            raise_err: bool = False,
            need_callback: bool = True,
    ) -> typing.Tuple[bool, dict]:
        """
        同步发送消息

        使用：status, value = send(method="", raise_err=False, params={})

        返回的结果是有两个值：
            - status 表示当前消息是否有错误发生（raise_err 为 True 时直接抛出）
            - value 是对应浏览器返回的消息，是一个 dict

        :param method:
        :param params:
        :param raise_err: 接收到错误消息时，是否抛出，默认为 False
        :param need_callback: 接收到消息时，是否返回，默认为 True
        :return
        """
        # 构建消息
        msg = {
            "id": self.__get_id,
            "method": method,  # 在此示例中启用网络事件
            "params": params
        }

        if need_callback:
            self.__result_monitor[msg["id"]] = SimpleQueue()

        msg_json = json.dumps(msg)
        logger.debug("[SEND] {}", msg_json)

        # 发送信息
        try:
            self.__ws.send(msg_json)
            return True, msg
        except (websocket.WebSocketConnectionClosedException, ConnectionResetError, BrokenPipeError, OSError):
            self.__stop = True
            if raise_err:
                raise errors.CDPConnClosed(f"连接已断开：{self.driver_url}")
            else:
                logger.warning("连接已断开：{}", self.driver_url)
        except:
            traceback.print_exc()
            raise

        return False, dict()

    def __recv_result(self):
        """
        接收消息、事件处理

        :return:
        """
        while not self.__stop:
            try:
                msg = self.__ws.recv()
                logger.debug("[RECV] {}", msg)
                msg = json.loads(msg)
            except websocket.WebSocketTimeoutException:
                continue
            except (websocket.WebSocketConnectionClosedException, ConnectionResetError, BrokenPipeError, OSError):
                logger.warning("连接已断开：{}", self.driver_url)
                self.__stop = True
                return
            except Exception:
                if self.__stop:
                    return
                else:
                    self.__stop = True
                    raise

            # 消息处理
            if msg.get("id"):
                has_error = False
                if msg.get("error"):
                    logger.warning("[RECV] {}", msg["error"])
                    has_error = True

                # 消息 id 存在的话就是需要立刻回调
                if msg["id"] in self.__result_monitor:
                    self.__add_result(msg_id=msg["id"], result=msg)
                else:
                    # 判断响应-body 获取事件的触发
                    event_name = f"Network.getResponseBody-{msg['id']}"
                    if event_name in self._events:
                        if has_error:
                            self.emit(event=event_name, status=False, body_data=msg["error"])
                        else:
                            self.emit(event=event_name, status=True, body_data=msg["result"])

            elif "method" in msg:
                method = msg.get("method", "")
                params = msg.get("params", {})
                if method in self._events:
                    self.emit(event=method, **params)

    def closed(self) -> bool:
        """
        判断连接是否断开，同时做一点处理

        :return:
        """
        if self.__stop:
            return True

        status = self.__ws.connected
        if not status:
            self.__stop = True

        return not status

    def close(self):
        """
        停止运行

        :return:
        """
        self.__stop = True
        self.__ws.close()

    def __add_result(self, msg_id: int, result: dict):
        """
        添加监控结果

        :param msg_id:
        :param result:
        :return:
        """
        if msg_id in self.__result_monitor:
            self.__result_monitor[msg_id].put(result)

    def __remove_result(self, msg_id: int):
        """
        移除监控

        :param msg_id:
        :return:
        """
        if msg_id in self.__result_monitor:
            del self.__result_monitor[msg_id]

    @property
    def __get_id(self):
        """
        获取一个消息 id

        :return:
        """
        self.__lock.acquire(timeout=2)
        self.__id += 1
        self.__lock.release()

        return self.__id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
