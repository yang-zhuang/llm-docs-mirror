> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/kimi-k2.6.md).

# Kimi K2.6 - How to Run Locally

Step-by-step guide to running Kimi-K2.6 on your own local device.

Kimi K2.6 is an open model by Moonshot that delivers SOTA performance across vision, coding, agentic, long context and chat tasks. The 1T-parameter hybrid thinking model has 256K context length and full precision requires 610GB of disk space Dynamic 2-bit requires **350GB (-43% size)**. Run Kimi K2.6 via Unsloth Dynamic [**Kimi-K2.6-GGUFs**](https://huggingface.co/unsloth/Kimi-K2.6-GGUF) on Unsloth Studio or llama.cpp.

**Dynamic 2-bit** upcasts important layers to 8-bit and needs **350GB+ VRAM/RAM** setup&#x73;**.** For **lossless** Kimi K2.6, use Q8 (`UD-Q8_K_XL`), which is only **10GB larger** than Q4 (`UD-Q4_K_XL`). All uploads use [Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) for SOTA quantization performance. Kimi-K2.6 GGUFs also **support vision.**

**Table: Hardware requirements** (units = total memory: RAM + VRAM, or unified memory)

| Measurement | Dynamic 2-bit | Q4     | Q8 (Lossless) |
| ----------- | ------------- | ------ | ------------- |
| Disk Space  | 340 GB        | 584 GB | 595 GB        |
| Perplexity  | 2.4131        | 1.8420 | 1.8419        |

### 📊 Quantization Analysis

`UD-Q8_K_XL` is lossless because Kimi uses int4 for MoE weights and BF16 for everything else, and `Q8_K_XL` follows that. `UD-Q4_K_XL` is similar except the remaining tensors are `Q8_0`, so it is near full precision and requires 600GB RAM/VRAM. Other non-Unsloth GGUFs from other providers may follow the `UD-Q4_K_XL` approach rather than the 'truly lossless' `UD-Q8_K_XL`.

We followed [jukofyork](https://github.com/jukofyork)'s finding that `const float d = max / -7;` instead of the default `const float d = max / -8;` during the quantization process only on the MoE layers. This bijection patch on INT4-native MoEs allows the `Q4_0` quant-type to reduce absolute error from 1.8% to near 0% (epsilon).

However we must keep other layers in BF16, and show below the error plots for both versus the BF16 baseline. `UD-Q8-K_XL` is truly "lossless" with some machine epsilon difference when converting Q4\_0 to BF16. The perplexity for `UD-Q8_K_XL` was 1.8419 ± 0.00721 and `UD-Q4_K_XL` 1.8420 ± 0.00720. Note the error plot below is RMSE divided by bfloat16 epsilon, so it's a small error scale.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F9aDDLGTfcKyREQKFCkfv%2Ftensor_rmse_over_eps_both_present_percent_thick_legend.png?alt=media&amp;token=2f39c305-5b12-454e-8917-5af54fe9890a" alt=""><figcaption><p>See difference between <code>Q4_K_XL</code> (blue) and <code>Q8_K_XL</code> (orange) which is lossless and 10GB larger.</p></figcaption></figure></div>

### :gear: Usage Guide

**Thinking and non-thinking mode require different settings:**

| Default (Thinking Mode) | Instant Mode      |
| ----------------------- | ----------------- |
| temperature = 1.0       | temperature = 0.6 |
| top\_p = 0.95           | top\_p = 0.95     |

* Suggested context length = `98,304` (up to `262,144`)

If the model fits, you will get >40 tokens/s when using B200s. We recommend `UD-Q2_K_XL` (350GB) as a good size/quality balance. Best rule of thumb: RAM+VRAM ≈ the quant size; otherwise it’ll still work, just slower due to offloading.

#### Chat Template for Kimi K2.6

Running `tokenizer.apply_chat_template([{"role": "user", "content": "What is 1+1?"},])` gets:

{% code overflow="wrap" %}

```
<|im_system|>system<|im_middle|>You are Kimi, an AI assistant created by Moonshot AI.<|im_end|><|im_user|>user<|im_middle|>What is 1+1?<|im_end|><|im_assistant|>assistant<|im_middle|><think>
```

{% endcode %}

## Run Kimi K2.6 Guide

### 🦥 Run Kimi-K2.6 in Unsloth Studio

Kimi K2.6 can run in [Unsloth Studio](/docs/new/studio.md), an open-source web UI for local AI. **Unsloth Studio automatically offloads to RAM and detects multiGPU setups**. With Unsloth Studio, you can run models locally on **MacOS, Windows**, Linux and:

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

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFeQ0UUlnjXkDdqhcWglh%2Fskinny%20studio%20chat.png?alt=media&amp;token=c2ee045f-c243-4024-a8e4-bb4dbe7bae79" alt=""><figcaption></figcaption></figure></div>
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

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

Then open `http://localhost:8888` in your browser.
{% endstep %}

{% step %}
**Search and download Kimi-K2.6**

Unsloth Studio automatically offloads to RAM and detects multiGPU setups. On first launch you will need to create a password to secure your account and sign in again later.

Then go to the [Unsloth Chat](/docs/new/studio/chat.md) tab and search for **Kimi-K2.6** in the search bar and download your desired model and quant. Ensure you have enough compute the run the model.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FK6m0UwUjRocivKbidBCl%2Fkimi%20screenshot%2026.png?alt=media&amp;token=403731cc-ab1c-44b0-9fca-cd0745149193" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}
**Run Kimi-K2.6**

Inference parameters should be auto-set when using Unsloth Studio, however you can still change it manually. You can also edit the context length, chat template and other settings.

For more information, you can view our [Unsloth Studio inference guide](/docs/new/studio/chat.md).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FTbH2CrUTG2TWwgOP74GF%2FGemma%204%20example.gif?alt=media&amp;token=56409d06-3735-4531-97c0-af9968371a26" alt="" width="563"><figcaption><p>Example of Qwen3.6 running with tool-calling</p></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### 🦙 Run Kimi K2.6 in llama.cpp

For this guide we'll be running the UD-Q2\_K\_XL quant which will require at least 350GB RAM. Feel free to change quantization type. GGUF: [**Kimi-K2.6-GGUF**](https://huggingface.co/unsloth/Kimi-K2.6-GGUF)

For these tutorials, we will using [llama.cpp](llama.cpphttps://github.com/ggml-org/llama.cpp) for fast local inference, especially if you have a CPU.

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
You can now use `llama.cpp` directly to load and download models, just like `ollama run`. First, select the quantization type you want like `Q2_K_XL`. Also use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location. Note this download process might be very slow, so it's probably best to use the manual download process in the next section.

Use one of the specific commands below, according to your use-case:

**Thinking mode:**

```bash
export LLAMA_CACHE="unsloth/Kimi-K2.6-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/Kimi-K2.6-GGUF:UD-Q2_K_XL \
    --temp 1.0 \
    --top-p 0.95
```

**Non-thinking mode (Instant):**

```bash
export LLAMA_CACHE="unsloth/Kimi-K2.6-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/Kimi-K2.6-GGUF:UD-Q2_K_XL \
    --temp 0.6 \
    --top-p 0.95 \
    --chat-template-kwargs '{"enable_thinking":false}'
```

{% endstep %}

{% step %}
If you want to download the model manually, we can download the model via the code below (after installing `pip install huggingface_hub`). If downloads get stuck, see: [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

```bash
hf download unsloth/Kimi-K2.6-GGUF \
    --local-dir unsloth/Kimi-K2.6-GGUF \
    --include "*mmproj-F16*" \
    --include "*UD-Q2_K_XL*" # Use "*UD-Q8_K_XL*" for full precision
```

{% endstep %}

{% step %}
Then run the model in conversation mode:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/Kimi-K2.6-GGUF/UD-Q2_K_XL/Kimi-K2.6-UD-Q2_K_XL-00001-of-0008.gguf \
    --mmproj unsloth/Kimi-K2.6-GGUF/mmproj-F16.gguf \
    --temp 1.0 \
    --top-p 0.95
```

{% endcode %}
{% endstep %}
{% endstepper %}

### 📊 Benchmarks

You can view further below for benchmarks in table format:

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FdBDLDaRXybr9JMCs33bC%2Fkimibench.jpg?alt=media&amp;token=040ea87d-09e8-452c-bfb2-4231305a20d2" alt="" width="563"><figcaption></figcaption></figure></div>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/kimi-k2.6.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
