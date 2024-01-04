from dotenv import load_dotenv
from openai import OpenAI
from prompt_hacker import constant
from prompt_hacker.generator import LLM

load_dotenv(True)


class AugmentPrompts(LLM):
    """
    Sampling With A Decaying Temperature' implementation from 'Extracting Training Data from Large Language Models'.
    """

    def __init__(self) -> None:
        super().__init__()

    def augment(
        self,
        input_: list[dict[str, str]],
        n: int = 50,
        max_tokens: int = 200,
    ) -> list[str]:
        high_temp_seq_length = int(max_tokens * 0.1)

        if len(input_) != 1:
            raise NotImplementedError("input_'s length should be 1")
        response = self._generate(
            query=input_,
            temperature=2,
            n=n,
            max_tokens=high_temp_seq_length,
        )

        # concat input + output
        concated_inputs_ = []
        for choice in response.choices:
            tmp = {
                "role": "user",
                "content": input_[0]["content"] + choice.message.content,
            }
            concated_inputs_.append(tmp)

        augmented_answers = []
        for input_ in concated_inputs_:
            response = self._generate(
                temperature=1,
                max_tokens=max_tokens - high_temp_seq_length,
                query=[input_],
            )
            answer = response.choices[0].message.content
            concat_answer = input_["content"] + answer  # concat input + output
            augmented_answers.append(concat_answer)

        augmented_answers = list(set(augmented_answers))
        return augmented_answers
