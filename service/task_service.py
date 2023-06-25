from typing import List, Dict

from db.mysql.task_dao import TaskDAO


class TaskService(object):
    """ 用户服务对象 """

    def __init__(self, *args, **kwargs):
        self._task_dao = TaskDAO()
        super(TaskService, self).__init__(*args, **kwargs)

    def get_tasks(self, user_id: int, page: int, page_size: int) -> List[Dict]:
        """
        获取特定用户的任务列表
        :param user_id: 用户id
        :param page: 页码
        :param page_size: 每页多少条数据
        :return:
        """
        tasks = self._task_dao.get_tasks(user_id=user_id, page=page, page_size=page_size)
        return tasks

    def get_task_pro_info(self, task_id: int) -> List[Dict]:
        """
        获取任务详细信息
        :param task_id: 任务id
        :return:
        """
        task_info = self._task_dao.get_task_pro_info(task_id=task_id)
        return task_info

    def get_task_base_info(self, task_id: int) -> List[Dict]:
        """
        获取任务基础信息
        :param task_id: 任务id
        :return:
        """
        task_info = self._task_dao.get_task_base_info(task_id=task_id)
        return task_info

    def create_task(self, user_id: int, city_id: int,
                    src_content_ids: List[int], client_version: str) -> int:
        """ 创建任务 """
        task_id = self._task_dao.create_task(user_id=user_id, city_id=city_id,
                                             src_content_ids=src_content_ids, client_version=client_version)

        return task_id

    def update_task(self, task_id: int, status: int):
        """ 更新任务状态 """
        self._task_dao.update_task(task_id=task_id, status=status)


def main():
    # 1. 查询任务列表
    task_service = TaskService()
    res = task_service.get_tasks(user_id=1)
    print(f"{res}")

    # 2. 创建任务
    # task_service = TaskService()
    # task_id = task_service.create_task(user_id=1, city_id=12, src_content_ids=[100, 101], client_version="1.0.0.0")
    # print(f"{task_id}")


if __name__ == '__main__':
    main()
