# coding=utf-8

from fastapi import APIRouter

from routers.task import task_api


router = APIRouter()


router.add_api_route(
    '/task',
    task_api.get_task,
    methods=['get'],
    summary='获取任务信息',
    description="通过任务id，获取任务信息"
)

router.add_api_route(
    '/task',
    task_api.create_task,
    methods=['post'],
    summary='创建任务',
    description="提交任务"
)

