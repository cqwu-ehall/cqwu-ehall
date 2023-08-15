from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class PayProject(BaseModel):
    id: str
    createDate: datetime
    createBy: str
    updateDate: datetime
    updateBy: str
    projectType: str
    projectCode: str
    projectName: str
    """ 项目名称 """
    imgUrl: Optional[str]


class PayProjectDetail(BaseModel):
    id: Optional[str]
    xh: Optional[int]
    """ 学号 """
    executespanname: Optional[str]
    financingname: Optional[str]
    """ 名称 """
    taxname: Optional[str]
    """ 税务名称 """
    ysje: Optional[float]
    """ 应收金额 """
    sfje: Optional[float]
    """ 已收金额 """
    qfje: Optional[float]
    """ 欠费金额 """
    jmje: Optional[float]
    """ 减免金额 """
    tfje: Optional[float]
    """ 退费金额 """

    @validator("ysje", "sfje", "qfje", "jmje", "tfje", pre=True)
    def _float(cls, v):
        if v == "":
            return 0.0
        return float(v) / 100.0


class PayUser(BaseModel):
    id: str
    createDate: datetime
    createBy: str
    updateDate: datetime
    updateBy: str
    idserial: Optional[int]
    name: Optional[str]
    idNum: Optional[int]
    """ 身份证号 """
    phone: Optional[int]
    """ 手机号 """
