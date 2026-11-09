> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/gemma-4/qat.md).

# Gemma 4 QAT

Run Google Gemma 4 QAT models locally, including E2B, E4B, 12B, 26B-A4B, and 31B.

Gemma 4 QAT (Quantization-Aware Training) is Google DeepMind’s new [Gemma 4](/docs/models/gemma-4.md) variants designed to **reduce memory requirements while preserving model quality**. This makes it possible to run larger models, such as **Gemma 4 26B-A4B**, locally on consumer GPUs with as little as **16GB of RAM**.

Gemma 4 QAT is trained with quantization in mind, allowing 4-bit format to have \~**72% lower memory usage** with **near original performance**. 2 special mobile quants of E2B and E4B are also provided which uses a mixture of quant widths.

Converting to `Q4_0` from QAT naively gets only 70.2% top-1 % accuracy for 26B-A4B. [We applied our Unsloth Dynamic method](#qat-analysis) to push it up to **85.6% (+15.6%) whilst also being** [**200MB smaller**](#usage-guide)!

Gemma 4 QAT includes: **E2B**, **E4B**, **12B, 26B-A4B**, and **31B.** They are multimodal, hybrid-thinking models that support 140+ languages and up to **256K context.**

{% columns %}
{% column %} <a href="/docs/models/gemma-4/qat.md#run-gemma-4-qat-tutorials" class="button primary">Run Gemma 4 QAT</a><a href="/docs/models/gemma-4/qat.md#qat-analysis" class="button secondary">QAT Analysis</a>

**Gemma-4-E2B** QAT runs on 3GB RAM, **E4B** on 5G&#x42;**, 12B** on 7G&#x42;**, 26-A4B** on 15GB and **31B** on 18G&#x42;**.**

We name our Gemma 4 QAT GGUFs as `UD-Q4_K_XL` as we found q4\_0 to degrade accuracy despite being bigger. See our [Gemma 4 QAT GGUFs](https://huggingface.co/collections/unsloth/gemma-4-qat).

To compare `int4` quantization, see the original vs. QAT size differences below. QAT uses \~72% less memory whilst retaining nearly all its original accuracy:
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FGLHNSIo3qe4ByThVZDzm%2Fgemma%204%20qat.png?alt=media&amp;token=ae72b8e1-def7-447c-bafc-67514354df7d" alt="" width="563"><figcaption><p>Visualization of how Gemma 4 Mobile QAT works.</p></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

| Gemma 4     | QAT (int4) GGUF | Original BF16 | Percentage change |
| ----------- | --------------: | ------------: | ----------------: |
| **E2B**     |         2.62 GB |       9.31 GB |            71.86% |
| **E4B**     |         4.22 GB |       15.1 GB |            72.05% |
| **12B**     |         6.72 GB |       23.8 GB |            71.76% |
| **26B A4B** |         14.2 GB |       50.5 GB |            71.88% |
| **31B**     |         17.3 GB |       61.4 GB |            71.82% |

### Usage Guide

Gemma 4 QAT variants for E2B and E4B are designed for phones and laptops, while the larger 26B-A4B and 31B QAT models now work on laptops rather than just strong home GPUs.

There is **only one GGUF file** for each Gemma 4 model because we found that precisions higher than the uploaded `UD-Q4_K_XL` version degrade accuracy rather than improve it. Use the original non QAT Q4\_0 quants [here](https://huggingface.co/collections/unsloth/gemma-4).

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FrTygbMBlZcUER9GUMzKg%2Fimage.png?alt=media&amp;token=85c3c44b-0f42-477a-9ce2-30b085e21b5c" alt="" width="563"><figcaption></figcaption></figure>

### Hardware requirements

**Table: Gemma 4 QAT Inference GGUF recommended hardware requirements** (units = total memory: RAM + VRAM, or unified memory).

| Gemma 4 QAT     | Requirements |
| --------------- | -----------: |
| **E2B** QAT     |         3 GB |
| **E4B** QAT     |         5 GB |
| **12B** QAT     |         7 GB |
| **26B A4B** QAT |        15 GB |
| **31B** QAT     |        18 GB |

{% hint style="info" %}
The table assumes \~8K tokens of context. llama.cpp’s default 256K context for 26B A4B adds \~5 GB of KV cache. On memory-limited CPU-only machines, use `-c 8192` or `-c 16384`; `--fit` currently ignores CPU repacked weights.
{% endhint %}

### Recommended Settings

The QAT checkpoints use the same recommended Gemma 4 settings:

* `temperature = 1.0`
* `top_p = 0.95`
* `top_k = 64`

{% hint style="info" %}
Gemma 4's max context is **128K** for **E2B**, **E4B** and **256K** for **12B**, **26B A4B**, **31B**.
{% endhint %}

## QAT Analysis

We found that naively converting the QAT Q4\_0 checkpoint to Q4\_0 in llama.cpp land actually degraded accuracy and was not actually aligned with the BF16 QAT lattice for Q4\_0. We applied our Unsloth dynamic method to force a better agreement between the llama.cpp compatible Q4\_0 format and the true BF16 QAT Q4\_0 format, and managed to both make the quants smaller (Q6\_K wasn't needed for embeddings), and also more accurate!

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FcBHRs9twWiAnjgtm4EKf%2Fimage.png?alt=media&amp;token=023d7771-dba1-4a1e-a8c4-da6ac98921f7" alt=""><figcaption></figcaption></figure>

Below is a table of KLD and Top 1% accuracy and Disk space. You can see our versions dramatically improve on 99.9% KLD and mean KLD. **E2B for example has a mean KLD of 0.00173 vs 0.05109 (29x better relatively) for a naive Q4\_0 quantization, and ours is even 22% smaller!**

The main issue is converting from QAT BF16 to llama.cpp's Q4\_0 format is not lossless. llama.cpp uses F16 scales, whilst QAT BF16 uses BF16 scales, and the scales are not determined optimally in llama.cpp land.

Naive conversion gets 24.77% byte exactness to BF16 QAT, whilst we found we can push it to 99.96% using some hacks!

<table><thead><tr><th width="100">Model</th><th>Method</th><th>Disk (GB)</th><th>99.9% KLD</th><th>Mean KLD</th><th width="77.5999755859375">Top-1 %</th></tr></thead><tbody><tr><td>E2B</td><td>Unsloth</td><td><strong>2.62</strong></td><td>0.0557</td><td>0.00173</td><td><strong>98.16</strong></td></tr><tr><td>E2B</td><td>Q4_0</td><td>3.35</td><td>1.0513</td><td>0.05109</td><td>89.29</td></tr><tr><td>E4B</td><td>Unsloth</td><td><strong>4.22</strong></td><td>0.0536</td><td>0.00121</td><td><strong>98.54</strong></td></tr><tr><td>E4B</td><td>Q4_0</td><td>5.15</td><td>0.6722</td><td>0.03778</td><td>90.94</td></tr><tr><td>26B</td><td>Unsloth</td><td><strong>14.25</strong></td><td>2.7087</td><td>0.09788</td><td><strong>85.63</strong></td></tr><tr><td>26B</td><td>Q4_0</td><td>14.44</td><td>4.5420</td><td>0.36094</td><td>70.20</td></tr><tr><td>31B</td><td>Unsloth</td><td><strong>17.29</strong></td><td>1.3659</td><td>0.01403</td><td><strong>96.67</strong></td></tr><tr><td>31B</td><td>Q4_0</td><td>17.65</td><td>3.0030</td><td>0.09349</td><td>87.91</td></tr><tr><td>12B</td><td>Unsloth</td><td><strong>6.72</strong></td><td>9.2740</td><td>0.13288</td><td><strong>88.76</strong></td></tr><tr><td>12B</td><td>Q4_0</td><td>6.98</td><td>14.7323</td><td>0.50702</td><td>74.08</td></tr></tbody></table>

## Mobile Mixture QAT

The Gemma-4 team also released special mobile mixture QAT versions of Gemma-4-E2B-it and Gemma-4-E4B-it. We also faithfully converted them to llama.cpp compatible format, and also recovered nearly all accuracy as well. We used TQ2\_0 for the 2-bit layers and did a negative scaler.

We made UD-Q2\_K\_XL quants for both E2B and E4B.

|                        | E2B mobile          | E4B mobile          |
| ---------------------- | ------------------- | ------------------- |
| Size                   | 2.19 GB             | 3.22 GB             |
| 2-bit (TQ2\_0) tensors | 61 (incl. deep MLP) | 2 (embeddings only) |
| Mean KLD vs BF16       | 0.00409             | 0.00102             |
| Top-1 %                | 97.82%              | 98.76%              |
| Base PPL               | \~103               | 42.4                |

See [gemma-4-E2B-it-qat-GGUF](https://huggingface.co/unsloth/gemma-4-E2B-it-qat-GGUF) and [gemma-4-E4B-it-qat-GGUF](https://huggingface.co/unsloth/gemma-4-E4B-it-qat-GGUF) for `UD-Q2_K_XL`.

## Run Gemma 4 QAT Tutorials

Because Gemma 4 GGUFs comes in several sizes, the recommended starting point for the small models is 8-bit and the larger models is **Dynamic 4-bit**. [Gemma 4 GGUFs](https://huggingface.co/collections/unsloth/gemma-4-qat):

| [E2B](https://huggingface.co/unsloth/gemma-4-E2B-it-qat-GGUF) | [E4B](https://huggingface.co/unsloth/gemma-4-E4B-it-qat-GGUF) | [12b](https://huggingface.co/unsloth/gemma-4-12b-it-qat-GGUF) | [26B-A4B](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-qat-GGUF) | [31B](https://huggingface.co/unsloth/gemma-4-31B-it-qat-GGUF) |
| ------------------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------- |

<a href="/docs/models/gemma-4/qat.md#unsloth-studio-guide" class="button primary">🦥 Unsloth Studio Guide</a><a href="/pages/9kjF1F7Gsb0dgOA9lcpl#llama.cpp-guide" class="button primary">🦙 Llama.cpp Guide</a>

{% columns %}
{% column %}
**You can run and train Gemma 4 QAT for free with a UI in our** [**Unsloth Studio**](/docs/new/studio.md)✨ **notebook:**
{% endcolumn %}

{% column %}
{% embed url="<https://colab.research.google.com/github/unslothai/unsloth/blob/main/studio/Unsloth_Studio_Colab.ipynb>" %}
{% endcolumn %}
{% endcolumns %}

### 🦥 Unsloth Studio Guide

Gemma 4 QAT can now be run and trained in [Unsloth Studio](/docs/new/studio.md), our new open-source web UI for local AI. Unsloth Studio lets you run models locally on **MacOS, Windows**, Linux and:

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

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FVrLgXwplAMcvkU4owjPk%2F26b%20gif.gif?alt=media&amp;token=8a569952-c152-435f-b815-c9f295619587" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% stepper %}
{% step %}

#### Install Unsloth

Run in your terminal:

**MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows PowerShell:**

```bash
irm https://unsloth.ai/install.ps1 | iex
```

{% endstep %}

{% step %}

#### Launch Unsloth

**MacOS, Linux, WSL and Windows:**

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

Then open `http://127.0.0.1:8888` (or your specific URL) in your browser.
{% endstep %}

{% step %}

#### Search and download Gemma 4 QAT

On first launch you will need to create a password to secure your account and sign in again.

Then go to the [Unsloth Chat](/docs/new/studio/chat.md) tab and search for Gemma 4 in the search bar and download your desired model and quant.
{% endstep %}

{% step %}

#### Run Gemma 4 QAT

Inference parameters should be auto-set when using Unsloth Studio, however you can still change it manually. You can also edit the context length, chat template and other settings.

For more information, you can view our [Unsloth Studio inference guide](/docs/new/studio/chat.md).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FVrLgXwplAMcvkU4owjPk%2F26b%20gif.gif?alt=media&amp;token=8a569952-c152-435f-b815-c9f295619587" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### 🦙 Llama.cpp Guide

For this guide there is no need to select quantization type since there is only one: `UD-Q4_K_XL`.  See: [Gemma 4 QAT collection](https://huggingface.co/collections/unsloth/gemma-4-qat). For these tutorials, we will using [llama.cpp](llama.cpphttps://github.com/ggml-org/llama.cpp) for fast local inference, especially if you have a CPU.

{% stepper %}
{% step %}
Obtain the latest `llama.cpp` **on** [**GitHub here**](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endstep %}

{% step %}
If you want to use `llama.cpp` directly to load models, you can follow commands below, according to each model. `UD-Q4_K_XL` is the ONLY quantization type. You can also download via Hugging Face (step 3). This is similar to `ollama run` . Use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location.

**26B-A4B:**

```bash
export LLAMA_CACHE="unsloth/gemma-4-26B-A4B-it-qat-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/gemma-4-26B-A4B-it-qat-GGUF:UD-Q4_K_XL \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64
```

**31B:**

```bash
export LLAMA_CACHE="unsloth/gemma-4-31B-it-qat-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/gemma-4-31B-it-qat-GGUF:UD-Q4_K_XL \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64
```

**E4B:**

```bash
export LLAMA_CACHE="unsloth/gemma-4-E4B-it-qat-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/gemma-4-E4B-it-qat-GGUF:UD-Q4_K_XL \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64
```

**E2B:**

```bash
export LLAMA_CACHE="unsloth/gemma-4-E2B-it-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/gemma-4-E2B-it-qat-GGUF:UD-Q4_K_XL \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64
```

{% endstep %}

{% step %}
Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD-Q4_K_XL` or other quantized versions like `Q8_0` . If downloads get stuck, see: [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

```bash
hf download unsloth/gemma-4-26B-A4B-it-qat-GGUF \
    --local-dir unsloth/gemma-4-26B-A4B-it-qat-GGUF \
    --include "*mmproj-BF16*" \
    --include "*UD-Q4_K_XL*" # Use "*UD-Q2_K_XL*" for Dynamic 2bit
```

{% endstep %}

{% step %}
Then run the model in conversation mode (with vision `mmproj-F16`):

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/gemma-4-26B-A4B-it-qat-GGUF/gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf \
    --mmproj unsloth/gemma-4-26B-A4B-it-qat-GGUF/mmproj-BF16.gguf \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64
```

{% endcode %}
{% endstep %}

{% step %}

### Llama-server deployment

To deploy Gemma-4 on llama-server, use:

```bash
./llama.cpp/llama-server \
    --model unsloth/gemma-4-26B-A4B-it-qat-GGUF/gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf \
    --mmproj unsloth/gemma-4-26B-A4B-it-qat-GGUF/mmproj-BF16.gguf \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64 \
    --alias "unsloth/gemma-4-26B-A4B-it-qat-GGUF" \
    --port 8001 \
    --chat-template-kwargs '{"enable_thinking":true}'
```

{% hint style="warning" %}
To [disable thinking / reasoning](#how-to-enable-or-disable-reasoning-and-thinking), use `--chat-template-kwargs '{"enable_thinking":false}'`

If you're on **Windows** Powershell, use: `--chat-template-kwargs "{\"enable_thinking\":false}"`

Use 'true' and 'false' interchangeably.
{% endhint %}
{% endstep %}
{% endstepper %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/gemma-4/qat.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
