> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/new/changelog.md).

# Unsloth Updates

Unsloth Changelog for our latest releases, improvements and fixes.

To use the latest changes, [update Unsloth](/docs/new/studio/install.md#update-unsloth-studio).

{% updates format="full" %}
{% update date="2026-11-06" tags="new-releases" %}

## Qwen3.8-Flash-Next Dynamic V3.1

We're releasing [Qwen3.8-Flash-Next](/docs/models/qwen3.8-next.md) Dynamic V3.1 GGUFs for 10-15% extra accuracy, 50% less token use and 7% faster speed. We're also bringing large performance fixes across Unsloth: faster typing and search in long chats, faster image/video loads, two-GPU image/video gen. It also adds separate browsers for each chat, floating browser window, and scrollable code + thinking blocks.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FfbUDW8UyiD6Z7cq93Ydc%2FScreenshot_2026-11-02_at_14.41.10.webp?alt=media&amp;token=7be485c5-6f5b-4caf-a97a-7470bcb31f91" alt=""><figcaption></figcaption></figure>

#### Highlights

* **Large performance fixes** with more Glass theme optimizations coming next week
* **Glass theme fixes** no more blur, better rendering, more options
* **Unified memory offloading** now properly works for big models
* **Separate browsers for each chat** - Multiple chats can now run their own browser individually
* **New look for Thinking + Code blocks** - now capped with a scrollable container
* **Floating browser** you can move and resize over the chat & let the model do it's thing
* **Two-GPU image and video** up to 2x faster on matching NVIDIA cards
* **Faster chat search and deleting** - search and delete chats much faster
* **Stable diffusion image/video models loads** up to 40% faster

<a href="https://github.com/unslothai/unsloth/releases/tag/v0.1.916-beta" class="button primary">Full Release notes</a><a href="/docs/models/qwen3.8-next.md" class="button secondary">Dynamic V3.1 Qwen</a>
{% endupdate %}

{% update date="2026-10-30" tags="new-releases" %}

## Dynamic V3.1 (preview) + Customize + Performance

Make Unsloth your own with custom backgrounds and a improved UI/UX. This release also cuts app update times and speeds up Linux app and Qwen-Image gen when VRAM is limited. Also new: DeepSeek-V4.1-Flash-1017 in Unsloth [Dynamic v3.1](https://unsloth.ai/docs/models/deepseek-v4.1-flash) GGUFs (preview), FLUX.2-klein-9B on low-RAM machines, smoother chats and batched MoE fine-tuning.

<img src="https://github.com/user-attachments/assets/a4c01069-da2f-4cf3-afee-d19499cfefc3" alt="" width="563">

#### Highlights

* **Custom backgrounds** to personalize your chats (+ move composer to bottom - more customization coming next week)
* **DeepSeek-V4.1-Flash-1017** new Unsloth Dynamic v3.1 GGUFs (preview), the most accurate for their size on nearly all benchmarks [Blog](https://unsloth.ai/docs/models/deepseek-v4.1-flash)
* **14 new languages** for Unsloth
* **App updates** finish twice as fast
* **Linux** much less lag and improved performance
* **Qwen-Image** renders up to 2x faster under a 16 GB VRAM limit
* **Updated interface** with consistency and cleaner UI
* **MoE fine-tuning** runs compatible API jobs together

<a href="https://github.com/unslothai/unsloth/releases/tag/v0.1.913-beta" class="button primary">Full Release notes</a><a href="/docs/models/deepseek-v4.1-flash.md" class="button secondary">Dynamic V3.1 DeepSeek</a>
{% endupdate %}

{% update date="2026-10-28" tags="new-releases" %}

## Scheduled + Optimizations + Halloween

DeepSeek-V4.1-Flash-1017 and FLUX.3 Image Klein are here! Run both locally in Unsloth. Also new: images and videos in chat, multi-GPU training with FSDP2 (alpha) and one-command MCP setup for coding agents.

#### Highlights

* **Faster Unsloth**: 2x faster first launch, plus speedups for tool calls, model lists, dataset prep and MiniMax-H3 loads
* **Scheduled tasks**: Run a prompt on a schedule with a local model or an API
* **Multi-LoRA batching**: up to 4 compatible queued fine-tuning jobs train together
* **SGLang thinking + auto-compact**: Resume and JSON output now work on vLLM and SGLang too
* **Browser use switch**: let models control the built-in browser from its new tab page
* **MiniMax-M3.1-Flash**: MiniMax's 428B MoE (23B active) [Guide](https://unsloth.ai/docs/models/minimax-m3.1-flash)
* **Trick or treat**: 🎃 11 Halloween themes
* **FLUX 3 Editing**: FLUX 3 now supports editing of images with prompts
* **Perf improvements**: Large Mac perf gains, less lag, reduced binary sizes
* **Saved presets**: Save your Run settings as named presets for each model

<a href="https://github.com/unslothai/unsloth/releases/tag/v0.1.912-beta" class="button primary">Full Release notes</a><a href="/docs/models/minimax-m3.1-flash.md" class="button secondary">MiniMax-M3.1-Flash</a><a href="/docs/models/nemotron-3.5-bolt.md" class="button secondary">NVIDIA Nemotron 3.5 4B</a>
{% endupdate %}

{% update date="2026-10-19" tags="new-releases" %}

## DeepSeek V4.1-Flash-1017 and FLUX.3

DeepSeek-V4.1-Flash-1017 and FLUX.3 Image Klein are here! Run both locally in Unsloth. Also new: images and videos in chat, multi-GPU training with FSDP2 (alpha) and one-command MCP setup for coding agents.

#### Highlights

* **DeepSeek-V4.1-Flash-1017**: 552B (16B active) - runs on \~125 GB at 1-bit with its Engram table on SSD [Guide](https://unsloth.ai/docs/models/deepseek-v4.1-flash)
* **FLUX.3 Image Klein**: Runs on 24 GB and edits with up to 10 reference images [GGUF](https://huggingface.co/unsloth/flux-3-image-klein-GGUF)
* **One-command MCP setup**: `unsloth mcp add` connects Claude Code, Codex or Cursor to Unsloth.
* **Images and videos in chat**: Local chat models use the image or video model loaded beside them.
* **Qwen-Image-Edit-2509 and 2511**: Edit with up to 3 images at once.
* **Token preview**: See what your model will learn before training starts.

<a href="https://github.com/unslothai/unsloth/releases/tag/v0.1.909-beta" class="button primary">Full Release notes</a><a href="/docs/models/deepseek-v4.1-flash.md" class="button secondary">DeepSeek-V4.1-Flash</a>
{% endupdate %}

{% update date="2026-10-15" tags="new-releases" %}

## NVIDIA Nemotron 3.5 + Meta Muse Spark Open

Run NVIDIA's new Nemotron 3.5 models and Meta's new Muse Spark Open locally in Unsloth. New: text-diffusion LLMs, DeepSpeed training and better prompt caching for coding agents.

#### Highlights

* **NVIDIA Nemotron 3.5 Bolt**: Run on 24 GB of memory. [Guide](https://unsloth.ai/docs/models/nemotron-3.5-bolt)
* **NVIDIA Nemotron 3.5 Super VL**: 120B (12B active) [Guide](https://unsloth.ai/docs/models/nemotron-3.5-super-vl)
* **Meta Muse Spark Open**: 816B (42.7B active) - runs on 256GB [Guide](https://unsloth.ai/docs/models/muse-spark-open)
* **Better prompt caching for coding agents**: Claude Code, Codex etc. on local GGUF models re-process far less of each prompt.
* **Browser use**: Always allow properly works, cursor, and separate tabs for each chat.
* **Images through your connections**: generate with sd-server, Ollama, Lemonade and other image servers.
* **Diffusion LLMs**: train and chat with LLaDA, Dream, SDAR and more, with a live denoising canvas.

<a href="https://github.com/unslothai/unsloth/releases/tag/v0.1.908-beta" class="button primary">Full Release notes</a><a href="/docs/models/nemotron-3.5-bolt.md" class="button secondary">Nemotron 3.5 Bolt</a><a href="/docs/models/muse-spark-open.md" class="button secondary">Meta Muse Spark Open</a>
{% endupdate %}

{% update date="2026-10-12" tags="new-releases" %}

## Browser Use + **Qwen-Image-2.1-Turbo**

Models can now use the browser in Unsloth. Turn on Browser use and your model can open pages, read them, click, type and scroll while you watch. Qwen-Image-2.1-Turbo is here too, making images in just 8 steps. Also included: text-diffusion LLM training, faster MoE GGUFs and speculative decoding on Mac.

#### Highlights

* **Browser use.** Local models can take control of the Unsloth Browser
* **Qwen-Image-2.1-Turbo**: images in 8 steps (2.5x faster). [See Guide](https://unsloth.ai/docs/models/qwen-image-2.1)
* **Train text-diffusion LLMs** like DiffusionGemma, LLaDA and Dream
* **Up to 3x faster MoE GGUFs** that are bigger than your VRAM
* **Speculative decoding on Mac** for up to 2.8x faster MLX replies

<a href="https://github.com/unslothai/unsloth/releases/tag/v0.1.906-beta" class="button primary">Full Release notes</a><a href="/docs/models/qwen-image-2.1.md" class="button secondary">Qwen Image 2.1</a>
{% endupdate %}

{% update date="2026-10-08" tags="new-releases" %}

## Train your own Decision model

Turn any text or vision LLM into a Jev-style decision model in Unsloth, with decision accuracy going from 30% to 80%. Train, test, export and serve decision models directly from Unsloth. Also included: native ComfyUI models, diffusion improvements and a better Browser in Desktop.

#### Highlights

* **Turn any model into a Jev-style decision model.** Accuracy 30% to 80%
* **Load ComfyUI diffusion models** natively in Unsloth
* **Faster + more accurate diffusion** with INT8 ConvRot and more
* **Better Browser in Desktop** with many bug fixes
* **Sandboxing** with Bwrap for Linux, Seatbelt for Mac and MXC for Windows

<a href="https://github.com/unslothai/unsloth/releases/tag/v0.1.904-beta" class="button primary">Full Release notes</a><a href="/docs/basics/train-your-own-decision-model-with-unsloth.md" class="button secondary">Decision Model Guide</a>

{% embed url="<https://github.com/user-attachments/assets/92959172-d2a2-450b-a5bf-6369a1e5ae16>" %}
{% endupdate %}

{% update date="2026-10-07" tags="new-releases" %}

## EmbeddingGemma 2 + Browser

This release adds a browser inside Unsloth (browser use coming very soon), so files, web pages and pages the model writes open right beside your chat. It also brings [EmbeddingGemma 2](https://unsloth.ai/docs/models/embeddinggemma-2), Google's new multimodal embedding model, plus new Audio pages and lower-memory training.

#### Highlights

* **Browser beside chat** for files, web pages and model-written HTML, as tabs
* **EmbeddingGemma 2**: run and fine-tune Google's new model for text, code, images, video and audio [Guide](https://unsloth.ai/docs/models/embeddinggemma-2)
* **Audio pages**: Speak, Clone, Music, Transcribe, Edit, Separate, Convert, with 70+ GGUF models
* **Keep multiple models loaded**, plus vLLM and SGLang engines (opt-in)
* **Sandbox** for code the model runs, now with a Settings tab and Colab and Docker support
* **Live preview** during image and video generation

<a href="https://github.com/unslothai/unsloth/releases/tag/v0.1.903-beta" class="button primary">Full Release notes</a><a href="/docs/models/embeddinggemma-2.md" class="button secondary">EmbeddingGemma 2</a>
{% endupdate %}

{% update date="2026-10-01" tags="new-releases" %}

## Command Palette + Desktop UI/UX

This release makes Unsloth Desktop faster and easier to use with improved navigation, shareable run settings, clearer errors, faster Laya decisions, expanded Decision API support, and better 4-bit LoRA training.

* **Cmd/Ctrl+P command palette** and shareable GGUF run settings.
* [**Laya decisions**](#laya-decision-models--library) **up to 4.1x faster** with hosted provider support.
* **Clearer errors** with improved load/generation messages and logs.
* **Lower-memory 4-bit LoRA training** for NVFP4, INT4, and MXFP4 checkpoints.

#### Desktop, chat, and models

* Share GGUF run settings without loading models.
* Continue responses and fix HTML canvas errors directly in chat.
* Improved model fit warnings, image loading, and desktop controls.
* Added `FastModel` fine-tuning support for T5, T5Gemma, BART, Marian, and more.
* Added `unsloth eval` for evaluating checkpoints and LoRA adapters.
* Improved multi-GPU training and generation support.

#### 4-bit checkpoint training

Pre-quantized checkpoints now train using their original packed weights, reducing memory use while preserving accuracy.

* Qwen3.8-27B-NVFP4 uses 40.2 GB peak memory instead of 72.9 GB.
* INT4 checkpoints stay packed instead of being re-quantized.
* Kimi-K2.7-Code and gpt-oss retain packed experts during LoRA training.

#### Decision API, image, and platform updates

* Laya decision models respond up to 4.1x faster, with hosted providers available through Connections.
* Image models preserve INT8/FP8 during offloading for faster generation.
* Qwen-Image-2.1 renders 1536×1536 images up to 3.6x faster on Radeon 8060S.
* Added AMD Windows support for RX 5000–9000 GPUs.
* Updated MLX support and Mac LoRA exports to PEFT or GGUF.

<a href="https://github.com/unslothai/unsloth/releases/tag/v0.1.902-beta" class="button primary">Full Release notes</a><a href="/docs/models/decision-laya.md" class="button secondary">Laya Decision Models Guide</a>
{% endupdate %}

{% update date="2026-09-28" tags="new-releases" %}

## Laya Decision Models + Library

We're adding support for decision models, a unified Library for docs and media, document viewer, many Apple Silicon improvements, creation of Skills, and \~4.5× faster image and video generation.

* Run and serve **Decision Models** like Laya (open-source Jev) locally through a TypeSafe-compatible API.
* **Skills Editor** to create, edit, and delete Skills directly in Desktop.
* **ModelScope** model downloading is now available for users who can't use Hugging Face
* **Document Viewer** for PDF, Word, Excel, PowerPoint, and chats.
* New **Library**: Manage chats, images, videos, and files from the new **Library** tab.
* **Apple Silicon Improvements** including batched serving, structured outputs, and TurboQuant KV cache.
* Configure how much of a model each GPU receives.
* **Faster Image + Video Generation** with \~4.5x faster LTX-2.3 clips and 1.7–6.3x faster VAE decoding.

<a href="https://github.com/unslothai/unsloth/releases/tag/v0.1.901-beta" class="button primary">Full Release notes</a><a href="/docs/models/decision-laya.md" class="button secondary">Laya Decision Models Guide</a>
{% endupdate %}

{% update date="2026-09-22" tags="new-releases" %}

## Qwen-Image-2.1 + Skills

You can now run Qwen-Image-2.1 locally with Unsloth! This release also includes custom Agent Skills, and easier chat/project management. It also brings 2x faster reasoning blocks (60 FPS vs 30 FPS), more reliable training, and improved Linux installs and updates.

<a href="/docs/models/qwen-image-2.1.md" class="button primary">Qwen-Image-1.2 Guide</a>

* **Qwen-Image-2.1 support:** Run Qwen-Image-2.1 locally with Unsloth for image generation.
* **Custom Agent Skills:** Add task-specific skills, reuse skills from Claude Code and `.agents` folders, and select them in chat with `@`.
* **Smoother chat experience:** Long reasoning blocks now render at 60 FPS, up from 30 FPS. Includes a redesigned thinking UI, smoother code streaming, and more reliable model loading and chat settings.
* **Easier chat and project management:** Drag chats to reorder, pin, or move them into projects across all platforms. Edit project names, instructions, and folders directly from the Projects page.
* **Better model and storage handling:** Vision models can see images returned by MCP tools. Reuse downloaded models without fetching duplicate copies, and inspect or clear caches from Settings.
* **More reliable training and exports:** Resume past training runs with accurate remaining-time estimates. Fixes improve Hugging Face dataset recipes, column mapping, and split/subset selection. Hub uploads exclude files left over from earlier exports.
* **Improved Linux and AMD support:** In-app updates for Debian installs, a native ARM64 installer for Ubuntu 24.04+, and a new AMD ROCm Docker image with Unsloth Studio and JupyterLab.
  {% endupdate %}

{% update date="2026-09-17" tags="new-releases" %}

## Docker + MultiUser + AMD Support

We're releasing our new updated Docker image along with multi-user accounts, RDNA1+2, FP8/INT8 diffusion support, ARM64 CUDA Windows support and many training, GRPO and inference improvements

#### Highlights:

* Updated Docker with NVIDIA and AMD support: [Guide](https://unsloth.ai/docs/get-started/install/docker)
* Multi-user accounts with isolation: **Settings > Accounts**
* INT8/FP8 image diffusion inference: 2x faster
* ARM64 Windows CUDA support for training and inference
* GRPO: Qwen3.5 and latest TRL/vLLM support
* AMD RDNA1 and RDNA2 support
* Better Windows NVIDIA GPU detection and recovery

#### Updated Docker image

* Updated CUDA image and Studio setup, removed bundled caches, and restored Unsloth’s training patches on GPU hosts.
* Studio data persists on a volume without pinning app code. Improved updates, generated passwords, configurable ports, and package preservation.
* Added an AMD ROCm image for supported Linux hosts.

#### Multi-user accounts

* Create accounts in **Settings > Accounts** with one-time setup codes and individual passwords.
* Accounts keep work separate while sharing a loaded model when settings match. Single-account behavior is unchanged.

#### Chat + reasoning

* Edit, reorder, and steer queued prompts, even while a local model loads.
* Added GGUF reasoning budgets, adjustable chat width, desktop scaling, and a compact composer.
* Improved long-reasoning responsiveness, chat-history preservation, and tool-generated file and image handling.

#### Hardware + inference

* MLX gains video input, optional MoE and decode optimizations, and more reliable multimodal chats.
* Improved GGUF memory estimates, DGX Spark handling, NVIDIA detection, NVLink checks, and user-selected GPU ordering.
* Added native Windows ARM64 desktop packaging, Qwen3.5 `fast_inference`, and Ascend NPU detection.

#### Research + API

* Deep Research better preserves unfinished reports, handles JSON output, and flags runs without evidence. Scanned PDF uploads gain a local OCR fallback.
* Improved provider reasoning controls, MCP compatibility, tool calling, and streamed error reporting.
* Added `/v1/chat/completions` video input and API access to installed Ollama models.

#### Training + installation

* Added Data Recipes dataset downloads and fixed 16-bit fine-tune exports, LoRA saves, and Push to Hub.
* Improved dataset handling, training memory estimates, and checkpoint saves on container shutdown. Core fixes cover normalization, RoPE, Q-GaLore, and distributed device selection.
* Improved Windows installs, GPU package repair, dependency caching, and verified offline installs.

#### Security + tool execution

* Strengthened credential protection and tool-call validation, with approval requests for file access outside the sandbox.
* Added preview OS-level tool sandboxing on supported Linux and macOS hosts. Network access remains unrestricted; automatic mode keeps existing safeguards when OS isolation is unavailable.

<a href="/docs/get-started/install/docker.md" class="button primary">Docker Guide</a>
{% endupdate %}

{% update date="2026-09-02" tags="new-releases" %}

## 2x Faster Qwen3.8-Flash + GLM-5.3

Run [**Qwen3.8-Flash-Next**](/docs/models/qwen3.8-next.md) and [**GLM-5.3-Flash**](/docs/models/glm-5.3-flash.md) up to **2× faster** with faster decoding and bonus MTP, now enabled by default. This release also includes **170+ improvements** across training, chat, hardware support, APIs, and performance.

* Faster Qwen and GLM generation with MTP, plus improved tool use and recommended Qwen settings.
* Much less laggy UI/UX for all chats especially on long conversations
* New support for **MiniMax-Music3, Higgs, and MOSS** audio models, including progress tracking and clip management.
* More reliable model loading across local servers and connected providers.
* Safer chat editing that preserves tool calls, replies, media, and conversation branches.
* Improved multi-GPU training, memory fitting, model placement, and GGUF exports.
* Stronger AMD/ROCm installation, detection, and GPU compatibility.
* More reliable MCP, Deep Research, OAuth, parallel tool calls, and agent workflows.
* New OpenAI-compatible APIs for **video, audio, and MLX-served models**.
* Improved desktop updates, LAN port controls, downloads, and GPU memory cleanup.

<a href="/docs/models/qwen3.8-next.md" class="button primary">Qwen3.8-Flash-Next</a><a href="/docs/models/glm-5.3-flash.md" class="button primary">GLM-5.3-Flash</a><a href="/docs/models/glm-5.3.md" class="button primary">GLM-5.3</a>
{% endupdate %}

{% update date="2026-08-27" tags="new-releases" %}

## Qwen3.8-Flash-Next + GLM-5.3

[Qwen3.8-Flash-Next](/docs/models/qwen3.8-next.md), [GLM-5.3-Flash](/docs/models/glm-5.3-flash.md) + [GLM-5.3](/docs/models/glm-5.3.md) can now run locally in Unsloth!

* Qwen3.8-Flash runs on 75GB RAM
* GLM-5.3-Flash runs on 102GB RAM + VRAM
* Up to 5x faster RAM offloading
* Repeated Auto Compaction now works reliably
* 100+ chat, reliability and performance improvements

<a href="/docs/models/qwen3.8-next.md" class="button primary">Qwen3.8-Flash-Next</a><a href="/docs/models/glm-5.3-flash.md" class="button primary">GLM-5.3-Flash</a><a href="/docs/models/glm-5.3.md" class="button primary">GLM-5.3</a>

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F1YneA51oWzaIiwep9H5I%2F1000024423.gif?alt=media&amp;token=40a169cc-12f1-403a-898c-b310f81ff52a" alt="" width="375"><figcaption></figcaption></figure></div>

#### Qwen3.8-Flash-Next

125B multimodal reasoning model and early preview of Qwen4's architecture.

* 1-bit Dynamic GGUF runs on 75GB RAM or unified memory
* Up to 262K context with text and images
* None, Low, Medium and Extra High reasoning modes
* Preserved Thinking improves consistency in long chats

#### GLM-5.3-Flash

320B multimodal model with 18B active parameters.

* 1-bit model runs on 102GB combined RAM + VRAM
* Up to 1M context for text, images and documents
* Low, High and Max reasoning modes
* Improved coding, agent and vision performance

#### Unsloth improvements

* Large GGUFs automatically split across GPU and system RAM
* See memory estimates before loading
* Chats recover after disconnects
* Better multi-image vision and MCP image support
* Export chats as JSONL
* Improved Auto Compaction controls
* Fixes for Linux, NVIDIA Wayland, AMD and Windows

To run or train the new models, you can download Unsloth Desktop:

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth Desktop</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)
  {% endupdate %}

{% update date="2026-08-20" tags="new-releases" %}

## Auto compaction + LAN Access

Thanks for the support for Qwen3.8-27B and Unsloth Desktop last week! For our [new `v0.1.801-beta` release](https://github.com/unslothai/unsloth/releases/tag/v0.1.801-beta), we merged 200+ PRs to introduce many new features, fixes including:

* **Auto Compaction (Experimental)** for longer chats beyond context limits
* [**Remote & LAN Access (Preview)**](/docs/basics/lan.md) for easy network access without Cloudflare links
* **Faster Chat** - Improved streaming performance, reduced UI lag, and smoother long conversations.
* Support for **custom llama.cpp builds**. Toggles for Cache RAM, Mmap, Mlock, Checkpoints, Spe Decoding KV Cache, Vision On / Off
* [Unsloth Dynamic v3.0](https://unsloth.ai/docs/basics/dynamic-3.0-ggufs) is released. New Qwen3.8-27B Dynamic v3.0 GGUFs deliver >10% higher top-1 accuracy compared to everyone else. Works with Unsloth.

#### Auto compaction (Experimental)

Long chats can now exceed context limits by moving older turns into a searchable archive.

* Older turns are removed only when needed and remain searchable.
* Fresh context epochs improve recall without permanently trimming chats.
* Uses retrieval instead of summarization for better accuracy.

#### Remote & LAN access (Preview)

Access Unsloth from other devices on your network.

* New remote access settings.
* LAN control, QR codes, and auto-start options.
* Disabled by default for security.

#### Chat improvements

* Faster long chats and improved threading.
* Projects organize chats, files, and workspaces.
* Added prompt queueing, shortcuts, `edit_file`, and better tool support.

#### Hardware, inference, API

* Support for custom llama.cpp builds and Intel XPU.
* More inference controls (cache, mmap, mlock, checkpoints, speculative decoding, vision).
* Improved GPU validation, VRAM handling, and compatibility.
* Structured outputs in Responses API.
* Better llama-server recovery.

To run or train Qwen3.8, you can download Unsloth Desktop:

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth Desktop</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)
  {% endupdate %}

{% update date="2026-08-14" tags="new-releases" %}

## Qwen3.8

Qwen3.8-27B and Qwen3.8-2.4T can now be run locally in Unsloth!

Run on 17GB RAM via Unsloth Dynamic GGUFs. You can also fine-tune Qwen3.8-27B in Unsloth. Qwen3.8-27B is by far the strongest model for its size. We also uploaded NVFP4 quants.

<a href="/docs/models/qwen3.8.md" class="button primary">Run Qwen3.8 Guide</a><a href="/docs/models/muse-glimmer/train.md" class="button secondary">Fine-tune Muse Glimmer</a>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FSqxs6NjShWrLfRKhDy1m%2Fvolcano%202.gif?alt=media&amp;token=395274a0-b437-403a-8a01-8e8502f9d225" alt="" width="375"><figcaption></figcaption></figure>

Other Unsloth updates include:

* Qwen3.8-27B + extra llama-server arguments allowed + custom VRAM toggle
* External provider has tool calling + tool support + login with Codex
* Fast FP8 10x faster MiniMax-H3 inference (3 minutes vs 30)
* 10% faster inference for GGUFs + Bypass permissions fixed
* Connected [API providers](/docs/integrations/connections.md) can use their own Search or Unsloth Desktop's built-in Search and tools. Tool results are passed back to the model so it can continue multi-step tasks.
* Sign in with a Codex subscription and use Codex tools inside Chat.

To run or train Qwen3.8, you can download Unsloth Desktop:

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth Desktop</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)
  {% endupdate %}

{% update date="2026-08-11" tags="new-releases" %}

## Introducing Unsloth Desktop

Introducing Unsloth Desktop 🦥 - the first desktop app to run and train models locally.\
Open-source. Runs on Mac, Windows and Linux

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FyUdniXManojk20Q3M5Lf%2Fintroducing%20unsloth%20desktop%20thumb.png?alt=media&amp;token=5ecd2f25-b996-4749-8242-ffd21b080ae7" alt=""><figcaption></figcaption></figure>

• Supports MLX, diffusion image/video, audio, GGUF\
• Connect Claude Code and Codex to local LLMs\
• 50% more accurate, self-healing tool calls + sandboxed code exec\
• Works for CPU + multiGPU setups - NVIDIA, AMD, Intel, Mac\
• Train models 2× faster with 70% less VRAM\
• Private web search, deep research, RAG, MCP + exports (NVFP4, GGUF)\
• Use Unsloth’s OpenAI-compatible API and cloud models\
• Securely deploy LLMs remotely and access anywhere

You can download Unsloth Desktop now:

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth Desktop</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)
  {% endupdate %}

{% update date="2026-08-10" tags="new-releases" %}

## Meta Muse Glimmer is here!

Meta has released Muse Glimmer, the first open model from Meta Superintelligence Labs. Muse Glimmer is a dense, 30B parameter model by Meta, built for local agentic and coding workflows. Released under the Apache 2.0 license you can run Muse Glimmer 30B via Unsloth and Unsloth Dynamic quants for the best performance.

<a href="/docs/models/muse-glimmer.md" class="button primary">Run Muse Glimmer</a><a href="/docs/models/muse-glimmer/train.md" class="button secondary">Fine-tune Muse Glimmer</a>

Muse Glimmer 30B can run locally on **20GB RAM/VRAM** setups, including Mac and GPUs. You can also train and fine-tune Muse Glimmer 30B using Unsloth on **20GB VRAM**.

You can run and fine-tune Muse Glimmer via Unsloth Desktop app:

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth Desktop</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)
  {% endupdate %}

{% update date="2026-07-29" tags="new-releases,v0.1.51-beta" %}

## Kimi K3 + Deep Research + Parallel Chat

Hey everyone! [Kimi K3](/docs/models/kimi-k3.md) can now run locally with Unsloth Dynamic GGUFs, Unsloth can keep multiple chats generating in parallel, and the new Deep Research mode plans, reads and cites sources using your local model.

This release also brings better [AMD](/docs/basics/amd.md) and Intel GPU support, DoRA training, and many installer, MLX, export and inference fixes.

#### Kimi K3

Moonshot AI’s **Kimi K3** is a 2.8T-parameter MoE model with 104B active parameters, native vision support and a 1M context window. Kimi K3 is thinking-only and Unsloth supports low, high and max reasoning efforts.

You can run our [Kimi K3 Dynamic GGUFs](https://huggingface.co/unsloth/Kimi-K3-GGUF) through Unsloth. Unsloth automatically detects multi-GPU setups and can offload model layers to system memory.

Kimi K3 is a very large model, so plan your hardware accordingly:

* `UD-IQ1_S` is 595GB in disk space.
* `UD-Q4_K_XL` is 1.51TB in disk space.
* For lossless inference, use `UD-Q8_K_XL`, which is 1.56TB in disk space.

Read our full [Kimi K3 guide](https://unsloth.ai/docs/models/kimi-k3) and learn more about [Unsloth Dynamic 2.0 GGUFs](https://unsloth.ai/docs/basics/unsloth-dynamic-2.0-ggufs).

#### Parallel Chat

Unsloth can now run multiple conversations at once. Starting a **New Chat** leaves the previous answer generating, and each active conversation gets its own progress indicator and Stop control.

* 4 llama-server slots by default, adjustable in the web UI.
* Tools, uploads, self-healing and agents stay isolated between chats.
* Stop one chat without interrupting others or restarting the server.
* Unsloth reduces the slot count when memory is limited.
* Reloading the model still stops active chats after confirmation.

#### Deep Research

Deep Research turns a local model into a complete research workflow. Give it a question and it will create a plan, search the web, organize the evidence and produce a cited report.

* Review and edit the plan before research begins.
* Follow its progress and collected sources while it works.
* Resume or cancel without losing completed research.
* Allow or block websites to control source selection.
* Sources and citations stay saved with each run.
* Before writing, Unsloth checks for unsupported claims, contradictions and unresolved gaps. Recommendations without direct evidence are marked as testable inferences.

One run can be active per chat. Deep Research currently works with local models. Optional full-page grounding can read top search results into temporary RAG before synthesis; enable it with `UNSLOTH_RESEARCH_AUTO_SCRAPE=1`. It remains off by default because it adds scraping time and needs additional context.

#### Improved AMD Support

This update builds on our initial [AMD release and setup guide](https://unsloth.ai/docs/basics/amd) with support for more GPUs and more reliable ROCm inference and training.

* Improved detection for RDNA2, Radeon, Ryzen, Strix Halo and workstation GPUs.
* MI50 and Radeon VII support 16-bit LoRA and full fine-tuning on Linux.
* Fixed 4-bit NaNs, library conflicts and long RDNA startup stalls.
* Unsupported Windows HIP GPUs can fall back to Vulkan.
* Vulkan devices show their real names and can be selected individually.
* Clean Windows installs no longer require Winget or developer tools.

#### Training, Models and Platform Updates

* Intel XPU enables local chat and training on Intel Arc and Data Center GPUs.
* DoRA is available alongside LoRA and full fine-tuning.
* Large exports can use all visible GPUs to avoid GPU 0 memory limits.
* MLX adds streaming datasets, continued pretraining, callbacks and better VLM and LoRA support.
* Fixed incorrect `flash_attention_2` model output.
* Unsloth and saving utilities now work without bitsandbytes.
* Fixed `.json` datasets and Qwen3.5/3.6 MoE and GRPO notebook setup.
* Hub download folders are easier to find and open.
* Release notes are available in the Unsloth update popup.
* `unsloth start --as-subagent` lets Codex, Claude Code and Pi delegate tasks to a local Unsloth model.
  {% endupdate %}

{% update date="2026-07-20" tags="new-releases,v0.1.50-beta" %}

## AMD support is here!

Hey everyone! This release brings local LLM training and inference to [AMD GPUs](/docs/basics/amd.md) across Windows, WSL and Linux.

<a href="/docs/basics/amd.md#installing-unsloth-on-amd" class="button primary" data-icon="bolt">Quickstart</a><a href="/docs/basics/amd.md#id-2x-faster-training-and-50-more-accurate-tool-calls" class="button secondary" data-icon="star">Features</a><a href="https://github.com/unslothai/unsloth" class="button secondary" data-icon="github">Github</a>

Starting today, our AMD collaboration, custom Triton kernels, and math algorithms enables you to train and run 500+ models across AMD's Radeon, Instinct, Vulkan, Ryzen and data center GPUs, up to 2× faster with 70% less VRAM and no accuracy loss. Optimized ROCm builds also support GGUF & Safetensors inference.

<img src="https://github.com/user-attachments/assets/bb8bc525-9fb8-405d-98f5-6c9c07128085" alt="" width="375">

#### July 23 Update

1. Added **RDNA2, Gorgon Halo, Vulkan support** + fixed AMD installing not detecting GPUs on Strix Halo / other AMD GPUs
2. Better RDNA4, HIP / ROCm failure auto fixing and catching
3. **2x faster unified memory** AMD safetensors loading + much faster gradient checkpointing for unified memory devices
4. Added **voice dictation / whisper.cpp** preliminary support for fast text to speech
5. Fixed rollback environments during installs eating 5GB of disk space - now auto cleans

#### Train LLMs Locally on AMD

* Train, run RL, chat with and deploy models locally on AMD GPUs.
* More reliable AMD GPU detection and installation across Windows, WSL and Linux.
* Improved ROCm compatibility for AMD MI300X and MI325X GPUs.
* Remote access Unsloth via `unsloth studio --secure` through free HTTPS via Cloudflare

#### Run Larger Models on Your Hardware

* Use automatic GPU placement or choose exactly which GPUs and model layers to use.
* Move MoE expert layers into system memory to help larger models fit.
* Split models across multiple GPUs or use Tensor Parallelism.
* Save hardware settings separately for each model and quant.

#### Faster Chat Restarts and More Reliable Downloads

* Resume long chats without rebuilding the full conversation after an idle model frees its VRAM.
* Stalled Hugging Face XET downloads automatically retry over standard HTTP.
* Existing GGUF files are reused instead of being downloaded again whenever a model loads.

#### Better Search, Tools and Agents

* Web search can now read PDF papers, manuals and other PDF results.
* Parallel tool calls, reasoning output and tool retries work more reliably.
* A new opt-in MCP endpoint lets compatible AI clients inspect models and training history, start or stop training, load checkpoints, validate recipes and export GGUFs.
  * Enable it with `UNSLOTH_STUDIO_ENABLE_MCP=1` and set the required bearer token with `UNSLOTH_STUDIO_MCP_TOKEN`.

#### Training and Export Fixes

* Text-only training with multimodal models no longer truncates long examples before packing.
* Fine-tuned Qwen3.5 and Qwen3.6 MTP models now export correctly to GGUF.
* Fixed a Windows permission error that could stop GGUF exports during the final write step.

#### In Case You Missed It

Our previous Studio release added Dynamic NVFP4 models, deeper personalization, seven new display languages, safer agents and Vulkan GPU acceleration.

**Dynamic NVFP4:**

Unsloth Dynamic NVFP4 keeps accuracy-sensitive layers in FP8 or BF16 while running the rest in W4A4. On NVIDIA Blackwell GPUs, this enables up to 2.5x faster inference, while calibrated FP8 KV caches provide up to 2x longer context.

Read the [Dynamic NVFP4 guide](https://unsloth.ai/docs/basics/nvfp4) and explore our expanded [NVFP4 collection](https://huggingface.co/collections/unsloth/nvfp4), including Qwen3.6, Qwen3.5, Inkling, GLM-4.7 Flash and Gemma 4.

**Personalize Your Studio:**

Choose between Standard, Classic and Minimal color palettes, each with light and dark modes. You can also customize colors, import fonts and adjust font size, contrast, reduced motion and more.

Unsloth also includes a Voice settings tab for dictation, custom dictionary settings and read-aloud.

**New Languages:**

Unsloth Studio is now available in French, German, Spanish, Hindi, Arabic, Russian and Korean, alongside Chinese (Simplified), Japanese and Portuguese (Brazil). Browser-language auto-detection is now the default.

**Safer Agents:**

A four-level tool-call permission selector-**Ask**, **Approve for me**, **Off** and **Full access**-provides finer control over agents. Agent workspace isolation and safer installer checks also reduce the risk of unintended changes.
{% endupdate %}

{% update date="2026-07-15" tags="new-releases,v0.1.49-beta" %}

## Personalization, NVFP4, languages

Hey guys we got lots of new update for Unsloth, especially customization. Unsloth now yours to personalize: three color palettes plus custom colors and fonts, seven new display languages, and a new Voice settings tab for dictation and read-aloud. Agents get safer with a four-level tool-call permission selector (Ask, Approve for me, Off, Full access) and workspace isolation, and Intel GPUs finally get GPU-accelerated inference through new Vulkan `llama.cpp` support.

We’ve also added native support for [Inkling](https://unsloth.ai/docs/models/inkling), a 975B-parameter open model with 41B active parameters and up to a 1M-token context window. Licensed under Apache 2.0, it accepts text, images, and audio and generates text.

#### Dynamic NVFP4

We expanded our [NVFP4 collection](https://huggingface.co/collections/unsloth/nvfp4) with quantized versions of Qwen3.6, Qwen3.5, Inkling, GLM-4.7 Flash, and Gemma 4.

Read the [Dynamic NVFP4 guide](https://unsloth.ai/docs/basics/nvfp4) for details.

Personalize Your Unsloth

Unsloth is no longer limited to light and dark mode:

* Choose from **Standard**, **Classic**, and **Minimal** palettes, each with light and dark variants.
* Customize accent, background, and foreground colors.
* Import your own UI, heading, chat, and code fonts.
* Adjust font size, contrast, motion, cursor behavior, and font smoothing.
* Search settings and sync preferences across devices.

Light and dark modes keep their own customization values.

#### Seven New Languages

Unsloth now supports French, German, Spanish, Hindi, Arabic, Russian, and Korean, alongside Chinese, Japanese, and Portuguese. Browser-language auto-detection is now the default.

#### Voice Settings

A new Voice tab adds controls for dictation, pronunciation dictionaries, and read-aloud. Speech-to-text and text-to-speech support are coming soon; full voice conversations are still in development.

#### Safer Agents and Tool Calls

The old bypass toggle is now a four-level permission selector:

* **Ask:** approve every tool call.
* **Approve for me:** automatically run read-only actions and pause for potentially unsafe ones.
* **Off:** disable tool calls.
* **Full access:** allow all calls and disable the sandbox.

These controls cover terminal, Python, web search, RAG, and MCP tools. Agents also gain isolated workspaces, resumable sessions with `--persist`, safer remote-installer warnings, live tool-output streaming, and improved web extraction.

#### Vulkan and `llama.cpp`

The new Vulkan `llama.cpp` backend gives Intel GPUs GPU-accelerated inference instead of falling back to the CPU. It supports existing VRAM management, automatic context sizing, multi-GPU selection, and layer offloading.

AMD users can opt in with:

```bash
UNSLOTH_FORCE_VULKAN=1
```

We also improved update reliability, model-state recovery, and interruption of stalled generations.

#### Models and Training

This release also includes:

* Native Inkling support and multi-GPU B200 improvements.
* DeepSeek-V4 eager attention and trainable FP8 grouped experts.
* Reliable completion-only training through automatic chat-template marker detection.
* Correct handling of disabled gradient checkpointing.
* Improved RoPE scaling and context extension.
* Force-stopping for stuck training runs.
* Automatic routing for new model architectures and newer Transformers releases.
  {% endupdate %}

{% update date="2026-07-07" tags="new-releases,v0.1.48-beta" %}

## DeepSeek-V4 + NVFP4

Unsloth can now export NVFP4, FP8, and imatrix GGUFs after training; act as a llama-swap API system; add Japanese and Brazilian Portuguese support; and includes MLX, safetensors, tool calling, healing support, and more. Unsloth core makes GRPO 1.3x faster, adds HTTP fallback for stalled downloads, improves offline mode, speeds up MoE training by 3-5x, and fixes many bugs. This release series uses `unsloth>=2026.7.1`.

[DeepSeek-V4-Flash](/docs/models/deepseek-v4.md) is now supported with Thinking toggles and our improved chat template fixes.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FChQx2DGoDLyhf7mp8G2d%2Fdeepseek%20v4%20flashhh.png?alt=media&amp;token=a84f2fbc-8ab0-44cf-a3a8-0bdaaf80a2a7" alt="" width="375"><figcaption></figcaption></figure></div>

#### Smarter OpenAI-Compatible API Serving

Run one local API endpoint with safer model swapping and better agent-tool recovery.

* API requests can opt into automatic switching between downloaded local GGUFs, while unknown model names safely keep using the current model.
* `/v1/models` now returns clean model IDs and the local GGUF catalog instead of local `.gguf` paths.
* Idle auto-unload can free VRAM after inactivity, and tool-call healing can now be controlled per request.

#### Export Improvements

Exports are more flexible and avoid unnecessary downloads.

* Select multiple export formats at once, including portable FP8/INT8, GGUF LoRA, source-matched exports, imatrix GGUF, and compressed FP8/FP4.
* Multi-checkpoint exports avoid more repeated base-model downloads.
* FP8, INT8, and GGUF-LoRA exports now respect `trust_remote_code`, and GGUF export handles missing quantization settings more reliably.

#### RAG and File Chat

File chat is more useful on real documents.

* RAG attachments can now use whole-document context, with customizable embedding models and Hugging Face search.
* File chat reads more PDFs and Word documents correctly, including right-to-left text, Indic text, and DOCX tables.
* Local RAG checks are more reliable behind proxy setups.

#### Unsloth Polish and Reliability

Everyday use should feel smoother and more stable.

* Long training and chat runs are less likely to freeze silently.
* Compare mode, model switching, model cancellation, Hub browsing, and Hub Discover are more reliable.
* Project exports, chat exports, settings, guided tours, file dialogs, update screens, and reasoning UI are cleaner and more consistent.

#### Installer, Hardware, and Platform Fixes

Unsloth installs and runs more reliably across platforms.

* macOS installs no longer require CMake or Homebrew when a prebuilt `llama.cpp` is available, and Apple Silicon support handles paths with spaces and unified memory sizing better.
* Windows startup, UTF-8 handling, ROCm RAG embedding, and ROCm-on-WSL GPU support were improved.
* Blackwell GPU prebuilt selection, GGUF fit checks, tensor parallelism for vision/mmproj GGUFs, and local `llama.cpp` reuse are now more reliable.

#### Training, Models, and Kernels

Training and model loading are more reliable across more setups.

* GRPO now supports sequence packing by default, avoids repeated shared prompts, and handles DDP logit scaling correctly.
* Full fine-tuning, RL precision settings, gradient checkpointing, DDP RoPE buffers, and MoE LoRA detection were fixed.
* FP8 quantization/dequantization, Llama 3 RoPE scaling with Transformers v5, PEFT 0.19 LoRA reloads, and `fast_generate` error messages were improved.
  {% endupdate %}

{% update date="2026-06-18" tags="new-releases,v0.1.47-beta" %}

## GLM 5.2 + Hub + 3x longer contexts

[GLM-5.2](/docs/models/glm-5.2.md) is now supported in Unsloth Studio! All reasoning levels supported. **3x longer context lengths** are now achievable with our new auto fit algorithm with MTP, allowing longer chats. Bypass permissions mode, forkable chats, queue-able chats, a new hub for model discovery, parallel modules + HTTPS Cloudflare support and more! Use `unsloth studio --secure` for secure HTTPS global access!

<div data-with-frame="true"><img src="https://github.com/user-attachments/assets/93c18616-415f-48ea-957d-9e0fa97a45dd" alt="" width="563"></div>

#### Better context length algorithm

As per [PR 1](https://github.com/unslothai/unsloth/pull/6312) and [PR 2](https://github.com/unslothai/unsloth/pull/6447), we made Unsloth Studio's determination of memory usage and context length much better, achieving 3x longer context overall:

| Scenario                        | KV    | before  | after   |
| ------------------------------- | ----- | ------- | ------- |
| 1x 32GB pipeline (\~31 GB free) | f16   | 23,040  | 64,000  |
|                                 | q8\_0 | 43,520  | 114,944 |
|                                 | q4\_0 | 82,432  | 199,680 |
| 2x 32GB pipeline                | any   | 262,144 | 262,144 |
| 2x 24GB tensor (\~23 GB free)   | f16   | 134,049 | 262,144 |
|                                 | q8\_0 | 252,329 | 262,144 |

#### Chat Canvas, Forking & Queueing

* Edit assistant messages in place and re-run from any point in the thread.
* Fork a thread to branch a conversation without losing the original.
* Temporary (incognito) chats that leave nothing behind.
* Queue new prompts while a generation is still running instead of waiting.
* Chat "artifacts" are now **canvas**, with inline **HTML canvas cards** that auto-render, a Code view, and DiffusionGemma keeps its raw code visible inline instead of collapsing.
* Chat search now covers every message and surfaces your own messages first.

#### Hub (Redesigned)

* Full-page Hub with a trending feed, search, and custom model paths support.
* README preview in a split-view feed so you can read before you download.
* Downloads default to the faster **Xet** transport, with automatic HTTP fallback if a transfer stalls.
* New "Load on selection" toggle to set load options before a model loads.
* Google logo shown for DiffusionGemma and future Gemma derivatives.

#### Models & Inference

* DeepSeek-OCR and more vision models now load and run without errors.
* Fixed fast inference on the latest vLLM (0.22+) so speed-ups work again.
* Tensor parallelism is more reliable: if the faster MTP path fails, it now recovers on its own instead of crashing.
* DiffusionGemma now shows the image forming live as it denoises, with accurate speed stats.

#### Security & Cloudflare Encrypted Studios

* New `--secure` Cloudflare-only mode for end-to-end encrypted studios, with server-side tools staying enabled under `--secure`. Use `unsloth studio --secure`!
* Bypass Permissions mode to skip confirmations and disable the tool sandbox when you want it.
* Auto detect Hugging Face Virus scanning + dangerous files in repos.

#### Logging and API

* New **API server monitor** in Unsloth.
* Faster API calling and less latency
* Much better streamlined logs - now with throughput and latency and removed a lot of bloated logs.

#### Hardware & Backend

* Better support for Blackwell RTX 50X and 60X GPUs
* Fix silent downgrading to CPU and not GPU
* torchao version is now selected from the installed torch.
* Installer now auto-repairs a broken or CPU-only PyTorch install and warns on silent CPU fallback, across NVIDIA + AMD on Win/Linux/Mac/WSL.
* Frees the chat model's VRAM when training starts, but only when the GPU is actually tight (no needless reloads otherwise).
* If llama-server hard-crashes at startup, Unsloth now steps through a recovery ladder instead of just failing.

#### Training & General Fixes & Parallel Modules

* MLX training updates.
* Improved GRPO training reliability with vLLM.
* Training startup made more reliable, with clearer errors for invalid VLM batches.
* Unsloth now cleans up leftover backend processes more reliably after crashes, restarts, or interrupted shutdowns.
* Export, Chat, Training, Recipes are all individualized / compartmentalized! This means you can do all 4 in parallel now! You can chat / do inference while you wait for a training run or an export!

To update Unsloth or install a new Unsloth Studio, you must use:

**macOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

{% endupdate %}

{% update date="2026-06-12" tags="new-releases,v0.1464-beta" %}

## DiffusionGemma + Gemma 4 MTP

Ensure you install the latest [`v0.1.464-beta`](https://github.com/unslothai/unsloth/tree/v0.1.462-beta) or `2026.6.7`. [DiffusionGemma](https://unsloth.ai/docs/models/diffusiongemma), [Gemma 4 MTP](https://unsloth.ai/docs/models/mtp) and [**MiniMax-M3**](https://unsloth.ai/docs/models/minimax-m3) are all now supported.

* Run and train [DiffusionGemma](https://unsloth.ai/docs/models/diffusiongemma) via [Unsloth Studio](https://unsloth.ai/docs/new/studio).
* [Gemma 4 MTP](https://unsloth.ai/docs/models/mtp) is here! Run [Gemma 4](https://unsloth.ai/docs/models/gemma-4) \~2x faster with MTP.
* Audio chat is now supported for Gemma 4 (`wav`, `mp3`, `m4a`, `flac`, `webm`).
* Preserve Think added to Gemma 4.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fszoidwwj70dLm5vBjpmL%2Fdiffusiongemma.gif?alt=media&amp;token=8ce359fd-f92c-4cf8-a491-06b04c505cb7" alt="" width="375"><figcaption></figcaption></figure>

#### Hub + Download Manager (Experimental)

* Added a new **Hub** page for browsing, downloading, and managing Hugging Face models and datasets.
* Unsloth can now detect models and datasets already on your machine and show them alongside downloaded assets.
* Downloaded [GGUF models](https://unsloth.ai/docs/basics/inference-and-deployment/saving-to-gguf) now have direct **Run / New Chat** actions.

#### RAG / Chat with Files (Experimental)

* Added [**Chat with Files**](https://unsloth.ai/docs/new/studio/chat) in Unsloth, letting you ask questions over your own documents and knowledge bases.
* Supports hybrid search, citations, PDF previews, per-thread documents, and a built-in `search_knowledge_base` tool.

#### New Update Button + Hardware Support

* Unsloth now uses constant fresh up to date [llama.cpp prebuilts](https://unsloth.ai/docs/new/changelog) across CUDA, ROCm, Windows, Linux, and macOS.
* Added an in-app **Update llama.cpp** button so users can update the local backend without reinstalling Unsloth.
* Improved Windows / WSL AMD support, [Strix Halo ROCm support](https://unsloth.ai/docs/get-started/install/amd), [Blackwell CUDA selection](https://unsloth.ai/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth), and clearer installer messages.

#### Local Chat, Tools & API Compatibility

* Local [tool calling](https://unsloth.ai/docs/basics/tool-calling-guide-for-local-llms) is more reliable, with better ordering of tool cards, fewer duplicate tool loops, and support for tool use with GGUF vision models.
* Improved [OpenAI-compatible API](https://unsloth.ai/docs/basics/inference-and-deployment/llama-server-and-openai-endpoint) and Anthropic-compatible API behavior for local Unsloth servers, including better errors, token usage, stop reasons, and [Claude Code compatibility](https://unsloth.ai/docs/basics/claude-code).

#### Training & Fixes

* Improved [MLX support](https://unsloth.ai/docs/new/studio/install) with better model labels, generation speed stats, and fixes for [VLM training](https://unsloth.ai/docs/basics/vision-fine-tuning).
* Fixed several [training](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide) and [dataset](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/datasets-guide) edge cases, including non-writable Hugging Face caches and custom dataset mappings.
* Added many UI polish fixes across chat, menus, model picker, dark mode, import/export, and settings.

To update Unsloth or install a new Unsloth Studio, you must use:

**macOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

{% endupdate %}

{% update date="2026-06-03" tags="new-releases,v0.1.44-beta" %}

## Gemma 4 12B, New UI, MCP, Projects

This update focuses mainly on Gemma 4 12B, MCP, Projects, Canvas, CUDA 13.3 and the new chat UI. Next week we'll have an even bigger update.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FoRn2YEPb9lJ81kP3GQQh%2Fwhats%20on%20ur%20mind.png?alt=media&amp;token=f388e42a-bb05-4a09-9cbf-ec699a6baf6b" alt="" width="375"><figcaption></figcaption></figure></div>

#### Gemma 4 12B

Google releases [Gemma 4 12B](https://unsloth.ai/docs/models/gemma-4), a new model that runs locally on 8GB RAM. [GGUF](https://huggingface.co/unsloth/gemma-4-12b-it-GGUF) / [Guide](https://unsloth.ai/docs/models/gemma-4)

Gemma 4 12B Unified supports image, audio and 256K context. Run and train the model via Unsloth Studio.

#### MCP

* Remote `MCP` server support, including custom headers and OAuth
* Local command-based `MCP` server support
* `MCP` can now be turned on from the chat composer
* Built-in presets for common `MCP` servers

#### New Chat UI

* Projects, Canvas, `MCP`, RAG and Compare controls now live in the plus menu
* Search and Code controls are easier to access from the composer
* Menus, overlays, icons and clickable controls are more consistent across Unsloth

#### Projects

* Organize related chats into dedicated project workspaces
* Move existing chats into projects
* Create and manage projects directly from the sidebar

#### Experimental Canvas / Artifacts

* Opens generated HTML in a dedicated canvas panel inside Unsloth Studio
* Supports interactive outputs, including browser based visualizations and CDN-loaded packages
* Lets you switch between rendered preview and source code

#### Install, Runtime and Hardware

* Windows prebuilt installs no longer require the early `CUDA Toolkit` check
* Linux `llama.cpp` prebuilts now match the detected runtime `cudart` major
* `ROCm` gfx detection is forwarded into prebuilt selection
* `Blackwell`, `B300` and `ARM64` Linux support updates

To update Unsloth or install a new Unsloth Studio, you must use:

**macOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

{% hint style="warning" %}
**DO NOT USE `unsloth studio update` anymore since packaging will not get the latest updates!**
{% endhint %}
{% endupdate %}

{% update date="2026-05-31" tags="new-releases,v0.1.43-beta" %}

## CUDA 13.3, Windows, Mac

**To update Unsloth or install a new Unsloth Studio, you must use:**

**macOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

{% hint style="warning" %}
**DO NOT USE `unsloth studio update` anymore since packaging will not get the latest updates!**
{% endhint %}

#### Mac Updates

* Re-enabled `llama.cpp` prebuilt binaries for Apple Silicon (M1-M4) - Mac OS 14 / 15 / 26 (Tahoe)
* Apple Silicon Mac OS 13 (Ventura) is source build
* Intel (x86\_64) for Mac OS 13.3 / 14 / 15 / 26 (Tahoe) uses `llama.cpp` prebuilt binaries
* Intel for Max 13.0 - 13.2 is source build

#### Windows Updates

* CUDA 13.3 `llama.cpp` prebuilt binaries now work for Windows
* For CUDA 13.2, CUDA 13.1 and below, Windows devices uses CUDA 12.4 fallback - we'll work on CUDA 13.1 binaries soon.

#### CUDA 13.3 Update

* CUDA 13.3 non Linux binaries work. We'll still use CUDA 13.1 for now
* CUDA 13.3 solves the CUDA 13.2 gibberish problem - see <https://github.com/unslothai/unsloth/issues/4849>

#### Blackwell GPUs Update

* For now Blackwell will have delayed releases of `llama.cpp` prebuilt binaries sine CUDA 12.4 does not work - we are working to resolve this soon.
  {% endupdate %}

{% update date="2026-05-26" tags="new-releases,v0.1.42-beta" %}

## An update before Revamp.

Hey guys, we're doing one more-ish update before a major revamp which is likely coming this week or next week. Our revamp will change a lot of things, especially with new major features and a lot of design changes.

{% embed url="<https://github.com/user-attachments/assets/70456395-e016-4273-8256-35adb206267e>" %}

* NEW: [**API calling support**](https://unsloth.ai/docs/integrations/connections) now with image generation + editing, proper web search, code execution, auto prompt caching. Connect [OpenAI](https://unsloth.ai/docs/integrations/connections/openai), [Anthropic](https://unsloth.ai/docs/integrations/connections/anthropic-claude) and more.
* Proper support for **non-English languages** e.g. Japanese, Chinese, Indian etc.

Many of you may have missed our previous release which only lasted for one day. We introduced:

* Connect to external inference backends: [vLLM](https://unsloth.ai/docs/integrations/connections/vllm), [Ollama](https://unsloth.ai/docs/integrations/connections/ollama), [llama-server](https://unsloth.ai/docs/integrations/connections/connect-llama.cpp-to-unsloth-run-ggufs-with-llama-server)
* **Security improvements**
* **Auto MTP speculative decoding** for MTP GGUFs; get the best settings customized for your hardware.

#### API provider calling & external connections

* You can now connect Unsloth to any API cloud provider (OpenAI, Anthropic, OpenRouter etc.)
* **Built-in web search** for OpenAI, Anthropic, OpenRouter and Kimi
* **Built-in code execution** for OpenAI and Anthropic (Anthropic containers persist and are reused across turns)
* Prompt caching is enabled for OpenAI and Anthropic models saving 50 to 90% of costs.
* Image generation + editing
* API key now optional for local providers (llama.cpp / vLLM / Ollama)
* Auto-load models when adding a cloud provider

#### Other Unsloth Studio updates

* OpenDocument chat attachments
* o3 reasoning summary payload
* Sending/prompting non-English languages (e.g. Japanese, Chinese) now works properly
* IME composer hardening, RTL `dir="auto"`, long log-line truncation fix
* Tool reasoning trace rendering in UI
* Fully offline support: cached GGUF discovery and offline DNS auto-detect for both inference and training

#### Unsloth Studio security improvements

* Authentication rate-limiting, proxy-aware so reverse proxies don't bypass it
* Sandboxed worker with a tightened blocklist (bash, `hf upload`, `NOFILE`)
* Path containment so workers can't escape their in-flight tmp dirs
* Strict schema validation across the Unsloth API
* Tightened CSP / security headers (only legitimate favicon hosts allowed)
* Removed the `torch.load` fallback on `training_args.bin` so untrusted pickles can never execute on model load
* Hardened Tauri desktop release flow
* Frontend auth: singleflight token refresh, current-password input on changes, working logout, shared 422 helper
* Cancel cleanup now scoped strictly to in-flight tmp dirs so it can never delete user state
  {% endupdate %}

{% update date="2026-05-19" tags="new-releases,v0.1.41-beta" %}

## MTP + Unsloth Fixes

Lots of bug fixes, UI, UX fixes to Unsloth! To get the latest updates do:

**macOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

#### Fixes

1. Fix `unsloth studio update` not working well
2. Fix getting stuck on `reset-password` page
3. More offline mode support
4. Improve MTP not being faster on Macs, CPUs and GPUs - now it's much better!
5. Fix Desktop Shortcut not working after update
6. Many many UI UX bug fixes
   {% endupdate %}

{% update date="2026-05-18" tags="new-releases,model-release,v0.1.405-beta" %}

## Qwen3.6 MTP + API Connections

We've got lots of new updates for Unsloth `v0.1.41-beta`:

* **\~2x faster GGUF inference** with automatically enabled [MTP](/docs/models/qwen3.6.md#mtp-guide)
* [**API calling support**](/docs/integrations/connections.md) for [OpenAI](/docs/integrations/connections/openai.md), [Anthropic](/docs/integrations/connections/anthropic-claude.md) etc. with auto prompt caching, web search, code execution
* Connect to external inference backends: [vLLM](/docs/integrations/connections/vllm.md), [Ollama](/docs/integrations/connections/ollama.md), [llama-server](/docs/integrations/connections/connect-llama.cpp-to-unsloth-run-ggufs-with-llama-server.md)
* Experimental **MLX inference**
* Proper support for **non-English languages**
* **Security** improvements

<a href="/pages/NpuhjPsxi8BKhuS8nnyY#qwen3.6-inference-tutorials" class="button primary">Run Qwen3.6 Tutorials</a><a href="/docs/models/qwen3.6.md#mtp-guide" class="button primary">MTP Guide</a>

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F0abq31rgj0gOSH9vnpQ6%2Fmtp.gif?alt=media&amp;token=c66ec3f5-91f0-4617-824c-c537a2dde8b0" alt="" width="375"><figcaption></figcaption></figure></div>

#### MTP speculative decoding support 1.4 to 2x faster inference!

* **Auto MTP speculative decoding** for MTP GGUFs; warn when the bundled llama.cpp prebuilt is stale or too old for MTP
* New pre-built llama.cpp binaries for MTP support!

#### API provider calling & external connections

* You can now connect Unsloth to any API cloud provider (OpenAI, Anthropic, OpenRouter etc.)
* **Built-in web search** for OpenAI, Anthropic, OpenRouter and Kimi
* **Built-in code execution** for OpenAI and Anthropic (Anthropic containers persist and are reused across turns)
* Prompt caching is enabled for OpenAI and Anthropic models saving 50 to 90% of costs.
* API key now optional for local providers (llama.cpp / vLLM / Ollama)
* Auto-load models when adding a cloud provider

#### MLX inference (Experimental)

* MLX quants and models now can run locally on your Mac machines!
* We'll be adding thinking, tools and web search soon!

#### Other Unsloth Studio updates

* Sending/prompting non-English languages (e.g. Japanese, Chinese) now works properly
* OpenDocument chat attachments
* o3 reasoning summary payload
* IME composer hardening, RTL `dir="auto"`, long log-line truncation fix
* Tool reasoning trace rendering in UI
* Fully offline support: cached GGUF discovery and offline DNS auto-detect for both inference and training
* Lots of UI/UX polish: dark theme refactor, right sidebar redesign, time-of-day sloth mascot, dismissable copyable toasts, larger chat composer, code-execution config polish, composer action pill styling, narrower Discord button

#### Training updates

* Gemma attention mask fixes
* Multi Image GRPO
* GRPO hidden-state return experiments
* New Continued Pretraining (CPT) training method as a first-class option
* Gemma-4 MoE LoRA extractor registered to fix `grouped_mm` contraction crash
* Opt-in fused `lm_head` + cross-entropy forward, with single-matmul path under `UNSLOTH_RETURN_LOGITS=1`
* Pass batch size for eval
* Eval/training paths now honour `HF_DATASETS_OFFLINE` alongside `HF_HUB_OFFLINE`

#### Unsloth Studio security improvements

* Authentication rate-limiting, proxy-aware so reverse proxies don't bypass it
* Sandboxed worker with a tightened blocklist (bash, `hf upload`, `NOFILE`)
* Path containment so workers can't escape their in-flight tmp dirs
* Strict schema validation across the Unsloth API
* Tightened CSP / security headers (only legitimate favicon hosts allowed)
* Removed the `torch.load` fallback on `training_args.bin` so untrusted pickles can never execute on model load
* Hardened Tauri desktop release flow
* Frontend auth: singleflight token refresh, current-password input on changes, working logout, shared 422 helper
* Cancel cleanup now scoped strictly to in-flight tmp dirs so it can never delete user state
  {% endupdate %}

{% update date="2026-05-05" tags="new-releases,v0.1.39-beta,v0.1.38-beta" %}

## Unsloth API endpoint

#### ***v0.1.39-beta bug fix*** **May 5th 2026**

Fixes chat history not being shown (existing chat history is not lost) and attachments not attaching correctly. The bug was render-only - use `2026.5.2` or directly call `curl -fsSL https://unsloth.ai/install.sh | sh`  to update

You can use local LLMs with tools like [Claude Code](https://unsloth.ai/docs/basics/claude-code) and [Codex](https://unsloth.ai/docs/basics/codex) by connecting them to Unsloth’s API endpoint. This lets you run models like [Qwen](https://unsloth.ai/docs/models/qwen3.6) and [Gemma](https://unsloth.ai/docs/models/gemma-4) locally, with additional features such as self-healing tool calling, code execution, and web search.

Using Unsloth as an API inference endpoint is beneficial not only because it is easy to setup and fast, but also because Unsloth provides:

* [Self-healing tool calling](https://unsloth.ai/docs/new/studio/chat#auto-healing-tool-calling), which helps reduce broken or malformed tool calls by 50%
* [Code execution](https://unsloth.ai/docs/new/studio/chat#code-execution) support, allowing Bash and Python execution for more accurate code outputs.
* Advanced [Web search](https://unsloth.ai/docs/new/studio/chat#advanced-web-search) that visits and actually reads webpages to gather in-depth info.
* [Automatic inference settings](https://unsloth.ai/docs/new/studio/chat#auto-parameter-tuning) for GGUF models (temp, top-k etc.)

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F1s98Id9xclzwMfxjXw2O%2Funsloth%20api%20cropped.png?alt=media&amp;token=64fac263-ca5b-4447-a740-41f58ec94904" alt="" width="375"><figcaption></figcaption></figure></div>

#### New models

We've also got a handful of new models to run including NVIDIA [Nemotron 3 Nano Omni](/docs/models/nemotron-3-nano-omni.md), IBM [Granite 4.1](/docs/models/ibm-granite-4.1.md) and [Mistral 3.5](/docs/models/mistral-3.5.md) Medium. We helped Mistral solve some issues with implementation in transformers and GGUFs.

#### Unsloth Updates

* Stopped Unsloth training runs can now resume from checkpoints.
* Chat threads now autosave and persist more reliably.
* DPO training hangs in multi-process setups were fixed.
* VLM GRPO support improved with MROPE updates.
* Unsloth’s stop button now properly stops generation.
* Fix chat template disappearing after browser refresh.
  {% endupdate %}

{% update date="2026-04-23" tags="new-releases,v0.1.37-beta" %}

## Brand New UI Redesign

Hey guys, we revamped the entire Unsloth Studio UI and UX experience to put an emphasis on chat and training:

* Added a collapsible sidebar based on community feedback

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FKoonE97b0H3RioMwVohd%2Fstudio%20new%20ui.gif?alt=media&amp;token=e37f2839-914e-48b8-8c81-2dac3ade9408" alt="" width="375"><figcaption></figcaption></figure></div>

* You can now delete chats and search past conversations

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fm6se3dOmBZH9d9Wlif4W%2FScreenshot%202026-04-23%20at%206.15.38%E2%80%AFAM.png?alt=media&amp;token=e83fe246-1f88-4bf7-aa15-baf7d3356676" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fa4EGTdaWQ6EA81PeC3JZ%2FScreenshot%202026-04-23%20at%206.01.36%E2%80%AFAM.png?alt=media&amp;token=1a1cc50d-e0e0-47cd-9c1a-80583a887794" alt=""><figcaption></figcaption></figure></div>

* New Preserve Thinking toggle for models that support it like Qwen3.6
* Cleaner, more consistent design with easier navigation
* Expanded Settings page with options to change your profile picture, name, and more

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FvMtRDH8cVXCu08OZ4TRf%2FScreenshot%202026-04-23%20at%206.18.35%E2%80%AFAM.png?alt=media&amp;token=d989c4b5-6293-402c-981c-3209b7e7d750" alt="" width="375"><figcaption></figcaption></figure></div>

* No more entering your Hugging Face token twice
* gpt-oss now has low, medium and high thinking toggles.
* Now uses latest llama.cpp prebuilt, even on Linux CUDA
* Lots of bug, consistency and stability fixes
* Kimi-K2.6 can now be run!
* We also added experimental API support. Guides, announcement etc will come next week.

Qwen3.6 was also also previously already supported in Unsloth Studio for running and training. You can train and run Qwen3.6-27B right now!
{% endupdate %}

{% update date="2026-04-22" tags="model-release,new-releases" %}

## **Qwen3.6-27B + Kimi K2.6**

[**Qwen3.6-27B**](/docs/models/qwen3.6.md) can now run (18GB RAM) and be fine-tuned in Unsloth Studio. Kimi K2.6 can also be ran in Unsloth (350GB RAM).

Unsloth Studio received many new updates so please update. Details and writeup coming in the next few days.
{% endupdate %}

{% update date="2026-04-16" tags="model-release,new-releases" %}

## **Qwen3.6**

[**Qwen3.6**](/docs/models/qwen3.6.md) can now run and be fine-tuned in Unsloth Studio. The model runs on 23GB RAM and is the strongest mid-sized LLM on nearly all benchmarks.
{% endupdate %}

{% update date="2026-04-11" tags="model-release" %}

## **Gemma 4 Update + MiniMax-M2.7**

[Gemma 4 GGUFs](https://huggingface.co/collections/unsloth/gemma-4) are now updated with Google's official chat template fixes (which fixed/improved tool-calling), along with the latest llama.cpp fixes. Update to the latest llama.cpp, re-download quants and you shouldn't see `unused token` issues anymore.\
\
[MiniMax-M2.7](/docs/models/tutorials/minimax-m27.md) is out now! You can run the model locally with our GGUFs in 4-bit quantization on 128GB RAM / unified memory. [**MiniMax-M2.7 GGUF**](https://huggingface.co/unsloth/MiniMax-M2.7-GGUF)
{% endupdate %}

{% update date="2026-04-08" tags="new-releases,v0.1.36-beta" %}

## **Gemma 4 Fixes**

We’ve updated Gemma 4 [with many fixes](/docs/models/gemma-4/train.md). These bugs are universal and affected all training packages and implementations and **did not originate from Unsloth**. We identified the bugs, fixed them, and Gemma 4 training now works properly in Unsloth.

You only need **8GB VRAM** to train **Gemma-4-E2B** locally. Unsloth trains Gemma 4 **\~1.5x faster while using \~60% less VRAM** than FA2 setups. For the full guide and notebooks on Gemma 4 training, [see our blog](/docs/models/gemma-4/train.md).

#### Gemma 4 Training Fixes

1. **Gradient accumulation** no longer causes loss explosions. Previously, losses could spike to **300–400**; expected loss is around **10–15**.
2. Fixed the **IndexError** affecting **26B** and **31B** inference in `transformers`.
3. Fixed gibberish outputs for **E2B/E4B** when `use_cache=False`. See [issue #45242](https://github.com/huggingface/transformers/issues/45242).
4. Fixed **float16 audio** overflow from `-1e9` values.

If you see losses above **13–15,** for example **100** or **300** - gradient accumulation is likely being handled incorrectly. This is fixed in both **Unsloth** and **Unsloth Studio**.

#### Gemma 4 Quant Re-uploads

We also updated our Gemma 4 GGUFs so you will need to re-download. Again, these quant issues are **not related to or caused by Unsloth**:

1. CUDA: check for buffer overlap before fusing - critical fix for `<unused24>` tokens - [PR #21566](https://github.com/ggml-org/llama.cpp/pull/21566)
2. `kv-cache`: support attention rotation for heterogeneous iSWA - [PR #21513](https://github.com/ggml-org/llama.cpp/pull/21513)
3. `vocab`: add byte token handling to BPE detokenizer for Gemma 4 - [PR #21488](https://github.com/ggml-org/llama.cpp/pull/21488)
4. `convert`: set `"add bos" == True` for Gemma 4 - [PR #21500](https://github.com/ggml-org/llama.cpp/pull/21500)
5. `common`: add Gemma 4 specialized parser - [PR #21418](https://github.com/ggml-org/llama.cpp/pull/21418)
6. `llama-model`: read `final_logit_softcapping` for Gemma 4 - [PR #21390](https://github.com/ggml-org/llama.cpp/pull/21390)
7. `llama`: add custom newline split for Gemma 4 - [PR #21406](https://github.com/ggml-org/llama.cpp/pull/21406)

#### Unsloth Studio Updates

* Add **speculative decoding** support (ngram-mod, on by default)
* Llama.cpp updated to use latest version with all Gemma 4 Fixes
* Fix Qwen3.5 and Gemma 4 training issues
* Enable exporting and saving of Gemma 4 models
* Harden sandbox security for terminal and python tools
* Let recipes use the model loaded in Chat
* Fix empty chat threads on navigation (and whenever switching tabs) and stabilize new chat flow
* Allow non-LLM recipes to run and move Data tab first in executions
* Reuse HF cached repo casing to prevent duplicate downloads
  {% endupdate %}

{% update date="2026-04-03" tags="new-releases,v0.1.36-beta" %}

## **Google - Gemma 4**

* You can now run and train the [Gemma 4](/docs/models/gemma-4.md) models in Unsloth.
* Intel Mac now works
* Pre-compiled binaries for llama.cpp for 2 Gemma-4 fixes:
  * vocab: fix Gemma4 tokenizer ([#21343](https://github.com/ggml-org/llama.cpp/pull/21343))
  * fix: gemma 4 template ([#21326](https://github.com/ggml-org/llama.cpp/pull/21326))
* Tool calls for smaller models are now more stable and don't cut off anymore
* Pre-compiled binaries for Windows, Linux, Mac, WSL devices - CPU and GPU
* Speculative Decoding added for non vision models (Gemma-4 is vision sadly and Qwen3.5)
* Context length is now properly applied.
* Web search now actually gets web content and not just summaries
* 90% reduced HF API calls - less rate limits
  {% endupdate %}

{% update date="2026-03-31" tags="new-releases,improvements" %}

## **+50% tool call accuracy + more support**

* Tool calls for all models are now **+30% to +80% more accurate.**
* Web search now actually gets web content and not just summaries
* Number of tool calls allowed are increased to 25 from 10
* Tool calls now terminate much better, so looping / repetitions will be reduced
* More **tool call healing** and de-duplication logic to stop tool callings from leaking XML as well
* Tested with `unsloth/Qwen3.5-4B-GGUF` (`UD-Q4_K_XL`), web search + code execution + thinking enabled.

| Metric                       | Before | After     |
| ---------------------------- | ------ | --------- |
| XML leaks in response        | 10/10  | 0/10      |
| URL fetches used             | 0      | 4/10 runs |
| Runs with correct song names | 0/10   | 2/10      |
| Avg tool calls               | 5.5    | 3.8       |
| Avg response time            | 12.3s  | 9.8s      |

#### New features

* Added **custom folders** so you can use any GGUFs in any folder - for now access in Advanced Settings in Chat and Custom Folders
* **Update button** now visible
* Install script styling all updated!
* Preliminary **Automatic Multi GPU support for inference and training** - useful for large models that don't fit on 1 GPU - Unsloth auto will allocate GPU resources
* Intel Macs should work out of the box

Much smoother and faster Unsloth

* **Fixed timeouts of downloads of large models** - no more timeouts seen.
* **Fixed Hugging Face rate limiting - HF API calls reduced by 90%**
* Fixed bun on Windows and faster installs
  {% endupdate %}

{% update date="2026-03-27" tags="new-releases,fixes,improvements" %}

## **New Important Updates**

It’s only been 2 days since our previous release, but we’ve got a more important updates:

* **Inference is now 20–30% faster.** Previously, tool-calling and repeat penalty could slow inference below normal speeds. Inference tokens/s should now perform the same as `llama-server` / `llama.cpp`.
* **Now Auto-detects older or pre-existing models** downloaded from **LM Studio, Hugging Face,** and similar sources.
* **Inference token/s speed is now calculated correctly.** Previously, tokens/s included startup time, which made the displayed speed look slower than it actually was. It should now reflect 'true' inference speed.
* **CPU usage no longer spikes.** Previously, inline querier identity changed every render, causing `useLiveQuery` to resubscribe continuously.
* **Unsloth Studio now has a shutdown x button and shuts down properly.** Previously, closing it after opening from the desktop icon would not close it properly. Now, launching from the shortcut also opens the terminal, and closing that terminal fully exits Unsloth Studio. If you still have it open from a previous session you can restart your computer or run `lsof -i :8888` then `kill -9 <PID>`.
* **Even better tool-calling and websearch** with reduced errors.
* Updated documentation with lots of new info on [deleting models, uninstalling](/docs/new/studio/install.md#uninstall) etc.
* **Cleaner, smarter install and setup logging across Windows and Linux.** Output is now easier to read with consistent formatting, quieter by default for a smoother experience, and supports richer `--verbose` diagnostics when you want full technical detail.
* You can now view your training history!
  {% endupdate %}

{% update date="2026-03-25" tags="new-releases,fixes,improvements" %}

## First Release post Unsloth Studio

Hey guys, this is our first release since we launched Unsloth Studio. Lots of new features and fixes:

* **You can now update Unsloth Studio!** Please update via the same install commands.
* **Windows** CPU or GPU now works seamlessly. Please reinstall!
* **App shortcuts**. Once installed, you can now launch in Windows, MacOS and Linux via a shortcut icon in the Start / Launch and Desktop.
* **Pre-compiled `llama.cpp` binaries** and `mamba_ssm` - 6x faster installs! Also <300MB in size for binaries.
* **50% reduced installation sizes** (-7GB or more savings), 2x faster installs and faster resolving. 50% smaller pypi sizes.
* **Tool calling improved.** Better llama.cpp parsing, no raw tool markup in chat, faster inference, a new Tool Outputs panel, timers.
* MacOS and CPU now have [Data Recipes](/docs/new/studio/data-recipe.md) enabled with multi-file uploading.
* **AMD support preliminary for Linux** only machines - auto detects.
* **Settings sidebar redesign.** Settings are now grouped into **Model, Sampling, Tools, and Preferences**
* **Context length** now adjustable. Keep in mind this is not needed as llama.cpp smartly uses the exact context you need via `--fit on`
* **Multi-file upload.** Data recipes now support multiple drag-and-drop uploads for PDF, DOCX, TXT, and MD, with backend extraction, saved uploads, and improved previews.
* **Colab** with free T4 GPUs with Unsloth Studio now fixed! [Try it here](https://colab.research.google.com/github/unslothai/unsloth/blob/main/studio/Unsloth_Studio_Colab.ipynb). Due to pre-compiled binaries, it's also 20x faster!
* **Better chat observability.** Unsloth now shows `llama-server` timings and usage, a context-window usage bar, and richer source hover cards.
* **Better UX overall** - clickable links, better LaTeX parsing, tool / code / web tooltips for default cards and much more!
* **LiteLLM -** Unsloth Studio and Unsloth were **NOT** affected by the recent LiteLLM compromise. Nemo Data Designer used LiteLLM only up to `1.80`, not the affected `1.82.7` or `1.82.8`, and has since removed it entirely.
* We now have a new one line install command, just run:&#x20;

  <pre class="language-bash" data-overflow="wrap" data-expandable="true"><code class="lang-bash">curl -fsSL https://unsloth.ai/install.sh | sh
  </code></pre>

#### **Fixes:**

* **Windows/setup improvements.** Fixed silent Windows exits, Anaconda/conda-forge startup crashes, broken non-NVIDIA Windows installs, and missing early CUDA/stale-venv setup checks.
* **System prompts fixed.** They work again for non-GGUF text and vision inference.
* **Persistent system prompts and presets.** Custom system prompts and chat presets now persist across reloads and page changes.
* **GGUF export expanded.** Full fine-tunes, not just LoRA/PEFT, can now export to GGUF. Base model resolution is more reliable, and unsupported export options are disabled in the UI.
* **Chat scroll/layout fixes.** Fixed scroll-position issues during generation, thinking-panel layout shift, and viewport jumps when collapsing reasoning panels.
* **Smarter port conflict detection.** Unsloth now detects loopback conflicts, can identify the blocking process when possible, and gives clearer fallback-port messages.
  {% endupdate %}

{% update date="2026-03-17" tags="fixes,improvements" %}

## New Tool calling + Windows Stability

* Claude Artifacts works so HTML can be executed like a snake game inside the chat
* +30% more accurate tool calls esp for small models + Timer for tool calls
* Tool + Web Search outputs can be saved + Toggle auto healing tool on/off
* Many bug fixes - Windows CPU works, Mac more seamless, faster and smaller installs
  {% endupdate %}
  {% endupdates %}

**Scheduled tasks**: Run a prompt on a schedule with a local model or an API


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/new/changelog.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
