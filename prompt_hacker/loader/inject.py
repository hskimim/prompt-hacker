from prompt_hacker import constant, utils


class PromptInjectLoader:
    def __init__(
        self,
    ) -> None:
        self._inject_prompts: list[dict[str, str]] = utils.read_file_with_rel_path(
            constant.INJECT_PROMPTS_JSON_REL_PATH,
        )

    def load(self) -> list[dict[str, str]]:
        return self._inject_prompts


class JailBreakLoader:
    def __init__(
        self,
    ) -> None:
        self.inject_prompts_loader = PromptInjectLoader()

    def __iter__(self) -> dict[str, str]:
        for data in self.inject_prompts_loader.load():
            yield data

    def __len__(self) -> int:
        return len(self.inject_prompts_loader.load())
