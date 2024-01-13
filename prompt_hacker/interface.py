from typing import Protocol


class ChatBaseModel(Protocol):
    def run(self, question: str, **kwargs) -> list[str]:
        ...


class EmbedBaseModel(Protocol):
    def run(self, txts: list[str], **kwargs) -> list[list[float]]:
        ...
