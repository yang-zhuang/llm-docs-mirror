> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth.md).

# Fine-tuning LLMs with Blackwell, RTX 50 series & Unsloth

Learn how to fine-tune LLMs on NVIDIA's Blackwell RTX 50 series and B200 GPUs with our step-by-step guide.

Unsloth now supports NVIDIA’s Blackwell architecture GPUs, including RTX 50-series GPUs (5060–5090), RTX PRO 6000, and GPUS such as B200, B40, GB100, GB102 and more! You can read the official [NVIDIA blogpost here](https://developer.nvidia.com/blog/train-an-llm-on-an-nvidia-blackwell-desktop-with-unsloth-and-scale-it/).

Unsloth is now compatible with every NVIDIA GPU from 2018+ including the [DGX Spark](/docs/blog/fine-tuning-llms-with-nvidia-dgx-spark-and-unsloth.md).

> **Our new** [**Docker image**](#docker) **supports Blackwell. Run the Docker image and start training!** [**Guide**](/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth.md)

### Pip install

Simply install Unsloth:

```bash
pip install unsloth
```

If you see issues, another option is to create a separate isolated environment:

```bash
python -m venv unsloth
source unsloth/bin/activate
pip install unsloth
```

Note it might be `pip3` or `pip3.13` and also `python3` or `python3.13`

You might encounter some Xformers issues, in which cause you should build from source:

{% code overflow="wrap" %}

```bash
# First uninstall xformers installed by previous libraries
pip uninstall xformers -y

# Clone and build
pip install ninja
export TORCH_CUDA_ARCH_LIST="12.0"
git clone --depth=1 https://github.com/facebookresearch/xformers --recursive
cd xformers && python setup.py install && cd ..
```

{% endcode %}

### Docker

[**`unsloth/unsloth`**](https://hub.docker.com/r/unsloth/unsloth) is Unsloth's only Docker image. For Blackwell and 50-series GPUs, use this same image - no separate image needed.

For installation instructions, please follow our [Unsloth Docker guide](/docs/blog/how-to-fine-tune-llms-with-unsloth-and-docker.md).

### uv

```bash
uv pip install unsloth
```

#### uv (Advanced)

The installation order is important, since we want the overwrite bundled dependencies with specific versions (namely, `xformers` and `triton`).

1. I prefer to use `uv` over `pip` as it's faster and better for resolving dependencies, especially for libraries which depend on `torch` but for which a specific `CUDA` version is required per this scenario.

   Install `uv`

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.local/bin/env
   ```

   Create a project dir and venv:

   ```bash
   mkdir 'unsloth-blackwell' && cd 'unsloth-blackwell'
   uv venv .venv --python=3.12 --seed
   source .venv/bin/activate
   ```
2. Install `vllm`

   ```bash
   uv pip install -U vllm --torch-backend=cu128
   ```

   Note that we have to specify `cu128`, otherwise `vllm` will install `torch==2.7.0` but with `cu126`.
3. Install `unsloth` dependencies

   ```bash
   uv pip install unsloth unsloth_zoo bitsandbytes
   ```

   If you notice weird resolving issues due to Xformers, you can also install Unsloth from source without Xformers:

   ```bash
   uv pip install -qqq \
   "unsloth_zoo[base] @ git+https://github.com/unslothai/unsloth-zoo" \
   "unsloth[base] @ git+https://github.com/unslothai/unsloth"
   ```
4. Download and build `xformers` (Optional)

   Xformers is optional, but it is definitely faster and uses less memory. We'll use PyTorch's native SDPA if you do not want Xformers. Building Xformers from source might be slow, so beware!

   ```bash
   # First uninstall xformers installed by previous libraries
   pip uninstall xformers -y

   # Clone and build
   pip install ninja
   export TORCH_CUDA_ARCH_LIST="12.0"
   git clone --depth=1 https://github.com/facebookresearch/xformers --recursive
   cd xformers && python setup.py install && cd ..
   ```

   Note that we have to explicitly set `TORCH_CUDA_ARCH_LIST=12.0`.
5. `transformers` Install any transformers version, but best to get the latest.

   ```bash
   uv pip install -U transformers
   ```

### Conda or mamba (Advanced)

1. Install `conda/mamba`

   ```bash
   curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
   ```

   Run the installation script

   ```bash
   bash Miniforge3-$(uname)-$(uname -m).sh
   ```

   Create a conda or mamba environment

   ```bash
   conda create --name unsloth-blackwell python==3.12 -y
   ```

   Activate newly created environment

   ```bash
   conda activate unsloth-blackwell
   ```
2. Install `vllm`

   Make sure you are inside the activated conda/mamba environment. You should see the name of your environment as a prefix to your terminal shell like this your `(unsloth-blackwell)user@machine:`

   ```bash
   pip install -U vllm --extra-index-url https://download.pytorch.org/whl/cu128
   ```

   Note that we have to specify `cu128`, otherwise `vllm` will install `torch==2.7.0` but with `cu126`.
3. Install `unsloth` dependencies

   Make sure you are inside the activated conda/mamba environment. You should see the name of your environment as a prefix to your terminal shell like this your `(unsloth-blackwell)user@machine:`

   ```bash
   pip install unsloth unsloth_zoo bitsandbytes
   ```
4. Download and build `xformers` (Optional)

   Xformers is optional, but it is definitely faster and uses less memory. We'll use PyTorch's native SDPA if you do not want Xformers. Building Xformers from source might be slow, so beware!

   You should see the name of your environment as a prefix to your terminal shell like this your `(unsloth-blackwell)user@machine:`

   ```bash
   # First uninstall xformers installed by previous libraries
   pip uninstall xformers -y

   # Clone and build
   pip install ninja
   export TORCH_CUDA_ARCH_LIST="12.0"
   git clone --depth=1 https://github.com/facebookresearch/xformers --recursive
   cd xformers && python setup.py install && cd ..
   ```

   Note that we have to explicitly set `TORCH_CUDA_ARCH_LIST=12.0`.
5. `Transformers` Install any transformers version, but best to get the latest.

   ```bash
   uv pip install -U transformers
   ```

If you are using mamba as your package just replace conda with mamba for all commands shown above.

Do not upgrade `triton` on its own. Each `torch` release pins the exact `triton` it was built with (which already supports Blackwell), so `pip install -U triton` causes errors like `torch ... requires triton==X, but you have triton Y which is incompatible`. If you already did, install the version named in the error, for example `pip install "triton==3.7.1"`.

### WSL-Specific Notes

If you're using WSL (Windows Subsystem for Linux) and encounter issues during xformers compilation (reminder Xformers is optional, but faster for training) follow these additional steps:

1. **Increase WSL Memory Limit** Create or edit the WSL configuration file:

   ```bash
   # Create or edit .wslconfig in your Windows user directory
   # (typically C:\Users\YourUsername\.wslconfig)

   # Add these lines to the file
   [wsl2]
   memory=16GB  # Minimum 16GB recommended for xformers compilation
   processors=4  # Adjust based on your CPU cores
   swap=2GB
   localhostForwarding=true
   ```

   After making these changes, restart WSL:

   ```powershell
   wsl --shutdown
   ```
2. **Install xformers** Use the following command to install xformers with optimized compilation for WSL:

   ```bash
   # Set CUDA architecture for Blackwell GPUs
   export TORCH_CUDA_ARCH_LIST="12.0"

   # Install xformers from source with optimized build flags
   pip install -v --no-build-isolation -U git+https://github.com/facebookresearch/xformers.git@main#egg=xformers
   ```

   The `--no-build-isolation` flag helps avoid potential build issues in WSL environments.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
