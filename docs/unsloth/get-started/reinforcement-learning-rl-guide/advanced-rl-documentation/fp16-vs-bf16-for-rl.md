> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/advanced-rl-documentation/fp16-vs-bf16-for-rl.md).

# FP16 vs BF16 for RL

Defeating the Training-Inference Mismatch via FP16 https\://arxiv.org/pdf/2510.26788 shows how using float16 is better than bfloat16

### Float16 vs Bfloat16

There was a paper titled "**Defeating the Training-Inference Mismatch via FP16**" <https://arxiv.org/pdf/2510.26788> showing how using float16 precision can dramatically be better than using bfloat16 when doing reinforcement learning.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Frec4qe1aQS0xyMzGvS9c%2Fimage.png?alt=media&amp;token=2137e766-0f1f-48ec-b25f-2292d6f149f4" alt=""><figcaption></figcaption></figure>

In fact the longer the generation, the worse it gets when using bfloat16:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FWs7ioB2lraTbDbUCOAnn%2Fimage.png?alt=media&amp;token=ac2b4f8e-210f-4bcc-bcbb-6e68f80781a6" alt=""><figcaption></figcaption></figure>

We did an investigation, and **DO find float16 to be more stable** than bfloat16 with much smaller gradient norms see <https://x.com/danielhanchen/status/1985557028295827482> and <https://x.com/danielhanchen/status/1985562902531850472>

{% columns %}
{% column width="50%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FhvQ1W5wtV6TTfsetp7y2%2FG44d7ZFbIAANBBd.jpg?alt=media&amp;token=35181a07-de3e-4321-b54e-4436b4a201ff" alt=""><figcaption></figcaption></figure>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F62HkxnGcaKvxnSxbZMZu%2FG44c20SbwAAGo8j.jpg?alt=media&amp;token=e0c7ecb8-6f0c-4ecf-b1a0-50f1b2a9a807" alt=""><figcaption></figcaption></figure>
{% endcolumn %}

{% column width="50%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fsi18IkGqE4IuUvzroyHh%2FG44ix5FbQAM0L5l.jpg?alt=media&amp;token=bc3b97ce-5df4-4b69-aa50-a8e339f21601" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

### :exploding\_head:A100 Cascade Attention Bug

As per <https://x.com/RichardYRLi/status/1984858850143715759> and <https://yingru.notion.site/When-Speed-Kills-Stability-Demystifying-RL-Collapse-from-the-Training-Inference-Mismatch-271211a558b7808d8b12d403fd15edda>, older vLLM versions (before 0.11.0) had broken attention mechanisms for A100 and similar GPUs. Please update vLLM! We also by default disable cascade attention in vLLM during Unsloth reinforcement learning if we detect an older vLLM version.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FnkCLRVIIGLADXBSCe58e%2Fimage.png?alt=media&amp;token=6669642f-8690-44bf-b2de-6aa89acf2332" alt=""><figcaption></figcaption></figure>

Different hardware also changes results, where newer and more expensive GPUs have less KL difference between the inference and training sides:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FaroTTz68zzyofy6nagtH%2Fimage.webp?alt=media&amp;token=3be09506-b8a0-42eb-8d17-af72496a9cd1" alt=""><figcaption></figcaption></figure>

### :fire:Using float16 in Unsloth RL

To use float16 precision in Unsloth GRPO and RL, you just need to set `dtype = torch.float16` and we'll take care of the rest!

{% code overflow="wrap" %}

```python
from unsloth import FastLanguageModel
import torch
max_seq_length = 2048 # Can increase for longer reasoning traces
lora_rank = 32 # Larger rank = smarter, but slower

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen3-4B-Base",
    max_seq_length = max_seq_length,
    load_in_4bit = False, # False for LoRA 16bit
    fast_inference = True, # Enable vLLM fast inference
    max_lora_rank = lora_rank,
    gpu_memory_utilization = 0.9, # Reduce if out of memory
    
    dtype = torch.float16, # Use torch.float16, torch.bfloat16
)
```

{% endcode %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/advanced-rl-documentation/fp16-vs-bf16-for-rl.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
