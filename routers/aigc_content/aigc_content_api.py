# coding=utf-8

import datetime

from items.aigc_content import AigcContentRequest
from items.response import GenericResponse
from logic import aigc_content_logic


def update_aigc_content(
        content_id: int,
        aigc_content: AigcContentRequest
):
    """
    创建任务
    :param content_id: 内容id
    :param aigc_content: AIGC内容对象
    :return: 任务id
    """

    aigc_content_logic.update_content_info(content_id=content_id, **aigc_content.dict())

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={}
    )
