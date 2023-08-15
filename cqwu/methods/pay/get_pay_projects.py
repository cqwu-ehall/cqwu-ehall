from typing import Optional, List

import cqwu
from cqwu.errors.auth import CookieError
from cqwu.types import PayProject


class GetPayProjects:
    async def get_pay_projects(
        self: "cqwu.Client",
    ) -> List[Optional[PayProject]]:
        """
        获取缴费项目

        Returns:
            List[Optional[PayProject]]: 缴费项目列表
        """
        if not self._pay_x_token:
            await self._oauth_pay()
        url = "https://pay.cqwu.edu.cn/api/pay/project/getAllProjectList"
        html = await self.request.get(url, headers=self.pay_headers)
        if html.status_code != 200:
            raise CookieError()
        data = html.json().get("data", [])
        if not data:
            return []
        return [PayProject(**i) for i in data]
