> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/deepseek-v3.1-how-to-run-locally.md).

# DeepSeek-V3.1: How to Run Locally

A guide on how to run DeepSeek-V3.1 and Terminus on your own local device!

DeepSeek’s V3.1 and **Terminus** update introduces hybrid reasoning inference, combining 'think' and 'non-think' into one model. The full 671B parameter model requires 715GB of disk space. The quantized dynamic 2-bit version uses 245GB (-75% reduction in size). GGUF: [**DeepSeek-V3.1-GGUF**](https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF)

{% hint style="success" %}
**NEW:** DeepSeek-V3.1-Terminus out now: [DeepSeek-V3.1-Terminus-GGUF](https://huggingface.co/unsloth/DeepSeek-V3.1-Terminus-GGUF)\
\
[**Sept 10, 2025 update:**](/docs/basics/dynamic-3.0-ggufs/unsloth-dynamic-ggufs-on-aider-polyglot.md) You asked for tougher benchmarks, so we’re showcasing Aider Polyglot results! Our Dynamic 3-bit DeepSeek V3.1 GGUF scores **75.6%**, surpassing many full-precision SOTA LLMs. [Read more.](/docs/basics/dynamic-3.0-ggufs/unsloth-dynamic-ggufs-on-aider-polyglot.md)

Our DeepSeek-V3.1 GGUFs include Unsloth [chat template fixes](#chat-template-bug-fixes) for llama.cpp supported backends.
{% endhint %}

All uploads use Unsloth [Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) for SOTA 5-shot MMLU and KL Divergence performance, meaning you can run & fine-tune quantized DeepSeek LLMs with minimal accuracy loss.

**Tutorials navigation:**

<a href="#run-in-llama.cpp" class="button secondary">Run in llama.cpp</a><a href="#run-in-ollama-open-webui" class="button secondary">Run in Ollama/Open WebUI</a>

## :gear: Recommended Settings

The 1-bit dynamic quant TQ1\_0 (1bit for unimportant MoE layers, 2-4bit for important MoE, and 6-8bit for rest) uses 170GB of disk space - this works well in a **1x24GB card and 128GB of RAM** with MoE offloading - it also **works natively in Ollama**!

{% hint style="info" %}
You must use `--jinja` for llama.cpp quants - this uses our [fixed chat templates](#chat-template-bug-fixes) and enables the correct template! You might get incorrect results if you do not use `--jinja`
{% endhint %}

The 2-bit quants will fit in a 1x 24GB GPU (with MoE layers offloaded to RAM). Expect around 5 tokens/s with this setup if you have bonus 128GB RAM as well. It is recommended to have at least 226GB RAM to run this 2-bit. For optimal performance you will need at least 226GB unified memory or 226GB combined RAM+VRAM for 5+ tokens/s. To learn how to increase generation speed and fit longer contexts, [read here](#improving-generation-speed).

{% hint style="success" %}
Though not a must, for best performance, have your VRAM + RAM combined equal to the size of the quant you're downloading. If not, hard drive / SSD offloading will work with llama.cpp, just inference will be slower.
{% endhint %}

## :butterfly:Chat template bug fixes

We fixed a few issues with DeepSeek V3.1's chat template since they did not function correctly in llama.cpp and other engines:

1. DeepSeek V3.1 is a hybrid reasoning model, meaning you can change the chat template to enable reasoning. The chat template introduced `thinking = True` , but other models use `enable_thinking = True` . We added the option to use `enable_thinking` as a keyword instead.
2. llama.cpp's jinja renderer via [minja](https://github.com/google/minja) does not allow the use of extra arguments in the `.split()` command, so using `.split(text, 1)` works in Python, but not in minja. We had to change this to make llama.cpp function correctly without erroring out.\
   \
   You will get the following error when using other quants:\
   `terminate called after throwing an instance of 'std::runtime_error' what(): split method must have between 1 and 1 positional arguments and between 0 and 0 keyword arguments at row 3, column 1908` We fixed it in all our quants!

### 🐳Official Recommended Settings

According to [DeepSeek](https://huggingface.co/deepseek-ai/DeepSeek-V3.1), these are the recommended settings for V3.1 inference:

* Set the <mark style="background-color:green;">**temperature 0.6**</mark> to reduce repetition and incoherence.
* Set <mark style="background-color:green;">**top\_p to 0.95**</mark> (recommended)
* **128K context length** or less
* Use `--jinja` for llama.cpp variants - we **fixed some chat template issues as well!**
* **Use** `enable_thinking = True` to use reasoning/ thinking mode. By default it's set to non reasoning.

#### :1234: Chat template/prompt format

You do not need to force `<think>\n` , but you can still add it in! With the given prefix, DeepSeek V3.1 generates responses to queries in non-thinking mode. Unlike DeepSeek V3, it introduces an additional token `</think>`.

```
<｜begin▁of▁sentence｜>{system prompt}<｜User｜>{query}<｜Assistant｜></think>
```

A BOS is forcibly added, and an EOS separates each interaction. To counteract double BOS tokens during inference, you should only call `tokenizer.encode(..., add_special_tokens = False)` since the chat template auto adds a BOS token as well. For llama.cpp / GGUF inference, you should skip the BOS since it’ll auto add it.

#### :notebook\_with\_decorative\_cover: Non-Thinking Mode (use `thinking = False`or `enable_thinking = False` and is by default)

**First-Turn**

Prefix: `<｜begin▁of▁sentence｜>{system prompt}<｜User｜>{query}<｜Assistant｜></think>`

With the given prefix, DeepSeek V3.1 generates responses to queries in non-thinking mode. Unlike DeepSeek V3, it introduces an additional token `</think>`.

**Multi-Turn**

Context: `<｜begin▁of▁sentence｜>{system prompt}<｜User｜>{query}<｜Assistant｜></think>{response}<｜end▁of▁sentence｜>...<｜User｜>{query}<｜Assistant｜></think>{response}<｜end▁of▁sentence｜>`

Prefix: `<｜User｜>{query}<｜Assistant｜></think>`

By concatenating the context and the prefix, we obtain the correct prompt for the query.

#### :books: Thinking Mode (use `thinking = True`or `enable_thinking = True` and is by default)

**First-Turn**

Prefix: `<｜begin▁of▁sentence｜>{system prompt}<｜User｜>{query}<｜Assistant｜><think>`

The prefix of thinking mode is similar to DeepSeek-R1.

**Multi-Turn**

Context: `<｜begin▁of▁sentence｜>{system prompt}<｜User｜>{query}<｜Assistant｜></think>{response}<｜end▁of▁sentence｜>...<｜User｜>{query}<｜Assistant｜></think>{response}<｜end▁of▁sentence｜>`

Prefix: `<｜User｜>{query}<｜Assistant｜><think>`

The multi-turn template is the same with non-thinking multi-turn chat template. It means the thinking token in the last turn will be dropped but the `</think>` is retained in every turn of context.

#### :bow\_and\_arrow: Tool Calling

Tool calling is supported in non-thinking mode. The format is:

`<｜begin▁of▁sentence｜>{system prompt}{tool_description}<｜User｜>{query}<｜Assistant｜></think>` where we populate the tool\_description is area after the system prompt.

## :arrow\_forward:Run DeepSeek-V3.1 Tutorials:

### :llama: Run in Ollama/Open WebUI

{% stepper %}
{% step %}
Install `ollama` if you haven't already! To run more variants of the model, [see here](#run-in-llama.cpp).

```bash
apt-get update
apt-get install pciutils -y
curl -fsSL https://ollama.com/install.sh | sh
```

{% endstep %}

{% step %}
Run the model! Note you can call `ollama serve`in another terminal if it fails! We include all our fixes and suggested parameters (temperature etc) in `params` in our Hugging Face upload!\
**(NEW) To DeepSeek-V3.1 model in Ollama, you can use our TQ1\_0 (170GB quant):**

```bash
OLLAMA_MODELS=unsloth ollama serve &

OLLAMA_MODELS=unsloth ollama run hf.co/unsloth/DeepSeek-V3.1-Terminus-GGUF:TQ1_0
```

{% endstep %}

{% step %}
To run other quants, you need to first merge the GGUF split files into 1 like the code below. Then you will need to run the model locally.

```bash
./llama.cpp/llama-gguf-split --merge \
  DeepSeek-V3.1-Terminus-GGUF/DeepSeek-V3.1-Terminus-UD-Q2_K_XL/DeepSeek-V3.1-Terminus-UD-Q2_K_XL-00001-of-00006.gguf \
	merged_file.gguf
```

```bash
OLLAMA_MODELS=unsloth ollama serve &

OLLAMA_MODELS=unsloth ollama run merged_file.gguf
```

{% endstep %}

{% step %}
Open WebUI also made a [step-by-step tutorial](https://docs.openwebui.com/tutorials/integrations/deepseekr1-dynamic/) on how to run R1 and for V3.1, you will just need to replace R1 with the new V3.1 quant.
{% endstep %}
{% endstepper %}

### ✨ Run in llama.cpp

{% stepper %}
{% step %}
Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split llama-mtmd-cli llama-server
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endstep %}

{% step %}
If you want to use `llama.cpp` directly to load models, you can do the below: (:Q2\_K\_XL) is the quantization type. You can also download via Hugging Face (point 3). This is similar to `ollama run` . Use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location. Remember the model has only a maximum of 128K context length.

{% hint style="success" %}
Please try out `-ot ".ffn_.*_exps.=CPU"` to offload all MoE layers to the CPU! This effectively allows you to fit all non MoE layers on 1 GPU, improving generation speeds. You can customize the regex expression to fit more layers if you have more GPU capacity.

If you have a bit more GPU memory, try `-ot ".ffn_(up|down)_exps.=CPU"` This offloads up and down projection MoE layers.

Try `-ot ".ffn_(up)_exps.=CPU"` if you have even more GPU memory. This offloads only up projection MoE layers.

And finally offload all layers via `-ot ".ffn_.*_exps.=CPU"` This uses the least VRAM.

You can also customize the regex, for example `-ot "\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU"` means to offload gate, up and down MoE layers but only from the 6th layer onwards.
{% endhint %}

```bash
export LLAMA_CACHE="unsloth/DeepSeek-V3.1-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/DeepSeek-V3.1-Terminus-GGUF:UD-Q2_K_XL \
    --jinja \
    --n-gpu-layers 99 \
    --temp 0.6 \
    --top-p 0.95 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407 \
    -ot ".ffn_.*_exps.=CPU"
```

{% endstep %}

{% step %}
Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD-`Q2\_K\_XL (dynamic 2bit quant) or other quantized versions like `Q4_K_M` . We <mark style="background-color:green;">**recommend using our 2.7bit dynamic quant**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**`UD-Q2_K_XL`**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**to balance size and accuracy**</mark>.

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0" # Can sometimes rate limit, so set to 0 to disable
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/DeepSeek-V3.1-Terminus-GGUF",
    local_dir = "unsloth/DeepSeek-V3.1-Terminus-GGUF",
    allow_patterns = ["*UD-Q2_K_XL*"], # Dynamic 2bit Use "*UD-TQ1_0*" for Dynamic 1bit
)
```

{% endstep %}

{% step %}
You can edit `--threads 32` for the number of CPU threads, `--ctx-size 16384` for context length, `--n-gpu-layers 2` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/DeepSeek-V3.1-Terminus-GGUF/UD-Q2_K_XL/DeepSeek-V3.1-Terminus-UD-Q2_K_XL-00001-of-00006.gguf \
    --jinja \
    --n-gpu-layers 99 \
    --temp 0.6 \
    --top-p 0.95 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407 \
    -ot ".ffn_.*_exps.=CPU"
```

{% endcode %}
{% endstep %}

{% step %}
Get the 1bit version (170GB) if you don't have enough combined RAM and VRAM:

```python
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/DeepSeek-V3.1-Terminus-GGUF",
    local_dir = "unsloth/DeepSeek-V3.1-Terminus-GGUF",
    allow_patterns = ["*UD-TQ1_0*"], # Use "*UD-Q2_K_XL*" for Dynamic 2bit
)
```

{% endstep %}
{% endstepper %}

### ✨ Deploy with llama-server and OpenAI's completion library

To use llama-server for deployment, use the following command:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-server \
    --model unsloth/DeepSeek-V3.1-Terminus-GGUF/DeepSeek-V3.1-Terminus-UD-TQ1_0.gguf \
    --alias "unsloth/DeepSeek-V3.1-Terminus" \
    --n-gpu-layers 999 \
    -ot ".ffn_.*_exps.=CPU" \
    --prio 3 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --port 8001 \
    --jinja
```

{% endcode %}

Then use OpenAI's Python library after `pip install openai` :

```python
from openai import OpenAI
import json
openai_client = OpenAI(
    base_url = "http://127.0.0.1:8001/v1",
    api_key = "sk-no-key-required",
)
completion = openai_client.chat.completions.create(
    model = "unsloth/DeepSeek-V3.1-Terminus",
    messages = [{"role": "user", "content": "What is 2+2?"},],
)
print(completion.choices[0].message.content)
```

## :minidisc:Model uploads

**ALL our uploads** - including those that are not imatrix-based or dynamic, utilize our calibration dataset, which is specifically optimized for conversational, coding, and language tasks.

* Full DeepSeek-V3.1 model uploads below:

We also uploaded [IQ4\_NL](https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF/tree/main/IQ4_NL) and [Q4\_1](https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF/tree/main/Q4_1) quants which run specifically faster for ARM and Apple devices respectively.

<table data-full-width="false"><thead><tr><th>MoE Bits</th><th>Type + Link</th><th>Disk Size</th><th>Details</th></tr></thead><tbody><tr><td>1.66bit</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF?show_file_info=DeepSeek-V3.1-UD-TQ1_0.gguf">TQ1_0</a></td><td><strong>170GB</strong></td><td>1.92/1.56bit</td></tr><tr><td>1.78bit</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF/tree/main/UD-IQ1_S">IQ1_S</a></td><td><strong>185GB</strong></td><td>2.06/1.56bit</td></tr><tr><td>1.93bit</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF/tree/main/UD-IQ1_M">IQ1_M</a></td><td><strong>200GB</strong></td><td>2.5/2.06/1.56</td></tr><tr><td>2.42bit</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF/tree/main/UD-IQ2_XXS">IQ2_XXS</a></td><td><strong>216GB</strong></td><td>2.5/2.06bit</td></tr><tr><td>2.71bit</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF/tree/main/UD-Q2_K_XL">Q2_K_XL</a></td><td><strong>251GB</strong></td><td>3.5/2.5bit</td></tr><tr><td>3.12bit</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF/tree/main/UD-IQ3_XXS">IQ3_XXS</a></td><td><strong>273GB</strong></td><td>3.5/2.06bit</td></tr><tr><td>3.5bit</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF/tree/main/UD-Q3_K_XL">Q3_K_XL</a></td><td><strong>296GB</strong></td><td>4.5/3.5bit</td></tr><tr><td>4.5bit</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF/tree/main/UD-Q4_K_XL">Q4_K_XL</a></td><td><strong>384GB</strong></td><td>5.5/4.5bit</td></tr><tr><td>5.5bit</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3.1-GGUF/tree/main/UD-Q5_K_XL">Q5_K_XL</a></td><td><strong>481GB</strong></td><td>6.5/5.5bit</td></tr></tbody></table>

We've also uploaded versions in [BF16 format](https://huggingface.co/unsloth/DeepSeek-V3.1-BF16), and original [FP8 (float8) format](https://huggingface.co/unsloth/DeepSeek-V3.1).

## :snowboarder: Improving generation speed

If you have more VRAM, you can try offloading more MoE layers, or offloading whole layers themselves.

Normally, `-ot ".ffn_.*_exps.=CPU"` offloads all MoE layers to the CPU! This effectively allows you to fit all non MoE layers on 1 GPU, improving generation speeds. You can customize the regex expression to fit more layers if you have more GPU capacity.

If you have a bit more GPU memory, try `-ot ".ffn_(up|down)_exps.=CPU"` This offloads up and down projection MoE layers.

Try `-ot ".ffn_(up)_exps.=CPU"` if you have even more GPU memory. This offloads only up projection MoE layers.

You can also customize the regex, for example `-ot "\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU"` means to offload gate, up and down MoE layers but only from the 6th layer onwards.

The [latest llama.cpp release](https://github.com/ggml-org/llama.cpp/pull/14363) also introduces high throughput mode. Use `llama-parallel`. Read more about it [here](https://github.com/ggml-org/llama.cpp/tree/master/examples/parallel). You can also **quantize the KV cache to 4bits** for example to reduce VRAM / RAM movement, which can also make the generation process faster.

## 📐How to fit long context (full 128K)

To fit longer context, you can use **KV cache quantization** to quantize the K and V caches to lower bits. This can also increase generation speed due to reduced RAM / VRAM data movement. The allowed options for K quantization (default is `f16`) include the below.

`--cache-type-k f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1`

You should use the `_1` variants for somewhat increased accuracy, albeit it's slightly slower. For eg `q4_1, q5_1`

You can also quantize the V cache, but you will need to **compile llama.cpp with Flash Attention** support via `-DGGML_CUDA_FA_ALL_QUANTS=ON`, and use `--flash-attn` to enable it. Then you can use together with `--cache-type-k` :

`--cache-type-v f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1`


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/deepseek-v3.1-how-to-run-locally.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
