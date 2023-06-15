# coding=utf-8

import datetime

from starlette.background import BackgroundTasks

from items.response import GenericResponse
from items.task import TaskRequest
from logic.task import task_logic


def get_tasks(
        user_id: int

):
    """
    获取特定用户的任务列表
    :param user_id: 用户id
    :return:
    """
    tasks = task_logic.get_tasks(user_id=user_id)

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "list": tasks,
            "count": len(tasks)
        }
    )


def create_task(
        task: TaskRequest,
        background_tasks: BackgroundTasks
):
    """
    创建任务
    :param task: 待完成的任务对象
    :param background_tasks: 后台任务
    :return: 任务id
    """
    task_id = task_logic.create_task(**task.dict())

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "task_id": task_id
        }
    )
