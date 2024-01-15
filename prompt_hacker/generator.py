import time
import warnings

import pandas as pd
import requests

from prompt_hacker import constant, prompts
from prompt_hacker.interface import ChatBaseModel
from prompt_hacker.model import OpenAIChatModel


class MaliciousGenerator(OpenAIChatModel):
    def __init__(self) -> None:
        super().__init__()

    def __call__(
        self, num_retry: int = 5, tol_time: int = 30, num_prompts: int = 30
    ) -> list[str]:
        start_t = time.time()
        for _ in range(num_retry):
            result = self._generate(
                question=prompts.malicious_generator(num_prompts),  # type:ignore
                temperature=1.5,
            )[0][0].split(constant.PROMPT_SEPERATOR)[0]
            if len(result) < num_prompts / 10:
                if time.time() - start_t > tol_time:
                    break
                continue
            return [i.strip() for i in result]
        warnings.warn(
            """Failed to create malicious prompt. It appears to be due to OpenAI's policy.
              pre-prepared examples will be returned in this time.
              """
        )
        return constant.MALICIOUS_PROMPTS


class JailBreakGenerator(OpenAIChatModel):
    def __init__(self) -> None:
        super().__init__()
        self._jailbreakers = self._crawl_jailbreakers()

    def _crawl_jailbreakers(self) -> list[str]:
        res = requests.get(constant.JAILBREAKCHAT_URL)
        df = pd.DataFrame(res.json())
        df["votes"] = df.upvotes - df.downvotes
        df = df[df["votes"] > 0]  # filtering with its vote
        df["text"] = df["text"].str.replace(constant.QUERY_LOC, "{query}")
        df.sort_values("votes", ascending=False, inplace=True)
        return df["text"].values.tolist()

    def _load_examples(self, num_examples: int) -> list[str]:
        ls = self._jailbreakers[:num_examples]
        for idx, val in enumerate(ls):
            ls[idx] = f"{idx+1}. {val}"
        return ls

    def __call__(self, num_examples: int = 5) -> list[str]:
        query = prompts.synthetic_prompt_generator(self._load_examples(num_examples))
        return self._generate(query)[0].split(constant.PROMPT_SEPERATOR)

    @property
    def jailbreak_prompt_list(self):
        return self._jailbreakers


class SystemPromptGenerator(OpenAIChatModel):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, num_examples: int = 5) -> list[str]:
        query = prompts.system_prompt_generator(num_prompts=num_examples)
        return self._generate(query)[0].split(constant.PROMPT_SEPERATOR)


class TemperatureDecaySampling:
    """
    Sampling With A Decaying Temperature' implementation from 'Extracting Training Data from Large Language Models'.
    """

    def __init__(
        self,
        model: ChatBaseModel,
        temperature: float = 2.0,
        temperature_ratio: float = 0.1,
        max_tokens: int = 200,
        sample_size: int = 50,
    ):
        self.model = model
        self.temperature = temperature
        self.temperature_ratio = temperature_ratio
        self.max_tokens = max_tokens
        self.sample_size = sample_size

    def augment(
        self,
        init_question: str,
    ) -> list[str]:
        high_temp_seq_length = int(self.max_tokens * self.temperature_ratio)
        messages: list[str] = self.model.run(
            question=init_question,
            temperature=self.temperature,
            n=self.sample_size,
            max_tokens=high_temp_seq_length,
        )
        # concat input + output
        concated_inputs_ = [init_question + msg for msg in messages]

        self.temperature = 1
        self.max_tokens = self.max_tokens - high_temp_seq_length
        self.sample_size = 1

        if self.max_tokens == 0:
            return concated_inputs_

        augmented_answers: list[str] = []

        for input_ in concated_inputs_:
            answer: str = self.model.run(
                question=input_,
                temperature=self.temperature,
                n=self.sample_size,
                max_tokens=high_temp_seq_length,
            )[0]
            concat_answer = input_ + answer  # concat input + output
            augmented_answers.append(concat_answer)

        return list(set(augmented_answers))
