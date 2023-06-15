# coding=utf-8

from fastapi import APIRouter, Depends

from routers.aigc_content import aigc_content_api
from utils.dependencies import check_access_token

router = APIRouter(
    dependencies=[Depends(check_access_token)]
)


router.add_api_route(
    '/',
    aigc_content_api.update_aigc_content,
    methods=['put'],
    summary='更新AIGC内容详情',
    description="通过内容id，更新AIGC内容详情"
)


router.add_api_route(
    '/',
    aigc_content_api.get_aigc_content,
    methods=['get'],
    summary='获取AIGC内容详情',
    description="通过内容id，获取AIGC内容详情"
)
