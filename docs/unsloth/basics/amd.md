> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/amd.md).

# Train & run models on AMD GPUs with Unsloth

Unsloth now officially supports AMD hardware, making it easy to run, train, fine-tune, RL, and deploy models locally on AMD GPUs. Fully open source, [Unsloth](/docs/desktop.md) runs on Windows, WSL, and Linux, supporting RDNA 1–4, Radeon RX 9000 and 7000 series GPUs, Instinct MI350 and MI300 data center GPUs, Vulkan, Strix Halo - powered Ryzen AI Max systems, and more.

We collaborated with [AMD](https://www.amd.com/en/developer/resources/technical-articles/2026/train-and-run-models-on-amd-gpus-with-unsloth.html) and our community to enable up to 2x faster and 70% less VRAM training for all models with no accuracy loss. If you don't have a GPU, Unsloth still supports native AMD inference for [Qwen3.6](/docs/models/qwen3.6.md), [Gemma 4](/docs/models/gemma-4.md), DeepSeek-V4, GLM 5.2, DiffusionGemma, Kimi K2.7 and other models.

<a href="/docs/basics/amd.md#installing-unsloth-on-amd" class="button primary" data-icon="bolt">Quickstart</a><a href="/docs/basics/amd.md#id-2x-faster-training-and-50-more-accurate-tool-calls" class="button secondary" data-icon="star">Features</a><a href="https://github.com/unslothai/unsloth" class="button secondary" data-icon="github">Github</a>

{% hint style="success" %}
**Sept 18 Update:** Added **RDNA 1, 2, Gorgon Halo, Vulkan support** + fixed not detecting GPUs on AMD GPUs.\
Better RDNA4, HIP / ROCm failure auto fixing and catching.
{% endhint %}

To install Unsloth on AMD, the easiest way is to download our [Desktop app](/docs/desktop.md).

<a href="https://unsloth.ai/download/windows" class="button secondary" data-icon="windows">Download for Windows</a><a href="https://unsloth.ai/download/linux" class="button secondary" data-icon="linux">Download for Linux</a>\
\
For manual installation:

**MacOS, Linux, WSL:**

{% code overflow="wrap" expandable="true" %}

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

{% endcode %}

**Windows Powershell:**

<pre class="language-powershell" data-overflow="wrap"><code class="lang-powershell"><strong>irm https://unsloth.ai/install.ps1 | iex 
</strong></code></pre>

### ⭐ Features

Unsloth supports both inference and training for AMD, so if you don't have a GPU and only CPU, you can still run models with Unsloth. When using Unsloth, you get:

* [**Tool call healing**](/docs/new/studio/chat.md#auto-healing-tool-calling) **for inference to increase accuracy by 50%**, unlimited free [web search](/docs/new/studio/chat.md#advanced-web-search), HTML canvases, [**secure HTTPS deployment**](#unsloth-on-phones-and-remote-https-tunneling) via Cloudflare and [Code Execution](/docs/new/studio.md#execute-code--heal-tool-calling) all work.
* **Train Gemma 4 models in 8GB VRAM** or Qwen3.5 in 3GB VRAM. Triton kernels, math algorithms and memory tricks allow 70% less VRAM use for AMD with no accuracy loss.
* Up to **80% less VRAM usage for** [**reinforcement learning**](/docs/get-started/reinforcement-learning-rl-guide/grpo-long-context.md) such as GRPO. And weight sharing with vLLM to save 50% memory usage.
* Optimized support for **RDNA 3** and newer GPUs & data-center grade GPUs. Strix Halo is also optimized for Linux, WSL and Windows.

{% columns %}
{% column %}

* [**Connect**](/docs/integrations/unsloth-start.md) **your local models to any agent harness**: [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md), [Hermes](/docs/integrations/hermes-agent.md), [OpenClaw](/docs/integrations/openclaw.md) and more.
* Support inference and training for nearly **all models**, including the latest [DeepSeek-V4](/docs/models/deepseek-v4.md), [GLM-5.2](/docs/models/glm-5.2.md), [Kimi-K2.7](/docs/models/kimi-k2.7-code.md), [MiniMax M3](/docs/models/minimax-m3.md), [DiffusionGemma](/docs/models/diffusiongemma.md), [Inkling](/docs/models/inkling.md) and more!
* AMD multi-GPU support + VRAM/RAM tracking. `llama.cpp` ROCm prebuilts are provided daily, so you always get the latest model updates!
  {% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fszoidwwj70dLm5vBjpmL%2Fdiffusiongemma.gif?alt=media&amp;token=8ce359fd-f92c-4cf8-a491-06b04c505cb7" alt="" width="375"><figcaption><p>DiffusionGemma running on AMD GPUs</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

### ⚡Quickstart

Unsloth auto installs the best ROCm builds for PyTorch, llama.cpp prebuilts, bitsandbytes, ROCm optimized kernels & Triton. We also ship our AMD optimizations and fixes together. You can read our more [detailed guide here](#guide-to-using-unsloth-on-amd) for more details.

We made Unsloth installations seamless for Windows and WSL folks - but we generally recommend using Linux directly since it'll have the broadest support. Unsloth supports MacOS, Linux, [Windows](/docs/get-started/install/windows-installation.md), [NVIDIA](/docs/get-started/install/pip-install.md), Intel and CPU setups. See: [Unsloth Requirements](/docs/get-started/fine-tuning-for-beginners/unsloth-requirements.md). Updating are the same commands!

**MacOS, Linux, WSL:**

{% code overflow="wrap" %}

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

{% endcode %}

**Windows PowerShell:**

{% code overflow="wrap" %}

```bash
irm https://unsloth.ai/install.ps1 | iex
```

{% endcode %}

{% columns %}
{% column %}
Unsloth will auto install ROCm, PyTorch, custom llama.cpp prebuilts and more!

#### Accessing Unsloth remotely

We also enabled [Cloudflare HTTPS tunneling](#unsloth-on-phones-and-remote-https-tunneling) for free - so you can access Unsloth securely via HTTPS remotely.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FsnKMaYneotmsSaEvA2mU%2Finstall%201.png?alt=media&amp;token=bbfba550-a47e-4273-80f5-a21bfc44717c" alt=""><figcaption><p>Installing Unsloth on AMD Windows machines</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

#### :inbox\_tray: Install Unsloth Notebooks & pip install

If you want plain Unsloth notebooks, see the general [AMD](/docs/get-started/install/amd.md) install guide. Be sure to read[AMD](/docs/get-started/install/amd.md) install guide! After you follow it for installing PyTorch and ROCm, then do:

{% code overflow="wrap" %}

```bash
uv pip freeze | grep -E '^(torch|torchvision|torchaudio)==' > torch-pins.txt
echo "triton ; sys_platform == 'never'" >> torch-pins.txt
echo "xformers ; sys_platform == 'never'" >> torch-pins.txt
uv pip install "unsloth[amd]" --overrides torch-pins.txt
```

{% endcode %}

#### :play\_pause:Unsloth Start

{% columns %}
{% column width="58.333333333333336%" %}
[Unsloth Start](/docs/integrations/unsloth-start.md) lets you connect [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md) and other agents to local models via the `unsloth start` command.

Start Unsloth, open your project folder, and run:

{% code overflow="wrap" %}

```bash
unsloth start claude --model \
    unsloth/gemma-4-E2B-it-GGUF:UD-Q4_K_XL
```

{% endcode %}

Replace `claude` with any agent below:
{% endcolumn %}

{% column width="41.666666666666664%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FpXE6kCHjh8qOEaggf94M%2FScreenshot_20260718_122426.png?alt=media&amp;token=a59e4c8c-efdb-451b-b1f8-621955564f6d" alt="" width="563"><figcaption><p>Claude Code running with Qwen3.5 locally.</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

| Agent                                                              | Command                  |
| ------------------------------------------------------------------ | ------------------------ |
| <i class="fa-claude">:claude:</i> Claude Code                      | `unsloth start claude`   |
| <i class="fa-openai">:openai:</i> OpenAI Codex                     | `unsloth start codex`    |
| <i class="fa-caduceus">:caduceus:</i> Hermes Agent                 | `unsloth start hermes`   |
| <i class="fa-lobster">:lobster:</i> OpenClaw                       | `unsloth start openclaw` |
| <i class="fa-rectangle-vertical">:rectangle-vertical:</i> OpenCode | `unsloth start opencode` |

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fs6AKlSRUrfdwYDIZpcjN%2Fimage(6).png?alt=media&amp;token=d8042094-2df1-4737-b806-08a77e45e105" alt=""><figcaption><p>Claude instances are all isolated</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FahmAqUZMFFI3VouqwIYf%2Fimage(5).png?alt=media&amp;token=0dd84f49-16cf-4799-a1d3-e6cbbe105115" alt=""><figcaption><p>Codex running unsloth/gemma-4-E2B-it dynamic 4bit</p></figcaption></figure></div>

### :bar\_chart: AMD Analysis

We brought many of our optimizations we made for non AMD GPUs over to make AMD GPUs shine! Getting AMD training to work on Windows devices and ensuring compatbility across nearly every AMD device was a lot of work but we're happy in the current state. We are still actively working on making AMD GPUs even better! Below are some analysis/benchmarks we conducted on a AMD MI300X.

#### Reinforcement learning: more accurate LoRA and QLoRA

During RL on AMD, Unsloth supports **weight sharing** with vLLM as introduced in [Memory Efficient RL](/docs/get-started/reinforcement-learning-rl-guide/memory-efficient-rl.md). We **halve memory usage** by directly accessing vLLM's allocation of the model.

During LoRA and QLoRA, we also do not do merging and demerging of the LoRA weights like below:

$$
W = W + sAB \\
\text{inference} = XW \\
W = W - sAB
$$

The above causes issues as **IEEE floats are not associative due to rounding**. When W is in BF16, this causes subtle differences when subtracting as done in other RL engines. This means in IEEE land:

$$
W \ne(W + sAB) - (sAB)
$$

And when W is in bfloat16 with few mantissa bits, it **rounds small numbers to zero**. Since A and B are float32 during LoRA, this means W can drift over time after merging & demerging. Unsloth uses vLLM's LoRA path directly, so we avoid this. The base weights are never edited and will never drift.

#### Faster Reinforcement Learning

{% columns %}
{% column %}
We benchmarked other setups with FA2 and vLLM co-located. Both use vLLM for generation, Unsloth pushes more of the step into generation while making training and roughly 2x faster.

All three benchmarks are reproducible: same seeds, same token budgets, and the loss curves match between the two stacks.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F31TQsJ8fBG7Vts7u37J8%2Fchart_grpo_combined.png?alt=media&amp;token=719e2729-839e-4287-aa00-5e3b77e1ad7b" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

#### Faster & more memory efficient training

On Llama-3.1-8B LoRA SFT (batch 2 x grad-accum 4 x 2048 = 16,384 tokens/step, packed), Unsloth trains at 2.07 s/step vs 2.87 s/step for TRL + FA2, and peaks at 18.3 GB versus 24.3 GB. That is 1.39x faster and 1.33x less memory usage, with no change in accuracy. We plan to make this even better!

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F1YySU2nLYyKoSyXh8lsi%2Fchart_llama8b_vram_over_time.png?alt=media&amp;token=526b2488-315e-487b-8baa-ee71d5e1408a" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FJQH7QTamM7zuK45NNnZY%2Fchart_llama8b_sft_efficiency.png?alt=media&amp;token=81388e0a-e9ca-433d-9cca-1b32f406043b" alt=""><figcaption></figcaption></figure></div>

The memory savings are not just a lower peak, they hold for the whole run. Sampling allocated VRAM every 0.1s, Unsloth stays flat and low the entire time, while other setups + FA2 spikes toward 22.8 GB on nearly every step and takes longer to finish (75s vs 56s for the same 25 steps).

### :sparkles:Supported AMD Hardware

Unsloth’s AMD support focuses on popular consumer, workstation, and datacenter GPUs. Training, Unsloth Studio, and GGUF/llama.cpp inference support can vary by architecture, so the table below separates optimized support from compatibility paths.

<table><thead><tr><th>Architecture</th><th>Series</th><th width="159">gfx</th><th>Support</th><th>Platform</th></tr></thead><tbody><tr><td>RDNA 4</td><td>Radeon™ RX 9000 Series</td><td>gfx1200, gfx1201</td><td>Full</td><td>Windows + WSL + Linux</td></tr><tr><td>RDNA 3.5</td><td>Ryzen AI 300 / Ryzen AI MAX (Strix Halo)</td><td>gfx1150, gfx1151, gfx1152</td><td>Full</td><td>Windows + WSL + Linux</td></tr><tr><td>RDNA 3</td><td>Radeon™ RX 7000 Series</td><td>gfx1100, gfx1101, gfx1102</td><td>Full</td><td>Windows + WSL + Linux</td></tr><tr><td>RDNA 2</td><td>Radeon™ RX 6000 Series</td><td>gfx1030, gfx1031, gfx1032, gfx1034</td><td>Full</td><td>Windows + WSL + Linux</td></tr><tr><td>RDNA 1</td><td>Radeon™ RX 5000 Series</td><td>gfx1010, gfx1012</td><td>Full</td><td>Windows + WSL + Linux</td></tr><tr><td>CDNA 4</td><td>Instinct™ MI350 Series GPUs</td><td>gfx950</td><td>Full</td><td>Linux only</td></tr><tr><td>CDNA 3</td><td>Instinct™ MI300 Series GPUs</td><td>gfx940, gfx941, gfx942</td><td>Full</td><td>Linux only</td></tr><tr><td>CDNA 2</td><td>Instinct™ MI200 Series GPUs</td><td>gfx90a</td><td>Full</td><td>Linux only</td></tr><tr><td>CDNA 1</td><td>Instinct™ MI100 Series GPUs</td><td>gfx908</td><td>Full</td><td>Linux only</td></tr></tbody></table>

### :desktop: Guide to using Unsloth on AMD

After installation, you can open Unsloth Studio in your browser. From there, you can run and fine-tune local LLMs on AMD hardware automatically. See below for detailed install instructions:

{% columns %}
{% column width="50%" %} <a href="/docs/get-started/install/amd.md" class="button primary">AMD Install Guide</a><a href="/docs/new/studio/install.md" class="button primary">Install Unsloth Studio</a>

Select your model, dataset, and training settings to begin. For example, you can run QLoRA 4-bit fine-tuning on Gemma 4 12B with a context length of \~16k, LoRA rank 16, learning rate 0.0002, and 30 max steps.
{% endcolumn %}

{% column width="50%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F2GbvLBqN03qsvh5N9Uq1%2Fft%20studio.png?alt=media&amp;token=71fd643b-32f1-4f7f-8183-1e1fa97e80c0" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}
Unsloth Studio’s fine-tuning screen is fully customizable, letting you configure your model, dataset, and training parameters. During training, Unsloth tracks progress in real time, including loss, RAM and VRAM usage, as well as support for multi-gpu. Once training starts you will see the progress plotted in real time.

After training, you can visit your history to see past and active training sessions. Select from any of your fine-tuned models to view past training logs:
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FhATsVSzX50cDHFtnfRAN%2Fimage.png?alt=media&amp;token=ce89695a-1579-4ae5-8423-e3ddace69f8e" alt="" width="563"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fxm20hpZ7TK1y3xrzN6vp%2Fimage.png?alt=media&amp;token=77d9959c-4415-4f49-9413-684e83a3f4b8" alt="" width="563"><figcaption></figcaption></figure></div>

{% columns %}
{% column %}
When training is complete, export your model as GGUF, merged model safetensors, or a LoRA Adapter for deployment with Hugging Face, llama.cpp, vLLM, or Unsloth. For GGUF exports, Unsloth uses AMD-aware llama.cpp ROCm prebuilts matched to your gfx architecture, with source compilation as a fallback when no prebuilt is available. Once export completes, you will see Export finished successfully. You can also push your model directly to the Hugging Face Hub.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FDVdUSCq0apPcx5mU2AYq%2Fimage.png?alt=media&amp;token=481db1ed-bae7-44c5-976e-2f5e85f886b6" alt="" width="563"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}
Export your model to your preferred format and deploy it anywhere. After exporting, load your fine-tuned model from the Fine-tuned section of the model dropdown in New Chat or Recents.

Select your fine-tuned model from the dropdown and chat with it directly in Unsloth. You can now use your trained or downloaded models in New Chat, Recents, or Projects. Enable think, code, and search toggles for the best experience, and see the [Unsloth Studio Chat](https://unsloth.ai/docs/new/studio/chat) docs for more details.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FRcgOQ8zbfLAYhypopa0V%2Fimage.png?alt=media&amp;token=393d9bb3-1eb7-4171-9dd3-ef0377a176d5" alt="" width="407"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

And finally, you can chat with your newly fine-tuned model directly in Unsloth!

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FCGaDuaOaNNzd6NrtpnD5%2Funsloth%20studio%20chat%20screenshot.png?alt=media&amp;token=d179749f-f027-4ab4-8082-f1c87b8a59be" alt=""><figcaption></figcaption></figure>

You can also monitor throughput and generation tokens / s within the terminal just like vLLM logging. You will see `"gen_tok_s"` which is the tokens / s and `"prompt_tok_s"` which is prompt processing.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F0wOZYG4Y72hZInt9BBjk%2Fthroughput.png?alt=media&amp;token=102dcc3a-75e6-4b7e-9631-4cd3115f7df9" alt=""><figcaption></figcaption></figure>

### :mobile\_phone:Unsloth on phones and remote HTTPS tunneling

We added **free** Cloudflare HTTPS tunnels for Unsloth (similar to LM Link), so you can remotely chat / train models with Unsloth on your phone (iPhone, Android - any phone!) via a link or any other computer! This works on Mac, Linux, WSL and Windows devices.

* Train & finetune from your phone / **remotely with live training loss logs** - cancel or retrain!
* Chat in the browser from anywhere with tool calling and live streaming.
* Actual **interact-able HTML canvas** outputs right in your phone - play games made by LLMs!

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FfuLfgQ7m7gB5IK8fZdDo%2Fphone%20inference.png?alt=media&amp;token=a7aec44c-02b8-483d-ab5b-7268f802a3e9" alt="" width="188"><figcaption><p>Chat remotely!</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FlmeAQLZAFGGy21rDmBUn%2Fphone%20thinking.png?alt=media&amp;token=6f0fe9a6-c849-4ff0-bd7d-dea8dbffd222" alt="" width="188"><figcaption><p>Live inference + tool calling</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FEQWneGD6ncfYTe6NugtO%2Fphone%20training%20logs.png?alt=media&amp;token=1c830286-f6bc-472c-8915-3f45daadb0a9" alt="" width="188"><figcaption><p>Remote training logs!</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fz1JnnGZmO5aWy57dK1w1%2Fphone%20flappy%20bird.png?alt=media&amp;token=b31fd81d-eb97-4c55-a93c-1e5f5742557a" alt="" width="188"><figcaption><p>Run live HTML in the phone</p></figcaption></figure></div>

To set it up, first in terminal after installing Unsloth, type `unsloth studio --secure` . Setup a password so no one unauthorized can access the HTTPS link!

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQfRsJGUWXMCGYczt1G0K%2Fsecure%20login%20password.png?alt=media&amp;token=23f3976b-4e23-49da-a95c-e32fb53952f0" alt=""><figcaption></figcaption></figure>

Then in the logs - use the <mark style="color:$success;">**green Cloudflare link**</mark> and enter this on our Phone or any remote device!

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F5UifJGPRo0GfSbm8UeAG%2Fsecure%20terminal%20link.png?alt=media&amp;token=8da77481-a380-4f26-af9f-c31342992d41" alt=""><figcaption></figcaption></figure>

And you're in! You can always monitor / cancel the live HTTPS served link by CTRL+C ing the terminal where Unsloth Studio was launched!

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FDYsI12Qy2lN1TuNu8HrJ%2Fphone%20model%20select.png?alt=media&amp;token=05891101-47cd-430b-9a76-698ccca60246" alt="" width="188"><figcaption><p>Edit inference settings</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fi9RMJOuSJCZ0eTGr4iIJ%2Fphone%20extra%20optios.png?alt=media&amp;token=5fa1d410-9d5d-4964-8d51-c1f3e82ac213" alt="" width="188"><figcaption><p>Edit temp, top_p, ctx length</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FgNBUBdVsZ08XfJtDv5Ux%2Fphone%20canvas.png?alt=media&amp;token=207ff0e7-9653-4181-9344-6fab86bc2b9a" alt="" width="188"><figcaption><p>Canvas auto renders HTML!</p></figcaption></figure></div>

### :question:How AMD support was built for Unsloth

Unsloth’s custom kernels were ported to AMD in close collaboration with the AMD team. This required changes across the installer, hardware detection, runtime routing, monitoring, and prebuilt asset selection.

* **ROCm kernels:** HIP/Triton ports tuned for RDNA and CDNA, with architecture-specific precision, performance, and stability fixes. ([#2520](https://github.com/unslothai/unsloth/pull/2520))
* **4-bit training:** bitsandbytes-based QLoRA support for Radeon and CDNA GPUs. ([#3748](https://github.com/unslothai/unsloth/pull/3748))
* **Automatic setup:** robust AMD GPU detection and installation of the correct ROCm PyTorch wheel, including repair and platform safeguards. ([#4770](https://github.com/unslothai/unsloth/pull/4770))
* **Windows and Strix Halo:** native Windows ROCm installation, runtime compatibility patches, unified-memory reporting, and WSL support. ([#5301](https://github.com/unslothai/unsloth/pull/5301), [#6227](https://github.com/unslothai/unsloth/pull/6227))
* **ROCm inference:** architecture-specific llama.cpp prebuilts, source-build fallback, AMD VRAM detection, and monitoring. ([#5172](https://github.com/unslothai/unsloth/pull/5172))

### :clock1: Future work

Thanks so much to the AMD team for collaborating with us on making AMD work well! Upcoming priorities include:

* Continued development and engagement with the AMD team.
* Expanded hardware-backend CI/CD using AMD Strix Halo and Radeon Lab hardware.
* Support for new AMD GPU cards and architectures as they launch.
* Clearer multi-GPU guidance: AMD distributed training is currently Linux-only. On Linux, ROCm uses RCCL, so distributed training works. On Windows, AMD ROCm does not yet provide a GPU-collective backend, with GLOO/CPU-only support as of [TheRock #5694](https://github.com/ROCm/TheRock/pull/5694), use Linux if you plan to do AMD multi-GPU training.
* Further speed optimizations with respect to the ROCm stack.

### :love\_letter: Thanks to AMD for collaborating!

Thanks so much to the AMD team and our amazing Unsloth community for collaborating with us on this release. We thank Strahinja Stamenkovic, Filip Jankovic, Iswarya Alex, Yue Yuan Bill He, Eda Zhou, Mahdi Ghodsi, Guruprasad and the entire AMD team for collaborating on making AMD support work great with Unsloth! Also huge thanks to community members: Nate, UBER6, AiwendilOfMirk..., Gene, Jimster480, VELICAN, Vintheboy, archmaker, BichonFriseMax, Calandracas, Chigoma333, Edd, electroglyph, jslowbell, mk 27B UD-, Satyam, snapcast3r, TotoMC for testing and debugging with us.

An easy way to use Unsloth on AMD is through [AMD Developer Cloud](https://www.amd.com/en/developer/resources/cloud-access/amd-developer-cloud.html), with one-click notebooks powered by MI300X GPUs with 192GB VRAM. AMD also offers free credits through the [AMD AI Developer Program](https://www.amd.com/en/developer/ai-dev-program.html). To run an Unsloth notebook, use any AMD notebook from [unslothai/notebooks](https://github.com/unslothai/notebooks) and swap the GitHub domain with the AMD Developer Cloud URL, since the notebook paths are the same.

Need help or want to share feedback? You can join our [Discord](https://discord.com/invite/unsloth), read the [AMD docs](https://unsloth.ai/docs/get-started/install/amd), open an issue or PR on [GitHub](https://github.com/unslothai/unsloth/issues), or post on our [Reddit r/unsloth](https://www.reddit.com/r/unsloth/).


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/amd.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
