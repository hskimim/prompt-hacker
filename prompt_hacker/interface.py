from typing import Protocol


class ChatBaseModel(Protocol):
    def run(self, question: str, **kwargs) -> list[str]:
        ...

    def async_run(self, questions: list[str], **kwargs) -> list[list[str]]:
        ...


class EmbedBaseModel(Protocol):
    def run(self, txts: list[str], **kwargs) -> list[list[float]]:
        ...


class Attacker(Protocol):
    def run(self, *args, **kwargs):
        pass


class Evaluator(Protocol):
    def evaluate(self, *args, **kwargs):
        pass

    def summary(self, *args, **kwargs):
        pass


class StringConverter(Protocol):
    def encode(self, string: str) -> str:
        ...

    def decode(self, encoded: str) -> str:
        ...


class Loader(Protocol):
    def __iter__(self) -> dict[str, str]:
        ...

    def __len__(self) -> int:
        ...
