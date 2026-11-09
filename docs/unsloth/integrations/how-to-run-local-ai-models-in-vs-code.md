> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/integrations/how-to-run-local-ai-models-in-vs-code.md).

# How to Run Local AI Models in VS Code

How to Run Local LLMs with VS Code

This guide shows you how to connect a local model running in Unsloth to VS Code’s Copilot Chat. Unsloth loads and serves the model, while VS Code provides the chat interface and coding tools.

You can chat about your code, ask questions, and use Agent mode to create and edit files with a model that supports tool calling.

### Install VS Code

{% tabs %}
{% tab title="macOS" %}
{% stepper %}
{% step %}

#### Download VS Code

Open the [VS Code download page](https://code.visualstudio.com/download) and download the macOS version for your Mac. Choose **Apple silicon**, **Intel**, or **Universal** if you’re unsure.
{% endstep %}

{% step %}

#### Setup VS Code

Open the downloaded `.zip` file, then drag **Visual Studio Code.app** into your **Applications** folder.

Then to open, go to **Applications** and double-click **Visual Studio Code**.
{% endstep %}
{% endstepper %}
{% endtab %}

{% tab title="Windows" %}
{% stepper %}
{% step %}

#### Download VS Code

Open the [VS Code download page](https://code.visualstudio.com/download) and download the Windows **User Installer** for your device. Most PCs use **x64**.
{% endstep %}

{% step %}

#### Setup VS Code

Open the downloaded `.exe` file and follow the installer prompts.

Then to open, go to the Start menu, search for **Visual Studio Code**, and launch it.

If you had a terminal open during installation, close and reopen it to pick up the updated PATH.
{% endstep %}
{% endstepper %}
{% endtab %}

{% tab title="Linux" %}
{% stepper %}
{% step %}

#### Download VS Code

Open the [VS Code download page](https://code.visualstudio.com/download) and choose the package for your distribution:

* **Ubuntu or Debian:** `.deb`
* **Fedora or RHEL:** `.rpm`
  {% endstep %}

{% step %}

#### Setup VS Code

Open a terminal in the folder containing your download and run:

**Ubuntu or Debian:**

```bash
sudo apt install ./code_*.deb
```

**Fedora or RHEL:**

```bash
sudo dnf install ./code-*.rpm
```

Then to open, go to your application launcher, search for **Visual Studio Code**, and launch it.
{% endstep %}
{% endstepper %}
{% endtab %}
{% endtabs %}

### ⚡ Quickstart

After installing VS Code, we'll need to install [Unsloth Desktop](/docs/desktop.md) to enable VS Code to serve and run inference of local models.

{% stepper %}
{% step %}

#### Download Unsloth

The easiest way to get started is by installing the Unsloth Desktop app. It supports [MacOS](/docs/get-started/install/mac.md), Linux, [Windows](/docs/get-started/install/windows-installation.md), [NVIDIA](/docs/get-started/install/pip-install.md), [AMD](/docs/get-started/install/amd.md), Intel and CPU setups.

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

Or, if you prefer manual installation:

{% tabs %}
{% tab title="Native install" %}
**MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

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

With your model loaded in Unsloth, run this in your terminal:

```bash
unsloth start vscode
```

Open **Copilot Chat** in VS Code and select your model under **Unsloth** in the model picker. Send a message to check the connection.

Keep Unsloth running while you use the model.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FpAGvwjGD0iVMZKBoyu7m%2Fgreeennn.png?alt=media&amp;token=d17a5528-8375-444c-9aff-f9e9f7903bcd" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### 🔌Connect your model

With a model loaded in Unsloth, open a terminal and run:

```bash
unsloth start vscode
```

This adds the model Unsloth is currently serving to VS Code’s model picker. It configures the connection; open VS Code separately if it isn’t already running.

You can also load a model and configure VS Code in one command:

```bash
unsloth start vscode --model unsloth/Qwen3.8-27B-GGUF:UD-Q4_K_XL --context-length 32768
```

Prefer another model? Replace the model ID with your choice. You can also pass a local GGUF file:

```bash
unsloth start vscode --model "/path/to/model.gguf" --context-length 32768
```

The command sets up the connection automatically, keeps your other models, and backs up your VS Code model settings.

It also creates an API key named **VS Code**. To revoke it, open **Settings** in Unsloth and select **API**.

### <i class="fa-vscode">:vscode:</i> Use your local model in VS Code

Open a project folder in VS Code, or an empty folder to try it out.

Open **Copilot Chat**, click the model picker below the chat input, and select your model under **Unsloth**. Choose **Agent** to let it create and edit files, or **Ask** to chat about your code.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fdimfm9IrGcW4PK2OFNan%2Fimage.png?alt=media&amp;token=6ab59f12-9fdf-4e08-82fc-e52dbe70f375" alt="" width="563"><figcaption></figcaption></figure></div>

Agent mode requires tool-calling support. We recommend at least **32K context**.

Let’s build a simple game. Try this prompt:

{% code overflow="wrap" %}

```
Create a playable Snake game in a single index.html file.

Use arrow keys to move, show the score, and add a restart button.

Give it a light background and a bright green snake. Use HTML, CSS, and JavaScript with no external dependencies.
```

{% endcode %}

{% columns %}
{% column %}
Review any tool permissions before approving them. Once the agent creates `index.html`, open it in your browser and play.

Want to change something? Ask it to add difficulty levels or a high-score tracker.

Keep your model loaded and the Unsloth server running while you work.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F7CYu4PotqktrbwiRXkPP%2Fwormgif.gif?alt=media&amp;token=08dbd04f-c6a4-48ea-986a-428131c8e970" alt="" width="375"><figcaption></figcaption></figure></div>

{% endcolumn %}
{% endcolumns %}

If your model doesn’t appear, check **Manage Models** in the model picker. You can also refresh VS Code by running `Developer: Reload Window` from the Command Palette.

#### Switch models

Load a different model in Unsloth, then run:

```bash
unsloth start vscode
```

Select the new model under **Unsloth** in Copilot Chat.

## Troubleshooting

**My model doesn’t appear**

Open **Manage Models** in the model picker and look for **Unsloth**. If it’s missing, check that GitHub Copilot Chat is enabled, then run `unsloth start vscode` again.

If it still doesn’t appear, open the Command Palette and run **Developer: Reload Window**.

**My model appears in Ask but not Agent mode**

Agent mode requires tool-calling support. Use **Ask** with this model, or switch to one whose chat template supports tools.

**I’m getting context-length errors**

Agent instructions and tools take up part of the model’s context window. We recommend at least **32K context** for Agent mode.

Replace the path below with your GGUF file and run:

{% code overflow="wrap" %}

```bash
unsloth start vscode --model "/path/to/model.gguf" --context-length 32768
```

{% endcode %}

Reload VS Code if the model details haven’t updated. It may display 32,768 tokens as **33K**.

#### Unsloth is running on a remote machine

In an SSH or container session without a VS Code user directory, the command prints the configuration to add locally and connection instructions.

Follow the printed instructions to make the server reachable from your computer, then add the configuration to your local VS Code installation.

If the model doesn’t appear in a Remote-SSH, WSL, or dev container window, try a **local VS Code window** connected to the remote Unsloth server.

For more model-loading options and remote connection settings, see the [Unsloth Start guide](https://unsloth.ai/docs/integrations/unsloth-start).


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/integrations/how-to-run-local-ai-models-in-vs-code.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
