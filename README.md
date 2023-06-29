# 简介

> 基于LLM的写作系统-后台
>
当前计划实现的功能如下：

- [x] **基于openai-gpt的能力，对文章进行批量化改写**
- [ ] **基于openai-gpt的能力，输出原创文章**

![](example/example.png)


# 快速开始

### 一.运行环境

支持各主流操作系统

先安装 `Python`
> 建议Python版本3.8.x，尤其是需要进行exe打包时（3.8为win7上可运行的最后一个python版本）。

创建虚拟环境并激活后，安装所需核心依赖：

```bash
pyhon -m venv venv
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 二.相关配置
```bash
# config.json文件内容示例
{
  "milvus": {  # milvus链接方式
    "debug": {
      "host": "xxx",
      "port": 19530,
      "user": "xxx",
      "passwd": "xxx"
    },
    "production": {
      "host": "xxx",
      "port": 19530,
      "user": "xxx",
      "passwd": "xxx"
    }
  },
  "mysql": {  # mysql链接方式
    "debug": {
      "user": "xxx",
      "password": "xxx",
      "host": "xxx",
      "port": 3306,
      "database": "easy_writing",
      "charset": "utf8mb4"
    },
    "production": {
      "user": "xxx",
      "password": "xxx",
      "host": "xxx",
      "port": 3306,
      "database": "easy_writing",
      "charset": "utf8mb4"
    }
  },
  "openai": {  # openai参数
    "open_ai_proxy": {  # 第三方代理厂商，免翻墙访问openai
      "enable": true,
      "api_base": "https://xxx/v1",
      "api_key": "xxx"
    },
    "api_key": "sk-xxx",
    "open_ai_chat_model": "gpt-3.5-turbo",
    "open_ai_embedding_model": "text-embedding-ada-002",
    "openai_retry": {  # openai接口调用失败时的重试机制
      "min_wait": 3,
      "max_wait": 5,
      "max_attempt_number": 3
    },
    "open_ai_system_prompt": [
      {
        "role": "system",
        "content": "你是个乐于助人的助手。"
      }
  ],
    "persist_session": false,
    "tokens_use_per_article": 7000  # 每篇文章预计所需消耗的token数量
  },
  "local_proxy": {
    "enable": true,
    "host": "127.0.0.1",
    "port": 10809,
    "port_socket": 10808
  },
  "redis": {  # redis链接方式
    "debug": {
      "host": "127.0.0.1",
      "port": 6379,
      "db": 10,
      "password": "xxx"
    },
    "production": {
      "host": "xxx",
      "port": 6379,
      "db": 10,
      "password": "xxx"
    }
  },
  "tencent": {  # 腾讯云账户，发送短信相关
    "sms": {
      "SECRET_ID" : "xxxxx",
      "SECRET_KEY" : "xxxxx",
      "SDK_APP_ID" : "xxxxx",
      "SIGN_NAME" : "xxxxx",
      "TEMPLATE_ID" : "xxxxx",
      "VERIFICATION_CODE_EXPIRE_MINUTES" : 5,  # 验证码过期时间（分钟）
      "VERIFICATION_CODE_SEND_FREQUENCY" : 1   # 验证码发送频率限制（分钟）
    }
  },
  "access_token": {  # 前后端通讯用的令牌生成参数
    "SECRET_KEY" : "xxxxx",
    "RSA_PRIVATE_KEY" : "xxxxx",
    "ALGORITHM" : "xxx",
    "EXPIRE_SECONDS" : 8640000  # 访问令牌过期时间
  },
  "encrypt": {
    "SECRET_KEY_AES": "xxx"  # api_key对称加密用的秘钥
  }
}
```

### 三.运行
**本地运行，** 直接在项目根目录下执行：
```bash
cd 项目根目录
venv\script\activate
python main.py
```
**线上（极简模式）：** 
```bash
cd 项目根目录
vim conf/config.py (update DEBUG = False)
source venv/bin/activate
nohup python main.py >> ./out.log 2>&1 & echo $! > ./pidfile
```

### 四.运行结果示例
![](example/example.png)
