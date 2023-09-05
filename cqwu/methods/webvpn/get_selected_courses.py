import re
from typing import Tuple, List, Union

from bs4 import BeautifulSoup

import cqwu
from cqwu.types.calendar import AiCourse


class GetSelectedCourses:
    async def get_selected_courses(
        self: "cqwu.Client",
        use_model: bool = False,
    ) -> Union[str, List[AiCourse]]:
        """ 获取选课结果 """
        jw_html = await self.login_jwmis()
        jw_host = self.get_web_vpn_host(jw_html.url)
        jw_url = f"{jw_host}/cqwljw/student/wsxk.zxjg.jsp"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Referer': f'{jw_host}/cqwljw/frame/homes.html',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41',
            'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        jw_html = await self.request.get(jw_url, headers=headers, timeout=60, follow_redirects=True)
        jw_html = jw_html.text.replace("""<script type="text/javascript" src="//clientvpn.cqwu.edu.cn/webvpn/bundle.debug.js" charset="utf-8"></script>""", "")
        return (
            parse_courses(jw_html)
            if use_model
            else jw_html.replace("<title></title>", '<meta charset="UTF-8">')
        )


def format_text(text: str) -> str:
    return text.replace("\n", "").replace("\t", "").replace("\r", "").strip()


def parse_courses(jw_html: str) -> List[AiCourse]:
    courses = []
    courses_keys = []
    soup = BeautifulSoup(jw_html, "lxml")
    trs = soup.find_all("tbody")[2].find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        name = format_text(tds[1].get_text()).split("]")[1]
        teacher = format_text(tds[4].get_text())
        calendars = str(tds[12]).replace("\u2002", "").split("<br/>")
        for calendar in calendars:
            text = (BeautifulSoup(calendar, "lxml")).text.strip()
            try:
                position, weeks, day, start_num, sections = parse_weeks_and_sections(text)
            except Exception:
                continue
            item = AiCourse(
                name=name,
                teacher=teacher,
                position=position,
                weeks=weeks,
                day=day,
                start_num=start_num,
                sections=sections,
            )
            if item.key not in courses_keys:
                courses_keys.append(item.key)
                courses.append(item)
    return courses


def parse_weeks_and_sections(text: str) -> Tuple[str, List[int], int, int, int]:
    # text: [1-3,5-17]周二[3-4节]格致-C305
    position, weeks_list, day, start_num, sections = "", [], 0, 0, 0
    weeks, days = text.split("周")
    position = days.split("]")[1]
    for week in re.findall(r"\d+-\d+", weeks):
        for i in range(int(week.split("-")[0]), int(week.split("-")[1]) + 1):
            weeks_list.append(i)
    day = "一二三四五六日".index(days[0]) + 1
    starts = re.findall(r"\d+-\d+", days)
    start_num = int(starts[0].split("-")[0])
    sections = int(starts[0].split("-")[1]) - start_num + 1
    return position, weeks_list, day, start_num, sections
