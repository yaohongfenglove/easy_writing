from typing import List, Dict

from service.task_service import TaskService
from service.user_service import UserService
from utils.exceptions import NoApiKeysAvailableError


def get_tasks(user_id: int):
    """
    获取特定用户的任务列表
    :param user_id: 用户id
    :return:
    """
    task_service = TaskService()
    tasks = task_service.get_tasks(user_id=user_id)

    return tasks


def create_task(user_id: int, city_id: int,
                src_content_ids: List[int], client_version: str) -> Dict:
    """
    创建任务
    :param user_id: 用户id
    :param city_id: 城市id
    :param src_content_ids: 源内容id列表
    :param client_version: 客户端版本号
    :return:
    """

    # 查询可用的api_key
    user_server = UserService()
    user_extra_info = user_server.get_user_extra_info(user_id=user_id)
    api_key_list = user_extra_info.get("api_key_list")
    if not api_key_list:
        raise NoApiKeysAvailableError("无可用的api_key了")
    api_key = api_key_list[0].get("api_key")
    api_base = api_key_list[0].get("api_base")

    # 创建任务
    task_service = TaskService()
    task_id = task_service.create_task(user_id=user_id, city_id=city_id,
                                       src_content_ids=src_content_ids, client_version=client_version)
    # 获取任务对应的详情列表
    task_info = task_service.get_task_pro_info(task_id=task_id)

    res = {
        "list": task_info,
        "api_key": api_key,
        "api_base": api_base,
        "task_id": task_id,
        "status": 0,
    }

    return res


def get_task_base_info(task_id: int):
    """
    获取任务基础信息
    :param task_id: 任务id
    :return:
    """

    task_service = TaskService()
    task_info = task_service.get_task_base_info(task_id=task_id)

    return task_info
