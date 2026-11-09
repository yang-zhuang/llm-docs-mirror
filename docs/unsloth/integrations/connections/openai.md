> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/integrations/connections/openai.md).

# Connect OpenAI to Unsloth: Run GPT Models in Local Chat

Learn how to connect OpenAI models, including GPT-5.5 to [Unsloth](https://github.com/unslothai/unsloth) so you can chat with all of them in an open-source local UI chat interface. By connecting your OpenAI API key, you can run GPT models inside Unsloth with features like [web search](#web-search-and-thinking), tool-calling, [code execution](#code-execution), [image generation](#image-generation), reusable code containers, and [prompt caching](#prompt-caching).

You can also connect your ChatGPT/Codex subscription directly to Unsloth.

This guide walks you through creating an OpenAI API key, connecting OpenAI as a provider, loading available models, and troubleshooting common setup issues.

### Setup

{% stepper %}
{% step %}

#### Create an OpenAI API key

Create an API key from the [OpenAI dashboard](https://platform.openai.com/api-keys).

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNbLWLZa1OBYQrwX0mQVv%2Funsloth_openai_api.gif?alt=media&amp;token=28187d50-8638-4e60-ba33-729efd13f1c1" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Configure Connections

Next, connect your provider to Unsloth.

1. Open **Settings** → **Connections**, then click **Add Connection.**
2. Select the OpenAI, then paste the API key you copied earlier.
3. Click **Reload Models** to refresh the list with models available to your account.
4. Choose the models you want to enable, then hit save.&#x20;

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FlAXYV1wS2lxeS36Lo8Dj%2Fexport-1779457818713.gif?alt=media&amp;token=99c6f0b2-2fb1-40e4-a15a-325bcef8c2f7" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Ready to Chat

The models you enabled will now appear under Connected in the Select Model dropdown. Supported GPT models can expose extra controls including image generation, thinking, web search and code execution.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FgKCJ3zsZzZuDqBAigsfG%2FScreenshot%202026-05-26%20at%201.31.03%E2%80%AFAM.png?alt=media&amp;token=c8df4285-ba69-4091-8978-e4197f6a12d2" alt=""><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### Code Execution

When enabled, supported OpenAI models can run code in a provider sandbox to solve problems, analyse data, and work with files.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fn65DzRsTGrflcqJBv67y%2FScreenshot%202026-05-26%20at%206.11.54%E2%80%AFAM.png?alt=media&amp;token=f620e467-2202-4843-ae16-e169a89f0a57" alt="" width="563"><figcaption></figcaption></figure>

{% columns %}
{% column width="50%" %}
OpenAI uses reusable shell containers. In **Code Execution** settings, you can set the idle timeout, create containers, select the active container, refresh the list, or delete old containers.

Select the same container in a new thread to continue with its files and state.
{% endcolumn %}

{% column width="50%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FBR0zCMzeC4IwPSmlx12A%2Fimage.png?alt=media&amp;token=3d9e80ee-4ceb-4454-9620-165650a29c0a" alt="" width="288"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

### Prompt Caching

{% columns %}
{% column width="66.66666666666666%" %}
Prompt caching reduces latency and cost when requests reuse the same long prefix. It is supported for compatible providers and servers, including OpenAI. Use the **Prompt caching** setting in the side panel to control caching behaviour for supported connections.
{% endcolumn %}

{% column width="33.33333333333334%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FKA6iU3qCFhUiq0KI16aU%2FScreenshot%202026-05-26%20at%203.28.44%E2%80%AFAM.png?alt=media&amp;token=41a43794-792d-48f4-8774-8b9d85702dfc" alt=""><figcaption></figcaption></figure>

{% endcolumn %}
{% endcolumns %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fq4csmTX5rS9isMkNkhTX%2FPrompt%20Caching%20Diagram%20(1).png?alt=media&amp;token=ade433bf-5eaf-4146-a266-525a85a6c98d" alt="" width="375"><figcaption></figcaption></figure>

### Web Search & Thinking

Provider-side web search is available for supported models from OpenAI. The **Think** control adapts to the selected model: some models use an on/off toggle, while reasoning-effort models use model specific thinking levels.&#x20;

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FC0Ed4kzN9h6c0ogEn6NT%2Fwebsearch%20api.png?alt=media&amp;token=d3335222-1d9e-4021-9bf9-734c6acf1fc0" alt="" width="563"><figcaption></figcaption></figure></div>

### Image Generation

Just like GPT, Unsloth also supports image generation. You can directly edit an image by clicking the “Edit Image” button and entering a new prompt to refine or regenerate it. Images are generated automatically when requested, but you can toggle this behavior off. A download button is also available, allowing you to save the image in its original full resolution.

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F5ZLU2BY19MN4yiYLx2Br%2FScreenshot%202026-05-26%20at%206.04.34%E2%80%AFAM.png?alt=media&amp;token=44327a8f-c14d-4541-9a02-f19f375b4326" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FDQ1bJ5KF8CiyItrfOrIt%2FScreenshot%202026-05-26%20at%206.06.07%E2%80%AFAM.png?alt=media&amp;token=ff6b00bc-0a2f-4375-a454-49429cf839f2" alt=""><figcaption></figcaption></figure></div>

### Troubleshooting

If OpenAI fails to connect, check that the API key is valid and belongs to the correct OpenAI account.

If a model does not appear after clicking **Load Models**, it may not be available for your account. You can enter the model ID manually or choose another model.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/integrations/connections/openai.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
