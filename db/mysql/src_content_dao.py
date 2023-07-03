import datetime
from typing import Dict, List

from conf.config import MYSQL_CONFIG
from db.mysql.mysql_db import MysqlClient
from utils.decorators import datetime_to_strftime


class SrcContentDAO(object):
    """ 源内容数据访问对象 """

    def __init__(self, *args, **kwargs):
        super(SrcContentDAO, self).__init__(*args, **kwargs)

    @staticmethod
    def get_mysql_conn():
        """ 获取mysql连接 """
        mysql_conn = MysqlClient(MYSQL_CONFIG)
        return mysql_conn

    @datetime_to_strftime
    def get_content_info(self, content_id: int) -> Dict:
        """
        获取内容信息
        :param content_id: 内容id
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        content_info = dict()
        try:
            sql = (
                'SELECT content_id, content_type_id, title, content, read_count, publish_time, source_web, source_link '
                'FROM src_content '
                'WHERE content_id = %s;')
            args = (content_id, )
            content_info = mysql_conn.fetchone(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return content_info

    @datetime_to_strftime
    def get_src_content_list(
            self,
            city_id: int,
            page: int,
            page_size: int,
            content_type_id: int,
            publish_start_time: str,
            publish_end_time: str
    ):
        """
        获取源内容列表
        :param page_size: 每页多少条数据
        :param page:  页码
        :param city_id: 城市id
        :param content_type_id: 内容类型id
        :param publish_end_time: 内容发布的截止时间
        :param publish_start_time: 内容发布的起始时间
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        content_list = list()
        try:
            sql = ('SELECT content_id, content_type_id, title, publish_time, source_web, source_link '
                   'FROM src_content '
                   'WHERE city_id = %s;')
            args = list()

            args.append(city_id)
            if content_type_id is not None:
                sql = sql[:-1]  # 去除末尾的分号
                sql += ' AND content_type_id = %s;'
                args.append(content_type_id)
            if publish_start_time is not None and publish_end_time is not None:
                sql = sql[:-1]  # 去除末尾的分号
                sql += ' AND publish_time BETWEEN %s AND %s;'
                args.append(publish_start_time)
                args.append(publish_end_time)
            sql = sql[:-1]
            sql += ' ORDER BY publish_time DESC LIMIT %s, %s;'
            args.append((page - 1)*page_size)
            args.append(page_size)
            _, content_list = mysql_conn.fetchall(sql, args=args)

            # 查询总记录数
            sql_count = ('SELECT COUNT(content_id) AS count '
                         'FROM src_content '
                         'WHERE city_id = %s;')
            args_count = list()

            args_count.append(city_id)

            if content_type_id is not None:
                sql_count = sql_count[:-1]  # 去除末尾的分号
                sql_count += ' AND content_type_id = %s;'
                args_count.append(content_type_id)

            if publish_start_time is not None and publish_end_time is not None:
                sql_count = sql_count[:-1]  # 去除末尾的分号
                sql_count += ' AND publish_time BETWEEN %s AND %s;'
                args_count.append(publish_start_time)
                args_count.append(publish_end_time)
            count = mysql_conn.fetchone(sql_count, args_count)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return content_list, count


def main():
    src_content_dao = SrcContentDAO()
    res = src_content_dao.get_src_content_list(
        city_id=3,
        page=1,
        page_size=5,
        content_type_id=2,
        publish_start_time="2023-06-07 00:00:00",
        publish_end_time="2023-06-15 10:45:35"
    )
    print(f"{res}")


if __name__ == '__main__':
    main()
