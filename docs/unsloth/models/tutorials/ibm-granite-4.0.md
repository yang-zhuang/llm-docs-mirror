> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/ibm-granite-4.0.md).

# IBM Granite 4.0

How to run IBM Granite-4.0 with Unsloth GGUFs on llama.cpp, Ollama and how to fine-tune!

IBM releases Granite-4.0 models with 3 sizes including **Nano** (350M & 1B), **Micro** (3B), **Tiny** (7B/1B active) and **Small** (32B/9B active). Trained on 15T tokens, IBM’s new Hybrid (H) Mamba architecture enables Granite-4.0 models to run faster with lower memory use.

Learn [how to run](#run-granite-4.0-tutorials) Unsloth Granite-4.0 Dynamic GGUFs or fine-tune/RL the model. You can [fine-tune Granite-4.0](#fine-tuning-granite-4.0-in-unsloth) with our free Colab notebook for a support agent use-case.

<a href="#run-granite-4.0-tutorials" class="button secondary">Running Tutorial</a><a href="#fine-tuning-granite-4.0-in-unsloth" class="button secondary">Fine-tuning Tutorial</a>

**Unsloth Granite-4.0 uploads:**

<table><thead><tr><th width="249">Dynamic GGUFs</th><th>Dynamic 4-bit + FP8</th><th>16-bit Instruct</th></tr></thead><tbody><tr><td><ul><li><a href="https://huggingface.co/unsloth/granite-4.0-h-350m-GGUF">H-350M</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-350m-GGUF">350M</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-h-1b-GGUF">H-1B</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-1b-GGUF">1B</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-h-small-GGUF">H-Small</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-h-tiny-GGUF">H-Tiny</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-h-micro-GGUF">H-Micro</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-micro-GGUF">Micro</a></li></ul></td><td><p>Dynamic 4-bit Instruct:</p><ul><li><a href="https://huggingface.co/unsloth/granite-4.0-h-micro-unsloth-bnb-4bit">H-Micro</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-micro-unsloth-bnb-4bit">Micro</a></li></ul><p>FP8 Dynamic:</p><ul><li><a href="https://huggingface.co/unsloth/granite-4.0-h-small-FP8-Dynamic">H-Small FP8</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-h-tiny-FP8-Dynamic">H-Tiny FP8</a></li></ul></td><td><ul><li><a href="https://huggingface.co/unsloth/granite-4.0-h-350m">H-350M</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-350m">350M</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-h-1b">H-1B</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-1b">1B</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-h-small">H-Small</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-h-tiny">H-Tiny</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-h-micro">H-Micro</a></li><li><a href="https://huggingface.co/unsloth/granite-4.0-micro">Micro</a></li></ul></td></tr></tbody></table>

You can also view our [Granite-4.0 collection](https://huggingface.co/collections/unsloth/granite-40-68ddf64b4a8717dc22a9322d) for all uploads including Dynamic Float8 quants etc.

**Granite-4.0 Models Explanations:**

* **Nano and H-Nano:** The 350M and 1B models offer strong instruction-following abilities, enabling advanced on-device and edge AI and research/fine-tuning applications.
* **H-Small (MoE):** Enterprise workhorse for daily tasks, supports multiple long-context sessions on entry GPUs like L40S (32B total, 9B active).
* **H-Tiny (MoE):** Fast, cost-efficient for high-volume, low-complexity tasks; optimized for local and edge use (7B total, 1B active).
* **H-Micro (Dense):** Lightweight, efficient for high-volume, low-complexity workloads; ideal for local and edge deployment (3B total).
* **Micro (Dense):** Alternative dense option when Mamba2 isn’t fully supported (3B total).

## Run Granite-4.0 Tutorials

### :gear: Recommended Inference Settings

IBM recommends these settings:

`temperature=0.0`, `top_p=1.0`, `top_k=0`

* <mark style="background-color:green;">**Temperature of 0.0**</mark>
* Top\_K = 0
* Top\_P = 1.0
* Recommended minimum context: 16,384
* Maximum context length window: 131,072 (128K context)

**Chat template:**

```
<|start_of_role|>system<|end_of_role|>You are a helpful assistant. Please ensure responses are professional, accurate, and safe.<|end_of_text|>
<|start_of_role|>user<|end_of_role|>Please list one IBM Research laboratory located in the United States. You should only output its name and location.<|end_of_text|>
<|start_of_role|>assistant<|end_of_role|>Almaden Research Center, San Jose, California<|end_of_text|>
```

### :llama: Ollama: Run Granite-4.0 Tutorial

1. Install `ollama` if you haven't already!

```bash
apt-get update
apt-get install pciutils -y
curl -fsSL https://ollama.com/install.sh | sh
```

2. Run the model! Note you can call `ollama serve`in another terminal if it fails! We include all our fixes and suggested parameters (temperature etc) in `params` in our Hugging Face upload! You can change the model name '`granite-4.0-h-small-GGUF`' to any Granite model like 'granite-4.0-h-micro:Q8\_K\_XL'.

```bash
ollama run hf.co/unsloth/granite-4.0-h-small-GGUF:UD-Q4_K_XL
```

### 📖 llama.cpp: Run Granite-4.0 Tutorial

1. Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

2. If you want to use `llama.cpp` directly to load models, you can do the below: (:Q4\_K\_XL) is the quantization type. You can also download via Hugging Face (point 3). This is similar to `ollama run`

```bash
./llama.cpp/llama-cli \
    -hf unsloth/granite-4.0-h-small-GGUF:UD-Q4_K_XL
```

3. **OR** download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose Q4\_K\_M, or other quantized versions (like BF16 full precision).

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/granite-4.0-h-small-GGUF",
    local_dir = "unsloth/granite-4.0-h-small-GGUF",
    allow_patterns = ["*UD-Q4_K_XL*"], # For Q4_K_M
)
```

4. Run Unsloth's Flappy Bird test
5. Edit `--threads 32` for the number of CPU threads, `--ctx-size 16384` for context length (Granite-4.0 supports 128K context length!), `--n-gpu-layers 99` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.
6. For conversation mode:

```bash
./llama.cpp/llama-mtmd-cli \
    --model unsloth/granite-4.0-h-small-GGUF/granite-4.0-h-small-UD-Q4_K_XL.gguf \
    --jinja \
    --ctx-size 16384 \
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.0 \
    --top-k 0 \
    --top-p 1.0
```

### 🐋 Docker: Run Granite-4.0 Tutorial

If you already have Docker desktop, all your need to do is run the command below and you're done:

```bash
docker model pull hf.co/unsloth/granite-4.0-h-small-GGUF:UD-Q4_K_XL
```

## :sloth: Fine-tuning Granite-4.0 in Unsloth

Unsloth now supports all Granite 4.0 models including nano, micro, tiny and small for fine-tuning. Training is 2x faster, use 50% less VRAM and supports 6x longer context lengths. Granite-4.0 micro and tiny fit comfortably in a 15GB VRAM T4 GPU.

* **Granite-4.0** [**free fine-tuning notebook**](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Granite4.0.ipynb)
* Granite-4.0-350M [fine-tuning notebook](https://github.com/unslothai/notebooks/blob/main/nb/Granite4.0_350M.ipynb)

This notebook trains a model to become a Support Agent that understands customer interactions, complete with analysis and recommendations. This setup allows you to train a bot that provides real-time assistance to support agents.

We also show you how to train a model using data stored in a Google Sheet.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-3e28a77b82c05f317dd8e648783903eb0ecb9c6e%2Fgranite%204%20colab.png?alt=media" alt="" width="563"><figcaption></figcaption></figure>

**Unsloth config for Granite-4.0:**

```python
!pip install --upgrade unsloth
from unsloth import FastLanguageModel
import torch
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/granite-4.0-h-micro",
    max_seq_length = 2048,   # Context length - can be longer, but uses more memory
    load_in_4bit = True,     # 4bit uses much less memory
    load_in_8bit = False,    # A bit more accurate, uses 2x memory
    full_finetuning = False, # We have full finetuning now!
    # token = "hf_...",      # use one if using gated models
)
```

If you have an old version of Unsloth and/or are fine-tuning locally, install the latest version of Unsloth:

```
pip install --upgrade --force-reinstall --no-cache-dir unsloth unsloth_zoo
```


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/ibm-granite-4.0.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
