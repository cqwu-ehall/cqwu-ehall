from typing import Dict

import cqwu

from .get_pay_project_detail import GetPayProjectDetail
from .get_pay_projects import GetPayProjects
from .get_pay_user import GetPayUser


class Pay(
    GetPayProjectDetail,
    GetPayProjects,
    GetPayUser,
):
    async def _oauth_pay(
        self: "cqwu.Client",
    ):
        url = f"https://pay.cqwu.edu.cn/api/pay/web/dlyscas/casLogin/{self.username}/2"
        html = await self.request.get(url, follow_redirects=False)
        if html.status_code == 302:
            location = html.headers["location"]
            params = {
                i.split("=")[0]: i.split("=")[1]
                for i in location.split("?")[1].split("&")
            }
            self._pay_x_token = params["token"]

    @property
    def pay_headers(self) -> Dict[str, str]:
        return {
            "X-Token": self._pay_x_token,
        }
