> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/codex.md).

# How to Run Local LLMs with OpenAI Codex

Use open models with OpenAI Codex on your device locally.

This step-by-step guide shows you how to connect open LLMs and APIs to OpenAI Codex **entirely locally**, complete with screenshots. Codex only needs a local endpoint that speaks the OpenAI Responses API. Run using any open model like Qwen, DeepSeek, Gemma, and more.

For this tutorial, we’ll use the open models: [Gemma 4](/docs/models/gemma-4.md) and [Qwen3.5](/docs/models/qwen3.5.md) which are strong agentic & coding models (works on 24GB RAM/unified mem device). For inference, we'll use [Unsloth Studio](https://github.com/unslothai/unsloth) and [`llama.cpp`](https://github.com/ggml-org/llama.cpp) enables you to run/serve LLMs on macOS, Linux, and Windows. You can swap in any other model, just update the model names in your scripts and Codex config.

<a href="/docs/basics/codex.md#setup-codex" class="button primary" data-icon="openai">Setup Codex</a><a href="/docs/basics/codex.md#quickstart-tutorials" class="button primary">📖 Setup Local Model Tutorial</a>

For model quants, we'll use Unsloth [**Dynamic GGUFs**](/docs/basics/dynamic-3.0-ggufs.md) so you can run quantized GGUF models while retaining as much accuracy as possible.

{% hint style="info" %}
Codex has changed quite a lot since Jan 2026. It now uses the [**OpenAI Responses API**](https://platform.openai.com/docs/api-reference/responses) **exclusively**, and Chat Completions support has been deprecated. [Unsloth Studio](#unsloth-tutorial) supports both, so we'll use `wire_api = "responses"` throughout this guide.
{% endhint %}

### <i class="fa-openai">:openai:</i> Setup Codex

[Codex](https://github.com/openai/codex) is OpenAI's official coding agent that runs locally. While designed for ChatGPT, it supports **custom API endpoints**, which makes it work for local LLMs. We'll later point it to Unsloth Studio's `/v1/responses` endpoint once Unsloth is up.

{% tabs %}
{% tab title="Linux / WSL" %}
Run in your terminal:

```bash
apt update
sudo apt install nodejs npm -y
npm install -g @openai/codex
```

{% endtab %}

{% tab title="Windows" %}
Run in Windows Powershel:

```powershell
winget install --id OpenAI.Codex
```

{% hint style="info" %}
**Prefer the Codex desktop app?** Install from the Microsoft Store:

```powershell
winget install --id 9PLM9XGG6VKS --source msstore
```

Or via the [Microsoft app Store](https://apps.microsoft.com/detail/9plm9xgg6vks). The app reads the same `%USERPROFILE%\.codex\config.toml`, so the provider config we set up later applies either way.
{% endhint %}

{% hint style="info" %}
**Prefer WSL?** Open PowerShell as admin, run `wsl --install`, restart, then follow the Linux tab above inside Ubuntu. You'll need a small networking trick to reach Unsloth on the Windows host - see the WSL hint in Connect Codex to Unsloth.
{% endhint %}
{% endtab %}

{% tab title="MacOS" %}
Run in your terminal:

<pre class="language-bash"><code class="lang-bash"><strong>bash brew install --cask codex
</strong></code></pre>

{% endtab %}
{% endtabs %}

That's it for the install - **don't run `codex` yet**. Running it bare drops you into OpenAI's "Sign in with ChatGPT" picker (which is modal - there's no escape hatch). Once we wire up a local profile,\
`codex --oss --profile unsloth_api` or `codex --oss --profile llama_cpp` skips that screen entirely because custom providers default to `requires_openai_auth = false`. Start the local model server first, then launch Codex against it.

## 📖 Quickstart Tutorials <a href="#quickstart-tutorials" id="quickstart-tutorials"></a>

Before we begin, we firstly need to complete setup for the specific model you're going to use. We use [Unsloth](https://unsloth.ai/docs/new/studio) (a web UI) and llama.cpp which are open-source frameworks for running and serving LLMs on your Mac, Linux, Windows devices.

{% columns %}
{% column %}
Before we begin, we firstly need to complete setup for the specific model you're going to use. We use [Unsloth](/docs/new/studio.md) (a web UI) and llama.cpp which are open-source frameworks for running and serving LLMs on your Mac, Linux, Windows devices.

Unsloth also has unique self-healing [tool-calling](/docs/new/studio/chat.md#auto-healing-tool-calling) and [web search](/docs/new/studio/chat.md#code-execution) capabilities. See right for Claude Code connected to Unsloth:
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FEGEKo6oPthjtSf0shavs%2F127.0.0.1_8889_chat%20(2).png?alt=media&amp;token=c59c7110-402c-4d21-96c5-cd96c921a184" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

<a href="/docs/basics/codex.md#unsloth-tutorial" class="button primary">🦥 Unsloth Tutorial</a><a href="/pages/PCjZ57h5pE0QccKyJMYD#llama.cpp-tutorial" class="button primary">🦙 llama.cpp Tutorial</a>

## 🦥 Unsloth Tutorial

For this tutorial, we will serve/connect local models to Claude Code via a UI by using [Unsloth](https://github.com/unslothai/unsloth). Unsloth works on Windows, WSL, Linux and MacOS.

{% columns %}
{% column %}

* Search, download, [run GGUFs](/docs/new/studio.md#run-models-locally) and safetensor models
* [**Self-healing** tool calling](/docs/new/studio.md#execute-code--heal-tool-calling) + **web search**
* [**Code execution**](/docs/new/studio.md#run-models-locally) (Python, Bash)
* [Automatic inference](https://unsloth.ai/docs/desktop#feature-deep-dive) parameter tuning (temp, top-p, etc.)
* Fast CPU + GPU inference via llama.cpp
* [Train LLMs](/docs/new/studio.md#no-code-training) 2x faster with 70% less VRAM

See below for install instructions:
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FY3nfB43TEk7k11zcE4wm%2Fthe%20big%20one.gif?alt=media&amp;token=335be087-7375-4f89-9039-71195ee44ab8" alt=""><figcaption><p>Example of Qwen3.6 2-bit running in Unsloth.</p></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% stepper %}
{% step %}

#### Download Unsloth

The easiest way to get started is by installing the [Unsloth Desktop](/docs/desktop.md) app. It supports [MacOS](/docs/get-started/install/mac.md), Linux, [Windows](/docs/get-started/install/windows-installation.md), [NVIDIA](/docs/get-started/install/pip-install.md), [AMD](/docs/get-started/install/amd.md), Intel and CPU setups.

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

Or, if you prefer manual installation:

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

#### Install

1. Open the Unsloth installer (`.dmg`, `.exe` files)
2. Drag Unsloth to Applications for Mac or complete setup for Windows.
3. Launch the app and wait for installation to complete
   {% endstep %}

{% step %}

#### Choose a model

Open 'Select model' dropdown ontop or 'Model hub' tab, choose a model and a quantization that fits your device, then download it. Once it finishes, start chatting - no setup required.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNCEVgKLJI0goPqjgcg9B%2Fmodel%20hub%20models.png?alt=media&amp;token=533b5e3c-a901-4b33-963e-4a703cc9d5a6" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Unsloth is now ready

To start chatting, type a message and press Enter.

* **Connect tools:** [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md), web search, [MCP](/docs/basics/mcp.md) and more
* **Train models:** Fine-tune text, diffusion, embedding, and more
* **Generate media:** Create and train images, video, TTS locally

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FpAGvwjGD0iVMZKBoyu7m%2Fgreeennn.png?alt=media&amp;token=d17a5528-8375-444c-9aff-f9e9f7903bcd" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### Model Loading + API Guide

{% stepper %}
{% step %}

#### Select Model

Before using the API, load a model from the **Select model** dropdown in the top-left corner of the Chat page.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FuZqd6tcZ5LgMSh4ZND5x%2Fexport-1778505117710-24fps.gif?alt=media&amp;token=9defec95-5404-4654-9c33-67be967c9820" alt=""><figcaption></figcaption></figure>

In this guide, we’ll use: `unsloth/gemma-4-26B-A4B-it-GGUF` with the recommended `UD-Q4_K_XL` quantization.
{% endstep %}

{% step %}

#### Test the Model

Before using the Client, send a quick message:

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F2Ivilke0aJX8AHWDwSmr%2Fimage.png?alt=media&amp;token=9f9380b9-f963-4861-a17b-fd0fe16684d4" alt="" width="563"><figcaption></figcaption></figure></div>

{% hint style="info" %}
This confirms that the model loaded correctly and is ready to respond.
{% endhint %}
{% endstep %}

{% step %}

#### **Unsloth API key**

In Unsloth, open **Settings → API** to view or create your API key. If you start Unsloth headless with `unsloth run`, the key is also printed to the console as `sk-unsloth-...`.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FAZwaRmBVPpXA2SFhMGW9%2Fexport-1778506924396-30fps.gif?alt=media&amp;token=96f3f1a7-fce4-4508-b1b0-e8b6294dc423" alt=""><figcaption></figcaption></figure>

Treat your API key like a password and avoid exposing it in screenshots or repositories.
{% endstep %}
{% endstepper %}

### Optional: adjust runtime settings

You can pass additional runtime options when starting a model with `unsloth run`.

```bash
# Enable reasoning and use a larger context window
unsloth run \
  --model unsloth/gemma-4-26B-A4B-it-GGUF \
  --reasoning on \
  -c 131072
```

Reasoning-capable models can be started with `--reasoning on` or `--reasoning off`. The `-c` flag controls the available context window.

```bash
# Serve for a coding agent on a custom port
unsloth run \
  --model unsloth/gemma-4-26B-A4B-it-GGUF \
  --disable-tools \
  -p 8888
```

Use `-p` if you need the API to run on a different port.

{% hint style="info" %}
When driving an external coding agent, add `--disable-tools`. This switches Unsloth Studio to passthrough so the agent's own tools are forwarded and returned as tool calls for the agent to run, instead of Unsloth executing its built-in tools server-side.
{% endhint %}

For more advanced runtime configuration, see the main [API tuning](https://unsloth.ai/docs/basics/api#unsloth-run-command) section.

## ⚙️ Connect Codex

Now that we have setup the local LLM for Codex, we now configure Codex to work with your tool. You can either connect easily with `unsloth start` below or do it [manually](#connect-manually).

### ⚡ Run OpenAI Codex with `unsloth start`

To launch Codex directly with a model, run:

```bash
unsloth start Code \
    --model unsloth/Qwen3.8-27B-GGUF-GGUF:UD-Q4_K_XL
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 20 \
    --min-p 0.0 \
    --reasoning-effort medium
```

{% hint style="success" %}
If there are no settings/sampling flags set, Unsloth automatically selects the best/recommended settings for the model including context length, temperature etc.
{% endhint %}

With a GGUF model loaded in Unsloth Studio, open your project folder and run:

```bash
unsloth start codex
```

Unsloth creates an isolated Codex home and a Unsloth backed Responses provider for the launch. Your normal `~/.codex` configuration is left alone.

Codex state is temporary by default. Use `--persist` when you want to keep its Unsloth-managed configuration and sessions:

```bash
unsloth start codex --persist
unsloth start codex --persist resume --last
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FzXhTRRhKnT7tc5A4su0w%2FScreenshot_20260714_150727.png?alt=media&amp;token=1ad76079-1127-443e-8e2b-96545269003e" alt="OpenAI Codex running with a local GGUF model through Unsloth Studio"><figcaption><p>Codex connected to a local GGUF model through the Unsloth Studio Responses endpoint.</p></figcaption></figure>

> Codex currently requires a GGUF model served through the `llama-server` backend.

See the complete `unsloth start` reference for model loading, persistence and all wrapper options.

The rest of this guide covers a fully manual Codex provider setup.

#### 🔌 Connect manually

This section is for manual setting up, it is the same whether you used Unsloth Studio, llama.cpp, or another OpenAI-compatible local server. Codex needs three values: the **API key**, the **base URL**, and the **model name**. The example below uses Unsloth Studio; for llama.cpp, use the same shape with the `llama_cpp` profile in the llama.cpp section.

{% stepper %}
{% step %}

#### **Configure the Unsloth provider**

Codex looks for `~/.codex/config.toml` on macOS/Linux/WSL or `%USERPROFILE%\.codex\config.toml` on Windows. Create or edit it:

{% code title="\~/.codex/config.toml" overflow="wrap" %}

```toml
# Default local provider used with `codex --oss`
oss_provider = "unsloth_api"

[model_providers.unsloth_api]
name                  = "Unsloth Studio"
base_url              = "http://localhost:8888/v1"
env_key               = "UNSLOTH_STUDIO_AUTH_TOKEN"
wire_api              = "responses"
requires_openai_auth  = false
```

{% endcode %}

Next, create a Codex profile for Unsloth:

{% code title="\~/.codex/unsloth\_api.config.toml" overflow="wrap" %}

```toml
model_provider = "unsloth_api"
model = "unsloth/gemma-4-26B-A4B-it-GGUF"
```

{% endcode %}

{% hint style="info" %}
`model` must match the id your server reports at `GET http://localhost:8888/v1/models`. Unsloth Studio exposes the full repo id (for example `unsloth/gemma-4-26B-A4B-it-GGUF`). The llama.cpp section below uses `--alias "unsloth/gemma-4-26B-A4B"`, so use that shorter id when pointing Codex at llama-server instead.
{% endhint %}

{% hint style="info" %}
This config registers an `unsloth_api` Codex model provider, points it at Unsloth Studio, and sets `unsloth_api` as the default local provider for `codex --oss`. The separate `unsloth_api` profile selects the Unsloth provider and model only when you launch Codex with `--profile unsloth_api`, so your normal Codex setup is not changed. Codex reads the API key from an environment variable named `UNSLOTH_STUDIO_AUTH_TOKEN`. You'll set the real key in the next step.
{% endhint %}

| Field                  | What it does                                                                                                               |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `base_url`             | Your local server endpoint + `/v1`                                                                                         |
| `env_key`              | **Name** of the env var Codex reads your API key from. This is not the key itself.                                         |
| `wire_api`             | `responses`. Codex now exclusively uses OpenAI's Responses API.                                                            |
| `requires_openai_auth` | `false` makes Codex skip the "Sign in with ChatGPT" screen for this provider. Default is already `false`, but be explicit. |
| `model`                | The model ID your server exposes. Hit `GET <base_url>/models` to confirm the exact string.                                 |
| `oss_provider`         | <p>Sets <code>unsloth\_api</code> as the default local provider when launching Codex with<br><code>--oss</code>.</p>       |
| `requires_openai_auth` | `false` makes Codex skip the "Sign in with ChatGPT" screen for this provider.                                              |

{% hint style="warning" %}
OpenAI removed `wire_api = "chat"` support. Always use `wire_api = "responses"`. If you set `wire_api = "chat"`, Codex refuses to start with `` `wire_api = "chat"` is no longer supported. How to fix: set `wire_api = "responses"` in your provider config. ``
{% endhint %}

{% hint style="info" %}
You can create multiple profile files, one for each Unsloth model you swap between. Launch the one you want with `codex --profile <profile-name>`.
{% endhint %}
{% endstep %}

{% step %}

#### Set the API key env var

Use the same env var name you wrote in `env_key`. In the Unsloth Studio example above, `env_key = "UNSLOTH_STUDIO_AUTH_TOKEN"`, so set `UNSLOTH_STUDIO_AUTH_TOKEN` in the same terminal you will run Codex from:

{% code title="MacOS / Linux / WSL" %}

```bash
export UNSLOTH_STUDIO_AUTH_TOKEN=YOUR_TOKEN
```

{% endcode %}

{% code title="Windows PowerShell" %}

```powershell
$env:UNSLOTH_STUDIO_AUTH_TOKEN = "YOUR_TOKEN"
```

{% endcode %}

If you renamed `env_key`, rename the variable in the commands too. For example, a llama.cpp profile that uses `env_key = "LLAMA_CPP_API_KEY"` needs `LLAMA_CPP_API_KEY`, not `UNSLOTH_STUDIO_AUTH_TOKEN`.

**Session vs Persistent:** the commands above apply to the current terminal only. To persist:

* **MacOS / Linux / WSL:** add the `export` line to `~/.bashrc` (bash) or `~/.zshrc` (zsh).
* **Windows:** run `setx UNSLOTH_STUDIO_AUTH_TOKEN "YOUR_TOKEN"` once, or add the `$env:` line to your PowerShell `$PROFILE`.

{% hint style="warning" %}
**Running Codex inside WSL with Unsloth on Windows?** WSL is a separate network namespace, so `localhost` from inside WSL doesn't reach Unsloth. Edit your `config.toml` to use the Windows host IP instead:

```bash
# Get the Windows host IP from inside WSL
ip route | grep default | awk '{print $3}'
```

Then set `base_url = "http://<that-ip>:8888/v1"`. If you have WSL2 mirrored networking enabled (`.wslconfig` → `networkingMode=mirrored`), `localhost` works as on native Windows.
{% endhint %}
{% endstep %}

{% step %}

#### **Launch Codex**

```bash
mkdir my-project && cd my-project
codex --oss --profile unsloth_api
```

{% hint style="info" %}
**First launch in a new directory** Codex asks *"Do you trust the contents of this directory?"* - pick *Yes, continue.* This is the per-cwd trust prompt, not the ChatGPT login (that one is skipped because of \`requires\_openai\_auth = false\`). Subsequent launches in the same directory skip this prompt.
{% endhint %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FWLWGwxYFup5JCptPghfx%2Fimage.png?alt=media&amp;token=e47961e9-20b6-4ec7-adec-919c819dc740" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
**Seeing `Model metadata for` unsloth/gemma-4-26B-A4B `not found. Defaulting to fallback metadata`?** Codex ships with a built-in table of context windows, tool support, and input modalities for OpenAI's own models. For anything else - it falls back to safe defaults. The warning fires once per session for every non-OpenAI slug. Everything still works, you can ignore it.

**To fix it:** add `model_context_window = 131072` to the top of `~/.codex/config.toml` so Codex uses Gemma 4's real 128K context instead of its fallback guess. For full control over tool support and input modalities too, point `model_catalog_json` inside `[profiles.unsloth_api]` at a JSON file containing a custom `ModelInfo` entry for your slug.
{% endhint %}

The `--profile unsloth_api` flag tells Codex to load `~/.codex/unsloth_api.config.toml`, which selects the Unsloth Studio provider and model. Add `--oss` to run through Codex's local OSS provider flow. The model name appears in Codex's status bar.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F0EDBeLBbGfnBbW2Osnh9%2Fimage.png?alt=media&amp;token=e96a4905-5816-4c12-bd4d-a3a41500ef29" alt=""><figcaption></figcaption></figure>

Add `--search` to enable web search:

```bash
codex --oss --profile unsloth_api --search
```

To bypass all approval prompts **(BEWARE this will make Codex do and execute code however it likes without any approvals!)**:

{% code overflow="wrap" %}

```bash
codex --oss --profile unsloth_api --search --dangerously-bypass-approvals-and-sandbox
```

{% endcode %}
{% endstep %}
{% endstepper %}

### Try a real task

Try this prompt to install and run a simple Unsloth finetune:

{% code overflow="wrap" %}

```
You can only work in the cwd project/. Do not search for AGENTS.md - this is it.
Install Unsloth via a virtual environment via uv. See
https://unsloth.ai/docs/get-started/install/pip-install on how (get it and read).
Then do a simple Unsloth finetuning run described in
https://github.com/unslothai/unsloth. You have access to 1 GPU.
```

{% endcode %}

and if we wait a little longer, you will see a successfully fine-tuned model with Unsloth!

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFPuzCCHWIIXwuvTloNDh%2Fexport-1778571001272-30fps.gif?alt=media&amp;token=2bcaeaf1-a906-4169-b4ac-f17388ebaebb" alt=""><figcaption></figcaption></figure>

### Disconnect or revert

Launch Codex without `-p unsloth_api` and it'll use its default provider. Or delete the `[profiles.unsloth_api]` and `[model_providers.unsloth_api]` blocks from `~/.codex/config.toml`.

```bash
unset UNSLOTH_STUDIO_AUTH_TOKEN
```

You can leave Unsloth Studio running or shut it down. It doesn't intercept anything when stopped.

### Troubleshooting

| Symptom                                    | Likely cause                                                              | Fix                                                                                                                    |
| ------------------------------------------ | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `Model metadata for ... not found`         | Non-OpenAI slug, no built-in metadata                                     | Harmless warning. To silence the side-effects, set `model_context_window = 131072` in `~/.codex/config.toml`, or point |
| Codex says it's GPT                        | Codex injects an OpenAI-referencing system prompt; local models mirror it | Not a routing bug. Verify via Unsloth's activity panel. Override the system prompt to change self-report.              |
| `Connection refused`                       | Unsloth isn't running or wrong port                                       | Confirm Unsloth is up at `http://localhost:8888`; check `base_url` in `config.toml`                                    |
| `wire_api = "chat" is no longer supported` | Legacy `wire_api = "chat"` in config                                      | Switch to `wire_api = "responses"`                                                                                     |
| `model not found`                          | Model ID typo                                                             | `GET http://localhost:8888/v1/models` and copy the exact ID                                                            |
| OOM mid-generation                         | Context too large for VRAM                                                | Reduce context in Unsloth **Settings → Inference**, or use a smaller quant                                             |
| Codex shows "Sign in with ChatGPT" picker  | <p>Launched bare <code>codex</code> (no<br><code>--oss</code>)</p>        | Quit (Ctrl+C), then re-launch with `codex --oss --profile unsloth_api`. Custom providers skip that                     |
| Tool calling unreliable                    | Need self-healing fallback                                                | Unsloth's [self-healing tool calls](file:///1382377/new/studio/#execute-code--heal-tool-calling) are on by default     |
| WSL: `Connection refused` to `localhost`   | WSL network namespace                                                     | Use the Windows host IP in `base_url`, or enable WSL2 mirrored networking                                              |

## 🦙 Llama.cpp Tutorial

We can also use `llama.cpp` directly. We need to deploy `llama-server` which is an open-source framework for running and serving LLMs efficiently on Mac, Linux and Windows devices. The model will be served on **port 8001** with all agent tool calls routed through that single OpenAI-compatible endpoint.

{% hint style="info" %}
The llama.cpp endpoint will be on **port 8001** instead of `8888` (Unsloth Studio's default). Adjust your Codex `base_url` accordingly in `~/.codex/config.toml`.
{% endhint %}

{% stepper %}
{% step %}

#### **Install llama.cpp**

We need to install `llama.cpp` to deploy/serve local LLMs to use in Codex. We follow the official build instructions for correct GPU bindings and maximum performance. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev git-all -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first \
    --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endstep %}

{% step %}

#### **Download and use models locally**

Download the model via the `hf` CLI (`pip install huggingface_hub hf_transfer`). We use the **UD-Q4\_K\_XL** quant for the best size/accuracy balance. You can find all Unsloth GGUF uploads in our [Collection here](file:///1382377/get-started/unsloth-model-catalog.md). If downloads get stuck, see [https://hugging-face-hub-xet-debugging.md](https://hugging-face-hub-xet-debugging.md "mention").

```bash
hf download unsloth/gemma-4-26B-A4B-it-GGUF \
    --local-dir unsloth/gemma-4-26B-A4B-it-GGUF \
    --include "*UD-Q4_K_XL*"
```

{% hint style="info" %}
**Want vision support?** Add `--include "*mmproj-BF16*"` to also pull the vision projector, then pass `--mmproj unsloth/gemma-4-26B-A4B-it-GGUF/mmproj-BF16.gguf` to `llama-server`. Codex itself is text-only, so this is optional.
{% endhint %}

{% hint style="success" %}
We used `unsloth/gemma-4-26B-A4B-it-GGUF`, but you can use anything like `unsloth/Qwen3.6-35B-A3B-GGUF` - see [Qwen3.6-35B-A3B](/docs/models/qwen3.6.md).
{% endhint %}
{% endstep %}

{% step %}

#### **Start the Llama-server**

To deploy Gemma-4-26B-A4B for agentic workloads, we use `llama-server`. We apply Google's recommended sampling parameters (`temp 1.0`, `top_p 0.95`, `top_k 64`) and enable `--jinja` for proper tool calling support.

Run this command in a new terminal (use `tmux` or open a new terminal). The below should **fit comfortably in a 24GB GPU (RTX 4090)** at \~18GB. `--fit on` will also auto offload, but if you see bad performance, reduce `--ctx-size`.

```bash
./llama.cpp/llama-server \
    --model unsloth/gemma-4-26B-A4B-it-GGUF/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf \
    --alias "unsloth/gemma-4-26B-A4B" \
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 64 \
    --port 8001 \
    --kv-unified \
    --cache-type-k q8_0 --cache-type-v q8_0 \
    --batch-size 4096 --ubatch-size 1024
```

{% hint style="info" %}
We used `--cache-type-k q8_0 --cache-type-v q8_0` for KV cache quantization to reduce VRAM use. If you see reduced quality, use `bf16` instead (`--cache-type-k bf16 --cache-type-v bf16`), but VRAM doubles.
{% endhint %}

{% hint style="success" %}
**Disabling thinking** can improve performance for agentic coding tasks. Gemma 4 enables thinking by default via the chat template - to disable it, add the following flag to the llama-server command:

**MacOS / Linux / WSL:**

`--chat-template-kwargs '{"enable_thinking":false}'`

**Windows PowerShell:**

`--chat-template-kwargs "{\"enable_thinking\":false}"`
{% endhint %}
{% endstep %}

{% step %}

#### **Point Codex at port 8001**

Edit your `~/.codex/config.toml` to use the llama-server port:

{% code title="\~/.codex/config.toml" %}

```toml
[model_providers.llama_cpp]
name      = "llama.cpp"
base_url  = "http://localhost:8001/v1"
env_key   = "LLAMA_CPP_API_KEY"
wire_api  = "responses"
```

{% endcode %}

Then launch with the new profile:

```bash
codex --oss llama_cpp
```

Since llama-server doesn't require a real key, you can set the auth token to anything:

{% code title="MacOS / Linux / WSL" %}

```bash
export LLAMA_CPP_API_KEY=sk-no-key-required
```

{% endcode %}

{% code title="Windows PowerShell" %}

```powershell
$env:LLAMA_CPP_API_KEY = "sk-no-key-required"
```

{% endcode %}
{% endstep %}
{% endstepper %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/codex.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
