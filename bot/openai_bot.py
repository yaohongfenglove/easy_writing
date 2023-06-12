import os
import pickle
import traceback
from copy import deepcopy
from typing import List, Dict, Optional, Union

import openai
from tenacity import wait_random, retry, stop_after_attempt, RetryError


try:
    from conf.config import config, logger, BASE_DIR
except ModuleNotFoundError:
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 离开IDE也能正常导入自己定义的包
    from conf.config import config, logger, BASE_DIR


session_list: Dict[str, List[Dict]] = dict()


class OpenAIBot(object):
    def __init__(self, temperature=0.7, presence_penalty=0, frequency_penalty=0,
                 logit_bias: Optional[Dict[int, float]] = None,
                 session_id: str = None,
                 persist: bool = config["openai"]["persist_session"], persist_dir_path: str = os.path.join(BASE_DIR, "output")):
        """
        初始化
        :param temperature: 温度值，多样性控制
        :param session_id: 会话id，用于多轮对话
        :param persist: 是否持久化到硬盘
        :param persist_dir_path: 持久化路径
        """
        self.temperature = temperature  # 使用什么采样温度，介于 0 和 2 之间。较高的值（如 0.8）将使输出更加随机，而较低的值（如 0.2）将使其更加集中和确定。
        self.presence_penalty = presence_penalty  # 介于 -2.0 和 2.0 之间的数字。正值会根据新标记到目前为止是否出现在文本中来惩罚它们，从而增加模型讨论新主题的可能性。
        self.frequency_penalty = frequency_penalty  # 介于 -2.0 和 2.0 之间的数字。正值会根据新标记到目前为止在文本中的现有频率来惩罚新标记，从而降低模型逐字重复同一行的可能性。
        self.logit_bias = logit_bias  # 修改指定令牌出现在答复中的可能性。接受一个json对象，该对象将令牌（由令牌化器中的令牌ID指定）映射到-100到100之间的相关偏差值。从数学上讲，在采样之前，将偏差添加到模型生成的logits中。每个模型的确切效果会有所不同，但-1到1之间的值应该会降低或增加选择的可能性；像-100或100这样的值应该导致对相关令牌的禁止或独占选择。
        self.session_id = session_id
        self.persist = persist
        self.persist_dir_path = persist_dir_path

        if not os.path.isdir(self.persist_dir_path):
            os.makedirs(self.persist_dir_path)

        if config["openai"]["open_ai_proxy"]["enable"]:  # 使用第三方代理服务器
            openai.api_base = config["openai"]["open_ai_proxy"]["api_base"]
            openai.api_key = config["openai"]["open_ai_proxy"]["api_key"]
        elif config["local_proxy"]["enable"]:  # 使用本地代理
            openai.api_key = config["openai"]["api_key"]
            openai.proxy = {"http": f"{config['local_proxy']['host']}:{config['local_proxy']['port']}",
                            "https": f"{config['local_proxy']['host']}:{config['local_proxy']['port']}"}  # api被墙时，开启代理
        else:  # 无需翻墙
            openai.api_key = config["openai"]["api_key"]

    def reply(self, question: str, session_round: int = None):
        """
        获取回复
        :param question: 问题
        :param session_round: 会话轮次
        :return:
        """
        if self.persist and (not session_round):
            logger.warning(f"persist为true，且session_round不为None，才会进行持久化！")

        question = question.strip()
        logger.info("[OPEN_AI QUERY] session_id={}, question={}".format(self.session_id, question))

        messages = Session.build_session_query(question, self.session_id)

        try:
            # 步骤1：先从硬盘中加载
            if self.persist and session_round:
                answer = self.load_reply(session_round=session_round)
                logger.info(f"[LOCAL REPLY] 从硬盘中加载到的回复：{answer}")
            else:
                answer = ""

            # 步骤2：硬盘中加载不到时，才发起请求
            if not answer:
                logger.info(f"生成响应中...")
                answer = self.reply_text(messages=messages)
                logger.info("[OPEN_AI REPLY] session_id={}, answer={}".format(self.session_id, answer))
                if self.persist and session_round:
                    self.dump_reply(session_round=session_round, question=question, answer=answer)

            # 有会话id时，才需要存储会话，否则认为是单轮对话
            if self.session_id and question and answer:
                Session.save_session(question, answer, self.session_id)
            return answer
        except RetryError:
            error_str = traceback.format_exc()
            logger.error(error_str)

    # TODO 2023-5-17 根据目前的测试结果，logit_bias参数貌似在openai.ChatCompletion中无效，在openai.Completion有效，已反馈至github作者
    @retry(wait=wait_random(min=config["openai"]["openai_retry"]["min_wait"], max=config["openai"]["openai_retry"]["max_wait"]),
           stop=stop_after_attempt(config["openai"]["openai_retry"]["max_attempt_number"]))
    def reply_text(self, messages: List):
        response = openai.ChatCompletion.create(
            model=config["openai"]["open_ai_chat_model"],  # 对话模型的名称
            messages=messages,
            temperature=self.temperature,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
            logit_bias=self.logit_bias
        )
        response_content = response['choices'][0]['message']['content']
        return response_content

    def load_reply(self, session_round: int):
        """
        加载本地回复
        :param session_round: 会话轮次
        :return:
        """
        pkl_path = os.path.join(self.persist_dir_path, f"{self.session_id}.pkl")
        if not os.path.exists(pkl_path):
            reply = ""
        else:
            with open(pkl_path, 'rb') as f:
                session: Dict = pickle.load(f, encoding='bytes')
            session_round = session.get(session_round)
            if session_round:
                reply = session_round.get("assistant")
            else:
                reply = ""
        return reply

    def dump_reply(self, session_round: int, question: str, answer: str):
        """
        将回复持久化到本地
        :param session_round: 会话轮次
        :param question: 问题
        :param answer: 答复
        :return:
        """

        pkl_path = os.path.join(self.persist_dir_path, f"{self.session_id}.pkl")
        if not os.path.exists(pkl_path):
            session = dict()
        else:
            with open(pkl_path, 'rb') as f:
                session: Dict = pickle.load(f, encoding='bytes')

        session.update({session_round: {"user": question, "assistant": answer}})
        with open(pkl_path, 'wb') as f:
            pickle.dump(session, f)

        return session

    @retry(wait=wait_random(min=config["openai"]["openai_retry"]["min_wait"], max=config["openai"]["openai_retry"]["max_wait"]),
           stop=stop_after_attempt(config["openai"]["openai_retry"]["max_attempt_number"]))
    def embeddings(self, text_list: List[str]) -> List[Union[float, List[float]]]:
        """
        将文本向量化
        :param text_list: 要向量化的文本列表
        :return:
        """
        embeddings = openai.Embedding.create(
            model=config["openai"]["open_ai_embedding_model"],
            input=text_list
        )

        vectors = [item["embedding"] for item in embeddings["data"]]

        return vectors


class Session(object):
    global session_list

    @staticmethod
    def build_session_query(question, session_id):
        """
        结合历史会话，生成查询内容
        :param question: 查询的问题
        :param session_id: 会话id，区分不同会话
        :return: 含历史会话记录的查询内容
        """

        open_ai_system_prompt: List = config["openai"]["open_ai_system_prompt"]
        session: List = session_list.get(session_id, [])

        session_query: List = deepcopy(open_ai_system_prompt)

        # 添加历史会话记录
        if session:
            for conversation in session:
                session_query.append({"role": "user", "content": f"{conversation['question']}"})
                session_query.append({"role": "assistant", "content": f"{conversation['answer']}"})

        session_query.append({"role": "user", "content": f"{question}"})
        return session_query

    @staticmethod
    def save_session(question, answer, user_id):

        max_tokens = config.get("session_max_tokens")
        if not max_tokens:
            max_tokens = 4096
        conversation = dict()
        conversation["question"] = question
        conversation["answer"] = answer
        session = session_list.get(user_id)

        if session:
            session.append(conversation)
        else:
            # create session
            session_list[user_id] = [conversation]

        # discard exceed limit conversation
        Session.discard_exceed_conversation(session_list[user_id], max_tokens)

    @staticmethod
    def discard_exceed_conversation(session, max_tokens):
        count = 0
        count_list = list()
        for i in range(len(session)-1, -1, -1):
            # count tokens of conversation list
            history_conv = session[i]
            count += len(history_conv["question"]) + len(history_conv["answer"])
            count_list.append(count)

        for c in count_list:
            if c > max_tokens:
                # pop first conversation
                session.pop(0)

    @staticmethod
    def clear_session(user_id):
        session_list[user_id] = []


def main():
    # 多轮会话测试
    # openai_bot = OpenAIBot(session_id="1003")
    #
    # answer1 = openai_bot.reply(question="1+2的结果？", session_round=1)
    # print(answer1)
    #
    # answer2 = openai_bot.reply(question="确定吗？不是等于5吗？", session_round=2)
    # print(answer2)

    # 文本向量化
    openai_bot = OpenAIBot()
    # res = openai_bot.embeddings(text_list=["red", "Red"])
    res = openai_bot.embeddings(text_list=["成都买第二套房现在的政策是怎样的", "上海二手房首付比例"])
    print(res)


if __name__ == '__main__':
    main()
