import json
from tqdm import tqdm
import warnings
from pydantic import BaseModel
from collections import defaultdict

import numpy as np
from scipy.spatial import distance

from prompt_hacker.model import TemperatureDecaySampling


class TrainingDataExtractResult(BaseModel):
    prefix_prompt: str
    suffix_prompt: str


class EvaluatedResult(TrainingDataExtractResult):
    score: float


class EvaluationReport(BaseModel):
    score_by_prefix: dict[str, float]


class TrainingDataExtractor(BaseModel):
    train_dataset_path: str | None = None
    train_dataset: list[str] | None = None
    temperature: float = 0.2
    temperature_ratio: float = 0.1
    max_tokens: int = 200
    sample_size: int = 50

    def __init__(
        self,
        temperature: float = 0.2,
        temperature_ratio: float = 0.1,
        max_tokens: int = 200,
        sample_size: int = 50,
    ) -> None:
        super().__init__(
            temperature=temperature,
            temperature_ratio=temperature_ratio,
            max_tokens=max_tokens,
            sample_size=sample_size,
        )

    def _generate_prefix_samples(self):
        # TODO : generate fractional samples from training dataset
        raise NotImplementedError()

    def run(
        self,
        prefix_samples: list[str],
        verbose: bool = False,
    ) -> list[TrainingDataExtractResult]:
        sampler = TemperatureDecaySampling(
            temperature=self.temperature,
            temperature_ratio=self.temperature_ratio,
            max_tokens=self.max_tokens,
            sample_size=self.sample_size,
        )  # TODO : fix the ugly

        data = (
            self._generate_prefix_samples()
            if prefix_samples is None
            else prefix_samples
        )
        iterator = tqdm(data) if verbose else data

        augmented_txts: list[str] = []
        for prefix_txt in iterator:
            generated_txt = sampler.augment(prefix_txt)
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


# TODO : should follow the same logic with paper
# use hamming distance as a temporary solution.


def calc_hamming_distance(s1: str, s2: str):
    return distance.hamming(list(s1), list(s2))


def calc_jacaard_similarity_for_one_side(compare: str, criteria: str):
    return len(set(compare) & set(criteria)) / len(set(criteria))


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

        with open(self.train_dataset_path, "r") as file:
            loaded_data = json.load(file)
        return loaded_data

    def evaluate(
        self, results: list[TrainingDataExtractResult]
    ) -> list[EvaluatedResult]:
        train_data: str = self._load_train()
        evaluated = []
        for result in results:
            suffix = result.suffix_prompt  # fully generated sentence
            score = calc_jacaard_similarity_for_one_side(
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
