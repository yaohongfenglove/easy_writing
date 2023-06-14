import datetime

from db.mysql.user_dao import UserDAO


class UserService(object):
    """ 用户服务对象 """

    def __init__(self, phone="", verification_code="", *args, **kwargs):
        self._user_dao = UserDAO(phone, verification_code)
        super(UserService, self).__init__(*args, **kwargs)

    def get_user(self) -> dict:
        user = self._user_dao.get_user()
        return user
