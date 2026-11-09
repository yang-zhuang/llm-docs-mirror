> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth.md).

# Train your own Decision Model with Unsloth

Fine-tune LLMs like Qwen and Gemma to make decisions with calibrated probabilities.

You can now train your own decision model like **Jev**, **Laya** and **Clef** with Unsloth. Learn how to fine-tune [Qwen3.8](/docs/models/qwen3.8.md) and [Gemma 4](/docs/models/gemma-4.md) LLMs, design effective dataset formats, and transform them into [decision-making](/docs/models/decision-laya.md) models that **make decisions** instead of generating text. The fine-tuned model reads your input, scores the options you provide and returns a choice with a probability.

<a href="/docs/basics/train-your-own-decision-model-with-unsloth.md#train-in-unsloth" class="button secondary">Training Guide</a><a href="/docs/basics/train-your-own-decision-model-with-unsloth.md#dataset-format" class="button secondary">Dataset Guide</a><a href="/docs/models/decision-laya.md" class="button secondary">Decisions API + Serving Guide</a>

See table for benchmarks after training:

| Model        | typed-decisions | BANKING77     | CLINC150       | Holdout acc |
| ------------ | --------------- | ------------- | -------------- | ----------- |
| Qwen3.5-0.8B | 36% -> **73%**  | 7% -> **74%** | 19% -> **76%** | 78%         |
| Qwen3.5-2B   | 33% -> **78%**  | 1% -> 58%     | 1% -> 62%      | 81%         |

{% columns %}
{% column %}
We fine-tuned LLMs with a Clef head using LoRA (r=64) for just one epoch, boosting downstream accuracy from 30–37% (which is roughly chance level) to **as high as 78%**.

Training uses the same dataset format as Laya and Clef. Test sets were **decontaminated** against the training data.
{% endcolumn %}

{% column %}
{% embed url="<https://github.com/user-attachments/assets/92959172-d2a2-450b-a5bf-6369a1e5ae16>" %}
{% endcolumn %}
{% endcolumns %}

**All models** work as well - and you can also **further** fine-tune Decision models like Laya / Clef.

| Model             | Test accuracy | VRAM   | Training time |
| ----------------- | ------------- | ------ | ------------- |
| Qwen3.5-0.8B      | 78%           | 4GB    | 42 min        |
| Qwen3.5-2B        | 81%           | 8GB    | 40 min        |
| Llama 3.2 3B      | 79%           | 4.1GB  | 30 min        |
| Gemma 4 E4B       | 77%           | 14.4GB | 49 min        |
| Laya (fine-tuned) | 77%           | 2.5GB  | 10 min        |

We used a mix of **12 sources**, plus `typed-decisions`: `ag_news`, `arc`, `banking77`, `boolq`, `clinc150`, `commonsense_qa`, `mmlu`, `mnli`, `prompt_injections`, `snli`, `sst5` and `wanli`. The **test set contained 3,000 rows**: 2000 from typed-decisions, 500 from BANKING77 and 500 from CLINC150.

### 🦥 Train in Unsloth

{% stepper %}
{% step %}

#### **Setup Unsloth**

The easiest way to get started is by downloading the [Unsloth Desktop app](/docs/desktop.md). Works on [macOS](/docs/get-started/install/mac.md), [Windows](/docs/get-started/install/windows-installation.md), and [Linux](/docs/get-started/install/linux.md).

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

Or, if you prefer to install manually:

MacOS, Linux, WSL:

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

Windows PowerShell:

```bash
irm https://unsloth.ai/install.ps1 | iex
```

{% endstep %}

{% step %}

#### **Select your model and dataset**

Open the Train tab and pick an LLM, like `unsloth/Qwen3.5-4B`. Then set **Train as** to **Decision model**. Unsloth fills in settings that work well. To match our results, set epochs to 2, LoRA rank to 16 and learning rate to 2e-4.

Upload a file or pick a dataset from Hugging Face, in the dataset format. For typed-decisions, set **Subset** to `all`.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FYL0pJRBFmFO0U1kjhv25%2F1-train-as-decision-model.png?alt=media&amp;token=bace6a9c-4c15-4794-b4ab-b2997014d5b6" alt="" width="375"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### **Start training**

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fcj5kfa0UJdty3SCM27dM%2F2-training-finished.png?alt=media&amp;token=4c1891e0-904a-4ca6-a9b4-7f2f5f059d35" alt=""><figcaption></figcaption></figure>

Click **Start Training**. Unsloth reports accuracy on held-out decisions before and after training, and calibrates the model's confidence.
{% endstep %}

{% step %}

#### **Run it in the Decision API**

Click **Use in Decision API**. Requests that use `laya`, `default` or `jev-latest` now go to your model.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FvzeWCbrxYPdTJFKI6dYg%2Fimage.png?alt=media&amp;token=5fd18788-4d63-4515-bd25-c0b8ebad75de" alt=""><figcaption></figcaption></figure>

Your model also shows up by its run name in Settings → API, under Decision API → Model.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FHR6LKi4f1NiVvClJTtc7%2F4-settings-api-model.png?alt=media&amp;token=bcc74621-c635-4feb-bfb3-50a45f411b4d" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}
You can also play with the trained decision model via the "Try It" option in the Decision API:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FqYXH1FE3U5feaT7QLUjA%2Fimage.png?alt=media&amp;token=37f1ee77-9a66-4821-86aa-7aa0da123d91" alt="" width="563"><figcaption></figcaption></figure>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FWvV5wGT1mqZaW4Ylbu0R%2Fimage.png?alt=media&amp;token=52500d48-0707-426d-bca9-a314bc9e29d3" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### 📒 Use our free notebooks

You can train your own decision model completely for free using our Google Colab or Kaggle notebooks. Colab and Kaggle both offer generous free GPU compute as long as you have a Google account. In these notebooks there is a step-by-step workflow you can work through and we show you how to data prep, train the actual model (in this case Qwen3.5-4B) and export it.

* Fine-tune Qwen3.5-4B into a decision model via our free notebooks:

| [**Google Colab** notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_5_\(4B\)-Decision.ipynb) | [**Kaggle** notebook](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Qwen3_5_\(4B\)-Decision.ipynb\&accelerator=nvidiaTeslaT4) |
| ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

You can also use our free Unsloth Studio notebook, to train a decision model with a UI interface:

{% embed url="<https://colab.research.google.com/github/unslothai/unsloth/blob/main/studio/Unsloth_Studio_Colab.ipynb>" %}

### 📈 Dataset Guide

Decision-model datasets contain an input, questions about that input, and the correct answers. Each row uses three fields:

| Field       | What it contains                                                       |
| ----------- | ---------------------------------------------------------------------- |
| `state`     | The input, such as a customer message.                                 |
| `questions` | What the model should decide, with instructions and available options. |
| `gold`      | The correct answer to each question.                                   |

Each row can contain several questions. `questions` and `gold` can be Python dictionaries or JSON-encoded strings.

**Question types**

| Type     | What it does                                   | Gold answer                                             |
| -------- | ---------------------------------------------- | ------------------------------------------------------- |
| `choice` | Picks an option from `criteria`.               | The option key, such as `"billing"`.                    |
| `noul`   | Answers yes or no.                             | `True` or `False` in Python; `true` or `false` in JSON. |
| `score`  | Picks a level from an ordered `criteria` list. | The level's index, starting at `0`.                     |

**Example: support tickets**

This example uses the support-ticket questions from our [decision-model notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_5_%284B%29-Decision.ipynb), with training labels and two additional sample tickets.

{% code expandable="true" %}

```python
questions = {
    "team": {
        "type": "choice",
        "instructions": "Which team should handle this?",
        "criteria": {
            "billing": "invoices, payments, refunds",
            "technical": "bugs, outages, errors",
            "sales": "pricing, new plans",
        },
    },
    "refund": {
        "type": "noul",
        "instructions": "Does the customer ask for a refund?",
    },
    "urgency": {
        "type": "score",
        "instructions": "How urgent is this?",
        "criteria": ["not urgent", "soon", "today"],
    },
}

rows = [
    {
        "state": "Hi, I was charged twice for invoice #4411. Please refund the duplicate today.",
        "questions": questions,
        "gold": {"team": "billing", "refund": True, "urgency": 2},
    },
    {
        "state": "The dashboard shows an error when I export a report. Please help in the next few days.",
        "questions": questions,
        "gold": {"team": "technical", "refund": False, "urgency": 1},
    },
    {
        "state": "Could you send pricing for your business plan? We are researching for next year; no rush.",
        "questions": questions,
        "gold": {"team": "sales", "refund": False, "urgency": 0},
    },
]
```

{% endcode %}

Each question needs a matching answer in `gold`. Choice answers must match a key in `criteria`. Score labels start at `0`, so `"urgency": 2` means `"today"`.

Keep inputs in `state` and answers in `gold`. These rows illustrate the format; add more examples covering your use case before training.

### 🎯 Make decisions

Give `predict` an input and the questions to decide, in the same format as your dataset:

{% code expandable="true" %}

```python
FastDecisionModel.for_inference(model)
answers = FastDecisionModel.predict(
    model,
    tokenizer,
    "Hi, I was charged twice for invoice #4411. Please refund the duplicate today.",
    {
        "team": {
            "type": "choice",
            "instructions": "Which team should handle this?",
            "criteria": {
                "billing": "invoices, payments, refunds",
                "technical": "bugs, outages, errors",
                "sales": "pricing, new plans",
            },
        },
        "refund": {"type": "noul", "instructions": "Does the customer ask for a refund?"},
        "urgency": {
            "type": "score",
            "instructions": "How urgent is this?",
            "criteria": ["not urgent", "soon", "today"],
        },
    },
)
for name, result in answers.items():
    print(name, result["answer"], {k: round(v, 3) for k, v in result["probabilities"].items()})
```

{% endcode %}

`answer` is the option key for choice, `True` or `False` for noul, and the level number for score. Each answer also has the same fields as a Decision API answer.

To check accuracy on a labeled test set, use `evaluate`:

```python
test = load_dataset("LocalLLaMA/typed-decisions", "all", split = "test")
test_items, _ = FastDecisionModel.build_dataset(test, tokenizer, model)
print(FastDecisionModel.evaluate(model, tokenizer, test_items))
```

### Use it in the Decision API

You can [read our detailed guide](/docs/models/decision-laya.md) for serving/running decision models otherwise read below for a quick summary. Models you train in Unsloth show up in Settings → API. For a model you trained with code, start Unsloth with the merged folder you saved:

```bash
UNSLOTH_SYSTEMONE_MODEL=/path/to/qwen-decisions-merged unsloth studio -H 0.0.0.0 -p 8888
```

Turn on the Decision API in Settings → API. Requests that use `laya`, `default` or `jev-latest` now go to your model, and the answers have the same format as Laya's. The model needs a GPU and loads on the first request, which can take a few minutes. While a training run is using the GPU, the Decision API waits and starts answering again when the run ends.

#### How it works

Unsloth puts your input in one prompt, followed by every question and its options. The LLM reads it once. A small head, the same design as Cloudflare's Clef, looks at the LLM's output over each question and option and scores every option, deciding all the questions together. It never writes text, so it doesn't spend memory on the LLM's word predictions.

### 🐍 Train with code

Install or update Unsloth with `pip install --upgrade unsloth`, and use the following code to train your own decision model.

{% code expandable="true" %}

```python
from unsloth import FastDecisionModel, DecisionTrainer, is_bfloat16_supported
from datasets import load_dataset
from transformers import TrainingArguments

model, tokenizer = FastDecisionModel.from_pretrained(
    model_name = "unsloth/Qwen3.5-4B",
    max_seq_length = 2048,
    load_in_4bit = True,
)

model = FastDecisionModel.get_peft_model(
    model,
    r = 16,
    lora_alpha = 16,
    lora_dropout = 0,
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
)

dataset = load_dataset("LocalLLaMA/typed-decisions", "all", split = "train")
items, report = FastDecisionModel.build_dataset(dataset, tokenizer, model)
print(f"Skipped {report['skipped']} of {report['total']} decisions")

train_items, eval_items = FastDecisionModel.split_holdout(items, seed = 3407)
print(f"{len(train_items)} training rows, {len(eval_items)} held out")

from transformers import TrainingArguments

trainer = DecisionTrainer(
    model = model,
    processing_class = tokenizer,
    train_dataset = train_items,
    eval_dataset = eval_items,
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4, # Use GA to mimic batch size!
        warmup_steps = 10,
        # num_train_epochs = 2, # Set this for 1 full training run.
        max_steps = 240,
        learning_rate = 2e-5,
        lr_scheduler_type = "cosine",
        weight_decay = 0.01,
        bf16 = is_bfloat16_supported(),
        fp16 = not is_bfloat16_supported(),
        eval_strategy = "epoch",
        logging_steps = 1,
        output_dir = "outputs",
        report_to = "none", # Use TrackIO/WandB etc
        seed = 3407,
    ),
)
trainer_stats = trainer.train()
```

{% endcode %}

To use Llama or Gemma 4, change `model_name` to `unsloth/Llama-3.2-3B-Instruct` or `unsloth/gemma-4-E4B-it`. Other LLMs that Unsloth can fine-tune should work the same way.

For your own data, see the dataset format. Each row has a state, the questions to decide and the gold answers.

#### Calibrate and save

Calibrate on the rows `split_holdout` kept out, so the model's probabilities match how often it's right:

```python
metrics = FastDecisionModel.calibrate(model, tokenizer, eval_items)
print(metrics) # held-out accuracy, calibration error (ece) and loss
```

Then save. `save_pretrained` saves the LoRA adapters and the head. `save_pretrained_merged` saves a full 16-bit model:

```python
model.save_pretrained("qwen-decisions")
model.save_pretrained_merged("qwen-decisions-merged")
# model.push_to_hub("hf_username/qwen-decisions", token = "hf_...")
```

Load it again the same way you loaded the base model:

```python
model, tokenizer = FastDecisionModel.from_pretrained("qwen-decisions", load_in_4bit = True)
```

### ⚙️ Recommended settings

* Start with 4-bit LoRA at rank 16 and a learning rate of 2e-4. The new head trains at 1e-4 by default. You can change that with `head_learning_rate` in `DecisionTrainer`.
* We used 2 epochs on typed-decisions. With less data, try 3 or 4.
* For a quick try, set `max_steps = 60`. Qwen3.5-4B reached 76% in 10 minutes on an L4.
* If you run out of memory, halve the batch size and double gradient accumulation.
* `max_seq_length` sets the longest input during training. Long inputs keep the question and options, and cut the end of the input to fit. Predictions read up to 16,384 tokens.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
