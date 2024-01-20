from abc import abstractmethod
from typing import Generic, Protocol, TypeVar

from prompt_hacker.schemas import AttackResult


class ChatBaseModel(Protocol):
    def run(self, question: str, **kwargs) -> list[str]:
        ...


class EmbedBaseModel(Protocol):
    def run(self, txts: list[str], **kwargs) -> list[list[float]]:
        ...

R = TypeVar("R", bound=AttackResult, covariant=True)

class Attacker(Protocol[R]):
    @abstractmethod
    def run(self) -> R:
        pass


class Evaluator(Protocol):
    def evaluate(self, *args, **kwargs):
        pass

    def summary(self, *args, **kwargs):
        pass
