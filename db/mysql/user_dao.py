from typing import Dict


from conf.config import MYSQL_CONFIG
from db.mysql.mysql_db import MysqlClient
from utils.decorators import datetime_to_strftime


class UserDAO(object):
    """ 用户数据访问对象 """
    def __init__(self, phone="", verification_code="", *args, **kwargs):
        super(UserDAO, self).__init__(*args, **kwargs)
        self.phone = phone
        self.verification_code = verification_code

    @staticmethod
    def get_mysql_conn():
        """ 获取mysql连接 """
        mysql_conn = MysqlClient(MYSQL_CONFIG)
        return mysql_conn

    def get_user(self) -> Dict:
        """
        根据手机号，获取用户信息
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        user = dict()
        try:
            sql = ('SELECT user_id, phone FROM user '
                   'WHERE phone = %s;')
            args = (self.phone, )
            user = mysql_conn.fetchone(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return user

    def get_user_city_list(self, user_id: int):
        """
        获取用户的城市列表
        :param user_id: 用户id
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        city_list = list()
        try:
            sql = ('SELECT c.city_id, c.city_name '
                   'FROM user_city uc '
                   'JOIN city c '
                   'ON uc.city_id = c.city_id '
                   'AND user_id = %s;')
            args = (user_id, )
            _, city_list = mysql_conn.fetchall(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return city_list

    @datetime_to_strftime
    def get_user_api_key_list(self, user_id: int):
        """
        获取用户的api_key列表
        :param user_id: 用户id
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        api_key_list = list()
        try:
            sql = ('SELECT api_key, api_base, token_total, token_left, expire_time '
                   'FROM api_key '
                   'WHERE user_id = %s '
                   'AND token_left > 0 '
                   'AND expire_time > NOW();')
            args = (user_id, )
            _, api_key_list = mysql_conn.fetchall(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return api_key_list


def main():
    user_dao = UserDAO()

    res = user_dao.get_user_city_list(user_id=1)
    print(f"{res}")

    res = user_dao.get_user_api_key_list(user_id=2)
    print(f"{res}")


if __name__ == '__main__':
    main()
