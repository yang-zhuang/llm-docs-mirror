> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/inkling.md).

# Inkling - How to Run Locally

Learn how to run Thinking Machine Labs' Inkling multimodal models locally.

Inkling by Thinking Machines Labs are open-weight multimodal models consisting of: **Inkling-Small** the new **276B** (12B active) model and the earlier **975B** (41B) parameter model. Licensed under Apache 2.0, the models support a 1M token context window, native multimodal input for **text**, **image**, and **audio**, and generates **text** as the output. Inkling excel at coding, agentic and tool-calling, RAG, chat, multilingual, and multimodal workloads.

Dynamic 2-bit reaches 81% top-1% accuracy whilst being 82% smaller. This shows if we shrink the model down by 82% with our [Unsloth Dyanmic ](/docs/basics/dynamic-3.0-ggufs.md)GGUF method - it does NOT mean the model gets 82% "dumber" - only \~18% degradation is seen. Thanks Thinking Machines Lab (TML) for giving Unsloth day-zero access. [**Inkling-Small-GGUF**](https://huggingface.co/unsloth/Inkling-Small-GGUF) and [**Inkling-GGUF**](https://huggingface.co/unsloth/inkling-GGUF)

<a href="/docs/models/inkling.md#run-inkling-tutorials" class="button primary">Run Inkling Tutorials</a><a href="/docs/models/inkling.md#quantization-analysis" class="button secondary">Quantization Results</a>

#### &#x20;:gear: Usage Guide

{% columns %}
{% column width="50%" %}
The 1-bit dynamic quant `UD-IQ1_S` uses **270GB** of disk space - this will need a Mac Studio Ultra or machines with at least RAM+VRAM to be 290GB or so.

The **1-bit** quant will fit on a 290GB RAM and 6/8-bit requires 900GB RAM. See the 1-bit GGUF in action to the right where we asked Inkling to make a Sudoku HTML game.

See right for 1-bit Inkling GGUF in Unsloth:
{% endcolumn %}

{% column width="50%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNOhWqx2nFNOSjiQlv3Bz%2Finklin.gif?alt=media&amp;token=2fdae9e3-e78b-4cd3-af07-a9c4989a937f" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

**Table: Inference hardware requirements** (units = total memory: RAM + VRAM, or unified memory):

| Model         | 2-bit  | 3-bit  | 4-bit        | 6/8bit | BF16    |
| ------------- | ------ | ------ | ------------ | ------ | ------- |
| Inkling-Small | 89 GB  | 128 GB | 132 - 170 GB | 256 GB | 543 GB  |
| Inkling       | 325 GB | 450 GB | 600 GB       | 870 GB | 1900 GB |

**Table: Top-1% Retained (Accuracy Recovery) for 975B Inkling:**

| 1-bit       | 2-bit | 3-bit | 4-bit | 6/8bit | BF16   |
| ----------- | ----- | ----- | ----- | ------ | ------ |
| 74.2%-77.4% | 81.0% | 88.7% | 94.4% | 99.8%  | 100.0% |

{% hint style="success" %}
For best performance, make sure your total available memory, including VRAM and system RAM, exceeds the quantized model file size by a comfortable margin.
{% endhint %}

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F0Dbxy6RiKTJpt9IhQrAI%2FScreenshot%202026-07-15%20at%209.35.28%E2%80%AFAM.png?alt=media&amp;token=55c1a479-6bf4-4593-92de-3e14d97e0d32" alt=""><figcaption><p>Sodoku with Inkling 1-bit</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFgJuxrLQurMb7sFnewYW%2FScreenshot%202026-07-15%20at%2010-37-22%20Chat%20-%20Unsloth%20Studio.png?alt=media&amp;token=1e9bb157-a07e-4699-88cc-daf65f1e3621" alt=""><figcaption><p>Audio parsing with 1-bit Inkling</p></figcaption></figure></div>

### Recommended Settings

Inkling has Non-thinking and Thinking modes. In [Unsloth Studio](#run-glm-5.2-in-unsloth-studio) you can easily toggle Thinking and non-Thinking with a UI.

Use these settings for most use cases:

| Default Settings (Most Tasks) |
| ----------------------------- |
| `temperature` = 1.0           |
| `top_p` = 1.0 (Off)           |

* **Maximum context window:** `1,048,576`.

#### Chat Template & thinking efforts

Inkling uses an interesting "Thinking effort level:" system prompt component where it's a number from 0.00 to 0.99! Tokenizing the below:

{% code overflow="wrap" expandable="true" %}

```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("unsloth/inkling")
tokenizer.apply_chat_template([
    {"role" : "user", "content" : "What is 1+1?"},
    {"role" : "assistant", "content" : "2!"},
    {"role" : "user", "content" : "What is 2+2?"},
], tokenize = False, reasoning_effort = "xhigh")
```

{% endcode %}

will get the below:

{% code overflow="wrap" expandable="true" %}

```
<|message_system|><|content_text|>Thinking effort level: 0.99<|end_message|><|message_user|><|content_text|>What is 1+1?<|end_message|><|message_model|><|content_text|>2!<|end_message|><|content_model_end_sampling|><|message_user|><|content_text|>What is 2+2?<|end_message|>
```

{% endcode %}

#### Disabling Thinking, changing reasoning effort

Inkling uses reasoning by default. It also supports reasoning efforts where `reasoning_effort` can be none = 0, low = 0.2, medium = 0.7, high = 0.9, xhigh = 0.99 and max = 0.99.

To disable thinking, use `--chat-template-kwargs '{"reasoning_effort":'none'}'`. If you're on **Windows** Powershell, use: `--chat-template-kwargs "{\"reasoning_effort\":'none'}"`

For reasoning effort customization and or to disable reasoning, use the below examples:

{% code overflow="wrap" expandable="true" %}

```bash
--chat-template-kwargs '{"reasoning_effort":"none"}'
--chat-template-kwargs '{"reasoning_effort":"low"}'
--chat-template-kwargs '{"reasoning_effort":"medium"}'
--chat-template-kwargs '{"reasoning_effort":"high"}'
--chat-template-kwargs '{"reasoning_effort":"xhigh"}'
--chat-template-kwargs '{"reasoning_effort":"max"}'
```

{% endcode %}

{% columns %}
{% column %}
Inkling also does interleaved thinking and tool calling - even with the dynamic 1-bit quant!
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FZ1EkZP1FKK3NwY8QvJZA%2FScreenshot%202026-07-15%20at%2010.37.16%E2%80%AFAM.png?alt=media&amp;token=27cc0012-dbe5-41b3-ae4f-9ac5116b7a3f" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

## Run Inkling Tutorials:

Inkling runs in Unsloth on MacOS, Windows, and Linux. You can:

{% columns %}
{% column %}

* Search, download, [run GGUFs](/docs/new/studio.md#run-models-locally) and safetensor models
* [**Self-healing** tool calling](/docs/new/studio.md#execute-code--heal-tool-calling) + **web search**
* [**Code execution**](/docs/new/studio.md#run-models-locally) (Python, Bash)
* [Automatic inference](https://unsloth.ai/docs/desktop#feature-deep-dive) parameter tuning (temp, top-p, etc.)
* Fast CPU + GPU inference via llama.cpp
* [Train LLMs](/docs/new/studio.md#no-code-training) 2x faster with 70% less VRAM
  {% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FiH68xloT5eoVUD1Eo3Ok%2FScreenshot%202026-07-15%20at%209.08.49%E2%80%AFAM.png?alt=media&amp;token=82c717b5-76ee-42e7-9823-550765bf7543" alt=""><figcaption><p>1-bit Inkling GGUF multimodal example</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

{% stepper %}
{% step %}
**Install and Launch Unsloth**

To install, run in your terminal:

MacOS, Linux, WSL:

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

Windows PowerShell:

```bash
irm https://unsloth.ai/install.ps1 | iex
```

**Launch Unsloth**

MacOS, Linux, WSL and Windows:
{% endstep %}

{% step %}
**Search and download** Inkling

Then go to the [Unsloth Chat](/docs/new/studio/chat.md) tab and search for **Inkling** in the search bar and download your desired model and quant. Ensure you have enough compute the run the model.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F7jl4PfIAwtWyC0qipNUd%2Finkling%20search.png?alt=media&amp;token=74fcf1fb-efd0-4c71-a3b9-438d10376e54" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}
**Run Inkling**

Inference parameters should be auto-set when using Unsloth Studio, however you can still change it manually. You can also edit the context length, chat template and other settings.

For more information, you can view our [Unsloth Studio inference guide](/docs/new/studio/chat.md).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FeXhBVDCZ5OP8B773Cg1m%2F2026-07-1510-31-00-ezgif.com-video-to-gif-converter.gif?alt=media&amp;token=76492c11-5b71-48ac-bfc9-f85a92f84011" alt=""><figcaption><p>1-bit Inkling running in Unsloth Studio</p></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### 🦙 Run Inkling in llama.cpp

For this guide we'll be running the `UD-IQ1_S` quant which will require at least 290GB RAM. Feel free to change quantization type. For these tutorials, we will using [llama.cpp](llama.cpphttps://github.com/ggml-org/llama.cpp) for fast local inference. GGUF: [**Inkling-GGUF**](https://huggingface.co/unsloth/Inkling-GGUF)&#x20;

#### Download Unsloth

### Unsloth Guide

<https://unsloth.ai/download>

{% stepper %}
{% step %}
Obtain the SPECIFIC `llama.cpp` PR on [GitHub here](https://github.com/ggml-org/llama.cpp/pull/25731). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
gh pr checkout 25731
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endstep %}

{% step %}
You can now use `llama.cpp` directly to load and download models, just like `ollama run`. First, select the quantization type you want like `Q2_K_XL`. Also use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location. Note this download process might be very slow, so it's probably best to use the manual download process in the next section.

**Inkling-Small 276B:**

```bash
export LLAMA_CACHE="unsloth/Inkling-Small-GGUF"
./build/bin/llama-cli \
    -hf unsloth/Inkling-Small-GGUF:UD-Q3_K_XL \
    --temp 1.0 \
    --top-p 1.0 \
    --min-p 0.0
```

**Inkling 975B:**

{% code overflow="wrap" %}

```bash
export LLAMA_CACHE="unsloth/Inkling-GGUF"
./build/bin/llama-cli \
    -hf unsloth/Inkling-GGUF:UD-IQ1_S \
    --temp 1.0 \
    --top-p 1.0 \
    --min-p 0.0
```

{% endcode %}
{% endstep %}

{% step %}
If you want to download the model manually, we can download the model via the code below (after installing `pip install huggingface_hub`). If downloads get stuck, see: [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

**Inkling-Small 276B:**

```bash
hf download unsloth/Inkling-Small-GGUF \
    --local-dir unsloth/Inkling-Small-GGUF \
    --include "*UD-Q3_K_XL*" # Use "*UD-Q4_K_XL*" for 4-bit
```

**Inkling 975B:**

{% code overflow="wrap" %}

```bash
hf download unsloth/Inkling-GGUF \
    --local-dir unsloth/Inkling-GGUF \
    --include "*UD-IQ1_S*" # Use "*UD-Q2_K_XL*" for 2-bit
```

{% endcode %}
{% endstep %}

{% step %}
You can edit `--threads 32` for the number of CPU threads, `--ctx-size 32768` for context length, `--n-gpu-layers 2` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference. We implemented a Flash Attention bias fused kernel in llama.cpp as well to reduce VRAM usage - but best to keep `--ctx-size` modest still!

**Inkling-Small 276B:**

{% code overflow="wrap" %}

```bash
./build/bin/llama-cli \
    --model unsloth/Inkling-Small-GGUF/UD-Q3_K_XL/Inkling-Small-UD-Q3_K_XL-00001-of-00004.gguf \
    --temp 1.0 \
    --top-p 1.0 \
    --min-p 0.0
```

{% endcode %}

**Inkling 975B:**

{% code overflow="wrap" %}

```bash
./build/bin/llama-cli \
    --model unsloth/Inkling-GGUF/UD-IQ1_S/inkling-UD-IQ1_S-00001-of-00007.gguf \
    --temp 1.0 \
    --top-p 1.0 \
    --min-p 0.0
```

{% endcode %}
{% endstep %}
{% endstepper %}

### :triangular\_ruler:Quantization Analysis

We also ran KLD (KL Divergence) benchmarks to gauge the accuracy of our quantizations of Inkling-GGUF. We first created a 8-bit + 6-bit quant mixture for the model with 6-bit for the ffn\_up and ffn\_gate exps, and found RMSE to be 1e-4 or less in terms of dequantization - quantizing ffn\_down increased error 10x more, so that is kept in Q8\_0 for the 8/6-bit quant

On pure top-1% accuracy, **dynamic 1-bit gets around 74.2% accuracy yet being 86% smaller**! Dynamic 2-bit gets around 81% accuracy whilst being 82% smaller. This shows dynamically quantizing some layers to higher precision does not make the model unusable and fully useless - we show selectively quantizing layers can recover a lot of accuracy!

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FRaRrtzsGoOqaA7Pcu4dx%2FScreenshot%202026-07-15%20at%2009-34-31%20inkling_975B_top1_match_green_GB.png%20(PNG%20Image%2011340%20%C3%97%205940%20pixels)%20%E2%80%94%20Scaled%20(7%25).png?alt=media&amp;token=408915f8-c6c3-447d-a74f-fd31d5b9b320" alt="" width="563"><figcaption></figcaption></figure>

**But what does "74% accuracy" actually entail?**

It does NOT mean 26% of the time the model outputs gibberish or wrong results - instead it means 26% of the top, it might choose the 2nd highest probable answer more.

For example asking "Create a poem" will produce vastly different results - 74% of the time it'll be similar poems to the BF16 baseline, but 26% it'll be another poem, but still correct. For factual answers where creativity and sampling is not involved, the model will always recall the same answer (for example "What is 2+2", it'll always say 4, not 5 ever)

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FJ7N99v9Doqxs0DaNiNAH%2Finkling_975B_kld_benchmarks_green_GB_detailed_y_axis.png?alt=media&amp;token=73ec06d5-d089-42f5-ab85-30161cef73d4" alt="" width="563"><figcaption></figcaption></figure>

## 📊 Benchmarks

You can view further below for Inkling benchmarks in table format:

Inkling results are reported at effort=0.99. Comparison scores are generated Jul 14, 2026. Nemotron 3 Ultra, Kimi K2.5, Kimi K2.6, GLM 5.2, and DeepSeek V4 Pro are open weights models; Gemini 3.1 Pro, Claude Fable 5, and GPT 5.6 Sol are closed weights models.

|                       |                                   | Inkling | Nemotron 3 Ultra | Kimi K2.5 | Kimi K2.6 | GLM 5.2 | DeepSeek V4 Pro | Gemini 3.1 Pro (high) | Claude Fable 5 (max) | GPT 5.6 Sol (xhigh) |
| --------------------- | --------------------------------- | ------- | ---------------- | --------- | --------- | ------- | --------------- | --------------------- | -------------------- | ------------------- |
| **Reasoning**         |                                   |         |                  |           |           |         |                 |                       |                      |                     |
|                       | HLE (text only)                   | 29.7%   | 26.6%            | 29.4%     | 35.9%     | 40.1%   | 35.9%           | 44.7%                 | 53.3%                | 47.2%               |
|                       | HLE (with tools)                  | 46.0%   | 37.4%            | 50.2%     | 54.0%     | 54.7%   | 48.2%           | 51.4%                 | 64.5%                | 55.0%               |
|                       | AIME 2026                         | 97.1%   | 94.2%            | 95.8%     | 96.4%     | 99.2%   | 96.7%           | 98.3%                 | –                    | 99.9%               |
|                       | GPQA Diamond                      | 87.2%   | 86.7%            | 87.9%     | 91.1%     | 89.5%   | 88.8%           | 94.1%                 | 92.6%                | 94.1%               |
| **Agentic (coding)**  |                                   |         |                  |           |           |         |                 |                       |                      |                     |
|                       | SWEBench Verified                 | 77.6%   | 70.7%            | 76.8%     | 80.2%     | –       | 80.6%           | 80.6%                 | 95.0%                | –                   |
|                       | SWEBench Pro (Public)             | 54.3%   | 46.4%            | 50.7%     | 58.6%     | 62.1%   | 55.4%           | 54.2%                 | 80.0%                | 64.6%               |
|                       | Terminal Bench 2.1 (Best Harness) | 63.8    | 56.4             | 51.3      | 71.3      | 82.7    | 64              | 73.8                  | 84.6                 | 89.5                |
|                       | GDPVal-AA v2                      | 1233    | 1164             | 1009      | 1190      | 1514    | 1307            | 962                   | 1760                 | 1748                |
| **Agentic (general)** |                                   |         |                  |           |           |         |                 |                       |                      |                     |
|                       | MCP Atlas                         | 74.1%   | 44.7%            | 64.0%     | 68.1%     | 77.8%   | 73.2%           | 78.2%                 | 83.3%                | 81.8%               |
|                       | Tau 3 Banking                     | 23.7%   | 13.8%            | 13.2%     | 20.6%     | 26.8%   | 25.8%           | 16.5%                 | 26.8%                | 33.0%               |
| **Factuality**        |                                   |         |                  |           |           |         |                 |                       |                      |                     |
|                       | BrowseComp (w/ Ctx)               | 77.1%   | –                | 74.9%     | 83.2%     | –       | 83.4%           | 85.9%                 | 88.0%                | 89.4%               |
|                       | SimpleQA Verified                 | 43.9%   | 32.4%            | 36.9%     | 38.7%     | 38.1%   | 57.0%           | 77.3%                 | 68.3%                | 71.6%               |
|                       | AA Omniscience                    | 1.0%    | -1.0%            | -8.0%     | 6.0%      | 4.0%    | -10.0%          | 33.0%                 | 40.0%                | 22.0%               |
| **Chat**              |                                   |         |                  |           |           |         |                 |                       |                      |                     |
|                       | IFBench                           | 79.8%   | 81.4%            | 70.2%     | 76.0%     | 73.3%   | 76.5%           | 77.1%                 | 63.5%                | 72.7%               |
|                       | Global-MMLU-Lite                  | 88.7%   | 85.6%            | 84.0%     | 88.4%     | 89.2%   | 89.3%           | 92.7%                 | 93.3%                | 91.8%               |
| **Vision**            |                                   |         |                  |           |           |         |                 |                       |                      |                     |
|                       | MMMU Pro (Standard 10)            | 73.3%   | –                | 75.0%     | 79.0%     | –       | –               | 82.0%                 | 84.2%                | 83.0%               |
|                       | Charxiv RQ                        | 78.1%   | –                | 77.5%     | 80.4%     | –       | –               | 80.2%                 | 86.5%                | 84.7%               |
|                       | Charxiv RQ (with python)          | 82.0%   | –                | 78.7%     | 86.7%     | –       | –               | 89.9%                 | 89.4%                | 87.8%               |
| **Audio**             |                                   |         |                  |           |           |         |                 |                       |                      |                     |
|                       | Audio MC                          | 56.6%   | –                | –         | –         | –       | –               | 66.8%                 | –                    | –                   |
|                       | MMAU                              | 77.2%   | –                | –         | –         | –       | –               | 82.5%                 | –                    | –                   |
|                       | VoiceBench                        | 91.4%   | –                | –         | –         | –       | –               | 94.3%                 | –                    | –                   |
| **Safety**            |                                   |         |                  |           |           |         |                 |                       |                      |                     |
|                       | FORTRESS (Adversarial)            | 78.0%   | 77.6%            | 54.1%     | 65.6%     | 71.3%   | 36.0%           | 65.2%                 | 96.0%                | 82.4%               |
|                       | FORTRESS (Benign)                 | 95.9%   | 90.5%            | 98.3%     | 97.2%     | 90.0%   | 98.5%           | 98.0%                 | 55.1%                | 98.1%               |
|                       | StrongREJECT                      | 98.6%   | 98.7%            | 99.5%     | 99.8%     | 98.5%   | 98.6%           | 98.0%                 | 98.7%                | 98.5%               |


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/inkling.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
