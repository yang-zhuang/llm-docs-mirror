> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/install/intel.md).

# Fine-tuning LLMs on Intel GPUs with Unsloth

Learn how to train and fine-tune large language models on Intel GPUs.

You can now fine-tune LLMs on your local Intel device with Unsloth! Read our guide on exactly how to get started with training your own custom model.

Before you begin, make sure you have:

* **Intel GPU:** Data Center GPU Max Series, Arc Series, or Intel Ultra AIPC
* **OS:** Linux (Ubuntu 22.04+ recommended) or Windows 11 (recommended)
* **Windows only:** Install Intel oneAPI Base Toolkit 2025.2.1 (select version 2025.2.1)
* **Intel Graphics driver:** Latest recommended driver for Windows/Linux
* **Python:** 3.10+

{% hint style="info" %}
Installing Unsloth Studio on an Intel GPU? See [Intel GPUs in the Studio install guide](/docs/new/studio/install.md#intel-gpus) for when the installer picks XPU PyTorch by itself and how to pin it.
{% endhint %}

### Build Unsloth with Intel Support

{% stepper %}
{% step %}

#### Create a new conda environment (Optional)

```bash
conda create -n unsloth-xpu python==3.10
conda activate unsloth-xpu
```

{% endstep %}

{% step %}

#### Install Unsloth

```bash
git clone https://github.com/unslothai/unsloth.git
cd unsloth
pip install .[intel-gpu-torch290]
```

{% hint style="info" %}
Linux Only: Install [vLLM](/docs/basics/inference-and-deployment/vllm-guide.md) (Optional)\
You can also install vLLM for [inference](/docs/basics/inference-and-deployment.md) and [RL](/docs/get-started/reinforcement-learning-rl-guide.md). Please follow [vLLM's guide](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/#intel-xpu).
{% endhint %}
{% endstep %}

{% step %}

#### Verify your environments

```python
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"XPU available: {torch.xpu.is_available()}")
print(f"XPU device count: {torch.xpu.device_count()}")
print(f"XPU device name: {torch.xpu.get_device_name(0)}")
```

{% endstep %}

{% step %}

#### Start fine-tuning.

You can directly use our Unsloth [notebooks](/docs/get-started/unsloth-notebooks.md) or view our dedicated [fine-tuning](/docs/get-started/fine-tuning-llms-guide.md) or [reinforcement learning](/docs/get-started/reinforcement-learning-rl-guide.md) guides.
{% endstep %}
{% endstepper %}

### Windows Only - Runtime Configurations

In Command Prompt with Administrator privilege, enable long path support in the Windows registry:

```bash
powershell -Command "Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\FileSystem" -Name "LongPathsEnabled" -Value 1
```

This command only needs to be set once on a single machine. It does not need to be configured before each run. Then:

1. Download level-zero-win-sdk-1.20.2.zip from [GitHub](https://github.com/oneapi-src/level-zero/releases/tag/v1.20.2)
2. Unzip the level-zero-win-sdk-1.20.2.zip
3. In Command Prompt, under conda environment unsloth-xpu:

```bash
call "C:\Program Files (x86)\Intel\oneAPI\setvars.bat" -
set ZE_PATH=path\to\the\unzipped\level-zero-win-sdk-1.20.2
```

### Example 1: QLoRA Fine-tuning with SFT

This example demonstrates how to fine-tune a Qwen3-32B model using 4-bit QLoRA on an Intel GPU. QLoRA significantly reduces memory requirements, making it possible to fine-tune large models on consumer-grade hardware.

{% code expandable="true" %}

```python
from unsloth import FastLanguageModel, FastModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
max_seq_length = 2048 # Supports RoPE Scaling internally, so choose any!
# Get LAION dataset
url = "https://huggingface.co/datasets/laion/OIG/resolve/main/unified_chip2.jsonl"
dataset = load_dataset("json", data_files = {"train" :
url}, split = "train")

# 4bit pre quantized models we support for fast downloading + no OOMs.
fourbit_models = [
"unsloth/Qwen3-32B-bnb-4bit",
"unsloth/Qwen3-14B-bnb-4bit",
"unsloth/Qwen3-8B-bnb-4bit",
"unsloth/Qwen3-4B-bnb-4bit",
"unsloth/Qwen3-1.7B-bnb-4bit",
"unsloth/Qwen3-0.6B-bnb-4bit",
# "unsloth/Qwen2.5-32B-bnb-4bit",
# "unsloth/Qwen2.5-14B-bnb-4bit",
# "unsloth/Qwen2.5-7B-bnb-4bit",
# "unsloth/Qwen2.5-3B-bnb-4bit",
# "unsloth/Qwen2.5-1.5B-bnb-4bit",
# "unsloth/Qwen2.5-0.5B-bnb-4bit",
# "unsloth/Llama-3.2-3B-bnb-4bit",
# "unsloth/Llama-3.2-1B-bnb-4bit",
# "unsloth/Llama-3.1-8B-bnb-4bit",
# "unsloth/Llama-3.1-70B-bnb-4bit",
# "unsloth/mistral-7b-bnb-4bit",
# "unsloth/Phi-4",
# "unsloth/Phi-3.5-mini-instruct",
# "unsloth/Phi-3-medium-4k-instruct",
# "unsloth/Phi-3-mini-4k-instruct",
# "unsloth/gemma-2-9b-bnb-4bit",
# "unsloth/gemma-2-27b-bnb-4bit",
] # More models at https://huggingface.co/unsloth

model, tokenizer = FastLanguageModel.from_pretrained(
model_name = "unsloth/Qwen3-32B-bnb-4bit",
max_seq_length = max_seq_length,
load_in_4bit = True,
# token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
)

model = FastLanguageModel.get_peft_model(
model,
r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
"gate_proj", "up_proj", "down_proj",
],
lora_alpha = 16,
lora_dropout = 0, # Supports any, but = 0 is optimized
bias = "none", # Supports any, but = "none" is optimized
use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
random_state = 3407,
use_rslora = False, # We support rank stabilized LoRA
loftq_config = None, # And LoftQ
)

trainer = SFTTrainer(
model = model,
tokenizer = tokenizer,
train_dataset = dataset,
dataset_text_field = "text",
max_seq_length = max_seq_length,
dataset_num_proc = 1, # Recommended on Windows
packing = False, # Can make training 5x faster for short sequences.
args = SFTConfig(
per_device_train_batch_size = 2,
gradient_accumulation_steps = 4,
warmup_steps = 5,
max_steps = 60,
learning_rate = 2e-4,
logging_steps = 1,
optim = "adamw_8bit",
weight_decay = 0.01,
lr_scheduler_type = "linear",
seed = 3407,
dataset_num_proc=1, # Recommended on Windows
),
)

trainer.train()
```

{% endcode %}

### Example 2: Reinforcement Learning GRPO

GRPO is a [reinforcement learning](/docs/get-started/reinforcement-learning-rl-guide.md) technique for aligning language models with human preferences. This example shows how to train a model to follow a specific XML output format using multiple reward functions.

#### What is GRPO?

GRPO improves upon traditional RLHF by:

* Using group-based normalization for more stable training
* Supporting multiple reward functions for multi-objective optimization
* Being more memory efficient than PPO

{% code expandable="true" %}

```python
from unsloth import FastLanguageModel
import re
from trl import GRPOConfig, GRPOTrainer
from datasets import load_dataset, Dataset

max_seq_length = 1024  # Can increase for longer reasoning traces
lora_rank = 32  # Larger rank = smarter, but slower
max_prompt_length = 256

# Load and prep dataset
SYSTEM_PROMPT = """
Respond in the following format:
<reasoning>
...
</reasoning>
<answer>
...
</answer>
"""

XML_COT_FORMAT = """\
<reasoning>
{reasoning}
</reasoning>
<answer>
{answer}
</answer>
"""


def extract_xml_answer(text: str) -> str:
    answer = text.split("<answer>")[-1]
    answer = answer.split("</answer>")[0]
    return answer.strip()


def extract_hash_answer(text: str) -> str | None:
    if "####" not in text:
        return None
    return text.split("####")[1].strip()


# uncomment middle messages for 1-shot prompting
def get_gsm8k_questions(split: str = "train") -> Dataset:
    data = load_dataset("openai/gsm8k", "main")[split]  # type: ignore
    data = data.map(
        lambda x: {  # type: ignore
            "prompt": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": x["question"]},
            ],
            "answer": extract_hash_answer(x["answer"]),
        }
    )  # type: ignore
    return data  # type: ignore


# Reward functions
def correctness_reward_func(prompts, completions, answer, **kwargs) -> list[float]:
    responses = [completion[0]["content"] for completion in completions]
    q = prompts[0][-1]["content"]
    extracted_responses = [extract_xml_answer(r) for r in responses]
    print(
        "-" * 20,
        f"Question:\n{q}",
        f"\nAnswer:\n{answer[0]}",
        f"\nResponse:\n{responses[0]}",
        f"\nExtracted:\n{extracted_responses[0]}",
    )
    return [2.0 if r == a else 0.0 for r, a in zip(extracted_responses, answer)]


def int_reward_func(completions, **kwargs) -> list[float]:
    responses = [completion[0]["content"] for completion in completions]
    extracted_responses = [extract_xml_answer(r) for r in responses]
    return [0.5 if r.isdigit() else 0.0 for r in extracted_responses]


def strict_format_reward_func(completions, **kwargs) -> list[float]:
    """Reward function that checks if the completion has a specific format."""
    pattern = r"^<reasoning>\n.*?\n</reasoning>\n<answer>\n.*?\n</answer>\n$"
    responses = [completion[0]["content"] for completion in completions]
    matches = [re.match(pattern, r) for r in responses]
    return [0.5 if match else 0.0 for match in matches]


def soft_format_reward_func(completions, **kwargs) -> list[float]:
    """Reward function that checks if the completion has a specific format."""
    pattern = r"<reasoning>.*?</reasoning>\s*<answer>.*?</answer>"
    responses = [completion[0]["content"] for completion in completions]
    matches = [re.match(pattern, r) for r in responses]
    return [0.5 if match else 0.0 for match in matches]


def count_xml(text: str) -> float:
    count = 0.0
    if text.count("<reasoning>\n") == 1:
        count += 0.125
    if text.count("\n</reasoning>\n") == 1:
        count += 0.125
    if text.count("\n<answer>\n") == 1:
        count += 0.125
    count -= len(text.split("\n</answer>\n")[-1]) * 0.001
    if text.count("\n</answer>") == 1:
        count += 0.125
    count -= (len(text.split("\n</answer>")[-1]) - 1) * 0.001
    return count


def xmlcount_reward_func(completions, **kwargs) -> list[float]:
    contents = [completion[0]["content"] for completion in completions]
    return [count_xml(c) for c in contents]


if __name__ == "__main__":
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/Qwen3-0.6B",
        max_seq_length=max_seq_length,
        load_in_4bit=False,  # False for LoRA 16bit
        fast_inference=False,  # Enable vLLM fast inference
        max_lora_rank=lora_rank,
        gpu_memory_utilization=0.7,  # Reduce if out of memory
        device_map="xpu:0",
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=lora_rank,  # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],  # Remove QKVO if out of memory
        lora_alpha=lora_rank,
        use_gradient_checkpointing="unsloth",  # Enable long context finetuning
        random_state=3407,
    )

    dataset = get_gsm8k_questions()

    training_args = GRPOConfig(
        learning_rate=5e-6,
        adam_beta1=0.9,
        adam_beta2=0.99,
        weight_decay=0.1,
        warmup_ratio=0.1,
        lr_scheduler_type="cosine",
        optim="adamw_torch",
        logging_steps=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,  # Increase to 4 for smoother training
        num_generations=4,  # Decrease if out of memory
        max_prompt_length=max_prompt_length,
        max_completion_length=max_seq_length - max_prompt_length,
        # num_train_epochs=1,  # Set to 1 for a full training run
        max_steps=20,
        save_steps=250,
        max_grad_norm=0.1,
        report_to="none",  # Can use Weights & Biases
        output_dir="outputs",
    )

    trainer = GRPOTrainer(
        model=model,
        processing_class=tokenizer,
        reward_funcs=[
            xmlcount_reward_func,
            soft_format_reward_func,
            strict_format_reward_func,
            int_reward_func,
            correctness_reward_func,
        ],
        args=training_args,
        train_dataset=dataset,
        dataset_num_proc=1,  # Recommended on Windows
    )

    trainer.train()

```

{% endcode %}

## Troubleshooting

### Out of Memory (OOM) Errors

If you run out of memory, try these solutions:

1. **Reduce batch size:** Lower `per_device_train_batch_size`.
2. **Use a smaller model:** Start with a smaller model to reduce memory requirements.
3. **Reduce sequence length:** Lower `max_seq_length`.
4. **Reduce LoRA rank:** Use `r=8` instead of `r=16` or `r=32`.
5. **For GRPO, reduce number of generations:** Lower `num_generations`.

### (Windows Only) Intel Ultra AIPC iGPU Shared Memory

For Intel Ultra AIPC with recent GPU drivers on Windows, the shared GPU memory for the integrated GPU typically defaults to **57%** of system memory. For larger models (e.g., **Qwen3-32B**), or when using longer max sequence length, larger batch size, LoRA adapters with larger LoRA rank, etc., during fine-tuning, you could increase available VRAM by raising the percentage of system memory allocated to the iGPU.

You can adjust this by modifying the registry:

* Path: `Computer\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers\MemoryManager`
* Key to change:\
  `SystemPartitionCommitLimitPercentage` (set to a larger percentage)


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/install/intel.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
