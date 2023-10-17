from typing import List

from pydantic import BaseModel


class ScoreDetailInfo(BaseModel):
    college: str = ""
    """院(系)/部"""
    major: str = ""
    """专业"""
    level: str = ""
    """培养层次"""
    class_name: str = ""
    """行政班级"""
    student_id: str = ""
    """学号"""
    student_name: str = ""
    """姓名"""
    date: str = ""
    """打印时间"""


class ScoreDetailCourse(BaseModel):
    id: int = 0
    """序号"""
    name: str = ""
    """课程/环节"""
    credit: float = 0.0
    """学分"""
    period: int = 0
    """总学时"""
    type: str = ""
    """类别"""
    nature: str = ""
    """修读性质"""
    exam_method: str = ""
    """考核方式"""
    score: float = 0.0
    """成绩"""
    score_point: float = 0.0
    """获得学分"""
    grade_point: float = 0.0
    """绩点"""
    gp: float = 0.0
    """学分绩点"""
    remark: str = ""
    """备注"""


class ScoreDetailTotal(BaseModel):
    num: int = 0
    """修读课程环节数"""
    credit: float = 0.0
    """学分"""
    get_credit: float = 0.0
    """获得学分"""
    grade_point: float = 0.0
    """获得绩点"""
    gp: float = 0.0
    """获得学分绩点"""
    gpa: float = 0.0
    """平均学分绩点"""
    score_avg: float = 0.0
    """平均成绩"""
    weighted_grade_avg: float = 0.0
    """加权平均成绩"""


class ScoreDetail(BaseModel):
    info: ScoreDetailInfo
    """基本信息"""
    courses: List[ScoreDetailCourse]
    """课程信息"""
    total: ScoreDetailTotal
    """总计"""
