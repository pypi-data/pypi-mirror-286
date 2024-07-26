from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Person(BaseModel):
    personid: int
    plastname: str
    pfirstname: str
    psurname: str
    ppsex: int
    isuser: bool
    pilogin: str
    pipassword: str
    caid: str
    caidname: str
    rspostid: str
    rspostidname: str
    personemail: str
    pstatus: int
    pextcode: str


class Measure(BaseModel):
    meid: int
    mename: str
    medescription: str
    metype: str
    mecode: str
    mestatus: str
    mestartdate: Optional[datetime] = None
    meenddate: Optional[datetime] = None
    meeduform: Optional[int] = None
    mecontenttype: Optional[int] = None
    testid: Optional[str] = None
    testidname: Optional[str] = None
    ugrid: Optional[int] = None
    ugridname: Optional[str] = None
    mepasses: Optional[int] = None
