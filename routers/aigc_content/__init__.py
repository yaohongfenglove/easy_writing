# coding=utf-8

from fastapi import APIRouter, Depends

from routers.aigc_content import aigc_content_api
from utils.dependencies import verify_access_token


router = APIRouter(
    dependencies=[Depends(verify_access_token)]
)


router.add_api_route(
    '/',
    aigc_content_api.update_aigc_content,
    methods=['put'],
    summary='更新AIGC内容详情',
    description="通过内容id，更新AIGC内容详情"
)
