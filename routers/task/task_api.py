# coding=utf-8

import datetime

from starlette.background import BackgroundTasks

from items.response import GenericResponse
from items.task import Task


def get_task(
        task_id: int

):
    """ 获取任务信息 """
    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "task_id": 1,
            "status": 1
        }
    )


def create_task(
        task: Task,
        background_tasks: BackgroundTasks
):
    """
    创建上下文
    :param task: 待完成的任务对象
    :param background_tasks: 后台任务
    :return: 文章id
    """
    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "task_id": 1
        }
    )
