from enum import Enum


class ExamRound(str, Enum):
    Supplementation = "1"
    """ 开学补缓考 """
    Scattered = "2"
    """ 分散考试 """
    Concentration = "3"
    """ 集中考试 """


class ScoreSearchType(str, Enum):
    """ 成绩查询类型 """
    All = "1"
    """入学以来"""
    XUENIAN = "2"
    """学年"""
    XUEQI = "3"
    """学期"""
