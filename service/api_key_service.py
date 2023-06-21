from typing import Dict, List

from db.mysql.api_key_dao import ApiKeyDAO


class ApiKeyService(object):
    """ api_key服务对象 """

    def __init__(self, *args, **kwargs):
        self._apikey_dao = ApiKeyDAO()
        super(ApiKeyService, self).__init__(*args, **kwargs)

    def get_api_key_list(self) -> List:
        """
        获取可用的api_key列表
        :return:
        """
        api_key_list = self._apikey_dao.get_api_key_list()

        return api_key_list


def main():
    apikey = ApiKeyService()
    res = apikey.get_api_key_list()
    print(res)


if __name__ == '__main__':
    main()
