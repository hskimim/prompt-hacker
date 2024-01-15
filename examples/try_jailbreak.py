import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from prompt_hacker.attack.jailbreak import JailBreaker
from prompt_hacker.evaluate.jailbreak import JailBreakEvaluator
from prompt_hacker.pipe import PipeLine
from prompt_hacker.test.api_client import TestModelClient  # noqa: E402

load_dotenv(verbose=True)


if __name__ == "__main__":
    pipe = PipeLine(
        attacker=JailBreaker(model=TestModelClient()),
        evaluator=JailBreakEvaluator(),
    )
    report = pipe(sample_size=10, verbose=True, shuffle=True)
    print(report)  # score=0.45454545454545453
