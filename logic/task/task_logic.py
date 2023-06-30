import json
import warnings
from typing import List, Dict

from AesEverywhere import aes256

from conf.config import config
from service.task_service import TaskService
from service.user_service import UserService
from utils.constants import TASK_STATUS
from utils.exceptions import NoApiKeysAvailableError, InsufficientTokenLeftCreditError


def get_tasks(user_id: int, page: int, page_size: int) -> List[Dict]:
    """
    获取特定用户的任务列表
    :param user_id: 用户id
    :param page: 页码
    :param page_size: 每页多少条数据
    :return:
    """

    page_size = min(page_size, 40)  # 每页几条记录做最大限制

    task_service = TaskService()
    tasks = task_service.get_tasks(user_id=user_id, page=page, page_size=page_size)

    return tasks


def create_task1(user_id: int, city_id: int,
                 src_content_ids: List[int], client_version: str) -> Dict:
    """
    创建任务
    :param user_id: 用户id
    :param city_id: 城市id
    :param src_content_ids: 源内容id列表
    :param client_version: 客户端版本号
    :return:
    """
    warnings.warn("此函数已弃用，不推荐使用", DeprecationWarning)

    # 查询可用的api_key
    user_server = UserService()
    user_extra_info = user_server.get_user_extra_info(user_id=user_id)
    api_key_list = user_extra_info.get("api_key_list")
    if not api_key_list:
        raise NoApiKeysAvailableError("无可用的api_key了")
    api_key = api_key_list[0].get("api_key")
    api_base = api_key_list[0].get("api_base")

    # 创建任务
    task_service = TaskService()
    task_id = task_service.create_task(user_id=user_id, city_id=city_id,
                                       src_content_ids=src_content_ids, client_version=client_version)
    # 获取任务对应的详情列表
    task_info = task_service.get_task_pro_info(task_id=task_id)

    res = {
        "list": task_info,
        "api_key": aes256.encrypt(api_key, config["encrypt"]["SECRET_KEY_AES"]),
        "api_base": aes256.encrypt(api_base, config["encrypt"]["SECRET_KEY_AES"]),
        "task_id": task_id,
        "status": TASK_STATUS["waiting"],
    }

    return res


def create_task(user_id: int, city_id: int,
                src_content_ids: List[int], client_version: str) -> Dict:
    """
    创建任务
    :param user_id: 用户id
    :param city_id: 城市id
    :param src_content_ids: 源内容id列表
    :param client_version: 客户端版本号
    :return:
    """

    # 查询用户token余量
    user_service = UserService()
    user_token_left = user_service.get_user_token_left(user_id=user_id)
    if user_token_left <= 0:
        raise InsufficientTokenLeftCreditError("当前用户没有额度了")

    # 创建任务
    task_service = TaskService()
    task_id = task_service.create_task(user_id=user_id, city_id=city_id,
                                       src_content_ids=src_content_ids, client_version=client_version)
    # 获取任务对应的详情列表
    task_info: List[Dict] = task_service.get_task_pro_info(task_id=task_id)

    '''
    【代码块功能说明】
        功能：通过多重for循环，将每个prompt模版中的变量的“实际值”赋给相应的变量
    
        for task in task_info:  # 循环读取任务列表中的每个任务
        
        for prompt in prompts:  # 循环读取多轮对话中每轮的prompt
        
        for input_variable in input_variables:  # 循环读取每个prompt要替换哪些变量，并将变量实际的值赋给value变量
        
    '''
    for task in task_info:  # 循环读取任务列表中的任务
        prompts = json.loads(task["prompt"])  # 读取每个任务内容的prompt
        for prompt in prompts:
            input_variables = prompt.get("input_variables")  # 获取prompt中的输入变量
            for input_variable in input_variables:
                if input_variable["name"] == "title":
                    input_variable["value"] = task["title"]
                if input_variable["name"] == "contexts":
                    input_variable["value"] = task["content"]  # 取源内容中的相应的值给输入变量赋值
        task["prompt"] = prompts  # 将新拼成的prompt赋值给prompt变量

    res = {
        "list": task_info,
        "task_id": task_id,
        "status": 0,
    }

    return res


def get_task_base_info(task_id: int):
    """
    获取任务基础信息
    :param task_id: 任务id
    :return:
    """

    task_service = TaskService()
    task_info = task_service.get_task_base_info(task_id=task_id)

    return task_info


def update_task(task_id: int, status: int):
    """
    更新任务状态
    :param task_id: 任务id
    :param status: 任务状态值
    :return:
    """
    task_service = TaskService()
    task_service.update_task(task_id=task_id, status=status)
