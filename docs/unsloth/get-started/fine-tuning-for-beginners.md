> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners.md).

# Fine-tuning for Beginners

If you're a beginner, here might be the first questions you'll ask before your first fine-tune. You can also always ask our community by joining our [Reddit page](https://www.reddit.com/r/unsloth/).

<table data-view="cards"><thead><tr><th data-type="content-ref"></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td><a href="/docs/models/tutorials.md">Complete LLM Directory</a></td><td>See every model you can run / train with Unsloth.</td><td>How to run GGUFs or train LLMs?</td><td><a href="/docs/models/tutorials.md">Complete LLM Directory</a></td></tr><tr><td><a href="/docs/get-started/fine-tuning-llms-guide.md">Fine-tuning Guide</a></td><td>Step-by-step on how to fine-tune!</td><td>Learn the core basics of training.</td><td><a href="/docs/get-started/fine-tuning-llms-guide.md">Fine-tuning Guide</a></td></tr><tr><td><a href="/docs/get-started/fine-tuning-llms-guide/what-model-should-i-use.md">What Model Should I Use?</a></td><td>Instruct or Base Model?</td><td>How big should my dataset be?</td><td><a href="/docs/get-started/fine-tuning-llms-guide/what-model-should-i-use.md">What Model Should I Use?</a></td></tr><tr><td><a href="/docs/get-started/fine-tuning-for-beginners/faq-+-is-fine-tuning-right-for-me.md">FAQ + Is Fine-tuning Right For Me?</a></td><td>What can fine-tuning do for me?</td><td>RAG vs. Fine-tuning?</td><td><a href="/docs/get-started/fine-tuning-for-beginners/faq-+-is-fine-tuning-right-for-me.md">FAQ + Is Fine-tuning Right For Me?</a></td></tr><tr><td><a href="/docs/get-started/install.md">Installation</a></td><td>How do I install Unsloth locally?</td><td>How to update Unsloth?</td><td><a href="/docs/get-started/install.md">Installation</a></td></tr><tr><td><a href="/docs/get-started/fine-tuning-llms-guide/datasets-guide.md">Datasets Guide</a></td><td>How do I structure/prepare my dataset?</td><td>How do I collect data?</td><td></td></tr><tr><td><a href="/docs/get-started/fine-tuning-for-beginners/unsloth-requirements.md">Unsloth Requirements</a></td><td>Does Unsloth work on my GPU?</td><td>How much VRAM will I need?</td><td><a href="/docs/get-started/fine-tuning-for-beginners/unsloth-requirements.md">Unsloth Requirements</a></td></tr><tr><td><a href="/docs/basics/inference-and-deployment.md">Inference &amp; Deployment</a></td><td>How do I save my model locally?</td><td>How do I run my model via Ollama or vLLM?</td><td><a href="/docs/basics/inference-and-deployment.md">Inference &amp; Deployment</a></td></tr><tr><td><a href="/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide.md">Hyperparameters Guide</a></td><td>What happens when I change a parameter?</td><td>What parameters should I change?</td><td></td></tr></tbody></table>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-559e7890f607e34fd6004517296e65e942c93b41%2FLarge%20sloth%20Question%20mark.png?alt=media" alt="" width="188"><figcaption></figcaption></figure>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/fine-tuning-for-beginners.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
