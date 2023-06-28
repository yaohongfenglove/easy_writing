# coding=utf-8

import datetime

from fastapi import Header
from starlette import status as starlette_status

from items.aigc_content import AigcContentRequest
from items.response import GenericResponse
from logic.aigc_content import aigc_content_logic
from utils.constants import StatusCodeEnum
from utils.exceptions import ApiKeyUpdateError, CustomHTTPException


def update_aigc_content(
        content_id: int,
        aigc_content: AigcContentRequest,
        access_token: str = Header()
):
    """
    更新内容信息
    :param access_token:访问令牌
    :param content_id: 内容id
    :param aigc_content: AIGC内容对象
    :return: 任务id
    """

    try:
        aigc_content_logic.update_content_info(content_id=content_id, aigc_content=aigc_content, access_token=access_token)
    except ApiKeyUpdateError:
        raise CustomHTTPException(
            status_code=starlette_status.HTTP_400_BAD_REQUEST,
            code=StatusCodeEnum.API_KEY_UPDATE_ERROR.code,
            msg=StatusCodeEnum.API_KEY_UPDATE_ERROR.errmsg,
        )

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={}
    )


def get_aigc_content(content_id: int):
    """
    获取AIGC内容详情
    :param content_id:
    :return:
    """
    src_content = aigc_content_logic.get_src_content(content_id=content_id)
    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "result": src_content
        }
    )
