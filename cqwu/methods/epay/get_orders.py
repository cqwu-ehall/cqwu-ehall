from typing import List

import cqwu
from cqwu.types.order import Order


class GetOrders:
    async def get_orders(
        self: "cqwu.Client",
        page: int = 1,
        page_size: int = 10,
        search: str = ""
    ) -> List[Order]:
        """
        获取历史订单

        :param page: 页码
        :param page_size: 每页数量
        :param search: 搜索关键字

        :return: 订单列表
        """
        url = "http://pay.cqwu.edu.cn/queryOrderList"
        params = {
            "orderno": search,
            "page": page,
            "pagesize": page_size,
        }
        if "pay.cqwu.edu.cn" not in self.init_sub_web:
            await self.oauth(
                "http://authserver.cqwu.edu.cn/authserver/login?service="
                "http%3A%2F%2Fpay.cqwu.edu.cn%2FsignAuthentication%3Furl%3DopenPortal")
        async with self.request(cookies=self.sub_cookies, follow_redirects=True) as client:
            html = await client.get(url, params=params)
            try:
                data = html.json()["payOrderList"]
            except KeyError:
                return []
        return [Order(**order) for order in data]
