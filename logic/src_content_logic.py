import datetime

from service.src_content_service import SrcContentService


def get_src_content_list(city_id: int, content_type_id=None,
                         publish_start_time=None, publish_end_time=None, page=1, page_size=10):
    """
    获取源内容列表
    :param city_id: 城市id
    :param content_type_id: 内容类型id
    :param page_size: 每页条数
    :param page: 页码
    :param publish_end_time: 内容发布的截止时间
    :param publish_start_time: 内容发布的起始时间
    :return:
    """
    src_content_list_service = SrcContentService()
    src_content_list = src_content_list_service.get_src_content_list(city_id=city_id)

    return src_content_list


def get_src_content(content_id: int):
    """
    获取源内容详情
    :param content_id: 内容id
    :return:
    """
    src_content_service = SrcContentService()
    src_content = src_content_service.get_src_content(content_id=content_id)

    return src_content
