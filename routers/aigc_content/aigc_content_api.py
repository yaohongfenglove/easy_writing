# coding=utf-8

import datetime

from items.aigc_content import AigcContentRequest
from items.response import GenericResponse
from logic.aigc_content import aigc_content_logic


def update_aigc_content(
        content_id: int,
        aigc_content: AigcContentRequest
):
    """
    更新内容信息
    :param content_id: 内容id
    :param aigc_content: AIGC内容对象
    :return: 任务id
    """

    aigc_content_logic.update_content_info(content_id=content_id, **aigc_content.dict())

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
