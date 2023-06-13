import traceback

from pymysql import DatabaseError

from conf.config import MYSQL_CONFIG, logger
from db.mysql.mysql_db import MysqlClient


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

    def get_user(self) -> dict:
        """
        根据用户名，获取用户信息
        :return: User对象
        """
        # mysql_conn = self.get_mysql_conn()
        # user = dict()
        # try:
        #     sql = ('SELECT user_id, role_id, city_id FROM user '
        #            'WHERE phone = %s;')
        #     args = (self.phone,)
        #     user = mysql_conn.fetchone(sql, args=args)
        # finally:
        #     if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
        #         mysql_conn.close()
        user = {"user": 1, "phone": 18649930703}

        return user

    def create_user(self) -> dict:
        """
        创建用户
        :return: User对象
        """
        mysql_conn = self.get_mysql_conn()
        user = dict()
        try:
            sql = ('INSERT INTO user(phone) '
                   'VALUES(%s);')
            args = (self.phone, )
            count = mysql_conn.execute(sql, args)
            mysql_conn.commit()

            # 新增成功，查找用户信息
            if count:
                user = self.get_user()
        except DatabaseError:
            error_str = traceback.format_exc()
            logger.error(error_str)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return user
