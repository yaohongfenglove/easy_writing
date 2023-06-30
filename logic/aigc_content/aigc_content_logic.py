import warnings
from typing import Dict, Union

from jose import jwt

from conf.config import config
from items.aigc_content import AigcContentRequest
from service.aigc_content_service import AigcContentService
from service.api_key_service import ApiKeyService
from service.user_service import UserService


def update_content_info1(content_id: int, aigc_content: AigcContentRequest, access_token: str):
    """
    更新内容信息
    :param content_id: 内容id
    :param aigc_content: AIGC内容对象
    :param access_token: 访问令牌
    :return:
    """
    warnings.warn("此方法已弃用，不推荐使用", DeprecationWarning)

    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'],
                         algorithms=[config['access_token']['ALGORITHM']])
    user_id = payload.get("user_id")

    if aigc_content.token_usage_count is None:
        content_token_usage_count = 0
    else:
        content_token_usage_count = aigc_content.token_usage_count

    user_service = UserService()
    user_token_left_old = user_service.get_user_token_left(user_id=user_id)
    user_token_left = user_token_left_old - content_token_usage_count

    api_key_service = ApiKeyService()
    api_key_token_left_old = api_key_service.get_api_key_token_left(api_key_id=aigc_content.api_key_id)
    api_key_token_left = api_key_token_left_old - content_token_usage_count

    aigc_content_service = AigcContentService()
    aigc_content_service.update_content_info(content_id=content_id, user_id=user_id, user_token_left=user_token_left,
                                             api_key_token_left=api_key_token_left, **aigc_content.dict())


# TODO 2023-6-27 10:16:15 sql事物控制
def update_content_info(content_id: int, aigc_content: AigcContentRequest, access_token: str):
    """
    更新内容信息
    :param content_id: 内容id
    :param aigc_content: AIGC内容对象
    :param access_token: 访问令牌
    :return:
    """

    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'],
                         algorithms=[config['access_token']['ALGORITHM']])
    user_id = payload.get("user_id")

    aigc_content_service = AigcContentService()
    aigc_content_service.update_content_info(content_id=content_id, user_id=user_id, **aigc_content.dict())


def get_src_content(content_id: int) -> Dict:
    """
    获取AIGC内容详情
    :param content_id: 内容id
    :return:
    """
    aigc_content_service = AigcContentService()
    content_info = aigc_content_service.get_content_info(content_id=content_id)

    return content_info
