> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/kimi-k2-thinking-how-to-run-locally.md).

# Kimi K2 Thinking: Run Locally Guide

Guide on running Kimi-K2-Thinking and Kimi-K2 on your own local device!

{% hint style="success" %}
Kimi-K2-Thinking got released. Read our [Thinking guide](#kimi-k2-thinking-guide) or access [GGUFs here](https://huggingface.co/unsloth/Kimi-K2-Thinking-GGUF).

We also collaborated with the Kimi team on [**system prompt fix**](#tokenizer-quirks-and-bug-fixes) for Kimi-K2-Thinking.
{% endhint %}

Kimi-K2 and **Kimi-K2-Thinking** achieve SOTA performance in knowledge, reasoning, coding, and agentic tasks. The full 1T parameter models from Moonshot AI requires 1.09TB of disk space, while the quantized **Unsloth Dynamic 1.8-bit** version reduces this to just 230GB (-80% size)**:** [**Kimi-K2-GGUF**](https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF)

You can also now run our [**Kimi-K2-Thinking** GGUFs](https://huggingface.co/unsloth/Kimi-K2-Thinking-GGUF).

All uploads use Unsloth [Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) for SOTA [Aider Polyglot](/docs/basics/dynamic-3.0-ggufs/unsloth-dynamic-ggufs-on-aider-polyglot.md) and 5-shot MMLU performance. See how our Dynamic 1–2 bit GGUFs perform on [coding benchmarks here](/docs/basics/dynamic-3.0-ggufs/unsloth-dynamic-ggufs-on-aider-polyglot.md).

<a href="#kimi-k2-thinking-guide" class="button primary">Run Thinking</a><a href="#kimi-k2-instruct-guide" class="button primary">Run Instruct</a>

### :gear: Recommended Requirements

{% hint style="info" %}
You need **247GB of disk space** to run the 1bit quant!

The only requirement is **`disk space + RAM + VRAM ≥ 247GB`**. That means you do not need to have that much RAM or VRAM (GPU) to run the model, but it will be much slower.
{% endhint %}

The 1.8-bit (UD-TQ1\_0) quant will fit in a 1x 24GB GPU (with all MoE layers offloaded to system RAM or a fast disk). Expect around \~1-2 tokens/s with this setup if you have bonus 256GB RAM as well. The full Kimi K2 Q8 quant is 1.09TB in size and will need at least 8 x H200 GPUs.

For optimal performance you will need at least **247GB unified memory or 247GB combined RAM+VRAM** for 5+ tokens/s. If you have less than 247GB combined RAM+VRAM, then the speed of the model will definitely take a hit.

**If you do not have 247GB of RAM+VRAM, no worries!** llama.cpp inherently has **disk offloading**, so through mmaping, it'll still work, just be slower - for example before you might get 5 to 10 tokens / second, now it's under 1 token.

We suggest using our **UD-Q2\_K\_XL (360GB)** quant to balance size and accuracy!

{% hint style="success" %}
For the best performance, have your VRAM + RAM combined = the size of the quant you're downloading. If not, it'll still work via disk offloading, just it'll be slower!
{% endhint %}

## 💭Kimi-K2-Thinking Guide

Kimi-K2-Thinking should generally follow the same instructions as the Instruct model, with a few key differences, particularly in areas such as settings and the chat template.

{% hint style="success" %}
**To run the model in full precision, you only need to use the 4-bit or 5-bit Dynamic GGUFs (e.g. UD\_Q4\_K\_XL) because the model was originally released in INT4 format.**

You can choose a higher-bit quantization just to be safe in case of small quantization differences, but in most cases this is unnecessary.
{% endhint %}

### 🌙 Official Recommended Settings:

According to [Moonshot AI](https://huggingface.co/moonshotai/Kimi-K2-Thinking), these are the recommended settings for Kimi-K2-Thinking inference:

* Set the <mark style="background-color:green;">**temperature 1.0**</mark> to reduce repetition and incoherence.
* Suggested context length = 98,304 (up to 256K)
* Note: Using different tools may require different settings

{% hint style="info" %}
We recommend setting <mark style="background-color:green;">**min\_p to 0.01**</mark> to suppress the occurrence of unlikely tokens with low probabilities.
{% endhint %}

For example given a user message of "What is 1+1?", we get:

{% code overflow="wrap" %}

```
<|im_system|>system<|im_middle|>You are Kimi, an AI assistant created by Moonshot AI.<|im_end|><|im_user|>user<|im_middle|>What is 1+1?<|im_end|><|im_assistant|>assistant<|im_middle|>
```

{% endcode %}

### ✨ Run Kimi K2 Thinking in llama.cpp

{% hint style="success" %}
You can now use the latest update of [llama.cpp](https://github.com/ggml-org/llama.cpp) to run the model:
{% endhint %}

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

2. If you want to use `llama.cpp` directly to load models, you can do the below: (:UD-TQ1\_0) is the quantization type. You can also download via Hugging Face (point 3). This is similar to `ollama run` . Use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location.

```bash
export LLAMA_CACHE="unsloth/Kimi-K2-Thinking-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/Kimi-K2-Thinking-GGUF:UD-TQ1_0 \
    --n-gpu-layers 99 \
    --temp 1.0 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407 \
    -ot ".ffn_.*_exps.=CPU"
```

3. The above will use around 8GB of GPU memory. If you have around 360GB of combined GPU memory, remove `-ot ".ffn_.*_exps.=CPU"` to get maximum speed!

{% hint style="info" %}
Please try out `-ot ".ffn_.*_exps.=CPU"` to offload all MoE layers to the CPU! This effectively allows you to fit all non MoE layers on 1 GPU, improving generation speeds. You can customize the regex expression to fit more layers if you have more GPU capacity.

If you have a bit more GPU memory, try `-ot ".ffn_(up|down)_exps.=CPU"` This offloads up and down projection MoE layers.

Try `-ot ".ffn_(up)_exps.=CPU"` if you have even more GPU memory. This offloads only up projection MoE layers.

And finally offload all layers via `-ot ".ffn_.*_exps.=CPU"` This uses the least VRAM.

You can also customize the regex, for example `-ot "\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU"` means to offload gate, up and down MoE layers but only from the 6th layer onwards.
{% endhint %}

3. Download the model via (after installing `pip install huggingface_hub hf_transfer` ). We recommend using our 2bit dynamic quant UD-Q2\_K\_XL to balance size and accuracy. All versions at: [huggingface.co/unsloth/Kimi-K2-Thinking-GGUF](https://huggingface.co/unsloth/Kimi-K2-Thinking-GGUF)

{% code overflow="wrap" %}

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0" # Can sometimes rate limit, so set to 0 to disable
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Kimi-K2-Thinking-GGUF",
    local_dir = "unsloth/Kimi-K2-Thinking-GGUF",
    allow_patterns = ["*UD-TQ1_0*"], # Use "*UD-Q2_K_XL*" for Dynamic 2bit (381GB)
)
```

{% endcode %}

{% hint style="info" %}
If you find that downloads get stuck at 90 to 95% or so, please see <https://docs.unsloth.ai/basics/troubleshooting-and-faqs#downloading-gets-stuck-at-90-to-95>
{% endhint %}

4. Run any prompt.
5. Edit `--threads -1` for the number of CPU threads (be default it's set to the maximum CPU threads), `--ctx-size 16384` for context length, `--n-gpu-layers 99` for GPU offloading on how many layers. Set it to 99 combined with MoE CPU offloading to get the best performance. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/Kimi-K2-Thinking-GGUF/UD-TQ1_0/Kimi-K2-Thinking-UD-TQ1_0-00001-of-00006.gguf \
    --n-gpu-layers 99 \
    --temp 1.0 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407 \
    -ot ".ffn_.*_exps.=CPU"
```

{% endcode %}

### :thinking:**No Thinking Tags?**

You may notice that there are no *thinking* tags when you run the model. This is normal and intended behavior.

In your `llama.cpp` script, make sure to include the `--special` flag at the very end of your command. Once you do, you’ll see the `<think>` token appear as expected.

You might also see every answer end with `<|im_end|>`. This is normal as `<|im_end|>` is a special token that appears when printing special tokens. If you’d like to hide it, you can set `<|im_end|>` as a stop string in your settings.

### ✨ Deploy with llama-server and OpenAI's completion library

After installing llama.cpp as per [#run-kimi-k2-thinking-in-llama.cpp](#run-kimi-k2-thinking-in-llama.cpp "mention"), you can use the below to launch an OpenAI compatible server:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-server \
    --model unsloth/Kimi-K2-Thinking-GGUF/UD-TQ1_0/Kimi-K2-Thinking-UD-TQ1_0-00001-of-00006.gguf \
    --alias "unsloth/Kimi-K2-Thinking" \
    -fa on \
    --n-gpu-layers 999 \
    -ot ".ffn_.*_exps.=CPU" \
    --min-p 0.01 \
    --ctx-size 16384 \
    --port 8001 \
    --jinja
```

{% endcode %}

Then use OpenAI's Python library after `pip install openai` :

```python
from openai import OpenAI
openai_client = OpenAI(
    base_url = "http://127.0.0.1:8001/v1",
    api_key = "sk-no-key-required",
)
completion = openai_client.chat.completions.create(
    model = "unsloth/Kimi-K2-Thinking",
    messages = [{"role": "user", "content": "What is 2+2?"},],
)
print(completion.choices[0].message.content)
```

## :mag:Tokenizer quirks and bug fixes

**7th November 2025: We notified the Kimi team, and fixed the default system prompt of** `You are Kimi, an AI assistant created by Moonshot AI.` **not appearing on the first user prompt!** See <https://huggingface.co/moonshotai/Kimi-K2-Thinking/discussions/12>

Huge thanks to the Moonshot Kimi team for their extremely fast response time to our queries and fixing the issue ASAP!

**16th July 2025: Kimi K2 updated their tokenizer to enable multiple tool calls** as per <https://x.com/Kimi_Moonshot/status/1945050874067476962>

**18th July 2025: We fixed a system prompt - Kimi tweeted about our fix as well here:** <https://x.com/Kimi_Moonshot/status/1946130043446690030>. The fix was described here as well: <https://huggingface.co/moonshotai/Kimi-K2-Instruct/discussions/28>

If you have the old checkpoints downloaded - now worries - simply download the first GGUF split which was changed. OR if you do not want to download any new files do:

```bash
wget https://huggingface.co/unsloth/Kimi-K2-Instruct/raw/main/chat_template.jinja
./llama.cpp ... --chat-template-file /dir/to/chat_template.jinja
```

The Kimi K2 tokenizer was interesting to play around with - <mark style="background-color:green;">**it's mostly similar in action to GPT-4o's tokenizer**</mark>! We first see in the [tokenization\_kimi.py](https://huggingface.co/moonshotai/Kimi-K2-Instruct/blob/main/tokenization_kimi.py) file the following regular expression (regex) that Kimi K2 uses:

```python
pat_str = "|".join(
    [
        r"""[\p{Han}]+""",
        r"""[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}&&[^\p{Han}]]*[\p{Ll}\p{Lm}\p{Lo}\p{M}&&[^\p{Han}]]+(?i:'s|'t|'re|'ve|'m|'ll|'d)?""",
        r"""[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}&&[^\p{Han}]]+[\p{Ll}\p{Lm}\p{Lo}\p{M}&&[^\p{Han}]]*(?i:'s|'t|'re|'ve|'m|'ll|'d)?""",
        r"""\p{N}{1,3}""",
        r""" ?[^\s\p{L}\p{N}]+[\r\n]*""",
        r"""\s*[\r\n]+""",
        r"""\s+(?!\S)""",
        r"""\s+""",
    ]
)
```

After careful inspection, we find Kimi K2 is nearly identical to GPT-4o's tokenizer regex which can be found in [llama.cpp's source code](https://github.com/ggml-org/llama.cpp/blob/55c509daf51d25bfaee9c8b8ce6abff103d4473b/src/llama-vocab.cpp#L400).

{% code overflow="wrap" %}

```
[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]*[\p{Ll}\p{Lm}\p{Lo}\p{M}]+(?i:'s|'t|'re|'ve|'m|'ll|'d)?|[^\r\n\p{L}\p{N}]?[\p{Lu}\p{Lt}\p{Lm}\p{Lo}\p{M}]+[\p{Ll}\p{Lm}\p{Lo}\p{M}]*(?i:'s|'t|'re|'ve|'m|'ll|'d)?|\p{N}{1,3}| ?[^\s\p{L}\p{N}]+[\r\n/]*|\s*[\r\n]+|\s+(?!\S)|\s+
```

{% endcode %}

Both tokenize numbers into groups of 1 to 3 numbers (9, 99, 999), and use similar patterns. The only difference looks to be the handling of "Han" or Chinese characters, which Kimi's tokenizer deals with more. [The PR](https://github.com/ggml-org/llama.cpp/pull/14654) by <https://github.com/gabriellarson> handles these differences well after some [discussions here](https://github.com/ggml-org/llama.cpp/issues/14642#issuecomment-3067324745).

<mark style="background-color:green;">**We also find the correct EOS token should not be \[EOS], but rather <|im\_end|>, which we have also fixed in our model conversions.**</mark>

## 🌝Kimi-K2-Instruct Guide

Step-by-step guide on running the Instruct Kimi K2 models including Kimi K2 0905 - the September 5 update.

### 🌙 Official Recommended Settings:

According to [Moonshot AI](https://huggingface.co/moonshotai/Kimi-K2-Instruct), these are the recommended settings for Kimi K2 inference:

* Set the <mark style="background-color:green;">**temperature 0.6**</mark> to reduce repetition and incoherence.
* Original default system prompt is:

  ```
  You are a helpful assistant
  ```
* (Optional) Moonshot also suggests the below for the system prompt:

  ```
  You are Kimi, an AI assistant created by Moonshot AI.
  ```

{% hint style="success" %}
We recommend setting <mark style="background-color:green;">**min\_p to 0.01**</mark> to suppress the occurrence of unlikely tokens with low probabilities.
{% endhint %}

### :1234: Chat template and prompt format

Kimi Chat does use a BOS (beginning of sentence token). The system, user and assistant roles are all enclosed with `<|im_middle|>` which is interesting, and each get their own respective token `<|im_system|>, <|im_user|>, <|im_assistant|>`.

{% code overflow="wrap" %}

```python
<|im_system|>system<|im_middle|>You are a helpful assistant<|im_end|><|im_user|>user<|im_middle|>What is 1+1?<|im_end|><|im_assistant|>assistant<|im_middle|>2<|im_end|>
```

{% endcode %}

To separate the conversational boundaries (you must remove each new line), we get:

{% code overflow="wrap" %}

```
<|im_system|>system<|im_middle|>You are a helpful assistant<|im_end|>
<|im_user|>user<|im_middle|>What is 1+1?<|im_end|>
<|im_assistant|>assistant<|im_middle|>2<|im_end|>
```

{% endcode %}

### :floppy\_disk: Model uploads

**ALL our uploads** - including those that are not imatrix-based or dynamic, utilize our calibration dataset, which is specifically optimized for conversational, coding, and reasoning tasks.

<table data-full-width="false"><thead><tr><th>MoE Bits</th><th>Type + Link</th><th>Disk Size</th><th>Details</th></tr></thead><tbody><tr><td>1.66bit</td><td><a href="https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF/tree/main/UD-TQ1_0">UD-TQ1_0</a></td><td><strong>245GB</strong></td><td>1.92/1.56bit</td></tr><tr><td>1.78bit</td><td><a href="https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF/tree/main/UD-IQ1_S">UD-IQ1_S</a></td><td><strong>281GB</strong></td><td>2.06/1.56bit</td></tr><tr><td>1.93bit</td><td><a href="https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF/tree/main/UD-IQ1_M">UD-IQ1_M</a></td><td><strong>304GB</strong></td><td>2.5/2.06/1.56</td></tr><tr><td>2.42bit</td><td><a href="https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF/tree/main/UD-IQ2_XXS">UD-IQ2_XXS</a></td><td><strong>343GB</strong></td><td>2.5/2.06bit</td></tr><tr><td>2.71bit</td><td><a href="https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF/tree/main/UD-Q2_K_XL">UD-Q2_K_XL</a></td><td><strong>381GB</strong></td><td>3.5/2.5bit</td></tr><tr><td>3.12bit</td><td><a href="https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF/tree/main/UD-IQ3_XXS">UD-IQ3_XXS</a></td><td><strong>417GB</strong></td><td>3.5/2.06bit</td></tr><tr><td>3.5bit</td><td><a href="https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF/tree/main/UD-Q3_K_XL">UD-Q3_K_XL</a></td><td><strong>452GB</strong></td><td>4.5/3.5bit</td></tr><tr><td>4.5bit</td><td><a href="https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF/tree/main/UD-Q4_K_XL">UD-Q4_K_XL</a></td><td><strong>588GB</strong></td><td>5.5/4.5bit</td></tr><tr><td>5.5bit</td><td><a href="https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF/tree/main/UD-Q5_K_XL">UD-Q5_K_XL</a></td><td><strong>732GB</strong></td><td>6.5/5.5bit</td></tr></tbody></table>

We've also uploaded versions in [BF16 format](https://huggingface.co/unsloth/Kimi-K2-Instruct-BF16).

### ✨ Run Instruct in llama.cpp

1. Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split llama-mtmd-cli
cp llama.cpp/build/bin/llama-* llama.cpp
```

2. If you want to use `llama.cpp` directly to load models, you can do the below: (:UD-IQ1\_S) is the quantization type. You can also download via Hugging Face (point 3). This is similar to `ollama run` . Use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location.\ <mark style="background-color:green;">**To run the new September 2025 update for the model, change the model name from 'Kimi-K2-Instruct' to 'Kimi-K2-Instruct-0905'.**</mark>

{% hint style="info" %}
Please try out `-ot ".ffn_.*_exps.=CPU"` to offload all MoE layers to the CPU! This effectively allows you to fit all non MoE layers on 1 GPU, improving generation speeds. You can customize the regex expression to fit more layers if you have more GPU capacity.

If you have a bit more GPU memory, try `-ot ".ffn_(up|down)_exps.=CPU"` This offloads up and down projection MoE layers.

Try `-ot ".ffn_(up)_exps.=CPU"` if you have even more GPU memory. This offloads only up projection MoE layers.

And finally offload all layers via `-ot ".ffn_.*_exps.=CPU"` This uses the least VRAM.

You can also customize the regex, for example `-ot "\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU"` means to offload gate, up and down MoE layers but only from the 6th layer onwards.
{% endhint %}

```bash
export LLAMA_CACHE="unsloth/Kimi-K2-Instruct-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/Kimi-K2-Instruct-GGUF:TQ1_0 \
    --n-gpu-layers 99 \
    --temp 0.6 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407 \
    -ot ".ffn_.*_exps.=CPU"
```

3. Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD-TQ1_0`(dynamic 1.8bit quant) or other quantized versions like `Q2_K_XL` . We <mark style="background-color:green;">**recommend using our 2bit dynamic quant**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**`UD-Q2_K_XL`**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**to balance size and accuracy**</mark>. More versions at: [huggingface.co/unsloth/Kimi-K2-Instruct-GGUF](https://huggingface.co/unsloth/Kimi-K2-Instruct-GGUF)

{% code overflow="wrap" %}

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "0" # Can sometimes rate limit, so set to 0 to disable
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Kimi-K2-Instruct-GGUF",
    local_dir = "unsloth/Kimi-K2-Instruct-GGUF",
    allow_patterns = ["*UD-TQ1_0*"], # Dynamic 1bit (281GB) Use "*UD-Q2_K_XL*" for Dynamic 2bit (381GB)
)
```

{% endcode %}

{% hint style="info" %}
If you find that downloads get stuck at 90 to 95% or so, please see <https://docs.unsloth.ai/basics/troubleshooting-and-faqs#downloading-gets-stuck-at-90-to-95>
{% endhint %}

4. Run any prompt.
5. Edit `--threads -1` for the number of CPU threads (be default it's set to the maximum CPU threads), `--ctx-size 16384` for context length, `--n-gpu-layers 99` for GPU offloading on how many layers. Set it to 99 combined with MoE CPU offloading to get the best performance. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/Kimi-K2-Instruct-GGUF/UD-TQ1_0/Kimi-K2-Instruct-UD-TQ1_0-00001-of-00005.gguf \
    --n-gpu-layers 99 \
    --temp 0.6 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407 \
    -ot ".ffn_.*_exps.=CPU"
```

{% endcode %}

### :bird: Flappy Bird + other tests <a href="#heptagon-test" id="heptagon-test"></a>

We introduced the Flappy Bird test when our 1.58bit quants for DeepSeek R1 were provided. We found Kimi K2 one of the only models to one-shot all our tasks including this one, [Heptagon ](/docs/models/tutorials/deepseek-r1-0528-how-to-run-locally.md#heptagon-test)and others tests even at 2-bit. The goal is to ask the LLM to create a Flappy Bird game but following some specific instructions:

{% code overflow="wrap" %}

```
Create a Flappy Bird game in Python. You must include these things:
1. You must use pygame.
2. The background color should be randomly chosen and is a light shade. Start with a light blue color.
3. Pressing SPACE multiple times will accelerate the bird.
4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.
5. Place on the bottom some land colored as dark brown or yellow chosen randomly.
6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.
7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.
8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.
The final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.
```

{% endcode %}

You can also test the dynamic quants via the Heptagon Test as per [r/Localllama](https://www.reddit.com/r/LocalLLaMA/comments/1j7r47l/i_just_made_an_animation_of_a_ball_bouncing/) which tests the model on creating a basic physics engine to simulate balls rotating in a moving enclosed heptagon shape.

<figure><img src="https://docs.unsloth.ai/~gitbook/image?url=https%3A%2F%2F3215535692-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FxhOjnexMCB3dmuQFQ2Zq%252Fuploads%252F2O72oTw5yPUbcxXjDNKS%252Fsnapshot.jpg%3Falt%3Dmedia%26token%3Dce852f9f-20ee-4b93-9d7b-1a5f211b9e04&#x26;width=768&#x26;dpr=4&#x26;quality=100&#x26;sign=55d1134d&#x26;sv=2" alt="" width="563"><figcaption></figcaption></figure>

The goal is to make the heptagon spin, and the balls in the heptagon should move. The prompt is below:

{% code overflow="wrap" %}

```
Write a Python program that shows 20 balls bouncing inside a spinning heptagon:\n- All balls have the same radius.\n- All balls have a number on it from 1 to 20.\n- All balls drop from the heptagon center when starting.\n- Colors are: #f8b862, #f6ad49, #f39800, #f08300, #ec6d51, #ee7948, #ed6d3d, #ec6800, #ec6800, #ee7800, #eb6238, #ea5506, #ea5506, #eb6101, #e49e61, #e45e32, #e17b34, #dd7a56, #db8449, #d66a35\n- The balls should be affected by gravity and friction, and they must bounce off the rotating walls realistically. There should also be collisions between balls.\n- The material of all the balls determines that their impact bounce height will not exceed the radius of the heptagon, but higher than ball radius.\n- All balls rotate with friction, the numbers on the ball can be used to indicate the spin of the ball.\n- The heptagon is spinning around its center, and the speed of spinning is 360 degrees per 5 seconds.\n- The heptagon size should be large enough to contain all the balls.\n- Do not use the pygame library; implement collision detection algorithms and collision response etc. by yourself. The following Python libraries are allowed: tkinter, math, numpy, dataclasses, typing, sys.\n- All codes should be put in a single Python file.
```

{% endcode %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/kimi-k2-thinking-how-to-run-locally.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
