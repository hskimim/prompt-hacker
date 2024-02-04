from typing_extensions import override

from prompt_hacker import constant, utils
from prompt_hacker.interface import Loader


class PromptLeakLoader(Loader):
    def __init__(
        self,
    ) -> None:
        self._inject_prompts: list[dict[str, str]] = utils.read_file_with_rel_path(
            constant.LEAK_PROMPTS_JSON_REL_PATH,
        )

    def load(self) -> list[dict[str, str]]:
        return self._inject_prompts

    @override
    def __iter__(self) -> dict[str, str]:
        for data in self.load():
            yield data

    @override
    def __len__(self) -> int:
        return len(self.load())
