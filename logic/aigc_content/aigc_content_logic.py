from typing import Dict

from items.aigc_content import AigcContentRequest
from service.aigc_content_service import AigcContentService


def update_content_info(content_id: int, **aigc_content: AigcContentRequest):
    """
    更新内容信息
    :param content_id: 内容id
    :return:
    """
    aigc_content_service = AigcContentService()
    aigc_content_service.update_content_info(content_id=content_id, **aigc_content)


def get_src_content(content_id: int) -> Dict:
    """
    获取AIGC内容详情
    :param content_id: 内容id
    :return:
    """
    aigc_content_service = AigcContentService()
    content_info = aigc_content_service.get_content_info(content_id=content_id)

    return content_info
