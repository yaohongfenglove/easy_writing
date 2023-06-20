import random
from typing import Dict

from jose import jwt
from starlette import status

from conf.config import config
from service.api_key_service import ApiKeyService
from service.user_service import UserService
from utils.constants import StatusCodeEnum
from utils.exceptions import NoApiKeysAvailableError, CustomHTTPException


def get_api_key1(access_token: str) -> Dict:
    """
    获取api_key
    :param access_token: 访问令牌
    :return:
    """
    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'],
                         algorithms=[config['access_token']['ALGORITHM']])
    user_id = payload.get("user_id")

    user_service = UserService()
    api_key_list = user_service.get_user_api_key_list(user_id=user_id)

    if not api_key_list:
        raise NoApiKeysAvailableError("无可用的api_key了")

    api_key = api_key_list[0].get("api_key")
    api_base = api_key_list[0].get("api_base")
    expire_time = api_key_list[0].get("expire_time")

    res = {
        "api_key": api_key,
        "api_base": api_base,
        "expire_time": expire_time
    }

    return res


def get_api_key(user_id) -> Dict:
    """
    获取api_key
    :param: user_id: 用户id
    :return:
    """
    user_service = UserService()
    api_key_list = user_service.get_user_token_left(user_id=user_id)
    if api_key_list <= 0:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code=StatusCodeEnum.NO_API_KEYS_AVAILABLE_ERR.code,
            msg=StatusCodeEnum.NO_API_KEYS_AVAILABLE_ERR.errmsg,
        )

    apikey_service = ApiKeyService()
    access_key_list = apikey_service.get_api_key()
    access_key = random.sample(access_key_list, 1)

    api_key = access_key[0].get("api_key")
    api_base = access_key[0].get("api_base")
    expire_time = access_key[0].get("expire_time")
    token_left = access_key[0].get("token_left")

    res = {
        "api_key": api_key,
        "api_base": api_base,
        "expire_time": expire_time,
        "token_left": token_left
    }

    return res


def main():
    pass


if __name__ == '__main__':
    main()
