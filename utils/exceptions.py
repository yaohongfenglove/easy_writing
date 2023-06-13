"""
    自定义异常
"""


class TaskCreateError(Exception):
    def __init__(self, message: str):
        self.message = message


class UserQueryError(Exception):
    """ 用户查询错误 """


class VerificationCodeError(Exception):
    """ 验证码校验错误 """
    ...


class DecodePhoneNumberError(Exception):
    """ 解码手机号错误 """
    ...


class UserRegisterError(Exception):
    """ 用户注册错误 """
    ...


class RequestIsTooFrequentError(Exception):
    """
    请求过于频繁异常
    """