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

    def get_user_extra_info(self, user_id: int) -> Dict:
        """
        获取用户的其他额外信息
        :param user_id: 用户id
        :return:
        """
        city_list = self._user_dao.get_user_city_list(user_id=user_id)
        user_token_left = self._user_dao.get_user_token_left(user_id=user_id)
        user_extra_info = {
            "city_list": city_list,
            "user_token_left": user_token_left
        }

        return user_extra_info

    def get_user_token_left(self, user_id: int) -> int:
        """
        获取用户的token_left
        :param user_id: 用户id
        :return: token_left
        """
        token_left = self._user_dao.get_user_token_left(user_id=user_id)

        return token_left
