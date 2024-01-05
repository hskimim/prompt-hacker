from prompt_hacker import constant, prompts
from prompt_hacker.interface import ChatBaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(verbose=True)


class OpenAIChatModel(ChatBaseModel):
    """openai model"""

    def __init__(self) -> None:
        super().__init__()
        self._client = OpenAI()

    def _generate(self, query: list[dict[str, str]], **kwargs) -> str:
        response = self._client.chat.completions.create(
            **kwargs,
            model=constant.model_nm,
            messages=query,
        )

        msg = response.choices[0].message.content
        return msg

    def run(self, query: str, **kwargs) -> str:
        input_ = [{"role": "user", "content": query}]
        return self._generate(input_, kwargs)
