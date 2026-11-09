> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/devstral-how-to-run-and-fine-tune.md).

# Devstral: How to Run & Fine-tune

Run and fine-tune Mistral Devstral 1.1, including Small-2507 and 2505.

**Devstral-Small-2507** (Devstral 1.1) is Mistral's new agentic LLM for software engineering. It excels at tool-calling, exploring codebases, and powering coding agents. Mistral AI released the original 2505 version in May, 2025.

Finetuned from [**Mistral-Small-3.1**](https://huggingface.co/unsloth/Mistral-Small-3.1-24B-Instruct-2503-GGUF), Devstral supports a 128k context window. Devstral Small 1.1 has improved performance, achieving a score of 53.6% performance on [SWE-bench verified](https://openai.com/index/introducing-swe-bench-verified/), making it (July 10, 2025) the #1 open model on the benchmark.

Unsloth Devstral 1.1 GGUFs contain additional <mark style="background-color:green;">**tool-calling support**</mark> and <mark style="background-color:green;">**chat template fixes**</mark>. Devstral 1.1 still works well with OpenHands but now also generalizes better to other prompts and coding environments.

As text-only, Devstral’s vision encoder was removed prior to fine-tuning. We've added [*<mark style="background-color:green;">**optional Vision support**</mark>*](#possible-vision-support) for the model.

{% hint style="success" %}
We also worked with Mistral behind the scenes to help debug, test and correct any possible bugs and issues! Make sure to **download Mistral's official downloads or Unsloth's GGUFs** / dynamic quants to get the **correct implementation** (ie correct system prompt, correct chat template etc)

Please use `--jinja` in llama.cpp to enable the system prompt!
{% endhint %}

All Devstral uploads use our Unsloth [Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) methodology, delivering the best performance on 5-shot MMLU and KL Divergence benchmarks. This means, you can run and fine-tune quantized Mistral LLMs with minimal accuracy loss!

#### **Devstral - Unsloth Dynamic** quants:

| Devstral 2507 (new)                                                                                                    | Devstral 2505                                                                                               |
| ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| GGUF: [Devstral-Small-2507-GGUF](https://huggingface.co/unsloth/Devstral-Small-2507-GGUF)                              | [Devstral-Small-2505-GGUF](https://huggingface.co/unsloth/Devstral-Small-2505-GGUF)                         |
| 4-bit BnB: [Devstral-Small-2507-unsloth-bnb-4bit](https://huggingface.co/unsloth/Devstral-Small-2507-unsloth-bnb-4bit) | [Devstral-Small-2505-unsloth-bnb-4bit](https://huggingface.co/unsloth/Devstral-Small-2505-unsloth-bnb-4bit) |

## 🖥️ **Running Devstral**

### :gear: Official Recommended Settings

According to Mistral AI, these are the recommended settings for inference:

* <mark style="background-color:blue;">**Temperature from 0.0 to 0.15**</mark>
* Min\_P of 0.01 (optional, but 0.01 works well, llama.cpp default is 0.1)
* <mark style="background-color:orange;">**Use**</mark><mark style="background-color:orange;">**&#x20;**</mark><mark style="background-color:orange;">**`--jinja`**</mark><mark style="background-color:orange;">**&#x20;**</mark><mark style="background-color:orange;">**to enable the system prompt.**</mark>

**A system prompt is recommended**, and is a derivative of Open Hand's system prompt. The full system prompt is provided [here](https://huggingface.co/unsloth/Devstral-Small-2505/blob/main/SYSTEM_PROMPT.txt).

```
You are Devstral, a helpful agentic model trained by Mistral AI and using the OpenHands scaffold. You can interact with a computer to solve tasks.

<ROLE>
Your primary role is to assist users by executing commands, modifying code, and solving technical problems effectively. You should be thorough, methodical, and prioritize quality over speed.
* If the user asks a question, like "why is X happening", don't try to fix the problem. Just give an answer to the question.
</ROLE>

.... SYSTEM PROMPT CONTINUES ....
```

{% hint style="success" %}
Our dynamic uploads have the '`UD`' prefix in them. Those without are not dynamic however still utilize our calibration dataset.
{% endhint %}

## :llama: Tutorial: How to Run Devstral in Ollama

1. Install `ollama` if you haven't already!

```bash
apt-get update
apt-get install pciutils -y
curl -fsSL https://ollama.com/install.sh | sh
```

2. Run the model with our dynamic quant. Note you can call `ollama serve &`in another terminal if it fails! We include all suggested parameters (temperature etc) in `params` in our Hugging Face upload!
3. Also Devstral supports 128K context lengths, so best to enable [**KV cache quantization**](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-set-the-quantization-type-for-the-kv-cache). We use 8bit quantization which saves 50% memory usage. You can also try `"q4_0"`

```bash
export OLLAMA_KV_CACHE_TYPE="q8_0"
ollama run hf.co/unsloth/Devstral-Small-2507-GGUF:UD-Q4_K_XL
```

## 📖 Tutorial: How to Run Devstral in llama.cpp

1. Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split llama-mtmd-cli
cp llama.cpp/build/bin/llama-* llama.cpp
```

2. If you want to use `llama.cpp` directly to load models, you can do the below: (:Q4\_K\_XL) is the quantization type. You can also download via Hugging Face (point 3). This is similar to `ollama run`

```bash
./llama.cpp/llama-cli -hf unsloth/Devstral-Small-2507-GGUF:UD-Q4_K_XL --jinja
```

3. **OR** download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose Q4\_K\_M, or other quantized versions (like BF16 full precision).

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Devstral-Small-2507-GGUF",
    local_dir = "unsloth/Devstral-Small-2507-GGUF",
    allow_patterns = ["*Q4_K_XL*", "*mmproj-F16*"], # For Q4_K_XL
)
```

4. Run the model.
5. Edit `--threads -1` for the maximum CPU threads, `--ctx-size 131072` for context length (Devstral supports 128K context length!), `--n-gpu-layers 99` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference. We also use 8bit quantization for the K cache to reduce memory usage.
6. For conversation mode:

<pre class="language-bash"><code class="lang-bash">./llama.cpp/llama-cli \
    --model unsloth/Devstral-Small-2507-GGUF/Devstral-Small-2507-UD-Q4_K_XL.gguf \
    --threads -1 \
    --ctx-size 131072 \
    <a data-footnote-ref href="#user-content-fn-1">--cache-type-k q8_0</a> \
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.15 \
    --repeat-penalty 1.0 \
    --min-p 0.01 \
    --top-k 64 \
    --top-p 0.95 \
    <a data-footnote-ref href="#user-content-fn-2">--jinja</a>
</code></pre>

7. For non conversation mode to test our Flappy Bird prompt:

<pre class="language-bash"><code class="lang-bash">./llama.cpp/llama-cli \
    --model unsloth/Devstral-Small-2507-GGUF/Devstral-Small-2507-UD-Q4_K_XL.gguf \
    --threads -1 \
    --ctx-size 131072 \
    <a data-footnote-ref href="#user-content-fn-1">--cache-type-k q8_0</a> \
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.15 \
    --repeat-penalty 1.0 \
    --min-p 0.01 \
    --top-k 64 \
    --top-p 0.95 \
    -no-cnv \
    --prompt "[SYSTEM_PROMPT]You are Devstral, a helpful agentic model trained by Mistral AI and using the OpenHands scaffold. You can interact with a computer to solve tasks.\n\n&#x3C;ROLE>\nYour primary role is to assist users by executing commands, modifying code, and solving technical problems effectively. You should be thorough, methodical, and prioritize quality over speed.\n* If the user asks a question, like "why is X happening", don\'t try to fix the problem. Just give an answer to the question.\n&#x3C;/ROLE>\n\n&#x3C;EFFICIENCY>\n* Each action you take is somewhat expensive. Wherever possible, combine multiple actions into a single action, e.g. combine multiple bash commands into one, using sed and grep to edit/view multiple files at once.\n* When exploring the codebase, use efficient tools like find, grep, and git commands with appropriate filters to minimize unnecessary operations.\n&#x3C;/EFFICIENCY>\n\n&#x3C;FILE_SYSTEM_GUIDELINES>\n* When a user provides a file path, do NOT assume it\'s relative to the current working directory. First explore the file system to locate the file before working on it.\n* If asked to edit a file, edit the file directly, rather than creating a new file with a different filename.\n* For global search-and-replace operations, consider using `sed` instead of opening file editors multiple times.\n&#x3C;/FILE_SYSTEM_GUIDELINES>\n\n&#x3C;CODE_QUALITY>\n* Write clean, efficient code with minimal comments. Avoid redundancy in comments: Do not repeat information that can be easily inferred from the code itself.\n* When implementing solutions, focus on making the minimal changes needed to solve the problem.\n* Before implementing any changes, first thoroughly understand the codebase through exploration.\n* If you are adding a lot of code to a function or file, consider splitting the function or file into smaller pieces when appropriate.\n&#x3C;/CODE_QUALITY>\n\n&#x3C;VERSION_CONTROL>\n* When configuring git credentials, use "openhands" as the user.name and "openhands@all-hands.dev" as the user.email by default, unless explicitly instructed otherwise.\n* Exercise caution with git operations. Do NOT make potentially dangerous changes (e.g., pushing to main, deleting repositories) unless explicitly asked to do so.\n* When committing changes, use `git status` to see all modified files, and stage all files necessary for the commit. Use `git commit -a` whenever possible.\n* Do NOT commit files that typically shouldn\'t go into version control (e.g., node_modules/, .env files, build directories, cache files, large binaries) unless explicitly instructed by the user.\n* If unsure about committing certain files, check for the presence of .gitignore files or ask the user for clarification.\n&#x3C;/VERSION_CONTROL>\n\n&#x3C;PULL_REQUESTS>\n* When creating pull requests, create only ONE per session/issue unless explicitly instructed otherwise.\n* When working with an existing PR, update it with new commits rather than creating additional PRs for the same issue.\n* When updating a PR, preserve the original PR title and purpose, updating description only when necessary.\n&#x3C;/PULL_REQUESTS>\n\n&#x3C;PROBLEM_SOLVING_WORKFLOW>\n1. EXPLORATION: Thoroughly explore relevant files and understand the context before proposing solutions\n2. ANALYSIS: Consider multiple approaches and select the most promising one\n3. TESTING:\n   * For bug fixes: Create tests to verify issues before implementing fixes\n   * For new features: Consider test-driven development when appropriate\n   * If the repository lacks testing infrastructure and implementing tests would require extensive setup, consult with the user before investing time in building testing infrastructure\n   * If the environment is not set up to run tests, consult with the user first before investing time to install all dependencies\n4. IMPLEMENTATION: Make focused, minimal changes to address the problem\n5. VERIFICATION: If the environment is set up to run tests, test your implementation thoroughly, including edge cases. If the environment is not set up to run tests, consult with the user first before investing time to run tests.\n&#x3C;/PROBLEM_SOLVING_WORKFLOW>\n\n&#x3C;SECURITY>\n* Only use GITHUB_TOKEN and other credentials in ways the user has explicitly requested and would expect.\n* Use APIs to work with GitHub or other platforms, unless the user asks otherwise or your task requires browsing.\n&#x3C;/SECURITY>\n\n&#x3C;ENVIRONMENT_SETUP>\n* When user asks you to run an application, don\'t stop if the application is not installed. Instead, please install the application and run the command again.\n* If you encounter missing dependencies:\n  1. First, look around in the repository for existing dependency files (requirements.txt, pyproject.toml, package.json, Gemfile, etc.)\n  2. If dependency files exist, use them to install all dependencies at once (e.g., `pip install -r requirements.txt`, `npm install`, etc.)\n  3. Only install individual packages directly if no dependency files are found or if only specific packages are needed\n* Similarly, if you encounter missing dependencies for essential tools requested by the user, install them when possible.\n&#x3C;/ENVIRONMENT_SETUP>\n\n&#x3C;TROUBLESHOOTING>\n* If you\'ve made repeated attempts to solve a problem but tests still fail or the user reports it\'s still broken:\n  1. Step back and reflect on 5-7 different possible sources of the problem\n  2. Assess the likelihood of each possible cause\n  3. Methodically address the most likely causes, starting with the highest probability\n  4. Document your reasoning process\n* When you run into any major issue while executing a plan from the user, please don\'t try to directly work around it. Instead, propose a new plan and confirm with the user before proceeding.\n&#x3C;/TROUBLESHOOTING>[/SYSTEM_PROMPT][INST]Create a Flappy Bird game in Python. You must include these things:\n1. You must use pygame.\n2. The background color should be randomly chosen and is a light shade. Start with a light blue color.\n3. Pressing SPACE multiple times will accelerate the bird.\n4. The bird\'s shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.\n5. Place on the bottom some land colored as dark brown or yellow chosen randomly.\n6. Make a score shown on the top right side. Increment if you pass pipes and don\'t hit them.\n7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.\n8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.\nThe final game should be inside a markdown section in Python. Check your code for error[/INST]"
</code></pre>

{% hint style="danger" %}
Remember to remove \<bos> since Devstral auto adds a \<bos>! Also please use `--jinja` to enable the system prompt!
{% endhint %}

## :eyes:Experimental Vision Support

[Xuan-Son](https://x.com/ngxson) from Hugging Face showed in their [GGUF repo](https://huggingface.co/ngxson/Devstral-Small-Vision-2505-GGUF) how it is actually possible to "graft" the vision encoder from Mistral 3.1 Instruct onto Devstral 2507. We also uploaded our mmproj files which allows you to use the following:

```bash
./llama.cpp/llama-mtmd-cli \
    --model unsloth/Devstral-Small-2507-GGUF/Devstral-Small-2507-UD-Q4_K_XL.gguf \
    --mmproj unsloth/Devstral-Small-2507-GGUF/mmproj-F16.gguf \
    --threads -1 \
    --ctx-size 131072 \
    --cache-type-k q8_0 \
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.15
```

For example:

| Instruction and output code                                                                                   | Rendered code                                                                                                 |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| ![](https://cdn-uploads.huggingface.co/production/uploads/63ca214abedad7e2bf1d1517/HDic53ANsCoJbiWu2eE6K.png) | ![](https://cdn-uploads.huggingface.co/production/uploads/63ca214abedad7e2bf1d1517/onV1xfJIT8gzh81RkLn8J.png) |

## 🦥 Fine-tuning Devstral with Unsloth

Just like standard Mistral models including Mistral Small 3.1, Unsloth supports Devstral fine-tuning. Training is 2x faster, use 70% less VRAM and supports 8x longer context lengths. Devstral fits comfortably in a 24GB VRAM L4 GPU.

Unfortunately, Devstral slightly exceeds the memory limits of a 16GB VRAM, so fine-tuning it for free on Google Colab isn't possible for now. However, you *can* fine-tune the model for free using our [Kaggle notebook](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Magistral_\(24B\)-Reasoning-Conversational.ipynb\&accelerator=nvidiaTeslaT4), which offers access to dual GPUs. Just change the notebook's Magistral model name to the Devstral model.

If you have an old version of Unsloth and/or are fine-tuning locally, install the latest version of Unsloth:

```bash
pip install --upgrade --force-reinstall --no-cache-dir unsloth unsloth_zoo
```

[^1]: K quantization to reduce memory use. Can be f16, q8\_0, q4\_0

[^2]: Must use --jinja to enable system prompt


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/devstral-how-to-run-and-fine-tune.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
