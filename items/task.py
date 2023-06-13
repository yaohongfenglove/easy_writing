# coding=utf-8

"""
    UserIn 和 UserOut
    https://fastapi.tiangolo.com/zh/tutorial/response-model/
"""

from typing import List

from pydantic import BaseModel


class TaskRequest(BaseModel):
    """
    请求时的任务对象
    """
    user_id: int  # 用户id
    city_id: int  # 城市id
    src_content_ids: List[int]  # 源内容id列表
    client_version: str  # 客户端版本号


class TaskResponse(BaseModel):
    """
    响应时的任务对象
    """
    task_id: int  # 任务id
    status: int  # 任务状态
