> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/mcp.md).

# How to Use MCP Servers with Local LLMs

Learn how to connect MCP Servers to open AI models with screenshots.

This step-by-step guide shows you how to connect **Model Context Protocol (MCP)** servers to local LLMs like [Qwen](/docs/models/qwen3.6.md) or [Gemma](/docs/models/gemma-4.md), so any model you run can call external tools and services via MCP. Connecting MCP to a local model lets it securely use your local files, apps, databases, and tools instead of only chatting from memory, to build a more useful, private, and interchangeable AI assistant that can act on your real environment.

We'll use the open-source repos [Unsloth](https://github.com/unslothai/unsloth) and [llama.cpp](#llama.cpp-guide) as they are popular frameworks for local model inference/deployment. MCP works for local GGUF models and cloud [provider models](/docs/integrations/connections.md). **We'll also show how** [**multiple MCP Servers**](#using-multiple-mcp-servers) **can be utilized.**

MCP tools work alongside other model capabilities such as [code execution](/docs/new/studio/chat.md#code-execution) and [web search](/docs/new/studio/chat.md#advanced-web-search), so a single model can search the web, run code, and call your connected services in the same thread.

### Use Cases

Once an MCP server is connected, you can ask your local model to do many automated tasks. A few examples:

* **Search docs:** “Find the relevant docs and summarize the setup steps.” - Context7 can be used.
* **Analyze a codebase:** “Map out this repo and explain where authentication, billing, and data access happen.” - The GitHub official MCP and GitMCP can be used to analyze repos.
* **Search the web with embeddings** - Exa's MCP Server can be used for semantic web searches with contextual embedding support.
* **Debug websites UIs** - The Playwright and Chrome DevTools MCP Servers can be used to drive websites to find fixes to issues.

### Quickstart

We'll be using two ways to connect your local model on your device to MCP Servers. Both use open-source packages: [Unsloth](https://github.com/unslothai/unsloth) and [llama.cpp](llama.cpphttps://github.com/ggml-org/llama.cpp) to run, serve and deploy your model.

<a href="/docs/basics/mcp.md#unsloth-guide" class="button primary">Unsloth MCP Guide</a><a href="/pages/txFFdu3I50OSJ0ZpPo0Z#llama.cpp-guide" class="button primary">Llama.cpp MCP Guide</a>

### 🦥 Unsloth Guide

In this example we'll use Unsloth to connect any local model like [Qwen3.6](/docs/models/qwen3.6.md) or [Gemma 4](/docs/models/gemma-4.md) with the MCP Servers: [Vercel](https://mcp.vercel.com), [Context7](https://context7.com/), [Exa](https://exa.ai/) and [Hugging Face](https://huggingface.co/docs/hub/en/agents-mcp). We'll then ask a model what it can do with it. The same steps work for any MCP server.

{% stepper %}
{% step %}

#### Setup Unsloth

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

[See here](/docs/desktop.md#get-started) for detailed instructions.
{% endstep %}

{% step %}

#### **Enable MCP**

Click on "MCP" in the chat toolbar.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FqNVeCtCvYRMqKT9sSZey%2Fimage.png?alt=media&amp;token=9755a1cc-8118-40ba-ba1f-3b9ac0ef773d" alt=""><figcaption></figcaption></figure>

Unsloth Studio by default has MCP support for Context7, Exa and Hugging Face. Turning on Exa [web search](/docs/new/studio/chat.md#advanced-web-search) will disable the default search tool which we have.
{% endstep %}

{% step %}

#### **Adding custom MCP servers**

To add the Vercel MCP server, click on "Add custom MCP", and you will get a pop-up:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FaO9zf15MX1jWL7nOmdyK%2Fimage.png?alt=media&amp;token=8ae977f0-8388-414c-9fbd-ae1efff464f2" alt=""><figcaption></figcaption></figure>

Fill in the server details:

1. **Display name**: a friendly label, e.g. `Vercel`.
2. **URL**: the server's base endpoint, e.g. `https://mcp.vercel.com`.
3. Choose an authentication method below.

{% tabs %}
{% tab title="OAuth sign-in" %}
For servers that require browser-based authentication (GitHub, Linear, Vercel, etc.), turn on **Use OAuth sign-in**. A browser window will open on first connect so you can authorize Unsloth.
{% endtab %}

{% tab title="Custom header" %}
For servers that authenticate with a token, leave OAuth off and click **Add header** under **Custom headers**. Add an `Authorization` header with your token:

```
Authorization: Bearer <your-token>
```

{% endtab %}
{% endtabs %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FbgCzTby2rF3qgleWLNXA%2Fmcp-server-added.png?alt=media&amp;token=8095e37e-a4fa-4857-a5aa-0562af526eca" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### **Test & add**

Click **Test connection** to confirm Unsloth can reach the server. Once it succeeds, click **Add server** to save it.

If **Test connection** fails, check that the URL is the server's base endpoint (not a docs page) and that your authentication method is correct. See Troubleshooting below.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FJeR2x79EkJaG4jYuOiBt%2Fmcp-add-server.png?alt=media&amp;token=38c4fdee-130f-415b-8c5d-e906f13c1555" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### **Verify tools loaded**

The server now appears in the MCP Servers list. Unsloth fetches its tools automatically and shows a confirmation, e.g. *Refreshed "Vercel" (18 tools)*.

Each server has controls to **toggle** it on/off, **refresh** its tools, **edit** it, or **delete** it. Make sure both the server's toggle and the **Use MCP Servers** master toggle are on, then close the dialog.

It'll be highlighted if enabled. You can also disable them by simply clicking on them again.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FgunafFRR6EdrF0xXjIuG%2Fimage.png?alt=media&amp;token=3a91e79f-33d0-44da-a7a3-ded37a34b594" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### **Use it in chat**

Pick any model from the **Select model** dropdown and start chatting. The model can now call the server's tools on its own when your request calls for it.

Above, a local `gemma-4-E2B-it-GGUF` was asked *"Can you use Vercel MCP server?"* and reported the actions it can take: managing projects, analysing logs, listing teams, generating access links, checking domains, and searching Vercel's documentation.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FoenMZ3aZx2yUX9ueAbmy%2Fmcp-chat-usecase.png?alt=media&amp;token=4284a8da-e77f-4961-8154-742cd75e4b01" alt=""><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

#### Using multiple MCP servers

How about calling multiple MCP servers like 3? We'll use Unsloth Studio's default Exa, Context7 & Hugging Face provided MCP servers and enable all 3.

If you ask "Can Unsloth support Qwen finetuning", Exa will provide great details on it:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FbqfXsWpuNJksyX2cLgfz%2Fimage.png?alt=media&amp;token=9f66e3e9-0e78-4016-853d-a7a8b63c4d25" alt=""><figcaption></figcaption></figure>

Then as a follow up "Search Unsloth docs on how to do this", and Context7 is used for docs:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FrPFQ90O4o8SIydVhDndx%2Fimage.png?alt=media&amp;token=35a48ee5-974b-45de-aba9-e9fb1e7833dd" alt=""><figcaption></figcaption></figure>

Then type "Search Hugging Face for unsloth/Qwen models", and Hugging Face's MCP Server will be called:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F9KPBtO3VFxC6Y9e4Hl0d%2Fimage.png?alt=media&amp;token=1c1757dc-4ccb-424f-b98b-29ae173df757" alt=""><figcaption></figcaption></figure>

#### Another Specific Use case Example

Once a server is connected, ask the model to do real work in plain language. A few examples with the Vercel server:

* **Debug a failing build**: *"Pull the build logs for my latest deployment and tell me why it failed."*
* **Check deployment status**: *"List my most recent deployments and their status."*
* **Search the docs**: *"Search the Vercel docs for how to set up a custom domain."*
* **Domain research**: *"Is `myproject.dev` available, and how much would it cost?"*

### 🦙 Llama.cpp Guide

{% stepper %}
{% step %}

#### Install or build llama.cpp

**macOS:**

```bash
brew install llama.cpp
```

Or for **Linux, Windows, WSL** build from source:

```bash
git clone https://github.com/ggml-org/llama.cpp
cmake -S llama.cpp -B llama.cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build llama.cpp/build --config Release -j --target llama-server llama-cli
```

{% endstep %}

{% step %}

#### Start llama-server with a GGUF

We are using [Gemma 4](/docs/models/gemma-4.md) E4B GGUF in this example:

```bash
llama-server \
  -hf unsloth/gemma-4-E4B-it-GGUF:UD-Q4_K_XL \
  --alias local \
  --host 127.0.0.1 \
  --port 8080 \
  --no-ui \
  --temp 1.0 \
  --top-p 0.95 \
  --top-k 64 \
  --reasoning off
```

For the bigger Gemma 4 26B-A4B model:

```bash
llama-server \
  -hf unsloth/gemma-4-26B-A4B-it-GGUF:UD-Q4_K_M \
  --alias local \
  --host 127.0.0.1 \
  --port 8080 \
  --no-ui \
  --temp 1.0 \
  --top-p 0.95 \
  --top-k 64 \
  --reasoning off
```

For more inference parameter adjustments, see our [Gemma 4 guide](/docs/models/gemma-4.md).

You can test the server:

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer none" \
  -d '{
    "model": "local",
    "messages": [{"role": "user", "content": "Say hello in one sentence."}]
  }'
```

{% endstep %}

{% step %}

#### Create an MCP filesystem sandbox

```bash
mkdir -p ~/mcp-workspace
cd ~/mcp-workspace
pwd
```

Copy the absolute path. Create a separate project folder for your MCP host:

```bash
mkdir -p ~/llama-mcp
cd ~/llama-mcp
```

Create `server_config.json`:

{% code expandable="true" %}

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/ABSOLUTE/PATH/TO/mcp-workspace"
      ],
      "env": {}
    }
  }
}
```

{% endcode %}

Replace the path with your real workspace path. IBM’s `mcp-cli` docs use this same `server_config.json` shape and the same `npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/files` filesystem configuration.
{% endstep %}

{% step %}

#### Run a terminal MCP host against llama.cpp

Use IBM’s `mcp-cli`; it is a command-line MCP client/host with chat mode, tool discovery, and custom OpenAI-compatible provider support. Its docs recommend `uvx mcp-cli --help`, support project `server_config.json`, and support runtime custom OpenAI-compatible providers via `--api-base` and `--api-key`.

`mcp-cli` needs a config file to start up. So it's necessary to add a step to create it. For example:

{% code title="" expandable="true" %}

```bash
mkdir -p ~/.chuk_llm
cat > ~/.chuk_llm/config.yaml <<'YAML'
openai_compatible:
  client_class: "chuk_llm.llm.providers.openai_client:OpenAILLMClient"
  default_model: "local"
  models: ["*"]
YAML
```

{% endcode %}

Then run:

```bash
uvx mcp-cli \
  --provider llamacpp \
  --api-base http://127.0.0.1:8080/v1 \
  --api-key none \
  --model local \
  --server filesystem \
  --config-file server_config.json
```

Then try:

```
List the files in the filesystem workspace.
```

Then:

```
Create hello.txt with a one-line greeting, then read it back.
```

`mcp-cli` has tool-call confirmation enabled by default, so you should see prompts before tool execution.

**Full code example:**

{% code expandable="true" %}

```bash
# terminal 1
llama-server -hf unsloth/gemma-4-E4B-it-GGUF:UD-Q4_K_XL \
  --alias local --host 127.0.0.1 --port 8080 --no-ui \
  --temp 1.0 --top-p 0.95 --top-k 64 \
  --chat-template-kwargs '{"enable_thinking":false}'

# terminal 2, in the folder with server_config.json
uvx mcp-cli \
  --provider llamacpp \
  --api-base http://127.0.0.1:8080/v1 \
  --api-key none \
  --model local \
  --server filesystem \
  --config-file server_config.json
```

{% endcode %}
{% endstep %}
{% endstepper %}

### Local MCP servers with Remote access or LAN access

Besides `http(s)://` URLs, the **URL or executable** field also accepts a local command such as `npx`, `uvx` or the path to a server binary, with its arguments in the **Arguments** rows. These local (stdio) servers run as a program on your computer.

While **Remote access** or **LAN access** is on in Settings (or Unsloth was started with `--secure`), Unsloth is reachable from other devices, so local commands are turned off and saving one shows:

{% code collapsedlinecount="10" %}

```
Local commands are disabled while Remote Access is on, because the server is reachable from outside this machine.
```

{% endcode %}

You can still use local MCP servers in two ways:

1. **Run the server over HTTP on your own machine (recommended).** Many MCP servers can serve HTTP themselves. Start it bound to `127.0.0.1` so only this computer can reach it, then add its address as the URL. For example, for [osmmcp](https://github.com/nervsystems/osmmcp):

   <pre class="language-bash" data-collapsed-line-count="10"><code class="lang-bash">osmmcp --enable-http --http-only --http-addr 127.0.0.1:7082
   </code></pre>

   Then add `http://127.0.0.1:7082/mcp` in the MCP dialog. This works in Unsloth Desktop and Studio with Remote access on. Run the MCP server on the computer running Unsloth, not on the device you browse from; with [Docker](/docs/get-started/install/docker.md), `127.0.0.1` is the container itself, so start the server inside the container (`docker exec`). For a server that only speaks stdio, an stdio-to-HTTP bridge such as [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy) does the same job, e.g. `mcp-proxy --port=8099 uvx mcp-server-fetch`, then add `http://127.0.0.1:8099/mcp`.
2. **Allow local commands explicitly (Studio).** Start Studio with the variable set yourself, and local commands stay enabled while Remote access or LAN access is on:

   <pre class="language-bash" data-collapsed-line-count="10"><code class="lang-bash">UNSLOTH_STUDIO_ALLOW_STDIO_MCP=1 unsloth studio
   </code></pre>

   On Windows PowerShell: `$env:UNSLOTH_STUDIO_ALLOW_STDIO_MCP = "1"; unsloth studio`.

{% hint style="warning" %}
With option 2, anyone who can sign in to your Studio over the network can run programs on your computer through an MCP server. Only use it with a strong password on networks you trust, and prefer option 1.
{% endhint %}

### Troubleshooting

If a server fails to connect or its tools don't appear, check the URL is the server's base endpoint (e.g. `https://mcp.vercel.com`), not a docs or dashboard page. For OAuth servers, complete the browser sign-in when it opens; for token-based servers, verify the `Authorization` header and that the token is valid.

If saving a local command fails with "Local commands are disabled while Remote Access is on", see [Local MCP servers with Remote access or LAN access](#local-mcp-servers-with-remote-access-or-lan-access).

Click **Refresh** if tools don't show up after connecting, and make sure both the individual server toggle and the **Use MCP Servers** master toggle are on.

### Security notes

Only connect MCP servers you trust. Review requested permissions and keep human confirmation enabled for actions that read private data, change deployments, purchase domains, or modify projects. Be especially careful when combining MCP servers with web search or other tools, because prompt-injected content can try to trigger unwanted tool calls.

### Popular MCP Servers

Here is a list of some popular and useful MCP Servers you can connect to:

| MCP server                       | Best for                                 | Why it’s useful                                                                                                                                                                                                  |
| -------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub MCP**                   | Repos, issues, PRs, code search, Actions | Official GitHub MCP with remote and local setup, covering repos, issues, pull requests, Actions, code security, and more. ([GitHub](https://github.com/github/github-mcp-server))                                |
| **Context7**                     | Fresh library docs and examples          | Pulls current, version-specific docs for coding assistants instead of relying on stale training data. Uses `https://mcp.context7.com/mcp`. ([GitHub](https://github.com/upstash/context7))                       |
| **Notion MCP**                   | Docs, notes, tasks, project knowledge    | Good for teams using Notion for specs, PRDs, roadmaps, or notes. Hosted MCP can read and write workspace content. ([Notion Developers](https://developers.notion.com/guides/mcp/overview))                       |
| **Slack MCP**                    | Team conversation search                 | Lets AI tools query Slack messages, channels, files, threads, and member info; actions depend on permissions. ([Slack](https://slack.com/help/articles/48855576908307-Guide-to-the-Slack-MCP-server))            |
| **Linear MCP**                   | Issues, projects, product workflows      | Official remote MCP for finding, creating, and updating Linear issues, projects, comments, and related objects. ([Linear](https://linear.app/changelog/2025-05-01-mcp))                                          |
| **Vercel MCP**                   | Deployments, logs, docs, domains         | Useful for frontend/web workflows: inspect deployments, logs, docs, and project context. Check client compatibility first. ([Vercel](https://vercel.com/docs/agent-resources/vercel-mcp?utm_source=chatgpt.com)) |
| **Sentry MCP**                   | Production debugging                     | Helps agents inspect Sentry issues, traces, errors, and performance data in human-in-the-loop dev workflows. ([GitHub](https://github.com/getsentry/sentry-mcp))                                                 |
| **Filesystem / local files MCP** | Local project files                      | Useful for local LLM setups, usually via `stdio`. Reference servers are best treated as examples or starting points. ([GitHub](https://github.com/modelcontextprotocol/servers))                                 |


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/mcp.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
