> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/integrations/connections/ollama.md).

# How to Connect Ollama to Unsloth

Ollama lets you run local LLMs on your own hardware, and [Unsloth](https://github.com/unslothai/unsloth) makes it easy to connect and run those models directly into a open-source UI chat interface. In this guide, you’ll learn how to install Ollama, run native Ollama models or GGUF models from Hugging Face, connect Ollama to Unsloth, and start chatting with local AI models.

Whether you want to use models like [Qwen](/docs/models/qwen3.6.md), import a GGUF file, or expose your local Ollama server through an OpenAI-compatible endpoint, this walkthrough covers the full setup from installation to first chat.

### Setup

{% stepper %}
{% step %}

#### Install or prepare Ollama

{% tabs %}
{% tab title="macOS" %}
Install Ollama with the install script:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

You can also download Ollama manually from [ollama.com/download](https://ollama.com/download).
{% endtab %}

{% tab title="Windows" %}
Install Ollama from PowerShell:

```powershell
irm https://ollama.com/install.ps1 | iex
```

You can also download Ollama manually from [ollama.com/download](https://ollama.com/download/OllamaSetup.exe).
{% endtab %}

{% tab title="Linux" %}
Install Ollama with the install script:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

You can also download Ollama manually from [ollama.com/download](https://docs.ollama.com/linux#manual-install).
{% endtab %}

{% tab title="Docker" %}
The official Ollama Docker image is `ollama/ollama` on Docker Hub.

```bash
docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

{% endtab %}
{% endtabs %}

Ollama usually runs at:

```
http://localhost:11434
```

{% endstep %}

{% step %}

#### Run a model

You can choose a model in two common ways:

* Search native Ollama models at [ollama.com/search](https://ollama.com/search), then copy the model name.
* Use a GGUF model from Hugging Face, then copy the Ollama command from **Use this model**.

For an Ollama model, pull and run it:

```bash
ollama pull qwen3.6:35b-a3b
ollama run qwen3.6:35b-a3b
```

If the Ollama app or service is not already running, start it first:

```bash
ollama serve
```

#### Pick a GGUF from Hugging Face

If you are using a GGUF model from Hugging Face, the easiest way to get the command is from the model page.

Open the model you want to use, click **Use this model**, then choose **Ollama** from the local apps list. Pick the quantization you want from the dropdown, then copy the generated command.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FRSR0qWpzSRJgeSIghoWO%2Fexport-1779051800964-small.gif?alt=media&amp;token=8e557e60-2e11-420e-a7f4-dd80533bd86b" alt=""><figcaption></figcaption></figure>

For example, with Ollama:

```bash
ollama run hf.co/unsloth/Qwen3.6-35B-A3B-GGUF:UD-Q4_K_XL
```

This helps avoid mistakes with the repo name or quantization tag.
{% endstep %}

{% step %}

#### Connect Ollama to Unsloth

Open **Settings → Connections**, then click **Add Connection**.

Select **Ollama**, then enter your connection details:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FIKDXfJZmRQVA742rXAHA%2Fimage.png?alt=media&amp;token=6c7105a0-9f6e-435b-bafb-1502e22331bd" alt="" width="563"><figcaption></figcaption></figure>

Use the Ollama URL shown in the Unsloth form. In most local setups, this is:

```
http://localhost:11434
```

If Unsloth asks for an OpenAI-compatible base URL, use:

```
http://localhost:11434/v1
```

Ollama normally does not need an API key. Leave the API key field empty unless you are using a proxy that requires one.

Click **Load Models** to fetch the models running in Ollama, or enter the **model ID** yourself, for example `qwen3.6`.
{% endstep %}

{% step %}

#### Ready to Chat

After you click **Add Connection**, the models you enabled will now appear under **Connected** in the **Select Model** dropdown.
{% endstep %}
{% endstepper %}

#### Common Ollama commands

Use these while setting up the model you want to expose to Unsloth:

| Command                       | What it does                             |
| ----------------------------- | ---------------------------------------- |
| `ollama run qwen3.6:35b-a3b`  | Run a model and open an interactive chat |
| `ollama pull qwen3.6:35b-a3b` | Download a model without starting chat   |
| `ollama ls`                   | List downloaded models                   |
| `ollama ps`                   | List models currently running            |
| `ollama stop qwen3.6:35b-a3b` | Stop a running model                     |
| `ollama rm qwen3.6:35b-a3b`   | Remove a downloaded model                |
| `ollama serve`                | Start the Ollama server                  |

If you are importing a local GGUF into Ollama, create a `Modelfile`, then run:

```bash
ollama create -f Modelfile
```

If Ollama is not detected, make sure the Ollama app or service is running. Then click **Load Models** again in Unsloth.

For the full command list, see the [Ollama CLI reference](https://docs.ollama.com/cli).


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/integrations/connections/ollama.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
