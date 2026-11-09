> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/integrations/unsloth-start.md).

# Run Coding Agents with Local LLMs using Unsloth Start

Unsloth lets you connect [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md), Hermes, OpenCode, and other coding agents to a local model via the `unsloth start` command. The entire workflow can run offline on your own hardware. [Unsloth](/docs/desktop.md) automatically configures the endpoint, API key, provider, model, and context length for each launch, so you can use your preferred agent without modifying them. This guide will show you how to launch models from the command line for offline use, and connect to Unsloth.

{% columns %}
{% column width="58.333333333333336%" %}

### Quickstart

First, make sure you have [Unsloth installed](/docs/new/studio/install.md). Then open Unsloth, load a model, go to your project folder, and run the command in terminal:

```bash
unsloth start claude
```

You can replace `claude` with any agent below:
{% endcolumn %}

{% column width="41.666666666666664%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FpXE6kCHjh8qOEaggf94M%2FScreenshot_20260718_122426.png?alt=media&amp;token=a59e4c8c-efdb-451b-b1f8-621955564f6d" alt=""><figcaption><p>Claude Code running with Qwen3.5 locally.</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

| Agent                                                              | Command                  |
| ------------------------------------------------------------------ | ------------------------ |
| <i class="fa-claude">:claude:</i> Claude Code                      | `unsloth start claude`   |
| <i class="fa-openai">:openai:</i> OpenAI Codex                     | `unsloth start codex`    |
| <i class="fa-vscode">:vscode:</i> Visual Studio Code               | `unsloth start vscode`   |
| <i class="fa-deepseek">:deepseek:</i> DeepSeek Harness             | `unsloth start dsh`      |
| <i class="fa-rectangle-vertical">:rectangle-vertical:</i> OpenCode | `unsloth start opencode` |
| <i class="fa-caduceus">:caduceus:</i> Hermes Agent                 | `unsloth start hermes`   |
| <i class="fa-lobster">:lobster:</i> OpenClaw                       | `unsloth start openclaw` |
| <i class="fa-pi">:pi:</i> Pi Agent                                 | `unsloth start pi`       |

Unsloth uses temporary or session-scoped provider configuration. It does not add an Unsloth provider to the agent's normal configuration files.

### Agent Guides

<table data-column-title-hidden data-view="cards"><thead><tr><th>Title</th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td>Claude Code</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FT8nv3UJzIrcxmjSn8OfW%2Fclaude-code.webp?alt=media&amp;token=811f9635-7321-427c-a11e-29a40e49e376">claude-code.webp</a></td><td><a href="/docs/basics/claude-code.md">Claude Code</a></td></tr><tr><td>Codex</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FLxRuVHEBYywquhRGBYu0%2Fcodex%20only%20logo.png?alt=media&amp;token=7faa9cbd-090a-45dc-9d5e-acb1a9591f27">codex only logo.png</a></td><td><a href="/docs/basics/codex.md">OpenAI Codex</a></td></tr><tr><td>Visual Studio Code</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FsBmg9gZ062wIQDAuibJ7%2Fvscode-card.png?alt=media&amp;token=1659960f-0876-4469-a6a7-7408e7a6570a">vscode-card.png</a></td><td><a href="/docs/integrations/how-to-run-local-ai-models-in-vs-code.md">Run models in VS Code</a></td></tr><tr><td>Hermes Agent</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F6ysPTzsXIO5diu4vOTCh%2Fimages.jpeg?alt=media&amp;token=5cc58141-69eb-4450-8214-7a8421fbe2a5">images.jpeg</a></td><td><a href="/docs/integrations/hermes-agent.md">Hermes Agent</a></td></tr><tr><td>OpenClaw</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FAd5uo6LjavtBrrKZfwZ3%2Fopenclaw-hero-light.png?alt=media&amp;token=3097e40f-e80c-4c9c-8efc-02ecf5530ef6">openclaw-hero-light.png</a></td><td><a href="/docs/integrations/openclaw.md">OpenClaw</a></td></tr><tr><td>OpenCode</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FlCi6Ab4f2qLlNj2EWGL0%2Fopencodelogo.png?alt=media&amp;token=6118773e-5392-4718-a431-a50157a34cbe">opencodelogo.png</a></td><td><a href="/docs/integrations/opencode.md">OpenCode</a></td></tr></tbody></table>

### Load a model from the command line

<div align="center"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FAOqECGHODYPDGeYDpXOz%2Fwasim%20unslothstart.png?alt=media&amp;token=a7a1bf5e-d964-4bd4-a0d0-f86753e9f5a8" alt="unsloth start launching Codex with a local GGUF model in Unsloth Studio" width="563"><figcaption><p>Unsloth start finds or loads the model, configures the coding agent and launches it from the current project.</p></figcaption></figure></div>

You can select and load a model while launching the agent:

{% hint style="success" %}
If there are no settings/sampling flags set, Unsloth automatically selects the best/recommended settings for the model including context length, temperature etc.
{% endhint %}

```bash
unsloth start claude \
  --model unsloth/Qwen3.8-27B-GGUF:UD-Q4_K_XL \
  --context-length 32768 \
  --temp 1.0 \
  --top-p 0.95 \
  --top-k 20 \
  --min-p 0.0 \
  --reasoning-effort medium
```

The `:UD-Q4_K_XL` suffix selects the GGUF quant.

On the default local address, passing `--model` lets `unsloth start` start a temporary server when Unsloth Studio is not already running. The temporary server stops when the agent exits. If Unsloth is already running, the command connects to it and leaves it running.

See below for examples of agents being connected to a local LLM:

{% columns %}
{% column width="50%" %}

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fmhay2zcaqL5mNNBeYwKv%2FScreenshot_20260717_163314.png?alt=media&amp;token=5a1e2f04-92b1-42f1-adac-9494fb43613a" alt=""><figcaption><p>OpenCode</p></figcaption></figure></div>

{% endcolumn %}

{% column width="50%" %}

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FnrT2lJtpD4uwMkn5HAhO%2FScreenshot_20260717_163427.png?alt=media&amp;token=ffe77a32-05a9-439e-845f-5a7a4b034464" alt=""><figcaption><p>Hermes</p></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column width="33.33333333333333%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FfKxk4eUVf0tZB1IFtava%2FScreenshot_20260717_161638.png?alt=media&amp;token=b709f099-704e-4d97-947e-d75cbf43cd8a" alt=""><figcaption><p>Claude Code</p></figcaption></figure>
{% endcolumn %}

{% column width="33.33333333333333%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FxPckgHYLacJK1jpwXHOR%2FScreenshot_20260717_163145.png?alt=media&amp;token=e61f7404-341e-474b-bc08-59adc66ce274" alt=""><figcaption><p>Codex</p></figcaption></figure>
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fy5QNC3RaSkCIr1KFBrMd%2FScreenshot_20260717_163831.png?alt=media&amp;token=e1501dbe-6a2b-4a4d-96df-92a3e8f2f3df" alt=""><figcaption><p>Openclaw</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

### Connect to a remote Unsloth server

Set the Unsloth URL and API key before launching an agent:

```bash
export UNSLOTH_STUDIO_URL=https://studio.example.com
export UNSLOTH_API_KEY=sk-unsloth-...
unsloth start claude
```

You can also pass the key with `--api-key`. For a verified local Unsloth server, `unsloth start` creates or reuses the API key automatically.

#### Use Unsloth in VS Code

Connect a local model to VS Code’s Copilot Chat. Requires the GitHub Copilot Chat extension; no Copilot plan needed.

```bash
# Connect the model Unsloth is already serving
unsloth start vscode

# Or load a model with 32K context for Agent mode
unsloth start vscode unsloth/Qwen3.5-4B-GGUF:UD-Q4_K_XL --context-length 32768
```

Open Copilot Chat and select your model under **Unsloth**. If it is missing, check **Manage Models** or run **Developer: Reload Window**.

Agent mode needs tool-calling support and at least **32K context**. Use Ask mode for models without tool calling.

The command backs up your VS Code configuration and preserves other models. After switching models, re-run `unsloth start vscode` to update its entry.

**Remote servers:** In an SSH or container session without a VS Code user directory, the command prints the configuration to add locally, plus connection or port-forwarding instructions. Use a local VS Code window if the model is missing from the remote workspace’s model picker.

### Flags + Options

If there are no settings/sampling flags set, Unsloth automatically selects the best/recommended settings for the model including context length, temperature etc.

Otherwise, you can customize these flags accordingly:

| Option                                       | What it does                                                                                                                                            |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model`, `-m`                              | Select a model. Without it, use the first model reported by Unsloth.                                                                                    |
| `--api-key`                                  | Supply a Unsloth API key. You can also set `UNSLOTH_API_KEY`.                                                                                           |
| `--launch` / `--no-launch`                   | Launch the agent or print the generated environment and command.                                                                                        |
| `--serve` / `--no-serve`                     | Allow or prevent automatic local server startup.                                                                                                        |
| `--gguf-variant`                             | Select a GGUF quantization variant.                                                                                                                     |
| `--reasoning`                                | Use reasoning in the chat: on, off, or auto. Auto follows the model's chat template, which usually means on.                                            |
| `--reasoning-effort`                         | Reasoning effort passed to the model's chat template, e.g. medium. Levels are per model, so use one that model accepts. Unset keeps the template's own. |
| `--context-length`, `--max-seq-length`       | Set the requested context length when loading the model.                                                                                                |
| `--load-in-4bit` / `--no-load-in-4bit`       | Control 4-bit loading for non-GGUF Hugging Face models.                                                                                                 |
| `--tensor-parallel` / `--no-tensor-parallel` | Enable or disable tensor-parallel GGUF loading for multi-GPU systems.                                                                                   |
| `--persist` / `--no-persist`                 | Keep the Unsloth-managed agent home where applicable.                                                                                                   |
| `--yolo`                                     | Use the selected agent's non-prompting or trust mode.                                                                                                   |
| `-h`, `--help`                               | Show command help.                                                                                                                                      |

Load options are used when Unsloth needs to load or reconcile the requested model.

### Pass normal commands to the agent

Arguments that are not Unsloth options are passed to the selected agent:

```bash
unsloth start claude --continue
unsloth start codex --persist resume --last
unsloth start opencode run --continue "Continue the previous task"
unsloth start pi --persist --continue
```

Use the agent's own help command for its complete list of native options.

### Sessions and `--persist`

`--persist` keeps managed storage. It does not resume a conversation by itself; also pass the agent's normal resume command.

| Agent           | Do you need `--persist`?                                              | Resume example                                                   |
| --------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Claude Code     | No. Claude uses its normal session store.                             | `unsloth start claude --continue`                                |
| OpenAI Codex    | Yes. Its managed Codex home is temporary by default.                  | `unsloth start codex --persist resume --last`                    |
| OpenClaw        | Yes. Managed config, workspace and sessions are temporary by default. | Use `--persist` with the same native session ID.                 |
| OpenCode        | No. OpenCode uses its normal session store.                           | `unsloth start opencode run --continue "Continue"`               |
| Hermes Agent    | Yes. Its managed Hermes home is temporary by default.                 | `unsloth start hermes --persist --continue --oneshot "Continue"` |
| Pi Coding Agent | Yes. Its managed Pi home is temporary by default.                     | `unsloth start pi --persist --continue`                          |

For Codex, OpenClaw, Hermes and Pi, use `--persist` from the first launch and again when returning to the session.

{% tabs %}
{% tab title="Codex" %}

```bash
unsloth start codex --persist
unsloth start codex --persist resume --last
```

{% endtab %}

{% tab title="OpenClaw" %}
Use a stable session ID for a named session:

```bash
unsloth start openclaw --persist \
  agent --local --session-id my-session --message "Inspect this repository"

unsloth start openclaw --persist \
  agent --local --session-id my-session --message "Continue"
```

{% endtab %}

{% tab title="Hermes Agent" %}

```bash
unsloth start hermes --persist --oneshot "Inspect this repository"
unsloth start hermes --persist --continue --oneshot "Continue"
```

{% endtab %}

{% tab title="Pi Coding Agent" %}

```bash
unsloth start pi --persist --print "Inspect this repository"
unsloth start pi --persist --continue --print "Continue"
```

{% endtab %}
{% endtabs %}

#### Print the launch command without running it

```bash
unsloth start claude --no-launch
```

This prints the generated environment and command. The output can contain connection credentials, so do not publish it in logs or screenshots.

### Permission-bypass mode

`--yolo` maps to the selected agent's trust or non-prompting mode. It can reduce approval prompts and allow the agent to run commands without asking first.

{% hint style="warning" %}
Only use it in an environment where unrestricted agent actions are acceptable.
{% endhint %}

#### Common issues

<details>

<summary>No Unsloth server was found</summary>

Start Unsloth and load a model, or pass \`--model\` so Unsloth can start a temporary local server.

</details>

<details>

<summary>Codex does not connect</summary>

Use a GGUF model running through \`llama-server\`. The current Codex integration does not use the Unsloth transformers backend.

</details>

<details>

<summary>A session was not restored</summary>

For Codex, OpenClaw, Hermes and Pi, use \`--persist\` on the first and later launches, then pass the agent's native resume option.

</details>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/integrations/unsloth-start.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
