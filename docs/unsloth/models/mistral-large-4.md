> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/mistral-large-4.md).

# Mistral Large 4 (Le Chonk): Run Locally

Guide to running Mistral Large 4 GGUFs locally with Unsloth and llama.cpp.

Mistral Large 4 (Le Chonk) is Mistral’s **1 trillion parameter** MoE model with **52B active parameters** (including embeddings and output layers). Mistral Large 4 is the **strongest Western open** model to date and supports text and image inputs, a **1M-context** window, 160+ languages, and reasoning. You can run Le Chonk locally with Unsloth Dynamic GGUFs via Unsloth or llama.cpp. GGUF: [Mistral-Large-4-1T-A52B-GGUF](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF)

Dynamic 1bit retains **91% of top-1 accuracy** across coding, agentic tasks, math and other areas whilst being 80% smaller (**223GB** vs **1.1TB** FP8). Dynamic 2bit retains 95% top-1 accuracy whilst 66% smaller (378GB). Thank you Mistral for day zero access.

<a href="/docs/models/mistral-large-4.md#run-mistral-large-4-tutorials" class="button primary">Run Mistral Large 4 Tutorials</a><a href="/docs/models/mistral-large-4.md#quantization-analysis" class="button secondary">Quant Analysis</a>

### **⚙️ Usage Guide**

The smallest Dynamic 1-bit quant, `UD-IQ1_S`, uses approximately **233GB** of disk space which should fit on 256GB RAM including a Mac Studio or 2x NVIDIA DGX Sparks.

**Table: Hardware requirements** (units = total memory: RAM + VRAM, or unified memory)

| 1-bit     | 2-bit     | 3-bit     | 4-bit | 8-bit |
| --------- | --------- | --------- | ----- | ----- |
| 256–270GB | 310–390GB | 435–500GB | 630GB | 1.2TB |

For best performance, your total available **RAM + VRAM**, or unified memory, should exceed the quant’s file size with room for the operating system, KV cache and runtime buffers. Longer contexts need more memory.

#### Recommended Settings

Mistral recommends the same sampling settings for all reasoning efforts:

| Temperature | Top-p  |
| ----------- | ------ |
| `1.0`       | `0.95` |

* Reasoning efforts = low, medium, and high
* Maximum **context window** is `1,048,576` tokens.

We also ran KLD benchmarks for all quants - more details in [#quantization-analysis](#quantization-analysis "mention")

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FAtJWJHFOCP7cu7IQKiGt%2Fsize_vs_top1_unsloth.png?alt=media&amp;token=27d694b8-db6f-4661-a8c8-c354823ca2c6" alt="" width="563"><figcaption></figcaption></figure>

## Run Mistral Large 4 Tutorials:

The examples below use [`UD-Q2_K_XL`](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-Q2_K_XL) for text inference. You can change the quantization type to any available quant in the [GGUF repository](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF).

### 🦥 Run Mistral Large 4 in Unsloth

[Unsloth Desktop](https://unsloth.ai/docs/desktop) runs GGUFs locally on **macOS, Windows and Linux**, automatically offloads to RAM and detects multi-GPU setups.

{% stepper %}
{% step %}

#### Install Unsloth

The easiest way to get started is by downloading the [Unsloth Desktop app](/docs/desktop.md). Works on [macOS](/docs/get-started/install/mac.md), [Windows](/docs/get-started/install/windows-installation.md), and [Linux](/docs/get-started/install/linux.md).

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

Or, if you prefer to install manually:

**MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows PowerShell:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

{% endstep %}

{% step %}

#### Search and download Mistral Large 4

Go to [Unsloth Chat](https://unsloth.ai/docs/new/studio/chat) or Model hub, search for **Mistral-Large-4-1T-A52B** and select [unsloth/Mistral-Large-4-1T-A52B-GGUF](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF). Download your desired quant using the sizes and memory requirements above.
{% endstep %}

{% step %}

#### Run Mistral Large 4

Mistral Large 4 uses `high` reasoning effort by default. Use `low` for fast chat, `medium` for everyday tasks, or `high` for complex prompts and agentic coding. Unsloth automatically selects the best configurations for you but you can still adjust manually.

For more information, you can view our [Unsloth inference guide](/docs/new/studio/chat.md).
{% endstep %}

{% step %}

#### Serve Mistral Large 4 with Unsloth API

You can use the `unsloth run` command to serve Mistral Large 4 via an API using `llama-server` runtime flags, including context sizing, GPU layers, threading and sampling. For more info see our [API docs](https://unsloth.ai/docs/basics/api) or [unsloth start](https://unsloth.ai/docs/integrations/unsloth-start).

{% code overflow="wrap" %}

```bash
unsloth run --model unsloth/Mistral-Large-4-1T-A52B-GGUF:UD-Q2_K_XL \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 0 \
    --min-p 0.0 \
    --chat-template-kwargs '{"reasoning_effort":"high"}'
```

{% endcode %}

Use a runtime with Mistral Large 4 support.
{% endstep %}

{% step %}

#### Unsloth is now ready

You can connect Mistral Large 4 to your tools through Unsloth Desktop. Unsloth also supports the following workflows:

* **Connect tools:** [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md), [web search](/docs/new/studio/chat.md#advanced-web-search), [MCP](/docs/basics/mcp.md) and more
* **Train models:** Fine-tune other supported text, diffusion, [embedding](/docs/basics/embedding-finetuning.md), and more
* **Generate media:** Create and train [images](/docs/basics/diffusion-image.md), video, [TTS](/docs/basics/text-to-speech-tts-fine-tuning.md) locally

<div align="center"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FYShiiub5gs5pCQLX6d4U%2FScreenshot%202026-08-15%20at%2012.18.24%E2%80%AFAM.png?alt=media&amp;token=d6996797-a144-4113-b4c3-155cca6c39a0" alt="Unsloth Desktop Agents settings interface example" width="563"><figcaption><p>Unsloth Desktop’s Agents settings (interface example). Select Mistral Large 4 and your downloaded quant when connecting a tool.</p></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### Quantization Analysis

We ran KLD and top-1% benchmarks across a variety of areas like tool calling, coding and agentic long traces, and show that Unsloth dynamic quantization (UD3) can retain a lot of accuracy whilst still making the model smaller.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F57miJQhlcpxXmZ1XuYc1%2Fsize_vs_top1_per_axis.png?alt=media&amp;token=6e121fc8-6f9a-43df-bea8-d317cbe5448e" alt=""><figcaption></figcaption></figure>

We also ran KLD and provide it per corpus as well:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FeclA1iBNKp9D2Gk2TzyL%2Fsize_vs_kld_per_axis.png?alt=media&amp;token=88cfa583-370a-4e1b-bf44-e9b797df8a9d" alt=""><figcaption></figcaption></figure>

| Quant                                                                                            | Size    | Mean KLD (7 categories) | Top-1 agreement |
| ------------------------------------------------------------------------------------------------ | ------- | ----------------------- | --------------- |
| [UD-IQ1\_S](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-IQ1_S)      | 233 GB  | 0.1263                  | 90.6%           |
| [UD-IQ1\_M](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-IQ1_M)      | 260 GB  | 0.0919                  | 92.3%           |
| [UD-IQ2\_XXS](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-IQ2_XXS)  | 302 GB  | 0.0566                  | 93.9%           |
| [UD-Q2\_K\_XL](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-Q2_K_XL) | 378 GB  | 0.0298                  | 95.6%           |
| [UD-IQ3\_XXS](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-IQ3_XXS)  | 424 GB  | 0.0217                  | 96.2%           |
| [UD-Q3\_K\_XL](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-Q3_K_XL) | 493 GB  | 0.0162                  | 96.6%           |
| [UD-Q4\_K\_XL](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-Q4_K_XL) | 605 GB  | 0.0071                  | 97.8%           |
| [UD-Q5\_K\_XL](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-Q5_K_XL) | 784 GB  | 0.0038                  | 98.5%           |
| [UD-Q6\_K\_XL](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-Q6_K_XL) | 890 GB  | 0.0032                  | 98.6%           |
| [UD-Q8\_K\_XL](https://huggingface.co/unsloth/Mistral-Large-4-1T-A52B-GGUF/tree/main/UD-Q8_K_XL) | 1115 GB |                         |                 |

### 🦙 Run Mistral Large 4 in llama.cpp

Use a llama.cpp build with **Mistral Large 4 support**. The commands below use the `UD-Q2_K_XL` quant (approximately **378GB**).

{% stepper %}
{% step %}

#### Install llama.cpp

Obtain [llama.cpp on GitHub](https://github.com/ggml-org/llama.cpp), or build it below. On Linux with an NVIDIA GPU, install the CUDA toolkit and build dependencies first:

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake curl libcurl4-openssl-dev
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --target llama-cli llama-server
```

For **CPU or Apple Metal**, use `-DGGML_CUDA=OFF`. Metal support is enabled by default on macOS. For Windows and other GPU backends, follow the repository’s build instructions.
{% endstep %}

{% step %}

#### Download and run Mistral Large 4

This command downloads the quant and starts a local chat server:

```bash
./llama.cpp/build/bin/llama-server \
    -hf unsloth/Mistral-Large-4-1T-A52B-GGUF:UD-Q2_K_XL \
    --ctx-size 32768 \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 0 \
    --min-p 0.0 \
    --chat-template-kwargs '{"reasoning_effort":"high"}' \
    --host 127.0.0.1 --port 8080
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080/) in your browser to chat. The API is available at `http://127.0.0.1:8080/v1`.

The example uses a **32K context** to limit KV-cache memory. `--top-k 0` and `--min-p 0.0` disable additional sampling filters so the recommended temperature and top-p settings apply. If you run out of memory, lower `--ctx-size` or choose a smaller quant.
{% endstep %}

{% step %}

#### Optional: download manually

Install the Hugging Face CLI and download only the quant you want:

```bash
pip install -U huggingface_hub
hf download unsloth/Mistral-Large-4-1T-A52B-GGUF \
    --local-dir unsloth/Mistral-Large-4-1T-A52B-GGUF \
    --include "UD-Q2_K_XL/*"
```

Keep **all 9 shards** in the same directory. In the server command above, replace `-hf unsloth/Mistral-Large-4-1T-A52B-GGUF:UD-Q2_K_XL` with:

```bash
--model unsloth/Mistral-Large-4-1T-A52B-GGUF/UD-Q2_K_XL/Mistral-Large-4-1T-A52B-UD-Q2_K_XL-00001-of-00009.gguf
```

llama.cpp loads the remaining shards automatically. To use Dynamic 1-bit instead, download `UD-IQ1_S/*` and point `--model` at `Mistral-Large-4-1T-A52B-UD-IQ1_S-00001-of-00006.gguf` in that folder.
{% endstep %}
{% endstepper %}

### Benchmarks

More benchmarks are listed in Mistral's [official blog](https://mistral.ai/news/mistral-large-4-oss/).

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FrTfj0eor2jVXeH9huZQf%2Fartificial-analysis-coding-agent-index-terminal-bench-4-0.png?alt=media&amp;token=a08947b8-0048-4c41-bc9d-1e5f3daed76f" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQSsBf7oTXp1DgRkktb3a%2Fartificial-analysis-cyber-index.png?alt=media&amp;token=1d81038d-082e-4784-93d4-24ebfdcb8eea" alt=""><figcaption></figcaption></figure></div>

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FvL6PLiJRKH6fuE5PIkY8%2Fweb-browsing-browsecomp.png?alt=media&amp;token=df26f6fa-e8ad-42f1-b29f-8284e9b27323" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FwlEZNXmsndI26kr6zLZP%2Fartificial-analysis-coding-agent-index-vs-token-efficiency.png?alt=media&amp;token=ec0e687d-1165-4602-8e5d-b5ccb395eb85" alt=""><figcaption></figcaption></figure></div>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/mistral-large-4.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
