> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/grok-2.md).

# Grok 2

Run xAI's Grok 2 model locally!

You can now run **Grok 2** (aka Grok 2.5), the 270B parameter model by xAI. Full precision requires **539GB**, while the Unsloth Dynamic 3-bit version shrinks size down to just **118GB** (a 75% reduction). GGUF: [Grok-2-GGUF](https://huggingface.co/unsloth/grok-2-GGUF)

The **3-bit Q3\_K\_XL** model runs on a single **128GB Mac** or **24GB VRAM + 128GB RAM**, achieving **5+ tokens/s** inference. Thanks to the llama.cpp team and community for [supporting Grok 2](https://github.com/ggml-org/llama.cpp/pull/15539) and making this possible. We were also glad to have helped a little along the way!

All uploads use Unsloth [Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) for SOTA 5-shot MMLU and KL Divergence performance, meaning you can run quantized Grok LLMs with minimal accuracy loss.

<a href="#run-in-llama.cpp" class="button secondary">Run in llama.cpp Tutorial</a>

## :gear: Recommended Settings

The 3-bit dynamic quant uses 118GB (126GiB) of disk space - this works well in a 128GB RAM unified memory Mac or on a 1x24GB card and 128GB of RAM. It is recommended to have at least 120GB RAM to run this 3-bit quant.

{% hint style="warning" %}
You must use `--jinja` for Grok 2. You might get incorrect results if you do not use `--jinja`
{% endhint %}

The 8-bit quant is \~300GB in size will fit in a 1x 80GB GPU (with MoE layers offloaded to RAM). Expect around 5 tokens/s with this setup if you have bonus 200GB RAM as well. To learn how to increase generation speed and fit longer contexts, [read here](#improving-generation-speed).

{% hint style="info" %}
Though not a must, for best performance, have your VRAM + RAM combined equal to the size of the quant you're downloading. If not, hard drive / SSD offloading will work with llama.cpp, just inference will be slower.
{% endhint %}

### Sampling parameters

* Grok 2 has a 128K max context length thus, use `131,072` context or less.
* Use `--jinja` for llama.cpp variants

There are no official sampling parameters to run the model, thus you can use standard defaults for most models:

* Set the <mark style="background-color:green;">**temperature = 1.0**</mark>
* <mark style="background-color:green;">**Min\_P = 0.01**</mark> (optional, but 0.01 works well, llama.cpp default is 0.1)

## Run Grok 2 Tutorial:

Currently you can only run Grok 2 in llama.cpp.

### ✨ Run in llama.cpp

{% stepper %}
{% step %}
Install the specific `llama.cpp` PR for Grok 2 on [GitHub here](https://github.com/ggml-org/llama.cpp/pull/15539). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp && git fetch origin pull/15539/head:MASTER && git checkout MASTER && cd ..
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split llama-mtmd-cli llama-server
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endstep %}

{% step %}
If you want to use `llama.cpp` directly to load models, you can do the below: (:Q3\_K\_XL) is the quantization type. You can also download via Hugging Face (point 3). This is similar to `ollama run` . Use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location. Remember the model has only a maximum of 128K context length.

{% hint style="info" %}
Please try out `-ot ".ffn_.*_exps.=CPU"` to offload all MoE layers to the CPU! This effectively allows you to fit all non MoE layers on 1 GPU, improving generation speeds. You can customize the regex expression to fit more layers if you have more GPU capacity.

If you have a bit more GPU memory, try `-ot ".ffn_(up|down)_exps.=CPU"` This offloads up and down projection MoE layers.

Try `-ot ".ffn_(up)_exps.=CPU"` if you have even more GPU memory. This offloads only up projection MoE layers.

And finally offload all layers via `-ot ".ffn_.*_exps.=CPU"` This uses the least VRAM.

You can also customize the regex, for example `-ot "\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU"` means to offload gate, up and down MoE layers but only from the 6th layer onwards.
{% endhint %}

```bash
export LLAMA_CACHE="unsloth/grok-2-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/grok-2-GGUF:Q3_K_XL \
    --jinja \
    --n-gpu-layers 99 \
    --temp 1.0 \
    --top-p 0.95 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407 \
    -ot ".ffn_.*_exps.=CPU"
```

{% endstep %}

{% step %}
Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD-Q3_K_XL` (dynamic 3-bit quant) or other quantized versions like `Q4_K_M` . We <mark style="background-color:green;">**recommend using our 2.7bit dynamic quant**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**`UD-Q2_K_XL`**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**or above to balance size and accuracy**</mark>.

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0" # Can sometimes rate limit, so set to 0 to disable
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/grok-2-GGUF",
    local_dir = "unsloth/grok-2-GGUF",
    allow_patterns = ["*UD-Q3_K_XL*"], # Dynamic 3bit
)
```

{% endstep %}

{% step %}
You can edit `--threads 32` for the number of CPU threads, `--ctx-size 16384` for context length, `--n-gpu-layers 2` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/grok-2-GGUF/UD-Q3_K_XL/grok-2-UD-Q3_K_XL-00001-of-00003.gguf \
    --jinja \
    --threads -1 \
    --n-gpu-layers 99 \
    --temp 1.0 \
    --top-p 0.95 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407 \
    -ot ".ffn_.*_exps.=CPU"
```

{% endcode %}
{% endstep %}
{% endstepper %}

## Model uploads

**ALL our uploads** - including those that are not imatrix-based or dynamic, utilize our calibration dataset, which is specifically optimized for conversational, coding, and language tasks.

| MoE Bits | Type + Link                                                                         | Disk Size   | Details       |
| -------- | ----------------------------------------------------------------------------------- | ----------- | ------------- |
| 1.66bit  | [TQ1\_0](https://huggingface.co/unsloth/grok-2-GGUF/blob/main/grok-2-UD-TQ1_0.gguf) | **81.8 GB** | 1.92/1.56bit  |
| 1.78bit  | [IQ1\_S](https://huggingface.co/unsloth/grok-2-GGUF/tree/main/UD-IQ1_S)             | **88.9 GB** | 2.06/1.56bit  |
| 1.93bit  | [IQ1\_M](https://huggingface.co/unsloth/grok-2-GGUF/tree/main/UD-IQ1_M)             | **94.5 GB** | 2.5/2.06/1.56 |
| 2.42bit  | [IQ2\_XXS](https://huggingface.co/unsloth/grok-2-GGUF/tree/main/UD-IQ2_XXS)         | **99.3 GB** | 2.5/2.06bit   |
| 2.71bit  | [Q2\_K\_XL](https://huggingface.co/unsloth/grok-2-GGUF/tree/main/UD-Q2_K_XL)        | **112 GB**  | 3.5/2.5bit    |
| 3.12bit  | [IQ3\_XXS](https://huggingface.co/unsloth/grok-2-GGUF/tree/main/UD-IQ3_XXS)         | **117 GB**  | 3.5/2.06bit   |
| 3.5bit   | [Q3\_K\_XL](https://huggingface.co/unsloth/grok-2-GGUF/tree/main/UD-Q3_K_XL)        | **126 GB**  | 4.5/3.5bit    |
| 4.5bit   | [Q4\_K\_XL](https://huggingface.co/unsloth/grok-2-GGUF/tree/main/UD-Q4_K_XL)        | **155 GB**  | 5.5/4.5bit    |
| 5.5bit   | [Q5\_K\_XL](https://huggingface.co/unsloth/grok-2-GGUF/tree/main/UD-Q5_K_XL)        | **191 GB**  | 6.5/5.5bit    |

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
GET https://unsloth.ai/docs/models/tutorials/grok-2.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
