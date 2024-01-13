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


# inject
class PromptInjectResult(BaseModel):
    injected_prompt: str
    answer: str


class PromptInjectScore(PromptInjectResult):
    score: float


# leak
class PromptLeakResult(BaseModel):
    prompt: str
    answer: str


class PromptLeakScore(PromptLeakResult):
    score: float


# jailbreak
class JailBreakResult(BaseModel):
    prompt: str
    question: str
    query: str
    answer: str


class JailBreakScore(JailBreakResult):
    score: float
