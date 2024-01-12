from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from prompt_hacker import constant
from prompt_hacker.api_client import ModelClient
from prompt_hacker.interface import ChatBaseModel

load_dotenv(verbose=True)


class OpenAIChatModel(ChatBaseModel):
    """openai model"""

    def __init__(self) -> None:
        super().__init__()
        self._client = OpenAI()

    def _generate(
        self, question: ChatCompletionMessageParam, **kwargs
    ) -> list[str]:
        response = self._client.chat.completions.create(
            **kwargs,
            model=constant.MODEL_NM,
            messages=question,
        )

        msg = response.choices[0].message.content
        return [msg]

    def run(self, question: str, **kwargs) -> list[str]:
        input_ = [{"role": "user", "content": question}]
        return self._generate(input_, **kwargs)


class TemperatureDecaySampling:
    """
    Sampling With A Decaying Temperature' implementation from 'Extracting Training Data from Large Language Models'.
    """

    def __init__(
        self,
        model: ModelClient,
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
