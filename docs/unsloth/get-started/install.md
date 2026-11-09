> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/install.md).

# Unsloth Installation

Install Unsloth Desktop, Unsloth Studio, or Unsloth Core.

Unsloth can be installed in three distinct ways: [**Unsloth Desktop**](/docs/desktop.md), the native app; [**Unsloth Studio**](/docs/new/studio.md), the browser-based web UI; or **Unsloth Core**, the original code-based Python package.

### Unsloth Desktop

Download the native desktop app for your operating system:

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

### Unsloth Studio

**Unsloth Studio** is our web-based UI. Follow the instructions below to install it natively:

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
**Install Unsloth:**

```bash
brew install --cask unsloth
```

Update Unsloth:

```bash
brew upgrade --cask unsloth
```

{% endtab %}

{% tab title="WinGet" %}
**Install Unsloth:**

```powershell
winget install --id UnslothAI.Unsloth -e
```

Update Unsloth:

<pre class="language-powershell"><code class="lang-powershell"><strong>winget upgrade --id UnslothAI.Unsloth -e
</strong></code></pre>

{% endtab %}
{% endtabs %}

For requirements and advanced options, see the [Unsloth Studio installation guide](https://unsloth.ai/docs/new/studio/install).

### Unsloth Core

**Unsloth Core** is the original Python package for code-based training and inference. Follow the [uv, pip, and virtual environment guide](https://unsloth.ai/docs/get-started/install/pip-install).

<table data-view="cards"><thead><tr><th data-type="content-ref"></th><th data-hidden data-card-cover data-type="image">Cover image</th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><a href="/docs/get-started/install/mac.md">MacOS</a></td><td></td><td><a href="/docs/get-started/install/mac.md">MacOS</a></td></tr><tr><td><a href="/docs/get-started/install/windows-installation.md">Windows</a></td><td></td><td><a href="/docs/get-started/install/windows-installation.md">Windows</a></td></tr><tr><td><a href="/docs/get-started/install/pip-install.md">uv, pip install &amp; venv</a></td><td></td><td><a href="/docs/get-started/install/pip-install.md">uv, pip install &amp; venv</a></td></tr><tr><td><a href="/docs/get-started/install/docker.md">Docker</a></td><td></td><td><a href="/docs/get-started/install/docker.md">Docker</a></td></tr><tr><td><a href="/docs/get-started/install/linux.md">Linux</a></td><td></td><td><a href="/docs/get-started/install/linux.md">Linux</a></td></tr><tr><td><a href="/docs/basics/amd.md">AMD</a></td><td></td><td><a href="/docs/basics/amd.md">AMD</a></td></tr><tr><td><a href="/docs/get-started/install/updating.md">Updating</a></td><td></td><td><a href="/docs/get-started/install/updating.md">Updating</a></td></tr><tr><td><a href="/docs/get-started/install/intel.md">Intel</a></td><td></td><td></td></tr><tr><td><a href="/docs/get-started/install/conda-install.md">Conda</a></td><td></td><td><a href="/docs/get-started/install/conda-install.md">Conda</a></td></tr><tr><td><a href="/docs/get-started/install/vs-code.md">VS Code</a></td><td></td><td></td></tr><tr><td><a href="/docs/get-started/install/google-colab.md">Google Colab</a></td><td></td><td><a href="/docs/get-started/install/google-colab.md">Google Colab</a></td></tr></tbody></table>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/install.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
