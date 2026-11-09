> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/inference-and-deployment/deploying-llms-with-hugging-face-jobs.md).

# Deploying LLMs with Hugging Face Jobs

Using Hugging Face jobs and skills to fine-tune LFM with Codex / Claude Code with a SKILL.

This guide covers how to use [Unsloth](https://github.com/unslothai/unsloth) and [Liquid LFM2.5](/docs/models/tutorials/lfm2.5.md) for fast LLM fine-tuning through coding agents like [Claude Code](/docs/basics/claude-code.md). Unsloth provides \~2x faster training and \~60% less VRAM usage compared to standard methods.

### You will need

* A [Hugging Face](https://huggingface.co) account (required for HF Jobs)
* A Hugging Face token with write permissions
* A coding agent (Open Code, Claude Code, Codex)
* Read our [Claude Code](/docs/basics/claude-code.md) guide on setting them up.

### Installing the Skill

#### Claude Code

Claude Code discovers skills through its [plugin system](https://code.claude.com/docs/en/discover-plugins).

1. Add the marketplace:

```bash
/plugin marketplace add huggingface/skills
```

2. Browse available skills in the **Discover** tab:

```bash
/plugin
```

3. Install the model trainer skill:

```bash
/plugin install hugging-face-model-trainer@huggingface-skills
```

For more details, see the [Claude Code plugins docs](https://code.claude.com/docs/en/discover-plugins) and the [Skills docs](https://code.claude.com/docs/en/skills).

#### Codex

Codex discovers skills through [`AGENTS.md`](https://developers.openai.com/codex/guides/agents-md) files and [`.agents/skills/`](https://developers.openai.com/codex/skills) directories.

**Install individual skills with `$skill-installer`**

{% code overflow="wrap" %}

```bash
$skill-installer install https://github.com/huggingface/skills/tree/main/skills/hugging-face-model-trainer
```

{% endcode %}

For more details, see the [Codex Skills docs](https://developers.openai.com/codex/skills) and the [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md).

### Quick Start

Once the skill is installed, ask your coding agent to train a model. We're using [Liquid LFM2.5](/docs/models/tutorials/lfm2.5.md)

{% code overflow="wrap" %}

```
Train LiquidAI/LFM2.5-1.2B-Instruct on trl-lib/Capybara using Unsloth on HF Jobs
```

{% endcode %}

The agent will generate a training script based on an [example in the skill](https://github.com/huggingface/skills/blob/main/skills/hugging-face-model-trainer/scripts/unsloth_sft_example.py), submit the training to HF Jobs, and provide a monitoring link via Trackio.

### Using Hugging Face Jobs

Training jobs will run on [Hugging Face Jobs](https://huggingface.co/docs/huggingface_hub/guides/jobs) — fully managed cloud GPUs. If you are familiar with Google Colab credits, Hugging Face Jobs also offers a similar credits system. It is a Pay As You Go structure, or your can get credits beforehand. The agent:

1. Generates a UV script with inline dependencies
2. Submits it to HF Jobs via the `hf` CLI
3. Reports the job ID and monitoring URL
4. The trained model is pushed to your Hugging Face Hub repository

#### Example Training Script

The skill generates scripts like this:

{% code expandable="true" %}

```py
# /// script
# dependencies = ["unsloth", "trl>=0.12.0", "datasets", "trackio"]
# ///

from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

model, tokenizer = FastLanguageModel.from_pretrained(
    "Qwen/Qwen2.5-0.5B",
    load_in_4bit=True,
    max_seq_length=2048,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=32,
    lora_dropout=0,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
)

dataset = load_dataset("trl-lib/Capybara", split="train")

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    args=SFTConfig(
        output_dir="./output",
        push_to_hub=True,
        hub_model_id="username/my-model",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        num_train_epochs=1,
        learning_rate=2e-4,
        report_to="trackio",
    ),
)

trainer.train()
trainer.push_to_hub()
```

{% endcode %}

The cost for training with Hugging Face Jobs is below:

| Model Size   | Recommended GPU | Approx Cost/hr |
| ------------ | --------------- | -------------- |
| <1B params   | `t4-small`      | \~$0.40        |
| 1-3B params  | `t4-medium`     | \~$0.60        |
| 3-7B params  | `a10g-small`    | \~$1.00        |
| 7-13B params | `a10g-large`    | \~$3.00        |

For a full overview of Hugging Face space pricing, check out the guide [here](https://huggingface.co/docs/hub/en/spaces-overview#hardware-resources).

### Tips for Working with Coding Agents

* Be specific about the model and dataset to use and include Hub IDs (e.g., `Qwen/Qwen2.5-0.5B`, `trl-lib/Capybara`). Agents will search for and validate those combinations.
* Mention Unsloth explicitly if you want it used. Otherwise the agent will decide framework based on model and budget.
* Ask for cost estimates before launching large jobs
* Request Trackio monitoring for real-time loss curves
* Check job status by asking the agent to inspect logs after submission

### Resources

* [Hugging Face Skills Repository](https://github.com/huggingface/skills)

{% embed url="<https://youtu.be/Gh5P4niIFNA>" %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/inference-and-deployment/deploying-llms-with-hugging-face-jobs.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
