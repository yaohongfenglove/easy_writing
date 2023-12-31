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

    def update_content_info(self, content_id: int, user_id: int, status: int, content: str, token_usage_count: int,
                            title: str, summary: str, keywords: str, word_count: int, originality: float,
                            api_key_id: int, error_msg: str, **kwargs):
        """
        更新内容信息
        :param content_id: 内容id
        :param user_id: 用户id
        :param status: 内容生成的进度
        :param content: 正文
        :param token_usage_count: token使用量
        :param title: 标题
        :param summary: 摘要
        :param keywords: 关键词
        :param word_count: 字数
        :param originality: 原创度
        :param api_key_id: api_Key的id
        :param error_msg: 失败原因
        :param kwargs: TODO 2023-6-27 10:51:25 AigcContentRequest类抽离api_key_id属性后，删去**kwargs
        :return:
        """
        self._task_dao.update_content_info(
            content_id=content_id, user_id=user_id, status=status, content=content, token_usage_count=token_usage_count,
            title=title, summary=summary, keywords=keywords, word_count=word_count, originality=originality,
            api_key_id=api_key_id, error_msg=error_msg
        )
