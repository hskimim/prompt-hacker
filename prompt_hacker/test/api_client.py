import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from prompt_hacker.interface import ChatBaseModel

load_dotenv(verbose=True)


# make a arbitrary chatbot model
class TestModelClient(ChatBaseModel):
    def __init__(self) -> None:
        self._client = OpenAI()
        self._async_client = AsyncOpenAI()

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

    async def _async_call(self, question: str, **kwargs) -> list[str]:
        input_: list[ChatCompletionMessageParam] = [
            {"role": "user", "content": question}
        ]
        response = await self._async_client.chat.completions.create(
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

    async def _async_calls(self, questions: list[str], **kwargs) -> list[list[str]]:
        result = await asyncio.gather(
            *[self._async_call(question, **kwargs) for question in questions]
        )
        return result

    def async_run(self, questions: list[str], **kwargs) -> list[list[str]]:
        return asyncio.run(self._async_calls(questions, **kwargs))


class InstructedTestModelClient(ChatBaseModel):
    def __init__(self, instruct) -> None:
        super().__init__()
        self.instruct = instruct
        self._client = OpenAI()
        self._async_client = AsyncOpenAI()

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

        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=input_,  # type: ignore
            **kwargs,
        )

        return [
            choice.message.content
            for choice in response.choices
            if choice.message.content
        ]

    async def _async_call(self, question: str, **kwargs) -> list[str]:
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
        response = await self._async_client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.9,
            messages=input_,  # type: ignore
            **kwargs,
        )

        msg = response.choices[0].message.content
        if isinstance(msg, str):
            return [msg]
        else:
            raise ValueError

    async def _async_calls(self, questions: list[str], **kwargs) -> list[list[str]]:
        result = await asyncio.gather(
            *[self._async_call(question, **kwargs) for question in questions]
        )
        return result

    def async_run(self, questions: list[str], **kwargs) -> list[list[str]]:
        return asyncio.run(self._async_calls(questions, **kwargs))
