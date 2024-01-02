from typing import Protocol


class ChatBaseModel(Protocol):
    def run(self, query: str) -> str:
        ...
