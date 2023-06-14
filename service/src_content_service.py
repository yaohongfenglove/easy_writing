from typing import Dict, List

from db.mysql.src_content_dao import SrcContentDAO


class SrcContentService(object):
    """ 用户服务对象 """

    def __init__(self, *args, **kwargs):
        self._src_content_dao = SrcContentDAO()
        super(SrcContentService, self).__init__(*args, **kwargs)

    def get_src_content_list(self, city_id: int, content_type_id=None,
                             publish_start_time=None, publish_end_time=None) -> List:
        """
        获取源内容列表
        :param city_id: 城市id
        :param content_type_id: 内容类型id
        :param publish_end_time: 内容发布的截止时间
        :param publish_start_time: 内容发布的起始时间
        :return:
        """
        src_content_list = self._src_content_dao.get_src_content_list(city_id=city_id)

        return src_content_list

    def get_src_content(self, content_id: int) -> Dict:
        """
        获取源内容详情
        :param content_id: 内容id
        :return:
        """
        src_content = self._src_content_dao.get_content_info(content_id=content_id)
        return src_content

