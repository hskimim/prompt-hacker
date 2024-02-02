from typing import Union

import pandas as pd
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
    attack_name: str
    attack_prompt: str
    target_string: str
    answer: str
    err: bool = False


class PromptInjectScore(PromptInjectResult):
    score: int


class PromptInjectInputs(PromptInjectModel):
    sample_size: int = 1
    verbose: bool = True


# leak
class PromptLeakModel(BaseModel):
    def __str__(self) -> str:
        return "leak"


class PromptLeakResult(PromptLeakModel):
    attack_name: str
    attack_prompt: str
    answer: str
    err: bool = False


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
    err: bool = False


class JailBreakScore(JailBreakResult):
    label: str
    confidence: float


class JailBreakInputs(JailBreakModel):
    sample_size: int | None = 10
    verbose: bool = True


class JailBreakSummary(BaseModel, arbitrary_types_allowed=True):
    attack_summary: pd.DataFrame
    tag_summary: pd.DataFrame


# wrap inputs
AttackerInputs = Union[
    JailBreakInputs,
    PromptLeakInputs,
    PromptInjectInputs,
    TrainingExtractInputs,
]
