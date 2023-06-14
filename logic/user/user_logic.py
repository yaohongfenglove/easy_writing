import datetime
import random
from typing import Dict

from jose import jwt
from starlette.background import BackgroundTasks

from api.tencent import send_sms_verification_code
from conf.config import config
from db.redis_db import redis_pool
from items.access_token import AccessTokenInfo
from items.user import UserAccessToken
from service.user_service import UserService
from utils.exceptions import RequestIsTooFrequentError, UserQueryError, VerificationCodeError


class Verify(object):
    """ 校验类 """

    def __init__(self, phone="", verification_code="", access_token="", *args, **kwargs):
        self.phone = phone
        self.verification_code = verification_code
        self.access_token = access_token
        super(Verify, self).__init__(*args, **kwargs)

    def get_verification_code(self, background_tasks) -> str:
        """
        获取验证码
        :param background_tasks: 后台任务
        :return:
        """
        redis_conn = redis_pool.get_conn()

        #  防止用户频繁点击验证码
        verification_code_send_flag_key = f"verification_code:send_flag:{self.phone}"  # 验证码是否已发送标志
        has_send = redis_conn.get(verification_code_send_flag_key)
        if has_send:
            verification_code_send_frequency = config['tencent']['sms']['VERIFICATION_CODE_SEND_FREQUENCY']
            raise RequestIsTooFrequentError(f"发送太频繁了，请{verification_code_send_frequency}分钟重试")
        else:
            background_tasks.add_task(self.redis_set_value, verification_code_send_flag_key, 1,
                                      config['tencent']['sms']['VERIFICATION_CODE_SEND_FREQUENCY'] * 60)

        # 生成验证码
        verification_code = self.generate_verification_code()
        verification_code_key = f"verification_code:login:{self.phone}"
        background_tasks.add_task(send_sms_verification_code, self.phone,
                                  verification_code, config['tencent']['sms']['VERIFICATION_CODE_EXPIRE_MINUTES'])
        background_tasks.add_task(self.redis_set_value, verification_code_key, verification_code,
                                  config['tencent']['sms']['VERIFICATION_CODE_EXPIRE_MINUTES']*60)
        return verification_code

    def verify_verification_code(self):
        redis_conn = redis_pool.get_conn()

        verification_code_key = f"verification_code:login:{self.phone}"
        verification_code = redis_conn.get(verification_code_key)
        if not verification_code:
            raise VerificationCodeError("验证码错误")

        if self.verification_code != verification_code:
            raise VerificationCodeError("验证码错误")

    @staticmethod
    def generate_verification_code() -> str:
        """
        生成验证码
        :return: 6为随机数字码
        """
        verification_code = random.randint(100300, 999998)
        return str(verification_code)

    def get_access_token(self, user_id: int, phone: str, background_tasks: BackgroundTasks) -> str:
        """
        获取访问令牌
        :param user_id: 用户id
        :param phone: 手机号
        :param background_tasks: 后台任务
        :return: access_token
        """
        redis_conn = redis_pool.get_conn()
        access_token_key = f'access_token:{phone}'
        access_token = redis_conn.get(access_token_key)

        if not access_token:
            access_token_info = AccessTokenInfo(user_id=user_id, phone=phone)
            access_token = Verify.generate_access_token(access_token_info)

        redis_conn.expire(name=access_token_key, time=config['access_token']['EXPIRE_SECONDS'])  # 刷新access_token的过期时间
        background_tasks.add_task(self.redis_set_value, access_token_key, access_token,
                                  config['access_token']['EXPIRE_SECONDS'])
        return access_token

    @staticmethod
    def generate_access_token(access_token_info: AccessTokenInfo):
        """
        生成访问令牌
        :param access_token_info: 需要进行JWT令牌加密的数据（解密的时候会用到）
        :return:
        """
        access_token_info = access_token_info.dict()

        # 添加失效时间
        expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=config["access_token"]["EXPIRE_SECONDS"])
        access_token_info.update({"exp": expiration})

        encoded_jwt = jwt.encode(access_token_info, config['access_token']['SECRET_KEY'], config['access_token']['ALGORITHM'])
        return encoded_jwt

    @staticmethod
    def redis_set_value(key, value, expiration):
        redis_conn = redis_pool.get_conn()
        redis_conn.set(key, value, expiration)
        return None


def get_verification_code(phone: str, background_tasks: BackgroundTasks):
    """
    获取验证码
    :param phone: 手机号
    :param background_tasks: 后台任务
    :return:
    """
    user_server = UserService(phone=phone)
    user = user_server.get_user()
    if not user:
        raise UserQueryError("用户不存在")

    verify_obj = Verify(phone)
    verify_obj.get_verification_code(background_tasks)


def check_verification_code(phone: str, verification_code: str) -> Dict:
    user_server = UserService(phone=phone)
    user = user_server.get_user()
    if not user:
        raise UserQueryError("用户不存在")

    verify_obj = Verify(phone=phone, verification_code=verification_code)
    verify_obj.verify_verification_code()

    return user


def get_access_token(user: UserAccessToken, background_tasks: BackgroundTasks) -> str:
    """
    获取访问令牌
    :param user: 用户对象
        :param background_tasks: 后台任务
    :return:
    """
    verify_obj = Verify()
    access_token = verify_obj.get_access_token(user_id=user.user_id, phone=user.phone,
                                               background_tasks=background_tasks)

    return access_token


def get_user_info(access_token: str) -> Dict:
    """
    获取用户信息
    :param access_token: 访问令牌
    :return:
    """
    payload = jwt.decode(access_token, config['access_token']['SECRET_KEY'], algorithms=[config['access_token']['ALGORITHM']])
    phone = payload.get("phone")

    user_server = UserService(phone=phone)
    user = user_server.get_user()
    if not user:
        raise UserQueryError("用户不存在")

    return user
