import os
import sys

import pandas as pd
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from prompt_hacker.attack.jailbreak import (
    JailBreaker,  # noqa: E402
    JailBreakEvaluator,  # noqa: E402; noqa: E402
)
from prompt_hacker.test.api_client import TestModelClient  # noqa: E402

load_dotenv(verbose=True)


if __name__ == "__main__":
    hacker = JailBreaker(model=TestModelClient())
    result = hacker.run(sample_size=10, verbose=True, shuffle=True)

    evaluator = JailBreakEvaluator()
    evaluated = evaluator.evaluate(result)
    summary = evaluator.summary(evaluated)

    stat_df = pd.DataFrame(
        [summary.prompt_score],
        index=["defended_ratio"],
    ).T  # the lower defended_ratio means the lower ability to defend against hacking
    stat_df.to_csv("./jailbreak_examples.csv", index=True)
