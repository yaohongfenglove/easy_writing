from typing import Dict

from db.mysql.aigc_content_dao import AigcContentDAO


class AigcContentService(object):
    """ AIGC内容服务对象 """

    def __init__(self, *args, **kwargs):
        self._task_dao = AigcContentDAO()
        super(AigcContentService, self).__init__(*args, **kwargs)

    def get_content_info(self, content_id: int) -> Dict:
        """
        获取内容详情
        :param content_id: 内容id
        :return:
        """
        content_info = self._task_dao.get_content_info(content_id=content_id)
        return content_info

    def update_content_info(self,
                            content_id,
                            user_id,
                            status,
                            content,
                            token_usage_count,
                            title,
                            summary,
                            keywords,
                            word_count,
                            originality,
                            ):
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
        self._task_dao.update_content_info(
            content_id=content_id,
            user_id=user_id,
            status=status,
            content=content,
            token_usage_count=token_usage_count,
            title=title,
            summary=summary,
            keywords=keywords,
            word_count=word_count,
            originality=originality,
        )
