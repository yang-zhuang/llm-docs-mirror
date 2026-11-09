> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune/gpt-oss-reinforcement-learning.md).

# gpt-oss Reinforcement Learning

You can now train OpenAI [gpt-oss](/docs/models/gpt-oss-how-to-run-and-fine-tune.md) with RL and GRPO via [Unsloth](https://github.com/unslothai/unsloth). Unsloth now offers the **fastest inference** (3x faster), **lowest VRAM usage** (50% less) and **longest context** (8x longer) for gpt-oss RL vs. any implementation - with no accuracy degradation.\
\
Since reinforcement learning (RL) on gpt-oss isn't yet vLLM compatible, we had to rewrite the inference code from Transformers code to deliver 3x faster inference for gpt-oss at \~21 tokens/s. For BF16, Unsloth also achieves the fastest inference (\~30 tokens/s), especially relative to VRAM usage, using 50% less VRAM vs. any other RL implementation. We plan to support our [50% weight sharing feature](/docs/get-started/reinforcement-learning-rl-guide/memory-efficient-rl.md) once vLLM becomes compatible with RL.

* **Free notebook:** [**gpt-oss-20b GRPO Colab notebook**](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-\(20B\)-GRPO.ipynb)\
  This notebook automatically creates **faster matrix multiplication kernels** and uses 4 new Unsloth reward functions. We also show how to [counteract reward-hacking](#can-we-counter-reward-hacking) which is one of RL's biggest challenges.\\

  <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-0217fec82f064279c090618091109c6b36c724de%2FAuto%20generated.png?alt=media" alt=""><figcaption></figcaption></figure>

With Unsloth, you can train gpt-oss-20b with GRPO on 15GB VRAM and for **free** on Colab. We introduced embedding offloading which reduces usage by 1GB as well via `offload_embeddings`. Unloth's new inference runs faster on **any** GPU including A100, H100 and old T4's. gpt-oss-120b fits nicely on a 120GB VRAM GPU.

Unsloth is the only framework to support 4-bit RL for gpt-oss. All performance gains are due to Unsloth's unique [weight sharing](/docs/get-started/reinforcement-learning-rl-guide.md#what-unsloth-offers-for-rl), [Flex Attention](/docs/get-started/reinforcement-learning-rl-guide/memory-efficient-rl.md), [Standby](/docs/get-started/reinforcement-learning-rl-guide/memory-efficient-rl.md#unsloth-standby) and custom kernels.

{% hint style="warning" %}
Reminder: **Flash Attention 3 (FA3) is** [**unsuitable for gpt-oss**](/docs/models/gpt-oss-how-to-run-and-fine-tune/long-context-gpt-oss-training.md#introducing-unsloth-flex-attention-support) **training** since it currently does not support the backward pass for attention sinks, causing **incorrect training losses**. If you’re **not** using Unsloth, FA3 may be enabled by default, so please double-check it’s not in use!\
\
Disabling FA3 will incur **O(N^2)** memory usage as well, so Unsloth is the only RL framework to offer **O(N)** memory usage for gpt-oss via our Flex attention implementation.
{% endhint %}

## ⚡Making Inference Much Faster

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-6e9b6a2f7381de84ed6eeb0feedc566cd443acf3%2F5b957843-eb58-4778-8b90-f25767c51495.png?alt=media" alt=""><figcaption></figcaption></figure>

Inference is crucial in RL training, since we need it to generate candidate solutions before maximizing some reward function ([see here](/docs/get-started/reinforcement-learning-rl-guide.md) for a more detailed explanation). To achieve the fastest inference speed for gpt-oss without vLLM, we rewrote Transformers inference code and integrated many innovations including custom algorithms like Unsloth [Flex Attention](/docs/models/gpt-oss-how-to-run-and-fine-tune/long-context-gpt-oss-training.md#introducing-unsloth-flex-attention-support), using special flags within `torch.compile` (like combo kernels). Our new inference code for gpt-oss was evaluated against an already optimized baseline (2x faster than native Transformers).

vLLM does not support RL for gpt-oss since it lacks BF16 training and LoRA support for gpt-oss. Without Unsloth, only training via full precision BF16 works, making memory use **800%+ higher**. Most frameworks enable FA3 (Flash Attention 3) by default (which reduces VRAM use & increases speed) **but this causes incorrect training loss**. See [Issue 1797](https://github.com/Dao-AILab/flash-attention/issues/1797) in the FA3 repo. You must disable FA3 though, since it'll prevent long-context training since FA3 uses O(N) memory usage, whilst naive attention will balloon with O(N^2) usage. So to enable attention sinks to be differentiable, we implemented [Unsloth Flex Attention](/docs/models/gpt-oss-how-to-run-and-fine-tune/long-context-gpt-oss-training.md).

We evaluated gpt-oss RL inference by benchmarking BitsandBytes 4-bit and also did separate tests for BF16. Unsloth’s 4-bit inference is \~4x faster, and BF16 is also more efficient, especially in VRAM use.

The best part about Unsloth's gpt-oss RL is that it can work on any GPU, even those that do not support BF16. Our free gpt-oss-20b Colab notebooks use older 15GB T4 GPUs, so the inference examples work well!

## 🛠️ gpt-oss Flex Attention Issues and Quirks

We had to change our implementation for attention sinks as [described here](/docs/models/gpt-oss-how-to-run-and-fine-tune/long-context-gpt-oss-training.md) to allow generation to work with left padding. We had to get the logsumexp and apply the sigmoid activation to alter the attention weights like below:

$$
A(X) = \sigma \bigg( \frac{1}{\sqrt{d}}QK^T \bigg)V \\

A(X) = \frac{\exp{\frac{1}{\sqrt{d}}QK^T}}{\sum{\exp{\frac{1}{\sqrt{d}}QK^T}}}V \\

\text{LSE} = \log{\sum{\exp{\frac{1}{\sqrt{d}}QK^T}}} \\

A\_{sinks}(X) = A(X) \odot \sigma (\text{LSE} - \text{sinks})
$$

Left padded masking during inference was also a tricky issue to deal with in gpt-oss. We found that we had to not only account for KV Cache prefill during generations of tokens, but also account for a unique amount of pad tokens in each prompt for batch generations which would change the way we would need to store the block mask. Example of such and example can be seen below:

**Normal Causal Mask:**

```
   k0 k1 k2 k3 k4   <-- keys
q0  X
q1  X  X
q2  X  X  X
q3  X  X  X  X
q4  X  X  X  X  X   <-- last query row (most important for decoding)
```

**For inference in general case (decoding)**

```
    k0 k1 k2 k3 k4
q0
q1
q2
q3
q4   X  X  X  X  X
```

**If we naively use the same masking strategy, this'll fail:**

```
    k0 k1 k2 k3 k4
q0
q1
q2
q3
q4   X   (note that q4 has q_idx=0 as this is the first query in current setup)
```

For generation (decoding phase), we usually only care about the last row of the attention matrix, since there’s just one query token attending to all previous key tokens. If we naively apply the causal mask (`q_idx ≥ k_idx`), this fails as our single query has index 0, while there are n\_k key tokens. To fix this, we need an offset in mask creation to decide which tokens to attend. But a naïve approach is slow, since offsets change each step, forcing mask and kernel regeneration. We solved this with cache and compile optimizations.

The harder part is batch generation. Sequences differ in length, so padding complicates mask creation. Flex Attention had a lot of [challenges](https://github.com/meta-pytorch/attention-gym/issues/15#issuecomment-2284148665) and dynamic masks are tricky. Worse, if not compiled, it falls back to eager attention which is slow and memory-heavy (quadratic vs. linear in sequence length).

> *Quote from* [*https://github.com/meta-pytorch/attention-gym/issues/15#issuecomment-2284148665*](https://github.com/meta-pytorch/attention-gym/issues/15#issuecomment-2284148665)
>
> You need to call this with \_compile=True. We essentially map your block mask over a full Q\_LEN x KV\_LEN matrix in order to produce the block mask. Without compile, we need to materialize this full thing, and it can cause OOMs on long sequences.
>
> As well, you need to run `flex_attention = torch.compile(flex_attention)`. Without compile, flex falls back to a non-fused eager implementation that is great for debugging, but it is much slower and materializes the full scores matrix.

Ultimately, the mask must dynamically handle prefill vs decode with the KV Cache, batch and padding tokens per sequence, remain `torch.compile` friendly, and support sliding windows.

### 🔍 Flash Attention Investigation

Another interesting direction we explored was trying to integrate Flash Attention. Its advantages are widely recognized, but one limitation is that it does not support attention sinks during the backward pass for gpt-oss. To work around this, we restructured the attention mechanism so that it operates solely on the attention output and the logsumexp values that FlashAttention readily provides. Given these benefits, it seemed like an obvious choice to try.

However, we soon began noticing issues. While the first few layers behaved as expected, the later layers, particularly layers 18 through 24, produced outputs that diverged significantly from the eager-mode implementation in transformers. Importantly, this discrepancy cannot be attributed to error accumulation, since the inputs to each method are identical at every layer. For further validation, we also compared the results against Unsloth **FlexAttention**.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-1c7a04d20aa814cd04065001d59e338c27426f19%2Fimage.png?alt=media" alt=""><figcaption></figcaption></figure>

This needs further investigation into why only the last few layers show such a drastic difference between flash attention implementation vs. the others.

{% hint style="danger" %}
**Flash Attention 3 doesn't support the backwards pass for attention sinks**

FA3 is often enabled by default for most training packages (not Unsloth), but this is incorrect for gpt-oss. Using FA3 will make training loss completely wrong as FA3 doesn’t support gpt-oss backward passes for attention sinks. Many people are still unaware of this so please be cautious!
{% endhint %}

## ⚠️ Can We Counter Reward Hacking?

The ultimate goal of RL is to maximize some reward (say speed, revenue, some metric). But RL can **cheat.** When the RL algorithm learns a trick or exploits something to increase the reward, without actually doing the task at end, this is called "**Reward Hacking**".

It's the reason models learn to modify unit tests to pass coding challenges, and these are critical blockers for real world deployment. Some other good examples are from [Wikipedia](https://en.wikipedia.org/wiki/Reward_hacking).

<div align="center"><figure><img src="https://i.pinimg.com/originals/55/e0/1b/55e01b94a9c5546b61b59ae300811c83.gif" alt="" width="188"><figcaption></figcaption></figure></div>

In our [free gpt-oss RL notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-\(20B\)-GRPO.ipynb) we explore how to counter reward hacking in a code generation setting and showcase tangible solutions to common error modes. We saw the model edit the timing function, outsource to other libraries, cache the results, and outright cheat. After countering, the result is our model generates genuinely optimized matrix multiplication kernels, not clever cheats.

## :trophy:Reward Hacking

Some common examples of reward hacking during RL include:

#### Laziness

RL learns to use Numpy, Torch, other libraries, which calls optimized CUDA kernels. We can stop the RL algorithm from calling optimized code by inspecting if the generated code imports other non standard Python libraries.

#### Caching & Cheating

RL learns to cache the result of the output and RL learns to find the actual output by inspecting Python global variables.

We can stop the RL algorithm from using cached data by wiping the cache with a large fake matrix. We also have to benchmark carefully with multiple loops and turns.

#### Cheating

RL learns to edit the timing function to make it output 0 time as passed. We can stop the RL algorithm from using global or cached variables by restricting it's `locals` and `globals`. We are also going to use `exec` to create the function, so we have to save the output to an empty dict. We also disallow global variable access via `types.FunctionType(f.__code__, {})`\\

## Tutorial: How to Train gpt-oss with RL

LLMs often struggle with tasks that involve complex environments. However, by applying [reinforcement learning](/docs/get-started/reinforcement-learning-rl-guide.md) (RL) and designing a custom [reward function](/docs/get-started/reinforcement-learning-rl-guide.md#reward-functions-verifiers), these challenges can be overcome.

RL can be adapted for tasks such as auto kernel or strategy creation. This tutorial shows how to train **gpt-oss** with [**GRPO**](/docs/get-started/reinforcement-learning-rl-guide.md#from-rlhf-ppo-to-grpo-and-rlvr) and Unsloth to autonomously beat 2048.

Our notebooks include step-by-step guides on how to navigate the whole process already.

| [2048 notebook](https://colab.research.google.com/github/openai/gpt-oss/blob/main/examples/reinforcement-fine-tuning.ipynb) (Official OpenAI example) | [Kernel generation notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-\(20B\)-GRPO.ipynb) |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |

**What you’ll build:**

* Train gpt-oss-20b so the model can automatically win 2048
* Create a minimal 2048 environment the model can interact with
* Define **reward functions** that:
  1. Check the generated strategy compiles and runs,
  2. Prevent reward hacking (disallow external imports), and
  3. Reward actual game success
* Run inference and export the model (MXFP4 4‑bit or merged FP16)

{% hint style="info" %}
**Hardware:** The 2048 example runs on a free Colab T4, but training will be slow. A100/H100 is much faster. 4‑bit loading + LoRA lets you fit a 20B model into modest VRAM
{% endhint %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/gpt-oss-how-to-run-and-fine-tune/gpt-oss-reinforcement-learning.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
