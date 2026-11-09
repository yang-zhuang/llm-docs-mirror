> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md).

# Hugging Face Hub, XET debugging

Debugging, troubleshooting stalled, stuck downloads and slow downloads

#### Downloads are stuck at 90% to 99%

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FAupnur7cpMvilAleA1Gp%2Fimage.png?alt=media&amp;token=146a3d2e-6c2c-438e-9bf7-6265bc6d6cb4" alt=""><figcaption></figcaption></figure>

If you see downloads via `hf download unsloth/*` get stuck at 90% or 99% of progress for quite some time, cancel the current run, and try adding using below commands:

```bash
pip install -U huggingface_hub

HF_HOME=".cache_new/huggingface" \
HF_XET_CACHE=".cache_new/huggingface/xet" \
HF_HUB_CACHE=".cache_new/huggingface/hub" \
HF_XET_HIGH_PERFORMANCE=1 \
HF_XET_CHUNK_CACHE_SIZE_BYTES=0 \
HF_XET_RECONSTRUCT_WRITE_SEQUENTIALLY=0 \
HF_XET_NUM_CONCURRENT_RANGE_GETS=64 \
hf download unsloth/Qwen3-Coder-Next-GGUF \
    --local-dir unsloth/Qwen3-Coder-Next-GGUF \
    --include "*UD-Q6_K_XL*"
```

#### Rate limited or 429 Too Many Requests?

Try using `snapshot_download` instead, then import Unsloth which will set the correct Hugging Face variables for you:

```python
import unsloth
import os

os.environ["HF_HOME"] = ".cache_new/huggingface"
os.environ["HF_XET_CACHE"] = ".cache_new/huggingface/xet"
os.environ["HF_HUB_CACHE"] = ".cache_new/huggingface/hub"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Qwen3-Coder-Next-GGUF",
    local_dir = "unsloth/Qwen3-Coder-Next-GGUF",
    allow_patterns = ["*UD-Q6_K_XL*"],
)
```

Or maybe try getting a Hugging Face token first via <https://huggingface.co/settings/tokens>

```bash
pip install -U huggingface_hub

HF_HOME=".cache_new/huggingface" \
HF_XET_CACHE=".cache_new/huggingface/xet" \
HF_HUB_CACHE=".cache_new/huggingface/hub" \
HF_XET_HIGH_PERFORMANCE=1 \
HF_XET_CHUNK_CACHE_SIZE_BYTES=0 \
HF_XET_RECONSTRUCT_WRITE_SEQUENTIALLY=0 \
HF_XET_NUM_CONCURRENT_RANGE_GETS=64 \
    hf download unsloth/Qwen3-Coder-Next-GGUF \
    --local-dir unsloth/Qwen3-Coder-Next-GGUF \
    --include "*UD-Q6_K_XL*" \
    --token "hf_ADD_YOUR_HUGGING_FACE_TOKEN_HERE"
```


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
