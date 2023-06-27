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

    def get_api_key_token_left(self, api_key_id):
        """
        获取key的token余量
        :param api_key_id: key的id
        :return:
        """
        api_key_token_left = self._apikey_dao.get_api_key_token_left(api_key_id=api_key_id)

        return api_key_token_left

    def update_api_key_token_left(self, api_key_id, api_key_token_left: int):
        """
        更新api_key的token余量
        :param: api_key_id: api_key的id
        :param: user_token_left:用户token余量
        :return:
        """
        self._apikey_dao.update_api_key_token_left(api_key_id=api_key_id, api_key_token_left=api_key_token_left)


def main():
    apikey = ApiKeyService()
    res = apikey.get_api_key_list()
    print(res)


if __name__ == '__main__':
    main()
