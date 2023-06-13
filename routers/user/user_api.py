from datetime import datetime
import datetime
from typing import Union

from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.background import BackgroundTasks

from items.response import GenericResponse
from jose import jwt, JWTError

import logging
import random


from conf.config import config
from db.redis_db import redis_pool
from api.tencent import send_sms_verification_code
from service.user_service import UserService
from utils.constants import StatusCodeEnum
from utils.exceptions import UserQueryError, VerificationCodeError, DecodePhoneNumberError, UserRegisterError, \
    RequestIsTooFrequentError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LoginView(object):

    def __init__(self, phone='', verification_code="", access_token="", *args, **kwargs):
        self.phone = phone
        self.verification_code = verification_code
        self.access_token = access_token
        self._user_service = UserService(phone, verification_code)
        super(LoginView, self).__init__(*args, **kwargs)

    def get_user(self) -> dict:
        """
        获取用户信息
        :return: User对象
        """

        user = self._user_service.get_user()
        return user

    def check_user(self, phone: str, verification_code: str) -> dict:
        """
        校验用户
        :param phone: 用户电话
        :param verification_code: 验证码
        :return: User对象
        """
        user = self.get_user()
        if not user:
            raise UserQueryError("User not found")

        passed = self.verify_verification_code()
        if not passed:
            raise VerificationCodeError("Verification code error, check user failed")

        return user

    def verify_verification_code(self):
        redis_conn = redis_pool.get_conn()

        if not self.verification_code:
            return False

        verification_code_key = f"verification_code:login:{self.phone}"
        verification_code = redis_conn.get(verification_code_key)
        if not verification_code:
            return False

        if self.verification_code != verification_code:
            return False
        else:
            return True

    @staticmethod
    def generate_verification_code() -> int:
        """
        生成验证码
        :return: 6为随机数字码
        """
        verification_code = random.randint(100300, 999998)
        return verification_code

    def get_verification_code(self, phone: str, background_tasks) -> int:
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

    def get_access_token(self, user_id: int, phone: int, background_tasks: BackgroundTasks) -> str:
        """
        获取访问令牌
        :param user_id: 用户id
        :param phone: 用户名
        :param background_tasks: 后台任务
        :return: access_token
        """
        redis_conn = redis_pool.get_conn()
        access_token_key = f'access_token:{phone}'
        access_token = redis_conn.get(access_token_key)
        if not access_token:
            access_token = self.create_access_token(data={"user_id": user_id, "phone": phone})
        redis_conn.expire(name=access_token, time=config['access_token']['EXPIRE_SECONDS'])  # 刷新access_token的过期时间
        background_tasks.add_task(self.redis_set_value, access_token_key, access_token,
                                  config['access_token']['EXPIRE_SECONDS'])
        return access_token

    @staticmethod
    def create_access_token(data: dict):
        """
        生成访问令牌
        :param data: 需要进行JWT令牌加密的数据（解密的时候会用到）
        :return:
        """

        # 添加失效时间
        to_encode = data.copy()
        expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=config['access_token']['EXPIRE_SECONDS'])
        to_encode.update({"exp": expiration})

        encoded_jwt = jwt.encode(to_encode, config['access_token']['SECRET_KEY'], config['access_token']['ALGORITHM'])

        return encoded_jwt

    @staticmethod
    def redis_set_value(self, key, value, expiration):
        redis_conn = redis_pool.get_conn()
        redis_conn.set(key, value, expiration)
        return None


def verify_access_token(access_token: Union[str, None] = Header(default=None)):
    """
    校验令牌是否有效
    :param access_token: 访问令牌
    """
    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'],
                         algorithms=[config['access_token']['ALGORITHM']])
    username = payload.get("username")

    redis_conn = redis_pool.get_conn()
    access_token_key = f'access_token:{username}'
    access_token_in_redis = redis_conn.get(access_token_key)

    if access_token_in_redis == access_token:
        return access_token
    else:
        return None


def get_verification_code(phone: str, background_tasks: BackgroundTasks):
    """
    获取验证码
    :param phone: 手机号
    :param background_tasks:
    :return:
    """
    login_obj = LoginView(phone)
    user = get_user(phone)
    if not user:
        raise UserRegisterError("User does not exist")
    else:
        try:
            login_obj.get_verification_code(phone, background_tasks)
            return GenericResponse(
                now=int(datetime.datetime.now().timestamp()),
            )
        except RequestIsTooFrequentError:
            return GenericResponse(
                now=int(datetime.datetime.now().timestamp()),
                sub_code=StatusCodeEnum.REQUEST_IS_TOO_FREQUENT.code,
                sub_msg=StatusCodeEnum.REQUEST_IS_TOO_FREQUENT.errmsg
            )


def check_verification_code(phone: str, verification_code: str, background_tasks: BackgroundTasks):
    """
    校验验证码
    :param phone: 手机号
    :param verification_code: 验证码
    :param background_tasks:
    :return:
    """
    login_obj = LoginView(phone, verification_code)
    try:
            user = login_obj.get_user()
            user_check = login_obj.check_user(phone, verification_code)
            access_token = login_obj.get_access_token(user["user_id"], user["username"], background_tasks)
            user.update({"access_token": access_token, "expiration": config['access_token']['EXPIRE_SECONDS']})
            return GenericResponse(
                now=int(datetime.datetime.now().timestamp()),
                data={
                    "user_id": 1,
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IjE1OTE1Mz"
                                    "ExNDUzIiwiZXhwIjoxNjk4MzExMjMxfQ.H_WEhTvEB8GVtbaa8UGPuorVz_Gr98bqdzxal28pJYc",
                    "expiration": 8640000
                }
            )
    except UserQueryError:
        return GenericResponse(
            sub_code=status.HTTP_404_NOT_FOUND,
            sub_msg="User not found",
            now=int(datetime.datetime.now().timestamp()),
            data={
                "user": {}
            }
        )
    except VerificationCodeError:
        return GenericResponse(
            sub_code=status.HTTP_400_BAD_REQUEST,
            sub_msg="Verification code error",
            now=int(datetime.datetime.now().timestamp()),
            data={
                "user": {}
            }
        )


def get_user(access_token: str = Depends(verify_access_token)):
    """
    根据访问令牌，获取用户信息
    :param access_token: 访问令牌
    :return:
    """
    if not access_token:
        return GenericResponse(
            sub_code=status.HTTP_401_UNAUTHORIZED,
            sub_msg="Access token expired error",
            now=int(datetime.datetime.now().timestamp()),
            data={}
        )
    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'],
                         algorithms=[config['access_token']['ALGORITHM']])
    phone = payload.get("phone")
    login_obj = LoginView(phone)
    user = login_obj.get_user()
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


def main():
    login_obj = LoginView(phone="13413617619", verification_code="")
    print(login_obj.get_user())


if __name__ == '__main__':
    main()
