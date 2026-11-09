> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/nemotron-3.5.md).

# NVIDIA Nemotron 3.5 Lightning: How To Run Locally

NVIDIA Nemotron-3.5-Lightning-30B-A3B is an open 30B parameter, 3B active hybrid reasoning MoE model built for high-volume task execution in long-running agents. It is designed for frequent agent calls including tool use, output validation, result formatting and subagent delegation. The model runs on **20GB RAM** for 4-bit and 33GB for 8-bit.

{% columns %}
{% column %}
With up to **1M context**, Nemotron 3.5 Lightning is one of the fastest and most accurate open execution models for its size. You can run Nemotron 3.5 locally via Unsloth Desktop and Unsloth Dynamic GGUFs. Thanks NVIDIA for day zero support!\
**GGUF:** [Nemotron-3.5-Lightning-30B-A3B](https://huggingface.co/unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF)

See on the right Nemotron-3.5 calls tools nonstop for 10mins in [Unsloth Desktop](/docs/desktop.md):
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FtdFt5POBXMva9TnvtsLM%2Fnvidia%20nemotron%202.gif?alt=media&amp;token=d423e192-87a4-46fb-8aed-e57601cbe8b1" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

#### ⚙️ Usage Guide

NVIDIA recommends these settings for inference:

{% columns %}
{% column %}
**Thinking mode:**

* `temperature = 0.6`
* `top_p = 0.95`
  {% endcolumn %}

{% column %}
**Instruct mode:**

* `temperature = 0.2`
  {% endcolumn %}
  {% endcolumns %}

#### Run Nemotron 3.5 Lightning

Depending on your use-case you will need to use different settings. Nemotron 3.5 Lightning activates 3B parameters per token, making it fast enough for repeated calls throughout long-running agent workflows. **GGUF:** [Nemotron-3.5-Lightning-30B-A3B](https://huggingface.co/unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF)

The 4-bit versions of the model require \~20GB RAM. 8-bit requires 33GB. For these guides, we will be using `UD-Q4-K-XL` which is a good balance between size and accuracy.

<a href="/docs/models/nemotron-3.5.md#unsloth-desktop-guide" class="button primary">Run in Unsloth Desktop</a><a href="/pages/KgtUq1iGVTDBeUIfzcv2#llama.cpp-tutorial" class="button secondary">Run in llama.cpp</a>

#### 🦥 Unsloth Desktop Guide

For this tutorial, we will be using [Unsloth Desktop](#unsloth-desktop-guide), an open-source local app for running and training models. With Unsloth, you can run models locally on **Mac, Windows and Linux** and:

{% columns %}
{% column %}

* Search, download and run GGUFs and safetensor models
* **Compare** models **side-by-side**
* Use **self-healing** tool calling and **web search**
* Run **code execution** with Python and Bash
* Use automatic inference parameter tuning
* Train LLMs 2x faster with 70% less VRAM
  {% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fy2ZDOKN4Uzw1fAKS7s13%2Fmuse%20glimmer%20unsloth%20final%20pic.png?alt=media&amp;token=efa438bf-907c-4121-b0b7-75936776d49e" alt=""><figcaption></figcaption></figure>
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

#### Search and download Nemotron 3.5

Go to [Unsloth Chat](/docs/new/studio/chat.md) or Model hub and search for Nemotron 3.5 in the search bar and download your desired model and quant.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FnEsctmLQ7YTzQ9d4JwBa%2FScreenshot%202026-08-12%20at%207.18.20%E2%80%AFAM.png?alt=media&amp;token=faf9a554-0008-438d-8795-34cf99db44ec" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Run Nemotron 3.5 Lightning

Inference parameters should be auto-set when using Unsloth, however you can still change it manually. You can also edit the context length, chat template and other settings.

For more information, you can view our [Unsloth inference guide](/docs/new/studio/chat.md).

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FtdFt5POBXMva9TnvtsLM%2Fnvidia%20nemotron%202.gif?alt=media&amp;token=d423e192-87a4-46fb-8aed-e57601cbe8b1" alt=""><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

#### 🦙 Llama.cpp Tutorial:

Instructions to run in llama.cpp (note we will be using 4-bit to fit most devices):

{% stepper %}
{% step %}
Obtain the latest [`llama.cpp`](https://github.com/ggml-org/llama.cpp) and build it. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you do not have a CUDA GPU or want CPU inference. **For Apple Mac and Metal devices**, set `-DGGML_CUDA=OFF`. Metal support is enabled by default.

{% code overflow="wrap" %}

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first \
    --target llama-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endcode %}
{% endstep %}

{% step %}
Now let's download the model manually. We can do this via the code below after installing `huggingface_hub`. If downloads get stuck, see: Hugging Face Hub, XET debugging

{% code overflow="wrap" %}

```bash
pip install huggingface_hub
hf download unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF \
    --local-dir unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF \
    --include "*UD-Q4_K_XL*" # Use "*UD-Q2_K_XL*" for Dynamic 2bit
```

{% endcode %}
{% endstep %}

{% step %}
Run the model in conversation mode:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-UD-Q4_K_XL.gguf \
    --temp 0.6 \
    --top-p 0.95 \
    --min-p 0.01
```

{% endcode %}
{% endstep %}
{% endstepper %}

{% hint style="info" %}
Nemotron 3.5 Lightning ships with MTP and dedicated DFlash and DSpark draft models for speculative decoding. These draft models predict multiple tokens ahead, increasing output speed for high-volume agent workloads.
{% endhint %}

#### 🦥 Fine-tuning Nemotron 3.5 Lightning

Unsloth supports post-training for the entire NVIDIA Nemotron model family. Nemotron 3.5 Lightning is useful for specialized, high-frequency work inside long-running agents. You can train the model 2x faster with 70% less VRAM using Unsloth.

Useful fine-tuning data can include:

* **Tool calling:** choosing the correct tool, producing valid arguments and recovering from tool errors
* **Result validation:** checking outputs against constraints, schemas or expected state
* **Repository work:** routine shell commands, test execution, formatting and structured summaries
* **Subagent delegation:** selecting a specialist, writing a focused task and integrating the result
* **Long-running agent traces:** observation → reasoning → action → validation → recovery examples
* **Domain workflows:** repetitive, organization-specific tasks where latency and consistency matter

Do not size fine-tuning hardware as if this were a dense 3B model. Although only 3B parameters are active for each token, the model contains 30B total parameters. Context length, optimizer choice, batch size and sequence length will also affect memory use.

For notebooks and training instructions, start from the existing Nemotron fine-tuning flow. Start with shorter contexts and smaller batch sizes, then scale up.

#### Benchmarks

Nemotron 3.5 Lightning sits on the accuracy-speed Pareto frontier for small open models:

* Up to **4x faster output** than similar-sized models
* **86% accuracy** on PinchBench
* Completes **10,000 PinchBench tasks 35% faster** than Qwen 3.6 35B at similar accuracy

The Artificial Analysis Intelligence Index combines evaluations across agentic tasks, coding, scientific reasoning and general intelligence. NVIDIA also measures time to complete useful agent work, not only raw tokens per second.

Nemotron 3.5 Lightning is designed to sit below frontier reasoning models in a routed agent system: difficult planning routes to a larger model, while high-volume execution routes to Lightning. NVIDIA plans to release the weights, training data and recipes under OpenMDW-1.1, and [NeMo Switchyard](https://developer.nvidia.com/topics/ai/nemotron) can route each request to the most appropriate model.

For NVIDIA's full launch details, see the [Nemotron 3.5 Lightning announcement](https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/).


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/nemotron-3.5.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
