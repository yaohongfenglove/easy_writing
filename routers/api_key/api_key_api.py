import datetime
from typing import Union

from starlette import status

from items.response import GenericResponse
from logic.api_key import api_key_logic
from utils.constants import StatusCodeEnum
from utils.exceptions import CustomHTTPException, NoApiKeysAvailableError


def get_api_key(access_token: Union[None, str] = None):
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
            "access_key": api_key
        }
    )
