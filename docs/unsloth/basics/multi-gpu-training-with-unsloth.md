> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/multi-gpu-training-with-unsloth.md).

# Multi-GPU Fine-tuning with Unsloth

Learn how to fine-tune LLMs on multiple GPUs and parallelism with Unsloth.

Unsloth currently supports multi-GPU setups through libraries like Accelerate and DeepSpeed. This means you can already leverage parallelism methods such as **FSDP** and **DDP** with Unsloth.

#### **See our new Distributed Data Parallel** [**(DDP) multi-GPU Guide here**](/docs/basics/multi-gpu-training-with-unsloth/ddp.md)**.**

We know that the process can be complex and requires manual setup. We’re working hard to make multi-GPU support much simpler and more user-friendly, and we’ll be announcing official multi-GPU support for Unsloth soon.

For now, you can use our [Magistral-2509 Kaggle notebook](/docs/models/tutorials/magistral-how-to-run-and-fine-tune.md#fine-tuning-magistral-with-unsloth) as an example which utilizes multi-GPU Unsloth to fit the 24B parameter model or our [DDP guide](/docs/basics/multi-gpu-training-with-unsloth/ddp.md).

**In the meantime**, to enable multi GPU for DDP, do the following:

1. Create your training script as `train.py` (or similar). For example, you can use one of our [training scripts](https://github.com/unslothai/notebooks/tree/main/python_scripts) created from our various notebooks!
2. Run `accelerate launch train.py` or `torchrun --nproc_per_node N_GPUS train.py` where `N_GPUS` is the number of GPUs you have.

#### **Pipeline / model splitting loading**

If you do not have enough VRAM for 1 GPU to load say Llama 70B, no worries - we will split the model for you on each GPU! To enable this, use the `device_map = "balanced"` flag:

```python
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Llama-3.3-70B-Instruct",
    load_in_4bit = True,
    device_map = "balanced",
)
```

**Stay tuned for our official announcement!**\
For more details, check out our ongoing [Pull Request](https://github.com/unslothai/unsloth/issues/2435) discussing multi-GPU support.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/multi-gpu-training-with-unsloth.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
