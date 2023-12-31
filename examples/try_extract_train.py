import os, sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import pandas as pd
from prompt_hacker.attack.extract_train import (
    TrainingDataExtractor,
    TrainingDataExtractorEvaluator,
)
from dotenv import load_dotenv

load_dotenv(True)

if __name__ == "__main__":
    extractor = TrainingDataExtractor()
    result = extractor.run(
        prefix_samples=["복귀하는 유저라면 방학에 주로 실시하는 버닝 이벤트나 신직업 사전 생성 이벤트 기간에"]
    )
    evaluator = TrainingDataExtractorEvaluator(train_dataset_path="./data.json")
    evaluated = evaluator.evaluate(results=result)
    report = evaluator.summary(evaluated).model_dump()
    report
