import time

from datetime import datetime
from urllib.parse import urlencode, urlparse
from lxml import etree

import cqwu
from cqwu.errors.auth import UsernameOrPasswordError
from cqwu.utils.auth import encode_password


class LoginWithPassword:
    async def login_with_password(
            self: "cqwu.Client",
    ):
        """
        使用学号加密码登录
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 Safari/537.36',
            "Referer": f"{self.auth_host}/authserver/login",
            "Origin": self.auth_host,
            "Host": urlparse(self.auth_host).netloc
        }
        session = self.request(headers=self.headers, follow_redirects=True)
        html = await session.get(f"{self.host}/authserver/login")
        self.cookies.update(html.cookies)
        tree = etree.HTML(html.text)
        pwd_default_encrypt_salt = tree.xpath('//*[@id="pwdDefaultEncryptSalt"]/@value')[0]
        form_data = {
            'username': str(self.username),
            'password': encode_password(self.password, pwd_default_encrypt_salt),
            'lt': tree.xpath('//*[@id="casLoginForm"]/input[1]/@value')[0],
            'dllt': tree.xpath('//*[@id="casLoginForm"]/input[2]/@value')[0],
            'execution': tree.xpath('//*[@id="casLoginForm"]/input[3]/@value')[0],
            '_eventId': tree.xpath('//*[@id="casLoginForm"]/input[4]/@value')[0],
            'rmShown': tree.xpath('//*[@id="casLoginForm"]/input[5]/@value')[0]
        }

        # 是否需要验证码
        params = {
            "username": self.username,
            "pwdEncrypt2": "pwdEncryptSalt",
            "_": str(round(time.time() * 1000))
        }

        need_captcha_url = f"{self.auth_host}/authserver/needCaptcha.html?{urlencode(params)}"
        async with self.request() as client:
            html = await client.get(need_captcha_url, follow_redirects=False)
        if html.text == 'true':
            ts = round(datetime.now().microsecond / 1000)  # get milliseconds
            captcha_url = f"{self.auth_host}/authserver/captcha.html?" + urlencode({"ts": ts})
            async with self.request() as client:
                res = await client.get(captcha_url, follow_redirects=False)
            with open("captcha.jpg", mode="wb") as f:
                f.write(res.content)
            print("验证码已保存在当前目录下的 captcha.jpg 文件中。")
            code = self.get_input("验证码")
            form_data['captchaResponse'] = code

        # 登录
        async with self.request(headers=headers, cookies=self.cookies) as client:
            html = await client.post(f"{self.auth_host}/authserver/login", data=form_data, follow_redirects=False)
        if 'CASTGC' not in html.cookies.keys():
            raise UsernameOrPasswordError
        self.cookies.update(html.cookies)
        self.sub_cookies.update(html.cookies)
        self.me = await self.get_me()  # noqa
