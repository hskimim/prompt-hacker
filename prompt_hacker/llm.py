from typing import Any
from pydantic import BaseModel


def is_str(s) -> bool:
    return isinstance(s, str)


def ensure_str(s) -> None:
    if not is_str(s):
        raise TypeError(f"input should be str type. but got {type(s)}")


class ChatBot:
    def __init__(self, model: Any):
        self._model = model

    def process(self, query: str) -> str:
        """
        Convert both the input and output of an model object to be of type string using inheritance
        """
        input_ = [
            {"role": "user", "content": query}
        ]  # convert string input into OpenAI style
        result = self._model(input_)
        return result

    def run(self, query: str) -> str:
        ensure_str(query)
        result = self.process(query)
        ensure_str(result)
        return result
