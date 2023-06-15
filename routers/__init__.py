# coding=utf-8

from fastapi import APIRouter

from routers import task, user, src_content, aigc_content, prompt, api_key

api_router = APIRouter(
    # prefix="",
    # tags=None,  # 按tags进行分组，swagger划分
)


# AIGC任务模块路由
api_router.include_router(task.router, prefix='/v1/task', tags=['任务模块'])
# 用户模块路由
api_router.include_router(user.router, prefix='/v1/user', tags=['用户模块'])
# 源内容模块路由
api_router.include_router(src_content.router, prefix='/v1/src_content', tags=['源内容模块'])
# AIGC内容模块路由
api_router.include_router(aigc_content.router, prefix='/v1/aigc_content', tags=['AIGC内容模块'])
# prompt模版模块路由
api_router.include_router(prompt.router, prefix='/v1/prompt', tags=['prompt模版模块'])
# api_key模块路由
api_router.include_router(api_key.router, prefix='/v1/api_key', tags=['api_key模块'])
