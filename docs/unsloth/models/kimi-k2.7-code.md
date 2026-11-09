> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/kimi-k2.7-code.md).

# Kimi K2.7 Code - How to Run Locally

Step-by-step guide to running Kimi K2.7 Code on your own local device.

Kimi K2.7 Code is Moonshot AI’s agentic coding model, building on [K2.6](/docs/models/kimi-k2.6.md) to improve task completion while using \~30% fewer thinking tokens. The 1T-parameter (32B active) MoE model supports thinking only, vision and 256K context. It delivers SOTA open performance across vision, coding, agentic, long-context, and chat tasks. Full precision requires 605GB of disk space; Unsloth [Dynamic](/docs/basics/dynamic-3.0-ggufs.md) 2-bit requires **325GB (-48%)**. Run [**Kimi-K2.7-Code-GGUF**](https://huggingface.co/unsloth/Kimi-K2.7-Code-GGUF) via Unsloth Studio or llama.cpp.

[**Unsloth Dynamic**](/docs/basics/dynamic-3.0-ggufs.md) **quants** upcasts important layers to 8-bit and 1-bit needs **310GB+ VRAM/RAM** setup&#x73;**.** For **lossless** Kimi K2.7, use Q8 (`UD-Q8_K_XL`), which is only **10GB larger** than Q4 (`UD-Q4_K_XL`). You can run Kimi K2.7 Code via a Mac Studio or [DGX Station](/docs/blog/dgx-station.md).

**Table: Hardware requirements** (units = total memory: RAM + VRAM, or unified memory)

| Dynamic 1-bit | Dynamic 2-bit | Dynamic Q3 | Q8 (Lossless) |
| ------------- | ------------- | ---------- | ------------- |
| 310 GB        | 325-350GB     | 385-470 GB | 605 GB        |

### 📊 Quantization Analysis

Like [Kimi-K2.6](/docs/models/kimi-k2.6.md), `UD-Q8_K_XL` is lossless because Kimi uses int4 for MoE weights and BF16 for everything else, and `Q8_K_XL` follows that. Thus, we use the same Dynamic methodology for Kimi-K2.6 conversion. `UD-Q4_K_XL` is similar except the remaining tensors are `Q8_0`, so it is near full precision and requires 600GB RAM/VRAM. `UD-Q8_K_XL` is 'truly lossless'.

| Measurement | UD-Q2\_K\_XL | UD-Q4\_K\_XL | UD-Q8\_K\_XL (Lossless) |
| ----------- | ------------ | ------------ | ----------------------- |
| Disk Space  | 339 GB       | 584 GB       | 595 GB                  |
| Perplexity  | \~2.4131     | \~1.8420     | \~1.8419                |

We followed [jukofyork](https://github.com/jukofyork)'s finding that `const float d = max / -7;` instead of the default `const float d = max / -8;` during the quantization process only on the MoE layers. This bijection patch on INT4-native MoEs allows the `Q4_0` quant-type to reduce absolute error from 1.8% to near 0% (epsilon). For example below is the histogram for Kimi-K2.7-Code, and you can see -8 is unused entirely:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FWsSY72AMu8NAmTZ1JcUQ%2Fimage.png?alt=media&amp;token=5b31677e-0c7a-4a34-94a7-7a873f096d19" alt=""><figcaption></figcaption></figure>

Note we must keep other layers in BF16 as well and not smart "Q4\_0". We show below the error plots for both versus the BF16 baseline. `UD-Q8-K_XL` is truly "lossless" with some machine epsilon difference when converting Q4\_0 to BF16. So Q4\_K\_XL does have some quantization error due to Q8\_0 being used, whilst Q8\_K\_XL is nearly lossless, except for BF16 rounding.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FswvcMMP78FBFZbqgRoB9%2Fimage.png?alt=media&amp;token=0be9b199-eb93-4f03-8843-075e012967fe" alt=""><figcaption></figcaption></figure>

For Q4\_K\_XL, we also plot the per tensor error from Q8\_0 vs BF16 as well. In general there is some error between Q8\_K\_XL (near lossless) vs Q4\_K\_XL, but not much.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FlrzkcdP1zDT53Mok23g6%2Fimage.png?alt=media&amp;token=542ea4cd-8e7e-4e29-b4f0-151d9ed9fdca" alt=""><figcaption></figcaption></figure>

### :gear: Usage Guide

Kimi K2.7 Code is **thinking-only**, with **`preserve_thinking` always enabled**. Instant mode is not supported.

| Default (Thinking Mode) |
| ----------------------- |
| temperature = 1.0       |
| top\_p = 0.95           |

* Suggested context length = `98,304` (up to `262,144`)

If the model fits, you will get >100 tokens/s when using B200s. We recommend `UD-Q2_K_XL` (345GB) as a good size/quality balance. Best rule of thumb: RAM+VRAM ≈ the quant size; otherwise it’ll still work, just slower due to offloading.

#### Chat Template for Kimi K2.7-Code

Running `tokenizer.apply_chat_template([{"role": "user", "content": "What is 1+1?"},])` gets:

{% code overflow="wrap" %}

```
<|im_user|>user<|im_middle|>What is 1+1?<|im_end|><|im_assistant|>assistant<|im_middle|><think>
```

{% endcode %}

If we also input tools as referenced in [Tool Calling Guide](/docs/basics/tool-calling-guide-for-local-llms.md), then we see the below:

{% code overflow="wrap" expandable="true" %}

```
<|im_system|>tool_declare<|im_middle|># Tools

## functions
namespace functions {
// Add two numbers.
type add_number = (_: {
  // The first number.
  a: string,
  // The second number.
  b: string
}) => any;
// Multiply two numbers.
type multiply_number = (_: {
  // The first number.
  a: string,
  // The second number.
  b: string
}) => any;
// Subtract two numbers.
type subtract_number = (_: {
  // The first number.
  a: string,
  // The second number.
  b: string
}) => any;
// Writes a random story.
type write_a_story = (_: {}) => any;
// Perform operations from the terminal.
type terminal = (_: {
  // The command you wish to launch, e.g `ls`, `rm`, ...
  command: string
}) => any;
// Call a Python interpreter with some Python code that will be ran.
type python = (_: {
  // The Python code to run
  code: string
}) => any;
}
<|im_end|><|im_user|>user<|im_middle|>What is 1+1?<|im_end|><|im_assistant|>assistant<|im_middle|><think>
```

{% endcode %}

## Run Kimi K2.7 Code Guide

### 🦥 Run Kimi-K2.7-Code in Unsloth Studio

Kimi K2.7 Code can run in [Unsloth Studio](/docs/new/studio.md), an open-source web UI for local AI. **Unsloth Studio automatically offloads to RAM and detects multiGPU setups**. With Unsloth Studio, you can run models locally on **MacOS, Windows**, Linux and:

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

Then open `http://127.0.0.1:8888` (or your specific URL) in your browser.
{% endstep %}

{% step %}
**Search and download Kimi K2.7-Code**

Unsloth Studio automatically offloads to RAM and detects multiGPU setups. On first launch you will need to create a password to secure your account and sign in again later.

Then go to the [Unsloth Chat](/docs/new/studio/chat.md) tab and search for **Kimi-K2.7 Code** in the search bar and download your desired model and quant. Ensure you have enough compute the run the model.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FV4uC7CyCwbiNpCfU7Cdx%2FScreenshot%202026-06-14%20at%2010.36.24%E2%80%AFPM.png?alt=media&amp;token=c6eb8013-dffd-49fb-8a46-cf82574e5793" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}
**Run Kimi-K2.7-Code**

Inference parameters should be auto-set when using Unsloth Studio, however you can still change it manually. You can also edit the context length, chat template and other settings.

For more information, you can view our [Unsloth Studio inference guide](/docs/new/studio/chat.md).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FTbH2CrUTG2TWwgOP74GF%2FGemma%204%20example.gif?alt=media&amp;token=56409d06-3735-4531-97c0-af9968371a26" alt="" width="563"><figcaption><p>Example of Qwen3.6 running with tool-calling</p></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### 🦙 Run Kimi K2.7 Code in llama.cpp

For this guide we'll be running the `UD-Q2_K_XL` quant which will require at least 345GB RAM. Feel free to change quantization type. GGUF: [**Kimi-K2.7-Code-GGUF**](https://huggingface.co/unsloth/Kimi-K2.7-Code-GGUF)

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
**Let's first get an image!** You can also upload images as well. We shall use <https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/unsloth%20made%20with%20love.png>, which is just our mini logo showing how finetunes are made with Unsloth:

{% code overflow="wrap" %}

```bash
wget https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/unsloth%20made%20with%20love.png -O unsloth.png
```

{% endcode %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-9bf7ec93680f889d7602e5f56a8d677d6a58ae6a%2Funsloth%20made%20with%20love.png?alt=media" alt="" width="188"><figcaption></figcaption></figure>

Let's get the 2nd image at <https://files.worldwildlife.org/wwfcmsprod/images/Sloth_Sitting_iStock_3_12_2014/story_full_width/8l7pbjmj29_iStock_000011145477Large_mini__1_.jpg>

{% code overflow="wrap" %}

```bash
wget https://files.worldwildlife.org/wwfcmsprod/images/Sloth_Sitting_iStock_3_12_2014/story_full_width/8l7pbjmj29_iStock_000011145477Large_mini__1_.jpg -O picture.png
```

{% endcode %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-4b30cc86b2c75edf95ee1ec6fe0c51fb30afd6c0%2F8l7pbjmj29_iStock_000011145477Large_mini__1_.jpg?alt=media" alt="" width="188"><figcaption></figcaption></figure>
{% endstep %}

{% step %}
You can now use `llama.cpp` directly to load and download models, just like `ollama run`. First, select the quantization type you want like `Q2_K_XL`. Also use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location. Note this download process might be very slow, so it's probably best to use the manual download process in the next section.

```bash
export LLAMA_CACHE="unsloth/Kimi-K2.7-Code-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/Kimi-K2.7-Code-GGUF:UD-Q2_K_XL \
    --temp 1.0 \
    --top-p 0.95
```

{% endstep %}

{% step %}
If you want to download the model manually, we can download the model via the code below (after installing `pip install huggingface_hub`). If downloads get stuck, see: [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

```bash
hf download unsloth/Kimi-K2.7-Code-GGUF \
    --local-dir unsloth/Kimi-K2.7-Code-GGUF \
    --include "*mmproj-F16*" \
    --include "*UD-Q2_K_XL*" # Use "*UD-Q8_K_XL*" for full precision
```

{% endstep %}

{% step %}
Then run the model in conversation mode:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/Kimi-K2.7-Code-GGUF/UD-Q2_K_XL/Kimi-K2.7-Code-UD-Q2_K_XL-00001-of-00008.gguf \
    --mmproj unsloth/Kimi-K2.7-Code-GGUF/mmproj-F16.gguf \
    --temp 1.0 \
    --top-p 0.95
```

{% endcode %}

Then you will see the below:\
![](https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F8EGq6pk1Cuz0er9k4n3p%2Fimage.png?alt=media\&token=4a71100c-f354-4ced-9e43-a0ed05916ce2)
{% endstep %}

{% step %}
Then use `/image` to load both images in and ask "What is this image":

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FdDbduh9D9DOOCOGO9TOH%2Fimage.png?alt=media&amp;token=62cf84a3-067c-47e5-9521-3992129201b6" alt=""><figcaption></figcaption></figure>

and you will get something like below:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fdd2fiwNxHQPPaSGnX1ox%2Fimage.png?alt=media&amp;token=17e35bd9-a957-4216-80a5-0e92e994b07a" alt=""><figcaption></figcaption></figure>

On the 2nd image of the sloth:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FqVOX047Ff0AUPgjg6gq6%2Fimage.png?alt=media&amp;token=b43e9af8-6fab-49b2-961a-9b0f14a05575" alt=""><figcaption></figcaption></figure>

Which will get you:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F67rxQcN9zVxWMt2ScEM5%2Fimage.png?alt=media&amp;token=8b6ef9a4-6532-49b8-a25f-afdf66d85fe0" alt=""><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### 📊 Benchmarks

You can view further below for benchmarks in table format:

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fg3tjodYLZGnqcXqHDico%2Fkimiii.jpg?alt=media&amp;token=be63bc15-fe63-4f59-af85-5ec6acfcb2c0" alt="" width="563"><figcaption></figcaption></figure></div>

|       Benchmark      | Kimi K2.7 Code | Kimi K2.6 | GPT-5.5 | Claude Opus 4.8 |
| :------------------: | :------------: | :-------: | :-----: | :-------------: |
|      **Coding**      |                |           |         |                 |
|  Kimi Code Bench v2  |      62.0      |    50.9   |   69.0  |       67.4      |
|     Program Bench    |      53.6      |    48.3   |   69.1  |       63.8      |
|    MLS Bench Lite    |      35.1      |    26.7   |   35.5  |       42.8      |
|      **Agentic**     |                |           |         |                 |
| Kimi Claw 24/7 Bench |      46.9      |    42.9   |   52.8  |       50.4      |
|       MCP Atlas      |      76.0      |    69.4   |   79.4  |       81.3      |
|   MCP Mark Verified  |      81.1      |    72.8   |   92.9  |       76.4      |


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/kimi-k2.7-code.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
