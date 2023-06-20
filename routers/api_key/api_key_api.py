import datetime

from fastapi import Header
from jose import jwt

from conf.config import config
from items.response import GenericResponse
from logic.api_key import api_key_logic


def get_api_key(access_token: str = Header()):
    """
    获取api_key
    :param: access_token: 访问令牌
    :return:
    """
    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'],
                         algorithms=[config['access_token']['ALGORITHM']])
    user_id = payload.get("user_id")
    api_key = api_key_logic.get_api_key(user_id=user_id)

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "result": {
                "api_key": api_key.get("api_key"),
                "api_base": api_key.get("api_base"),
                "expire_time": api_key.get("expire_time"),
                "token_left": api_key.get("token_left")
            }
        }
    )
