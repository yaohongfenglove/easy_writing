from conf.config import MYSQL_CONFIG
from db.mysql.mysql_db import MysqlClient
from items.aigc_content import AigcContentRequest


class AigcContentDAO(object):
    """ AIGC内容数据访问对象 """
    def __init__(self, *args, **kwargs):
        super(AigcContentDAO, self).__init__(*args, **kwargs)

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
            sql = ('SELECT content_id, title, summary, keywords, content, word_count, originality '
                   'FROM aigc_content '
                   'WHERE content_id = %s;')
            args = (content_id,)
            content_info = mysql_conn.fetchone(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return content_info

    def update_content_info(self, content_id: int, **aigc_content: AigcContentRequest) -> int:
        """
        更新内容信息
        :param content_id: 内容id
        :return:
        """
        mysql_conn = self.get_mysql_conn()

        try:
            sql = 'UPDATE aigc_content SET '
            args = list()

            for key, value in aigc_content.items():
                if value is not None:
                    sql += f'{key} = %s, '
                    args.append(value)

            sql = sql[:-2]  # 去除末尾的逗号和空格

            sql += ' WHERE content_id = %s;'
            args.append(content_id)

            count = mysql_conn.execute(sql, args)
            mysql_conn.commit()

            return count
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()


def main():
    aigc_content_dao = AigcContentDAO()
    res = aigc_content_dao.get_content_info(content_id=1)
    print(f"{res}")


if __name__ == '__main__':
    main()
