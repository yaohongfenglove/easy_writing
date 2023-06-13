# coding=utf-8

import datetime

from items.aigc_content import AigcContentRequest
from items.response import GenericResponse


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

    # task_id = task_logic.create_task(**task.dict())

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={}
    )
