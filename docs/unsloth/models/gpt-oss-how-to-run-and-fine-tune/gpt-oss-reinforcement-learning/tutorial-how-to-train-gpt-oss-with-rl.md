> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune/gpt-oss-reinforcement-learning/tutorial-how-to-train-gpt-oss-with-rl.md).

# Tutorial: How to Train gpt-oss with RL

Learn to train OpenAI gpt-oss with GRPO to autonomously beat 2048 locally or on Colab.

LLMs often struggle with tasks that involve complex environments. However, by applying [reinforcement learning](/docs/get-started/reinforcement-learning-rl-guide.md) (RL) and designing a custom [reward function](/docs/get-started/reinforcement-learning-rl-guide.md#reward-functions-verifiers), these challenges can be overcome.

RL can be adapted for tasks such as auto kernel or strategy creation. This tutorial shows how to train **gpt-oss** with [**GRPO**](/docs/get-started/reinforcement-learning-rl-guide.md#from-rlhf-ppo-to-grpo-and-rlvr) and Unsloth to autonomously beat 2048.

| [2048 notebook](https://colab.research.google.com/github/openai/gpt-oss/blob/main/examples/reinforcement-fine-tuning.ipynb) (Official OpenAI example) | [Kernel generation notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-\(20B\)-GRPO.ipynb) |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |

**What you’ll build:**

* Train gpt-oss-20b so the model can automatically win 2048
* Create a minimal 2048 environment the model can interact with
* Define **reward functions** that:
  1. Check the generated strategy compiles and runs,
  2. Prevent reward hacking (disallow external imports), and
  3. Reward actual game success
* Run inference and export the model (MXFP4 4‑bit or merged FP16)

{% hint style="info" %}
**Hardware:** The 2048 example runs on a free Colab T4, but training will be slow. A100/H100 is much faster. 4‑bit loading + LoRA lets you fit a 20B model into modest VRAM.
{% endhint %}

{% stepper %}
{% step %}

#### Install Unsloth

Run this cell at the top of a notebook (works on Colab).

```bash
!pip install --upgrade -qqq uv
try: import numpy; get_numpy = f"numpy=={numpy.__version__}"
except: get_numpy = "numpy"
!uv pip install -qqq \
    "torch>=2.8.0" "triton>=3.4.0" {get_numpy} torchvision bitsandbytes "transformers==4.56.2" \
    "unsloth_zoo[base] @ git+https://github.com/unslothai/unsloth-zoo" \
    "unsloth[base] @ git+https://github.com/unslothai/unsloth" \
    git+https://github.com/triton-lang/triton.git@05b2c186c1b6c9a08375389d5efe9cb4c401c075#subdirectory=python/triton_kernels
!uv pip install --upgrade --no-deps transformers==4.56.2 tokenizers
!uv pip install --no-deps trl==0.22.2
```

{% endstep %}

{% step %}

#### Load gpt-oss with Unsloth

Load the 20B model in 4‑bit QLoRA for memory efficiency, then wrap it with a LoRA adapter. You can also train it in 16-bit LoRA but it will use 4x more memory. For more settings view our [configuration guide](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune/gpt-oss-reinforcement-learning/pages/nw2c1elNySGBBav8WP9B#id-2.-choose-the-right-model--method).

```python
from unsloth import FastLanguageModel
import torch

max_seq_length = 768        # Increase if your task needs longer outputs
lora_rank      = 4          # Higher rank → better but more VRAM/compute

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name        = "unsloth/gpt-oss-20b",  # or unsloth/gpt-oss-20b-BF16 on H100
    max_seq_length    = max_seq_length,
    load_in_4bit      = True,                    # False for 16‑bit
    offload_embedding = True,                    # saves ~1GB VRAM
)

model = FastLanguageModel.get_peft_model(
    model,
    r = lora_rank,
    target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_alpha = lora_rank * 2,
    use_gradient_checkpointing = "unsloth",     # big memory saver
    random_state = 3407,
)
```

{% hint style="info" %}
If you hit OOM, try lowering `max_seq_length`, `lora_rank`, or `num_generations` (later), and keep `load_in_4bit=True`.
{% endhint %}
{% endstep %}

{% step %}

#### 2048 game environment (minimal)

* A `GameBoard` class supporting **W/A/S/D** moves
* Merge/score logic
* `execute_with_time_limit` wrapper so poorly written strategies can’t hang the kernel

You can quickly smoke‑test with a trivial policy:

```python
def always_move_left(board):
    return "W"

steps, outcome = execute_strategy(always_move_left, GameBoard(size=8, seed=42, target=2048, probability_fours=0.10))
```

{% endstep %}

{% step %}

#### Safe code execution & anti‑cheat checks

Generated strategies are **Python functions**. To keep execution safe and prevent reward hacking:

* **Module whitelist check** — only allow Python stdlib symbols:

  ```python
  from unsloth import check_python_modules
  ok, info = check_python_modules("""
  def strategy(board):
      import math
      from typing import Callable
      return "W"
  """)
  # ok == True means only Python‑level imports were used
  ```
* **Block disallowed imports** (e.g., NumPy):

  ```python
  sample = """
  def strategy(board):
      from numpy import matmul
      return "W"
  """
  ok, info = check_python_modules(sample)  # ok => False
  ```
* **Lock down execution** to a sandboxed function:

  ```python
  from unsloth import create_locked_down_function
  function = """
  def add(a, b):
      def adder(a):
          return a + b
      return adder(b) + b
  """
  f = create_locked_down_function(function)  # errors if globals / imports are used
  ```
* **Enforce a hard wall‑clock limit** on strategy runs:

  ```python
  from unsloth import execute_with_time_limit
  @execute_with_time_limit(2)
  def execute_strategy(strategy, game):
      # loop until game ends or timeout
      ...
  ```

{% endstep %}

{% step %}
\### Prompt & dataset

We prompt the model to **emit a short strategy function** inside triple backticks:

````
Create a new short 2048 strategy using only native Python code.
You are given a list of list of numbers for the current board state.
Output one action for "W", "A", "S", "D" on what is the optimal next step.
Output your new short function in backticks using the format below:
```python
def strategy(board):
    return "W"  # Example
````

All helper functions should be inside def strategy. Only output the short function `strategy`.

````

Create a tiny synthetic dataset (reusing the same prompt) and compute the prompt length so GRPO knows how many completion tokens to sample:

```python
from datasets import Dataset

prompt = ...  # as above

maximum_length = len(tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt}], add_generation_prompt=True
))

dataset = Dataset.from_list([
    {"prompt": [{"role": "user", "content": prompt}], "answer": 0, "reasoning_effort": "low"}
] * 1000)
````

{% hint style="info" %} You can replace this dataset with real prompts for your own RL task. {% endhint %} {% endstep %}

{% step %}

#### Reward function time!

1. **Extract the code block** from the model’s reply:

   ````python
   def extract_function(text):
       if text.count("```") >= 2:
           first = text.find("```") + 3
           second = text.find("```", first)
           fx = text[first:second].strip()
           fx = fx.removeprefix("python\n")
           fx = fx[fx.find("def"):]
           if fx.startswith("def strategy(board):"):
               return fx
       return None
   ````
2. **`function_works`** - Does it compile & create a callable?

   ```python
   from unsloth import create_locked_down_function, check_python_modules

   def function_works(completions, **kwargs):
       scores = []
       for completion in completions:
           response = completion[0]["content"]
           function = extract_function(response)
           if function is None:
               scores.append(-2.0)
               continue
           ok, info = check_python_modules(function)
           if "error" in info:
               scores.append(-2.0)
               continue
           try:
               _ = create_locked_down_function(function)
               scores.append(1.0)
           except Exception:
               scores.append(-0.5)
       return scores
   ```
3. **`no_cheating`** - No non‑stdlib imports allowed:

   ```python
   def no_cheating(completions, **kwargs):
       scores = []
       for completion in completions:
           response = completion[0]["content"]
           function = extract_function(response)
           if function is None:
               scores.append(-1.0)
               continue
           ok, _ = check_python_modules(function)
           scores.append(1.0 if ok else -20.0)  # heavy penalty if cheating
       return scores
   ```
4. **`strategy_succeeds`** - Play a random board; reward success:

   ```python
   import numpy as np

   PRINTER = 0  # occasionally print for debugging

   def strategy_succeeds(completions, **kwargs):
       global PRINTER
       scores = []
       seed = np.random.randint(10000)
       for completion in completions:
           response = completion[0]["content"]
           function = extract_function(response)
           if function is None:
               scores.append(-2.0)
               continue
           try:
               new_strategy = create_locked_down_function(function)
           except Exception:
               scores.append(0.0)
               continue
           try:
               game = GameBoard(size=6, seed=seed, target=2048, probability_fours=0.10)
               steps, state = execute_strategy(new_strategy, game)
               if PRINTER % 5 == 0:
                   print(function)
                   print(f"Steps={steps} State={state}")
                   print(game.board().pretty())
               PRINTER += 1
               if state == "success":
                   scores.append(20.0)
               else:
                   scores.append(2.0)   # worked but didn’t reach 2048
           except TimeoutError:
               scores.append(-1.0)      # timed out
           except Exception:
               scores.append(-3.0)      # crashed
       return scores
   ```

{% endstep %}

{% step %}

#### Configure GRPO

We will use the **GRPOTrainer**. Set the prompt/completion lengths, then build a `GRPOConfig`. Keep in mind you could also set the RL algorithm type to others such as [GSPO](/docs/get-started/reinforcement-learning-rl-guide/advanced-rl-documentation/gspo-reinforcement-learning.md) or Dr. GRPO.

```python
from trl import GRPOConfig, GRPOTrainer

max_prompt_length     = maximum_length + 1
max_completion_length = max_seq_length - max_prompt_length

training_args = GRPOConfig(
    temperature=1.0,
    learning_rate=5e-5,
    weight_decay=0.01,
    warmup_ratio=0.1,
    lr_scheduler_type="linear",
    optim="adamw_8bit",
    logging_steps=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1,    # bump to 4 for smoother reward signals
    num_generations=2,                # lower if you OOM
    max_prompt_length=max_prompt_length,
    max_completion_length=max_completion_length,
    max_steps=1000,                   # or set num_train_epochs=1
    save_steps=100,
    report_to="none",
    output_dir="outputs",
)

trainer = GRPOTrainer(
    model=model,
    processing_class=tokenizer,
    reward_funcs=[function_works, no_cheating, strategy_succeeds],
    args=training_args,
    train_dataset=dataset,
    # Optional eval split:
    # train_dataset=new_dataset["train"],
    # eval_dataset=new_dataset["test"],
)
```

{% hint style="info" %} **Reading logs:** Look at `reward` and `reward_std`. It’s normal to see low/zero rewards early (first \~100–200 steps on small GPUs). {% endhint %} {% endstep %}

{% step %}

#### Train your model

```python
trainer.train()
```

This launches the full RL loop: sample completions → score with your rewards → optimize the policy (LoRA). {% endstep %}

{% step %}

#### Inference (after training)

Generate a fresh strategy with the trained adapter:

```python
from transformers import TextStreamer

text = tokenizer.apply_chat_template(
    [{"role": "user", "content": prompt}],
    tokenize=False,
    add_generation_prompt=True,
    reasoning_effort="low",
)

_ = model.generate(
    **tokenizer(text, return_tensors="pt").to("cuda"),
    temperature=1.0,
    max_new_tokens=1024,
    streamer=TextStreamer(tokenizer, skip_prompt=False)
```

{% endstep %}

{% step %}

#### Save / Export your fine-tuned mode

* **Merge & save 4‑bit (MXFP4)**

  ```
  ```

python model.save\_pretrained\_merged("finetuned\_model", tokenizer, save\_method="mxfp4") # or push model.push\_to\_hub\_merged("\<org\_or\_user>/", tokenizer, token="\<hf\_token>", save\_method="mxfp4") \`\`\`

* **Merge & save 16‑bit**

  ```python
  model.save_pretrained_merged("finetuned_model", tokenizer, save_method="merged_16bit")
  # or push
  model.push_to_hub_merged("<org_or_user>/<repo>", tokenizer, token="<hf_token>", save_method="merged_16bit")
  ```

{% endstep %}

{% step %}

#### Troubleshooting & tips

* **OOM / slow**: reduce `max_seq_length`, `num_generations`, `lora_rank`; keep 4‑bit; try A100 if available.
* **No reward improvement**: increase training steps, soften penalties, or add curriculum (start with smaller boards / lower targets).
* **Reward hacking**: keep `check_python_modules` strict; validate strategy behavior across multiple random seeds.
* **Unstable training**: raise `gradient_accumulation_steps` to smooth updates; lower `learning_rate` (e.g., 2e‑5).
* **Long hangs**: ensure `execute_with_time_limit` wraps any strategy execution.
  {% endstep %}

{% step %}

#### Adapt to your own RL task

* Replace the 2048 env with your own environment and **three rewards**: (a) syntax/compilation, (b) anti‑cheat/safety, (c) task success.
* Update the **prompt** to request the kind of function or output you need.
* Keep the same Unsloth + GRPO scaffolding; only swap the env and rewards.
  {% endstep %}
  {% endstepper %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune/gpt-oss-reinforcement-learning/tutorial-how-to-train-gpt-oss-with-rl.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
