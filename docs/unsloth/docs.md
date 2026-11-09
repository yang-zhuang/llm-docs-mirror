> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/docs.md).

# Unsloth Docs

Unsloth is an open-source framework for running and training LLMs.

Unsloth lets you run and train AI models on your own local hardware via an open-source UI.

Our docs will guide you through running & training your own LLM locally.

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download</a><a href="/docs/desktop.md#features" class="button secondary" data-icon="sparkles">Features</a><a href="https://github.com/unslothai/unsloth" class="button secondary" data-icon="github">GitHub</a>

<table data-view="cards"><thead><tr><th></th><th></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><strong>DeepSeek-V4.1-Flash</strong></td><td>Run the new October 17 model update!</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F4qwswsAZxmUaTEksSNJJ%2Fdeepseekv4.1.png?alt=media&amp;token=203263d6-e100-4c3f-9dd4-898391874d74">deepseekv4.1.png</a></td><td><a href="/docs/models/deepseek-v4.1-flash.md">DeepSeek-V4.1-Flash</a></td></tr><tr><td><strong>Qwen3.8-27B</strong></td><td>Run and train Qwen3.8-27B in Unsloth.</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FSQJGLfV6lTdcvKUuBsjC%2Fqwen3.8%20logo.png?alt=media&amp;token=7942746b-409d-4064-8e66-221fceb920dd">qwen3.8 logo.png</a></td><td><a href="/docs/models/qwen3.8.md">Qwen3.8-27B</a></td></tr><tr><td><strong>Qwen3.8-Flash-Next</strong></td><td>Run Qwen Flash with our new Nov 4 update!</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F02STQ7sMPvXPUVmCanee%2Fqwen%20next%20logo.png?alt=media&amp;token=b451d135-18c0-47e0-8584-ef64c30bc11f">qwen next logo.png</a></td><td><a href="/docs/models/qwen3.8-next.md">Qwen3.8-Flash-Next</a></td></tr><tr><td><strong>Browser Use</strong></td><td>Local LLMs can now control your browser!</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FHg3Knjk1GznF8V6R39wk%2Ffour_grid_2x2.gif?alt=media&amp;token=008f7dab-7e91-43cb-a7bd-a8e3bfec29d5">four_grid_2x2.gif</a></td><td><a href="/docs/basics/browser-use.md">Browser Use</a></td></tr><tr><td><strong>Dynamic V3.1</strong></td><td>Our new Dynamic V3.1 quants are here!</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FaG7kvP1uhrrSmKeh1lYc%2Fdynamic%20v3.png?alt=media&amp;token=509f71d9-52ce-422e-a307-b62fb3455129">dynamic v3.png</a></td><td><a href="/docs/models/nemotron-3.5-bolt.md">NVIDIA Nemotron 3.5 Bolt</a></td></tr><tr><td><strong>Qwen-Image-2.1</strong></td><td>Run the new Turbo image model locally!</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FjBLXH1oRP52poQcN1pOn%2Fqwen%20image%202.1%20logo.png?alt=media&amp;token=ab285b72-146a-4409-b9ee-327fb78cb127">qwen image 2.1 logo.png</a></td><td><a href="/docs/models/qwen-image-2.1.md">Qwen-Image-2.1</a></td></tr></tbody></table>

### ⚡ Quickstart

Unsloth supports MacOS, Linux, [Windows](/docs/get-started/install/windows-installation.md), [NVIDIA](/docs/get-started/install/pip-install.md), [AMD](/docs/get-started/install/amd.md), Intel and CPU setups. See: [Unsloth Requirements](/docs/get-started/fine-tuning-for-beginners/unsloth-requirements.md). Download the native desktop app for your operating system:

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth Desktop</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

Or, install Unsloth Studio natively, our browser-based web UI:

{% tabs %}
{% tab title="MacOS, Linux, WSL" %}
**Install Unsloth:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

Use the same command to update.
{% endtab %}

{% tab title="Windows" %}
**Install Unsloth:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

Use the same command to update.
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

{% columns %}
{% column width="50%" %}
{% content-ref url="/pages/BAeSP6aOxvSeDUzCgKOK" %}
[Complete LLM Directory](/docs/models/tutorials.md)
{% endcontent-ref %}

{% content-ref url="/pages/nw2c1elNySGBBav8WP9B" %}
[Fine-tuning Guide](/docs/get-started/fine-tuning-llms-guide.md)
{% endcontent-ref %}
{% endcolumn %}

{% column width="50%" %}
{% content-ref url="/pages/nQlzs5BcvqlaEjhsgbtY" %}
[Models](/docs/get-started/unsloth-model-catalog.md)
{% endcontent-ref %}

{% content-ref url="/pages/7sCtc6YWnJBYthTjQsr7" %}
[Unsloth API](/docs/basics/api.md)
{% endcontent-ref %}
{% endcolumn %}
{% endcolumns %}

### 👾 Unsloth Start

{% columns %}
{% column width="58.333333333333336%" %}
[Unsloth Start](/docs/integrations/unsloth-start.md) lets you connect [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md) and other agents to local models via the `unsloth start` command.

Start Unsloth, load a model, open your project folder, and then run:

```bash
unsloth start claude
```

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
| <i class="fa-deepseek">:deepseek:</i> DeepSeek Harness             | `unsloth start dsh`      |
| <i class="fa-vscode">:vscode:</i> Visual Studio Code               | `unsloth start vscode`   |
| <i class="fa-rectangle-vertical">:rectangle-vertical:</i> OpenCode | `unsloth start opencode` |
| <i class="fa-caduceus">:caduceus:</i> Hermes Agent                 | `unsloth start hermes`   |
| <i class="fa-lobster">:lobster:</i> OpenClaw                       | `unsloth start openclaw` |

### 🦥 Why Unsloth?

* We directly collab with teams behind [gpt-oss](https://docs.unsloth.ai/new/gpt-oss-how-to-run-and-fine-tune#unsloth-fixes-for-gpt-oss), [Qwen3](https://www.reddit.com/r/LocalLLaMA/comments/1kaodxu/qwen3_unsloth_dynamic_ggufs_128k_context_bug_fixes/), [Llama 4](https://github.com/ggml-org/llama.cpp/pull/12889), [Mistral](https://huggingface.co/mistralai/Mistral-Medium-3.5-128B/discussions/18), [Gemma 1-3](https://news.ycombinator.com/item?id=39671146) and [Phi-4](https://unsloth.ai/blog/phi4), where we’ve **fixed critical bugs** that greatly improved model accuracy. Andrej Karpathy for example has [praised our work](https://x.com/karpathy/status/1765473722985771335).
* Unsloth streamlines local training, inference, data, and deployment
* Unsloth supports inference and training for 500+ models: [vision](/docs/basics/vision-fine-tuning.md), [TTS](/docs/basics/text-to-speech-tts-fine-tuning.md), [embedding](/docs/basics/embedding-finetuning.md), [RL](/docs/get-started/reinforcement-learning-rl-guide.md)

### ⭐ Features

Unsloth lets you run and train models for text, [audio](https://unsloth.ai/docs/basics/text-to-speech-tts-fine-tuning), [embedding](https://unsloth.ai/docs/new/embedding-finetuning), [vision](https://unsloth.ai/docs/basics/vision-fine-tuning) and more. Unsloth provides many key features for both inference and training:

#### Inference

* Run and train LLMs, diffusion, embedding, audio models: [Qwen3.8](/docs/models/qwen3.8.md), [Kimi K3](https://unsloth.ai/docs/models/kimi-k3), MiniMax-H3, [Muse Glimmer](https://unsloth.ai/docs/models/muse-glimmer), [DeepSeek-V4](https://unsloth.ai/docs/models/deepseek-v4), [Gemma 4](https://unsloth.ai/docs/models/gemma-4).
* **Agents & Tools:** Use local models with [Claude Code](https://unsloth.ai/docs/basics/claude-code), [Codex](https://unsloth.ai/docs/basics/codex), and [MCP](https://unsloth.ai/docs/basics/mcp), including tool calling and code execution.
* **Search & RAG:** Use private and unlimited web search, deep research, auto-compaction (rolling context window) and RAG.
* **Browser use:** [Navigate websites](/docs/basics/browser-use.md), fill out forms, read PDFs, and edit files with a local model.
* **Image and video:** Run and train [image](https://unsloth.ai/docs/basics/diffusion-image) and video diffusion or multimodal models
* **Remote & LAN:** Access your local models from any device on [LAN](https://unsloth.ai/docs/basics/lan) or remotely through secure [Cloudflare](https://unsloth.ai/docs/basics/how-to-serve-local-llms-anywhere-secure-remote-access-with-cloudflare-and-unsloth) HTTPS.
* **Connect:** Serve models through an [OpenAI compatible API](https://unsloth.ai/docs/basics/api). Also connect your ChatGPT/Codex subscription and [cloud providers](https://unsloth.ai/docs/integrations/connections)
* **Sandboxing:** [Control which files your model can access](https://unsloth.ai/docs/new/studio/sandboxing-in-unsloth) when it runs commands.

#### Train & Deploy

* **Fine-tuning:** Train LLMs, diffusion, TTS, and embedding models 2× faster with 70% less VRAM with [no accuracy loss](https://unsloth.ai/blog#training)
* **Complete support:** Supports [reinforcement learning](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide), LoRA, QLoRA, full fine tuning, pretraining, RL, GRPO, DPO, and FP8.
* **Export & Deploy:** [Export](https://unsloth.ai/docs/new/studio/export) or Deploy models with including [GGUF](https://unsloth.ai/docs/basics/inference-and-deployment/saving-to-gguf), NVFP4, FP8 and more formats.
* **Datasets:** Build datasets from PDFs, CSVs, DOCX files, and more with [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe).

### **Video Demo**

{% embed url="<https://www.youtube.com/watch?v=_1hgTTuber4>" %}

{% columns %}
{% column width="50%" %}
{% content-ref url="/pages/OktH76Rsg2WQ12B4KR5H" %}
[Unsloth Updates](/docs/new/changelog.md)
{% endcontent-ref %}

{% content-ref url="/pages/gEugERiAw2ztDNt98JVR" %}
[Inference & Deployment](/docs/basics/inference-and-deployment.md)
{% endcontent-ref %}
{% endcolumn %}

{% column width="50%" %}
{% content-ref url="/pages/55c8159250801d9ea2207b9eb88a9a11b331d3ad" %}
[Unsloth Start](/docs/integrations/unsloth-start.md)
{% endcontent-ref %}

{% content-ref url="/pages/QznsvWxKKvrY6PdiByzz" %}
[Dynamic 3.0 GGUFs](/docs/basics/dynamic-3.0-ggufs.md)
{% endcontent-ref %}
{% endcolumn %}
{% endcolumns %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-134302f2507d4313b9575917c9a43b0a0028856c%2Flarge%20sloth%20wave.png?alt=media" alt="" width="188"><figcaption></figcaption></figure>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/docs.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
