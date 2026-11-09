> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/diffusiongemma.md).

# DiffusionGemma - How to Run Locally

DiffusionGemma **26B-A4B** is Google DeepMind’s new open **multimodal** model, built on the [Gemma 4](/docs/models/gemma-4.md) MoE architecture. With support for **256K context**, **140+ languages**, DiffusionGemma is designed for **high-speed text generation** across text, video and image inputs. DiffusionGemma can run locally on **18GB RAM**, and [fine-tuning](#fine-tune-diffusiongemma) is now supported via [Unsloth](https://github.com/unslothai/unsloth).

Instead of standard token-by-token decoding, DiffusionGemma uses **diffusion generation** to produce outputs in parallel and gradually refine them into a final answer - similar to diffusion image models, but for text. Run the model via [Unsloth Studio](/docs/new/studio.md) or llama.cpp. On a RTX 6000, DiffusionGemma can reach **2000+ tokens/s**. **GGUF:** [diffusiongemma-26B-A4B-it-GGUF](https://huggingface.co/unsloth/diffusiongemma-26B-A4B-it-GGUF)

<a href="/docs/models/diffusiongemma.md#run-diffusiongemma-tutorials" class="button primary">Run DiffusionGemma</a><a href="/docs/models/diffusiongemma.md#fine-tune-diffusiongemma" class="button secondary">Fine-tune DiffusionGemma</a>

{% hint style="success" %}
**Jun 12:** You can now run DiffusionGemma via [Unsloth Studio](#unsloth-studio-guide) ✨ with 1.8x faster inferece!
{% endhint %}

### Usage Guide

DiffusionGemma is designed for users who need faster generation than standard models. It is suited to fast local inference, long-context doc analysis, image/video understanding, OCR and document parsing, code generation, tool use, agentic workflows, and low-latency small-batch inference.

Unlike standard Gemma 4 models, DiffusionGemma requires a diffusion-aware inference runtime. Autoregressive settings such as `temperature`, `top_p`, and `top_k` alone are not enough to reproduce the recommended behavior without the required diffusion sampler.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fszoidwwj70dLm5vBjpmL%2Fdiffusiongemma.gif?alt=media&amp;token=8ce359fd-f92c-4cf8-a491-06b04c505cb7" alt="" width="563"><figcaption></figcaption></figure></div>

### Hardware requirements

It's generally best to have at least 18GB RAM to run the model in 4-bit precision. **GGUF:** [diffusiongemma-26B-A4B-it-GGUF](https://huggingface.co/unsloth/diffusiongemma-26B-A4B-it-GGUF)

**Table: DiffusionGemma Inference GGUF recommended hardware requirements** (units = total memory: RAM + VRAM, or unified memory).

| 4-bit | 5-bit | 6-bit | 8-bit | BF16 / FP16 |
| ----- | ----- | ----- | ----- | ----------- |
| 18 GB | 20 GB | 24 GB | 28 GB | 52 GB       |

{% hint style="info" %}
As a rule of thumb, your total available memory should at least exceed the size of the quantized model you download. If it does not you can still run using partial RAM / disk offload, but generation will be slower. You will also need more compute, depending on the context window you use.
{% endhint %}

## Run DiffusionGemma Tutorials

It's best to use at least 4-bit precision so we'll use the 4-bit `Q4_K_M` quant which needs 18GB RAM. **GGUF:** [diffusiongemma-26B-A4B-it-GGUF](https://huggingface.co/unsloth/diffusiongemma-26B-A4B-it-GGUF)

<a href="/docs/models/diffusiongemma.md#unsloth-studio-guide" class="button primary">🦥 Unsloth Studio Guide</a><a href="/pages/vTAENqjMpaMcreC9lp4b#llama.cpp-guide" class="button primary">🦙 Llama.cpp Guide</a>

### 🦥 Unsloth Studio Guide

{% hint style="success" %}
You can now run DiffusionGemma via [Unsloth Studio](#unsloth-studio-guide) ✨. Ensure you use [`v0.1.463-beta`](https://github.com/unslothai/unsloth/tree/v0.1.462-beta) or `2026.6.6`.
{% endhint %}

DiffusionGemma can now be run and trained in [Unsloth Studio](/docs/new/studio.md), our new open-source web UI for local AI. Unsloth Studio lets you run models locally on **MacOS**, **Windows**, Linux and:

{% columns %}
{% column %}

* Search, download, [run GGUFs](/docs/new/studio.md#run-models-locally) and safetensor models
* [**Self-healing** tool calling](/docs/new/studio.md#execute-code--heal-tool-calling) + **web search**
* [**Code execution**](/docs/new/studio.md#run-models-locally) (Python, Bash)
* [Automatic inference](https://unsloth.ai/docs/desktop#feature-deep-dive) parameter tuning (temp, top-p, etc.)
* Fast CPU + GPU inference via llama.cpp
* [Train LLMs](/docs/new/studio.md#no-code-training) 2x faster with 70% less VRAM
  {% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fszoidwwj70dLm5vBjpmL%2Fdiffusiongemma.gif?alt=media&amp;token=8ce359fd-f92c-4cf8-a491-06b04c505cb7" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% stepper %}
{% step %}

#### Install Unsloth

Ensure you use the latest [`v0.1.463-beta`](https://github.com/unslothai/unsloth/tree/v0.1.462-beta) or `2026.6.6`. Run in your terminal:

**MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows PowerShell:**

```bash
irm https://unsloth.ai/install.ps1 | iex
```

{% endstep %}

{% step %}

#### Launch Unsloth

**MacOS, Linux, WSL and Windows:**

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

Then open `http://127.0.0.1:8888` (or your specific URL) in your browser.
{% endstep %}

{% step %}

#### Search and download DiffusionGemma

On first launch you will need to create a password to secure your account and sign in again.

Then go to the [Unsloth Chat](/docs/new/studio/chat.md) tab and search for DiffusionGemma in the search bar and download your desired model and quant.
{% endstep %}

{% step %}

#### Run DiffusionGemma

Inference parameters should be auto-set when using Unsloth Studio, however you can still change it manually. You can also edit the context length, chat template and other settings.

For more information, you can view our [Unsloth Studio inference guide](/docs/new/studio/chat.md).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fszoidwwj70dLm5vBjpmL%2Fdiffusiongemma.gif?alt=media&amp;token=8ce359fd-f92c-4cf8-a491-06b04c505cb7" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### 🦙 Llama.cpp Guide

For this tutorial, we will be utilizing the Dynamic 4-bit `Q4_K_M` quant which needs 18GB RAM and [llama.cpp](llama.cpphttps://github.com/ggml-org/llama.cpp) for fast local inference, especially if you have a CPU.

{% stepper %}
{% step %}
Obtain the SPECIFIC `llama.cpp` PR on [**GitHub here**](https://github.com/ggml-org/llama.cpp/pull/24423). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
gh pr checkout 24423
# build with CUDA (drop -DGGML_CUDA=ON for a CPU-only build)
cmake -B build -DGGML_CUDA=ON
cmake --build build -j --config Release --target llama-diffusion-cli
cd ..
```

{% endstep %}

{% step %}
Download the model via (after installing `pip install huggingface_hub`). You can choose `Q4_K_M` or other quantized versions like `Q8_0` . If downloads get stuck, see: [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

```bash
pip install -U "huggingface_hub[cli]"
hf download unsloth/diffusiongemma-26B-A4B-it-GGUF \
    --local-dir unsloth/diffusiongemma-26B-A4B-it-GGUF \
    --include "*Q8_0*" # Use "*Q4_K_M*" for a smaller 16 GB download
```

{% endstep %}
{% endstepper %}

### Chat with DiffusionGemma

Then run the below:

{% code overflow="wrap" %}

```bash
./build/bin/llama-diffusion-cli \
  -m unsloth/diffusiongemma-26B-A4B-it-GGUF/diffusiongemma-26B-A4B-it-Q8_0.gguf \
  -ngl 99 -cnv -n 2048
```

{% endcode %}

You will see:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fqax7SXjUrxZpWORhexyj%2Fimage.png?alt=media&amp;token=066fb8a1-8865-417a-9ca0-2c5443ebe520" alt=""><figcaption></figcaption></figure>

And if you type a question like "Create a Flappy Bird Game", you will see steps:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FWBxW71WgZwEmj8vqEuhT%2Fimage.png?alt=media&amp;token=19ae3bfc-2a8d-463b-b2cb-7b9456ee9226" alt=""><figcaption></figcaption></figure>

Then afterwards you'll see the output:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fngo7EXmeZnJKhmWAcrNy%2Fimage.png?alt=media&amp;token=f6024241-227c-41f9-9a23-cac8418f89e7" alt="" width="375"><figcaption></figcaption></figure>

You can continue conversing as well!

Change `-n 2048` as the number of tokens you want to predict, so more will produce longer answers.

### Live visualization of diffusion

To see diffusion actually live, use the below - specially enable `--diffusion-visual`:

```bash
./build/bin/llama-diffusion-cli \
  -m unsloth/diffusiongemma-26B-A4B-it-GGUF/diffusiongemma-26B-A4B-it-Q8_0.gguf \
  -ngl 99 -cnv -n 2048 --diffusion-visual
```

You will again see:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FwvBjHSctfgHXYDAu1TFp%2Fimage.png?alt=media&amp;token=860a27d0-6d1c-404b-972a-4cdbdcce166a" alt=""><figcaption></figcaption></figure>

And we get:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FTrPopPhlJZGW28cyjaJB%2Fdiffusiongem.gif?alt=media&amp;token=b8d9434b-d929-4f13-81ad-ecfe21262169" alt="" width="563"><figcaption></figcaption></figure>

All parameters for llama.cpp using the branch:

* `-n, --n-predict N` - target tokens; derives `--diffusion-blocks` and grows `-ub` / `-b` / `-c`.
* `-ngl 99` - offload all layers to the GPU (`-ngl 0` for CPU-only).
* `-cnv` - multi-turn conversation mode.
* `--diffusion-visual` - live canvas denoising view.
* The Entropy-Bound sampler is on by default (`--diffusion-eb auto`). Tune it with `--diffusion-eb-max-steps` (default 48), `--diffusion-eb-t-max` / `--diffusion-eb-t-min` (0.8 -> 0.4), `--diffusion-eb-entropy-bound` (0.1), and `--diffusion-eb-confidence` (0.005).
* `--diffusion-kv-cache {auto,on,off}` - prompt prefix KV cache (auto = on for single GPU).

## Fine-tune DiffusionGemma

You can now train and fine-tune DiffusionGemma directly with [**Unsloth**](#unsloth-studio-guide). In our example, we demonstrate the impact of domain-specific training by fine-tuning the model on Sudoku. The base model initially performs poorly on Sudoku tasks, but after training on a targeted dataset, it learns how to actually solve sudoku and solves every example correctly.

You can use our Colab notebook (A100) to fine-tune DiffusionGemma with:

{% embed url="<https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/DiffusionGemma_(26B-A4B)-Sudoku.ipynb>" %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FexAR7eC5YN44boNs2tFD%2Fsudoku_before_after(1).gif?alt=media&amp;token=2bc254a8-dbf9-4638-a5cb-8a7877d3c9fa" alt="" width="563"><figcaption></figcaption></figure></div>

## Recommended Settings

[Unsloth Studio](#unsloth-studio-guide) automatically sets the best inference settings for your model. Use below if necessary:

| Category          | Setting                   | Value                       |
| ----------------- | ------------------------- | --------------------------- |
| Sampling          | Method                    | `diffusion_sampling`        |
| Sampling          | Sampler                   | `entropy_bounded_denoising` |
| Sampling          | Max denoising steps       | `48`                        |
| Temperature       | Temperature schedule      | `linear_decay`              |
| Temperature       | Temperature start         | `0.8`                       |
| Temperature       | Temperature end           | `0.4`                       |
| Entropy           | Entropy bound             | `0.1`                       |
| Adaptive stopping | Adaptive stopping enabled | `true`                      |
| Adaptive stopping | Entropy threshold         | `0.005`                     |
| Canvas            | Canvas length             | `256`                       |

**Adaptive Stopping Trigger Conditions**

Adaptive stopping should trigger only when **both** conditions are met:

| Condition                                                 | Required Value |
| --------------------------------------------------------- | -------------- |
| Average canvas entropy                                    | `< 0.005`      |
| Highest-probability tokens stable for 2 consecutive steps | `true`         |

At each denoising step, the sampler should select the lowest-entropy tokens whose mutual information bound remains: `entropy_bound = 0.1`. Non-selected tokens should be fully renoised before the next denoising step.

### Thinking Mode

DiffusionGemma supports Gemma 4-style thinking mode. To enable thinking, add the thinking token at the start of the system prompt:

```
<|think|>
```

When thinking is enabled, the model may emit an internal reasoning channel followed by the final answer:

```
<|channel>thought
[internal reasoning]
<channel|>
[final answer]
```

To disable thinking, remove the `<|think|>` token from the system prompt. When thinking is disabled, the model may still emit an empty thought channel:

```
<|channel>thought
<channel|>
[final answer]
```

For multi-turn conversations, do **not** include previous hidden thoughts in the conversation history. Only include the final assistant response before the next user turn.

## DiffusionGemma Best Practices

### Multimodal Prompting

DiffusionGemma supports interleaved multimodal inputs, including text and images. Video can be processed as sequences of image frames.

For best results with multimodal prompts, place image or frame content before text instructions. Example:

```
[image]
Describe the chart and summarize the key trend.
```

For document parsing, OCR, chart understanding, UI understanding, or small text extraction, use a higher visual token budget.

Supported visual token budgets:

| Visual Token Budget | Best For                                         |
| ------------------- | ------------------------------------------------ |
| 70                  | Fast classification, simple captioning           |
| 140                 | Lightweight visual QA                            |
| 280                 | General image understanding                      |
| 560                 | OCR, charts, UI screenshots                      |
| 1120                | Dense documents, small text, detailed extraction |

For video-style inputs, DiffusionGemma can process up to **60 seconds** when sampled at **1 frame per second**.

### Sampling Notes

DiffusionGemma is not a normal next-token-only model. It generates a block of tokens, called a **canvas**, by repeatedly refining noisy token predictions. The generation process works roughly as follows:

1. The encoder processes the prompt and builds a context cache.
2. The decoder receives a 256-token generation canvas.
3. The diffusion sampler iteratively denoises the canvas.
4. Confident tokens are selected and preserved.
5. Uncertain tokens are renoised and refined again.
6. Once the canvas is complete, it is appended to the context.
7. The model continues with the next canvas.

This block-autoregressive approach allows DiffusionGemma to generate many tokens in fewer forward passes than a standard autoregressive model.

## Benchmarks

DiffusionGemma is optimized for speed and multimodal reasoning, though standard Gemma 4 is stronger on conventional reasoning benchmarks.

| Benchmark           | DiffusionGemma 26B-A4B | Gemma 4 26B-A4B |
| ------------------- | ---------------------: | --------------: |
| MMLU Pro            |                  77.6% |           82.6% |
| AIME 2026 no tools  |                  69.1% |           88.3% |
| LiveCodeBench v6    |                  69.1% |           77.1% |
| Codeforces ELO      |                   1429 |            1718 |
| GPQA Diamond        |                  73.2% |           82.3% |
| Tau2 Average        |                  56.2% |           68.2% |
| HLE no tools        |                  11.0% |            8.7% |
| HLE with search     |                  11.9% |           17.2% |
| BigBench Extra Hard |                  47.6% |           64.8% |
| MMMLU               |                  81.5% |           86.3% |

| Long Context Benchmark        | DiffusionGemma 26B-A4B | Gemma 4 26B-A4B |
| ----------------------------- | ---------------------: | --------------: |
| MRCR v2 8 needle 128K average |                  32.0% |           44.1% |

**Vision benchmarks:**

| Vision Benchmark                  | DiffusionGemma 26B-A4B | Gemma 4 26B-A4B |
| --------------------------------- | ---------------------: | --------------: |
| MMMU Pro                          |                  54.3% |           73.8% |
| OmniDocBench 1.5, lower is better |                  0.319 |           0.149 |
| MATH-Vision                       |                  70.5% |           82.4% |
| MedXPertQA MM                     |                  49.0% |           58.1% |


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/diffusiongemma.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
