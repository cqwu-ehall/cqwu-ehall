from typing import List, Dict

from pydantic import BaseModel


class AiCourse(BaseModel):
    name: str  # 课程名称
    position: str  # 上课地点
    teacher: str  # 上课老师
    weeks: List[int]  # 上课周数
    day: int  # 星期
    start_num: int  # 开始节数
    sections: int  # 连上节数

    @property
    def key(self):
        return f"{','.join([str(i) for i in self.weeks])}_{self.day}_{self.start_num}"

    @property
    def second_key(self):
        return f"{self.day}_{self.sections}"

    @property
    def ai(self) -> Dict:
        return {
            "name": self.name,
            "position": self.position,
            "teacher": self.teacher,
            "weeks": ",".join(list(map(str, self.weeks))),
            "day": self.day,
            "style": "",
            "sections": ",".join(
                list(
                    map(
                        str, list(range(self.start_num, self.start_num + self.sections))
                    )
                )
            ),
        }
