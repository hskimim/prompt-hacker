import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from dotenv import load_dotenv
import pandas as pd
from openai import OpenAI

from prompt_hacker.interface import ChatBaseModel
from prompt_hacker.attack import Hacker, Evaluator


load_dotenv(True)


# make a arbitrary chatbot model
class LLM(ChatBaseModel):
    def __init__(self) -> None:
        self._client = OpenAI()

    def run(self, query: str) -> str:
        input_ = [{"role": "user", "content": query}]
        response = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.9,
            messages=input_,
        )

        msg = response.choices[0].message.content
        return msg


if __name__ == "__main__":
    model = LLM()
    hacker = Hacker(model=model)
    result = hacker.run(sample_size=100, verbose=True, shuffle=True)

    evaluator = Evaluator()
    evaluated = evaluator.evaluate(result)
    summary = evaluator.summary(evaluated)

    stat_df = pd.DataFrame(
        [summary.prompt_score],
        index=["defended_ratio"],
    ).T  # the lower defended_ratio means the lower ability to defend against hacking
    stat_df.to_csv("./test.csv", index=True)
