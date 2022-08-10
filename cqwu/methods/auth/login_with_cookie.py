import cqwu
from cqwu.errors.auth import CookieError


class LoginWithCookie:
    async def login_with_cookie(
        self: "cqwu.Client",
    ):
        """
        使用 cookie 登录
        """
        if not self.cookie:
            raise CookieError()

        try:
            data = self.cookie.split(";")
            for cookie in data:
                if not cookie:
                    continue
                key, value = cookie.split("=")
                self.cookies.set(key, value)
                self.sub_cookies.set(key, value)
            self.me = await self.get_me()  # noqa
        except:
            raise CookieError()
