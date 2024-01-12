import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from prompt_hacker.attack.jailbreak import JailBreaker, JailBreakEvaluator
from prompt_hacker.interface import ChatBaseModel

load_dotenv(verbose=True)


# make a arbitrary chatbot model
class LLM(ChatBaseModel):
    def __init__(self) -> None:
        self._client = OpenAI()

    def run(self, question: str, **kwargs) -> list[str]:
        input_:list[ChatCompletionMessageParam] = [{"role": "user", "content": question}]
        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.9,
            messages=input_,
        )

        msg = response.choices[0].message.content
        if type(msg) == str : 
            return [msg]
        else : 
            raise ValueError


if __name__ == "__main__":
    model = LLM()
    hacker = JailBreaker(model=model)
    result = hacker.run(sample_size=10, verbose=True, shuffle=True)

    evaluator = JailBreakEvaluator()
    evaluated = evaluator.evaluate(result)
    summary = evaluator.summary(evaluated)

    stat_df = pd.DataFrame(
        [summary.prompt_score],
        index=["defended_ratio"],
    ).T  # the lower defended_ratio means the lower ability to defend against hacking
    stat_df.to_csv("./jailbreak_examples.csv", index=True)
