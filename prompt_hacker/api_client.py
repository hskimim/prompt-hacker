from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

from prompt_hacker import constant
from prompt_hacker.interface import ChatBaseModel

load_dotenv(verbose=True)


class ModelClient(ChatBaseModel):
    def run(self, question: str, **kwargs) -> list[str]:
        input_ = constant.TEST_MSG_HISTORY + [
            ChatCompletionUserMessageParam(
                content=question,
                role="user",
            )
        ]

        response = OpenAI().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=input_,
            **kwargs,
        )

        return [
            choice.message.content
            for choice in response.choices
            if choice.message.content
        ]
