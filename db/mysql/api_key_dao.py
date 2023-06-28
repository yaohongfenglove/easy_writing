import warnings
from typing import List, Dict, Union

from conf.config import MYSQL_CONFIG
from db.mysql.mysql_db import MysqlClient
from utils.decorators import datetime_to_strftime


class ApiKeyDAO(object):
    """ api_key数据访问对象 """

    def __init__(self,api_key_id="", *args, **kwargs):
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
            sql = ('SELECT api_key_id, api_key, api_base, token_total, token_left, expire_time '
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

    def get_api_key_token_left(self, api_key_id: int) -> Union[int, None]:
        """
        获取api_key的token余量
        :param: api_key_id:
        :return:
        """

        mysql_conn = self.get_mysql_conn()
        try:
            sql = ('SELECT token_left '
                   'FROM api_key '
                   'WHERE api_key_id = %s;')
            args = (api_key_id,)
            api_key_token_left = mysql_conn.fetchone(sql, args=args)
            if api_key_token_left is None:
                return None
            key_token_left = api_key_token_left["token_left"]
        finally:
            if "mysql_conn" in dir():
                mysql_conn.close()

        return key_token_left

    def update_api_key_token_left(self, api_key_id: int, api_key_token_left: int) -> int:
        """
        更新api_key的token余量
        :param: api_key_id: api_key的id
        :param: user_token_left:用户token余量
        :return:
        """
        warnings.warn("此方法已弃用，不推荐使用", DeprecationWarning)

        mysql_conn = self.get_mysql_conn()

        try:
            sql = ('UPDATE api_key '
                   'SET token_left=%s '
                   'WHERE api_key_id=%s; ')
            args = (api_key_token_left, api_key_id)

            count = mysql_conn.execute(sql, args)
            mysql_conn.commit()

            return count
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()


def main():
    apikey = ApiKeyDAO()
    res = apikey.get_api_key_list()
    print(res)


if __name__ == '__main__':
    main()
