"""
   依赖项
"""
from fastapi import Header
from jose import jwt
from starlette import status

from conf.config import config
from db.redis_db import redis_pool
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


def check_access_token(access_token: str = Header()):
    """
    校验令牌是否有效
    :param access_token: 访问令牌
    """
    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'],
                         algorithms=[config['access_token']['ALGORITHM']])
    phone = payload.get("phone")

    redis_conn = redis_pool.get_conn()
    access_token_key = f'access_token:{phone}'
    access_token_in_redis = redis_conn.get(access_token_key)

    if access_token_in_redis == access_token:
        return access_token
    else:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=StatusCodeEnum.ACCESS_TOKEN_HAS_EXPIRED.code,
            msg=StatusCodeEnum.ACCESS_TOKEN_HAS_EXPIRED.errmsg
        )
