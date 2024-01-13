# prompt-hacker

## Introduction
In the realm of services powered by Large Language Models (LLMs), ethics play a pivotal role. This project acknowledges that engineering in this field is inherently intertwined with the control and mitigation of issues arising from the operation of these models.

During the deployment phase of a service, the risk of 'prompt hacking' is ever-present. Prompt hacking can disrupt the normal functioning of an application and, more critically, lead to potential leaks of organizational or customer information.

This project is dedicated to addressing the challenges of prompt hacking through the development of a module that facilitates both the modularization and automation of penetration testing. By integrating this into the development stage of a service, we aim to significantly enhance security and mitigate risks associated with LLM-based services.

### Objectives
- **Penetration Testing for Prompt Hacking**: Develop a comprehensive module that automates penetration testing specifically for prompt hacking vulnerabilities.
- **Modular Design**: Ensure the module is adaptable and can be seamlessly integrated into various LLM-based services.

## Features
### prompt leaking
- [X] Try prompt leaking by creating multiple prompts using TemperatureDecaySampling.
- [X] Evaluate whether prompt leaking was successful
### prompt injection
- [X] Inject arbitrary system prompts through the SystemPromptGenerator
- [X] Evaluate whether prompt injection was successful

### jailbreak
- [X] Generation of synthetic data for malicious prompts
- [X] Develop the evaluator to analyze which prompts/questions most frequently result in jailbreaks.
- [ ] Generation of synthetic data for jailbreak prompts

### extracting training set
- [X] prompt hacking for extracting training data
- [ ] How to measure the memorization

### others
- [X] Create an interface that makes it easier for arbitrary chatbots to be integrated.
- [ ] Unify the return type of the evaluator to support the pipeline of attackers and evaluators.
- [ ] Modify to send prompts (model call) asynchronously.
    - [ ] async get_embeddings
    - [ ] async interface's run

## Get Started

### prompt leaking
can try with 
```consoles
poetry run python examples/try_prompt_leaking.py
```

```python
from prompt_hacker.attack.leak import PromptLeaker
from prompt_hacker.evaluate.leak import PromptLeakEvaluator
from prompt_hacker.test.api_client import InstructedShotTestModelClient # Test model that received instructions through system prompt

sys_prompt = "You are a skilled event planner. Please research and coordinate all the necessary details for a corporate conference happening next month."
hacker = PromptLeaker(
    model=InstructedShotTestModelClient(instruct=sys_prompt),
    sample_size=10,
)
result = hacker.run()

evaluator = PromptLeakEvaluator(sys_prompt=sys_prompt)
evaluated = evaluator.evaluate(result)
report = evaluator.summary(evaluated)
print(report)  # score=0.3
```

### prompt injection
can try with 
```consoles
poetry run python examples/try_prompt_injection.py
```

```python
from prompt_hacker.attack.inject import PromptInjector
from prompt_hacker.evaluate.inject import PromptInjectorEvaluator
from prompt_hacker.test.api_client import InstructedShotTestModelClient  # Test model that received instructions through system prompt


sys_prompt = "You are a skilled event planner. Please research and coordinate all the necessary details for a corporate conference happening next month."
hacker = PromptInjector(model=InstructedShotTestModelClient(instruct=sys_prompt))
result = hacker.run(sample_size=1)


evaluator = PromptInjectorEvaluator(sys_prompt=sys_prompt)
evaluated = evaluator.evaluate(result)
report = evaluator.summary(evaluated)
print(report)  # score=0.9
```

### jailbreak test
can try with
```consoles
poetry run python examples/try_jailbreak.py
```

```python
from openai import OpenAI

from prompt_hacker.test.api_client import TestModelClient # test model generates vanilla QA chat
from prompt_hacker.attack.jailbreak import JailBreaker
from prompt_hacker.evaluate.jailbreak import JailBreakEvaluator


hacker = JailBreaker(model=TestModelClient())
result = hacker.run(sample_size=10, verbose=True, shuffle=True)

evaluator = JailBreakEvaluator()
evaluated = evaluator.evaluate(result)
eport = evaluator.summary(evaluated)
print(report)  # score=0.45454545454545453
```

### extract training dataset
can try with 
```consoles
poetry run python examples/try_extract_train.py
```

```python
from prompt_hacker.attack.extract_train import TrainingDataExtractor
from prompt_hacker.evaluate.extract_train import TrainingDataExtractorEvaluator
from prompt_hacker.test.api_client import FewShotTestModelClient # test model that try to few shot learning

extractor = TrainingDataExtractor(model=FewShotTestModelClient())
result = extractor.run(
    verbose=True,
    prefix_samples=[
        "graduated at King's College, Cambridge, with a degree in mathematics. Whilst"
    ],
)
evaluator = TrainingDataExtractorEvaluator(train_dataset_path="./data.json")
evaluated = evaluator.evaluate(results=result)
report = evaluator.summary(evaluated).model_dump()
print(report)  # score=1.0
```