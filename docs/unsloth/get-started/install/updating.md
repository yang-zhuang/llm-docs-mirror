> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/install/updating.md).

# Updating Unsloth

Update Unsloth Desktop, Unsloth Studio, or Unsloth Core.

### Update Unsloth Desktop

Unsloth Desktop checks for updates automatically after startup. To check manually, open **Settings** → **General** and select **Check for updates**.

* **macOS and Windows:** Select **Update now**. Unsloth installs the update and relaunches the app.
* **Linux AppImage:** In-app updates are supported for the AppImage build.
* **Linux `.deb`:** Download the latest package from the [Linux download page](https://unsloth.ai/download/linux) and install it over the existing version. Debian package installs update manually.

Unsloth Desktop updates independently from manual Unsloth Studio and Unsloth Core installations.

### Update Unsloth Studio

You can use the same install commands to update

#### **MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

#### **Windows PowerShell:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

#### **Homebrew:**

```bash
brew update && brew upgrade --cask unsloth
```

### Updating Unsloth Core:

```bash
pip install --upgrade unsloth unsloth_zoo
```

#### Updating Unsloth Core without dependency updates:

<pre class="language-bash" data-overflow="wrap"><code class="lang-bash">pip install --upgrade --force-reinstall --no-cache-dir --no-deps unsloth
<strong>pip install --upgrade --force-reinstall --no-cache-dir --no-deps unsloth_zoo
</strong></code></pre>

### **Use an Old Version**

#### **Unsloth Desktop**

To use an old version of Unsloth Desktop, it is very simple. Just look through [our GitHub releases](https://github.com/unslothai/unsloth/releases) and select the specific release you want to install in the 'Assets' area.

#### **Unsloth Studio**

To use an old version of Unsloth Studio, follow the below with your desired version and names:

**macOS, Linux, WSL:**

```shellscript
uv pip install \
  --python "$HOME/.unsloth/studio/unsloth_studio/bin/python" \
  --reinstall --no-deps "unsloth==VERSION"

"$HOME/.unsloth/studio/unsloth_studio/bin/unsloth" studio -p 8888
```

**Windows:**

```shellscript
uv pip install `
  --python "$env:USERPROFILE\.unsloth\studio\unsloth_studio\Scripts\python.exe" `
  --reinstall --no-deps "unsloth==VERSION"

& "$env:USERPROFILE\.unsloth\studio\unsloth_studio\Scripts\unsloth.exe" studio -p 8888
```

#### **Unsloth Core**

<pre class="language-bash" data-overflow="wrap"><code class="lang-bash"><strong>pip install --force-reinstall --no-cache-dir --no-deps unsloth==2025.1.5
</strong></code></pre>

'2025.1.5' is one of the previous old versions of Unsloth. Change it to a specific release listed on our [Github here](https://github.com/unslothai/unsloth/releases).


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/install/updating.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
