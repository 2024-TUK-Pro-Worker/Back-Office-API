# Python 모듈
from typing import Union, List
from pydantic import BaseModel

# 소스 파일 선언


class RS_common(BaseModel):
    result: str = 'success'
    data: Union[List[dict], dict, None]


class RS_fail(BaseModel):
    result: str = 'fail'
    message: str
