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

    # TODO 时间显示错误，为datetime格式，需转为str格式字符串
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
                'SELECT content_id,content_type_id, title, content, read_count, publish_time, source_web, source_link '
                'FROM src_content '
                'WHERE content_id = %s;')
            args = (content_id,)
            content_info = mysql_conn.fetchone(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return content_info

    def get_src_content_list(self, city_id: int, content_type_id=None,
                             publish_start_time=None, publish_end_time=None) -> List:
        """
        获取源内容列表
        :param city_id: 城市id
        :param content_type_id: 内容类型id
        :param publish_end_time: 内容发布的截止时间
        :param publish_start_time: 内容发布的起始时间
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        src_content_list = list()
        content_info = dict()
        args = list()
        try:
            sql = 'SELECT content_id,content_type_id, title, publish_time, source_web, source_link ' \
                  'FROM src_content WHERE city_id = %s;'
            args = [city_id]
            if content_type_id is not None:
                sql = sql[:-1]  # 去除末尾的分号
                sql += f' and content_type_id= %s ;'
                args.append(content_type_id)
            if publish_start_time is not None and publish_end_time is not None:
                sql = sql[:-1]  # 去除末尾的分号
                sql += f' AND publish_time BETWEEN %s AND %s ;'
                args.append(publish_start_time)
                args.append(publish_end_time)
            content_info = mysql_conn.fetchall(sql, args=args)
            src_content_list.append(content_info)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return src_content_list


def main():
    src_content_dao = SrcContentDAO()
    res = src_content_dao.get_src_content_list(city_id=3,
                                               content_type_id=1)
    print(f"{res}")


if __name__ == '__main__':
    main()
