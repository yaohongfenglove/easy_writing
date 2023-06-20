from typing import List

from conf.config import MYSQL_CONFIG
from db.mysql.mysql_db import MysqlClient


class ApiKeyDAO(object):
    """ 用户数据访问对象 """

    def __init__(self, *args, **kwargs):
        super(ApiKeyDAO, self).__init__(*args, **kwargs)

    @staticmethod
    def get_mysql_conn():
        """获取mysql连接"""
        mysql_conn = MysqlClient(MYSQL_CONFIG)
        return mysql_conn

    def get_api_key(self) -> List:
        """
        获取可用的api_key
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        try:
            sql = ('SELECT api_key, api_base, token_total, token_left, expire_time '
                   'FROM api_key '
                   'WHERE token_left > 0 '
                   'AND expire_time > NOW() '
                   'ORDER BY expire_time '
                   'LIMIT 0,20;')
            args = ()
            _, access_key = mysql_conn.fetchall(sql, args=args)
        finally:
            if "mysql_conn" in dir():
                mysql_conn.close()

        return access_key


if __name__ == '__main__':
    apikey = ApiKeyDAO()
    res = apikey.get_api_key()
    print(res)
