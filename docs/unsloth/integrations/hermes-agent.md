> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/integrations/hermes-agent.md).

# How to Run Local AI Models with Hermes Agent

Guide on using open LLMs with Hermes Agent locally.

This guide enables you to run open LLMs locally with **Hermes Agent** via [**Unsloth**](https://github.com/unslothai/unsloth). Hermes Agent by Nous Research is an **open-source** autonomous AI agent that connects to a model endpoint, executes tasks, and improves over time through memory and learned skills.

{% columns %}
{% column width="58.333333333333336%" %}
Hermes will work with any **local model** exposed through Unsloth’s **OpenAI-compatible API**, including: DeepSeek, Qwen, Gemma, and more. Hermes acts as the agent client, while Unsloth loads and serves models via the [local API](/docs/basics/api.md) entirely offline.

After setup, every prompt sent through Hermes will run using your local model on your device.
{% endcolumn %}

{% column width="41.666666666666664%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FYhiTzkyz0fVPMxIfWg6D%2FScreenshot_20260718_122219.png?alt=media&amp;token=a8063d58-0d49-467a-aa2a-35b30c448390" alt=""><figcaption><p>Qwen3.5 running locally in Hermes via Unsloth.</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

<a href="https://unsloth.ai/docs/integrations/hermes-agent#setup-hermes-agent" class="button primary" data-icon="caduceus">Setup Hermes</a><a href="https://unsloth.ai/docs/integrations/hermes-agent#integrate-hermes-with-unsloth-api" class="button primary">🦥 Connect your local model</a>

{% hint style="info" %}
In this tutorial, you’ll install Hermes and configure it to use `unsloth/Qwen3.6-27B-GGUF` served from Unsloth. Prefer a different model? Swap in any other model by loading it in Unsloth and updating the configuration.
{% endhint %}

### <i class="fa-caduceus">:caduceus:</i> Setup Hermes Agent

**Prerequisites:**

The [Hermes](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/installation.md) command-line installer supports Linux, macOS, and WSL2. Make sure **Git** is installed; on Linux, also install **curl** and **xz-utils**. The installer automatically provisions `uv`, Python 3.11, Node.js 22, `ripgrep`, and `ffmpeg`.

#### 1. Run the installer

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

The installer:

* Detects your platform and checks dependencies.
* Clones Hermes to `~/.hermes/hermes-agent/`.
* Creates a Python virtual environment and installs the Python dependencies.
* Installs the browser-tool dependencies and Playwright’s Chromium engine.
* Adds the `hermes` command and launches the setup wizard.

{% columns %}
{% column %}
Playwright may request `sudo` to install Chromium’s shared system libraries. Hermes itself does not require root access.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FnabBNaHLvb1rH58cQwyC%2FScreenshot%202026-07-18%20at%205.31.57%E2%80%AFAM.png?alt=media&amp;token=4ac35864-89aa-45ce-84db-ad5b17f8b3e5" alt="" width="375"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

#### **2. Reload your shell** so the `hermes` command is on your `PATH`:

{% code title="bash" %}

```bash
source ~/.bashrc
```

{% endcode %}

{% code title="zsh" %}

```bash
source ~/.zshrc
```

{% endcode %}

#### **3. Verify the install:**

```bash
hermes --version
```

If the command resolves, Hermes is installed. Everything lives under `~/.hermes/`:

| Path                                    | What it is                                     |
| --------------------------------------- | ---------------------------------------------- |
| `~/.hermes/config.yaml`                 | Main settings (model, provider, tools, TTS, …) |
| `~/.hermes/.env`                        | API keys and other secrets                     |
| `~/.hermes/hermes-agent/`               | The Hermes source + virtualenv                 |
| `~/.hermes/cron/`, `sessions/`, `logs/` | Runtime data                                   |
| `~/.hermes/skills/`                     | Installed skills (synced from the Skills Hub)  |

{% hint style="info" %}
Full install reference: [hermes-agent.nousresearch.com/docs/getting-started/installation](https://hermes-agent.nousresearch.com/docs/getting-started/installation). If the installer reports a missing prerequisite, install it and re-run the one-liner. The installer is idempotent.
{% endhint %}

### ⚡ Quickstart

After installing Hermes, we'll need to install Unsloth Desktop to enable Hermes to serve and run inference of local models.

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

### Unsloth is now ready

To start chatting, type a message and press Enter.

**Connect Hermes.** Run `unsloth start hermes` in your terminal while Unsloth is open. It mints an API key, writes the config, and launches Hermes against your loaded model.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FpAGvwjGD0iVMZKBoyu7m%2Fgreeennn.png?alt=media&amp;token=d17a5528-8375-444c-9aff-f9e9f7903bcd" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### ⚡ Run Hermes Agent with `unsloth start`

To launch Hermes directly with a model, run:

```bash
unsloth start hermes \
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

With a model loaded in Unsloth Studio, run:

```bash
unsloth start hermes
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FOaFdKwRASHSoxDQx06l5%2FScreenshot_20260714_152023.png?alt=media&amp;token=c7e13fb2-e03e-49d1-8efa-f7494578943a" alt="Hermes Agent connected to a local model through Unsloth Studio"><figcaption><p>Hermes Agent running through its Unsloth Studio provider.</p></figcaption></figure>

Unsloth launches Hermes from a separate managed home with the Unsloth provider, model, and context settings already configured. Your existing Hermes setup is left unchanged.

This managed home is temporary by default. To keep your sessions and state, add `--persist` from your first launch:

```bash
unsloth start hermes --persist
```

To return to your latest session later, run:

```bash
unsloth start hermes --persist --continue
```

To reopen a specific session, use `--resume <session-id-or-title>` instead.

See the complete [unsloth start](/docs/integrations/unsloth-start.md) reference for model selection, remote connections, and advanced options.

The setup wizard below remains available if you prefer to manage the Hermes provider yourself.

### 🔑 Creating an API key

1. Open the sidebar, click your **Unsloth** avatar at the bottom-left.
2. Go to **Settings** → **API**.
3. Enter a friendly name (e.g. `hermes-agent-macbook`).
4. *(Optional)* Set an expiry.
5. Click **Create**.
6. **Copy the key immediately.** Unsloth stores only a hash and you won't be able to view it again.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FrWnqY5PgvZdbWK8pmlD5%2Fimage.png?alt=media&amp;token=3507e7d7-b552-447f-b503-2418802b8f6e" alt="" width="375"><figcaption></figcaption></figure>

All keys start with the `sk-unsloth-` prefix. Revoke a key from the same page at any time. Requests made with a revoked key will fail with `401 Unauthorized`.

### 🦥 Integrate Hermes with Unsloth API

Hermes sends each chat turn to a configured inference provider and connects to **OpenAI-compatible** endpoints. Configure the provider during installation or later in the setup wizard.

**1. Open the setup wizard:**

{% columns %}
{% column %}

```bash
hermes setup
```

Pick **Model & Provider** from the "What would you like to do?" menu to configure only the inference endpoint, or **Full Setup** to walk through everything (TTS, tools, messaging gateway, agent settings).
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FChF6By1Dl44hVQl63kGW%2FScreenshot%202026-07-18%20at%205.34.39%E2%80%AFAM.png?alt=media&amp;token=371a287e-1264-47d2-af3e-fa3ed302e038" alt="" width="539"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

**2. Select the Custom OpenAI-compatible endpoint** when Hermes prompts you for an inference provider.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FA5VVaVsL7GzZGq9Dn3Bt%2Fhermes_agent_setup_2.png?alt=media&amp;token=a234d29d-14f6-431f-be1f-9a4e14f5951d" alt="" width="563"><figcaption></figcaption></figure>

**3. Fill in the prompts** as Hermes walks through them:

| Prompt                                | Value                                                      |
| ------------------------------------- | ---------------------------------------------------------- |
| **API base URL**                      | `http://localhost:8888/v1` *(your Unsloth port + `/v1`)*   |
| **API key**                           | Your `sk-unsloth-…` key                                    |
| **Detected model: … Use this model?** | `Y` *(Hermes auto-detects the model via `GET /v1/models`)* |
| **Context length in tokens**          | *(leave blank for auto-detect)*                            |
| **Display name**                      | Anything you like, e.g. `unsloth-api`                      |

Hermes verifies the endpoint against `/v1/models` and confirms the detected model before continuing.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FehQjrLJ0ztoSdNp94dfH%2Fhermes_agent_setup_3.png?alt=media&amp;token=641c6e6a-44c3-4013-8c08-32472b256283" alt=""><figcaption></figcaption></figure>

**4. Accept defaults for the remaining prompts** (TTS, tools, messaging gateway, agent settings) you can reconfigure any of them later. Hermes writes everything to `~/.hermes/config.yaml` and `~/.hermes/.env`.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FWbj2YWKpXw9T2jR0QQjh%2Fhermes_agent_setup_5.png?alt=media&amp;token=59985534-69e3-46ec-8ab9-1db8829c1721" alt=""><figcaption></figcaption></figure>

**5. Launch Hermes:**

```bash
hermes
```

The startup banner shows your Unsloth model name in the status bar (e.g. `unsloth/Qwen3.6-27B-GGUF`), and the prompt is ready for input.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FU8UlRyw9n1SrENvZXSjD%2Fhermes_unsloth_run.png?alt=media&amp;token=6fd14920-a287-4aed-815e-33b7e4d09c68" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
To reconfigure just the model later, run `hermes setup model`. To edit the config file directly, `hermes config edit` opens `~/.hermes/config.yaml` in your `$EDITOR`.
{% endhint %}

### Optional: tune the Unsloth server

`unsloth run` starts the local API server and loads a model for your app to connect to. You can also customize how the server behaves when starting it.

```bash
# Serve Hermes (--disable-tools passes the agent's own tools through)
unsloth run \
  --model unsloth/gemma-4-26B-A4B-it-GGUF \
  --disable-tools \
  --reasoning off \
  -p 8888
```

{% hint style="warning" %}
Use `--disable-tools` when driving Hermes (or any external agent with its own tools). By default Unsloth Studio runs its own server-side tools, which swallows the agent's tool calls, so Hermes answers but never runs its tools. `--disable-tools` switches to passthrough, so Hermes's own tools are used.
{% endhint %}

Use `--reasoning off` to turn thinking off, or `--reasoning on` to turn it on for models that support reasoning.

```bash
# Expose the API on your local network
unsloth run \
  --model unsloth/gemma-4-26B-A4B-it-GGUF \
  -H 0.0.0.0 \
  -p 8888
```

This starts the server on `0.0.0.0:8888`, allowing other devices on your local network to connect. `-p` changes which port the server runs on. If you want phones, laptops, or other devices on your network to connect to the API server, start it with `-H 0.0.0.0`.

Some apps may still override generation settings for individual requests. For more advanced runtime configuration, see the main [API tuning](https://unsloth.ai/docs/basics/api#unsloth-run-command) section.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/integrations/hermes-agent.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
