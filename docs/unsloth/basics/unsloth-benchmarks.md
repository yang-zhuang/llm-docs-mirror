> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/unsloth-benchmarks.md).

# Unsloth Benchmarks

Unsloth recorded benchmarks on NVIDIA GPUs.

* For more detailed benchmarks, read our [Llama 3.3 Blog](https://unsloth.ai/blog/llama3-3).
* Benchmarking of Unsloth was also conducted by [🤗Hugging Face](https://huggingface.co/blog/unsloth-trl).

{% hint style="warning" %}
If your speed seems slower at first, it’s likely because `torch.compile` typically takes \~5 minutes (or longer) to warm up and finish compiling. Make sure you measure throughput **after** it’s fully loaded as over longer runs, Unsloth should be much faster.
{% endhint %}

Tested on H100 and [Blackwell](/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth.md) GPUs. We tested using the Alpaca Dataset, a batch size of 2, gradient accumulation steps of 4, rank = 32, and applied QLoRA on all linear layers (q, k, v, o, gate, up, down):

<table data-full-width="false"><thead><tr><th>Model</th><th>VRAM</th><th>🦥Unsloth speed</th><th>🦥VRAM reduction</th><th>🦥Longer context</th><th>😊Hugging Face + FA2</th></tr></thead><tbody><tr><td>Llama 3.3 (70B)</td><td>80GB</td><td>2x</td><td>>75%</td><td>13x longer</td><td>1x</td></tr><tr><td>Llama 3.1 (8B)</td><td>80GB</td><td>2x</td><td>>70%</td><td>12x longer</td><td>1x</td></tr></tbody></table>

## Context length benchmarks

{% hint style="info" %}
The more data you have, the less VRAM Unsloth uses due to our [gradient checkpointing](https://unsloth.ai/blog/long-context) algorithm + Apple's CCE algorithm!
{% endhint %}

### **Llama 3.1 (8B) max. context length**

We tested Llama 3.1 (8B) Instruct and did 4bit QLoRA on all linear layers (Q, K, V, O, gate, up and down) with rank = 32 with a batch size of 1. We padded all sequences to a certain maximum sequence length to mimic long context finetuning workloads.

| GPU VRAM | 🦥Unsloth context length | Hugging Face + FA2 |
| -------- | ------------------------ | ------------------ |
| 8 GB     | 2,972                    | OOM                |
| 12 GB    | 21,848                   | 932                |
| 16 GB    | 40,724                   | 2,551              |
| 24 GB    | 78,475                   | 5,789              |
| 40 GB    | 153,977                  | 12,264             |
| 48 GB    | 191,728                  | 15,502             |
| 80 GB    | 342,733                  | 28,454             |

### **Llama 3.3 (70B) max. context length**

We tested Llama 3.3 (70B) Instruct on a 80GB A100 and did 4bit QLoRA on all linear layers (Q, K, V, O, gate, up and down) with rank = 32 with a batch size of 1. We padded all sequences to a certain maximum sequence length to mimic long context finetuning workloads.

| GPU VRAM | 🦥Unsloth context length | Hugging Face + FA2 |
| -------- | ------------------------ | ------------------ |
| 48 GB    | 12,106                   | OOM                |
| 80 GB    | 89,389                   | 6,916              |


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/unsloth-benchmarks.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
