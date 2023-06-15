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
    user_extra_info = user_service.get_user_extra_info(user_id=user_id)
    api_key_list = user_extra_info.get("api_key_list")
    if not api_key_list:
        raise NoApiKeysAvailableError("无可用的api_key了")
    api_key = api_key_list[0].get("api_key")
    api_base = api_key_list[0].get("api_base")

    res_key = {
        "api_key": api_key,
        "api_base": api_base
    }

    return res_key


def main():

    res = get_api_key("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI"
                      "6IjE1OTE1MzExNDUzIiwiZXhwIjoxNjk4MzExMjMxfQ.H_WEhTvEB8GVtbaa8UGPuorV"
                      "z_Gr98bqdzxal28pJYc")
    print(f"{res}")


if __name__ == '__main__':
    main()
