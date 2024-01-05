from prompt_hacker.model import OpenAIChatModel


class AugmentPrompts(OpenAIChatModel):
    """
    Sampling With A Decaying Temperature' implementation from 'Extracting Training Data from Large Language Models'.
    """

    def __init__(self) -> None:
        super().__init__()

    def augment(
        self,
        input_: str,
        n: int = 50,
        max_tokens: int = 200,
    ) -> list[str]:
        high_temp_seq_length = int(max_tokens * 0.1)

        response = self.run(
            query=input_,
            temperature=2,
            n=n,
            max_tokens=high_temp_seq_length,
        )

        # concat input + output
        concated_inputs_: list[str] = []
        for choice in response.choices:
            tmp = input_[0]["content"] + choice.message.content
            concated_inputs_.append(tmp)

        augmented_answers: list[str] = []
        for input_ in concated_inputs_:
            response = self.run(
                temperature=1,
                max_tokens=max_tokens - high_temp_seq_length,
                query=input_,
            )
            answer = response.choices[0].message.content
            concat_answer = input_["content"] + answer  # concat input + output
            augmented_answers.append(concat_answer)

        return list(set(augmented_answers))
