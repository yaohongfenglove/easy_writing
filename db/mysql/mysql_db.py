import datetime
import pymysql

from dbutils.pooled_db import PooledDB

from conf.config import logger, MYSQL_CONFIG


class MysqlClient(object):
    __pool = None

    def __init__(self, kwargs):
        if not self.__pool:
            self.__class__.__pool = PooledDB(cursorclass=pymysql.cursors.DictCursor, **kwargs)
        self._conn = None
        self._cursor = None
        self.__get_conn()

    def __get_conn(self):
        self._conn = self.__pool.connection()
        self._cursor = self._conn.cursor()

    def close(self):
        try:
            self._cursor.close()
            self._conn.close()
        except Exception as e:
            logger.error(e)

    def __execute(self, sql, args=()):
        count = self._cursor.execute(sql, args)
        return count

    def __executemany(self, sql, args=()):
        count = self._cursor.executemany(sql, args)
        return count

    @staticmethod
    def __dict_datetime_obj_to_str(result_dict):
        """
        把字典里面的datatime对象转成字符串，使json转换不出错
        """
        if result_dict:
            result_replace = {k: v.__str__() for k, v in result_dict.items() if isinstance(v, datetime.datetime)}
            result_dict.update(result_replace)
        return result_dict

    def fetchone(self, sql, args=()):
        """
        查询单个结果
        :param sql: qsl语句
        :param args: sql参数
        :return: 结果数量和查询结果集
        """
        self.__execute(sql, args)
        result = self._cursor.fetchone()
        return result

    def fetchall(self, sql, args=()):
        """
        查询多个结果
        :param sql:sql语句
        :param args: sql参数
        :return: 结果数量和查询结果集
        """
        count = self.__execute(sql, args)
        result = self._cursor.fetchall()
        return count, result

    def execute(self, sql, args=()):
        count = self.__execute(sql, args)
        return count

    def commit(self):
        res = self._conn.commit()
        return res

    def rollback(self):
        res = self._conn.rollback()
        return res

    def begin(self):
        """开启事务"""
        self._conn.autocommit(0)

    def end(self, option='commit'):
        """结束事务"""
        if option == 'commit':
            self._conn.autocommit()
        else:
            self._conn.rollback()


def main():
    conn = MysqlClient(MYSQL_CONFIG)
    sql = 'SELECT * FROM user LIMIT 2;'
    count, res = conn.fetchall(sql)
    logger.info(f"{count},{res}")
    conn.close()


if __name__ == '__main__':
    main()



