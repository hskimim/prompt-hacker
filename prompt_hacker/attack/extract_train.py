import json
import warnings
from collections import defaultdict

from pydantic import BaseModel
from tqdm import tqdm

from prompt_hacker import utils
from prompt_hacker.generator import TemperatureDecaySampling
from prompt_hacker.interface import ChatBaseModel


class TrainingDataExtractResult(BaseModel):
    prefix_prompt: str
    suffix_prompt: str


class EvaluatedResult(TrainingDataExtractResult):
    score: float


class EvaluationReport(BaseModel):
    score_by_prefix: dict[str, float]


class TrainingDataExtractor:
    def __init__(
        self,
        model: ChatBaseModel,
        temperature: float = 0.2,
        temperature_ratio: float = 0.1,
        max_tokens: int = 200,
        sample_size: int = 50,
    ) -> None:
        self.sampler = TemperatureDecaySampling(
            model=model,
            temperature=temperature,
            temperature_ratio=temperature_ratio,
            max_tokens=max_tokens,
            sample_size=sample_size,
        )  # TODO : fix the ugly

    def _generate_prefix_samples(self):
        # TODO : generate fractional samples from training dataset
        raise NotImplementedError()

    def run(
        self,
        prefix_samples: list[str],
        verbose: bool = False,
    ) -> list[TrainingDataExtractResult]:
        augmented_txts: list[TrainingDataExtractResult] = []

        iters = tqdm(iterable=prefix_samples) if verbose else prefix_samples
        for prefix_txt in iters:  # type: ignore
            generated_txt = self.sampler.augment(prefix_txt)
            remained_prompts = [
                i.replace(prefix_txt, "").strip() for i in generated_txt
            ]

            augmented_txts += [
                TrainingDataExtractResult(
                    prefix_prompt=prefix_txt,
                    suffix_prompt=txt,
                )
                for txt in remained_prompts
            ]
        return augmented_txts


class TrainingDataExtractorEvaluator(BaseModel):
    train_dataset_path: str | None = None
    train_dataset: str | None = None

    def __init__(
        self,
        train_dataset_path: str | None = None,
        train_dataset: str | None = None,
    ) -> None:
        super().__init__(
            train_dataset_path=train_dataset_path,
            train_dataset=train_dataset,
        )

        if not (train_dataset or train_dataset_path):
            raise ValueError(
                "you have to insert one of train_dataset_path or train_dataset"
            )
        if train_dataset_path and train_dataset:
            warnings.warn(
                "you give train_dataset_path and train_dataset both. train_dataset will be only used with ignoring train_dataset_path"
            )

        self.train_dataset_path = train_dataset_path
        self.train_dataset = train_dataset

    def _load_train(self) -> str:
        if self.train_dataset:
            return self.train_dataset

        if isinstance(self.train_dataset_path, str):
            with open(self.train_dataset_path, "r") as file:
                return json.load(file)
        raise ValueError(
            "you have to insert one of train_dataset_path or train_dataset"
        )  # can't be happened

    def evaluate(
        self, results: list[TrainingDataExtractResult]
    ) -> list[EvaluatedResult]:
        train_data: str = self._load_train()
        evaluated = []
        for result in results:
            suffix = result.suffix_prompt  # fully generated sentence
            score = utils.calc_jacaard_similarity_for_one_side(  # TODO : should follow the same logic with paper
                compare=train_data, criteria=suffix
            )
            evaluated.append(
                EvaluatedResult(
                    prefix_prompt=result.prefix_prompt,
                    suffix_prompt=result.suffix_prompt,
                    score=score,
                )
            )
        return evaluated

    def summary(self, results: list[EvaluatedResult]) -> EvaluationReport:
        sum_dict: dict[str, float] = defaultdict(int)
        cnt_dict: dict[str, float] = defaultdict(int)
        for result in results:
            sum_dict[result.prefix_prompt] += result.score
            cnt_dict[result.prefix_prompt] += 1
        avg_dict = {k: sum_dict[k] / cnt_dict[k] for k in sum_dict}
        return EvaluationReport(score_by_prefix=avg_dict)
