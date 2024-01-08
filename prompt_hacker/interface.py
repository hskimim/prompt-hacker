from typing import Protocol


class ChatBaseModel(Protocol):
    def run(self, question: str, **kwargs) -> list[str]:
        ...
