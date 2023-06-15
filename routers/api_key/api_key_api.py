import datetime

from starlette import status

from items.response import GenericResponse
from logic.api_key import api_key_logic
from utils.constants import StatusCodeEnum
from utils.exceptions import CustomHTTPException, NoApiKeysAvailableError


def get_api_key(access_token: str):
    """
    获取api_key
    :param access_token: 访问令牌
    :return:
    """
    try:
        api_key = api_key_logic.get_api_key(access_token=access_token)
    except NoApiKeysAvailableError:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code=StatusCodeEnum.NO_API_KEYS_AVAILABLE_ERR.code,
            msg=StatusCodeEnum.NO_API_KEYS_AVAILABLE_ERR.errmsg,
        )

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "result": {
                "api_key": api_key.get("api_key"),
                "api_base": api_key.get("api_base"),
                "expire_time": api_key.get("expire_time"),
            }
        }
    )
