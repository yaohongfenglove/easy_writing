# coding=utf-8

import datetime

from fastapi import Header
from jose import jwt
from starlette import status as starlette_status

from conf.config import config
from items.response import GenericResponse
from items.task import TaskRequest
from logic.task import task_logic
from utils.constants import StatusCodeEnum
from utils.exceptions import NoApiKeysAvailableError, CustomHTTPException


def get_tasks(
        access_token: str = Header()

):
    """
    获取特定用户的任务列表
    :param access_token: 访问令牌
    :return:
    """

    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'],
                         algorithms=[config['access_token']['ALGORITHM']])
    user_id = payload.get("user_id")
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
            status_code=starlette_status.HTTP_400_BAD_REQUEST,
            code=StatusCodeEnum.NO_API_KEYS_AVAILABLE_ERR.code,
            msg=StatusCodeEnum.NO_API_KEYS_AVAILABLE_ERR.errmsg,
        )

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "result": res
        }
    )


def get_task_base_info(task_id: int):
    """
    获取任务基础信息
    :param task_id: 任务id
    :return:
    """
    task_info = task_logic.get_task_base_info(task_id=task_id)

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "list": task_info,
            "count": len(task_info)
        }
    )


def update_task(
        task_id: int,
        status: int
):
    """
    更新任务状态
    :param task_id: 任务id
    :param status: 任务状态值
    :return: 任务id
    """

    task_logic.update_task(task_id=task_id, status=status)

    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={}
    )
