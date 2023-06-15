# coding=utf-8

from fastapi import APIRouter

from routers.task import task_api


router = APIRouter()


router.add_api_route(
    '/list/',
    task_api.get_tasks,
    methods=['get'],
    summary='获取任务列表',
    description="通过用户id，获取任务列表"
)


router.add_api_route(
    '/',
    task_api.create_task,
    methods=['post'],
    summary='创建任务',
    description="提交任务"
)


router.add_api_route(
    '/',
    task_api.get_task_base_info,
    methods=['get'],
    summary='获取任务基础信息',
    description="通过任务id，获取任务基础信息"
)
