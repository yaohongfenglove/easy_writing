
class UserService(object):
    def __init__(self, phone="", verification_code="", *args, **kwargs):
        self._user_dao = UserDAO(phone, verification_code)
        super(UserService, self).__init__(*args, **kwargs)
