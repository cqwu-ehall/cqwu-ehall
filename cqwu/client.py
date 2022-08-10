import asyncio
from typing import Coroutine, Optional
from httpx import AsyncClient, Cookies
from urllib.parse import urlparse

from cqwu.methods import Methods
from cqwu.types import User


class Client(Methods):
    """CQWU main client."""

    def __init__(
        self,
        username: int = None,
        password: str = None,
        cookie: str = None,
        cookie_file_path: str = "cookie.txt",
        client_vpn: bool = False,
    ):
        self.username = username
        self.password = password
        self.cookie = cookie
        self.cookie_file_path = cookie_file_path
        if client_vpn:
            self.host = "https://clientvpn.cqwu.edu.cn:10443/http/webvpn507e990968de07079b0f10d16c49bdb1cb8d3ca3a4d14f557999e92cbdf19fcd"
            self.auth_host = self.host
        else:
            self.host = "http://ehall.cqwu.edu.cn"
            self.auth_host = "http://authserver.cqwu.edu.cn"

        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Host": urlparse(self.host).netloc,
            "Origin": self.host,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        }
        self.cookies = Cookies()
        self.sub_cookies = Cookies()
        self.init_sub_web = []
        self.request = AsyncClient
        self.loop = asyncio.get_event_loop()
        self.me: Optional[User] = None

    @staticmethod
    def get_input(word: str = "", is_int: bool = False):
        while True:
            value = input(f"请输入{word}：")
            if not value:
                continue
            if is_int:
                try:
                    value = int(value)
                except ValueError:
                    continue
            confirm = (input(f'确认是 "{value}" 吗？(y/N): ')).lower()
            if confirm == "y":
                break
        return value

    def sync(self, coroutine: Coroutine):
        """
        同步执行异步函数

        Args:
            coroutine (Coroutine): 异步函数

        Returns:
            该异步函数的返回值
        """
        return self.loop.run_until_complete(coroutine)
