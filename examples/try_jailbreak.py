import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from prompt_hacker.attack.jailbreak import JailBreaker, JailBreakEvaluator
from prompt_hacker.pipe import PipeLine
from prompt_hacker.schemas import JailBreakInputs
from prompt_hacker.test.api_client import TestModelClient  # noqa: E402

load_dotenv(verbose=True)


if __name__ == "__main__":
    pipe = PipeLine(
        attacker=JailBreaker(model=TestModelClient()),
        evaluator=JailBreakEvaluator(),
    )
    report = pipe(JailBreakInputs(sample_size=10))
    print(report)  # score=0.45454545454545453
