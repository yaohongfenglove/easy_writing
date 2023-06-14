# coding=utf-8

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from routers import api_router
from utils.exceptions import CustomHTTPException

try:
    from conf.config import DEBUG
except ModuleNotFoundError:
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 离开IDE也能正常导入自己定义的包
    from conf.config import DEBUG


if DEBUG:
    app = FastAPI(
        title="LLM写作系统-后台服务",
        description="""
          功能列表：
            - 文章改写
            - 
        """,
        version="1.0.0.0"
    )
else:
    app = FastAPI(
        title="LLM写作系统-后台服务",
        description="""
          功能列表：
            - 文章改写
            - 
        """,
        version="1.0.0.0",
        docs_url=None,
        redoc_url=None
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(CustomHTTPException)
async def custom_exception_handler(request: Request, exc: CustomHTTPException):
    """ 处理程序抛出的自定义异常 """
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "msg": exc.msg},
    )


@app.on_event('startup')
def startup_event():
    """ 项目启动时准备环境 """

    # 加载路由
    app.include_router(api_router, prefix='/api')


def main():
    if DEBUG:
        uvicorn.run(app="main:app", host="0.0.0.0", port=9088, reload=True)
    else:
        uvicorn.run(app="main:app", host="127.0.0.1", port=9088, reload=False, workers=4)


if __name__ == '__main__':
    main()
