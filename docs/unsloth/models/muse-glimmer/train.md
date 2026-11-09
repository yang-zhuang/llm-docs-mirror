> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/muse-glimmer/train.md).

# Muse Glimmer Fine-tuning Guide

Train Meta's Muse Glimmer 30B model with Unsloth.

You can now fine-tune and perform reinforcement learning (RL) with Meta’s Muse Glimmer 30B parameter agentic model via [Unsloth](https://github.com/unslothai/unsloth). Muse Glimmer supports vision and trains locally on 24GB VRAM via Unsloth with support for vision, text, audio and RL training.

* Unsloth trains Muse Glimmer **\~1.5x faster** with **\~50% less VRAM** than FA2 setups (no accuracy loss)
* Fine-tune Muse Glimmer via our **free** **Kaggle notebooks**:

| [**Vision + Text**](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Muse_Glimmer_\(30B\)-Vision.ipynb\&accelerator=nvidiaTeslaT4) | [**RL GRPO**](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Muse_Glimmer_\(30B\)-GRPO.ipynb\&accelerator=nvidiaTeslaT4) | [**Conversational**](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Muse_Glimmer_\(30B\)-Conversational.ipynb\&accelerator=nvidiaTeslaT4) |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

* You can also train Muse Glimmer with [reinforcement learning](#reinforcement-learning-rl) (RL) free or on 24GB VRAM.
* **30B QLoRA works with 24GB** and LoRA needs >40GB
* **Exporting**/saving models to GGUF etc. and full fine-tuning **(FFT)** works as well.

We also optimized Muse Glimmer to make them fit including these optimizations:

* `offload_embedding = True` keeps `embed_tokens` in CPU RAM and only moves the looked-up rows to the GPU. Muse Glimmer's input embedding is 202048 x 6656 in 16-bit, so this gives back 2.5 GB at load time - for now only works on single GPU (WIP on multi GPU setups)
* Dynamic 4-bit BnB quants which compress the model from 56GB to 21GB, allowing 24GB card finetunes! Measured on one 180 GiB card at `max_seq_length = 1024`, batch size 1, LoRA r=16: weights 18.22 GiB after load with the offload on (20.72 GiB without it), and **22.57 GiB peak reserved** through training. Plan for a 24 GiB card as the realistic minimum.

### Quick Start

Muse Glimmer is a dense causal Transformer with a dedicated perception encoder, designed for autonomous agents requiring planning, tool execution, multimodal understanding, and long-context reasoning.

* If you want to preserve reasoning ability, mix reasoning-style examples with direct answers. Avoid training only short answers, as this may reduce multi-step reasoning performance.
* Muse Glimmer supports long contexts up to 131K+ tokens, but start fine-tuning with shorter contexts first.
* After fine-tuning, you can export your model to NVFP4, FP8 or GGUF for local inference formats.

### Free Fine-tuning notebooks

For free Muse Glimmer fine-tuning via [Unsloth](https://github.com/unslothai/unsloth), we provide multiple Kaggle notebooks that offer **30 hours of free GPU usage with 2× Tesla T4 GPUs**. Kaggle is a Google product, similar to Google Colab, and provides a convenient way to run fine-tuning workflows without needing your own GPU hardware.

| [**Vision + Text**](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Muse_Glimmer_\(30B\)-Vision.ipynb\&accelerator=nvidiaTeslaT4) | [**RL GRPO**](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Muse_Glimmer_\(30B\)-GRPO.ipynb\&accelerator=nvidiaTeslaT4) | [**Conversational**](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Muse_Glimmer_\(30B\)-Conversational.ipynb\&accelerator=nvidiaTeslaT4) |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

{% columns %}
{% column %}
Muse Glimmer **Vision** Kaggle

{% embed url="<https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Muse_Glimmer_(30B)-Vision.ipynb&accelerator=nvidiaTeslaT4>" %}
{% endcolumn %}

{% column %}
Muse Glimmer **Conversational** Kaggle

{% embed url="<https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Muse_Glimmer_(30B)-Conversational.ipynb&accelerator=nvidiaTeslaT4>" %}
{% endcolumn %}
{% endcolumns %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FJwIF423NWv3xNpDezvJn%2Fimage.png?alt=media&amp;token=b2674c63-f4bf-424f-9497-f1c5ca620544" alt=""><figcaption></figcaption></figure>

### Reinforcement Learning RL

We also successfully made Muse Glimmer do GRPO / RL in a free Tesla T4 x 2 Kaggle environment - it barely fits but it works!

On 2 x 16 GB T4 GPUs `num_generations = 2`, `max_seq_length = 1536` and a 128-row cap on the log-softmax, needs 4.10 GiB of GPU VRAM. The same run at 3072 tokens needs 7.57 GiB so that does not fit.

We made an explicit device map with `unsloth_zoo.device_map_planner`, which reserves the logit headroom on the main GPU card as well.

{% embed url="<https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Muse_Glimmer_(30B)-GRPO.ipynb&accelerator=nvidiaTeslaT4>" %}
Reinforcement Learning Kaggle Free Notebook for Muse Glimmer
{% endembed %}

{% code overflow="wrap" %}

```python
from unsloth_zoo.device_map_planner import plan_device_map_for_pretrained
_plan = plan_device_map_for_pretrained(
    MODEL_NAME,
    # Free memory, not total: the CUDA context is already resident
    max_memory = {i: torch.cuda.mem_get_info(i)[0] for i in range(_n)},
    rows_per_chunk = 128,                       # matches the log-softmax cap below
    retained_rows  = BATCH_SIZE * max_seq_length,
    softcapped = True, temperature_scaled = True,
)
```

{% endcode %}

### 🦥 Unsloth Guide

{% columns %}
{% column %}
Muse Glimmer can be run and fine-tuned in [Unsloth](/docs/new/studio.md) Desktop, our new open-source web UI for local AI.

With Unsloth Studio, you can run models locally on **MacOS, Windows**, Linux and train NVIDIA GPUs. Intel, MLX and AMD training support coming this month.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FD7qpbGJLY5YMv0E0QgrB%2Ftrainingrun_LLM-unsloth.gif?alt=media&amp;token=feb766a7-1a7b-4f47-b5f4-b38e3a0d1470" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% stepper %}
{% step %}

#### Install Unsloth

The easiest way to get started is by downloading the [Unsloth Desktop app](/docs/desktop.md). Works on [macOS](/docs/get-started/install/mac.md), [Windows](/docs/get-started/install/windows-installation.md), and [Linux](/docs/get-started/install/linux.md).

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

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

#### Train Muse glimmer

On first launch you will need to create a password to secure your account and sign in again later. You’ll then see a brief onboarding wizard to choose a model, dataset, and basic settings. You can skip it at any time.

Search for Muse Glimmer in the search bar and select your desired model and dataset. Next, adjust your hyperparameters, context length as desired.
{% endstep %}

{% step %}

#### Monitor training progress

After you click start training, you will be able to monitor and observe the training progress of the model. The training loss should be steadily decreasing.\
Once done, the model will be automatically saved.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FeBrnu9zxARIkhOHzd0pq%2FScreenshot%202026-04-07%20at%205.53.32%E2%80%AFAM.png?alt=media&amp;token=dae77231-5020-4e8c-b2b8-cc49a98a9edf" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}

#### Export your fine-tuned model

Once done, Unsloth Studio allows you to export the model to GGUF, safetensor etc formats.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FBtpx58zCdrOD4zB4DPSC%2FScreenshot%202026-04-07%20at%206.12.41%E2%80%AFAM.png?alt=media&amp;token=05f05af2-5f7f-4b91-9c99-21d6a9b04935" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}

#### Compare fine-tuned model vs original model

Click on `Compare Mode` to compare the LoRA adapter and the original model.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fvm2CBSg7QBkKwTMKutyr%2FScreenshot%202026-04-07%20at%206.14.50%E2%80%AFAM.png?alt=media&amp;token=8c9c159f-9d5b-4468-8984-681d19ebc427" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}
{% endstepper %}

## Muse Glimmer-30B Overview

| Model Architecture | Dense Causal Transformer with Perception Encoder |
| ------------------ | ------------------------------------------------ |
| Parameters         | \~29.6B                                          |
| Layers             | 52                                               |
| Hidden Dimension   | 6656                                             |
| Attention          | Local, Local, Local, Global repeating            |
| Sliding Window     | 2048                                             |
| Attention Heads    | 32 Query / 2 KV                                  |
| FFN                | SwiGLU                                           |
| Context Length     | 131,072+                                         |
| Vision Encoder     | ViT-G/14 (\~1.8B parameters)                     |
| Modalities         | Text + Image input, Text output                  |
| Vocabulary         | 202,048 tokens                                   |

Muse Glimmer uses:

* Long-context reasoning
* Tool-use planning
* Failure recovery
* Multimodal understanding
* Agent scaffold compatibility
* Controllable reasoning effort

## Recommended Fine-tuning Method

### LoRA Fine-tuning

For most users, LoRA is the recommended approach.

Advantages:

* Much lower VRAM usage
* Faster training
* Smaller adapter files
* Easy model sharing
* Preserves base model capabilities

Recommended starting configuration:

```python
r = 16
lora_alpha = 16
lora_dropout = 0
```

For more difficult agentic tasks:

```python
r = 32
lora_alpha = 32
```

Start smaller and increase only if required.

## QLoRA Fine-tuning

QLoRA is recommended when GPU memory is limited.

Muse Glimmer was designed for efficient local deployment, including quantized inference. The same principles make QLoRA a practical fine-tuning approach.

Use QLoRA when:

* Training on consumer GPUs
* Fine-tuning larger datasets
* Keeping memory usage low
* Training multiple adapters

Example:

```python
load_in_4bit = True
```

***

## Multimodal Fine-tuning

Muse Glimmer includes a dedicated perception encoder for image understanding.

For vision tasks:

* Keep the perception encoder frozen initially.
* Fine-tune language layers first.
* Only train vision components if your dataset requires visual adaptation.

Good multimodal datasets include:

* Screenshot understanding
* Document reasoning
* Chart interpretation
* GUI interaction
* Image-grounded agent workflows

Example format:

```json
{
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image",
          "image": "example.png"
        },
        {
          "type": "text",
          "text": "Explain this screenshot."
        }
      ]
    },
    {
      "role": "assistant",
      "content": "The screenshot shows..."
    }
  ]
}
```

## Agentic Fine-tuning

Muse Glimmer is optimized for autonomous agent workflows.

For agent datasets, include:

* Tool descriptions
* Correct function calls
* Tool outputs
* Recovery from failures
* Multi-step planning examples
* Permission handling
* Final user-facing responses

Example:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Find my latest report and summarize it."
    },
    {
      "role": "assistant",
      "content": "I will search your files.",
      "tool_calls": [
        {
          "name": "file_search",
          "arguments": {
            "query": "latest report"
          }
        }
      ]
    }
  ]
}
```

## Dataset Preparation

Muse Glimmer works best with high-quality instruction datasets.

Recommended datasets:

* Multi-turn conversations
* Tool-use traces
* Coding tasks
* Agent trajectories
* Vision-language examples
* Reasoning examples

Avoid:

* Duplicate examples
* Low-quality generated answers
* Incorrect tool calls
* Inconsistent formatting

For reasoning preservation:

* Keep reasoning examples diverse.
* Include final answers.
* Avoid training exclusively on chain-of-thought outputs.

## Training Settings

A good starting configuration:

```python
trainer = SFTTrainer(
    max_seq_length = 4096,
    packing = True,
)
```

Recommended:

| Setting               | Value     |
| --------------------- | --------- |
| Batch size            | 1-8       |
| Gradient accumulation | 4-16      |
| Learning rate         | 2e-4 LoRA |
| Epochs                | 1-3       |
| Optimizer             | AdamW     |
| Precision             | BF16      |

For long-context training:

* Increase sequence length gradually.
* Monitor VRAM usage.
* Use gradient checkpointing.

## Reasoning Fine-tuning

Muse Glimmer supports controllable reasoning strength:

```
Reasoning strength: low
Reasoning strength: medium
Reasoning strength: high
Reasoning strength: xhigh
```

For complex tasks:

* Coding → high/xhigh
* Agent workflows → high/xhigh
* Simple assistants → medium
* Fast responses → low

When fine-tuning reasoning models:

* Include difficult examples.
* Include failures and corrections.
* Include multi-step tasks.
* Preserve general capabilities.

## Exporting Your Fine-tuned Model

After training, export your adapter:

```python
model.save_pretrained("muse-glimmer-lora")
tokenizer.save_pretrained("muse-glimmer-lora")
```

You can merge LoRA adapters:

```python
model.merge_and_unload()
```

Export formats can include:

* Hugging Face format
* Safetensors
* GGUF-compatible formats

## Inference Settings

Recommended generation settings:

```python
temperature = 1.0
top_p = 0.95
top_k = 64
```

For difficult reasoning tasks:

```
Reasoning strength: high
```

For fast conversations:

```
Reasoning strength: low
```

## Hardware Requirements

Muse Glimmer is optimized for local deployment.

Approximate requirements:

| Training Method  | Hardware                                            |
| ---------------- | --------------------------------------------------- |
| LoRA             | High-memory GPU recommended                         |
| QLoRA            | Consumer GPUs possible depending on sequence length |
| Full Fine-tuning | Multi-GPU systems                                   |

The model itself can run efficiently using quantized weights, with released 4-bit variants targeting 24GB and 32GB consumer hardware.

## Safety Fine-tuning

When deploying Muse Glimmer in agentic systems:

* Add tool permission checks.
* Validate external actions.
* Require confirmation for irreversible operations.
* Test prompt injection resistance.
* Evaluate privacy risks.

Recommended safety datasets:

* Tool misuse examples
* Permission boundaries
* Unsafe instruction handling
* Data minimization examples

## Troubleshooting

### Out of Memory

Try:

* Reduce sequence length
* Lower LoRA rank
* Enable 4-bit loading
* Reduce batch size
* Enable gradient checkpointing

### Model Quality Decreases

Try:

* Reduce learning rate
* Train fewer epochs
* Increase dataset quality
* Mix original instruction examples

### Tool Calls Become Incorrect

Add:

* More tool-call examples
* Correct schemas
* Failure recovery examples
* Multi-turn workflows


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/muse-glimmer/train.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
