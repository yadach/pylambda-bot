import json
import logging

import openai

from pylambda_bot.nlp_engines.base import BaseNLPEngine

logger = logging.getLogger(__name__)

INITIAL_PROMPT_EXAMPLE = """
あなたは料理研究家です。
以下の制約条件をもとに、ユーザーからの質問に答える、もしくは指示に従ってください。
# 制約条件
- あなたの名前はクック先生です
- 句読点をできるだけ多く含む返答を返してください
- ユーザーが食材を指定した場合、その食材を使用した料理のレシピをステップ順に教えて下さい
- ユーザーが料理名を指定した場合、そのその料理のレシピをステップ順に教えて下さい
- ユーザーから食材や料理名の指定がない場合は、おすすめのレシピを提案し調理手順を教えて下さい
- ユーザーの指示が不明確な場合は、聞き返してください
"""


class OpenAI(BaseNLPEngine):
    def __init__(
        self,
        params={
            "model": "gpt-3.5-turbo",
            "n": 1,
            "max_tokens": 512,
        },  # https://platform.openai.com/docs/api-reference/chat/create
        initial_prompts=None,
        num_max_retry: int = 3,
    ) -> None:
        self.gpt_params = params
        if initial_prompts is None:
            initial_prompts = INITIAL_PROMPT_EXAMPLE
        self.init_msg = [
            {"role": "system", "content": initial_prompts},
        ]
        self.messages = [
            {"role": "system", "content": initial_prompts},
        ]
        self.num_max_retry = num_max_retry

    def get_reply(self, input_text: str, conv_hist: list = []):
        """Generate response by GPT-3.

        Args:
            input_text (str): Prompt text.
            conv_hist (list): List of conversation histories.

        Returns:
            str: Response text.
        """
        self.messages += conv_hist
        self.messages += [{"role": "user", "content": input_text}]

        for i in range(self.num_max_retry):
            logger.debug(f"[To OpenAI take{i + 1}] messages({len(self.messages)}): {self.messages}")
            try:
                response = openai.ChatCompletion.create(
                    messages=self.messages,
                    stream=False,
                    **self.gpt_params,
                )
                break
            except openai.error.InvalidRequestError:
                self.messages = self.init_msg + self.messages[-len(self.messages) // 2 :]
                logger.warning(f"Reduce the number of messages to be sent. -> {len(self.messages)}")

        full_response = response.choices[0]["message"]["content"]
        logger.debug(f"[From OpenAI] response: {json.dumps(full_response, ensure_ascii=False)}")
        return full_response
