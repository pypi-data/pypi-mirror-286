"""
    浏览器 driver
"""
from typing import Tuple, Union, Dict, List, Callable
from easypage import definition, errors
from easypage.driver.page import PageDriver
from easypage.listener import Listener
from easypage.logger import logger
from easypage.conn import TYPE_BROWSER, TYPE_PAGE
from easypage.driver.driver import Driver
from easypage.options import BrowserOptions
from easypage.utils.other_utils import DoublyLinkedDict


class BrowserDriver(Driver):
    PAGES: Dict[str, "PageDriver"] = {}  # {page_id:page_driver}
    CONTEXTS: Dict[str, Union["BrowserDriver", "ContextDriver"]] = {}  # {context_id:context_driver}
    PAGE_CONTENT_MAPS: Dict[str, str] = {}  # {page_id:context_id}
    CONTENT_PAGE_MAPS: Dict[str, List[str]] = {}  # {context_id:[page_id]}

    # TODO CONTEXT 对 PAGE 是一对多的，不能用双向表

    def __init__(self, opts: BrowserOptions, driver_id: str):
        """

        :param opts:
        :param driver_id:
        """
        super().__init__(opts, TYPE_BROWSER, driver_id)

        # 获取基本信息
        _, targets = self.cdp.target.get_targets()
        self.context_id = targets['targetInfos'][0]['browserContextId']
        self._proxy = self._opts.proxy
        self.__class__.CONTEXTS[self.context_id] = self
        self.__create_page_driver(targets['targetInfos'])  # 启动时创建页面的 driver
        self.__listener = Listener(context_id=self.context_id)

        # 启用事件
        self.cdp.target.set_discover_targets()

        # 事件监听
        self.cdp.on(event="Target.targetCreated", callback=self.__on_target_target_created)
        self.cdp.on(event="Target.targetInfoChanged", callback=self.__on_target_target_info_changed)
        self.cdp.on(event="Target.targetDestroyed", callback=self.__on_target_target_destroyed)

    def __create_page_driver(self, target_infos: List[Dict]):
        """
        根据 target_infos 创建页面的连接

        :param target_infos: 启动时所有的页面信息
        :return:
        """
        for target_info in target_infos:
            if target_info.get("type") != "page":
                continue

            context_id = target_info["browserContextId"]
            proxy = self.__class__.CONTEXTS[context_id]._proxy if context_id in self.__class__.CONTEXTS else None

            # 创建 driver
            page_driver = PageDriver(
                opts=self._opts,
                page_id=target_info["targetId"],  # 页面的 targetId
                context_id=context_id,  # 页面的上下文 id
                context_driver=self.__class__.CONTEXTS[context_id],
                proxy=proxy,
            )
            self.__class__.PAGES[target_info["targetId"]] = page_driver
            self.__class__.PAGE_CONTENT_MAPS[target_info["targetId"]] = context_id

            if context_id not in self.__class__.CONTENT_PAGE_MAPS:
                self.__class__.CONTENT_PAGE_MAPS[context_id] = []
            self.__class__.CONTENT_PAGE_MAPS[context_id].append(target_info["targetId"])

    @property
    def listen(self) -> Listener:
        """
        事件监听

        :return:
        """
        return self.__listener

    def new_context(self, proxy: definition.Proxy = None, **kwargs) -> "ContextDriver":
        """
        创建新上下文（类似于隐身模式）

        :param proxy:
        :param kwargs:
        :return:
        """
        # 检查代理
        if proxy and not self._opts.proxy:
            raise errors.ProxySetError(
                "受限于 chromium 限制，上下文设置代理前一定要给全局设置代理，请使用 set_proxy 设置并重新启动浏览器！"
            )

        # 新建上下文
        _, context_data = self.cdp.target.create_browser_context(
            proxy=proxy.get("server") if proxy else None,
            proxy_pass_list=proxy.get("bypass") if proxy else None,
            **kwargs
        )

        # 存储上下文
        context_driver = ContextDriver(browser_driver=self, context_id=context_data["browserContextId"], proxy=proxy)
        self.__class__.CONTEXTS[context_data["browserContextId"]] = context_driver

        return context_driver

    def new_page(
            self,
            new_window: bool = False,
            context_id: str = None,
            **kwargs
    ) -> "PageDriver":
        """
        创建页面

        :param new_window: 是否打开新窗口
        :param context_id:
        :param kwargs:
        :return:
        """
        kwargs.update({
            "url": "about:blank",  # 必要参数
        })

        if new_window:
            kwargs["newWindow"] = True

        if context_id:
            kwargs["browserContextId"] = context_id

        _, target_data = self.cdp.target.create_target(
            **kwargs
        )

        return self.__class__.PAGES[target_data["targetId"]]

    def close(self):
        """
        关闭浏览器

        :return:
        """
        self.cdp.browser.close()

    """
       事件监听
    """

    def __on_target_target_created(self, *args, **kwargs):
        """
        Target.targetCreated 事件监听器

        :param args:
        :param kwargs:
        :return:
        """
        target_info = kwargs["targetInfo"]
        if target_info.get("type") != "page":
            return

        # 为页面创建 driver
        self.__create_page_driver(target_infos=[target_info])

    def __on_target_target_info_changed(self, *args, **kwargs):
        """
        Target.targetInfoChanged 事件监听器

        :param args:
        :param kwargs:
        :return:
        """

    def __on_target_target_destroyed(self, *args, **kwargs):
        """
        Target.targetDestroyed 事件监听器

        :param args:
        :param kwargs:
        :return:
        """
        target_id = kwargs["targetId"]

        if target_id in self.__class__.PAGES:
            if "target_id" in self.__class__.PAGES:
                del self.__class__.PAGES[target_id]

            if "target_id" in self.__class__.PAGE_CONTENT_MAPS:
                context_id = self.__class__.PAGE_CONTENT_MAPS.pop(target_id)
                self.__class__.CONTENT_PAGE_MAPS[context_id].remove(target_id)


class ContextDriver:

    def __init__(self, browser_driver: BrowserDriver, context_id: str, proxy: definition.Proxy = None):
        """

        :param browser_driver:
        :param context_id:
        :param proxy: 代理
        """
        self._browser_driver = browser_driver
        self.context_id = context_id
        self._proxy = proxy
        self.__listener = Listener(context_id=self.context_id)

    def new_page(
            self,
            new_window: bool = False,
            **kwargs
    ) -> "PageDriver":
        """
        创建页面

        :param new_window: 是否打开新窗口
        :param kwargs:
        :return:
        """
        return self._browser_driver.new_page(
            new_window=new_window,
            context_id=self.context_id,
            proxy=self._proxy,
            **kwargs
        )

    @property
    def listen(self) -> Listener:
        """
        事件监听

        :return:
        """
        return self.__listener

    def close(self):
        """
        关闭上下文

        :return:
        """
        self._browser_driver.cdp.target.close_target(target_id=self.context_id)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
