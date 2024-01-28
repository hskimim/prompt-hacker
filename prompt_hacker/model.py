from typing import List, Optional
from typing_extensions import override
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from prompt_hacker import constant
from prompt_hacker.interface import ChatBaseModel, EmbedBaseModel

load_dotenv(verbose=True)


class OpenAIChatModel(ChatBaseModel):
    """openai model"""

    def __init__(self, client: Optional[OpenAI] = None, prompts: List[ChatCompletionMessageParam] = []) -> None:
        super().__init__()
        self._client = client or OpenAI()
        self._prompts = prompts

    @override
    def run(self, question: str) -> str:
        return self._generate([{"role": "user", "content": question}])

    def _generate(self, question: List[ChatCompletionMessageParam]) -> str:
        response = self._client.chat.completions.create(
            model=constant.MODEL_NM,
            messages=question,
        )

        content = response.choices[0].message.content
        if content is None:
            raise RuntimeError("failed to generate response")

        return content

    def with_prompts(self, prompts: List[ChatCompletionMessageParam]) -> "OpenAIChatModel":
        return OpenAIChatModel(client=self._client, prompts=prompts)


class OpenAIEmbedModel(EmbedBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self._client = OpenAI()

    @override
    def run(self, txt: str) -> List[float]:
        response = self._client.embeddings.create(input=txt, model=constant.EMBEDDING_MODEL_NM)
        return response.data[0].embedding
