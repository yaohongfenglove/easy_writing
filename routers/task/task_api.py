# coding=utf-8

import datetime

from starlette import status

from items.response import GenericResponse
from items.task import TaskRequest
from logic.task import task_logic
from utils.constants import StatusCodeEnum
from utils.exceptions import NoApiKeysAvailableError, CustomHTTPException


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
        task: TaskRequest
):
    """
    创建任务
    :param task: 待完成的任务对象
    :return: 任务id
    """
    try:
        res = task_logic.create_task(**task.dict())
    except NoApiKeysAvailableError:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code=StatusCodeEnum.NO_API_KEYS_AVAILABLE_ERR.code,
            msg=StatusCodeEnum.NO_API_KEYS_AVAILABLE_ERR.errmsg,
        )

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "result": res
        }
    )


def get_api_key(user_id: int):
    """ 获取 """
