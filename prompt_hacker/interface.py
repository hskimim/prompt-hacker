from abc import abstractmethod
from typing import List, Protocol

from prompt_hacker.schemas import T_EVALUATION_RESULT, EvaluationSummary, T_ATTACK_RESULT_co, T_ATTACK_RESULT_con


class ChatBaseModel(Protocol):
    def run(self, question: str) -> str:
        ...


class EmbedBaseModel(Protocol):
    def run(self, txt: str) -> List[float]:
        ...


class Attacker(Protocol[T_ATTACK_RESULT_co]):
    @abstractmethod
    def run(self, model: ChatBaseModel) -> T_ATTACK_RESULT_co:
        pass


class Evaluator(Protocol[T_ATTACK_RESULT_con, T_EVALUATION_RESULT]):
    @abstractmethod
    def evaluate(self, result: T_ATTACK_RESULT_con) -> T_EVALUATION_RESULT:
        pass

    @abstractmethod
    def summary(self, result: T_EVALUATION_RESULT) -> EvaluationSummary:
        pass
