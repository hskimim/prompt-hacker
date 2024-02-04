import itertools

import pandas as pd
import requests
from typing_extensions import override

from prompt_hacker import constant, utils
from prompt_hacker.convert import Base64Convertor, Obfuscationer
from prompt_hacker.interface import Loader


class MaliciousPromptLoader(Loader):
    def __init__(self) -> None:
        super().__init__()
        self._malicious_prompt = utils.read_file_with_rel_path(
            constant.MALICIOUS_PROMPTS_JSON_REL_PATH
        )

    @override
    def __len__(self) -> int:
        return len(self._malicious_prompt)

    @override
    def __iter__(self) -> dict[str, str]:
        for data in self._malicious_prompt:
            yield data

    def load(self) -> list[dict[str, str]]:
        return self._malicious_prompt


class JailBreakChatPromptsLoader(Loader):
    """jailbreak prefix prompt synthetic data generator"""

    def __init__(self, sample_size: int | None = None) -> None:
        super().__init__()
        self.sample_size = sample_size
        self._jailbreakchat_json = self._crawl_jailbreakers()

    def _crawl_jailbreakers(self) -> list[dict[str, str]]:
        res = requests.get(constant.JAILBREAKCHAT_URL)

        df = pd.DataFrame(res.json())

        df["votes"] = df.upvotes - df.downvotes
        df = df[df["votes"] > 0]

        df["text"] = df["text"].str.replace(
            constant.JAILBREAKCHAT_PROMPT_LOC, constant.PROMPT_TAG
        )

        df = df.sort_values("votes", ascending=False).rename(
            columns={
                "name": "attack_name",
                "text": "attack_prompt",
            }
        )
        df = (
            df[["attack_name", "attack_prompt"]].head(self.sample_size)
            if self.sample_size
            else df[["attack_name", "attack_prompt"]].copy()
        )

        return [
            dict(zip(df.columns.tolist(), df.iloc[idx].to_numpy()))
            for idx in range(len(df))
        ]

    @override
    def __len__(self) -> int:
        return len(self._jailbreakchat_json)

    @override
    def __iter__(self) -> dict[str, str]:
        for data in self._jailbreakchat_json:
            yield data

    def load(self) -> list[dict[str, str]]:
        return self._jailbreakchat_json


class JailBreakPromptsLoader(Loader):
    def __init__(
        self,
        use_jailbreakchat: bool = False,
        num_jailbreakchat: int = 10,
        ignore_error: bool = False,
    ) -> None:
        self._jailbreak_prompts: list[dict[str, str]] = utils.read_file_with_rel_path(
            constant.JAILBREAK_PROMPTS_JSON_REL_PATH,
        )
        self.ignore_error = ignore_error
        if use_jailbreakchat:
            self._jailbreak_prompts += JailBreakChatPromptsLoader(
                sample_size=num_jailbreakchat
            ).load()

        self._jailbreak_prompts = self._validate_prompts(self._jailbreak_prompts)

    def _validate_prompts(self, prompts: list[dict[str, str]]) -> list[dict[str, str]]:
        validated_prompts: list[dict[str, str]] = []
        for prompt in prompts:
            if not any(tag in prompt["attack_prompt"] for tag in constant.TAGS):
                if self.ignore_error:
                    continue
                print(prompt["attack_prompt"])
                raise ValueError(f"at least one of {constant.TAGS} should be in prompt")
            validated_prompts.append(prompt)
        return validated_prompts

    @override
    def __len__(self) -> int:
        return len(self._jailbreak_prompts)

    @override
    def __iter__(self) -> dict[str, str]:
        for data in self._jailbreak_prompts:
            yield data

    def load(self) -> list[dict[str, str]]:
        return self._jailbreak_prompts


class JailBreakLoader(Loader):
    def __init__(
        self,
        use_jailbreakchat: bool = False,
        num_jailbreakchat: int = 10,
        ignore_jailbreakchat_error: bool = False,
    ) -> None:
        self._malicious_prompt_loader = MaliciousPromptLoader()
        self._jailbreak_prompts_loader = JailBreakPromptsLoader(
            use_jailbreakchat=use_jailbreakchat,
            num_jailbreakchat=num_jailbreakchat,
            ignore_error=ignore_jailbreakchat_error,
        )

    @override
    def __iter__(self) -> dict[str, str]:
        for prompt, jailbreak in itertools.product(
            self._malicious_prompt_loader.load(),
            self._jailbreak_prompts_loader.load(),
        ):
            data = {**prompt, **jailbreak}
            query = data["malicious_prompt"]
            data["question"] = data["attack_prompt"].format(
                PROMPT=query,
                BASE64=Base64Convertor().encode(query),
                ROT13=Obfuscationer(method="rot13").encode(query),
                LEETSPEAK=Obfuscationer(method="leetspeak").encode(query),
                DISEMVOWEL=Obfuscationer(method="disemvowel").encode(query),
            )
            yield data

    @override
    def __len__(self) -> int:
        return len(self._malicious_prompt_loader.load()) * len(
            self._jailbreak_prompts_loader.load()
        )
