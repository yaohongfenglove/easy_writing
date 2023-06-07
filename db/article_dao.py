import json
import traceback
from typing import List

from pymysql import DatabaseError

from conf.config import MYSQL_CONFIG, logger
from db.mysql_db import MysqlClient


class ArticleDAO(object):
    """文章访问对象"""
    def __init__(self, *args, **kwargs):
        super(ArticleDAO, self).__init__(*args, **kwargs)

    @staticmethod
    def get_mysql_conn():
        """
        获取mysql连接
        :return:
        """
        mysql_conn = MysqlClient(MYSQL_CONFIG)
        return mysql_conn

    def get_article(self, article_id: int) -> dict:
        mysql_conn = self.get_mysql_conn()
        article = dict()
        try:
            sql = ('SELECT article_id, title, content '
                   'FROM article '
                   'WHERE article_id = %s;')
            args = (article_id, )
            article = mysql_conn.fetchone(sql, args=args)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()
        return article

    def create_article(self, article_id: int, title: str, contexts: List, article_type: int):
        """
        创建文章
        :param article_id: 文章id
        :param title:  文章标题
        :param contexts:  写作基于的上下文（加上用户自己的）
        :param article_type:  文章类型
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        try:
            sql = ('UPDATE 'article' SET title = %s, contexts = %s, article_type = %s WHERE article_id = %s;')
            args = (title, json.dumps(contexts,ensure_ascii=False), article_type, article_id)
            mysql_conn.execute(sql, args)
            mysql_conn.commit()
        except DatabaseError:
            mysql_conn.rollback()
            error_str = traceback.format_exc()
            logger.error(error_str)
        finally:
            if "mysql_conn" in dir():
                mysql_conn.close()
        return article_id

    def get_context(self, article_id: int) -> dict:
        """
        获取上下文
        :param article_id:  文章id
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        context = dict()
        try:
            sql = ('SELECT article_id, context_desc, context as content '
                   'FROM article '
                   'WHERE article_id = %s;')
            args = (article_id, )
            context = mysql_conn.fetchone(sql, args=args)
        finally:
            if "mysql_conn" in dir():
                mysql_conn.close()
        return context

    def create_context(self, desc: str) -> dict:
        """
        创建上下文
        :param desc: 上下文描述
        :return:
        """
        mysql_conn = self.get_mysql_conn()
        article_id = None
        try:  # 新建文章
            sql = ('INSERT INTO `article`(context_desc) '
                   'VALUES(%s);')
            args = (desc, )
            mysql_conn.commit()

            sql = 'SELECT LAST_INSERT_ID() AS article_id;'  #查找自增id
            args = ()
            article_id = mysql_conn.fetchone(sql, args).get("article_id")
        except DatabaseError:
            mysql_conn.rollback()
            error_str = traceback.format_exc()
            logger.error(error_str)
        finally:
            if "mysql_conn" in dir():
                mysql_conn.close()
        return article_id

    def update_context(self, context, article_id):
        mysql_conn = self.get_mysql_conn()
        try:
            sql = ('UPDATE article SET context = %s '
                   'WHERE article_id = %s;')
            args = (context, article_id)
            count = mysql_conn.execute(sql, args)
            mysql_conn.commit()
        except DatabaseError:
            error_str = traceback.format_exc()
            logger.error(error_str)
        finally:
            if "mysql_conn" in dir():  # 判断连接是否成功创建，创建了才能执行close()
                mysql_conn.close()
        return None


