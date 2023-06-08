# coding=utf-8

from fastapi import APIRouter

from routers import task


api_router = APIRouter(
    # prefix="",
    # tags=None,  # 按tags进行分组，swagger划分
)

# 任务模块路由
api_router.include_router(task.router, prefix='/v1/task', tags=['任务模块'])
