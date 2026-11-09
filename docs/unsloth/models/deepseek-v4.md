> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/deepseek-v4.md).

# DeepSeek-V4: How to Run Locally

Run DeepSeek-V4-Pro-0813 and DeepSeek-V4-Flash-0731 locally on your own device!

DeepSeek-V4, DeepSeek-V4-Flash-Vision-Exp, V4-**Pro-0813**, and V4-**Flash-0731** are new open-weight models - the Flash variant has 284B parameters (13B active), while V4-Pro has 1.6T (49B active). **V4-Pro-0813**, released on **Aug 13**, matches Claude-4.8-Opus performance, while **V4-Flash-0731**, released on **July 31**, delivers the best performance in its size class and **outperforms V4-Pro** (Preview). Built for coding, agentic, and chat workflows with a **1M context window**, this guide shows how to run DeepSeek-V4-Flash-0731 locally using Unsloth Dynamic GGUFs and [Unsloth Desktop](/docs/desktop.md).

For **lossless** DeepSeek, use Q8 (`UD-Q8_K_XL`), which is only **7GB larger** than Q4 (`UD-Q4_K_XL`). The lossless 8-bit GGUF is **162 GB** and 3-bit is **103GB** which can run on a **110GB RAM** devic&#x65;**.** DeepSeek-V4-Flash-0731 scores 82.7% on Terminal Bench 2.1, 54.4% on DeepSWE, and 54.2% on NL2Repo. [DSpark](#dspark-speculative-decoding) is also enabled for GGUFs, enabling up to **2x faster decoding speed**!

{% hint style="success" %}
**Aug 31:** DeepSeek-Flash-Vision-Exp is now available!

**Aug 13:** DeepSeek-**V4-Pro-0813** was released and [quants are now](https://huggingface.co/unsloth/DeepSeek-V4-Pro-0813-GGUF) available to run.
{% endhint %}

{% hint style="success" %}
**Aug 6: DSpark is enabled for DeepSeek-V4-Flash-0731 - enabling 1.5x to 1.9x faster inference! DSpark is automatically enabled in** [**Unsloth**](#unsloth-studio-guide)**.**

We also improved the [DeepSeek-V4 chat jinja template](#deepseek-v4-chat-template-improvements), and tested over 4000 conversations to be equivalent with the official baseline.
{% endhint %}

| [DeepSeek-V4-Pro-0813-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Pro-0813-GGUF) | [DeepSeek-V4-Flash-**0731**-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF) | [DeepSeek-V4-Flash-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-GGUF) |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |

<a href="/docs/models/deepseek-v4.md#usage-guide" class="button primary">Usage Guide</a><a href="/docs/models/deepseek-v4.md#run-deepseek-v4-flash-tutorials" class="button primary">Running Tutorials</a>

### 📊 Quantization Analysis

Our `UD-Q8_K_XL` quant is fully lossless. DeepSeek-V4-Flash is [quantization-aware-trained](/docs/blog/quantization-aware-training-qat.md): the official checkpoint stores its routed experts (96% of the model) natively in MXFP4 and everything else in FP8 or BF16. GGUF's MXFP4 is exactly that format, so we repack the experts bit-for-bit, and FP8 dequantizes into BF16 with no rounding. We checked every tensor against the official DeepSeek weights: all 1,328 are bit-identical, and it stays lossless at inference (KL-divergence \~0, 100% top-token agreement).

**Non**-Unsloth DeepSeek-V4-Flash GGUFs were converted without these paths thus deviating from the official weights. `UD-Q4_K_XL` keeps the same bit-exact experts and only quantizes the non-expert tensors (4% of the model) to Q8\_0, so it sits right next to Q8 in size and quality.

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FXjXSVsiH2ZIKlJ7iZPDx%2Fkldddd.webp?alt=media&amp;token=e1db5fca-b2b4-411e-8956-29127ef6bfe0" alt="" width="563"><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FHoYuIu6dNNuLrM4nmdbi%2Fpareto.png?alt=media&amp;token=1c7a44bb-13c3-4fc4-8d57-fb350ffe3c14" alt="" width="563"><figcaption></figcaption></figure></div>

Measured against the official weights, both Unsloth quants are on the quality/size frontier. UD-Q8\_K\_XL is the only lossless point. UD-Q4\_K\_XL matches other community MXFP4 formats and is more accurate than the Q4\_K-experts conversions, which are larger yet land at 0.029 KLD.

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FxW5lIQID1dIRlVajHSWm%2Fper_layer.png?alt=media&amp;token=94dd4abc-e7ef-4aa8-8d2f-de8c98a69166" alt="" width="563"><figcaption></figcaption></figure></div>

The error split by layer shows why. Keeping the native MXFP4 experts means 0% weight error at every layer. Conversions that re-quantize the experts to Q4\_K or IQ2\_XXS round almost every weight: 5% for Q4\_K, over 30% for IQ2\_XXS.

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FINDS7DqyP9TUAs4Bj9rS%2Fwhy_lossless.png?alt=media&amp;token=efdb261b-f969-42b8-89ec-bc25e8bbdaf3" alt="" width="563"><figcaption><p>Our MXFP4 has exactly zero error on all 8.4M weights, while Q4_K, a different 4-bit grid, must round each one (5.2% RMSE).</p></figcaption></figure></div>

We also found using Q8\_0 and F16 for some tensors  is not lossless, and it gets worse since QAT was applied by DeepSeek to make MXFP4 / FP8 work well, so we had to leave them in BF16 directly. So use UD-Q8\_K\_XL for a true lossless quant, and UD-Q4\_K\_XL downcasts some of the BF16 items to Q8\_0.

For full benchmark tables of [GGUF Benchmarks, see here](#gguf-benchmarks).

### :speech\_balloon: DeepSeek V4 Chat template improvements

We also improved the DeepSeek-V4 chat jinja template, and tested over 4000 conversations to be equivalent with the golden baseline (official DS4)

We added `reasoning_effort` and you can select `max, high` just like official DeepSeek-V4. We prepend the correct system prompt as per DS4, and followed gpt-oss's style.

And for tool calls, `reasoning_content` was retained for DS4, but the jinja chat template would exclude them. We added it back.

#### **Disabling Thinking, changing reasoning effort**

DeepSeek-V4 uses reasoning by default. It also supports reasoning efforts where `reasoning_effort` can be "high", "max" or disabled.

To disable thinking, use `--chat-template-kwargs '{"enable_thinking":false}'`. If you're on **Windows** Powershell, use: `--chat-template-kwargs "{\"enable_thinking\":false}"`

You can also use `--reasoning on` or `--reasoning off` in llama.cpp as well now!

For reasoning effort customization and or to disable reasoning, use the below examples:

```bash
--chat-template-kwargs '{"reasoning_effort":"max"}'
--chat-template-kwargs '{"reasoning_effort":"high"}'
--chat-template-kwargs '{"enable_thinking":false}'
```

### ⚙️ Usage Guide

DeepSeek-V4-Flash is smaller and faster than DeepSeek-V4-Pro, with **284B** parameters (13B active), and a **1M context window**. The model has 3 modes, **Non-think**, **Think** **High** and **Think** **Max**.&#x20;

It's recommended to use `UD-IQ3_XXS` which is **103GB** for best results. Because the file size does not include KV cache, context allocation, try to have at least **110GB RAM** to run the model.

The `UD-Q8_K_XL` quant is DeepSeek-V4-Flash in full original precision. It is 162GB size and it's best to have at least 169GB of available RAM/VRAM available.

**Table: Inference hardware requirements** (units = total memory: RAM + VRAM, or unified memory)

<table><thead><tr><th>Format</th><th width="129.8004150390625">1-bit</th><th width="130.85650634765625">2-bit</th><th width="140.26702880859375">3-bit</th><th>4-bit (near Lossless)</th><th>Q8_K_XL (Lossless)</th></tr></thead><tbody><tr><td>Standard</td><td>92 GB</td><td>102 GB</td><td>110-135 GB</td><td>162 GB</td><td>169 GB</td></tr><tr><td>DSpark</td><td>102 GB</td><td>112 GB</td><td>120-145 GB</td><td>172 GB</td><td>179 GB</td></tr></tbody></table>

{% hint style="info" %}
**DSpark uses more VRAM than standard**, so plan for **\~10 GB** additional RAM/VRAM headroom.
{% endhint %}

{% hint style="success" %}
For best performance, make sure your total available memory, including VRAM and system RAM, exceeds the quantized model file size by a comfortable margin.
{% endhint %}

### Recommended Settings

DeepSeek recommends these parameters for best performance: `temperature = 1.0`, `top-p = 1.0`. For **DeepSeek-V4-Flash-0731** and agentic scenarios, `top-p = 0.95` is suggested instead and `top-p = 1.0` for other tasks.

**Think High is on by default.** If disabled, you can enable it via: `--chat-template-kwargs '{"enable_thinking":true}'` or toggle it via the UI dropdown in [Unsloth](#unsloth-studio-guide). Also see [#deepseek-v4-chat-template-improvements](#deepseek-v4-chat-template-improvements "mention")

{% columns %}
{% column width="50%" %}

| DeepSeek-V4-Flash-0731        |
| ----------------------------- |
| `temperature = 1.0`           |
| `top-p = 1.0`                 |
| `top-p = 0.95` (agentic only) |
| {% endcolumn %}               |

{% column width="50%" %}

| Old DeepSeek-V4-Flash and V4-Pro |
| -------------------------------- |
| `temperature = 1.0`              |
| `top-p = 1.0`                    |
| {% endcolumn %}                  |
| {% endcolumns %}                 |

* **Maximum context window:** `1,048,576`
* For Think Max, set context to at least **384K tokens**.

## Run DeepSeek-V4-Flash Tutorials:

For this tutorial, we will use the 3-bit quant `UD-IQ3_XXS`, as it fits on a 128GB RAM device. Replace `UD-IQ3_XXS` with `UD-Q8_K_XL` (original quality) or another quant if your machine has enough memory. You can now run DeepSeek-V4-Flash-0731 in [Unsloth Desktop](#run-in-unsloth-studio) . **DSpark is automatically enabled in** [**Unsloth**](#unsloth-studio-guide)**.**

<a href="/docs/models/deepseek-v4.md#unsloth-studio-guide" class="button primary">🦥 Unsloth Guide</a><a href="/pages/2f4eyCpdyRknNuEtv22n#llama.cpp-guide" class="button primary">🦙 Llama.cpp Guide</a><a href="/docs/models/deepseek-v4.md#dspark-speculative-decoding" class="button secondary">⚡DSpark Guide</a>

### 🦥 Unsloth Guide

DeepSeek-V4-Flash-0731 can now be run and trained in [Unsloth](/docs/new/studio.md), our new open-source UI for local AI. Unsloth Desktop lets you run models locally on **MacOS**, **Windows**, Linux and:

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

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FCwcXvmLERJSUNF6iNTiY%2Fdeepseek-v4-flash-0731-unsloth-studio.png?alt=media&amp;token=6fdc0216-d21e-42e7-bb57-8e1abf6e7f4f" alt=""><figcaption></figcaption></figure>
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

#### Search and download DeepSeek-V4-Flash

Go to [Unsloth Chat](/docs/new/studio/chat.md) or Model hub and search for DeepSeek-V4-Flash in the search bar and download your desired model and quant.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FGEc90VxPAgTHulQe9zB0%2FScreenshot%202026-07-31%20at%208.01.35%E2%80%AFAM.png?alt=media&amp;token=2931411d-8f75-4bfe-918a-73fcafe918f9" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Run DeepSeek-V4-Flash-0731

Inference parameters should be auto-set when using Unsloth, however you can still change it manually. Because **Think High is on by default**, you can go to the right dropdown to toggle it to Non-think or Think Max. You can also edit the context length, chat template and other settings. **DSpark is automatically enabled in** [**Unsloth**](#unsloth-studio-guide)**.**

For more information, you can view our [Unsloth inference guide](/docs/new/studio/chat.md).

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FlvJqDRKlWdAVkn3HXJZA%2F1000024247.png?alt=media&amp;token=e84fd31d-7720-40d5-aba1-ba65ac34ce97" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Serve DeepSeek-V4 with Unsloth API

You can use `unsloth run` command and serve DeepSeek via an API using `llama-server` runtime flags, including context sizing, GPU layers, threading, sampling, networking, and tool configuration. For more info see our [API docs](/docs/basics/api.md) or [unsloth start](/docs/integrations/unsloth-start.md).

```bash
unsloth run --model unsloth/DeepSeek-V4-Flash-0731-GGUF:UD-IQ3_S
```

{% endstep %}

{% step %}

#### Unsloth is now ready

You can also do many other things with DeepSeek via Unsloth Desktop like:

* **Connect tools:** [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md), [web search](/docs/new/studio/chat.md#advanced-web-search), [MCP](/docs/basics/mcp.md) and more
* **Train models:** Fine-tune text, diffusion, [embedding](/docs/basics/embedding-finetuning.md), and more
* **Generate media:** Create and train [images](/docs/basics/diffusion-image.md), video, [TTS](/docs/basics/text-to-speech-tts-fine-tuning.md) locally
  {% endstep %}
  {% endstepper %}

### 🦙 Llama.cpp Guide

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
You can now use `llama.cpp` directly to load and download models, just like `ollama run`. First, select the quantization type you want like `IQ3_XXS`. Also use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location. Note this download process might be very slow, so it's probably best to use the manual download process in the next section.

```bash
export LLAMA_CACHE="unsloth/DeepSeek-V4-Flash-0731-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/DeepSeek-V4-Flash-0731-GGUF:UD-IQ3_S \
    --temp 1.0 \
    --top-p 1.0 \
    --min-p 0.01
```

{% endstep %}

{% step %}
If you want to download the model manually, we can download the model via the code below (after installing `pip install huggingface_hub`). If downloads get stuck, see: [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

```bash
hf download unsloth/DeepSeek-V4-Flash-0731-GGUF \
    --local-dir unsloth/DeepSeek-V4-Flash-0731-GGUF \
    --include "*UD-IQ3_S*" # Use "*UD-IQ4_XS*" for 4-bit
```

{% endstep %}

{% step %}
You can edit `--threads 32` for the number of CPU threads, `--ctx-size 32768` for context length, `--n-gpu-layers 2` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/DeepSeek-V4-Flash-0731-GGUF/UD-IQ3_S/DeepSeek-V4-Flash-0731-UD-IQ3_S-00001-of-00004.gguf \
    --temp 1.0 \
    --top-p 1.0 \
    --min-p 0.01
```

{% endcode %}
{% endstep %}
{% endstepper %}

## :zap:DSpark - Speculative Decoding

DeepSeek-V4-Flash-0731 has native DSpark, which allows for up to **2x faster decoding speed**! DSpark is a new algorithm by DeepSeek that is superior to naive MTP, and was introduced in this [paper](https://arxiv.org/abs/2607.05147). DSpark enables DeepSeek-V4-Flash to reach **120 tokens/s** on a B200 GPU compared to the original 60 tokens/s baseline. **DSpark is automatically enabled in the** [**Unsloth**](#unsloth-studio-guide) **local UI.**

Llama.cpp integrated DSpark as part of [PR 25784](https://github.com/ggml-org/llama.cpp/pull/25784) with further improvements to multi GPU and more. We show using `--spec-draft-n-max 3` as a good default, allowing 1.9x faster inference speed. Larger values seem to be slower.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FRV0T1cVPpCnacNnywAsL%2Fimage.png?alt=media&amp;token=b570026f-4577-4a45-936f-98a650d644ac" alt=""><figcaption></figcaption></figure>

Download both the drafter and the GGUF - we made 2 Q8\_0 and the lossless BF16 one. Note DSpark will need \~10GB more memory usage, so 128GB machines will need IQ3\_XXS and Q8\_0

{% code overflow="wrap" %}

```bash
hf download unsloth/DeepSeek-V4-Flash-0731-GGUF \
    --local-dir unsloth/DeepSeek-V4-Flash-0731-GGUF \
    --include "*dspark-DeepSeek-V4-Flash-0731-Q8_0*" \
    --include "*UD-IQ3_XXS*" # Use "*UD-IQ4_XS*" for 4-bit
```

{% endcode %}

Then load it via llama-cli or llama-server:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/DeepSeek-V4-Flash-0731-GGUF/UD-IQ3_XXS/DeepSeek-V4-Flash-0731-UD-IQ3_XXS-00001-of-00004.gguf \
    -md unsloth/DeepSeek-V4-Flash-0731-GGUF/dspark-DeepSeek-V4-Flash-0731-Q8_0.gguf \
    --temp 1.0 \
    --top-p 1.0 \
    --min-p 0.01 \
    --spec-type draft-dspark \
    --spec-draft-n-max 3 \
    -ngl 99 -ngld 99
```

{% endcode %}

Benchmarks from the original DSpark paper as well showing how it fares against MTP:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNXmTkimQGD9JzAq4OtK9%2Fimage.png?alt=media&amp;token=bab3816c-e3cd-4bd8-a234-6226520f45f6" alt=""><figcaption></figcaption></figure>

## 📊 Benchmarks

### GGUF Benchmarks

See below for a table comparing benchmarks for quants from Unsloth and other providers. Reference = official weights. Perplexity and KL-divergence over wikitext-2 at ctx 512 on 4x B200.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FXjXSVsiH2ZIKlJ7iZPDx%2Fkldddd.webp?alt=media&amp;token=e1db5fca-b2b4-411e-8956-29127ef6bfe0" alt="" width="563"><figcaption></figcaption></figure>

| Quant                              | Size (GB) | PPL    | Mean KLD           | RMS delta-p | Same top token | Bit-exact weights |
| ---------------------------------- | --------- | ------ | ------------------ | ----------- | -------------- | ----------------- |
| Official (reference)               | 156.4     | 4.5319 | 0                  | 0%          | 100%           | 100%              |
| **Unsloth UD-Q8\_K\_XL**           | 161.9     | 4.5319 | **\~0 (lossless)** | 0.000%      | 100.000%       | **100.000%**      |
| **Unsloth UD-Q4\_K\_XL**           | 155.1     | 4.5335 | 0.0102             | 3.40%       | 96.28%         | 97.46%            |
| bartowski MXFP4                    | 156.0     | 4.5351 | 0.0105             | 3.42%       | 96.18%         | 97.57%            |
| antirez Q4KExperts-F16 (imatrix)   | 164.6     | 4.5743 | 0.0291             | 5.87%       | 93.95%         | 0.51%             |
| antirez Q4KExperts-F16             | 164.6     | 4.5726 | 0.0290             | 5.89%       | 93.94%         | 0.93%             |
| antirez mixed L37-42-Q4K (imatrix) | 97.6      | 5.8169 | 0.3605             | 21.15%      | 79.74%         | 0.41%             |
| antirez IQ2XXS (imatrix)           | 86.7      | 6.0808 | 0.4079             | 22.23%      | 78.15%         | 0.39%             |
| antirez IQ2XXS                     | 86.7      | 6.1518 | 0.4207             | 22.74%      | 77.92%         | 0.47%             |

### Official Benchmarks

DeepSeek-V4-Flash-0731 outperforms DeepSeek-V4-Pro (Preview) on the benchmarks below despite using far fewer activated parameters, and remains competitive with leading proprietary models.

| Benchmark              | DeepSeek-V4-Flash-0731 | DeepSeek-V4-Flash (Preview) | DeepSeek-V4-Pro (Preview) | GLM-5.2 | Opus-4.8 |
| ---------------------- | :--------------------: | :-------------------------: | :-----------------------: | :-----: | :------: |
| Terminal Bench 2.1     |          82.7          |             61.8            |            72.1           |   81.0  |   85.0   |
| NL2Repo                |          54.2          |             39.4            |            38.5           |   48.9  |   69.7   |
| Cybergym               |          76.7          |             38.7            |            52.7           |    -    |   83.1   |
| DeepSWE                |          54.4          |             7.3             |            12.8           |   46.2  |   58.0   |
| Toolathlon-Verified    |          70.3          |             49.7            |            55.9           |   59.9  |   76.2   |
| Agents' Last Exam      |          25.2          |             15.8            |            16.5           |   23.8  |   25.7   |
| AutomationBench Public |          25.1          |             10.8            |            12.8           |   12.9  |   27.2   |
| DSBench-FullStack †    |          68.7          |             37.0            |            41.8           |   61.8  |   71.6   |
| DSBench-Hard †         |          59.6          |             25.8            |            31.1           |   54.5  |   71.7   |


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/deepseek-v4.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
