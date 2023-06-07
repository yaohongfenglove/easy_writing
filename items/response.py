
from typing import Generic, TypeVar

from pydantic.generics import GenericModel
from starlette import status


T = TypeVar('T')  # 泛型类型 T


class GenericResponse(GenericModel, Generic[T]):
    """ 通用响应格式 """
    code: int = status.HTTP_200_OK
    msg: str = "success"
    sub_code: int = 0
    sub_msg: str = ""
    now: int  # 时间戳：int(datetime.datetime.now().timestamp())
    data: T
