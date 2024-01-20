from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
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


TEST_MSG_HISTORY = [
    ChatCompletionUserMessageParam(
        content="""
Born in Maida Vale, London, Turing was raised in southern England. He graduated at King's College, Cambridge, with a degree in mathematics. Whilst he was a fellow at Cambridge, he published a proof demonstrating that some purely mathematical yes–no questions can never be
""",
        role="user",
    ),
    ChatCompletionAssistantMessageParam(
        content="""
answered by computation. He defined a Turing machine and proved that the halting problem for Turing machines is undecidable. In 1938, he obtained his PhD from the Department of Mathematics at Princeton University.
""",
        role="assistant",
    ),
]  # example from https://en.wikipedia.org/wiki/Alan_Turing


class FewShotTestModelClient(ChatBaseModel):
    def run(self, question: str, **kwargs) -> list[str]:
        input_ = TEST_MSG_HISTORY + [
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


class InstructedTestModelClient(ChatBaseModel):
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
