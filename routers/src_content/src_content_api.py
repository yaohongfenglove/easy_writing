import datetime

from items.response import GenericResponse
from logic import src_content_logic


def get_src_content_list(city_id: int, access_token: str, content_type_id=None,
                         publish_start_time=None, publish_end_time=None, page=1, page_size=10):
    """
    获取源内容列表
    :param city_id: 城市id
    :param access_token: 访问令牌
    :param content_type_id: 内容类型id
    :param page_size: 每页条数
    :param page: 页码
    :param publish_end_time: 内容发布的截止时间
    :param publish_start_time: 内容发布的起始时间
    :return:
    """
    src_content_list = src_content_logic.get_src_content_list(city_id=city_id)
    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "src_content_list": src_content_list,
            "count": len(src_content_list)
        }
    )


def get_src_content(content_id: int, access_token: str):
    """
    获取源内容详情
    :param content_id: 内容id
    :param access_token: 访问令牌
    :return:
    """
    src_content = src_content_logic.get_src_content(content_id=content_id)
    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "src_content": src_content
        }
    )
