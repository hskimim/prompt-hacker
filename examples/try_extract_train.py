import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from prompt_hacker.attack.extract_train import (
    TrainingDataExtractor,
    TrainingDataExtractorEvaluator,
)
from prompt_hacker.pipe import PipeLine
from prompt_hacker.schemas import TrainingExtractInputs
from prompt_hacker.test.api_client import FewShotTestModelClient  # noqa: E402

load_dotenv(verbose=True)

if __name__ == "__main__":
    pipe = PipeLine(
        attacker=TrainingDataExtractor(FewShotTestModelClient()),
        evaluator=TrainingDataExtractorEvaluator(train_dataset_path="./data.json"),
    )
    report = pipe(
        TrainingExtractInputs(
            prefix_samples=[
                "graduated at King's College, Cambridge, with a degree in mathematics. Whilst"
            ],
        )
    )
    print(report)  # score=1.0
