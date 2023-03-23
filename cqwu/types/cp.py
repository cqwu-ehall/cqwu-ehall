from pydantic import BaseModel


class CP(BaseModel):
    id: int
    name: str
    xue_nian: str
    xue_qi: str
    score: float
    class_rank: int
    class_member: int
    grade_rank: int
    grade_member: int
    dysz: float
    zysz: float
    cxsz: float
    wtsz: float
    zysz_class_rank: int
    zysz_grade_rank: int
