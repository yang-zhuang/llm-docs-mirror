> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/unsloth-environment-flags.md).

# Unsloth Environment Flags

Advanced flags which might be useful if you see breaking finetunes, or you want to turn stuff off.

<table><thead><tr><th width="397.4666748046875">Environment variable</th><th>Purpose</th><th data-hidden></th></tr></thead><tbody><tr><td><code>os.environ["UNSLOTH_RETURN_LOGITS"] = "1"</code></td><td>Forcibly returns logits - useful for evaluation if logits are needed.</td><td></td></tr><tr><td><code>os.environ["UNSLOTH_COMPILE_DISABLE"] = "1"</code></td><td>Disables auto compiler. Could be useful to debug incorrect finetune results.</td><td></td></tr><tr><td><code>os.environ["UNSLOTH_DISABLE_FAST_GENERATION"] = "1"</code></td><td>Disables fast generation for generic models.</td><td></td></tr><tr><td><code>os.environ["UNSLOTH_ENABLE_LOGGING"] = "1"</code></td><td>Enables auto compiler logging - useful to see which functions are compiled or not.</td><td></td></tr><tr><td><code>os.environ["UNSLOTH_FORCE_FLOAT32"] = "1"</code></td><td>On float16 machines, use float32 and not float16 mixed precision. Useful for Gemma 3.</td><td></td></tr><tr><td><code>os.environ["UNSLOTH_STUDIO_DISABLED"] = "1"</code></td><td>Disables extra features.</td><td></td></tr><tr><td><code>os.environ["UNSLOTH_COMPILE_DEBUG"] = "1"</code></td><td>Turns on extremely verbose <code>torch.compile</code>logs.</td><td></td></tr><tr><td><code>os.environ["UNSLOTH_COMPILE_MAXIMUM"] = "0"</code></td><td>Enables maximum <code>torch.compile</code>optimizations - not recommended.</td><td></td></tr><tr><td><code>os.environ["UNSLOTH_COMPILE_IGNORE_ERRORS"] = "1"</code></td><td>Can turn this off to enable fullgraph parsing.</td><td></td></tr><tr><td><code>os.environ["UNSLOTH_FULLGRAPH"] = "0"</code></td><td>Enable <code>torch.compile</code> fullgraph mode</td><td></td></tr><tr><td><code>os.environ["UNSLOTH_DISABLE_AUTO_UPDATES"] = "1"</code></td><td>Forces no updates to <code>unsloth-zoo</code></td><td></td></tr></tbody></table>

Another possibility is maybe the model uploads we uploaded are corrupted, but unlikely. Try the following:

```python
model, tokenizer = FastVisionModel.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct",
    use_exact_model_name = True,
)
```


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/unsloth-environment-flags.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
