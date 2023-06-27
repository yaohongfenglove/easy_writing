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
            sql = ('SELECT content_id, title, summary, keywords, content, word_count, originality, status '
                   'FROM aigc_content '
                   'WHERE content_id = %s;')
            args = (content_id,)
            content_info = mysql_conn.fetchone(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()

        return content_info

    def update_content_info1(self, content_id: int, **aigc_content: AigcContentRequest) -> int:
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

    def update_content_info(self,
                            content_id: int,
                            status: int,
                            user_id: int,
                            content: str,
                            token_usage_count: int,
                            title: str,
                            summary: str,
                            keywords: str,
                            word_count: int,
                            originality: float,
                            ) -> int:
        """
        更新内容信息
        :param content_id: 内容id
        :param status: 内容生成的进度
        :param user_id: 用户id
        :param content: 正文
        :param token_usage_count: token使用量
        :param title: 标题
        :param summary: 摘要
        :param keywords: 关键词
        :param word_count: 字数
        :param originality: 原创度
        :return: 任务id
        """
        mysql_conn = self.get_mysql_conn()

        try:
            sql = 'UPDATE aigc_content SET '
            args = list()

            if status is not None:
                sql += 'status = %s, '
                args.append(status)

            if user_id is not None:
                sql += 'user_id = %s, '
                args.append(user_id)

            if content is not None:
                sql += 'content = %s, '
                args.append(content)

            if token_usage_count is not None:
                sql += 'token_usage_count = %s, '
                args.append(token_usage_count)

            if title is not None:
                sql += 'title = %s, '
                args.append(title)

            if summary is not None:
                sql += 'summary = %s, '
                args.append(summary)

            if keywords is not None:
                sql += 'keywords = %s, '
                args.append(summary)

            if word_count is not None:
                sql += 'word_count = %s, '
                args.append(word_count)

            if originality is not None:
                sql += 'originality = %s, '
                args.append(originality)

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
