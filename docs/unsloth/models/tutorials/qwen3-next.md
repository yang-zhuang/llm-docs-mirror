> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/qwen3-next.md).

# Qwen3-Next: Run Locally Guide

Run Qwen3-Next-80B-A3B-Instruct and Thinking versions locally on your device!

Qwen released Qwen3-Next in Sept 2025, which are 80B MoEs with Thinking and Instruct model variants of [Qwen3](/docs/models/tutorials/qwen3-how-to-run-and-fine-tune.md). With 256K context, Qwen3-Next was designed with a brand new architecture (Hybrid of MoEs & Gated DeltaNet + Gated Attention) that specifically optimizes for fast inference on longer context lengths. Qwen3-Next has 10x faster inference than Qwen3-32B.

<a href="/docs/models/tutorials/qwen3-next.md#run-qwen3-next-tutorials" class="button secondary">Run Qwen3-Next Instruct</a><a href="/docs/models/tutorials/qwen3-next.md#thinking-qwen3-next-80b-a3b-thinking" class="button secondary">Run Qwen3-Next Thinking</a>

Qwen3-Next-80B-A3B Dynamic GGUFs: [**Instruct**](https://huggingface.co/unsloth/Qwen3-Next-80B-A3B-Instruct-GGUF) **•** [**Thinking**](https://huggingface.co/unsloth/Qwen3-Next-80B-A3B-Thinking-GGUF)

### ⚙️ Usage Guide

{% hint style="success" %}
NEW as of Dec 6, 2025: Unsloth Qwen3-Next now updated with iMatrix for improved performance.

The thinking model uses `temperature = 0.6`, but the instruct model uses `temperature = 0.7`\
The thinking model uses `top_p = 0.95`, but the instruct model uses `top_p = 0.8`
{% endhint %}

To achieve optimal performance, Qwen recommends these settings:

| Instruct:                                                                                                     | Thinking:                                                                                                     |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| <mark style="background-color:blue;">`Temperature = 0.7`</mark>                                               | <mark style="background-color:blue;">`Temperature = 0.6`</mark>                                               |
| `Min_P = 0.00` (llama.cpp's default is 0.1)                                                                   | `Min_P = 0.00` (llama.cpp's default is 0.1)                                                                   |
| `Top_P = 0.80`                                                                                                | `Top_P = 0.95`                                                                                                |
| `TopK = 20`                                                                                                   | `TopK = 20`                                                                                                   |
| `presence_penalty = 0.0 to 2.0` (llama.cpp default turns it off, but to reduce repetitions, you can use this) | `presence_penalty = 0.0 to 2.0` (llama.cpp default turns it off, but to reduce repetitions, you can use this) |

**Adequate Output Length**: Use an output length of `32,768` tokens for most queries for the thinking variant, and `16,384` for the instruct variant. You can increase the max output size for the thinking model if necessary.

Chat template for both Thinking (thinking has `<think></think>`) and Instruct is below:

```
<|im_start|>user
Hey there!<|im_end|>
<|im_start|>assistant
What is 1+1?<|im_end|>
<|im_start|>user
2<|im_end|>
<|im_start|>assistant
```

## 📖 Run Qwen3-Next Tutorials

Below are guides for the [Thinking](#thinking-qwen3-next-80b-a3b-thinking) and [Instruct](#instruct-qwen3-next-80b-a3b-instruct) versions of the model.

### Instruct: Qwen3-Next-80B-A3B-Instruct

Given that this is a non thinking model, the model does not generate `<think> </think>` blocks.

#### ⚙️Best Practices

To achieve optimal performance, Qwen recommends the following settings:

* We suggest using `temperature=0.7, top_p=0.8, top_k=20, and min_p=0.0` `presence_penalty` between 0 and 2 if the framework supports to reduce endless repetitions.
* **`temperature = 0.7`**
* `top_k = 20`
* `min_p = 0.00` (llama.cpp's default is 0.1)
* **`top_p = 0.80`**
* `presence_penalty = 0.0 to 2.0` (llama.cpp default turns it off, but to reduce repetitions, you can use this) Try 1.0 for example.
* Supports up to `262,144` context natively but you can set it to `32,768` tokens for less RAM use

#### :sparkles: Llama.cpp: Run Qwen3-Next-80B-A3B-Instruct Tutorial

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

2. You can directly pull from HuggingFace via:

   ```bash
   ./llama.cpp/llama-cli \
       -hf unsloth/Qwen3-Next-80B-A3B-Instruct-GGUF:Q4_K_XL \
       --jinja -ngl 99 --ctx-size 32768 \
       --temp 0.7 --min-p 0.0 --top-p 0.80 --top-k 20 --presence-penalty 1.0
   ```
3. Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD_Q4_K_XL` or other quantized versions.

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Qwen3-Next-80B-A3B-Instruct-GGUF",
    local_dir = "Qwen3-Next-80B-A3B-Instruct-GGUF",
    allow_patterns = ["*UD-Q4_K_XL*"],
)
```

### Thinking: Qwen3-Next-80B-A3B-Thinking

This model supports only thinking mode and a 256K context window natively. The default chat template adds `<think>` automatically, so you may see only a closing `</think>` tag in the output.

#### ⚙️Best Practices

To achieve optimal performance, Qwen recommends the following settings:

* We suggest using `temperature=0.6, top_p=0.95, top_k=20, and min_p=0.0` `presence_penalty` between 0 and 2 if the framework supports to reduce endless repetitions.
* **`temperature = 0.6`**
* `top_k = 20`
* `min_p = 0.00` (llama.cpp's default is 0.1)
* **`top_p = 0.95`**
* `presence_penalty = 0.0 to 2.0` (llama.cpp default turns it off, but to reduce repetitions, you can use this) Try 1.0 for example.
* Supports up to `262,144` context natively but you can set it to `32,768` tokens for less RAM use

#### :sparkles: Llama.cpp: Run Qwen3-Next-80B-A3B-Thinking Tutorial

1. Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

2. You can directly pull from Hugging Face via:

   ```bash
   ./llama.cpp/llama-cli \
       -hf unsloth/Qwen3-Next-80B-A3B-Thinking-GGUF:Q4_K_XL \
       --jinja -ngl 99 --ctx-size 32768 \
       --temp 0.6 --min-p 0.0 --top-p 0.95 --top-k 20 --presence-penalty 1.0
   ```
3. Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD_Q4_K_XL` or other quantized versions.

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Qwen3-Next-80B-A3B-Thinking-GGUF",
    local_dir = "Qwen3-Next-80B-A3B-Thinking-GGUF",
    allow_patterns = ["*UD-Q4_K_XL*"],
)
```

### 🛠️ Improving generation speed <a href="#improving-generation-speed" id="improving-generation-speed"></a>

If you have more VRAM, you can try offloading more MoE layers, or offloading whole layers themselves.

Normally, `-ot ".ffn_.*_exps.=CPU"` offloads all MoE layers to the CPU! This effectively allows you to fit all non MoE layers on 1 GPU, improving generation speeds. You can customize the regex expression to fit more layers if you have more GPU capacity.

If you have a bit more GPU memory, try `-ot ".ffn_(up|down)_exps.=CPU"` This offloads up and down projection MoE layers.

Try `-ot ".ffn_(up)_exps.=CPU"` if you have even more GPU memory. This offloads only up projection MoE layers.

You can also customize the regex, for example `-ot "\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU"` means to offload gate, up and down MoE layers but only from the 6th layer onwards.

The [latest llama.cpp release](https://github.com/ggml-org/llama.cpp/pull/14363) also introduces high throughput mode. Use `llama-parallel`. Read more about it [here](https://github.com/ggml-org/llama.cpp/tree/master/examples/parallel). You can also **quantize the KV cache to 4bits** for example to reduce VRAM / RAM movement, which can also make the generation process faster. The [next section](#how-to-fit-long-context-256k-to-1m) talks about KV cache quantization.

### 📐How to fit long context <a href="#how-to-fit-long-context-256k-to-1m" id="how-to-fit-long-context-256k-to-1m"></a>

To fit longer context, you can use **KV cache quantization** to quantize the K and V caches to lower bits. This can also increase generation speed due to reduced RAM / VRAM data movement. The allowed options for K quantization (default is `f16`) include the below.

`--cache-type-k f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1`

You should use the `_1` variants for somewhat increased accuracy, albeit it's slightly slower. For eg `q4_1, q5_1` So try out `--cache-type-k q4_1`

You can also quantize the V cache, but you will need to **compile llama.cpp with Flash Attention** support via `-DGGML_CUDA_FA_ALL_QUANTS=ON`, and use `--flash-attn` to enable it. After installing Flash Attention, you can then use `--cache-type-v q4_1`

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-be34c101c627020c7a6cfb6cd249f2462587d235%2Fqwen33%20mascot.png?alt=media" alt=""><figcaption></figcaption></figure>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/qwen3-next.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
