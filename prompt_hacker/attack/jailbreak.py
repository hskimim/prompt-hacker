import random
from copy import copy
from itertools import product

from tqdm import tqdm

from prompt_hacker.generator import JailBreakGenerator, MaliciousGenerator
from prompt_hacker.interface import ChatBaseModel
from prompt_hacker.schemas import JailBreakResult


class JailBreaker:
    def __init__(self, model: ChatBaseModel) -> None:
        self._model = model
        self._jb = JailBreakGenerator()
        self._mal = MaliciousGenerator()

    def _prepare_prompts(
        self,
        sample_size: int | None,
        verbose: bool,
        shuffle: bool,
    ) -> product | tqdm:
        # TODO: Refactor for cleaner and more interpretable
        prompts = copy(self._jb.jailbreak_prompt_list)
        questions = copy(self._mal())
        if shuffle:
            random.shuffle(prompts)
            random.shuffle(questions)
        iters = list(product(prompts, questions))
        total_len = int(len(prompts) * len(questions))
        iters = (
            tqdm(iters, total=sample_size if sample_size else total_len)  # type: ignore
            if verbose  # type: ignore
            else iters  # type: ignore
        )
        return iters  # type: ignore

    def run(
        self,
        sample_size: int | None = None,
        shuffle: bool = False,
        verbose: bool = False,
    ) -> list[JailBreakResult]:
        iters = self._prepare_prompts(sample_size, verbose, shuffle)
        result = []
        cnt = 0
        try:
            for prompt, question in iters:  # type: ignore
                query = prompt.format(query=question)
                answer = self._model.run(query)[0]
                result.append(
                    JailBreakResult(
                        prompt=prompt,
                        question=question,
                        query=query,
                        answer=answer,
                    )
                )
                cnt += 1
                if sample_size:
                    if cnt > sample_size:
                        break
        except KeyboardInterrupt:
            return result
        except Exception:
            print(
                f"""there was error during model api call.
                prompt : {prompt}
                question : {question}"""
            )
        return result
