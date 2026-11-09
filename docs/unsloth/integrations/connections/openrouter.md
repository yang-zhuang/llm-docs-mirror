> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/integrations/connections/openrouter.md).

# How to Connect OpenRouter to Unsloth: API Key & Model Setup

This guide explains how to connect **OpenRouter to** [**Unsloth**](https://github.com/unslothai/unsloth) so you can access hosted AI models from providers like **OpenAI, Anthropic,** and **Google** through an open-source local UI chat interface. You’ll learn how to create an OpenRouter API key, add OpenRouter as a provider in Unsloth, load or manually enter model IDs, and enable external models for chat.

Once a single API key is connected, OpenRouter models in Unsloth can provide advanced features such as thinking, web search, tool calling, code execution, and customizable generation settings directly from the chat page.

### Setup

{% stepper %}
{% step %}

#### Create an OpenRouter API key

Sign in to your OpenRouter account. Create an API key from the [OpenRouter dashboard](https://openrouter.ai/settings/keys):

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FumQXaeZGAQ8f3hMQSQQY%2Fimage.png?alt=media&amp;token=51ec273d-4271-4683-8cf2-0fb11bccb1ba" alt="" width="563"><figcaption></figcaption></figure>

Copy the key. You will paste it into Unsloth in the next step.

When creating the key, you can optionally set a credit limit or expiration date.
{% endstep %}

{% step %}

#### Connect OpenRouter to Unsloth

Open **Settings → Connections**, then click **Add Connected**.

Select **OpenRouter**, then enter your connection details.

Enter your OpenRouter details:

* **API key:** paste your OpenRouter API key

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FB9fDpRnYfDjhCI5yDoon%2Fimage.png?alt=media&amp;token=97ecc7e3-a3fe-4cd8-a5c6-738c9de7fbf3" alt="" width="375"><figcaption></figcaption></figure>

* **Model IDs:** click **Load Models**, or enter model IDs manually

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F59F88IYS0BzteOqcavUj%2Fimage.png?alt=media&amp;token=72632261-b3cd-486c-b4dd-09b56fa3a58a" alt="" width="375"><figcaption></figcaption></figure>

Finally, click **Add Connection**.&#x20;
{% endstep %}

{% step %}

#### Ready to Chat

After saving the connection, select an OpenRouter model under **Connected** in the model dropdown.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFFvSXoLCnvydwmTgS7Ru%2Fimage.png?alt=media&amp;token=79ca30bb-e049-4106-8b98-0871f79dfba5" alt="" width="337"><figcaption></figcaption></figure>

OpenRouter models can expose different controls depending on the upstream model, including web search, thinking, tool-calling, and generation settings.
{% endstep %}
{% endstepper %}

### Model Selection

OpenRouter provides access to many models from different providers. If **Load Models** does not return the models you want to select, enter the model IDs you want enabled.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQM4eHEcNpWQazKtyS06X%2Fimage.png?alt=media&amp;token=8774a4a0-7d00-4888-9e03-72c0e8641533" alt="" width="563"><figcaption></figcaption></figure>

Example model IDs:

```
openai/gpt-5.5 
anthropic/claude-sonnet-4.6 
google/gemini-3-pro
```

### Troubleshooting

If OpenRouter fails to connect, check that the API key is valid and belongs to the correct OpenRouter account.

If a model does not appear after clicking **Load Models**, it may not be available for your account or region. You can enter the model ID manually or choose another model.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/integrations/connections/openrouter.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
