> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/browser-use.md).

# Browser Use with Local LLMs

Use local models to navigate websites and complete tasks in the built-in browser.

Browser use lets local LLMs navigate websites and complete tasks for you, in a browser you can watch beside your chat. In the open-source [Unsloth Desktop](/docs/desktop.md) app for macOS, Windows and Linux, any tool-calling model can open pages, click buttons, fill out forms and read documents like PDFs, while vision models can also inspect screenshots.

{% columns %}
{% column %}
&#x20;This guide shows how to set up browser use with local models and give them web tasks.

Unsloth asks for your approval before sign-ins, form submissions, purchases or downloads, and you can set permissions for each website. You can also connect it to any cloud or API model.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FHg3Knjk1GznF8V6R39wk%2Ffour_grid_2x2.gif?alt=media&amp;token=008f7dab-7e91-43cb-a7bd-a8e3bfec29d5" alt=""><figcaption><p>Qwen3.8-27B completing 4 different browser tasks</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

### ⚡ Quickstart

Install Unsloth Desktop to run a local model and let it browse websites beside your chat.

{% stepper %}
{% step %}

#### Download Unsloth

The easiest way to get started is by installing the Unsloth Desktop app. It supports [MacOS](/docs/get-started/install/mac.md), Linux, [Windows](/docs/get-started/install/windows-installation.md), [NVIDIA](/docs/get-started/install/pip-install.md), [AMD](/docs/get-started/install/amd.md), Intel and CPU setups.

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

Or, if you prefer manual installation:

{% tabs %}
{% tab title="Native install" %}
**MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

{% endtab %}

{% tab title="Docker" %}
The [Unsloth Docker image](https://hub.docker.com/r/unsloth/unsloth) `unsloth/unsloth` is available on Docker. [Read guide.](https://unsloth.ai/docs/get-started/install/docker)
{% endtab %}

{% tab title="Homebrew" %}
Install Unsloth Desktop:

{% code collapsedlinecount="10" %}

```bash
brew install --cask unsloth
```

{% endcode %}

Update Unsloth Desktop:

```bash
brew upgrade --cask unsloth
```

{% endtab %}

{% tab title="WinGet" %}
Install Unsloth Desktop:

```powershell
winget install --id UnslothAI.Unsloth -e
```

Update Unsloth Desktop:

```powershell
winget upgrade --id UnslothAI.Unsloth -e
```

{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}

#### Install

1. Open the Unsloth installer (`.dmg`, `.exe` files)
2. Drag Unsloth to Applications for Mac or complete setup for Windows.
3. Launch the app and wait for installation to complete
   {% endstep %}

{% step %}

#### Choose a model

Open Model Hub or the Select model dropdown. Choose a model that supports tool calling and a quantization that fits your device, then download and load it.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNCEVgKLJI0goPqjgcg9B%2Fmodel%20hub%20models.png?alt=media&amp;token=533b5e3c-a901-4b33-963e-4a703cc9d5a6" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Start browsing

Open the **+** menu beside the chat input and enable **Browser use**. Try this prompt:

```
Open https://kenney.nl/assets and find three asset packs
for a small pirate-island game: environments, characters
and UI.

Open each pack’s page. Share its name, link and a short
explanation of how we could use it. Check the listed
license. Don’t download anything.
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQXmNUrzvl9pRbNBbbEWI%2FUI%20pack%20adventure.gif?alt=media&amp;token=76426c04-5aeb-4c4b-a158-bdccc26fc5b3" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

### Browse with your model

Give your model a website and a task. It can read pages, follow links and interact with buttons, forms and other controls. For clearer navigation, refer to visible labels: “Open Pricing, then select Annual billing.”

**Annotations** allow you to ask about specific parts of a page. Select **Request edits**, highlight the content and add a question or instruction. The selection is sent to the model in chat.

#### Continue your task

You can ask follow-up questions in the same chat. After finding the asset packs, try:

```
Which of these packs would work best for a top-down game?
Compare their styles and suggest what else we might need.
```

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fj0521NE4P44p74DzHTGJ%2Fimage.png?alt=media&amp;token=2f58f4e8-5e9b-4f11-a988-01f6ad913470" alt="" width="563"><figcaption></figcaption></figure></div>

It helps to be specific about what you’d like checked. You can ask the model to compare options, check details on another page or explain how it reached its answer.

#### Work with visual content

Models with vision support can inspect screenshots of images, charts and other content that page text doesn’t capture. Models without vision can still use page text, links and controls, but cannot inspect the images themselves.

Ask the model to open or enlarge the content you want it to inspect. For example:

```
Can you navigate the Kenney assets and share a screenshot
of the enlarged preview image on the Pirate Kit page?
```

The model can navigate to the pack’s page, open its preview and take a screenshot. Expand the `browser_screenshot` tool call to see the exact image it captured.&#x20;

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FA2D4w7KXmfWBzHzqCneJ%2Fimage.png?alt=media&amp;token=c3e9f395-7d9b-41f6-ab8a-e0b6fd868ea9" alt="" width="563"><figcaption></figcaption></figure></div>

You can then ask follow-up questions about the image or request a closer look at a specific area.

### Control the browser

Watch the model work beside your chat. If you need to handle a step yourself, select **Stop**, complete it in the browser and ask the model to continue.

To disable browser use, click the **Browser** indicator beside the chat input.

#### Approve actions

When approval is needed, the browser shows a request with **Allow** and **Deny** buttons.

By default, Unsloth asks before submitting forms, signing in or taking actions such as sending, buying or deleting. It may also ask before opening a new website.

Enter passwords and payment details yourself. The standard browser tools cannot fill these fields or upload files.

#### Set website permissions

Open Settings and select **Browser**. Under **Agent permissions**, choose defaults or add exceptions for individual websites.

| Setting           | What it controls                                                               |
| ----------------- | ------------------------------------------------------------------------------ |
| Browsing          | Which websites the model can visit.                                            |
| Actions           | Approval for sign-ins, form submissions and actions such as sending or buying. |
| Downloads         | Whether downloads are allowed, need approval or are blocked.                   |
| Unlabelled clicks | Clicks and drags on areas without a named control, such as a canvas.           |

#### History and Select a passagescripts

You can choose whether the model can read your Unsloth browsing history. Set it to ask first, always allow or never allow.

Scripts need approval each time. You’ll see the script before it runs. To disable them, set **Run scripts** to **Never**.

Full access skips several approval prompts, including history requests unless history access is set to **Never**. Blocked sites and downloads remain blocked, and scripts still need approval.

### <i class="fa-file">:file:</i> Work with files beside your chat

You can also use the browser panel to edit and browse PDFs, Office documents, HTML and text files.

Open Settings, select **Browser** and enable **Open files in the browser**. Click a supported attachment to open it beside your conversation.

To ask about a specific passage or suggest a change, select **Request edits**, highlight the passage and tell your model what you’d like it to do. Your request goes to the model in chat.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FkjknhKM8DGLjafiEwfHS%2Fimage.png?alt=media&amp;token=f6fd67d0-490e-46e8-b52a-3503b395c90a" alt="" width="563"><figcaption></figcaption></figure></div>

As you read, ask your model to summarize the file, explain a section or find a detail. To ask about a specific passage or suggest an edit, select **Request edits** and highlight the text you mean.

The compatible file types are as follows:&#x20;

| File type      | Extension |
| -------------- | --------- |
| PDF            | `.pdf`    |
| Word documents | `.docx`   |
| Spreadsheets   | `.xlsx`   |
| Presentations  | `.pptx`   |
| Markdown       | `.md`     |
| HTML           | `.html`   |
| Plain text     | `.txt`    |

**Troubleshooting**

<details>

<summary>Browser use is unavailable</summary>

Choose a model that supports tool calling and open the regular chat view. Browser use isn’t available in mobile or comparison layouts. Enable **Browser use** from the **+** menu beside the chat input.

</details>

<details>

<summary>The model describes actions without taking them</summary>

Check that **Browser use** is enabled. Try asking for one concrete action, such as “Open this URL and read the page title.” Tool-calling reliability can vary between models.

</details>

<details>

<summary>A website or part of a page doesn’t work</summary>

Some websites and embedded content may not work with the browser tools. If the model cannot find a control, describe its visible label or location. For visual content, try a vision-capable model.

You can also select **Stop**, complete the step manually if possible, then ask the model to continue.

</details>

<details>

<summary>An action is waiting for approval</summary>

Check the browser panel for an approval request and select **Allow** or **Deny**. If the request has timed out, ask the model to try again when you’re ready to review it.

</details>

<details>

<summary>A local page won’t open</summary>

Browser use supports public HTTP and HTTPS websites. Localhost, private-network addresses and `file://` URLs aren’t supported as navigation targets. To view a supported attachment, enable **Open files in the browser** under **Settings → Browser**, then click the attachment.

</details>

<details>

<summary>The model cannot access another browser tab</summary>

The model works in its own Unsloth browser tab. It cannot control tabs in Chrome, Firefox or other browsers. Copy the page’s URL into the chat and ask the model to open it in Unsloth.

</details>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/browser-use.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
