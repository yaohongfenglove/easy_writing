# coding=utf-8

import uvicorn
from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

try:
    from conf.config import DEBUG
    from routers import api_router
    from utils.exceptions import CustomHTTPException
except ModuleNotFoundError:
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 离开IDE也能正常导入自己定义的包
    from conf.config import DEBUG
    from routers import api_router
    from utils.exceptions import CustomHTTPException


def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.staticfile.org/swagger-ui/4.15.5/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdn.staticfile.org/swagger-ui/4.15.5/swagger-ui.min.css")


if DEBUG:
    # 解决fastapi的swagger的js和css文件所在服务器国内被墙的问题
    applications.get_swagger_ui_html = swagger_monkey_patch


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
