> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/flint.md).

# Flint: Run Locally Guide

Run Recursive Flint locally with Unsloth Dynamic GGUFs, Unsloth Desktop and llama.cpp.

Recursive Flint is a **39.8B-parameter MoE (2.5B active)**, with reasoning, multi-turn tool use and **256K context**. Flint is released as Apache-2.0 and is the **strongest MoE model** under 50B parameters on agentic coding benchmarks. Run locally in [Unsloth Desktop](/docs/desktop.md) or llama.cpp with Unsloth’s 3-bit GGUFs on 24GB RAM. You can run at 125+ tokens/sec on an M4 Pro MacBook Pro and 150+ on a 64GB NVIDIA RTX Spark.

Our **3-bit UD-Q3\_K\_XL GGUF** is 18.50GB and fits **24GB RAM setups** at short contexts. The full BF16 GGUF is 79.58GB, while UD-Q4\_K\_XL is 25.05GB. GGUFs: [unsloth/flint-GGUF](https://huggingface.co/unsloth/flint-GGUF)

#### ⚙️ Usage Guide

**Table: Hardware Requirements** (RAM + VRAM, or unified memory).

| 2-bit    | 3-bit    | 4-bit | 6-bit | 8-bit |
| -------- | -------- | ----- | ----- | ----- |
| 13–15 GB | 16–20 GB | 26 GB | 38 GB | 44 GB |

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FGXYEQqEXseTna162HHNa%2Fflint%20pic.webp?alt=media&amp;token=bcddff05-8e5d-4026-a05e-02cab135af2e" alt="" width="563"><figcaption><p>Flint running inside of Unsloth.</p></figcaption></figure>

#### Recommended Settings

[Recursive recommends](https://huggingface.co/RecursiveSI/flint) the following sampling settings:

| Parameter       | Setting                          |
| --------------- | -------------------------------- |
| Temperature     | 1.0                              |
| Top-p           | 0.95                             |
| Top-k           | 20                               |
| Maximum context | 262,144 tokens (prompt + output) |

**Chat template:** Use the template bundled with the GGUF. For custom multi-turn clients, preserve returned `reasoning_content` and tool-call messages in the conversation history, as described in the model card.

### Run Flint Guide

We'll use **UD-Q4\_K\_XL (25.05GB)**. If memory is limited, select **UD-Q3\_K\_XL (18.5GB)** instead.

You can also read Recursive's official [guide for Flint here](#usage-guide).

#### 🦥 Run Flint in Unsloth Desktop

Run Flint in [Unsloth Desktop](https://unsloth.ai/docs/desktop) on **macOS, Windows and Linux**.

{% stepper %}
{% step %}

#### Install Unsloth

Download and launch the latest [Unsloth Desktop app](https://unsloth.ai/download) for your device:

* [Download for macOS](https://unsloth.ai/download/mac)
* [Download for Windows](https://unsloth.ai/download/windows)
* [Download for Linux](https://unsloth.ai/download/linux)

For manual installation on macOS, Linux or WSL:

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

For Windows PowerShell:

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

{% endstep %}

{% step %}

#### Download and run Flint

1. Open **Model hub** or the **Select model** dropdown in Chat.
2. Search for `unsloth/flint-GGUF`, select the Unsloth repository, and download `UD-Q4_K_XL` or a smaller quant.

Flint accepts **text input**. See our [Unsloth Chat guide](https://unsloth.ai/docs/new/studio/chat) for model loading and inference settings.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FGXYEQqEXseTna162HHNa%2Fflint%20pic.webp?alt=media&amp;token=bcddff05-8e5d-4026-a05e-02cab135af2e" alt="" width="375"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Connect a coding agent

After installing Unsloth and your preferred agent, run this from your project folder:

```bash
unsloth start claude \
    --model unsloth/flint-GGUF:UD-Q4_K_XL \
    --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0
```

This uses a larger context for coding tasks and requires more memory than the 8K example. You can replace `claude` with another supported agent, such as `opencode`. See [Unsloth Start](https://unsloth.ai/docs/integrations/unsloth-start) for setup and supported integrations.
{% endstep %}

{% step %}

#### Serve Flint with Unsloth API

Use `unsloth run` to load the quant and serve it locally. The `:UD-Q4_K_XL` suffix chooses the quantization:

```bash
unsloth run --model unsloth/flint-GGUF:UD-Q4_K_XL \
    --parallel 1 --alias flint \
    --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0 \
    --host 127.0.0.1 --port 8001
```

Use the endpoint and authentication details shown by Unsloth. For Desktop API access, create a key in **Settings → API** and follow our [API guide](https://unsloth.ai/docs/basics/api) to connect your client.
{% endstep %}
{% endstepper %}

### 📊 Quantization Analysis

The benchmarks below from the [Flint GGUF README](https://huggingface.co/unsloth/flint-GGUF) compare quantization quality against model size. **Lower KLD is better; higher top-1 accuracy is better.** These measure how closely each quant matches the reference model. Read more about [Unsloth Dynamic 3.0 GGUFs](https://unsloth.ai/docs/basics/unsloth-dynamic-v3.0-gguf).

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FR3k6FK1PyIJuU7qBx6h8%2Fsize_vs_top1(3).png?alt=media&amp;token=1ffcb4fc-696f-4fec-92a8-68b2c160246b" alt="" width="563"><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FtU9zTQiXR66yrHnGX19y%2Fsize_vs_kld(3).png?alt=media&amp;token=0d18a630-93d4-448f-b00b-df41000d61de" alt="" width="563"><figcaption></figcaption></figure></div>

### 🦙 Run Flint in llama.cpp

{% stepper %}
{% step %}

#### Build llama.cpp

Use the [latest llama.cpp](https://github.com/ggml-org/llama.cpp) with Flint support. The commands below use a macOS/Linux/WSL shell. Install Git, CMake and a C++ compiler first. For NVIDIA, also install the CUDA toolkit.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone --branch iq1-narrow https://github.com/unslothai/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

**Apple Silicon:** replace `-DGGML_CUDA=ON` with `-DGGML_CUDA=OFF`; Metal is enabled by default. For CPU-only builds, also set `-DGGML_METAL=OFF` on macOS. See the [build instructions](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md) for other platforms.
{% endstep %}

{% step %}

#### Download the Unsloth GGUF

From the same working directory, download the exact 4-bit file:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U huggingface_hub
hf download unsloth/flint-GGUF \
    flint-UD-Q4_K_XL.gguf \
    --local-dir models/flint
```

For the smaller 2-bit model, replace the filename with `flint-UD-IQ2_XXS.gguf` in both the download and run commands. If you choose BF16, download all three shards into the same folder and point the runtime at the first shard.
{% endstep %}

{% step %}

#### Chat with Flint

```bash
./llama.cpp/llama-cli \
    --model models/flint/flint-UD-Q4_K_XL.gguf \
    --ctx-size 8192 --n-gpu-layers 99 \
    --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0 \
    --prompt "Write a Python function that merges overlapping intervals and include tests."
```

`--jinja` uses the model's chat template. Reduce `--n-gpu-layers` if VRAM is limited, or set it to `0` for CPU inference. Keep enough system RAM for layers that are offloaded.
{% endstep %}
{% endstepper %}

### Benchmarks

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fvx89npzlDGi6Mq3sWqmJ%2Fflint_benchmarks_nvfp4.png?alt=media&amp;token=759b8b48-8c15-4ca9-a1a5-3d3aab34a522" alt=""><figcaption></figcaption></figure>

| Model         | Terminal-Bench 2.1 | SWE-bench Pro v2† | SWE-bench Verified | LiveCodeBench v6 | IFBench | IFEval |
| ------------- | ------------------ | ----------------- | ------------------ | ---------------- | ------- | ------ |
| Flint BF16    | 54.9               | 89.7              | 74.2               | 80.3             | 89.2    | 95.1   |
| Flint NVFP4   | 53.7               | 88.5              | 74.1               | 80.8             | 88.1    | 94.6   |
| Qwen 3.5      | 38.7               | 68.6              | 69.2               | 74.6             | 70.2    | 91.9   |
| Qwen 3.6      | 44.9               | 73.8              | 73.4               | 80.4             | 67.9    | 89.6   |
| Laguna XS 2.1 | 24.7†              | 38.6              | 70.9               | 49.5†            | 34.4†   | 73.7†  |
| Qwen 3.8      | 73.0               | 94.9              | 75.6†              | 90.3             | 79.5    | 94.6†  |
| Muse Glimmer  | 51.7               | 86.0              | 76.0               | 63.5†            | 77.0    | 94.7†  |
| Gemma 4       | 43.4               | 61.7              | 66.6               | 80.0             | 76.0    | 94.6   |

Notes from the chart:

* † = Measured internally (as marked in the original chart).
* Flint BF16: 40B total parameters, approximately 2B active.
* Flint NVFP4: Quantized Flint checkpoint.
* Qwen 3.5, Qwen 3.6, Laguna XS 2.1: Sparse MoE category (33–35B total, 3B active).
* Qwen 3.8, Muse Glimmer, Gemma 4: Dense category (27–31B).
* All benchmark panels use a zero-based scale.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/flint.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
