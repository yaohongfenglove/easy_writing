# coding=utf-8

from fastapi import APIRouter

from routers.api_key import api_key_api


router = APIRouter()


router.add_api_route(
    '/',
    api_key_api.get_api_key,
    methods=['get'],
    summary='获取api_key',
    description="通过访问令牌获取api_key"
)
