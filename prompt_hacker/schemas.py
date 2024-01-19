from typing import Union

from pydantic import BaseModel


# general
class Evaluation(BaseModel):
    score: float


# extract_train
class TrainingDataExtractResult(BaseModel):
    prefix_prompt: str
    suffix_prompt: str


class TrainingExtractScore(TrainingDataExtractResult):
    score: float


class TrainingExtractInputs(BaseModel):
    prefix_samples: list[str]
    sample_size: int = 50
    verbose: bool = False

    def __str__(self) -> str:
        return "extract_train"


# inject
class PromptInjectResult(BaseModel):
    injected_prompt: str
    answer: str


class PromptInjectScore(PromptInjectResult):
    score: float


class PromptInjectInputs(BaseModel):
    sample_size: int = 1
    verbose: bool = True

    def __str__(self) -> str:
        return "inject"


# leak
class PromptLeakResult(BaseModel):
    prompt: str
    answer: str


class PromptLeakScore(PromptLeakResult):
    score: float


class PromptLeakInputs(BaseModel):
    sample_size: int = 50
    verbose: bool = True

    def __str__(self) -> str:
        return "leak"


# jailbreak
class JailBreakResult(BaseModel):
    prompt: str
    question: str
    query: str
    answer: str


class JailBreakScore(JailBreakResult):
    score: float


class JailBreakInputs(BaseModel):
    sample_size: int | None = 10
    shuffle: bool = False
    verbose: bool = False

    def __str__(self) -> str:
        return "jailbreak"


# wrap inputs
AttackerInputs = Union[
    JailBreakInputs,
    PromptLeakInputs,
    PromptInjectInputs,
    TrainingExtractInputs,
]
