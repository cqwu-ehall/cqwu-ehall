import datetime
from typing import Tuple

from pydantic import BaseModel


class ExamType:
    supplementation: str
    """ 开学补缓考 """
    graduate: str
    """ 毕业年级考试 """
    scattered: str
    """ 分散考试 """
    concentration: str
    """ 集中考试 """

    def __init__(
        self,
        supplementation: str = "",
        graduate: str = "",
        scattered: str = "",
        concentration: str = "",
    ):
        self.supplementation = supplementation
        self.graduate = graduate
        self.scattered = scattered
        self.concentration = concentration


class AiExam(BaseModel):
    name: str
    """ 课程名称 """
    credit: float
    """ 学分 """
    time: str
    """ 考试时间 """
    position: str
    """ 考试地点 """
    seat: str
    """ 座位号 """
    exam_round: str
    """ 考试轮次 """

    @property
    def name_no_id(self) -> str:
        """获取课程名称(去除课程编号)"""
        return self.name.split("]")[-1]

    @property
    def days_left(self) -> int:
        """获取距离考试的天数"""
        return (self.get_time()[0] - datetime.datetime.now()).days

    def get_time(self) -> Tuple[datetime.datetime, datetime.datetime]:
        """获取格式化后的考试时间"""
        # 2023-06-25(18周 星期日)09:00-11:00
        day = datetime.datetime.strptime(self.time.split("(")[0], "%Y-%m-%d")
        start_time = datetime.datetime.strptime(
            self.time.split(")")[1].split("-")[0], "%H:%M"
        )
        start_time = datetime.datetime(
            day.year, day.month, day.day, start_time.hour, start_time.minute
        )
        end_time = datetime.datetime.strptime(
            self.time.split(")")[1].split("-")[1], "%H:%M"
        )
        end_time = datetime.datetime(
            day.year, day.month, day.day, end_time.hour, end_time.minute
        )
        return start_time, end_time
