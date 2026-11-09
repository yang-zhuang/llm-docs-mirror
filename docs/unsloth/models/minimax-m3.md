> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/minimax-m3.md).

# MiniMax M3 - How to Run Locally

Run MiniMax M3 LLM locally on your own device!

MiniMax M3 is a new **\~428B (23B active)** open model for coding, agentic workflows, cowork tasks, and multimodal chat. The multimodal model has support for text, image, and video inputs, and a **1M context** **window**. The unquantized bf16 weights are \~**855GB** and the 1-bit GGUF decreases this to just **128GB (-85%)**: [**MiniMax-M3 GGUF**](https://huggingface.co/unsloth/MiniMax-M3-GGUF)

The model performs on par with Gemini 3.1 Pro - scoring 59% on SWE-Bench Pro, 66% on Terminal-Bench 2.1, 34.8% on SWE-fficiency, and 28.8% on KernelBench Hard. Thanks MiniMax for day zero access.

{% columns %}
{% column width="50%" %}
{% hint style="info" %}
MiniMax-M3 GGUFs are currently experimental. MiniMax-M3 itself is native multimodal, but the current experimental GGUF is **text-only** and does not support MiniMax Sparse Attention.
{% endhint %}
{% endcolumn %}

{% column width="50%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F7A3LPw7ex1psFIPkY6FF%2Fminimax%20m3%20guide.gif?alt=media&amp;token=b733672e-fa14-4572-952c-c9b3dbf82beb" alt="" width="375"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

#### :gear: Usage Guide

The smallest GGUF quant, `UD-IQ1_M`, uses **128GB** of disk space. Because the file size does not include KV cache, context allocation, try to have at least **133GB RAM** to run the model. It's recommended to use `UD-IQ3_XXS` which is **159GB** for best results.

The **4-bit** `UD-IQ4_XS` quant is **208GB**, while `UD-Q4_K_XL` is **265GB**. These are better suited to 256GB+ or 512GB-class systems, multi-GPU servers, or systems with CPU RAM plus GPU offload.

**Table: Inference hardware requirements** (units = total memory: RAM + VRAM, or unified memory)

<table><thead><tr><th>1-bit</th><th>2-bit</th><th width="128">3-bit</th><th>4-bit</th><th>5-bit</th><th>8-bit</th></tr></thead><tbody><tr><td>133 GB</td><td>148 GB</td><td>164-200 GB</td><td>213-270 GB</td><td>325 GB</td><td>460-470 GB</td></tr></tbody></table>

{% hint style="success" %}
For best performance, make sure your total available memory, including VRAM and system RAM, exceeds the quantized model file size by a comfortable margin.
{% endhint %}

#### Recommended Settings

MiniMax recommends the following parameters for best performance: `temperature=1.0`, `top_p=0.95`, `top_k=40`.

{% columns %}
{% column %}

| `temperature = 1.0` |
| ------------------- |
| `top_p = 0.95`      |
| `top_k = 40`        |
| {% endcolumn %}     |

{% column %}

* **Maximum context window:** `1,048,576`
* Default system prompt:

{% code overflow="wrap" %}

```
You are a helpful assistant. Your name is MiniMax-M3 and was built by MiniMax.
```

{% endcode %}
{% endcolumn %}
{% endcolumns %}

## Run MiniMax-M3 Tutorials:

For this tutorial, we will use the smallest current quant, UD-IQ1\_M, because MiniMax-M3 is large. Replace UD-IQ1\_M with UD-IQ4\_XS, UD-Q4\_K\_XL, or another quant if your machine has enough memory. You can now run MiniMax-M3 in Unsloth.

Unsloth Guide

#### Download Unsloth

#### Download Unsloth

<https://unsloth.ai/download>

<https://unsloth.ai/download>

### Unsloth Guide

#### Download Unsloth

<https://unsloth.ai/download>

{% hint style="success" %}
You can now run MiniMax M3 via [Unsloth](#unsloth-studio-guide) ✨. Ensure you use > [`v0.1.463-beta`](https://github.com/unslothai/unsloth/tree/v0.1.462-beta) or `2026.6.6`.
{% endhint %}

MiniMax M3 runs in Unsloth on MacOS, Windows, and Linux. You can:

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

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fszoidwwj70dLm5vBjpmL%2Fdiffusiongemma.gif?alt=media&amp;token=8ce359fd-f92c-4cf8-a491-06b04c505cb7" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% stepper %}
{% step %}

#### Install Unsloth

Ensure you use the latest [`v0.1.463-beta`](https://github.com/unslothai/unsloth/tree/v0.1.462-beta) or `2026.6.6`. Run in your terminal:

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
{% endstep %}

{% step %}

#### Search and download MiniMax M3

Then go to the [Unsloth Chat](/docs/new/studio/chat.md) tab and search for MiniMax M3 in the search bar and download your desired model and quant.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FYUbbg1xVmfmJYVEQTNaS%2FScreenshot%202026-06-12%20at%206.33.22%E2%80%AFPM.png?alt=media&amp;token=9b672870-3c8b-4b38-bfe8-16cdef0b5e25" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Run MiniMax M3

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F7A3LPw7ex1psFIPkY6FF%2Fminimax%20m3%20guide.gif?alt=media&amp;token=b733672e-fa14-4572-952c-c9b3dbf82beb" alt=""><figcaption></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### 🦙 Llama.cpp Guide

{% stepper %}
{% step %}
Obtain the SPECIFIC `llama.cpp` PR on [**GitHub here**](https://github.com/ggml-org/llama.cpp/pull/24523). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
git fetch origin pull/24523/head:minimax-m3
git checkout minimax-m3
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j --target llama-cli llama-server
```

{% endstep %}

{% step %}
You can now use `llama.cpp` directly to load and download models, just like `ollama run`. First, select the quantization type you want like `Q2_K_XL`. Also use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location. Note this download process might be very slow, so it's probably best to use the manual download process in the next section.

```bash
export LLAMA_CACHE="unsloth/MiniMax-M3-GGUF"
./build/bin/llama-cli \
    -hf unsloth/MiniMax-M3-GGUF:UD-IQ1_M \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 40
```

{% hint style="info" %}
Note: MiniMax Sparse Attention is not supported yet, so inference falls back to dense attention.
{% endhint %}
{% endstep %}

{% step %}
If you want to download the model manually, we can download the model via the code below (after installing `pip install huggingface_hub`). If downloads get stuck, see: [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

```bash
hf download unsloth/MiniMax-M3-GGUF \
    --local-dir unsloth/MiniMax-M3-GGUF \
    --include "*UD-IQ1_M*" # Use "*UD-IQ4_XS*" for 4-bit
```

{% endstep %}

{% step %}
You can edit `--threads 32` for the number of CPU threads, `--ctx-size 32768` for context length, `--n-gpu-layers 2` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference. Remember MSA is not yet supported, so keep `--ctx-size` modest - dense attention at very long contexts will use a lot of memory.

{% code overflow="wrap" %}

```bash
./build/bin/llama-cli \
    --model unsloth/MiniMax-M3-GGUF/UD-IQ1_M/MiniMax-M3-UD-IQ1_M-00001-of-00004.gguf \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 40
```

{% endcode %}
{% endstep %}
{% endstepper %}

## 📊 Benchmarks

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F4SjJ6hXo8PijYgtdfMGp%2Fminimaxm3%20short%20benchmarks.jpeg?alt=media&amp;token=1a544bfd-1c81-4b45-89f7-04b88190d473" alt=""><figcaption></figcaption></figure>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FnRfDibKjJo3LG99RxlqW%2Fminimaxm3.jpeg?alt=media&amp;token=f0c4b21f-9680-4fa8-862f-c79f1c0bf55f" alt=""><figcaption></figcaption></figure>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/minimax-m3.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
