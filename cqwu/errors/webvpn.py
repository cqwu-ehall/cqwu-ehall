from .base import CQWUEhallError


class CQWUWebVPNError(CQWUEhallError):
    pass


class NoExamData(CQWUWebVPNError):
    """没有检索到对应的考试记录"""


class NoScoreDetailData(CQWUWebVPNError):
    """没有检索到对应的成绩明细记录"""
