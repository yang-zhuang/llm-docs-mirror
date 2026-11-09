> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/phi-4-reasoning-how-to-run-and-fine-tune.md).

# Phi-4 Reasoning: How to Run & Fine-tune

Learn to run & fine-tune Phi-4 reasoning models locally with Unsloth + our Dynamic 2.0 quants

Microsoft's new Phi-4 reasoning models are now supported in Unsloth. The 'plus' variant performs on par with OpenAI's o1-mini, o3-mini and Sonnet 3.7. The 'plus' and standard reasoning models are 14B parameters while the 'mini' has 4B parameters.\
\
All Phi-4 reasoning uploads use our [Unsloth Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) methodology.

#### **Phi-4 reasoning - Unsloth Dynamic 2.0 uploads:**

| Dynamic 2.0 GGUF (to run)                                                                                                                                                                                                                                                                                    | Dynamic 4-bit Safetensor (to finetune/deploy)                                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <ul><li><a href="https://huggingface.co/unsloth/Phi-4-reasoning-plus-GGUF/">Reasoning-plus</a> (14B)</li><li><a href="https://huggingface.co/unsloth/Phi-4-reasoning-GGUF">Reasoning</a> (14B)</li><li><a href="https://huggingface.co/unsloth/Phi-4-mini-reasoning-GGUF/">Mini-reasoning</a> (4B)</li></ul> | <ul><li><a href="https://huggingface.co/unsloth/Phi-4-reasoning-plus-unsloth-bnb-4bit">Reasoning-plus</a></li><li><a href="https://huggingface.co/unsloth/phi-4-reasoning-unsloth-bnb-4bit">Reasoning</a></li><li><a href="https://huggingface.co/unsloth/Phi-4-mini-reasoning-unsloth-bnb-4bit">Mini-reasoning</a></li></ul> |

## 🖥️ **Running Phi-4 reasoning**

### :gear: Official Recommended Settings

According to Microsoft, these are the recommended settings for inference:

* <mark style="background-color:blue;">**Temperature = 0.8**</mark>
* Top\_P = 0.95

### **Phi-4 reasoning Chat templates**

Please ensure you use the correct chat template as the 'mini' variant has a different one.

#### **Phi-4-mini:**

{% code overflow="wrap" %}

```
<|system|>Your name is Phi, an AI math expert developed by Microsoft.<|end|><|user|>How to solve 3*x^2+4*x+5=1?<|end|><|assistant|>
```

{% endcode %}

#### **Phi-4-reasoning and Phi-4-reasoning-plus:**

This format is used for general conversation and instructions:

{% code overflow="wrap" %}

```
<|im_start|>system<|im_sep|>You are Phi, a language model trained by Microsoft to help users. Your role as an assistant involves thoroughly exploring questions through a systematic thinking process before providing the final precise and accurate solutions. This requires engaging in a comprehensive cycle of analysis, summarizing, exploration, reassessment, reflection, backtracing, and iteration to develop well-considered thinking process. Please structure your response into two main sections: Thought and Solution using the specified format: <think> {Thought section} </think> {Solution section}. In the Thought section, detail your reasoning process in steps. Each step should include detailed considerations such as analysing questions, summarizing relevant findings, brainstorming new ideas, verifying the accuracy of the current steps, refining any errors, and revisiting previous steps. In the Solution section, based on various attempts, explorations, and reflections from the Thought section, systematically present the final solution that you deem correct. The Solution section should be logical, accurate, and concise and detail necessary steps needed to reach the conclusion. Now, try to solve the following question through the above guidelines:<|im_end|><|im_start|>user<|im_sep|>What is 1+1?<|im_end|><|im_start|>assistant<|im_sep|>
```

{% endcode %}

{% hint style="info" %}
Yes, the chat template/prompt format is this long!
{% endhint %}

### 🦙 Ollama: Run Phi-4 reasoning Tutorial

1. Install `ollama` if you haven't already!

```bash
apt-get update
apt-get install pciutils -y
curl -fsSL https://ollama.com/install.sh | sh
```

2. Run the model! Note you can call `ollama serve`in another terminal if it fails. We include all our fixes and suggested parameters (temperature etc) in `params` in our Hugging Face upload.

```bash
ollama run hf.co/unsloth/Phi-4-mini-reasoning-GGUF:Q4_K_XL
```

### 📖 Llama.cpp: Run Phi-4 reasoning Tutorial

{% hint style="warning" %}
You must use `--jinja` in llama.cpp to enable reasoning for the models, expect for the 'mini' variant. Otherwise no token will be provided.
{% endhint %}

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

2. Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose Q4\_K\_M, or other quantized versions.

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Phi-4-mini-reasoning-GGUF",
    local_dir = "unsloth/Phi-4-mini-reasoning-GGUF",
    allow_patterns = ["*UD-Q4_K_XL*"],
)
```

3. Run the model in conversational mode in llama.cpp. You must use `--jinja` in llama.cpp to enable reasoning for the models. This is however not needed if you're using the 'mini' variant.

```bash
./llama.cpp/llama-cli \
    --model unsloth/Phi-4-mini-reasoning-GGUF/Phi-4-mini-reasoning-UD-Q4_K_XL.gguf \
    --threads -1 \
    --n-gpu-layers 99 \
    --prio 3 \
    --temp 0.8 \
    --top-p 0.95 \
    --jinja \
    --min-p 0.00 \
    --ctx-size 32768 \
    --seed 3407
```

## 🦥 Fine-tuning Phi-4 with Unsloth

[Phi-4 fine-tuning](https://unsloth.ai/blog/phi4) for the models are also now supported in Unsloth. To fine-tune for free on Google Colab, just change the `model_name` of 'unsloth/Phi-4' to 'unsloth/Phi-4-mini-reasoning' etc.

* [Phi-4 (14B) fine-tuning notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Phi_4-Conversational.ipynb)


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/phi-4-reasoning-how-to-run-and-fine-tune.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
