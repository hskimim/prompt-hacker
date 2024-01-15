from typing import Union

from prompt_hacker.attack.extract_train import TrainingDataExtractor
from prompt_hacker.attack.inject import PromptInjector
from prompt_hacker.attack.jailbreak import JailBreaker
from prompt_hacker.attack.leak import PromptLeaker
from prompt_hacker.evaluate.extract_train import TrainingDataExtractorEvaluator
from prompt_hacker.evaluate.inject import PromptInjectorEvaluator
from prompt_hacker.evaluate.jailbreak import JailBreakEvaluator
from prompt_hacker.evaluate.leak import PromptLeakEvaluator
from prompt_hacker.schemas import (
    Evaluation,
    JailBreakInputs,
    PromptInjectInputs,
    PromptLeakInputs,
    TrainingExtractInputs,
)

Attacker = Union[
    TrainingDataExtractor,
    PromptInjector,
    PromptLeaker,
    JailBreaker,
]
Evaluator = Union[
    TrainingDataExtractorEvaluator,
    PromptInjectorEvaluator,
    PromptLeakEvaluator,
    JailBreakEvaluator,
]

Inputs = Union[
    JailBreakInputs,
    PromptLeakInputs,
    PromptInjectInputs,
    TrainingExtractInputs,
]


class PipeLine:
    def __init__(self, attacker: Attacker, evaluator: Evaluator) -> None:
        self._attacker = attacker
        self._evaluator = evaluator

        if str(self._attacker) != str(self._evaluator):
            raise ValueError(
                f"attacker and evaluator is incompatible. we got {str(self._attacker)} attacker but {str(self._evaluator)} in evalutor"
            )

    def __str__(self) -> str:
        return str(self._attacker)

    def __call__(self, *args, **kwargs) -> Evaluation:
        result = self._attacker.run(*args, **kwargs)
        evaluated = self._evaluator.evaluate(result)  # type:ignore
        return self._evaluator.summary(evaluated)  # type:ignore


class CompositePipeLine:
    def __init__(self, pipelines: list[PipeLine]) -> None:
        self._pipelines = pipelines

    @staticmethod
    def _convert_inputs_to_input_dict(inputs: list[Inputs]) -> dict[str, Inputs]:
        return {str(input_): input_ for input_ in inputs}

    def __call__(self, inputs: list[Inputs]) -> dict[str, Evaluation]:
        input_dict = self._convert_inputs_to_input_dict(inputs)
        return {str(pipe): pipe(input_dict[str(pipe)]) for pipe in self._pipelines}
