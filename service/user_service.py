import datetime
from typing import Dict, List

from db.mysql.user_dao import UserDAO


class UserService(object):
    """ 用户服务对象 """

    def __init__(self, phone="", verification_code="", *args, **kwargs):
        self._user_dao = UserDAO(phone, verification_code)
        super(UserService, self).__init__(*args, **kwargs)

    def get_user(self) -> dict:
        user = self._user_dao.get_user()
        return user

    def get_user_extra_info(self, user_id: int) -> Dict[str, List]:
        """
        获取用户的其他额外信息
        :param user_id: 用户id
        :return:
        """
        city_list = self._user_dao.get_user_city_list(user_id=user_id)
        api_key_list = self._user_dao.get_user_api_key_list(user_id=user_id)
        user_extra_info = {
            "city_list": city_list,
            "api_key_list": api_key_list
        }

        return user_extra_info

    def get_user_api_key_list(self, user_id: int) -> List[Dict]:
        """
        获取用户的api_key列表
        :param user_id: 用户id
        :return:
        """
        api_key_list = self._user_dao.get_user_api_key_list(user_id=user_id)

        return api_key_list
