import traceback
from typing import List, Dict

from pymysql import DatabaseError

from conf.config import MYSQL_CONFIG, logger
from db.mysql.mysql_db import MysqlClient
from utils.decorators import datetime_to_strftime
from utils.exceptions import TaskCreateError


class TaskDAO(object):
    """ 任务数据访问对象 """
    def __init__(self, *args, **kwargs):
        super(TaskDAO, self).__init__(*args, **kwargs)

    @staticmethod
    def get_mysql_conn():
        """ 获取mysql连接 """
        mysql_conn = MysqlClient(MYSQL_CONFIG)
        return mysql_conn

    @datetime_to_strftime
    def get_tasks(self, user_id: int) -> List[Dict]:
        """
        获取特定用户的任务列表
        :param user_id: 用户id
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        tasks = list()
        try:
            sql = ('SELECT task_id, status, create_time '
                   'FROM aigc_task '
                   'WHERE user_id = %s;')
            args = (user_id, )
            _, tasks = mysql_conn.fetchall(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return tasks

    @datetime_to_strftime
    def get_task_pro_info(self, task_id: int) -> List[Dict]:
        """
        获取任务详细信息
        :param task_id: 任务id
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        task_info = list()
        try:
            sql = ('SELECT ac.content_id, ac.status, ac.create_time, '
                   'sc.title, sc.content, '
                   'p.prompt '
                   'FROM aigc_content ac '
                   'JOIN aigc_task at ON ac.task_id = at.task_id AND ac.task_id = %s '
                   'JOIN src_content sc ON ac.src_content_id = sc.content_id '
                   'JOIN prompt p ON sc.content_type_id = p.content_type_id AND writing_type_id = 1;')
            args = (task_id, )
            _, task_info = mysql_conn.fetchall(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return task_info

    @datetime_to_strftime
    def get_task_base_info(self, task_id: int) -> List[Dict]:
        """
        获取任务基础信息
        :param task_id: 任务id
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        task_base_info = list()
        try:
            sql = ('SELECT ac.content_id, ac.title, ac.word_count, ac.originality,'
                   ' ac.status, ac.create_time '
                   'FROM aigc_content ac '
                   'JOIN aigc_task at ON ac.task_id = at.task_id AND ac.task_id = %s;')
            args = (task_id, )
            _, task_base_info = mysql_conn.fetchall(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return task_base_info

    def create_task(self, user_id: int, city_id: int,
                    src_content_ids: List[int], client_version: str) -> int:
        """
        创建任务
        :param user_id: 用户id
        :param city_id: 城市id
        :param src_content_ids: 源内容id列表
        :param client_version: 客户端版本号
        :return: 任务id
        """
        mysql_conn = self.get_mysql_conn()

        try:
            mysql_conn.begin()

            # 1.插入aigc任务表
            sql = ('INSERT INTO `aigc_task`(user_id, city_id, client_version) '
                   'VALUES(%s, %s, %s);')
            args = (user_id, city_id, client_version)
            mysql_conn.execute(sql, args)
            # 查找自增id
            sql = 'SELECT LAST_INSERT_ID() AS task_id;'
            args = ()
            task_id = mysql_conn.fetchone(sql, args).get("task_id")

            # 2.插入aigc内容表
            sql = ('INSERT INTO `aigc_content`(src_content_id, task_id) '
                   'VALUES(%s, %s);')
            args = [(src_content_id, task_id) for src_content_id in src_content_ids]
            mysql_conn.executemany(sql, args)

            # 提交事物
            mysql_conn.commit()
            return task_id
        except DatabaseError:
            mysql_conn.rollback()
            error_str = traceback.format_exc()
            logger.error(error_str)
            raise TaskCreateError("任务创建失败")
        except Exception:
            mysql_conn.rollback()
            error_str = traceback.format_exc()
            logger.error(error_str)
            raise TaskCreateError("任务创建失败")
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()


def main():
    # 1. 查询任务列表
    # task_dao = TaskDAO()
    # res = task_dao.get_tasks(user_id=1)
    # print(f"{res}")

    # 2. 创建任务
    # task_dao = TaskDAO()
    # task_id = task_dao.create_task(user_id=1, city_id=12, src_content_ids=[100, 101], client_version="1.0.0.0")
    # print(f"{task_id}")

    # 3. 查询任务详细信息
    task_dao = TaskDAO()
    res = task_dao.get_task_pro_info(task_id=1)
    print(f"{res}")


if __name__ == '__main__':
    main()
