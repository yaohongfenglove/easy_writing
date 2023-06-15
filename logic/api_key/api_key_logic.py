from typing import Dict

from jose import jwt

from conf.config import config
from service.user_service import UserService
from utils.exceptions import NoApiKeysAvailableError


def get_api_key(access_token: str) -> Dict:
    """
    获取api_key
    :param access_token: 访问令牌
    :return:
    """
    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'], algorithms=[config['access_token']['ALGORITHM']])
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


def main():
    pass


if __name__ == '__main__':
    main()
