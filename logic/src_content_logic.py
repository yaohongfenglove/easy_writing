from typing import List, Dict

from jose import jwt

from conf.config import config
from service.src_content_service import SrcContentService


def get_src_content_list(
        city_id: int,
        content_type_id: int,
        access_token: str,
        is_used: int,
        page: int,
        page_size: int,
        publish_start_time: str,
        publish_end_time: str
):
    """
    获取源内容列表
    :param city_id: 城市id
    :param access_token: 访问令牌
    :param is_used: 是否使用过
    :param content_type_id: 内容类型id
    :param page: 页码
    :param page_size: 每页多少条数据
    :param publish_end_time: 内容发布的截止时间
    :param publish_start_time: 内容发布的起始时间
    :return:
    """
    src_content_list_service = SrcContentService()
    page_size = min(page_size, 40)  # 每页几条记录做最大限制

    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'],
                         algorithms=[config['access_token']['ALGORITHM']])
    user_id = payload.get("user_id")

    src_content_list, count = src_content_list_service.get_src_content_list(
        user_id=user_id,
        city_id=city_id,
        is_used=is_used,
        content_type_id=content_type_id,
        page=page,
        page_size=page_size,
        publish_start_time=publish_start_time,
        publish_end_time=publish_end_time
    )

    return src_content_list, count


def get_src_content(content_id: int) -> Dict:
    """
    获取源内容详情
    :param content_id: 内容id
    :return:
    """
    src_content_service = SrcContentService()
    src_content = src_content_service.get_src_content(content_id=content_id)

    return src_content
