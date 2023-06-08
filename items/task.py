# coding=utf-8

from pydantic import BaseModel


class Task(BaseModel):
    task_id: int  # 任务id
    status: int  # 任务状态
