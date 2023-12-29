from json import JSONDecodeError

import cqwu
from cqwu.types.exam import ExamType


class GetExamCalendarAction:
    async def get_exam_calendar_action(
        self: "cqwu.Client",
        xue_nian: int = None,
        xue_qi: int = None,
    ) -> ExamType:
        """获取考试安排可用类型"""
        xue_nian = xue_nian or self.xue_nian
        xue_qi = xue_qi or self.xue_qi
        jw_html = await self.login_jwmis()
        jw_host = self.get_web_vpn_host(jw_html.url, https=True)
        jw_url = f"{jw_host}/cqwljw/frame/droplist/getDropLists.action"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,zh-Hans;q=0.8,und;q=0.7,en;q=0.6,zh-Hant;q=0.5,ja;q=0.4",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Pragma": "no-cache",
            "Referer": f"{jw_host}/cqwljw/student/ksap.ksapb.html?menucode=S20403",
            "Sec-Fetch-Dest": "iframe",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Chromium";v="112", "Not:A-Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
        }
        data = {
            "comboBoxName": "Ms_KSSW_FBKSLC",
            "paramValue": f"xtdm=jw&zxtdm=7&kgmc=kw_fbksap&xnxq={xue_nian}{xue_qi}",
            "isYXB": "0",
            "isCDDW": "0",
            "isXQ": "0",
            "isDJKSLB": "0",
            "isZY": "0",
        }
        jw_html = await self.request.post(
            jw_url, data=data, headers=headers, timeout=60, follow_redirects=True
        )
        data = ExamType()
        try:
            jw_data = jw_html.json()
            for i in jw_data:
                if "开学补缓考" in i["name"]:
                    data.supplementation = i["code"]
                elif "毕业年级考试" in i["name"]:
                    data.graduate = i["code"]
                elif "分散考试" in i["name"]:
                    data.scattered = i["code"]
                elif "集中考试" in i["name"]:
                    data.concentration = i["code"]
        except JSONDecodeError:
            pass
        return data
