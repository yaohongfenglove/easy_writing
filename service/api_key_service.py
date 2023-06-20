from typing import Dict, List

from db.mysql.api_key_dao import ApiKeyDAO
from db.mysql.user_dao import UserDAO


class ApiKeyService(object):
    """ 用户服务对象 """

    def __init__(self, *args, **kwargs):
        self._apikey_dao = ApiKeyDAO()
        self._user_dao = UserDAO()
        super(ApiKeyService, self).__init__(*args, **kwargs)

    def get_api_key(self) -> List:
        """
        获取用户的api_key列表
        :return:
        """
        access_key = self._apikey_dao.get_api_key()

        return access_key


if __name__ == '__main__':
    apikey = ApiKeyService()
    res = apikey.get_api_key()
    print(res)
