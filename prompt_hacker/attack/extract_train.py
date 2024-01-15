from tqdm import tqdm

from prompt_hacker.generator import TemperatureDecaySampling
from prompt_hacker.interface import ChatBaseModel
from prompt_hacker.schemas import TrainingDataExtractResult


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

    def run(
        self,
        prefix_samples: list[str],
        sample_size: int = 50,
        verbose: bool = False,
    ) -> list[TrainingDataExtractResult]:
        sampler = TemperatureDecaySampling(
            model=self.model,
            temperature=self.temperature,
            temperature_ratio=self.temperature_ratio,
            max_tokens=self.max_tokens,
            sample_size=sample_size,
        )
        iters = tqdm(prefix_samples) if verbose else prefix_samples
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
