from enum import Enum


class ScoreSearchType(str, Enum):
    """成绩查询类型"""

    All = "1"
    """入学以来"""
    XUENIAN = "2"
    """学年"""
    XUEQI = "3"
    """学期"""
