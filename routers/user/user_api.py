from datetime import datetime
import datetime

from fastapi import Header
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.background import BackgroundTasks

from items.response import GenericResponse


from items.user import UserAccessToken
from logic.user import user_logic
from utils.constants import StatusCodeEnum
from utils.exceptions import UserQueryError, VerificationCodeError, RequestIsTooFrequentError, CustomHTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_verification_code(phone: str, background_tasks: BackgroundTasks):
    """
    获取验证码
    :param phone: 手机号
    :param background_tasks: 后台任务
    :return:
    """
    try:
        user_logic.get_verification_code(phone=phone, background_tasks=background_tasks)
        return GenericResponse(
            now=int(datetime.datetime.now().timestamp()),
            msg="验证码已发送"
        )
    except UserQueryError:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=StatusCodeEnum.USER_NOT_FOUND.code,
            msg=StatusCodeEnum.USER_NOT_FOUND.errmsg,
        )
    except RequestIsTooFrequentError:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code=StatusCodeEnum.REQUEST_IS_TOO_FREQUENT.code,
            msg=StatusCodeEnum.REQUEST_IS_TOO_FREQUENT.errmsg
        )


def check_verification_code(phone: str, verification_code: str, background_tasks: BackgroundTasks):
    """
    校验验证码
    :param phone: 手机号
    :param verification_code: 验证码
    :param background_tasks: 后台任务
    :return:
    """
    try:
        user = user_logic.check_verification_code(phone=phone, verification_code=verification_code)
        access_token = user_logic.get_access_token(user=UserAccessToken(**user), background_tasks=background_tasks)
        return GenericResponse(
            now=int(datetime.datetime.now().timestamp()),
            data={
                "user": {
                    "user_id": user["user_id"],
                    "access_token": access_token
                }
            }
        )
    except UserQueryError:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=StatusCodeEnum.USER_NOT_FOUND.code,
            msg=StatusCodeEnum.USER_NOT_FOUND.errmsg,
        )
    except VerificationCodeError:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code=StatusCodeEnum.VERIFICATION_CODE_ERR.code,
            msg=StatusCodeEnum.VERIFICATION_CODE_ERR.errmsg,
        )


def get_user_info(access_token: str = Header()):
    """
    根据访问令牌，获取用户信息
    :param access_token: 访问令牌
    :return:
    """
    user = user_logic.get_user_info(access_token=access_token)
    user_extra_info = user_logic.get_user_extra_info(user["user_id"])
    return GenericResponse(
        now=int(datetime.datetime.now().timestamp()),
        data={
            "user_id": user["user_id"],
            "city_list": user_extra_info.get("city_list"),
            "token_left": user_extra_info.get("token_left"),
            "expire_time": user_extra_info.get("expire_time"),
            "article_left": user_extra_info.get("article_left"),
        }
    )


def main():
    pass


if __name__ == '__main__':
    main()
