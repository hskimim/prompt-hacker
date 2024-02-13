from typing_extensions import override

from prompt_hacker import constant, utils
from prompt_hacker.convert import Base64Convertor, Obfuscationer
from prompt_hacker.interface import Loader


class PromptInjectLoader(Loader):
    def __init__(
        self,
    ) -> None:
        self._inject_prompts: list[dict[str, str]] = utils.read_file_with_rel_path(
            constant.INJECT_PROMPTS_JSON_REL_PATH,
        )

    def load(self) -> list[dict[str, str]]:
        return self._inject_prompts

    @override
    def __iter__(self) -> dict[str, str]:  # type: ignore
        for data in self.load():
            if any(
                data["attack_prompt"].endswith(model_nm)
                for model_nm in Obfuscationer(method="rot13").models()
            ):
                for query in constant.INJECT_PROMPTS:
                    data["attack_prompt"] = data["attack_prompt"].format(
                        PROMPT=query,
                        BASE64=Base64Convertor().encode(query),
                        ROT13=Obfuscationer(method="rot13").encode(query),
                        LEETSPEAK=Obfuscationer(method="leetspeak").encode(query),
                        DISEMVOWEL=Obfuscationer(method="disemvowel").encode(query),
                        HEX=Obfuscationer(method="hex").encode(query),
                    )
                    yield data
            else:
                yield data

    @override
    def __len__(self) -> int:
        return len(self.load())
