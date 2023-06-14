from typing import List

from starlette.background import BackgroundTasks

from service.task_service import TaskService


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
                src_content_ids: List[int], client_version: str,
                background_tasks: BackgroundTasks = None) -> int:
    """
    创建任务
    :param user_id: 用户id
    :param city_id: 城市id
    :param src_content_ids: 源内容id列表
    :param client_version: 客户端版本号
    :param background_tasks: 后台任务
    :return:
    """
    task_service = TaskService()
    task_id = task_service.create_task(user_id=user_id, city_id=city_id,
                                       src_content_ids=src_content_ids, client_version=client_version)

    if background_tasks:
        background_tasks.add_task(generate_content, task_id=task_id)

    return task_id


def generate_content(self, task_id: int):
    """ 生成内容 """
    pass
