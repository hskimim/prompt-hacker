import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from prompt_hacker.attack.jailbreak import JailBreaker, JailBreakEvaluator
from prompt_hacker.schemas import JailBreakInputs
from prompt_hacker.test.api_client import TestModelClient  # noqa: E402

load_dotenv(verbose=True)


if __name__ == "__main__":
    attacker = JailBreaker(TestModelClient())
    result = attacker.run(JailBreakInputs(sample_size=50, use_async=True))

    evaluator = JailBreakEvaluator()
    evaluated = evaluator.evaluate(result)
    summary = evaluator.summary(evaluated)

    metrics = evaluator.evaluation_metric
    jailbreak_result_df = evaluator.evaluate2df(evaluated)

    print(summary)  # Evaluation(score=0.5)
