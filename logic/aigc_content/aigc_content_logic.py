from typing import Dict

from jose import jwt

from conf.config import config
from items.aigc_content import AigcContentRequest
from logic.api_key import api_key_logic
from service.aigc_content_service import AigcContentService
from service.api_key_service import ApiKeyService
from service.user_service import UserService


def update_content_info(content_id: int, access_token: str, **aigc_content: AigcContentRequest):
    """
    更新内容信息
    :param access_token: 访问令牌
    :param content_id: 内容id
    :return:
    """
    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'],
                         algorithms=[config['access_token']['ALGORITHM']])
    user_id = payload.get("user_id")
    if aigc_content.get("token_usage_count") is None:
        content_token_usage_count = 0
    else:
        content_token_usage_count = aigc_content.get("token_usage_count")

    aigc_content_service = AigcContentService()
    aigc_content_service.update_content_info(content_id=content_id, **aigc_content)

    user_service = UserService()
    user_token_left_old = user_service.get_user_token_left(user_id=user_id)
    user_token_left = user_token_left_old - content_token_usage_count
    user_service.update_user_token_left(user_id=user_id, user_token_left=user_token_left)

    api_key_service = ApiKeyService()
    api_key_id = aigc_content["api_key_id"]
    api_key_token_left_old = api_key_service.get_api_key_token_left(api_key_id=api_key_id)
    api_key_token_left = api_key_token_left_old - content_token_usage_count
    api_key_service.update_api_key_token_left(api_key_id=api_key_id, api_key_token_left=api_key_token_left)


def get_src_content(content_id: int) -> Dict:
    """
    获取AIGC内容详情
    :param content_id: 内容id
    :return:
    """
    aigc_content_service = AigcContentService()
    content_info = aigc_content_service.get_content_info(content_id=content_id)

    return content_info
