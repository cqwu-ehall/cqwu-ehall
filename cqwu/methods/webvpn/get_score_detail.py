from typing import Union, List

from bs4 import BeautifulSoup, Tag

import cqwu
from cqwu.enums import ScoreSearchType
from cqwu.errors import NoScoreDetailData
from cqwu.types import ScoreDetail, ScoreDetailInfo, ScoreDetailCourse, ScoreDetailTotal


class GetScoreDetail:
    async def get_score_detail(
        self: "cqwu.Client",
        search_type: Union[str, ScoreSearchType] = ScoreSearchType.XUEQI,
        xue_nian: int = None,
        xue_qi: int = None,
        origin: bool = False,
        use_model: bool = False,
    ) -> Union[str, ScoreDetail]:
        """获取学业成绩"""
        xue_nian = xue_nian or self.xue_nian
        xue_qi = xue_qi or self.xue_qi
        search_type = ScoreSearchType(search_type)
        jw_html = await self.login_jwmis()
        jw_host = self.get_web_vpn_host(jw_html.url, https=True)
        jw_url = f"{jw_host}/cqwljw/student/xscj.stuckcj_data.jsp"
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
            "sjxz": f"sjxz{search_type.value}",
            "ysyx": "yscj" if origin else "yxcj",
            "zx": "1",
            "fx": "1",
            "btnExport": "%B5%BC%B3%F6",
            "rxnj": str(xue_nian),
            "xn": str(xue_nian),
            "xn1": str(xue_nian + 1),
            "xq": str(xue_qi),
            "ysyxS": "on",
            "sjxzS": "on",
            "zxC": "on",
            "fxC": "on",
            "xsjd": "1",
        }
        jw_html = await self.request.post(
            jw_url, data=data, headers=headers, timeout=60, follow_redirects=True
        )
        if "没有检索到记录!" in jw_html.text:
            raise NoScoreDetailData("没有检索到记录!")
        jw_html = jw_html.text.replace(
            """<script type="text/javascript" src="//clientvpn.cqwu.edu.cn/webvpn/bundle.debug.js" charset="utf-8"></script>""",
            "",
        )
        jw_html = jw_html.replace(
            """<script language='javascript' type='text/javascript' src='../js/Print.js'></script>""",
            "",
        )
        jw_html = jw_html.replace("charset=GBK", "charset=UTF-8")
        if not use_model:
            return jw_html
        return parse_html(jw_html, origin)


def parse_info(tag: Tag) -> ScoreDetailInfo:
    divs = tag.find_all("div")

    def get_text(_tag) -> str:
        return ("：".join(_tag.text.split("：")[1:])).strip()

    return ScoreDetailInfo(
        college=get_text(divs[0]),
        major=get_text(divs[1]),
        level=get_text(divs[2]),
        class_name=get_text(divs[3]),
        student_id=get_text(divs[4]),
        student_name=get_text(divs[5]),
        date=get_text(divs[6]),
    )


def parse_course(tag: Tag) -> List[ScoreDetailCourse]:
    trs = tag.find_all("tr")
    courses = []
    for tr in trs:
        tds = tr.find_all("td")
        course = ScoreDetailCourse(
            id=tds[0].text,
            name=tds[1].text,
            credit=tds[2].text,
            period=tds[3].text,
            type=tds[4].text,
            nature=tds[5].text,
            exam_method=tds[6].text,
            score=tds[7].text,
            score_point=tds[8].text,
            grade_point=tds[9].text,
            gp=tds[10].text,
            remark=tds[11].text,
        )
        courses.append(course)
    return courses


def parse_course_origin(tag: Tag) -> List[ScoreDetailCourse]:
    trs = tag.find_all("tr")
    courses = []
    for tr in trs:
        tds = tr.find_all("td")
        course = ScoreDetailCourse(
            id=tds[0].text,
            name=tds[1].text,
            credit=tds[2].text,
            period=tds[3].text,
            type=tds[4].text,
            nature=tds[5].text,
            exam_method=tds[6].text,
            score=tds[8].text,
            remark=tds[9].text,
        )
        courses.append(course)
    return courses


def parse_total(tag: Tag) -> ScoreDetailTotal:
    tr = tag.find_all("tr")[-1]
    tds = tr.find_all("td")
    return ScoreDetailTotal(
        num=tds[1].text,
        credit=tds[2].text,
        get_credit=tds[3].text,
        grade_point=tds[4].text,
        gp=tds[5].text,
        gpa=tds[6].text,
        score_avg=tds[7].text,
        weighted_grade_avg=tds[8].text,
    )


def parse_html(html: str, origin: bool) -> ScoreDetail:
    soup = BeautifulSoup(html, "lxml")
    group_div = soup.find("div", {"group": "group"})
    info = parse_info(group_div)
    tbody_s = soup.find_all("tbody")
    courses = []
    total = None
    if origin:
        courses += parse_course_origin(tbody_s[0])
    else:
        for tbody in tbody_s[:-1]:
            courses += parse_course(tbody)
        total = parse_total(tbody_s[-1])
    return ScoreDetail(info=info, courses=courses, total=total)
