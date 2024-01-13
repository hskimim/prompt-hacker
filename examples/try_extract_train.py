import os
import sys

import pandas as pd
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from prompt_hacker.attack.extract_train import (
    TrainingDataExtractor,  # noqa: E402
    TrainingDataExtractorEvaluator,  # noqa: E402; noqa: E402
)
from prompt_hacker.test.api_client import FewShotTestModelClient  # noqa: E402

load_dotenv(verbose=True)

if __name__ == "__main__":
    extractor = TrainingDataExtractor(FewShotTestModelClient())
    result = extractor.run(
        verbose=True,
        prefix_samples=[
            "graduated at King's College, Cambridge, with a degree in mathematics. Whilst"
        ],
    )
    evaluator = TrainingDataExtractorEvaluator(train_dataset_path="./data.json")
    evaluated = evaluator.evaluate(results=result)
    report = evaluator.summary(evaluated).model_dump()
    pd.DataFrame([report]).T.to_csv("./extract_train_examples.csv", index=True)
