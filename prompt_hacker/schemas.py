from typing import Union

from pydantic import BaseModel


# general
class Evaluation(BaseModel):
    score: float


# extract_train
class TrainingDataExtractModel(BaseModel):
    def __str__(self) -> str:
        return "extract_train"


class TrainingDataExtractResult(TrainingDataExtractModel):
    prefix_prompt: str
    suffix_prompt: str


class TrainingExtractScore(TrainingDataExtractResult):
    score: float


class TrainingExtractInputs(TrainingDataExtractModel):
    prefix_samples: list[str]
    sample_size: int = 50
    verbose: bool = True


# inject
class PromptInjectModel(BaseModel):
    def __str__(self) -> str:
        return "inject"


class PromptInjectResult(PromptInjectModel):
    injected_prompt: str
    answer: str


class PromptInjectScore(PromptInjectResult):
    score: float


class PromptInjectInputs(PromptInjectModel):
    sample_size: int = 1
    verbose: bool = True


# leak
class PromptLeakModel(BaseModel):
    def __str__(self) -> str:
        return "leak"


class PromptLeakResult(PromptLeakModel):
    prompt: str
    answer: str


class PromptLeakScore(PromptLeakResult):
    score: float


class PromptLeakInputs(PromptLeakModel):
    sample_size: int = 50
    verbose: bool = True


# jailbreak
class JailBreakModel(BaseModel):
    def __str__(self) -> str:
        return "jailbreak"


class JailBreakResult(JailBreakModel):
    malicious_name: str
    malicious_tag: str
    malicious_prompt: str
    attack_name: str
    attack_prompt: str
    answer: str

    # prompt: str
    # question: str
    # query: str
    # answer: str


class JailBreakScore(JailBreakResult):
    score: float


class JailBreakInputs(JailBreakModel):
    sample_size: int | None = 10
    verbose: bool = True


# wrap inputs
AttackerInputs = Union[
    JailBreakInputs,
    PromptLeakInputs,
    PromptInjectInputs,
    TrainingExtractInputs,
]
