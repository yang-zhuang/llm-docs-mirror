> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/integrations/openclaw.md).

# How to Run Local AI Models with OpenClaw

Guide to running local LLMs with OpenClaw.

This guide will show how to use open LLMs locally with **OpenClaw by connecting it to Unsloth**. OpenClaw is an **open-source AI agent** interface that connects to a model to run tasks across your project. OpenClaw is able to works with any local model by connecting through **Unsloth’s OpenAI-compatible API**: including DeepSeek, Qwen, Gemma, and more.

OpenClaw acts as the client, while Unsloth loads and serves models via a **local API**.After setup, OpenClaw will run against your local model through Unsloth, letting you use it directly as an **AI agent.** In this tutorial, we'll use [Qwen3.6](/docs/models/qwen3.6.md).

<a href="/docs/integrations/openclaw.md#connecting-to-openclaw" class="button primary" data-icon="lobster">Connecting to OpenClaw</a><a href="/docs/integrations/openclaw.md#quickstart" class="button primary">Quickstart</a>

{% hint style="info" %}
In this tutorial, we’ll use `unsloth/Qwen3.6-27B-GGUF` in Unsloth and access it through OpenClaw. Prefer a different model? Swap in any other model by loading it in Unsloth and updating the configuration.
{% endhint %}

### Installing OpenClaw

{% tabs %}
{% tab title="macOS, Linux, WSL" %}
Install OpenClaw using the official installer:

`curl -fsSL https://openclaw.ai/install.sh | bash`

This sets up OpenClaw and guides you through initial setup.
{% endtab %}

{% tab title="Windows (PowerShell)" %}
Install OpenClaw using the official installer:

`iwr -useb https://openclaw.ai/install.ps1 | iex`

This sets up OpenClaw and guides you through initial setup.
{% endtab %}
{% endtabs %}

### ⚡ Quickstart

After installing OpenClaw, we'll need to install [Unsloth Desktop](/docs/desktop.md) to enable OpenClaw to serve and run inference of local models.

{% stepper %}
{% step %}

#### Download Unsloth

The easiest way to get started is by installing the Unsloth Desktop app. It supports [MacOS](/docs/get-started/install/mac.md), Linux, [Windows](/docs/get-started/install/windows-installation.md), [NVIDIA](/docs/get-started/install/pip-install.md), [AMD](/docs/get-started/install/amd.md), Intel and CPU setups.

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

### Unsloth is now ready

To start chatting, type a message and press Enter.

**Connect OpenClaw.** Run `unsloth start openclaw` to launch OpenClaw with the loaded Unsloth model in a separate managed environment. Your normal OpenClaw configuration is left unchanged.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FpAGvwjGD0iVMZKBoyu7m%2Fgreeennn.png?alt=media&amp;token=d17a5528-8375-444c-9aff-f9e9f7903bcd" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### ⚙️ Launch OpenClaw with `unsloth start`

OpenClaw can connect to a model already running in Unsloth Studio, or start one automatically when Unsloth is not running.

Connect to a running Unsloth instance

Once a model is loaded in Unsloth Studio, run:

```bash
unsloth start openclaw
```

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQm2hy6E5WvSzvmhQX0VL%2Fimage.png?alt=media&amp;token=e87ad9ac-8c43-4d20-9276-10eed404bd89" alt="" width="563"><figcaption></figcaption></figure></div>

Unsloth launches OpenClaw in local TUI mode with the Unsloth provider, model, and context length configured inside a separate managed environment. Your normal OpenClaw setup is left unchanged.

Once OpenClaw opens, give it a task such as:

```
inspect this repo and summarize it in one sentence: https://github.com/unslothai/unsloth
```

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fz93FYVhDJZKkBw3bY5X9%2Fimage.png?alt=media&amp;token=f79db6e8-59ea-4ac7-8008-fe6e6124d977" alt="" width="563"><figcaption></figcaption></figure></div>

#### Start a model automatically

If Unsloth is not already running, pass a model ID:

To launch OpenClaw directly with a model, run:

```bash
unsloth start openclaw \
    --model unsloth/Qwen3.8-27B-GGUF-GGUF:UD-Q4_K_XL
    --temp 1.0 \
    --top-p 0.95 \
    --top-k 20 \
    --min-p 0.0 \
    --reasoning-effort medium
```

Unsloth automatically selects the correct parameters to use but you can still change it.

Unsloth starts the model, launches OpenClaw, and stops the temporary server when you exit.\
\
To keep your OpenClaw state and return to the same session later, add `--persist` and choose a session key:

```bash
unsloth start openclaw \
  --model unsloth/Qwen3.6-27B-GGUF \
  --persist \
  agent --local \
  --session-key my-session \
  --message "Inspect this repository"
```

Continue later using the same session key:

```bash
unsloth start openclaw \
  --model unsloth/Qwen3.6-27B-GGUF \
  --persist \
  agent --local \
  --session-key my-session \
  --message "Continue"
```

See the complete [unsloth start](/docs/integrations/unsloth-start.md) reference for named sessions, model loading, remote Unsloth servers, and advanced options.

The rest of this guide covers the manual OpenClaw provider setup.

### Manual OpenClaw provider setup

### 🔑 Creating an API key

Keys are created from **Unsloth → Settings → API Keys**.

1. Open the sidebar, click your **Unsloth** avatar at the bottom-left.
2. Go to **Settings** → **API Keys**.
3. Enter a friendly name (e.g. `claude-code-macbook`).
4. *(Optional)* Set an expiry.
5. Click **Create**.
6. **Copy the key immediately.** Unsloth stores only a hash and you won't be able to view it again.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FrWnqY5PgvZdbWK8pmlD5%2Fimage.png?alt=media&amp;token=3507e7d7-b552-447f-b503-2418802b8f6e" alt="" width="375"><figcaption></figcaption></figure></div>

All keys start with the `sk-unsloth-` prefix. Revoke a key from the same page at any time. Requests made with a revoked key will fail with `401 Unauthorized`.

### Connecting to OpenClaw

OpenClaw reads its config from `~/.openclaw/openclaw.json`. Add (or merge) a `models` block with a `unsloth` provider pointing at Unsloth's Anthropic Messages API.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fs5g7Epfb2KjiQQf4MJf7%2Fopenclaw_unsloth_chat.png?alt=media&amp;token=c4de5f80-2a99-4527-bde0-c4e05e086f79" alt="" width="375"><figcaption></figcaption></figure></div>

{% code title="\~/.openclaw/openclaw\.json" %}

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "unsloth": {
        "baseUrl": "http://localhost:8888",
        "apiKey": "sk-unsloth-xxxxxxxxxxxx",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "unsloth/Qwen3.6-27B-GGUF",
            "name": "unsloth/Qwen3.6-27B-GGUF"
          }
        ],
        "authHeader": true
      }
    }
  }
}
```

{% endcode %}

**Notes:**

* `baseUrl` is the Unsloth origin with no path. OpenClaw talks to Unsloth over the Anthropic Messages API, and the Anthropic SDK appends `/v1/messages` itself, so do not add `/v1` here (a trailing `/v1` would send requests to `/v1/v1/messages`).
* `api: "anthropic-messages"` tells OpenClaw to talk to Unsloth's `/v1/messages` endpoint.
* `authHeader: true` sends your key as `Authorization: Bearer …`.
* Set each model's `id` and `name` to the name you chose when loading the model in Unsloth.
* If you're running Unsloth on a remote machine, replace `localhost:8888` with that machine's address (e.g. `http://10.0.0.42:8888`).

### Optional: configure model behavior

OpenClaw connects through the model running in Unsloth. Runtime settings can be configured when starting the server.

```bash
# Configure default generation behavior (--disable-tools passes OpenClaw's own tools through)
unsloth run \
  --model unsloth/gemma-4-26B-A4B-it-GGUF \
  --disable-tools \
  --reasoning off \
  --temp 0.6
```

{% hint style="warning" %}
Use `--disable-tools` when driving OpenClaw (or any external coding agent). By default Unsloth Studio runs its own server-side tools, which swallows the agent's tool calls, so OpenClaw answers but never edits files. `--disable-tools` switches to passthrough, so OpenClaw's own tools are used.
{% endhint %}

Use `--reasoning off` to turn thinking off, or `--reasoning on` to turn it on for models that support reasoning.

```bash
# Allow connections from other devices
unsloth run \
  --model unsloth/gemma-4-26B-A4B-it-GGUF \
  -H 0.0.0.0 \
  -p 8888
```

This starts the server on `0.0.0.0:8888`, allowing other devices on your local network to connect.

For more advanced runtime configuration, see the main [API tuning](https://unsloth.ai/docs/basics/api#unsloth-run-command) section.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/integrations/openclaw.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
