> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/install/amd/amd-hackathon.md).

# AMD AI Reinforcement Learning Hackathon with Unsloth

​​Learn hands-on techniques for ​Reinforcement Learning for AI models with Unsloth from Daniel Han, the creator of Unsloth.

You can view Unsloth's GitHub repo here: <https://github.com/unslothai/unsloth>

Here is the link to our AMD fine-tuning notebooks:

{% embed url="<https://github.com/unslothai/notebooks/blob/main/nb/gpt_oss_(20B)_Reinforcement_Learning_2048_Game_BF16.ipynb>" %}

<https://github.com/unslothai/notebooks/blob/main/nb/gpt_oss_(20B)_Reinforcement_Learning_2048_Game_BF16.ipynb>

{% code overflow="wrap" %}

```bash
wget 'https://raw.githubusercontent.com/unslothai/notebooks/refs/heads/main/nb/gpt_oss_(20B)_Reinforcement_Learning_2048_Game_BF16.ipynb'
```

{% endcode %}

If wanting to upgrade Unsloth / Unsloth Zoo:

{% code overflow="wrap" %}

```bash
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm7.0 --upgrade --force-reinstall

pip uninstall unsloth unsloth_zoo -y && \
    pip install git+https://github.com/unslothai/unsloth-zoo git+https://github.com/unslothai/unsloth --no-deps --force-reinstall --no-cache-dir
```

{% endcode %}

For bitsandbytes:

```bash
pip install "unsloth[amd] @ git+https://github.com/unslothai/unsloth"
```

If you see:

{% code overflow="wrap" %}

```
error: Failed to install: bitsandbytes-1.33.7rc0-py3-none-manylinux_2_24_x86_64.whl (bitsandbytes==1.33.7rc0 (from https://github.com/bitsandbytes-foundation/bitsandbytes/releases/download/continuous-release_main/bitsandbytes-1.33.7.preview-py3-none-manylinux_2_24_x86_64.whl)) Caused by: Wheel version does not match filename (0.49.2.dev0 != 1.33.7rc0), which indicates a malformed wheel. If this is intentional, set UV_SKIP_WHEEL_FILENAME_CHECK=1.
```

{% endcode %}

Do NOT use UV\_SKIP\_WHEEL\_FILENAME\_CHECK, instead ONLY use `pip install "unsloth[amd] @ git+https://github.com/unslothai/unsloth"` (NOT uv) since uv destroys bitsandbytes. Maybe add a check to the PRs if possible to catch these.

For AMD installation instructions, you can view our guide here:

{% content-ref url="/pages/GUxDmG8LaAiQinraCXCr" %}
[AMD](/docs/get-started/install/amd.md)
{% endcontent-ref %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/install/amd/amd-hackathon.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
