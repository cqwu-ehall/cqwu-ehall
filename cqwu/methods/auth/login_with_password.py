from lxml import etree

import cqwu
from cqwu.errors.auth import UsernameOrPasswordError
from cqwu.utils.auth import encode_password


class LoginWithPassword:
    async def login_with_password(
        self: "cqwu.Client",
        captcha_code: str = None,
        show_qrcode: bool = True,
    ):
        """
        使用学号加密码登录
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
        }
        html = await self.request.get(f"{self.auth_host}/authserver/login", headers=headers, follow_redirects=True)
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
        if not captcha_code:
            captcha_code = await self.check_captcha(show_qrcode=show_qrcode)
            if captcha_code:
                form_data['captchaResponse'] = captcha_code
        # 登录
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Origin': self.auth_host,
            'Referer': f'{self.auth_host}/authserver/login',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63',
        }
        html = await self.request.post(
            f"{self.auth_host}/authserver/login",
            headers=headers,
            data=form_data,
            follow_redirects=False,
        )
        if 'CASTGC' not in html.cookies.keys():
            raise UsernameOrPasswordError
        self.cookies.update(html.cookies)
        self.me = await self.get_me()  # noqa
