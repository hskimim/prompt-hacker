from typing import Dict, Generic, List
from typing_extensions import override
from prompt_hacker.interface import Attacker, ChatBaseModel, Evaluator
from prompt_hacker.schemas import (
    T_EVALUATION_RESULT,
    EvaluationSummary,
    T_ATTACK_RESULT_co,
    T_ATTACK_RESULT_con,
)


class PipeLine(Generic[T_EVALUATION_RESULT]):
    def __init__(
        self, attacker: Attacker[T_ATTACK_RESULT_co], evaluator: Evaluator[T_ATTACK_RESULT_con, T_EVALUATION_RESULT]
    ) -> None:
        self._attacker = attacker
        self._evaluator = evaluator

        if str(self._attacker) != str(self._evaluator):
            raise ValueError(
                f"attacker and evaluator is incompatible. we got {str(self._attacker)} attacker but {str(self._evaluator)} in evalutor"
            )

    @override
    def __str__(self) -> str:
        return str(self._attacker)

    def __call__(self, model: ChatBaseModel) -> EvaluationSummary:
        result = self._attacker.run(model=model)
        evaluated = self._evaluator.evaluate(result)  # TODO: we need to fix typo here
        return self._evaluator.summary(evaluated)  # type:ignore


class PipelineChain:
    def __init__(self, pipelines: List[PipeLine[T_EVALUATION_RESULT]]) -> None:
        self._pipelines = pipelines

    def __call__(self, model: ChatBaseModel) -> Dict[str, EvaluationSummary]:
        return {str(pipe): pipe(model) for pipe in self._pipelines}


# TODO: deprecate
# class CompositePipeLine:
#     def __init__(self, pipelines: List[PipeLine]) -> None:
#         self._pipelines = pipelines

#     @staticmethod
#     def _convert_inputs_to_input_dict(
#         inputs: list[AttackerInputs],
#     ) -> dict[str, AttackerInputs]:
#         return {str(input_): input_ for input_ in inputs}

#     def _validate_inputs(self, input_dict: dict[str, AttackerInputs]) -> None:
#         missed_input: set[str] = set([str(pipe) for pipe in self._pipelines]) - set(list(input_dict.keys()))
#         if len(missed_input):
#             raise ValueError(f"there is missed input for {missed_input} component(s)")

#     def __call__(self, inputs: list[AttackerInputs]) -> dict[str, Evaluation]:
#         input_dict = self._convert_inputs_to_input_dict(inputs)
#         self._validate_inputs(input_dict)

#         return {str(pipe): pipe(input_dict[str(pipe)]) for pipe in self._pipelines}  # TODO : make it async
