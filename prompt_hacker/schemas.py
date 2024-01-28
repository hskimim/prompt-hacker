from typing import List, TypeVar
from typing_extensions import override

from pydantic import BaseModel


# general
class AttackResult(BaseModel):
    pass


T_ATTACK_RESULT_co = TypeVar("T_ATTACK_RESULT_co", bound=AttackResult, covariant=True)
T_ATTACK_RESULT_con = TypeVar("T_ATTACK_RESULT_con", bound=AttackResult, contravariant=True)


class EvaluationResult(BaseModel):
    score: float


T_EVALUATION_RESULT = TypeVar("T_EVALUATION_RESULT", bound=EvaluationResult)


class EvaluationSummary(BaseModel):
    score: float


# extract_train
class TrainingDataExtractModel(BaseModel):
    @override
    def __str__(self) -> str:
        return "extract_train"


# class TrainingDataExtractResult(AttackResult, TrainingDataExtractModel):
#     prefix_prompt: str
#     suffix_prompt: str


# class TrainingExtractScore(TrainingDataExtractResult):
#     score: float


# class TrainingExtractInputs(TrainingDataExtractModel):
#     prefix_samples: list[str]
#     sample_size: int = 50
#     verbose: bool = True


# inject
class PromptInjectBaseModel(BaseModel):
    @override
    def __str__(self) -> str:
        return "inject"


class PromptInjectInputs(PromptInjectBaseModel):
    sample_size: int = 1
    verbose: bool = True


class PromptInjectAttackResult(AttackResult):
    results: List["PromptInjectAttackResult.Result"]

    class Result(PromptInjectBaseModel):
        injected_prompt: str
        answer: str


class PromptInjectEvaulationResult(EvaluationResult):
    score: float
    results: List["PromptInjectEvaulationResult.Result"]

    class Result(PromptInjectBaseModel, EvaluationResult):
        score: float
        attack: PromptInjectAttackResult.Result


# leak
class PromptLeakModel(BaseModel):
    @override
    def __str__(self) -> str:
        return "leak"


# class PromptLeakResult(AttackResult, PromptLeakModel):
# prompt: str
# answer: str
#
#
# class PromptLeakScore(PromptLeakResult):
# score: float
#
#
# class PromptLeakInputs(PromptLeakModel):
# sample_size: int = 50
# verbose: bool = True


# jailbreak
class JailBreakModel(BaseModel):
    @override
    def __str__(self) -> str:
        return "jailbreak"


# class JailBreakResult(AttackResult, JailBreakModel):
# prompt: str
# question: str
# query: str
# answer: str
#
#
# class JailBreakScore(JailBreakResult):
# score: float
#
#
# class JailBreakInputs(JailBreakModel):
# sample_size: int | None = 10
# shuffle: bool = True
# verbose: bool = True
#
#
# wrap inputs
# AttackerInputs = Union[
# JailBreakInputs,
# PromptLeakInputs,
# PromptInjectInputs,
# TrainingExtractInputs,
# ]
#
