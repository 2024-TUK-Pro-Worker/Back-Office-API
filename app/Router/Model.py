from typing import Union, List
from pydantic import BaseModel


class RS_common(BaseModel):
    result: str = 'success'
    data: Union[List[dict], dict, None]


class RS_fail(BaseModel):
    result: str = 'fail'
    message: str
