from typing import Union

import pandas as pd
from pydantic import BaseModel


# general
class Evaluation(BaseModel):
    score: float


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
    label: str
    confidence: float


class PromptInjectInputs(PromptInjectModel):
    verbose: bool = True
    use_async: bool = False


class PromptInjectSummary(BaseModel, arbitrary_types_allowed=True):
    attack_summary: pd.DataFrame


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
    label: str
    confidence: float


class PromptLeakInputs(PromptLeakModel):
    verbose: bool = True
    use_async: bool = False


class PromptLeakSummary(BaseModel, arbitrary_types_allowed=True):
    attack_summary: pd.DataFrame


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
    sample_size: int | None
    repeat_nums: int = 5
    verbose: bool = True
    use_async: bool = False


class JailBreakSummary(BaseModel, arbitrary_types_allowed=True):
    attack_summary: pd.DataFrame
    tag_summary: pd.DataFrame


# wrap inputs
AttackerInputs = Union[
    JailBreakInputs,
    PromptLeakInputs,
    PromptInjectInputs,
]
