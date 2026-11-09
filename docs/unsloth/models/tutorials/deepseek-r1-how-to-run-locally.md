> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/deepseek-r1-how-to-run-locally.md).

# DeepSeek-R1: How to Run Locally

A guide on how you can run our 1.58-bit Dynamic Quants for DeepSeek-R1 using llama.cpp.

{% hint style="success" %}
Please see <https://docs.unsloth.ai/basics/deepseek-r1-0528-how-to-run-locally> for an updated DeepSeek R1-0528 (May 28th 2025 version)
{% endhint %}

## Using llama.cpp (recommended)

1. Do not forget about `<｜User｜>` and `<｜Assistant｜>` tokens! - Or use a chat template formatter
2. Obtain the latest `llama.cpp` at: [github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=ON -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

3. It's best to use `--min-p 0.05` to counteract very rare token predictions - I found this to work well especially for the 1.58bit model.
4. Download the model via:

```python
# pip install huggingface_hub hf_transfer
# import os # Optional for faster downloading
# os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

from huggingface_hub import snapshot_download
snapshot_download(
  repo_id = "unsloth/DeepSeek-R1-GGUF",
  local_dir = "DeepSeek-R1-GGUF",
  allow_patterns = ["*UD-IQ1_S*"], # Select quant type UD-IQ1_S for 1.58bit
)
```

6. Example with Q4\_0 K quantized cache **Notice -no-cnv disables auto conversation mode**

```bash
./llama.cpp/llama-cli \
    --model DeepSeek-R1-GGUF/DeepSeek-R1-UD-IQ1_S/DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf \
    --cache-type-k q4_0 \
    -no-cnv --prio 2 \
    --temp 0.6 \
    --ctx-size 8192 \
    --seed 3407 \
    --prompt "<｜User｜>What is 1+1?<｜Assistant｜>"
```

Example output:

```txt
 <think>
 Okay, so I need to figure out what 1 plus 1 is. Hmm, where do I even start? I remember from school that adding numbers is pretty basic, but I want to make sure I understand it properly.
 Let me think, 1 plus 1. So, I have one item and I add another one. Maybe like a apple plus another apple. If I have one apple and someone gives me another, I now have two apples. So, 1 plus 1 should be 2. That makes sense.
 Wait, but sometimes math can be tricky. Could it be something else? Like, in a different number system maybe? But I think the question is straightforward, using regular numbers, not like binary or hexadecimal or anything.
 I also recall that in arithmetic, addition is combining quantities. So, if you have two quantities of 1, combining them gives you a total of 2. Yeah, that seems right.
 Is there a scenario where 1 plus 1 wouldn't be 2? I can't think of any...
```

4. If you have a GPU (RTX 4090 for example) with 24GB, you can offload multiple layers to the GPU for faster processing. If you have multiple GPUs, you can probably offload more layers.

```bash
./llama.cpp/llama-cli \
    --model DeepSeek-R1-GGUF/DeepSeek-R1-UD-IQ1_S/DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf \
    --cache-type-k q4_0 \
    -no-cnv --prio 2 \
    --n-gpu-layers 7 \
    --temp 0.6 \
    --ctx-size 8192 \
    --seed 3407 \
    --prompt "<｜User｜>Create a Flappy Bird game in Python.<｜Assistant｜>"
```

5. To test our Flappy Bird example as mentioned in our blog post here: <https://unsloth.ai/blog/deepseekr1-dynamic>, we can produce the 2nd example like below using our 1.58bit dynamic quant:

<table data-column-title-hidden data-view="cards" data-full-width="false"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td>Original DeepSeek R1</td><td></td><td></td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-3c484081174c631653c8c7bf7e7674f05255f740%2FInShot_20250127_043158375_H8Uu6tyJXYAFwUEIu04Am.gif?alt=media">InShot_20250127_043158375_H8Uu6tyJXYAFwUEIu04Am.gif</a></td></tr><tr><td>1.58bit Dynamic Quant</td><td></td><td></td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-c41eac0fea9362017e94123ee8f9793df21b8e97%2FInShot_20250127_042648160_lrtL8-eRhl4qtLaUDSU87.gif?alt=media">InShot_20250127_042648160_lrtL8-eRhl4qtLaUDSU87.gif</a></td></tr></tbody></table>

The prompt used is as below:

{% code overflow="wrap" %}

```
<｜User｜>Create a Flappy Bird game in Python. You must include these things:
1. You must use pygame.
2. The background color should be randomly chosen and is a light shade. Start with a light blue color.
3. Pressing SPACE multiple times will accelerate the bird.
4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.
5. Place on the bottom some land colored as dark brown or yellow chosen randomly.
6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.
7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.
8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.
The final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.<｜Assistant｜>
```

{% endcode %}

To call llama.cpp using this example, we do:

```bash
./llama.cpp/llama-cli \
    --model DeepSeek-R1-GGUF/DeepSeek-R1-UD-IQ1_S/DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf \
    --cache-type-k q4_0 \
    -no-cnv --prio 2 \
    --n-gpu-layers 7 \
    --temp 0.6 \
    --ctx-size 8192 \
    --seed 3407 \
    --prompt "<｜User｜>Create a Flappy Bird game in Python. You must include these things:\n1. You must use pygame.\n2. The background color should be randomly chosen and is a light shade. Start with a light blue color.\n3. Pressing SPACE multiple times will accelerate the bird.\n4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.\n5. Place on the bottom some land colored as dark brown or yellow chosen randomly.\n6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.\n7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.\n8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.\nThe final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.<｜Assistant｜>"
```

5. Also, if you want to merge the weights together for use in Ollama for example, use this script:

```bash
./llama.cpp/llama-gguf-split --merge \
    DeepSeek-R1-GGUF/DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf \
    merged_file.gguf
```

6. DeepSeek R1 has 61 layers. For example with a 24GB GPU or 80GB GPU, you can expect to offload after rounding down (reduce by 1 if it goes out of memory):

| Quant   | File Size | 24GB GPU | 80GB GPU | 2x80GB GPU    |
| ------- | --------- | -------- | -------- | ------------- |
| 1.58bit | 131GB     | 7        | 33       | All layers 61 |
| 1.73bit | 158GB     | 5        | 26       | 57            |
| 2.22bit | 183GB     | 4        | 22       | 49            |
| 2.51bit | 212GB     | 2        | 19       | 32            |

### Running on Mac / Apple devices

For Apple Metal devices, be careful of --n-gpu-layers. If you find the machine going out of memory, reduce it. For a 128GB unified memory machine, you should be able to offload 59 layers or so.

```bash
./llama.cpp/llama-cli \
    --model DeepSeek-R1-GGUF/DeepSeek-R1-UD-IQ1_S/DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf \
    --cache-type-k q4_0 \
    --prio 2 \
    --temp 0.6 \
    --ctx-size 8192 \
    --seed 3407 \
    --n-gpu-layers 59 \
    -no-cnv \
    --prompt "<｜User｜>Create a Flappy Bird game in Python.<｜Assistant｜>"
```

### Run in Ollama/Open WebUI

Open WebUI has made an step-by-step tutorial on how to run R1 here: <https://docs.openwebui.com/tutorials/integrations/llm-providers/deepseekr1-dynamic>

\
If you want to use Ollama for inference on GGUFs, you need to first merge the 3 GGUF split files into 1 like the code below. Then you will need to run the model locally.

```bash
./llama.cpp/llama-gguf-split --merge \
  DeepSeek-R1-GGUF/DeepSeek-R1-UD-IQ1_S/DeepSeek-R1-UD-IQ1_S-00001-of-00003.gguf \
	merged_file.gguf
```

## DeepSeek Chat Template

All distilled versions and the main 671B R1 model use the same chat template:

`<｜begin▁of▁sentence｜><｜User｜>What is 1+1?<｜Assistant｜>It's 2.<｜end▁of▁sentence｜><｜User｜>Explain more!<｜Assistant｜>`

A BOS is forcibly added, and an EOS separates each interaction. To counteract double BOS tokens during inference, you should only call *tokenizer.encode(..., add\_special\_tokens = False)* since the chat template auto adds a BOS token as well.\
For llama.cpp / GGUF inference, you should skip the BOS since it’ll auto add it.

`<｜User｜>What is 1+1?<｜Assistant｜>`

The \<think> and \</think> tokens get their own designated tokens. For the distilled versions for Qwen and Llama, some tokens are re-mapped, whilst Qwen for example did not have a BOS token, so <|object\_ref\_start|> had to be used instead.\
\
**Tokenizer ID Mappings:**

| Token                     | R1     | Distill Qwen | Distill Llama |
| ------------------------- | ------ | ------------ | ------------- |
| \<think>                  | 128798 | 151648       | 128013        |
| \</think>                 | 128799 | 151649       | 128014        |
| <\|begin\_of\_sentence\|> | 0      | 151646       | 128000        |
| <\|end\_of\_sentence\|>   | 1      | 151643       | 128001        |
| <\|User\|>                | 128803 | 151644       | 128011        |
| <\|Assistant\|>           | 128804 | 151645       | 128012        |
| Padding token             | 2      | 151654       | 128004        |

Original tokens in models:

| Token                 | Qwen 2.5 32B Base        | Llama 3.3 70B Instruct            |
| --------------------- | ------------------------ | --------------------------------- |
| \<think>              | <\|box\_start\|>         | <\|reserved\_special\_token\_5\|> |
| \</think>             | <\|box\_end\|>           | <\|reserved\_special\_token\_6\|> |
| <｜begin▁of▁sentence｜> | <\|object\_ref\_start\|> | <\|begin\_of\_text\|>             |
| <｜end▁of▁sentence｜>   | <\|endoftext\|>          | <\|end\_of\_text\|>               |
| <｜User｜>              | <\|im\_start\|>          | <\|reserved\_special\_token\_3\|> |
| <｜Assistant｜>         | <\|im\_end\|>            | <\|reserved\_special\_token\_4\|> |
| Padding token         | <\|vision\_pad\|>        | <\|finetune\_right\_pad\_id\|>    |

All Distilled and the original R1 versions seem to have accidentally assigned the padding token to <｜end▁of▁sentence｜>, which is mostly not a good idea, especially if you want to further finetune on top of these reasoning models. This will cause endless infinite generations, since most frameworks will mask the EOS token out as -100.\
\
We fixed all distilled and the original R1 versions with the correct padding token (Qwen uses <|vision\_pad|>, Llama uses <|finetune\_right\_pad\_id|>, and R1 uses <｜▁pad▁｜> or our own added <｜PAD▁TOKEN｜>.

## GGUF R1 Table

<table data-full-width="true"><thead><tr><th>MoE Bits</th><th>Type</th><th>Disk Size</th><th>Accuracy</th><th>Link</th><th>Details</th></tr></thead><tbody><tr><td>1.58bit</td><td>UD-IQ1_S</td><td><strong>131GB</strong></td><td>Fair</td><td><a href="https://huggingface.co/unsloth/DeepSeek-R1-GGUF/tree/main/DeepSeek-R1-UD-IQ1_S">Link</a></td><td>MoE all 1.56bit. <code>down_proj</code> in MoE mixture of 2.06/1.56bit</td></tr><tr><td>1.73bit</td><td>UD-IQ1_M</td><td><strong>158GB</strong></td><td>Good</td><td><a href="https://huggingface.co/unsloth/DeepSeek-R1-GGUF/tree/main/DeepSeek-R1-UD-IQ1_M">Link</a></td><td>MoE all 1.56bit. <code>down_proj</code> in MoE left at 2.06bit</td></tr><tr><td>2.22bit</td><td>UD-IQ2_XXS</td><td><strong>183GB</strong></td><td>Better</td><td><a href="https://huggingface.co/unsloth/DeepSeek-R1-GGUF/tree/main/DeepSeek-R1-UD-IQ2_XXS">Link</a></td><td>MoE all 2.06bit. <code>down_proj</code> in MoE mixture of 2.5/2.06bit</td></tr><tr><td>2.51bit</td><td>UD-Q2_K_XL</td><td><strong>212GB</strong></td><td>Best</td><td><a href="https://huggingface.co/unsloth/DeepSeek-R1-GGUF/tree/main/DeepSeek-R1-UD-Q2_K_XL">Link</a></td><td>MoE all 2.5bit. <code>down_proj</code> in MoE mixture of 3.5/2.5bit</td></tr></tbody></table>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/deepseek-r1-how-to-run-locally.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
