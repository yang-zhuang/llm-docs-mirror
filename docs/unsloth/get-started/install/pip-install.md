> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/install/pip-install.md).

# Install Unsloth via pip and uv

Install Unsloth Studio manually or install Unsloth Core with pip, uv, or a virtual environment.

**Unsloth Desktop**, **Unsloth Studio**, and **Unsloth Core** are installed differently. This page covers manual Studio installation and the code-based Core package.

### Unsloth Desktop

For the native desktop app, use the OS download instead of the commands below:

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

## **Unsloth Studio**

**Unsloth Studio** is our web UI. Follow below for native installation:

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

```powershell
winget upgrade --id UnslothAI.Unsloth -e
```

{% endtab %}
{% endtabs %}

#### Launch:

{% columns %}
{% column %}
Standard local launch:

```bash
unsloth studio
```

For details about install and uninstallation please visit the [Unsloth Studio Install](/docs/new/studio/install.md) section.
{% endcolumn %}

{% column %}
Launch Unsloth securely over HTTPS:

```bash
unsloth studio --secure
```

Use a [free Cloudflare](/docs/basics/how-to-serve-local-llms-anywhere-secure-remote-access-with-cloudflare-and-unsloth.md) tunnel on Windows, Mac, or Linux.
{% endcolumn %}
{% endcolumns %}

### **Install from Main Repo**

#### **macOS, Linux, WSL developer installs:**

```bash
git clone https://github.com/unslothai/unsloth
cd unsloth
./install.sh --local
unsloth studio -H 0.0.0.0 -p 8888
```

#### **Windows PowerShell developer installs:**

```powershell
winget install -e --id Python.Python.3.13 --source winget
winget install --id=astral-sh.uv  -e --source winget
winget install --id Git.Git -e --source winget
git clone https://github.com/unslothai/unsloth
cd unsloth
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1 --local
unsloth studio -H 0.0.0.0 -p 8888
```

### **Nightly Install**

#### **Nightly - MacOS, Linux, WSL:**

```bash
git clone https://github.com/unslothai/unsloth
cd unsloth
git checkout nightly
./install.sh --local
```

Then to launch every time:

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

#### **Nightly - Windows:**

Run in Windows Powershell:

```bash
winget install -e --id Python.Python.3.13 --source winget
winget install --id=astral-sh.uv  -e --source winget
winget install --id Git.Git -e --source winget
git clone https://github.com/unslothai/unsloth
cd unsloth
git checkout nightly
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1 --local
```

Then to launch every time:

<pre class="language-bash"><code class="lang-bash"><strong>unsloth studio -H 0.0.0.0 -p 8888
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

**Windows:**&#x20;

```shellscript
uv pip install `
  --python "$env:USERPROFILE\.unsloth\studio\unsloth_studio\Scripts\python.exe" `
  --reinstall --no-deps "unsloth==VERSION"

& "$env:USERPROFILE\.unsloth\studio\unsloth_studio\Scripts\unsloth.exe" studio -p 8888
```

### Uninstall

The recommended way to fully remove Unsloth Studio is the uninstall script for your OS. It stops any running servers, removes the app, CLI command, launcher data, shortcuts, and platform-specific entries (macOS `.app` bundle + Launch Services; Windows Start Menu + registry + PATH):

**macOS, WSL, Linux:**

```shellscript
curl -fsSL https://raw.githubusercontent.com/unslothai/unsloth/main/scripts/uninstall.sh | sh
```

**Windows (PowerShell):**

```ps1
irm https://raw.githubusercontent.com/unslothai/unsloth/main/scripts/uninstall.ps1 | iex 
```

#### Manual uninstall

If you prefer to remove only specific parts:

**1. Remove app only** (keeps history, chats, checkpoints, and exports intact):

* **macOS, WSL, Linux:** `rm -rf ~/.unsloth/studio/unsloth_studio`
* **Windows (PowerShell):** `Remove-Item -Recurse -Force "$HOME\.unsloth\studio\unsloth_studio"`

**2. Remove Unsloth entirely** (keeps other Unsloth tools intact):

* **macOS, WSL, Linux:** `rm -rf ~/.unsloth/studio`
* **Windows (PowerShell):** `Remove-Item -Recurse -Force "$HOME\.unsloth\studio"`

**3. Remove everything Unsloth-related:**

* **macOS, WSL, Linux:** `rm -rf ~/.unsloth`
* **Windows (PowerShell):** `Remove-Item -Recurse -Force "$HOME\.unsloth"`

{% hint style="warning" %}
Note: Step 3 deletes everything in history, chats, model checkpoints, and exports. This cannot be undone.
{% endhint %}

**4. Remove shortcuts and symlinks:**

**macOS:**

```shellscript
rm -rf ~/Applications/Unsloth\ Studio.app ~/Desktop/Unsloth\ Studio
```

**Linux:**&#x20;

```shellscript
rm -f ~/.local/share/applications/unsloth-studio.desktop ~/Desktop/unsloth-studio.desktop
```

**WSL / Windows (PowerShell):**

```shellscript
Remove-Item -Force "$HOME\Desktop\Unsloth Studio.lnk"
Remove-Item -Force "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Unsloth Studio.lnk"
```

**5. Remove the CLI command:**

* **macOS, Linux, WSL:** `rm -f ~/.local/bin/unsloth`
* **Windows (PowerShell):** The installer added the venv's `Scripts` directory to your User PATH. To remove it, open Settings → System → About → Advanced system settings → Environment Variables, find `Path` under User variables, and remove the entry pointing to `.unsloth\studio\...\Scripts`.

{% hint style="info" %}
Note: Steps 1-5 dont touch your downloaded HF model files. See Deleting cached HF model files below if you want to reclaim that space.
{% endhint %}

### **Deleting cached HF model files**

You can delete old model files either from the bin icon in model search or by removing the relevant cached model folder from the default Hugging Face cache directory. By default, Hugging Face uses `~/.cache/huggingface/hub/` on macOS/Linux/WSL and `C:\Users\<username>\.cache\huggingface\hub\` on Windows.

* **MacOS, Linux, WSL:** `~/.cache/huggingface/hub/`
* **Windows:** `%USERPROFILE%\.cache\huggingface\hub\`

If `HF_HUB_CACHE` or `HF_HOME` is set, use that location instead. On Linux and WSL, `XDG_CACHE_HOME` can also change the default cache root.

## **Unsloth Core**

**Install uv with the following command:**

**macOS, WSL, Linux:**

```shellscript
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Install unsloth core with uv pip (recommended) for the latest pip release:**

```bash
uv venv unsloth_env --python 3.13
source unsloth_env/bin/activate
uv pip install unsloth --torch-backend=auto
```

Or just pip:

```bash
pip install unsloth
```

To install **vLLM and Unsloth** together, do:

```bash
uv pip install unsloth vllm --torch-backend=auto
```

To install the **latest main branch** of Unsloth, do:

{% code overflow="wrap" %}

```bash
uv pip install unsloth --torch-backend=auto
pip uninstall unsloth unsloth_zoo -y && pip install --no-deps git+https://github.com/unslothai/unsloth_zoo.git && pip install --no-deps git+https://github.com/unslothai/unsloth.git
```

{% endcode %}

For **venv and virtual environments installs** to isolate your installation to not break system packages, and to reduce irreparable damage to your system, use venv:

{% code overflow="wrap" %}

```bash
apt install python3.10-venv python3.11-venv python3.12-venv python3.13-venv -y
python -m venv unsloth_env
source unsloth_env/bin/activate
pip install --upgrade pip && pip install uv
uv pip install unsloth --torch-backend=auto
```

{% endcode %}

If you're installing Unsloth in Jupyter, Colab, or other notebooks, be sure to prefix the command with `!`. This isn't necessary when using a terminal

{% hint style="info" %}
Python 3.13 is now supported!
{% endhint %}

### Uninstall Unsloth Core

If you're still encountering dependency issues with Unsloth, many users have resolved them by forcing uninstalling and reinstalling Unsloth:

{% code overflow="wrap" %}

```bash
pip install --upgrade --force-reinstall --no-cache-dir --no-deps unsloth
pip install --upgrade --force-reinstall --no-cache-dir --no-deps unsloth_zoo
```

{% endcode %}

### Advanced Pip Installation

{% hint style="warning" %}
Do **NOT** use this if you have [Conda](/docs/get-started/install/conda-install.md).
{% endhint %}

Pip is a bit more complex since there are dependency issues. The pip command is different for `torch 2.2,2.3,2.4,2.5` and CUDA versions.

For other torch versions, we support `torch211`, `torch212`, `torch220`, `torch230`, `torch240` and for CUDA versions, we support `cu118` and `cu121` and `cu124`. For Ampere devices (A100, H100, RTX3090) and above, use `cu118-ampere` or `cu121-ampere` or `cu124-ampere`.

For example, if you have `torch 2.4` and `CUDA 12.1`, use:

```bash
pip install --upgrade pip
pip install "unsloth[cu121-torch240] @ git+https://github.com/unslothai/unsloth.git"
```

Another example, if you have `torch 2.5` and `CUDA 12.4`, use:

```bash
pip install --upgrade pip
pip install "unsloth[cu124-torch250] @ git+https://github.com/unslothai/unsloth.git"
```

And other examples:

```bash
pip install "unsloth[cu121-ampere-torch240] @ git+https://github.com/unslothai/unsloth.git"
pip install "unsloth[cu118-ampere-torch240] @ git+https://github.com/unslothai/unsloth.git"
pip install "unsloth[cu121-torch240] @ git+https://github.com/unslothai/unsloth.git"
pip install "unsloth[cu118-torch240] @ git+https://github.com/unslothai/unsloth.git"

pip install "unsloth[cu121-torch230] @ git+https://github.com/unslothai/unsloth.git"
pip install "unsloth[cu121-ampere-torch230] @ git+https://github.com/unslothai/unsloth.git"

pip install "unsloth[cu121-torch250] @ git+https://github.com/unslothai/unsloth.git"
pip install "unsloth[cu124-ampere-torch250] @ git+https://github.com/unslothai/unsloth.git"
```

Or, run the below in a terminal to get the **optimal** pip installation command:

```bash
wget -qO- https://raw.githubusercontent.com/unslothai/unsloth/main/unsloth/_auto_install.py | python -
```

Or, run the below manually in a Python REPL:

{% code overflow="wrap" %}

```python
# Licensed under the Apache License, Version 2.0 (the "License")
try: import torch
except: raise ImportError('Install torch via `pip install torch`')
from packaging.version import Version as V
import re
v = V(re.match(r"[0-9\.]{3,}", torch.__version__).group(0))
cuda = str(torch.version.cuda)
is_ampere = torch.cuda.get_device_capability()[0] >= 8
USE_ABI = torch._C._GLIBCXX_USE_CXX11_ABI
if cuda not in ("11.8", "12.1", "12.4", "12.6", "12.8", "13.0"): raise RuntimeError(f"CUDA = {cuda} not supported!")
if   v <= V('2.1.0'): raise RuntimeError(f"Torch = {v} too old!")
elif v <= V('2.1.1'): x = 'cu{}{}-torch211'
elif v <= V('2.1.2'): x = 'cu{}{}-torch212'
elif v  < V('2.3.0'): x = 'cu{}{}-torch220'
elif v  < V('2.4.0'): x = 'cu{}{}-torch230'
elif v  < V('2.5.0'): x = 'cu{}{}-torch240'
elif v  < V('2.5.1'): x = 'cu{}{}-torch250'
elif v <= V('2.5.1'): x = 'cu{}{}-torch251'
elif v  < V('2.7.0'): x = 'cu{}{}-torch260'
elif v  < V('2.7.9'): x = 'cu{}{}-torch270'
elif v  < V('2.8.0'): x = 'cu{}{}-torch271'
elif v  < V('2.8.9'): x = 'cu{}{}-torch280'
elif v  < V('2.9.1'): x = 'cu{}{}-torch290'
elif v  < V('2.9.2'): x = 'cu{}{}-torch291'
else: raise RuntimeError(f"Torch = {v} too new!")
if v > V('2.6.9') and cuda not in ("11.8", "12.6", "12.8", "13.0"): raise RuntimeError(f"CUDA = {cuda} not supported!")
x = x.format(cuda.replace(".", ""), "-ampere" if False else "") # is_ampere is broken due to flash-attn
print(f'pip install --upgrade pip && pip install --no-deps git+https://github.com/unslothai/unsloth-zoo.git && pip install "unsloth[{x}] @ git+https://github.com/unslothai/unsloth.git" --no-build-isolation')
```

{% endcode %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/install/pip-install.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
