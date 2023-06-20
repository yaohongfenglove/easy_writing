# coding=utf-8

from fastapi import APIRouter, Depends

from routers.api_key import api_key_api
from utils.dependencies import check_access_token


router = APIRouter(
    dependencies=[Depends(check_access_token)]
)


router.add_api_route(
    '/',
    api_key_api.get_api_key,
    methods=['get'],
    summary='获取api_key',
    description="通过访问令牌获取api_key"
)
