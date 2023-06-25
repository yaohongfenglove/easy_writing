# coding=utf-8

"""
    UserIn 和 UserOut
    https://fastapi.tiangolo.com/zh/tutorial/response-model/
"""

from typing import Union

from pydantic import BaseModel


class AigcContentRequest(BaseModel):
    """
    请求时的AIGC内容对象
    """
    status: int  # 内容生成的进度
    api_key_id: int  # key的id
    content: Union[str, None] = None  # 正文
    token_usage_count: Union[int, None] = None  # token使用量
    title: Union[str, None] = None  # 标题
    summary: Union[str, None] = None  # 摘要
    keywords: Union[str, None] = None  # 关键词
    word_count: Union[str, None] = None  # 字数
    originality: Union[str, None] = None  # 原创度


class AigcContentResponse(BaseModel):
    """
    响应时的AIGC内容对象
    """
    content_id: int  # 内容id
    status: int  # 内容生成的进度
