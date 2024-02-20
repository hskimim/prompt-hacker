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
- [ ] Try multiple times to sample prompt since LLM used to make result under stochastic term

### prompt injection
- [X] Inject arbitrary system prompts through the SystemPromptGenerator
- [X] Evaluate whether prompt injection was successful
- [ ] Try multiple times to sample prompt since LLM used to make result under stochastic term

### jailbreak
- [X] Generation of synthetic data for malicious prompts
- [X] Develop the evaluator to analyze which prompts/questions most frequently result in jailbreaks.
- [ ] Generation of synthetic data for jailbreak prompts
- [ ] Try multiple times to sample prompt since LLM used to make result under stochastic term
  
### others
- [X] Create an interface that makes it easier for arbitrary chatbots to be integrated.
- [X] Pipeline design that allows you to use various attackers on a single model and receive results
- [X] Unify the return type of the evaluator to support the pipeline of attackers and evaluators.
- [ ] Make some benchmarks using open/close model such as chatgpt, llama etc
- [X] Modify to send prompts (model call) asynchronously.
    - [X] async interface's run
    - [ ] unify async interface with sync
- [ ] Make understandable CLI during progress

## Get Started

### jailbreak test
can try with
```consoles
poetry run python examples/try_jailbreak.py
```

```python
from openai import OpenAI

from prompt_hacker.test.api_client import TestModelClient
from prompt_hacker.schemas import JailBreakInputs
from prompt_hacker.attack.jailbreak import JailBreaker, JailBreakEvaluator

attacker = JailBreaker(TestModelClient())
result = attacker.run(JailBreakInputs(sample_size=50, use_async=True))

evaluator = JailBreakEvaluator()
evaluated = evaluator.evaluate(result)
summary = evaluator.summary(evaluated)

metrics = evaluator.evaluation_metric
jailbreak_result_df = evaluator.evaluate2df(evaluated)

print(summary)  # Evaluation(score=0.5)
```

### prompt leaking
can try with 
```consoles
poetry run python examples/try_prompt_leaking.py
```

```python
from prompt_hacker.attack.leak import PromptLeaker, PromptLeakEvaluator
from prompt_hacker.test.api_client import InstructedTestModelClient
from prompt_hacker.schemas import PromptLeakInputs
from prompt_hacker.pipe import PipeLine

sys_prompt = "You are a skilled event planner. Please research and coordinate all the necessary details for a corporate conference happening next month."

attacker = PromptLeaker(model=InstructedTestModelClient(instruct=sys_prompt))
result = attacker.run(PromptLeakInputs())

evaluator = PromptLeakEvaluator(sys_prompt=sys_prompt)
evaluated = evaluator.evaluate(result)
summary = evaluator.summary(evaluated)
print(summary)  # Evaluation(score=0.8)
```

### prompt injection
can try with 
```consoles
poetry run python examples/try_prompt_injection.py
```

```python
from prompt_hacker.attack.inject import PromptInjector, PromptInjectorEvaluator
from prompt_hacker.test.api_client import InstructedTestModelClient 
from prompt_hacker.schemas import PromptInjectInputs
from prompt_hacker.pipe import PipeLine

sys_prompt = "You are a skilled event planner. Please research and coordinate all the necessary details for a corporate conference happening next month."

attacker = PromptInjector(model=InstructedTestModelClient(instruct=sys_prompt))
result = attacker.run(PromptInjectInputs())

evaluator = PromptInjectorEvaluator()
evaluated = evaluator.evaluate(result)
summary = evaluator.summary(evaluated)
print(summary)  # Evaluation(score=0.14285714285714285)
```