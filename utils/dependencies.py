"""
   依赖项
"""
from fastapi import Header
from starlette import status

from utils.constants import StatusCodeEnum
from utils.exceptions import CustomHTTPException


def verify_access_token(access_token: str = Header()):
    """
    校验访问令牌
    :param access_token: 访问令牌
    :return:
    """
    if access_token != "xxx":
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=StatusCodeEnum.ACCESS_TOKEN_HAS_EXPIRED.code,
            msg=StatusCodeEnum.ACCESS_TOKEN_HAS_EXPIRED.errmsg,
        )
