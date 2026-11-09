> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/install/windows-installation.md).

# Install Unsloth on Windows

Install Unsloth Desktop, Unsloth Studio, or Unsloth Core on Windows.

To install Unsloth Desktop on Windows, follow the steps below.

{% stepper %}
{% step %}

### Download

<a href="https://unsloth.ai/download/windows" class="button secondary" data-icon="windows">Download Unsloth for Windows</a>
{% endstep %}

{% step %}

### Install

1. Open the Unsloth installer (`.exe` file)
2. Follow the setup prompts
3. Launch the app and wait for installation to complete
   {% endstep %}

{% step %}

### Choose a model

Open Select model or Model hub, choose a model and quantization, then download it. Once it finishes, start chatting - no setup required.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNCEVgKLJI0goPqjgcg9B%2Fmodel%20hub%20models.png?alt=media&amp;token=533b5e3c-a901-4b33-963e-4a703cc9d5a6" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

### Unsloth is now ready

To start chatting, type a message and press Enter.

* **Connect tools:** [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md), web search, [MCP](/docs/basics/mcp.md) and more
* **Train models:** Fine-tune text, diffusion, embedding, and more
* **Generate media:** Create and train images, video, TTS locally

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FpAGvwjGD0iVMZKBoyu7m%2Fgreeennn.png?alt=media&amp;token=d17a5528-8375-444c-9aff-f9e9f7903bcd" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### Install Unsloth manually

The sections below cover the web-based **Unsloth Studio** and the original code-based **Unsloth Core**.

For **Unsloth Core** on Windows, choose Conda, Docker, or WSL below. If PyTorch is already installed, `pip install unsloth` may be enough.

<a href="/docs/get-started/install/windows-installation.md#method-1-windows-via-conda" class="button secondary">Conda Tutorial</a><a href="/docs/get-started/install/windows-installation.md#method-2-docker" class="button secondary">Docker Tutorial</a><a href="/docs/get-started/install/windows-installation.md#method-3-wsl" class="button secondary">WSL Tutorial</a>

### Unsloth Studio

See below for command to install our web UI [Unsloth Studio](/docs/new/studio/install.md)

#### **Powershell**:

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

Use the same command to update.

#### **Winget**:

{% tabs %}
{% tab title="Install" %}

```powershell
winget install --id UnslothAI.Unsloth -e
```

{% endtab %}

{% tab title="Update" %}

```powershell
winget upgrade --id UnslothAI.Unsloth -e
```

{% endtab %}
{% endtabs %}

#### **Launch:**

{% tabs %}
{% tab title="Local launch" %}

```powershell
unsloth studio
```

{% endtab %}

{% tab title="Remote access" %}

```powershell
unsloth studio --secure
```

{% endtab %}
{% endtabs %}

For detailed Unsloth Studio install instructions and requirements, [view our guide](/docs/new/studio/install.md).

Below are installation instructions for the original **Unsloth Core**:

### Method #1 - Windows via Conda:

{% stepper %}
{% step %}
**Install Miniconda (or Anaconda)**

Download Anaconda [here](https://www.anaconda.com/download). Our suggestion is to use [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions). To use it, first enter Powershell - search "Windows Powershell" in Start:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FvCgJ3hTR5ChVmCR1ndAh%2Fimage.png?alt=media&amp;token=bcabe210-793f-40ae-944a-a349dddc8c35" alt="" width="375"><figcaption></figcaption></figure>

Then it'll open up Powershell:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fm7J0b8Qz5W2aGktt3KA9%2Fimage.png?alt=media&amp;token=f84327e4-408f-492c-a909-982ed458f393" alt="" width="375"><figcaption></figcaption></figure>

Then copy paste the below: CTRL+C, and paste it in Powershell CTRL+V:

{% code overflow="wrap" %}

```ps
Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile ".\miniconda.exe"
Start-Process -FilePath ".\miniconda.exe" -ArgumentList "/S" -Wait
del .\miniconda.exe
```

{% endcode %}

Accept the warning and press "Paste anyway" and wait.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FZCFxO1FrYGk7sV7AmCe8%2Fimage.png?alt=media&amp;token=f753dbdb-efa9-462c-875b-0a18509a10cf" alt="" width="375"><figcaption></figcaption></figure>

It's downloading the installer like below:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F2TzsqlGZyUI4wBT0hXW9%2Fimage.png?alt=media&amp;token=a680690a-3179-4525-bf83-0163424b5ddc" alt="" width="375"><figcaption></figcaption></figure>

After installing, open up open **Anaconda Powershell Prompt** to use Miniconda via Start -> Search for it:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FWoQSFFfmB26WT6BdzrvJ%2Fimage.png?alt=media&amp;token=747c6c4e-f676-4927-abad-cb667e757309" alt="" width="375"><figcaption></figcaption></figure>

Then you'll see:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNTTeflwW9Gw7lxJdCUcy%2Fimage.png?alt=media&amp;token=77f093b7-9fd5-47f2-856d-18f238f5a95e" alt="" width="375"><figcaption></figcaption></figure>
{% endstep %}

{% step %}
**Make conda environment**

```bash
conda create --name unsloth_env python==3.12 -y
conda activate unsloth_env
```

**You will see:**

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FEFYV6IhOeXIDbzxYHzEJ%2Fimage.png?alt=media&amp;token=e3452b73-cfd2-4148-a735-cfe400369c17" alt="" width="375"><figcaption></figcaption></figure>
{% endstep %}

{% step %}
**Check `nvidia-smi` to confirm you have a GPU, and look for the CUDA version**

After typing `nvidia-smi` in Powershell, you should see something like below. If you don't have `nvidia-smi` or the below fails to pop up, you need to reinstall [NVIDIA drivers](https://www.nvidia.com/en-us/drivers/).

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F1CMAzx7LX8LEc8GHy1I9%2Fimage.png?alt=media&amp;token=a0ad52e3-be17-4dc4-ae97-ba400a639098" alt="" width="375"><figcaption></figcaption></figure>
{% endstep %}

{% step %}
**Install PyTorch**

When running `nvidia-smi` you will see at the top right corner: "CUDA Version: 13.0". Install PyTorch in PowerShell via. Change `130` to your CUDA version - ensure the [version exists](https://pytorch.org/) and matches your CUDA driver version.

{% code overflow="wrap" %}

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
```

{% endcode %}

You will see:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fo4aNeIbILGYvfpjYa1X2%2Fimage.png?alt=media&amp;token=444d6907-04e0-4d5e-8de5-d8cdcaf85364" alt="" width="563"><figcaption></figcaption></figure>

Try running this in Python via `python` after PyTorch is installed:

{% code overflow="wrap" %}

```python
import torch
print(torch.cuda.is_available())
A = torch.ones((10, 10), device = "cuda")
B = torch.ones((10, 10), device = "cuda")
A @ B
```

{% endcode %}

You should see a matrix of 10s. Also verify True for the first.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FJkf39Nyfgyt4QmTLGhOx%2Fimage.png?alt=media&amp;token=2d1a16a6-e524-461a-ac75-a24b6bda333f" alt="" width="375"><figcaption></figcaption></figure>
{% endstep %}

{% step %}
**Install Unsloth (only if PyTorch works!)**

{% hint style="danger" %}
**Confirm PyTorch works fine and runs - if not PyTorch is broken and that means your Windows machine might need a re installation of CUDA drivers unfortunately.**
{% endhint %}

In Powershell (after exiting Python via `exit()` , do and wait:

```bash
pip install unsloth
```

{% endstep %}

{% step %}
**Verify Unsloth works**

Now use any script in [Unsloth Notebooks](/docs/get-started/unsloth-notebooks.md) (save to .py file), or use the below basic script:

{% code expandable="true" %}

```python
from unsloth import FastLanguageModel, FastModel
import torch
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
max_seq_length = 512
url = "https://huggingface.co/datasets/laion/OIG/resolve/main/unified_chip2.jsonl"
dataset = load_dataset("json", data_files = {"train" : url}, split = "train")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/gemma-3-270m-it",
    max_seq_length = max_seq_length, # Choose any for long context!
    load_in_4bit = True,  # 4-bit quantization. False = 16-bit LoRA.
    load_in_8bit = False, # 8-bit quantization
    load_in_16bit = False, # 16-bit LoRA
    full_finetuning = False, # Use for full fine-tuning.
    trust_remote_code = False, # Enable to support new models
    # token = "hf_...", # use one if using gated models
)

# Do model patching and add fast LoRA weights
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    max_seq_length = max_seq_length,
    use_rslora = False,  # We support rank stabilized LoRA
    loftq_config = None, # And LoftQ
)

trainer = SFTTrainer(
    model = model,
    train_dataset = dataset,
    tokenizer = tokenizer,
    args = SFTConfig(
        max_seq_length = max_seq_length,
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 10,
        max_steps = 60,
        logging_steps = 1,
        output_dir = "outputs",
        optim = "adamw_8bit",
        seed = 3407,
        dataset_num_proc = 1,
    ),
)
trainer.train()
```

{% endcode %}

You should see:

```bash
🦥 Unsloth: Will patch your computer to enable 2x faster free finetuning.
🦥 Unsloth Zoo will now patch everything to make training faster!
==((====))==  Unsloth 2026.1.4: Fast Gemma3 patching. Transformers: 4.57.6.
   \\   /|    NVIDIA GeForce RTX 3060. Num GPUs = 1. Max memory: 12.0 GB. Platform: Windows.
O^O/ \_/ \    Torch: 2.10.0+cu130. CUDA: 8.6. CUDA Toolkit: 13.0. Triton: 3.6.0
\        /    Bfloat16 = TRUE. FA [Xformers = 0.0.34. FA2 = False]
 "-____-"     Free license: http://github.com/unslothai/unsloth
Unsloth: Fast downloading is enabled - ignore downloading bars which are red colored!
Unsloth: Gemma3 does not support SDPA - switching to fast eager.
Unsloth: Making `model.base_model.model.model` require gradients
Unsloth: Tokenizing ["text"] (num_proc=1):   0%|                 | 0/210289 [00:00<?, ? examples/s]�  Unsloth: Will patch your computer to enable 2x faster free finetuning.
🦥 Unsloth: Will patch your computer to enable 2x faster free finetuning.
```

And training:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FfJalYwpN7ffC88J2dsOQ%2Fimage.png?alt=media&amp;token=e2129773-9255-4983-b52e-51de5729a7ab" alt="" width="375"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### Method #2 - Docker:

Docker might be the easiest way for Windows users to get started with Unsloth as there is no setup needed or dependency issues. [**`unsloth/unsloth`**](https://hub.docker.com/r/unsloth/unsloth) is Unsloth's only Docker image. For [Blackwell](/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth.md) and 50-series GPUs, use this same image - no separate image needed.

For installation instructions, please follow our [Docker guide](/docs/blog/how-to-fine-tune-llms-with-unsloth-and-docker.md), otherwise here is a quickstart guide:

{% stepper %}
{% step %}
**Install Docker and NVIDIA Container Toolkit.**

Install Docker via [Linux](https://docs.docker.com/engine/install/) or [Desktop](https://docs.docker.com/desktop/) (other). Then install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation):

```bash
export NVIDIA_CONTAINER_TOOLKIT_VERSION=1.17.8-1
sudo apt-get update && sudo apt-get install -y \
  nvidia-container-toolkit=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
  nvidia-container-toolkit-base=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
  libnvidia-container-tools=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
  libnvidia-container1=${NVIDIA_CONTAINER_TOOLKIT_VERSION}
```

{% endstep %}

{% step %}
**Run the container.**

[**`unsloth/unsloth`**](https://hub.docker.com/r/unsloth/unsloth) is Unsloth's only Docker image.

```bash
docker run -d -e JUPYTER_PASSWORD="mypassword" \
  -p 8888:8888 -p 2222:22 \
  -v $(pwd)/work:/workspace/work \
  --gpus all \
  unsloth/unsloth
```

{% endstep %}

{% step %}
**Access Jupyter Lab**

Go to [http://localhost:8888](http://localhost:8888/) and open Unsloth. Access the `unsloth-notebooks` tabs to see Unsloth notebooks.
{% endstep %}

{% step %}
**Start training with Unsloth**

If you're new, follow our step-by-step [Fine-tuning Guide](/docs/get-started/fine-tuning-llms-guide.md), [RL Guide](/docs/get-started/reinforcement-learning-rl-guide.md) or just save/copy any of our premade [notebooks](/docs/get-started/unsloth-notebooks.md).
{% endstep %}

{% step %}
**Docker issues - GPU not discovered?**

Try doing WSL via [#method-2-wsl](#method-2-wsl "mention")
{% endstep %}
{% endstepper %}

### Method #3 - WSL:

{% stepper %}
{% step %}
**Install WSL**

Open up Command Prompt, the Terminal, and install Ubuntu. Set the password if asked.

```bash
wsl.exe --install Ubuntu-24.04
wsl.exe -d Ubuntu-24.04
```

{% endstep %}

{% step %} <mark style="color:$primary;background-color:orange;">**If you did NOT do (1), so you already installed WSL**</mark>**, enter WSL by typing `wsl` and ENTER in the command prompt**

```bash
wsl
```

{% endstep %}

{% step %}
**Install Python**

{% code overflow="wrap" %}

```bash
sudo apt update
sudo apt install python3 python3-full python3-pip python3-venv -y
```

{% endcode %}
{% endstep %}

{% step %}
**Install PyTorch**

{% code overflow="wrap" %}

```bash
pip install torch torchvision --force-reinstall --index-url https://download.pytorch.org/whl/cu130
```

{% endcode %}

If you encounter permission issues, use `–break-system-packages` so `pip install torch torchvision --force-reinstall --index-url https://download.pytorch.org/whl/cu130 –break-system-packages`
{% endstep %}

{% step %}
**Install Unsloth and Jupyter Notebook**

{% code overflow="wrap" %}

```bash
pip install unsloth jupyter
```

{% endcode %}

If you encounter permission issues, use `–-break-system-packages` so `pip install unsloth jupyter –-break-system-packages`
{% endstep %}

{% step %}
**Launch Unsloth via Jupyter Notebook**

{% code overflow="wrap" %}

```bash
jupyter notebook
```

{% endcode %}

Then open up our notebooks within [Unsloth Notebooks](/docs/get-started/unsloth-notebooks.md)and load them up! You can also go to Colab notebooks and download > download .ipynb and load them.

![](https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FVbqNWsG2CCHKJJjrnU4s%2Funknown.png?alt=media\&token=854a6d0e-fc84-4e44-bf8e-4bf254801692)
{% endstep %}
{% endstepper %}

{% hint style="warning" %}
If you're using GRPO or plan to use vLLM, currently vLLM does not support Windows directly but only via WSL or Linux.
{% endhint %}

### **Troubleshooting /** Advanced

For **advanced installation instructions** or if you see weird errors during installations:

1. Install `torch` and `triton`. Go to <https://pytorch.org> to install it. For example `pip install torch torchvision torchaudio triton`
2. Confirm if CUDA is installated correctly. Try `nvcc`. If that fails, you need to install `cudatoolkit` or CUDA drivers.
3. If using an Intel GPU, you will need to follow our [Intel Windows guide](/docs/get-started/install/intel.md#windows-only-runtime-configurations)
4. Install `xformers` manually. You can try installing `vllm` and seeing if `vllm` succeeds. Check if `xformers` succeeded with `python -m xformers.info` Go to <https://github.com/facebookresearch/xformers>. Another option is to install `flash-attn` for Ampere GPUs.
5. Double check that your versions of Python, CUDA, CUDNN, `torch`, `triton`, and `xformers` are compatible with one another. The [PyTorch Compatibility Matrix](https://github.com/pytorch/pytorch/blob/main/RELEASE.md#release-compatibility-matrix) may be useful.
6. Finally, install `bitsandbytes` and check it with `python -m bitsandbytes`
7. If Unsloth is not detecting or using your GPU and if you are using our Docker container on Windows, your CUDA toolkit version `nvcc --version` should match the version of CUDA shown by nvidia-smi on the host GPU support for Docker containers on Windows is not automatic. [You need to follow Docker's guide](https://docs.docker.com/desktop/features/gpu/).

## Uninstall

#### Unsloth Desktop

1. Close Unsloth if it is running.
2. Open **Settings** in Windows.
3. Go to **Apps** → **Installed apps**.
4. Find **Unsloth**, select the three-dot menu, then choose **Uninstall**.
5. Follow the prompts to remove the app.

Uninstalling Unsloth Desktop does not remove downloaded models or your files.

#### Unsloth Studio (manual installation)

The recommended way to fully remove Unsloth Studio is the uninstall script for your OS. It stops any running servers, removes the app, CLI command, launcher data, shortcuts, and platform-specific entries (macOS `.app` bundle + Launch Services; Windows Start Menu + registry + PATH):

```ps1
irm https://raw.githubusercontent.com/unslothai/unsloth/main/scripts/uninstall.ps1 | iex 
```

#### Manual uninstall

If you prefer to remove only specific parts:

**1. Remove app only** (keeps history, chats, checkpoints, and exports intact):

* `Remove-Item -Recurse -Force "$HOME\.unsloth\studio\unsloth_studio"`

**2. Remove Unsloth entirely** (keeps other Unsloth tools intact):

* `Remove-Item -Recurse -Force "$HOME\.unsloth\studio"`

**3. Remove everything Unsloth-related:**

* `Remove-Item -Recurse -Force "$HOME\.unsloth"`

{% hint style="warning" %}
Note: Step 3 deletes everything in history, chats, model checkpoints, and exports. This cannot be undone.
{% endhint %}

**4. Remove shortcuts and symlinks:**

```shellscript
Remove-Item -Force "$HOME\Desktop\Unsloth Studio.lnk"
Remove-Item -Force "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Unsloth Studio.lnk"
```

**5. Remove the CLI command:**

* **Windows (PowerShell):** The installer added the venv's `Scripts` directory to your User PATH. To remove it, open Settings → System → About → Advanced system settings → Environment Variables, find `Path` under User variables, and remove the entry pointing to `.unsloth\studio\...\Scripts`.

{% hint style="info" %}
Note: Steps 1-5 dont touch your downloaded HF model files. See Deleting cached HF model files below if you want to reclaim that space.
{% endhint %}

### **Deleting cached HF model files**

You can delete old model files either from the bin icon in model search or by removing the relevant cached model folder from the default Hugging Face cache directory. By default, Hugging Face uses `~/.cache/huggingface/hub/` on macOS/Linux/WSL and `C:\Users\<username>\.cache\huggingface\hub\` on Windows.

* **Windows:** `%USERPROFILE%\.cache\huggingface\hub\`

If `HF_HUB_CACHE` or `HF_HOME` is set, use that location instead. On Linux and WSL, `XDG_CACHE_HOME` can also change the default cache root.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/install/windows-installation.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
