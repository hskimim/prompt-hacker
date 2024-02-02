from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from prompt_hacker import constant
from prompt_hacker.interface import ChatBaseModel, EmbedBaseModel

load_dotenv(verbose=True)


class OpenAIChatModel(ChatBaseModel):
    """openai model"""

    def __init__(self) -> None:
        super().__init__()
        self._client = OpenAI()

    def _generate(self, question: ChatCompletionMessageParam, **kwargs) -> list[str]:
        response = self._client.chat.completions.create(
            **kwargs,
            model=constant.MODEL_NM,
            messages=question,
        )  # type:ignore
        if len(response.choices) == 1:
            return [response.choices[0].message.content]
        else:
            return [choice.message.content for choice in response.choices]

    def run(self, question: str, **kwargs) -> list[str]:
        input_ = [{"role": "user", "content": question}]
        return self._generate(input_, **kwargs)  # type:ignore


class OpenAIEmbedModel(EmbedBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self._client = OpenAI()

    def run(self, txts: list[str], **kwargs) -> list[list[float]]:
        vectors: list[list[float]] = []
        for answer in txts:
            try:
                v: list[float] = (
                    self._client.embeddings.create(
                        input=answer,
                        model=constant.EMBEDDING_MODEL_NM,
                    )
                    .data[0]
                    .embedding
                )
                vectors.append(v)
            except Exception:
                print(f"err for {answer}")
        return vectors
