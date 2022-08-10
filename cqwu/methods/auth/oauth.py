from urllib.parse import urlparse

import cqwu


class Oauth:
    async def oauth(
        self: "cqwu.Client",
        url: str,
        host: str = None,
    ):
        """
        使用 统一身份认证平台 登录子系统，并且保存 cookie
        """
        host = host or urlparse(url).hostname
        async with self.request(cookies=self.sub_cookies, follow_redirects=True) as client:
            html = await client.get(url)
            for history in html.history:
                self.sub_cookies.update(history.cookies)
                if host not in self.init_sub_web:
                    self.init_sub_web.append(host)
            return None if html.url.host != host else html
