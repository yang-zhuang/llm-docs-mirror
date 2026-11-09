> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/nemotron-3.5-bolt.md).

# NVIDIA Nemotron 3.5 Bolt: Run Locally Guide

Run Nemotron 3.5 Bolt locally with Unsloth GGUFs.

NVIDIA Nemotron-3.5-Bolt-**E4B** and Nemotron-3.5-Bolt-**74B-A9B** are new open models by NVIDIA. Bolt-74B-A9B is a **74B parameter**, 9B active hybrid reasoning MoE model compressed from Super VL. It supports **text, images and video**, tool calling and a **128K context** window. Run the model locally via [Unsloth Desktop](/docs/desktop.md) or llama.cpp.

Bolt-E4B-4GB is an **8B parameter** (4B effective), model based on [Gemma 4](/docs/models/gemma-4.md) E4B. It supports a **64K context window**, multi-turn tool calling and configurable reasoning. Downloads: [74B-A9B Unsloth GGUFs](https://huggingface.co/unsloth/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-GGUF) · [E4B NVIDIA GGUF](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB).

<a href="/docs/models/nemotron-3.5-bolt.md#run-nemotron-35-bolt-guide" class="button primary">Run Nemotron-3.5-Bolt Guide</a><a href="/docs/models/nemotron-3.5-super-vl.md" class="button secondary">Nemotron-3.5-Super-VL Guide</a>

### ⚙️ Usage Guide

**Nemotron 3.5 Bolt Requirements**

For **74B-A9B** short-context use, budget around **32GB RAM or unified memory**; **48–64GB** gives more headroom. **E4B** runs on roughly **4GB VRAM** or **6GB RAM.**

| Model / quantization           | Download size | Memory guidance         |
| ------------------------------ | ------------- | ----------------------- |
| **E4B** · Q4\_K\_M (4-bit)     | 6.18GB        | \~4GB VRAM + system RAM |
| **74B-A9B** · IQ2\_XXS (2-bit) | 22GB          | 24–32GB RAM             |

* Memory use varies with context and runtime. E4B’s \~4GB figure is VRAM, not total system RAM or download size. The 74B-A9B model needs extra memory for images/video and the vision projector. Download sizes are for the GGUF weights.

{% hint style="info" %}
**74B-A9B** uses a **LiLiCorr** draft model in **NVFP4** (998MB) by default in Unsloth for faster output. It needs about 1–2GB more memory. E4B has a separate optional [DFlash drafter](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-E4B-4GB-DFlash).
{% endhint %}

#### Recommended Settings

Unsloth automatically configures inference settings. The 74B-A9B examples use default sampling settings. For E4B, NVIDIA recommends **temperature 1.0** and **top\_p 0.95** with reasoning enabled or disabled.

* **Context:** Up to **128K for 74B-A9B** or **64K for E4B**.

### Run Nemotron 3.5 Bolt Guide <a href="#run-nemotron-35-bolt-guide" id="run-nemotron-35-bolt-guide"></a>

We’ll use the **22GB 74B-A9B IQ2\_XXS** quant in this tutorial.

#### 🦥 Run Nemotron 3.5 Bolt in Unsloth Desktop <a href="#run-nemotron-35-bolt-in-unsloth-desktop" id="run-nemotron-35-bolt-in-unsloth-desktop"></a>

Run Nemotron 3.5 Bolt directly in [Unsloth Desktop](https://unsloth.ai/docs/desktop) on **macOS, Windows and Linux**. Search, download and chat with the model in the app.

{% stepper %}
{% step %}

#### **Install Unsloth**

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

#### **Setup and Run Nemotron 3.5 Bolt**

Go to [Unsloth Chat](/docs/new/studio/chat.md) or Model hub and search for **Nemotron 3.5 Bolt** in the search bar and download your desired model and quant. Now you're ready to run the model!

Inference parameters should be auto-set when using Unsloth, however you can still change it manually. You can also edit the context length, chat template and other settings.

To try image understanding, attach a PNG or JPEG and ask **“What is this image?”**

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FREZvGu7WyeaPxOjmrzPQ%2Fnemotron-bolt-unsloth-desktop.png?alt=media&amp;token=79d73c34-27fa-43b0-8362-99718df43478" alt="" width="375"><figcaption></figcaption></figure>

For more information, you can view our [Unsloth inference guide](/docs/new/studio/chat.md).
{% endstep %}

{% step %}
Serve Nemotron 3.5 Bolt with Unsloth API

Serve Nemotron 3.5 Bolt with `unsloth run`. You can pass llama-server flags for context size, GPU layers and other settings. Change model name accordingly. See our [API docs](https://unsloth.ai/docs/basics/api) or [unsloth start](https://unsloth.ai/docs/integrations/unsloth-start).

{% code overflow="wrap" %}

```bash
unsloth run --model unsloth/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-GGUF:IQ2_XXS \
    --ctx-size 4096 --parallel 1 --alias nemotron-bolt \
    --host 127.0.0.1 --port 8001
```

{% endcode %}
{% endstep %}

{% step %}

#### Unsloth is now ready

You can also do many other things with Nemotron 3.5 Bolt via Unsloth Desktop like:

* **Connect tools:** [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md), [web search](/docs/new/studio/chat.md#advanced-web-search), [MCP](/docs/basics/mcp.md) and more
* **Train models:** Fine-tune text, diffusion, [embedding](/docs/basics/embedding-finetuning.md), and more
* **Generate media:** Create and train [images](/docs/basics/diffusion-image.md), video, [TTS](/docs/basics/text-to-speech-tts-fine-tuning.md) locally
  {% endstep %}
  {% endstepper %}

#### 🦙 Run Nemotron 3.5 Bolt in llama.cpp <a href="#run-nemotron-35-bolt-in-llama.cpp" id="run-nemotron-35-bolt-in-llama.cpp"></a>

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

Download `IQ2_XXS` and the vision projector for image/video input. Change the quant name below to download another version:

{% code overflow="wrap" %}

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U huggingface_hub

hf download unsloth/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-GGUF \
    --local-dir models/nemotron-bolt \
    --include "*IQ2_XXS*.gguf" "*mmproj*.gguf"
```

{% endcode %}

Set the paths to the downloaded model and its matching projector. For a split GGUF, keep every shard together and point to the **first shard**. Adjust the filenames below to match your download.

```bash
MODEL_FILE="models/nemotron-bolt/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-IQ2_XXS.gguf"
MMPROJ_FILE="models/nemotron-bolt/mmproj-BF16.gguf"
```

{% endstep %}

{% step %}
**Run text and images**

For text:

```bash
./llama.cpp/llama-cli \
    --model "$MODEL_FILE" --ctx-size 4096 \
    --prompt "Explain what a vision-language model does."
```

For an image, set the path to your own PNG or JPEG:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-mtmd-cli \
    --model "$MODEL_FILE" --mmproj "$MMPROJ_FILE" \
    --ctx-size 4096 \
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
    --ctx-size 4096
```

Then enter these lines **inside the CLI**:

```
/video /path/to/video.mp4
Summarize the video and describe the key events.
```

Supports MP4 clips up to 2 minutes. Use up to 1 FPS / 128 frames at 1080p, or 2 FPS / 256 frames at 720p. Start with a short clip and increase context as needed.
{% endstep %}
{% endstepper %}

### Benchmarks

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FHf4Zgb51geMaxzCKvfaF%2Faccuracy.png?alt=media&amp;token=26ede764-8518-4867-8427-0e4171187747" alt=""><figcaption></figcaption></figure>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/nemotron-3.5-bolt.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
