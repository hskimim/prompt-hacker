from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from prompt_hacker import constant
from prompt_hacker.interface import ChatBaseModel

load_dotenv(verbose=True)


# make a arbitrary chatbot model
class TestModelClient(ChatBaseModel):
    def __init__(self) -> None:
        self._client = OpenAI()

    def run(self, question: str, **kwargs) -> list[str]:
        input_: list[ChatCompletionMessageParam] = [
            {"role": "user", "content": question}
        ]
        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.9,
            messages=input_,
            **kwargs,
        )

        msg = response.choices[0].message.content
        if isinstance(msg, str):
            return [msg]
        else:
            raise ValueError


class FewShotTestModelClient(ChatBaseModel):
    def run(self, question: str, **kwargs) -> list[str]:
        input_ = constant.TEST_MSG_HISTORY + [
            ChatCompletionUserMessageParam(
                content=question,
                role="user",
            )
        ]

        response = OpenAI().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=input_,  # type: ignore
            **kwargs,
        )

        return [
            choice.message.content
            for choice in response.choices
            if choice.message.content
        ]


class InstructedShotTestModelClient(ChatBaseModel):
    def __init__(self, instruct) -> None:
        super().__init__()
        self.instruct = instruct

    def run(self, question: str, **kwargs) -> list[str]:
        input_ = [
            ChatCompletionSystemMessageParam(
                content=self.instruct,
                role="system",
            ),
            ChatCompletionUserMessageParam(
                content=question,
                role="user",
            ),
        ]

        response = OpenAI().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=input_,  # type: ignore
            **kwargs,
        )

        return [
            choice.message.content
            for choice in response.choices
            if choice.message.content
        ]
