> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/minimax-m3.1-flash.md).

# MiniMax-M3.1-Flash: Run Locally

Run MiniMax-M3.1-Flash locally with Unsloth Dynamic GGUFs.

MiniMax-M3.1-Flash is MiniMax’s new **428B** MoE multimodal model, with 23B active parameters and **1M context**, built for coding and agentic use. Learn how to run MiniMax-M3.1-Flash via [Unsloth GGUFs](https://huggingface.co/unsloth/MiniMax-M3.1-Flash-GGUF) locally with Unsloth Desktop or llama.cpp.

Our 129.4GB **1-bit** achieves **\~89.9% top-1 accuracy**; 143.9GB **2-bit** reaches **91.5%**, and 249.4 GB 4-bit UD-Q4\_K\_XL 98.0%. On coding, Q2 reaches 91.2% and Q4 97.6%. We weighted quant performance across **seven categories**: coding, math, chat, tools, multilingual, reasoning and agentic use. Thank you MiniMax for day-zero access.

### ⚙️ Usage Guide

MiniMax-M3.1-Flash supports text, images and video and adds sparse attention across all layers, QAT for attention and routed experts, and DSpark.

For 2-bit UD-Q2\_K\_XL, budget 160GB+ RAM + VRAM (or unified memory); for 4-bit UD-Q4\_K\_XL, budget 256GB+. These planning estimates assume 16K text context and one parallel slot.

Plan to keep the full quantized weights in RAM and VRAM, even though only 23B parameters are active per token. Use CPU offloading when GPU memory is limited.

#### MiniMax-M3.1-Flash Requirements:

**Table: Hardware requirements** (RAM + VRAM, or unified memory).

| 1-bit  | 2-bit  | 3-bit      | 4-bit  | 8-bit (lossless) |
| ------ | ------ | ---------- | ------ | ---------------- |
| 134 GB | 150 GB | 176–208 GB | 256 GB | 272 GB           |

Planning estimates for 16K text context and one slot, allowing roughly 20–32 GiB above the weights for KV cache, runtime and OS. Memory targets use GiB, commonly marketed as GB. Longer contexts, vision and DSpark need more memory.

For 3-bit, use 176GB+ for `UD-IQ3_XXS`, 192GB+ for `UD-IQ3_S`, or 208GB+ for `UD-Q3_K_XL`. The 8-bit column refers to `UD-Q8_K_XL`, the highest-precision GGUF listed here.

**Weight sizes:** Downloads below use decimal GB. Start with 16K context and increase it as memory allows.

| Quant        | Download size (GB) | Weight size (GiB) |
| ------------ | ------------------ | ----------------- |
| `UD-IQ1_M`   | 129.4 GB           | 120.5 GiB         |
| `UD-IQ2_XXS` | 134.9 GB           | 125.7 GiB         |
| `UD-Q2_K_XL` | 143.9 GB           | 134.0 GiB         |
| `UD-IQ3_XXS` | 160.0 GB           | 149.1 GiB         |
| `UD-IQ3_S`   | 175.5 GB           | 163.4 GiB         |
| `UD-Q3_K_XL` | 194.0 GB           | 180.6 GiB         |
| `UD-Q4_K_XL` | 249.4 GB           | 232.3 GiB         |
| `UD-Q8_K_XL` | 259.1 GB           | 241.3 GiB         |

### Recommended Settings

Use MiniMax’s recommended configurations:

| Setting     | Value            |
| ----------- | ---------------- |
| Temperature | `1.0`            |
| Top-p       | `0.95`           |
| Top-k       | `0` (disabled)   |
| Min-p       | `0.0` (disabled) |

#### Thinking effort

The template uses adaptive thinking. Set `reasoning_effort` to `low`, `medium`, `high`, `xhigh` or `max`. We use `high`; effort is separate from context and output-token limits.

```bash
--chat-template-kwargs '{"reasoning_effort":"high"}'
```

### 📊 Quantization Analysis

UD-Q8\_K\_XL is a direct lossless conversion from the original safetensors. MiniMax uses NVFP4 for the MoE layers and MXFP8 for the rest - we left UD-Q8\_K\_XL at NVFP4 + BF16.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FwPOGpnK3wxeulnC9lrJq%2Fminimax-kld.png?alt=media&amp;token=c7fb9b86-729f-45f1-827a-c8acee92d0a5" alt="MiniMax-M3.1-Flash GGUF KLD by file size across seven evaluation categories. Lower is better."><figcaption><p>Mean KLD by file size. Lower is better; the vertical axis is logarithmic.</p></figcaption></figure>

We tested the MiniMax M3.1 Flash quants we made vs generic llama.cpp + imatrix quants across multiple different domains to ensure our quantization algorithms do not overfit to a particular area. We show how Unsloth Dynamic v3 works surprisingly well across all fields.

We also did top-1% plots and show how UD3 continues to work well even at smaller bits vs naive llama.cpp layouts with imatrix.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FEGL7IdsBG2LJa8kp9krw%2Fsize_vs_top1_per_axis.png?alt=media&amp;token=1898d4b7-b4b4-46a7-b5e2-9a9a4915cdce" alt=""><figcaption></figcaption></figure>

**Top-1 agreement by quant:**

| Quant        | File size | General chat top-1 | Math top-1 |
| ------------ | --------- | ------------------ | ---------- |
| `UD-IQ1_M`   | 129.4 GB  | 86.2%              | 94.9%      |
| `UD-IQ2_XXS` | 134.9 GB  | 87.5%              | 95.3%      |
| `UD-Q2_K_XL` | 143.9 GB  | 88.5%              | 95.7%      |
| `UD-IQ3_XXS` | 160.0 GB  | 89.9%              | 96.3%      |
| `UD-IQ3_S`   | 175.5 GB  | 91.2%              | 96.8%      |
| `UD-Q3_K_XL` | 194.0 GB  | 92.6%              | 97.4%      |
| `UD-Q4_K_XL` | 249.4 GB  | 97.3%              | 99.0%      |
| `UD-Q8_K_XL` | 259.1 GB  | 97.8%              | 99.3%      |

Dynamic quants show lower KLD and higher agreement at comparable or smaller sizes. **UD-Q3\_K\_XL (194.0 GB)** beats generic **IQ4\_XS (about 230 GB)** on top-1 agreement in all seven categories.

**Choosing a quant:** Q2 offers 88.5% general-chat and 95.7% math agreement at 143.9 GB. Q4 raises these to 97.3% and 99.0%, and multilingual agreement from Q3’s 90.8% to 97.6%. Q8 adds 9.7 GB for a smaller fidelity gain.

## Run MiniMax-M3.1-Flash Tutorials:

We use **UD-Q2\_K\_XL** for the examples. Image input and DSpark are auto enabled in Unsloth.

### 🦥 Unsloth Guide

[Unsloth Desktop](https://unsloth.ai/docs/desktop) is our open-source UI for macOS, Windows and Linux. Download GGUFs and configure sampling and CPU/GPU offloading in one app.

{% stepper %}
{% step %}

### Install Unsloth

Download [Unsloth Desktop](https://unsloth.ai/download) for your OS. Use a build with MiniMax-M3.1 support, or the llama.cpp PR below.

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>
{% endstep %}

{% step %}

### Search and download MiniMax-M3.1-Flash

In **Unsloth Chat** or **Model hub**, search for **MiniMax-M3.1-Flash** and select [unsloth/MiniMax-M3.1-Flash-GGUF](https://huggingface.co/unsloth/MiniMax-M3.1-Flash-GGUF). Download your quant; we use `UD-Q2_K_XL` (143.9 GB).
{% endstep %}

{% step %}

### Run MiniMax-M3.1-Flash

Load the model with the recommended settings, **16K context**, **one parallel slot** and `high` reasoning effort. Use the included chat template and adjust CPU/GPU offloading to fit your memory.

For more information, see the [Unsloth inference guide](/docs/new/studio/chat.md).
{% endstep %}

{% step %}

### Serve MiniMax-M3.1-Flash with Unsloth API

With a compatible runtime, serve the model using `unsloth run` and llama-server options:

```bash
unsloth run --model unsloth/MiniMax-M3.1-Flash-GGUF:UD-Q2_K_XL \
    --temp 1.0 --top-p 0.95 --top-k 0 --min-p 0.0 \
    --chat-template-kwargs '{"reasoning_effort":"high"}' \
    --host 127.0.0.1 --port 8080
```

Chat at `http://localhost:8080`; the OpenAI-compatible API base URL is `http://localhost:8080/v1`.
{% endstep %}

{% step %}

### Connect your tools

Connect your API client to this endpoint using a model ID from `/v1/models`. Keep the server running.
{% endstep %}
{% endstepper %}

### 🦙 Run MiniMax-M3.1-Flash in llama.cpp

{% stepper %}
{% step %}

### Build llama.cpp with MiniMax-M3.1 support

Build [PR #31192](https://github.com/ggml-org/llama.cpp/pull/31192) using Bash on Linux, WSL or macOS.

On Ubuntu / WSL, install the build dependencies:

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake git libssl-dev
```

For NVIDIA, install the [CUDA toolkit](https://developer.nvidia.com/cuda-downloads). On macOS, install Xcode command line tools and CMake; use `-DGGML_CUDA=OFF` (Metal is enabled by default). Use `OFF` for CPU-only builds too.

```bash
git clone https://github.com/ggml-org/llama.cpp
git -C llama.cpp fetch origin pull/31192/head:minimax-m31
git -C llama.cpp checkout minimax-m31
cmake llama.cpp -B llama.cpp/build \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --target llama-server
```

{% endstep %}

{% step %}

### Download the GGUF

Install the Hugging Face CLI and download **all four shards** of `UD-Q2_K_XL`:

```bash
pip install -U huggingface_hub
hf download unsloth/MiniMax-M3.1-Flash-GGUF \
    --local-dir unsloth/MiniMax-M3.1-Flash-GGUF \
    --include "UD-Q2_K_XL/*"
```

Keep all shards together and point `--model` at the first; llama.cpp loads the rest. For another quant, change the download filter and model path.
{% endstep %}

{% step %}

### Run MiniMax-M3.1-Flash

Start the local chat server:

```bash
./llama.cpp/build/bin/llama-server \
    --model unsloth/MiniMax-M3.1-Flash-GGUF/UD-Q2_K_XL/MiniMax-M3.1-Flash-UD-Q2_K_XL-00001-of-00004.gguf \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 0 \
    --min-p 0.0 \
    --chat-template-kwargs '{"reasoning_effort":"high"}' \
    --host 127.0.0.1 --port 8080
```

{% endstep %}
{% endstepper %}

#### Image inputs

For image inputs, download the separate `mmproj-BF16.gguf` vision projector (about 1.74 GB):

```bash
hf download unsloth/MiniMax-M3.1-Flash-GGUF \
    --local-dir unsloth/MiniMax-M3.1-Flash-GGUF \
    --include "mmproj-BF16.gguf"
```

Add this server option and allow extra memory for the projector and image processing:

```bash
--mmproj unsloth/MiniMax-M3.1-Flash-GGUF/mmproj-BF16.gguf
```

### ⚡ DSpark - Speculative Decoding

M3.1 replaces EAGLE-like [MTP](/docs/models/mtp.md) with **DSpark**: a draft model proposes tokens for the main model to verify, potentially speeding up decoding. It needs a matching MiniMax-M3.1 draft and extra memory.

[PR #31192](https://github.com/ggml-org/llama.cpp/pull/31192) supports DSpark, the commands above use ordinary decoding. With a matching draft, add these options and replace the filename with its local path:

```bash
--spec-type draft-dspark \
    -md MiniMax-M3.1-Flash-DSpark-BF16.gguf \
    --spec-draft-p-min 0
```

## 📊 Benchmarks

### GGUF KLD and Top-1% Benchmarks

Across the seven categories, **UD-Q2\_K\_XL reaches \~85.3–95.7% top-1 agreement**, **UD-Q4\_K\_XL \~97.3–99.0%**, and **UD-Q8\_K\_XL \~97.8–99.3%**. Q4 saves 9.7 GB versus Q8 with only a small agreement gap; Q8 also has lower KLD throughout.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FLKBqgmIgiNf9wTXbGNsX%2Fminimax-top1.png?alt=media&amp;token=3a155732-d550-4397-86b2-c3d134e5912d" alt="MiniMax-M3.1-Flash GGUF top-1 agreement by file size across seven evaluation categories. Higher is better."><figcaption><p>Top-1 token agreement across seven categories. Higher is better; reported values are approximate graph readings.</p></figcaption></figure>

### Official Benchmarks

[MiniMax’s official results](https://huggingface.co/MiniMaxAI/MiniMax-M3.1-Flash) are shown below.

| Benchmark               | MiniMax-M3.1-Flash | DeepSeek-V4.1-Flash-1017 |
| ----------------------- | ------------------ | ------------------------ |
| Automation-Bench v1.0.6 | 62.8               | 60.5                     |
| Terminal Bench 4.0      | 38.1               | 42.3                     |
| DeepSWE v1.1            | 73.7               | 77.0                     |
| NL2Repo-Bench           | 61.2               | 68.2                     |
| BabyVision (with tools) | 91.0               | 92.5                     |
| HLE (without tools)†    | 43.4               | 42.6                     |
| OSWorld 2.0             | 61.7               | —                        |
| LOCA-Bench 256K         | 60.3               | —                        |

† HLE uses the text-only subset. Evaluation harnesses: Codex 0.149.1 for Terminal Bench; mini-SWE-agent 2.4.5 for DeepSWE; Claude Code 2.1.233 for NL2Repo. The latter two use 512K context. Scores depend on setup and reasoning effort; — means no reported result.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/minimax-m3.1-flash.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
