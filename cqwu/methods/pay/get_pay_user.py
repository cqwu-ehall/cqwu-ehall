from typing import Optional, List

import cqwu
from cqwu.errors.auth import CookieError
from cqwu.types import PayUser


class GetPayUser:
    async def get_pay_user(
        self: "cqwu.Client",
    ) -> Optional[PayUser]:
        """
        获取缴费用户信息

        Returns:
            List[Optional[PayUser]]: 缴费用户信息列表
        """
        if not self._pay_x_token:
            await self._oauth_pay()
        url = f"https://pay.cqwu.edu.cn/api/pay/queryUserInfo/{self._pay_x_token}"
        html = await self.request.get(url, headers=self.pay_headers)
        if html.status_code != 200:
            raise CookieError()
        data = html.json().get("data")
        if not data:
            return None
        return PayUser(**data)
