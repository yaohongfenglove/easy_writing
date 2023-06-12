from conf.config import MYSQL_CONFIG
from db.mysql.mysql_db import MysqlClient


class SrcContentDAO(object):
    """ 源内容数据访问对象 """
    def __init__(self, *args, **kwargs):
        super(SrcContentDAO, self).__init__(*args, **kwargs)

    @staticmethod
    def get_mysql_conn():
        """ 获取mysql连接 """
        mysql_conn = MysqlClient(MYSQL_CONFIG)
        return mysql_conn

    def get_content_info(self, content_id: int) -> dict:
        """
        获取内容信息
        :param content_id: 内容id
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        content_info = dict()
        try:
            sql = ('SELECT content_id, title, content, publish_time '
                   'FROM src_content '
                   'WHERE content_id = %s;')
            args = (content_id,)
            content_info = mysql_conn.fetchone(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return content_info


def main():
    src_content_dao = SrcContentDAO()
    res = src_content_dao.get_content_info(content_id=1)
    print(f"{res}")


if __name__ == '__main__':
    main()
