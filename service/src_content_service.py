from typing import Dict, List

from db.mysql.src_content_dao import SrcContentDAO


class SrcContentService(object):
    """ 用户服务对象 """

    def __init__(self, *args, **kwargs):
        self._src_content_dao = SrcContentDAO()
        super(SrcContentService, self).__init__(*args, **kwargs)

    def get_src_content_list(
            self,
            user_id: int,
            city_id: int,
            is_used: int,
            content_type_id: int,
            page: int,
            page_size: int,
            publish_start_time: str,
            publish_end_time: str
    ):
        """
        获取源内容列表
        :param user_id: 用户id
        :param city_id: 城市id
        :param is_used: 是否使用过
        :param content_type_id: 内容类型id
        :param page: 页码
        :param page_size: 每页多少条数据
        :param publish_end_time: 内容发布的截止时间
        :param publish_start_time: 内容发布的起始时间
        :return:
        """
        src_content_list, count = self._src_content_dao.get_src_content_list(
            user_id=user_id,
            city_id=city_id,
            is_used=is_used,
            content_type_id=content_type_id,
            page=page,
            page_size=page_size,
            publish_start_time=publish_start_time,
            publish_end_time=publish_end_time
        )

        return src_content_list, count

    def get_src_content(self, content_id: int) -> Dict:
        """
        获取源内容详情
        :param content_id: 内容id
        :return:
        """
        src_content = self._src_content_dao.get_content_info(content_id=content_id)
        return src_content
