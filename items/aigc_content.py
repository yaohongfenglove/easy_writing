# coding=utf-8

"""
    UserIn 和 UserOut
    https://fastapi.tiangolo.com/zh/tutorial/response-model/
"""


from pydantic import BaseModel


class AigcContentRequest(BaseModel):
    """
    请求时的AIGC内容对象
    """
    content: str  # 正文
    token_usage_count: int  # token使用量
    status: int  # 内容生成的进度
    title: str  # 标题
    summary: str  # 摘要
    keywords: str  # 关键词
    word_count: int  # 字数
    originality: int  # 原创度


class AigcContentResponse(BaseModel):
    """
    响应时的AIGC内容对象
    """
    content_id: int  # 内容id
    status: int  # 内容生成的进度
