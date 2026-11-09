> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements.md).

# Unsloth Requirements

Here are Unsloth's requirements including system and GPU VRAM requirements.

Unsloth can be used in three ways: our [Unsloth Desktop](/docs/desktop.md) app, our [Unsloth Studio](/docs/new/studio/install.md) web UI, or through [Unsloth Core](#unsloth-core-requirements), the original code-based version. Each has different requirements.

## **Unsloth Requirements**

* **Mac:** Training, MLX and GGUF inference are ALL supported.
* **CPU: Unsloth still works without a GPU**, for Chat + Data Recipes.
* **Training:** Works on **NVIDIA**, **AMD**, **Intel** GPUs and **Mac** devices

### <i class="fa-windows">:windows:</i> Window**s**

Unsloth Studio works directly on Windows without WSL. To train models, make sure your system satisfies these requirements:

**Requirements**

* Windows 10 or Windows 11 (64-bit)
* NVIDIA GPU with drivers installed
* **App Installer** (includes `winget`): [here](https://learn.microsoft.com/en-us/windows/msix/app-installer/install-update-app-installer)
* **Git**: `winget install --id Git.Git -e --source winget`
* **Python**: version 3.11 up to, but not including, 3.14
* Work inside a Python environment such as **uv**, **venv**, or **conda/mamba**

### <i class="fa-apple">:apple:</i> MacOS

Unsloth Studio works on MacOS device with full support for training, MLX and GGUF inference.

* macOS 12 Monterey or newer (Intel or Apple Silicon)
* Install Homebrew: [here](https://brew.sh/)
* Git: `brew install git`&#x20;
* cmake: `brew install cmake`&#x20;
* openssl: `brew install openssl`
* Python: version 3.11 up to, but not including, 3.14
* Work inside a Python environment such as **uv**, **venv**, or **conda/mamba**

### <i class="fa-linux">:linux:</i> Linux & WSL

* Ubuntu 20.04+ or similar distro (64-bit)
* NVIDIA GPU with drivers installed
* CUDA toolkit (12.4+ recommended, 12.8+ for blackwell)
* Git: `sudo apt install git`
* Python: version 3.11 up to, but not including, 3.14
* Work inside a Python environment such as **uv**, **venv**, or **conda/mamba**

### <i class="fa-microchip">:microchip:</i> CPU only

Unsloth Studio supports CPU devices for [Chat](#run-models-locally) for GGUF models and [Data Recipes](/docs/new/studio/data-recipe.md) ([Export](/docs/new/studio/export.md) coming very soon)

* Same as the ones mentioned above for Linux (except for NVIDIA GPU drivers) and MacOS.

### **Training**

Unsloth Studio Training currently works on NVIDIA, [AMD](/docs/get-started/install/amd.md), MLX, Intel devices. You can still use the [original Unsloth Core](#unsloth-requirements) to train on AMD and Intel devices. **Python 3.11–3.13** is required.

| Requirement      | Linux / WSL                              | Windows                                       |
| ---------------- | ---------------------------------------- | --------------------------------------------- |
| **Git**          | Usually preinstalled                     | Installed by setup script (`winget`)          |
| **CMake**        | Preinstalled or `sudo apt install cmake` | Installed by setup script (`winget`)          |
| **C++ compiler** | `build-essential`                        | Visual Studio Build Tools 2022                |
| **CUDA Toolkit** | Optional; `nvcc` auto-detected           | Installed by setup script (matched to driver) |

## Unsloth Core Requirements

* **Operating System**: Works on Linux and [Windows](https://docs.unsloth.ai/get-started/install-and-update/windows-installation)
* Supports NVIDIA GPUs since 2018+ including [Blackwell RTX 50](/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth.md) and [DGX Spark](/docs/blog/fine-tuning-llms-with-nvidia-dgx-spark-and-unsloth.md)
* Minimum CUDA Capability 7.0 (V100, T4, Titan V, RTX 20 & 50, A100, H100, L40 etc) [Check your GPU!](https://developer.nvidia.com/cuda-gpus) GTX 1070, 1080 works, but is slow.
* The official [Unsloth Docker image](https://hub.docker.com/r/unsloth/unsloth) `unsloth/unsloth` is available on Docker Hub
  * [Docker](/docs/get-started/install/docker.md)
* Unsloth works on [AMD](/docs/get-started/install/amd.md) and [Intel](/docs/get-started/install/intel.md) GPUs (follow our [specific guides](/docs/get-started/install.md)). Apple/Silicon/MLX is in the works
* Your device should have `xformers`, `torch`, `BitsandBytes` and `triton` support.
* If you have different versions of torch, transformers etc., `pip install unsloth` will automatically install all the latest versions of those libraries so you don't need to worry about version compatibility.

{% hint style="info" %}
Python 3.13 is supported!
{% endhint %}

### Fine-tuning VRAM requirements:

How much GPU memory do I need for LLM fine-tuning using Unsloth?

{% hint style="info" %}
A common issue when you OOM or run out of memory is because you set your batch size too high. Set it to 1, 2, or 3 to use less VRAM.

**For context length benchmarks, see** [**here**](/docs/basics/unsloth-benchmarks.md#context-length-benchmarks)**.**
{% endhint %}

Check this table for VRAM requirements sorted by model parameters and fine-tuning method. QLoRA uses 4-bit, LoRA uses 16-bit. Keep in mind that sometimes more VRAM is required depending on the model so these numbers are the absolute minimum:

| Model parameters | QLoRA (4-bit) VRAM | LoRA (16-bit) VRAM |
| ---------------- | ------------------ | ------------------ |
| 3B               | 3.5 GB             | 8 GB               |
| 7B               | 5 GB               | 19 GB              |
| 8B               | 6 GB               | 22 GB              |
| 9B               | 6.5 GB             | 24 GB              |
| 11B              | 7.5 GB             | 29 GB              |
| 14B              | 8.5 GB             | 33 GB              |
| 27B              | 22GB               | 64GB               |
| 32B              | 26 GB              | 76 GB              |
| 40B              | 30GB               | 96GB               |
| 70B              | 41 GB              | 164 GB             |
| 81B              | 48GB               | 192GB              |
| 90B              | 53GB               | 212GB              |
| 405B             | 237 GB             | 950 GB             |


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
