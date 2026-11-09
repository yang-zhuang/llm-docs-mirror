> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/integrations/connections/anthropic-claude.md).

# Connect Anthropic to Unsloth: Run Claude Models in Local Chat

Connect the Anthropic API to [Unsloth](https://github.com/unslothai/unsloth) to chat with Claude models including Claude Opus 4.7 directly alongside your local models in an open-source UI chat interface. This guide shows you how to create an Anthropic API key, add Anthropic as a provider in Unsloth, load Claude LLMs, and start chatting.

Supported Claude models in Unsloth can also access advanced features such as thinking, [web search](#web-search-and-thinking), Anthropic [code execution](#code-execution), and [prompt caching](#prompt-caching) to improve cost effiencey.

### Setup

{% stepper %}
{% step %}

#### Create an Anthropic API key

Create an API key from the [Anthropic Console](https://console.anthropic.com/settings/keys). Copy the key. You will paste it into Unsloth in the next step.
{% endstep %}

{% step %}

#### Connect Anthropic to Unsloth

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FSzJ57mYBpBCavIKyksDy%2Fclaude_studio_api.gif?alt=media&amp;token=bd7b7da5-bb25-4f9d-bfb8-b63602c1f082" alt="" width="563"><figcaption></figcaption></figure>

Next, connect Anthropic to Unsloth.

1. Open **Settings** → **Connections**, then click **Add Connection.**
2. Select the provider you want to add, then paste the API key you copied earlier.
3. Click **Reload Models** to refresh the list with models available to your account.
4. Choose the models you want to enable, then hit save.&#x20;
   {% endstep %}

{% step %}

#### Ready to Chat

After saving the connection, select a Claude model under **Connected** in the model dropdown. Supported Claude models can expose extra controls including image generation, thinking, web search and code execution.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FpOMKHdhunTepcJSvf8pA%2Fimage.png?alt=media&amp;token=ca454678-a98b-4edb-b407-beeb879b4f76" alt="" width="337"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### Code Execution

When enabled, supported Claude models can run code in Anthropic’s provider sandbox to solve problems, analyze data, and work with files. Claude uses Anthropic’s Code execution tool. Code execution appears in the response timeline as tool activity, alongside other tool calls.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F4W9Zq684jCgJy9kGvrkk%2FScreenshot%202026-05-26%20at%206.10.12%E2%80%AFAM.png?alt=media&amp;token=c7b6a106-1a22-4120-a22d-f9ad8a9471c7" alt="" width="563"><figcaption></figcaption></figure>

### Prompt Caching

{% columns %}
{% column width="66.66666666666666%" %}
Prompt caching reduces latency and cost when requests reuse the same long prefix. It is supported for compatible providers and servers, including Anthropic models. Use the **Prompt caching** setting in the side panel to control caching behavior for supported connections.
{% endcolumn %}

{% column width="33.33333333333334%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FKA6iU3qCFhUiq0KI16aU%2FScreenshot%202026-05-26%20at%203.28.44%E2%80%AFAM.png?alt=media&amp;token=41a43794-792d-48f4-8774-8b9d85702dfc" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fq4csmTX5rS9isMkNkhTX%2FPrompt%20Caching%20Diagram%20(1).png?alt=media&amp;token=ade433bf-5eaf-4146-a266-525a85a6c98d" alt="" width="375"><figcaption></figcaption></figure>

### Web Search & Thinking

Supported Claude models can use provider-side web search. The **Think** control appears when the selected model supports thinking. Depending on the model, this may expose different thinking levels or availability.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FC0Ed4kzN9h6c0ogEn6NT%2Fwebsearch%20api.png?alt=media&amp;token=d3335222-1d9e-4021-9bf9-734c6acf1fc0" alt="" width="563"><figcaption></figcaption></figure>

The **Think** control adapts to the selected model: some models use an on/off toggle, while reasoning-effort models use model specific thinking levels.&#x20;

### Troubleshooting

If Anthropic API fails to connect, check that the API key is valid and belongs to the correct Anthropic account.

If a model does not appear after clicking **Load Models**, it may not be available for your account. You can enter the model ID manually or choose another model.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/integrations/connections/anthropic-claude.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
