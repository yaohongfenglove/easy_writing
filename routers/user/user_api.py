from datetime import datetime

from items.response import GenericResponse


import logging
import random


from conf.config import config
from db.redis_db import redis_pool
from api.tencent import send_sms_verification_code
from service.user_service import UserService


class RequestIsTooFrequentError(Exception):
    """
    请求过于频繁异常
    """


class LoginView(object):

    def __init__(self, phone="", verification_code="", login_token="", *args, **kwargs):
        self.phone = phone
        self.verification_code = verification_code
        self.login_token = login_token
        self._user_service = UserService(phone, verification_code)
        super(LoginView, self).__init__(*args, **kwargs)

    def generate_verification_code(self):
        """
        生成验证码
        :return: 6为随机数字码
        """
        verification_code = random.randint(100300, 999998)
        return verification_code

    def get_verification_code(self, phone: str, background_tasks):
        """
        获取验证码
        :param phone: 用户电话
        :param background_tasks: 后台任务
        :return:
        """

        #  防止用户频繁点击验证码
        redis_conn = redis_pool.get_conn()
        verification_code_send_flag_key = f"verification_code:send_flag:{phone}"
        res = redis_conn.get(verification_code_send_flag_key)
        if res:
            raise RequestIsTooFrequentError(f"The request is too frequent."
                                            f" Please try again in "
                                            f"{config['tencent']['sms']['VERIFICATION_CODE_SEND_FREQUENCY'] * 60} seconds")
        else:
            background_tasks.add_task(self.redis_set_value, verification_code_send_flag_key, 1,
                                      config['tencent']['sms']['VERIFICATION_CODE_SEND_FREQUENCY'] * 60)
        verification_code = self.generate_verification_code()
        verification_code_key = f"verification_code:login:{phone}"
        background_tasks.add_task(send_sms_verification_code, phone,
                                  verification_code, config['tencent']['sms']['VERIFICATION_CODE_EXPIRE_MINUTES'])
        background_tasks.add_task(self.redis_set_value, verification_code_key, verification_code,
                                  config['tencent']['sms']['VERIFICATION_CODE_EXPIRE_MINUTES'] * 60)
        return verification_code

    @staticmethod
    def redis_set_value(self, key, value, expiration):
        redis_conn = redis_pool.get_conn()
        redis_conn.set(key, value, expiration)
        return None


def get_user(access_token: str):
    """
    根据手机号，获取用户信息
    :param access_token: 访问令牌
    :return:
    """
    return GenericResponse(
        now=int(datetime.now().timestamp()),
        data={
            "user_id": 1,
            "city_list": [
                {
                    "city_id": 12,
                    "city_name": "深圳"
                },
                {
                    "city_id": 10,
                    "city_name": "北京"
                }
            ],
            "token_left": 84,
            "expire_time": "1974-07-24 15:35:02",
            "access_key_id": 69,
            "article_left": 92
        }
    )


def get_verification_code(phone: int):
    """
    获取验证码
    :param phone: 手机号
    :return:
    """
    return GenericResponse(
        now=int(datetime.now().timestamp()),
        data={
        }
    )


def check_verification_code(phone: int, verification_code: int):
    """
    校验验证码
    :param phone: 手机号
    :param verification_code: 验证码
    :return:
    """
    return GenericResponse(
        now=int(datetime.now().timestamp()),
        data={
            "user_id": 1,
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IjE1OTE1MzExNDUzIi"
                            "wiZXhwIjoxNjk4MzExMjMxfQ.H_WEhTvEB8GVtbaa8UGPuorVz_Gr98bqdzxal28pJYc",
            "expiration": 8640000
        }
    )


if __name__ == '__main__':
    phone_number = "18649930703"
    verification = get_verification_code(phone=phone_number)
    logging.info(verification)
