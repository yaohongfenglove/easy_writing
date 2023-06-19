import datetime
from typing import Union

from items.response import GenericResponse
from logic import src_content_logic


def get_src_content_list(
        city_id: int,
        page: int = 1,
        page_size: int = 20,
        content_type_id: Union[None, int] = None,
        publish_start_time: Union[None, str] = None,
        publish_end_time: Union[None, str] = None
):
    """
    获取源内容列表
    :param page_size: 每页多少条数据
    :param page: 页码
    :param city_id: 城市id
    :param content_type_id: 内容类型id
    :param publish_end_time: 内容发布的截止时间
    :param publish_start_time: 内容发布的起始时间
    :return:
    """
    src_content_list = src_content_logic.get_src_content_list(
        city_id=city_id,
        page=page,
        page_size=page_size,
        content_type_id=content_type_id,
        publish_start_time=publish_start_time,
        publish_end_time=publish_end_time
    )
    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "list": src_content_list,
            "count": len(src_content_list)
        }
    )


def get_src_content(content_id: int):
    """
    获取源内容详情
    :param content_id: 内容id
    :return:
    """
    src_content = src_content_logic.get_src_content(content_id=content_id)
    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "result": src_content
        }
    )
