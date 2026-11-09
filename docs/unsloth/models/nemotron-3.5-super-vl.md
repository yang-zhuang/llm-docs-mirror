> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/nemotron-3.5-super-vl.md).

# NVIDIA Nemotron 3.5 Super VL: Run Locally Guide

Run Nemotron 3.5 Super VL locally with Unsloth GGUFs.

NVIDIA Nemotron-3.5-Super-VL-120B-A12B is a **120B parameter, 12B active** hybrid reasoning MoE model with **up to 1M tokens of context**. It accepts text, images and video for document understanding, computer use and agent workflows, and generates text.

It supports JSON output and tool calling, and includes a built-in Multi-Token Prediction (MTP) head. Unsloth GGUFs range from **46.1GB (1-bit) to 132GB (8-bit)**. We also made NVFP4 quants (79GB) and added the LiLiCorr DSpark module. **Unsloth quants:** [NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-GGUF](https://huggingface.co/unsloth/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-GGUF)

<a href="/docs/models/nemotron-3.5-super-vl.md#run-nemotron-35-super-vl-guide" class="button primary">Nemotron-3.5-Super-VL Guide</a><a href="/docs/models/nemotron-3.5-bolt.md" class="button secondary">Run Nemotron-3.5-Bolt Guide</a>

### ⚙️ Usage Guide

**Nemotron 3.5 Super VL Requirements**

The smallest **1-bit GGUF is 46.1GB**; plan for at least **64GB of RAM or unified memory**. The **4-bit GGUF is 86.9GB**, with around **128GB** recommended. You can also split the model across system RAM and GPU VRAM. You can also run the NVFP4 which is a direct lossless conversion from NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-NVFP4.

| Quantization         | GGUF size | Est. minimum memory |
| -------------------- | --------- | ------------------- |
| UD-IQ1\_M (1-bit)    | 46.1GB    | 64GB                |
| UD-IQ2\_XXS (2-bit)  | 51.1GB    | 64GB                |
| UD-IQ2\_M (2-bit)    | 55.9GB    | 80GB                |
| UD-Q2\_K\_XL (2-bit) | 57.8GB    | 80GB                |
| UD-IQ3\_XXS (3-bit)  | 59.8GB    | 80GB                |
| UD-Q3\_K\_XL (3-bit) | 65.8GB    | 96GB                |
| NVFP4 (4-bit)        | 79GB      | 96GB                |
| UD-Q4\_K\_XL (4-bit) | 86.9GB    | 128GB               |
| UD-Q5\_K\_XL (5-bit) | 111GB     | 160GB               |
| UD-Q6\_K\_XL (6-bit) | 121GB     | 160GB               |
| Q8\_0 (8-bit)        | 132GB     | 192GB               |

Memory figures are **planning estimates** for a modest context, including headroom for the operating system, runtime, KV cache and vision projector. GGUF file size alone is not the RAM requirement. Longer contexts and video need more memory; all model weights must be stored even though only 12B parameters are active per token. Count unified memory once.

A **128GB unified-memory system**, such as DGX Spark, fits the suggested 4-bit memory budget. NVIDIA documents DGX Spark support through NIM; these GGUF memory estimates are not measured performance results.

### Recommended Settings

NVIDIA recommends these settings:

| Parameter     | Value  |
| ------------- | ------ |
| `temperature` | `1.0`  |
| `top_p`       | `0.95` |

Start with **16K context** and increase it as memory allows. The model supports up to **1M tokens**, but your runtime or NIM profile may have a lower limit. Prompt and output tokens share this budget. The examples serve one request at a time.

**Thinking on or off**

The model supports `enable_thinking=True` (default) for reasoning and `enable_thinking=False` for direct answers. NVIDIA NIM accepts this through chat-template kwargs. For local GGUFs, use the model’s chat template and your runtime’s supported thinking controls.

{% hint style="info" %}
Nemotron 3.5 Super VL ships with **MTP (Multi-Token Prediction)**, which is enabled by default in Unsloth for faster output. You can turn it off in the settings. See our [MTP guide](https://unsloth.ai/docs/models/mtp).
{% endhint %}

### Run Nemotron 3.5 Super VL Guide <a href="#run-nemotron-35-super-vl-guide" id="run-nemotron-35-super-vl-guide"></a>

For this tutorial, we will use **UD-Q4\_K\_XL (86.9GB)** with around **128GB of memory**. Choose a smaller quant from the table above if you have less memory.

#### 🦥 Run Nemotron 3.5 Super VL in Unsloth Desktop <a href="#run-nemotron-35-super-vl-in-unsloth-desktop" id="run-nemotron-35-super-vl-in-unsloth-desktop"></a>

Run Nemotron 3.5 Super VL directly in [Unsloth Desktop](https://unsloth.ai/docs/desktop) on **macOS, Windows and Linux**. Search, download and chat with the model in the app.

{% stepper %}
{% step %}

#### **Setup Unsloth**

The easiest way to get started is by downloading the [Unsloth Desktop app](/docs/desktop.md).

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

You can also install manually:

{% tabs %}
{% tab title="Native install" %}
**MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

{% endtab %}

{% tab title="Docker" %}
The [Unsloth Docker image](https://hub.docker.com/r/unsloth/unsloth) `unsloth/unsloth` is available on Docker. [Read guide.](https://unsloth.ai/docs/get-started/install/docker)
{% endtab %}

{% tab title="Homebrew" %}
Install Unsloth Desktop:

{% code collapsedlinecount="10" %}

```bash
brew install --cask unsloth
```

{% endcode %}

Update Unsloth Desktop:

```bash
brew upgrade --cask unsloth
```

{% endtab %}

{% tab title="WinGet" %}
Install Unsloth Desktop:

```powershell
winget install --id UnslothAI.Unsloth -e
```

Update Unsloth Desktop:

```powershell
winget upgrade --id UnslothAI.Unsloth -e
```

{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}

#### Setup and Run Nemotron 3.5 Super VL

Go to [Unsloth Chat](/docs/new/studio/chat.md) or Model hub and search for Nemotron 3.5 Super VL in the search bar and download your desired model and quant. Now you're ready to run the model!

Inference parameters should be auto-set when using Unsloth, however you can still change it manually. You can also edit the context length, chat template and other settings.

To try image understanding, attach a PNG or JPEG and ask **“What is this image?”**

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FrTV33NAoY62hmlGHaEyw%2Fnemotron-super-vl-unsloth-desktop.png?alt=media&amp;token=e38fc0f5-bae6-442f-8c6f-4e9c54d326aa" alt="" width="563"><figcaption></figcaption></figure>

For more information, you can view our [Unsloth inference guide](/docs/new/studio/chat.md).
{% endstep %}

{% step %}

#### Serve Nemotron 3.5 Super VL with Unsloth API

Serve Nemotron 3.5 Super VL with `unsloth run`. You can pass llama-server flags for context size, GPU layers and other settings. See our [API docs](https://unsloth.ai/docs/basics/api) or [unsloth start](https://unsloth.ai/docs/integrations/unsloth-start).

{% code overflow="wrap" %}

```bash
unsloth run --model unsloth/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-GGUF:UD-IQ2_XXS \
    --ctx-size 4096 --parallel 1 --alias nemotron-super-vl \
    --host 127.0.0.1 --port 8001
```

{% endcode %}
{% endstep %}

{% step %}

#### Unsloth is now ready

You can also do many other things with Nemotron 3.5 Super VL via Unsloth Desktop like:

* **Connect tools:** [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md), [web search](/docs/new/studio/chat.md#advanced-web-search), [MCP](/docs/basics/mcp.md) and more
* **Train models:** Fine-tune text, diffusion, [embedding](/docs/basics/embedding-finetuning.md), and more
* **Generate media:** Create and train [images](/docs/basics/diffusion-image.md), video, [TTS](/docs/basics/text-to-speech-tts-fine-tuning.md) locally
  {% endstep %}
  {% endstepper %}

### KLD Benchmarks

We used UD-3 to convert Nemotron Super and did general KLD and also an unseen text KLD dataset to gauge for overfitting - generally UD-Q4\_K\_XL is the best in terms of KLD vs disk space - NVFP4 is also generally ok, and UD-Q3\_K\_XL is a also reasonable.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FI0Lb9lHn00vouMw6Lj8n%2Fnemotron35_super_vl_kld_vs_disk(2).png?alt=media&amp;token=7aea3a84-5740-45e3-b542-2982133cafdb" alt=""><figcaption></figcaption></figure>

#### 🦙 Run Nemotron 3.5 Super VL in llama.cpp <a href="#run-nemotron-35-super-vl-in-llama.cpp" id="run-nemotron-35-super-vl-in-llama.cpp"></a>

{% stepper %}
{% step %}
**Build llama.cpp**

Install the latest version of llama.cpp. You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

Video needs both `ffmpeg` and `ffprobe` on your PATH. Continue the commands below from this `llama.cpp` directory.
{% endstep %}

{% step %}
**Download the Unsloth GGUF**

Download the model and its vision projector:

{% code overflow="wrap" %}

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U huggingface_hub

hf download unsloth/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-GGUF \
    --local-dir models/nemotron-super-vl \
    --include "*UD-Q4_K_XL*.gguf" "*mmproj*.gguf"
```

{% endcode %}

Set the paths to the downloaded model and its matching projector. For a split GGUF, keep every shard together and point to the **first shard**. Adjust the filenames below to match your download.

```bash
MODEL_FILE="models/nemotron-super-vl/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-UD-Q4_K_XL.gguf"
MMPROJ_FILE="models/nemotron-super-vl/mmproj-BF16.gguf"
```

{% endstep %}

{% step %}
**Run text and images**

For text:

```bash
./llama.cpp/llama-cli \
    --model "$MODEL_FILE" --ctx-size 16384 --temp 1.0 --top-p 0.95 --top-k 0 --min-p 0.0 \
    --prompt "Explain what a vision-language model does."
```

For an image, set the path to your own RGB PNG or JPEG. For PDFs, render pages to images first:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-mtmd-cli \
    --model "$MODEL_FILE" --mmproj "$MMPROJ_FILE" \
    --ctx-size 16384 --temp 1.0 --top-p 0.95 --top-k 0 --min-p 0.0 \
    --image /path/to/picture.jpg \
    --prompt "Describe this image and extract any visible text."
```

{% endcode %}
{% endstep %}

{% step %}
**Run video**

Start the multimodal CLI:

```bash
./llama.cpp/llama-mtmd-cli \
    --model "$MODEL_FILE" --mmproj "$MMPROJ_FILE" \
    --ctx-size 16384 --temp 1.0 --top-p 0.95 --top-k 0 --min-p 0.0
```

Then enter these lines **inside the CLI**:

```
/video /path/to/video.mp4
Summarize the video and describe the key events.
```

The model card recommends **MP4 clips of 1–2 minutes**. NIM samples at 2 FPS, up to 256 frames; local sampling depends on the runtime. Start with a short clip and increase context as needed, since video frames consume prompt tokens.
{% endstep %}
{% endstepper %}

#### Llama-server serving and deployment <a href="#llama-server-serving-and-deployment" id="llama-server-serving-and-deployment"></a>

{% stepper %}
{% step %}
**Start llama-server**

Create a media directory and start the server:

{% code overflow="wrap" %}

```bash
mkdir -p media
./llama.cpp/llama-server \
    --model "$MODEL_FILE" --mmproj "$MMPROJ_FILE" \
    --alias nemotron-super-vl \
    --ctx-size 16384 --parallel 1 --temp 1.0 --top-p 0.95 --top-k 0 --min-p 0.0 \
    --media-path "$PWD/media" \
    --host 127.0.0.1 --port 8001
```

{% endcode %}

Open **<http://127.0.0.1:8001>** on the same machine to chat with the llama.cpp server.
{% endstep %}

{% step %}
**Send an API request**

For video, copy a short clip to `media/clip.mp4`, then run this command in another terminal:

{% code overflow="wrap" %}

```bash
curl http://127.0.0.1:8001/v1/chat/completions \
    -H 'Content-Type: application/json' \
    -d '{
      "model": "nemotron-super-vl",
      "messages": [{"role": "user", "content": [
        {"type": "text", "text": "Summarize this video."},
        {"type": "input_video", "input_video": {"url": "file://clip.mp4"}}
      ]}],
      "max_tokens": 1024
    }'
```

{% endcode %}

`--media-path` allows the server to read local media from that directory. For text-only requests, use `"content": "What is 2+2?"` instead of the content array.
{% endstep %}
{% endstepper %}

#### 📊 Benchmarks

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FBjoqDdZWELPnsSztDMlZ%2Faccuracy_plot(1).png?alt=media&amp;token=e4994520-d7a8-4d06-b183-fd6182c878d3" alt=""><figcaption></figcaption></figure>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/nemotron-3.5-super-vl.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
