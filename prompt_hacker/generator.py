from prompt_hacker import constant, prompts
from prompt_hacker.interface import ChatBaseModel
from prompt_hacker.model import OpenAIChatModel


class SystemPromptGenerator(OpenAIChatModel):
    """random system message synthetic data generator"""

    def __init__(self) -> None:
        super().__init__()

    def __call__(self, num_examples: int = 5) -> list[str]:
        query = prompts.system_prompt_generator(num_prompts=num_examples)
        return self._generate(query)[0].split(constant.PROMPT_SEPERATOR)


class PigLatinGenerator(OpenAIChatModel):
    """replace sensitive word with pig latin game"""

    def __init__(self) -> None:
        super().__init__()

    def __call__(self, word: str) -> str:
        query = prompts.pig_latin_generator(word)
        return self._generate(query)[0]


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

        for input_ in concated_inputs_:  # TODO : make it async
            answer: str = self.model.run(
                question=input_,
                temperature=self.temperature,
                n=self.sample_size,
                max_tokens=high_temp_seq_length,
            )[0]
            concat_answer = input_ + answer  # concat input + output
            augmented_answers.append(concat_answer)

        return list(set(augmented_answers))


class DisemvowelDecoder(OpenAIChatModel):
    def decode(self, text: str) -> str:
        return self._generate(prompts.disemvowel_decode_prompt(text))[0]
