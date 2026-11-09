> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/cogito-v2-how-to-run-locally.md).

# Cogito v2.1: How to Run Locally

Cogito v2.1 LLMs are one of the strongest open models in the world trained with IDA. Also v1 comes in 4 sizes: 70B, 109B, 405B and 671B, allowing you to select which size best matches your hardware.

{% hint style="success" %}
Deep Cogito v2.1 is an updated 671B MoE that is the most powerful open weights model as of 19 November 2025.
{% endhint %}

Cogito v2.1 comes in 1 671B MoE size, whilst Cogito v2 Preview is [Deep Cogito](https://www.deepcogito.com/)'s release of models spans 4 model sizes ranging from 70B to 671B. By using **IDA (Iterated Distillation & Amplification)**, these models are trained with the model internalizing the reasoning process using iterative policy improvement, rather than simply searching longer at inference time (like DeepSeek R1).

Deep Cogito is based in [San Fransisco, USA](https://techcrunch.com/2025/04/08/deep-cogito-emerges-from-stealth-with-hybrid-ai-reasoning-models/) (like Unsloth :flag\_us:) and we're excited to provide quantized dynamic models for all 4 model sizes! All uploads use Unsloth [Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) for SOTA 5-shot MMLU and KL Divergence performance, meaning you can run & fine-tune quantized these LLMs with minimal accuracy loss!

**Tutorials navigation:**

<a href="https://docs.unsloth.ai/basics/tutorials-how-to-fine-tune-and-run-llms/cogito-v2-how-to-run-locally#run-cogito-671b-moe-in-llama.cpp" class="button secondary">Run 671B MoE</a><a href="https://docs.unsloth.ai/basics/tutorials-how-to-fine-tune-and-run-llms/cogito-v2-how-to-run-locally#run-cogito-109b-moe-in-llama.cpp" class="button secondary">Run 109B MoE</a><a href="https://docs.unsloth.ai/basics/tutorials-how-to-fine-tune-and-run-llms/cogito-v2-how-to-run-locally#run-cogito-405b-dense-in-llama.cpp" class="button secondary">Run 405B Dense</a><a href="https://docs.unsloth.ai/basics/tutorials-how-to-fine-tune-and-run-llms/cogito-v2-how-to-run-locally#run-cogito-70b-dense-in-llama.cpp" class="button secondary">Run 70B Dense</a>

{% hint style="success" %}
Choose which model size fits your hardware! We upload 1.58bit to 16bit variants for all 4 model sizes!
{% endhint %}

## :gem: Model Sizes and Uploads

There are 4 model sizes:

1. 2 Dense models based off from Llama - 70B and 405B
2. 2 MoE models based off from Llama 4 Scout (109B) and DeepSeek R1 (671B)

<table data-full-width="false"><thead><tr><th>Model Sizes</th><th width="256.9999694824219">Recommended Quant &#x26; Link</th><th>Disk Size</th><th>Architecture</th></tr></thead><tbody><tr><td>70B Dense</td><td><a href="https://huggingface.co/unsloth/cogito-v2-preview-llama-70B-GGUF">UD-Q4_K_XL</a></td><td><strong>44GB</strong></td><td>Llama 3 70B</td></tr><tr><td>109B MoE</td><td><a href="https://huggingface.co/unsloth/cogito-v2-preview-llama-109B-MoE-GGUF">UD-Q3_K_XL</a></td><td><strong>50GB</strong></td><td>Llama 4 Scout</td></tr><tr><td>405B Dense</td><td><a href="https://huggingface.co/unsloth/cogito-v2-preview-llama-405B-GGUF">UD-Q2_K_XL</a></td><td><strong>152GB</strong></td><td>Llama 3 405B</td></tr><tr><td>671B MoE</td><td><a href="https://huggingface.co/unsloth/cogito-v2-preview-deepseek-671B-MoE-GGUF">UD-Q2_K_XL</a></td><td><strong>251GB</strong></td><td>DeepSeek R1</td></tr></tbody></table>

{% hint style="success" %}
Though not necessary, for the best performance, have your VRAM + RAM combined = to the size of the quant you're downloading. If you have less VRAM + RAM, then the quant will still function, just be much slower.
{% endhint %}

## 🐳 Run Cogito 671B MoE in llama.cpp

1. Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

{% code overflow="wrap" %}

```shellscript
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split llama-mtmd-cli
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endcode %}

2. If you want to use `llama.cpp` directly to load models, you can do the below: (:IQ1\_S) is the quantization type. You can also download via Hugging Face (point 3). This is similar to `ollama run` . Use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location.

{% hint style="success" %}
Please try out `-ot ".ffn_.*_exps.=CPU"` to offload all MoE layers to the CPU! This effectively allows you to fit all non MoE layers on 1 GPU, improving generation speeds. You can customize the regex expression to fit more layers if you have more GPU capacity.

If you have a bit more GPU memory, try `-ot ".ffn_(up|down)_exps.=CPU"` This offloads up and down projection MoE layers.

Try `-ot ".ffn_(up)_exps.=CPU"` if you have even more GPU memory. This offloads only up projection MoE layers.

And finally offload all layers via `-ot ".ffn_.*_exps.=CPU"` This uses the least VRAM.

You can also customize the regex, for example `-ot "\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU"` means to offload gate, up and down MoE layers but only from the 6th layer onwards.
{% endhint %}

```shellscript
export LLAMA_CACHE="unsloth/cogito-671b-v2.1-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/cogito-671b-v2.1-GGUF:UD-Q2_K_XL \
    --n-gpu-layers 99 \
    --temp 0.6 \
    --top-p 0.95 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407 \
    --jinja \
    -ot ".ffn_.*_exps.=CPU"
```

3. Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD-IQ1_S`(dynamic 1.78bit quant) or other quantized versions like `Q4_K_M` . We <mark style="background-color:green;">**recommend using our 2.7bit dynamic quant**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**`UD-Q2_K_XL`**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**to balance size and accuracy**</mark>. More versions at: <https://huggingface.co/unsloth/cogito-671b-v2.1-GGUF>

{% code overflow="wrap" %}

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0" # Can sometimes rate limit, so set to 0 to disable
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/cogito-671b-v2.1-GGUF",
    local_dir = "unsloth/cogito-671b-v2.1-GGUF",
    allow_patterns = ["*UD-IQ1_S*"], # Dynamic 1bit (168GB) Use "*UD-Q2_K_XL*" for Dynamic 2bit (251GB)
)
```

{% endcode %}

4. Edit `--threads 32` for the number of CPU threads, `--ctx-size 16384` for context length, `--n-gpu-layers 2` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.

## :mouse\_three\_button:Run Cogito 109B MoE in llama.cpp

1. Follow the same instructions as running the [671B model above](#run-cogito-671b-moe-in-llama.cpp).
2. Then run the below:

```shellscript
export LLAMA_CACHE="unsloth/cogito-v2-preview-llama-109B-MoE-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/cogito-v2-preview-llama-109B-MoE-GGUF:Q3_K_XL \
    --n-gpu-layers 99 \
    --temp 0.6 \
    --min-p 0.01 \
    --top-p 0.9 \
    --ctx-size 16384 \
    --jinja \
    -ot ".ffn_.*_exps.=CPU"
```

## :deciduous\_tree:Run Cogito 405B Dense in llama.cpp

1. Follow the same instructions as running the [671B model above](#run-cogito-671b-moe-in-llama.cpp).
2. Then run the below:

```shellscript
export LLAMA_CACHE="unsloth/cogito-v2-preview-llama-405B-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/cogito-v2-preview-llama-405B-GGUF:Q2_K_XL \
    --n-gpu-layers 99 \
    --temp 0.6 \
    --min-p 0.01 \
    --top-p 0.9 \
    --jinja \
    --ctx-size 16384
```

## :sunglasses: Run Cogito 70B Dense in llama.cpp

1. Follow the same instructions as running the [671B model above](#run-cogito-671b-moe-in-llama.cpp).
2. Then run the below:

```shellscript
export LLAMA_CACHE="unsloth/cogito-v2-preview-llama-70B-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/cogito-v2-preview-llama-70B-GGUF:Q4_K_XL \
    --n-gpu-layers 99 \
    --temp 0.6 \
    --min-p 0.01 \
    --top-p 0.9 \
    --jinja \
    --ctx-size 16384
```

See <https://www.deepcogito.com/research/cogito-v2-1> for more details


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/cogito-v2-how-to-run-locally.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
