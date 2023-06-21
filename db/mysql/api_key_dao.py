from typing import List

from conf.config import MYSQL_CONFIG
from db.mysql.mysql_db import MysqlClient
from utils.decorators import datetime_to_strftime


class ApiKeyDAO(object):
    """ api_key数据访问对象 """

    def __init__(self, *args, **kwargs):
        super(ApiKeyDAO, self).__init__(*args, **kwargs)

    @staticmethod
    def get_mysql_conn():
        """获取mysql连接"""
        mysql_conn = MysqlClient(MYSQL_CONFIG)
        return mysql_conn

    @datetime_to_strftime
    def get_api_key_list(self) -> List:
        """
        获取可用的api_key列表
        :return:
        """

        mysql_conn = self.get_mysql_conn()
        try:
            sql = ('SELECT api_key, api_base, token_total, token_left, expire_time '
                   'FROM api_key '
                   'WHERE token_left > 0 '
                   'AND expire_time > NOW() '
                   'ORDER BY expire_time '
                   'LIMIT 0, 20;')
            args = ()
            _, api_key_list = mysql_conn.fetchall(sql, args=args)
        finally:
            if "mysql_conn" in dir():
                mysql_conn.close()

        return api_key_list


def main():
    apikey = ApiKeyDAO()
    res = apikey.get_api_key_list()
    print(res)


if __name__ == '__main__':
    main()
