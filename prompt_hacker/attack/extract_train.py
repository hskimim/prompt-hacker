import json
import warnings

from pydantic import BaseModel
from tqdm import tqdm

from prompt_hacker import utils
from prompt_hacker.generator import TemperatureDecaySampling
from prompt_hacker.interface import ChatBaseModel
from prompt_hacker.schemas import (
    Evaluation,
    TrainingDataExtractResult,
    TrainingExtractInputs,
    TrainingExtractScore,
)


class TrainingDataExtractor:
    def __init__(
        self,
        model: ChatBaseModel,
        temperature: float = 0.2,
        temperature_ratio: float = 0.1,
        max_tokens: int = 200,
    ) -> None:
        self.model = model
        self.temperature = temperature
        self.temperature_ratio = temperature_ratio
        self.max_tokens = max_tokens

    def __str__(self) -> str:
        return "extract_train"

    def _generate_prefix_samples(self):
        # TODO : generate fractional samples from training dataset
        raise NotImplementedError()

    def run(self, inputs: TrainingExtractInputs) -> list[TrainingDataExtractResult]:
        sampler = TemperatureDecaySampling(
            model=self.model,
            temperature=self.temperature,
            temperature_ratio=self.temperature_ratio,
            max_tokens=self.max_tokens,
            sample_size=inputs.sample_size,
        )
        iters = tqdm(inputs.prefix_samples) if inputs.verbose else inputs.prefix_samples
        augmented_txts = [
            TrainingDataExtractResult(
                prefix_prompt=prefix_txt,
                suffix_prompt=txt,
            )
            for prefix_txt in iters  # type: ignore
            for txt in [
                i.replace(prefix_txt, "").strip() for i in sampler.augment(prefix_txt)
            ]
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

    def __str__(self) -> str:
        return "extract_train"

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
    ) -> list[TrainingExtractScore]:
        train_data: str = self._load_train()
        evaluated = []
        for result in results:
            suffix = result.suffix_prompt  # fully generated sentence
            score = (
                1
                - utils.calc_jacaard_similarity_for_one_side(  # TODO : should follow the same logic with paper
                    compare=train_data, criteria=suffix
                )
            )
            evaluated.append(
                TrainingExtractScore(
                    prefix_prompt=result.prefix_prompt,
                    suffix_prompt=result.suffix_prompt,
                    score=score,
                )
            )
        return evaluated

    def summary(self, results: list[TrainingExtractScore]) -> Evaluation:
        sum_ = 0.0
        cnt_ = 0
        for result in results:
            sum_ += result.score
            cnt_ += 1
        score = sum_ / cnt_

        return Evaluation(score=score)
