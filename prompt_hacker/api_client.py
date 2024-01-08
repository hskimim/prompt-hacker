from dotenv import load_dotenv
import pandas as pd
from openai import OpenAI

from prompt_hacker.interface import ChatBaseModel
from prompt_hacker import constant

load_dotenv(True)


class ModelClient(ChatBaseModel):
    ...


class TestModelClient(ChatBaseModel):
    def run(self, question: str, **kwargs) -> list[str]:
        input_ = constant.TEST_MSG_HISTORY + [
            {
                "role": "user",
                "content": question,
            },
        ]

        response = OpenAI().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=input_,
            **kwargs,
        )
        return [choice.message.content for choice in response.choices]
