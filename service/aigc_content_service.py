from db.mysql.aigc_content_dao import AigcContentDAO
from items.aigc_content import AigcContentRequest


class AigcContentService(object):
    """ AIGC内容服务对象 """

    def __init__(self, *args, **kwargs):
        self._task_dao = AigcContentDAO()
        super(AigcContentService, self).__init__(*args, **kwargs)

    def update_content_info(self, content_id: int, **aigc_content: AigcContentRequest):
        """ 更新内容信息 """
        self._task_dao.update_content_info(content_id, **aigc_content)
