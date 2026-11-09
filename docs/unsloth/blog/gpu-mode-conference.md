> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/blog/gpu-mode-conference.md).

# GPU Mode - Reinforcement Learning Mini Conference 2026

Slides to our PyTorch Conference 2025 Talks.

Unsloth GitHub for efficient GRPO / GSPO with lots of custom kernel work: <https://github.com/unslothai/unsloth>

Here are our attached PDF slides:

{% file src="/files/XP2Q9dkkXqKuDEMO1gdo" %}

### Reinforcement Learning Resources

For step-by-step guides, beginner or advanced tutorials, you can refer to our docs for:

{% columns %}
{% column width="50%" %}
{% content-ref url="/pages/vT6jTKG1LCfN7HoJ4fVR" %}
[Reinforcement Learning](/docs/get-started/reinforcement-learning-rl-guide.md)
{% endcontent-ref %}

{% content-ref url="/pages/PVxTK4Eal3B77LmfhdRU" %}
[RL Reward Hacking](/docs/get-started/reinforcement-learning-rl-guide/advanced-rl-documentation/rl-reward-hacking.md)
{% endcontent-ref %}
{% endcolumn %}

{% column width="50%" %}
{% content-ref url="/pages/P9PfsQ0BjnZuwPaXA93E" %}
[Advanced RL Docs](/docs/get-started/reinforcement-learning-rl-guide/advanced-rl-documentation.md)
{% endcontent-ref %}

{% content-ref url="/pages/wQboNZf1ZtBJ9Qk4WQxb" %}
[FP16 vs BF16 for RL](/docs/get-started/reinforcement-learning-rl-guide/advanced-rl-documentation/fp16-vs-bf16-for-rl.md)
{% endcontent-ref %}
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column width="50%" %}
{% content-ref url="/pages/pFyRT83vVFiXANdxamCs" %}
[FP8 RL](/docs/get-started/reinforcement-learning-rl-guide/fp8-reinforcement-learning.md)
{% endcontent-ref %}
{% endcolumn %}

{% column width="50%" %}
{% content-ref url="/pages/aV6S9cmDmSv5ky4ZCo5d" %}
[Vision RL](/docs/get-started/reinforcement-learning-rl-guide/vision-reinforcement-learning-vlm-rl.md)
{% endcontent-ref %}
{% endcolumn %}
{% endcolumns %}

### Live Video Recording

{% embed url="<https://www.youtube.com/watch?v=jMSCJZAEYR8>" %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/blog/gpu-mode-conference.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
