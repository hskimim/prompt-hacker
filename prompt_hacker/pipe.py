from prompt_hacker.interface import Attacker, Evaluator
from prompt_hacker.schemas import AttackerInputs, Evaluation


class PipeLine:
    def __init__(self, attacker: Attacker, evaluator: Evaluator) -> None:
        self._attacker = attacker
        self._evaluator = evaluator

        if str(self._attacker) != str(self._evaluator):
            raise ValueError(
                f"attacker and evaluator is incompatible. we got {self._attacker!s} attacker but {self._evaluator!s} in evalutor",
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
    def _convert_inputs_to_input_dict(
        inputs: list[AttackerInputs],
    ) -> dict[str, AttackerInputs]:
        return {str(input_): input_ for input_ in inputs}

    def _validate_inputs(self, input_dict: dict[str, AttackerInputs]) -> None:
        missed_input: set[str] = set([str(pipe) for pipe in self._pipelines]) - set(
            list(input_dict.keys()),
        )
        if len(missed_input):
            raise ValueError(f"there is missed input for {missed_input} component(s)")

    def __call__(self, inputs: list[AttackerInputs]) -> dict[str, Evaluation]:
        input_dict = self._convert_inputs_to_input_dict(inputs)
        self._validate_inputs(input_dict)

        return {str(pipe): pipe(input_dict[str(pipe)]) for pipe in self._pipelines}  # TODO : make it async
