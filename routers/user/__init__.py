# coding=utf-8

from fastapi import APIRouter, Depends

from routers.user import user_api
from utils.dependencies import check_access_token

router = APIRouter()


router.add_api_route(
    '/info',
    user_api.get_user_info,
    methods=['get'],
    dependencies=[Depends(check_access_token)],
    summary='获取用户信息',
    description="通过访问令牌获取用户信息"
)


router.add_api_route(
    '/verification_code',
    user_api.get_verification_code,
    methods=['get'],
    summary='获取码验证',
    description="通过手机号获取验证码"
)


router.add_api_route(
    '/verification_code',
    user_api.check_verification_code,
    methods=['post'],
    summary='校验验证码',
    description="提交对验证码的校验"
)
