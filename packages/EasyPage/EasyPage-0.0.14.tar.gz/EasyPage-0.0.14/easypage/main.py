import atexit
import shutil
from subprocess import Popen
from typing import List, Dict
from easypage.logger import logger
from easypage.utils import browser_utils
from easypage.options import BrowserOptions
from easypage.driver.page import PageDriver
from easypage import settings, operate, definition
from easypage.driver.browser import BrowserDriver, ContextDriver


class EasyPage:
    def __init__(
            self,
            opts: BrowserOptions = None,
            log_level: int = None,
            reuse: bool = False,
            reuse_close: bool = False
    ):
        """

        :param opts: 配置
        :param log_level: 日志等级（如：logging 模块的 logging.WARNING）
        :param reuse: 是否复用已经存在的浏览器（根据 opts 内的端口判断复用，无法复用则创建新端口）
        :param reuse_close: 复用浏览器时，是否在结束时关闭浏览器并清理资源（默认不关闭）
        """
        # 配置日志等级
        log_level = log_level or settings.LOGGER_LEVEL
        # TODO: 临时处理，为了通过 loguru，后续需要修改
        # if not settings.SYSTEM_TYPE.startswith("win"):
        logger.logger.setLevel(log_level)

        self._opts = opts or BrowserOptions()
        self._reuse = reuse
        self._reuse_close = reuse_close

        self._proc: "Popen" = None  # type: ignore
        self._start_browser()

        self._browser_driver_id = browser_utils.parse_driver_id(operate.browser(opts.address))[0]
        self._browser_driver = BrowserDriver(opts=self._opts, driver_id=self._browser_driver_id)

    @property
    def browser(self) -> "BrowserDriver":
        return self._browser_driver

    @property
    def page(self) -> "PageDriver":
        """
        默认页面

        :return:
        """
        default_page_id = BrowserDriver.CONTENT_PAGE_MAPS[self.browser.context_id][0]
        return BrowserDriver.PAGES[default_page_id]

    @property
    def pages(self) -> List["PageDriver"]:
        """
        获取所有的当前页面

        TODO 需要修改成实时的，面对高并发网站可能会失败

        :return:
        """
        return list(BrowserDriver.PAGES.values())

    @property
    def contexts(self) -> List["ContextDriver"]:
        """
        获取指定上下文

        TODO 需要修改成实时的，面对高并发网站可能会失败

        :return:
        """
        return list(BrowserDriver.CONTEXTS.values())

    def page_infos(self) -> dict:
        """
        获取所有页面

        :return:
        """
        status, infos = self.browser.cdp.target.get_targets()
        if not status:
            return {}

        result_infos = {
            "page": []
        }
        for info in infos["targetInfos"]:
            if info["type"] == "page":
                result_infos["page"].append({
                    "targetId": info['targetId'],
                    "contextId": info['browserContextId'],
                })

        return result_infos

    def new_context(self, proxy: definition.Proxy = None, **kwargs) -> "ContextDriver":
        """
        创建新上下文（类似于隐身模式）

        :param proxy:
        :param kwargs:
        :return:
        """
        return self._browser_driver.new_context(proxy=proxy, **kwargs)

    def _start_browser(self):
        """
        启动或连接浏览器

        :return:
        """
        # 复用的话检查是否有可以复用的浏览器
        if not self._opts.address:
            self._opts.set_address(ip=settings.BROWSER_START_IP, port=settings.BROWSER_START_PORT)

        if self._reuse:
            status = browser_utils.port_in_use(port=self._opts.port, ip=self._opts.ip)
            if not status:
                logger.debug("浏览器复用失败，当前地址无已打开的浏览器：{}，将获取随机端口启动！", self._opts.address)
            else:
                logger.debug("浏览器复用成功：{}", self._opts.address)
                if self._reuse_close:
                    atexit.register(self.close)
                return

        # 打开新的浏览器
        from easypage import operate
        self._proc = operate.new_browser(opts=self._opts)
        if not self._reuse:
            atexit.register(self.close)

        if self._reuse and self._reuse_close:
            atexit.register(self.close)

        # 等待浏览器打开
        operate.wait_connection(opts=self._opts)

    def close(self):
        """
        关闭浏览器，清理资源，如删除资源文件夹

        :return:
        """
        # cdp 发送关闭浏览器
        try:
            self._browser_driver.close()
        except:
            pass

        # 杀掉进程
        try:
            if self._proc and self._proc.poll() is None:
                self._proc.terminate()
                self._proc.wait()
        except:
            pass

        # 清空资源文件夹
        if self._opts.delete_user_data_dir_when_stop and self._opts.user_data_dir:
            shutil.rmtree(self._opts.user_data_dir, ignore_errors=True)
