"""
    prompt模板格式化后，再存入mysql中
"""

import json


def main():

    template = """你是一名专业的楼盘测评师，你会结合当年的市场情况，对相关楼盘做分析，要求不出现新闻来源，并且在文章不改变原意的基础上,原创度为65%，适当对文章进行缩写或者扩写，字数超过800字。将正文控制在900-1200字左右，写成3段，每段起一个小标题；每个小标题都需要加<p><strong></strong></p>标签；每段字数在300-400字左右；每个段落加<p></p>标签,以下是标题：
    {{ titles }}
    以下是内容：
    {{ contexts }}
    """

    prompts = [
        {
            "template": template,
            "input_variables": [
                {
                    "name": "titles",
                    "value": "xxx",
                    "replaced_string": "{{ titles }}"
                },
                {
                    "name": "contexts",
                    "value": "xxx",
                    "replaced_string": "{{ contexts }}"
                }
            ]
        },
        {
            "template": "",
            "input_variables": []
        },
        {
            "template": "",
            "input_variables": []
        }
    ]

    res = json.dumps(prompts, ensure_ascii=False)
    print(res)


if __name__ == '__main__':
    main()
