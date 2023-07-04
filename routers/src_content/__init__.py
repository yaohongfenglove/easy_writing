# coding=utf-8

from fastapi import APIRouter, Depends

from routers.src_content import src_content_api
from utils.dependencies import check_access_token

router = APIRouter(
    dependencies=[Depends(check_access_token)],
)


router.add_api_route(
    '/list/',
    src_content_api.get_src_content_list,
    methods=['get'],
    summary='获取源内容列表',
    description='通过限制条件获取源内容列表'
)

router.add_api_route(
    '/',
    src_content_api.get_src_content,
    methods=['get'],
    summary='获取源内容详情',
    description='通过源内容id获取源内容详情'
)
