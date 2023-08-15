from typing import Optional, List

import cqwu
from cqwu.errors.auth import CookieError
from cqwu.types import PayProjectDetail


class GetPayProjectDetail:
    async def get_pay_project_detail(
        self: "cqwu.Client",
        project_id: str,
    ) -> List[Optional[PayProjectDetail]]:
        """
        获取缴费项目详情

        Returns:
            List[Optional[PayProjectDetail]]: 缴费项目详情列表
        """
        if not self._pay_x_token:
            await self._oauth_pay()
        url = (f"https://pay.cqwu.edu.cn/api/pay/web/tuitionAndDorm/getTuitionAndDormList/"
               f"{self.username}/{project_id}")
        html = await self.request.get(url, headers=self.pay_headers)
        if html.status_code != 200:
            raise CookieError()
        data = html.json().get("data", [])
        if not data:
            return []
        return [PayProjectDetail(**i) for i in data]
