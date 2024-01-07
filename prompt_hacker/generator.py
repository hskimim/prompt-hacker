from prompt_hacker import constant, prompts
from prompt_hacker.model import OpenAIChatModel
import requests
import pandas as pd
import warnings


class MaliciousGenerator(OpenAIChatModel):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, num_retry: int = 5, num_prompts: int = 30) -> list[str]:
        for _ in range(num_retry):
            result = self._generate(
                query=prompts.malicious_generator(num_prompts)
            ).split(constant.prompt_seperator)[0]
            if len(result) < 5:
                continue
            return [i.strip() for i in result]
        warnings.warn(
            """Failed to create malicious prompt. It appears to be due to OpenAI's policy.
              Try by increasing the size of temepature or increasing the number of num_retry.
              5 pre-prepared examples will be returned in this time.
              """
        )
        return constant.malicious_prompts


class JailBreakGenerator(OpenAIChatModel):
    def __init__(self) -> None:
        super().__init__()
        self._jailbreakers = self._crawl_jailbreakers()

    def _crawl_jailbreakers(self) -> list[str]:
        res = requests.get(constant.jailbreakchat_url)
        df = pd.DataFrame(res.json())
        df["votes"] = df.upvotes - df.downvotes
        df = df[df["votes"] > 0]  # filtering with its vote
        df["text"] = df["text"].str.replace(constant.query_loc, "{query}")
        df.sort_values("votes", ascending=False, inplace=True)
        return df["text"].values.tolist()

    def _load_examples(self, num_examples: int) -> list[str]:
        ls = self._jailbreakers[:num_examples]
        for idx, val in enumerate(ls):
            ls[idx] = f"{idx+1}. {val}"
        return ls

    def __call__(self, num_examples: int = 5) -> list[str]:
        query = prompts.synthetic_prompt_generator(self._load_examples(num_examples))
        return self._generate(query).split(constant.prompt_seperator)[0]

    @property
    def jailbreak_prompt_list(self):
        return self._jailbreakers
