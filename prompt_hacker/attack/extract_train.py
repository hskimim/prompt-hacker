import json
from prompt_hacker.model import TemperatureDecaySampling
from prompt_hacker import constant


class TrainingDataExtractor:
    def __init__(
        self,
        train_dataset_path: str,
        temperature: float = 0.2,
        temperature_ratio: float = 0.1,
        max_tokens: int = 200,
        sample_size: int = 50,
    ) -> None:
        self.train_dataset_path = train_dataset_path
        if not train_dataset_path.endswith(constant.TRAINING_DATASET_PATH):
            raise ValueError(
                f"training dataset's file name should be {constant.TRAINING_DATASET_PATH}"
            )
        self.sampler = TemperatureDecaySampling(
            temperature=temperature,
            temperature_ratio=temperature_ratio,
            max_tokens=max_tokens,
            sample_size=sample_size,
        )

    def _load_train(self) -> list[str]:
        with open(self.train_dataset_path, "r") as file:
            loaded_data = json.load(file)
        return loaded_data

    def run(self, prefix_txt: str) -> dict[str, float]:
        augmented_txt = self.sampler.augment(prefix_txt)
        remained_prompts = [i.replace(prefix_txt, "").strip() for i in augmented_txt]

        train_data = self._load_train()
        target_data = [x.replace(prefix_txt, "").strip() for x in train_data]

        # evaluate TODO : seperate it into Evaluator
        max_score = 0
        for gen_prompt in remained_prompts:
            for train_data in target_data:
                score = sum(
                    [
                        1 if train_data[idx] == txt else 0
                        for idx, txt in enumerate(gen_prompt)
                    ]
                ) / len(gen_prompt)

                if max(max_score, score) == score:
                    max_score = score
                    max_prompt = gen_prompt

        return {max_prompt: max_score}
