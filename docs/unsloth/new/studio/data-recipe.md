> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/new/studio/data-recipe.md).

# Unsloth Data Recipes

Learn how to create, build and edit datasets with Unsloth Studio's Data Recipes.

Unsloth Studio's Data Recipes lets you upload documents like PDFs or CSVs files and transforms them into useable / synthetic datasets. Create and edit datasets visually via a graph-node workflow. This guide will get you started with the basics before you dive into Unsloth Data Recipes.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQ6e19jESrJg0VjHnX58c%2Fdata%20recipes%20final.png?alt=media&amp;token=8d74e453-815d-4790-83d1-76d0bc80a3ce" alt=""><figcaption></figcaption></figure></div>

### How Data Recipes works

Data Recipes follows the same basic path. You open the recipes page, create or pick a recipe, build the workflow in the editor, validate it run a preview, then run the full dataset once the output looks right. Add seed data and generation blocks, validate the workflow, preview sample output, then run a full dataset build. Unsloth Data Recipes is powered by **NVIDIA Nemo** [**Data Designer**](https://github.com/NVIDIA-NeMo/DataDesigner).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fc5m3JX1kUA3UwmdcJcxH%2FArea.gif?alt=media&amp;token=33bbd908-7d6c-456a-bc58-ce495c0adca1" alt=""><figcaption><p>Example of generating dataset and fine-tuning a model</p></figcaption></figure></div>

At a glance a usual workflow should look like this:

1. Open the recipes page.
2. Create a new recipe or open an existing one.
3. Add blocks to define your dataset workflow.
4. Click **Validate** to catch configuration issues early.
5. Run a preview to inspect sample rows quickly.
6. Run a full dataset build when the recipe is ready.
7. Review progress and output live in graph or in **Executions** view for mode details.
8. Select the resulting dataset in **Unsloth** and fine tune a model.

### Get Started

The recipes page is the main entry point. Recipes are stored locally in the browser, so you come back to saved work later. From here, you can create a blank recipe or open a guided learning recipe.

{% hint style="info" %}
Recipes can be exported and imported, so it is easy to share workflows with other Unsloth users :tada:. If you are trying to build a specific dataset pattern, ask in Unsloth Discord. Someone may already have a recipe they can share.
{% endhint %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FAwKh7speKv3eXERFhPg2%2FScreenshot%202026-03-13%20at%2008.26.11.png?alt=media&amp;token=809ac83f-75c8-4ef2-9721-65971b3faaa5" alt="" width="563"><figcaption><p>Recipes landing page</p></figcaption></figure></div>

If you are new to concept of workflows, learning recipes are the fastest way to see how seed data, prompts, expressions, and validators fit together in one working example. If you already know the shape of dataset you want, starting empty is usually quicker.

#### Choose a starting path

<table><thead><tr><th>If you want to:</th><th>Start with:</th><th data-hidden></th></tr></thead><tbody><tr><td><sub><strong>Build a custom workflow quickly</strong></sub></td><td><sub><strong>Start Empty</strong></sub></td><td></td></tr><tr><td><sub><strong>Learn the product from an example</strong></sub></td><td><sub><strong>Start from Learning Recipe</strong></sub></td><td></td></tr><tr><td><sub><strong>Continue previous work</strong></sub></td><td><sub><strong>Open a saved recipe</strong></sub></td><td></td></tr></tbody></table>

### What you build in the editor

The editor is where the recipe takes shape. You add blocks from the block sheet, configure them in dialogs, connect them on the canvas, and then validate or run the workflow.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F6A2uN85dkYAdP7v0eUyX%2Fworkflow.gif?alt=media&amp;token=b44d9682-1825-4ddb-88f6-485a2aea3359" alt="" width="563"><figcaption><p>Example of building product description workflow</p></figcaption></figure></div>

{% columns %}
{% column %}
The editor has a few core parts:

* The recipe header, where you rename the recipe and switch between **Editor** and **Executions**
* The canvas, where the recipe graph is shown
* The block sheet, where you add new blocks
* Configuration dialogs, where you define prompts, references, model aliases, validators and seed settings.
* The floating **Run** and **Validate** controls
* need to add more here

{% endcolumn %}

{% column %}
The most common blocks in reciper are:

* **Seed** for input data from hugginface, local structured files (or unstructured documents that get chunked into rows.
* **LLM + Models** for providers, model configs, LLM generation blocks, and shared tool profiles.
* **Expression** for jinja2-based transforms that do not require an LLM call.
* **Validators** for filtering bad generated code with built in linters for Python, SQL, and Javascript/Typescript.
* **Samplers** for deterministic columns such as categories and subcategories.
  {% endcolumn %}
  {% endcolumns %}

### How references work

Most blocks that produce data (with some exceptions) becomes a reference for later blocks. That is one of the main ideas behind Data Recipes. You create a value once, then reuse it in prompts, expressions, structured outputs, and validation steps.

{% hint style="info" %}
Jinja Expressions help you work with values that arleady exist in the recipe. You can reference nested fields like `{{customer.first_name}}` , join values like `{{customer.first_name}} {{customer.last_name}}` and add conditional logic with patterns such as `{% if condition %}...{% endif %}`&#x20;
{% endhint %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNJYWKeIDC6aqgT2dShsB%2FScreenshot%202026-03-13%20at%2010.06.14.png?alt=media&amp;token=9d20bb8c-8a25-4395-9616-6429021d76f0" alt="" width="563"><figcaption><p>Example of references shown in the editor</p></figcaption></figure></div>

For example:

* A category block named `domain` can be references as `{{ domain }}`
* a seed column can be used directly in an LLM prompt, the columns in your seed data (eg. HF dataset columns, csv)
* a structured LLM output can expose fileds for later prompts
* an expression block can combine earlyier values without another model call

### What happens after?

Preview runs are for quick iteration. They return sample rows and analysis in the editor so you can inspect the generated data before commiting to a full run.

Full runs create a persisted local dataset artifact. That output later appears in Unsloth's local dataset picker, where you can inspect it again and use it for fine-tuning. Optionally you can publish your dataset to you hugginface repo.

### Core building blocks

{% columns %}
{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FuphMi76re2aUX7JvFNce%2FScreenshot%202026-03-13%20at%2011-35-45%20Unsloth%20Studio.png?alt=media&amp;token=674eb5ef-5acb-4b32-ab85-11a2af2e210f" alt="" width="188"><figcaption><p>Core building blocks</p></figcaption></figure></div>
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FsdoYKdurtGeu4YgVqu0q%2FScreenshot%202026-03-13%20at%2011-38-59%20Unsloth%20Studio.png?alt=media&amp;token=328c7ea6-591e-43fa-9e87-c71277a54736" alt="" width="188"><figcaption><p>Model and LLM blocks</p></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

#### Model setup is split into two usable layers:

* **Model provider** defines the endpoint and authentifcation
* **Model Config** defines the model name and inference settings

This setup works with hosted providers, self-hosted endpoints, `vLLM` , `llama.cpp` , or any OpenAI-compatible API that you run outside Unsloth.

{% hint style="info" %}
Recipes are not limited to one model. You can add multiple **Model providers** and **Model config** blocks, then use different models for different steps, such as one for coding and another for general text tasks.
{% endhint %}

After model setup, you can use Four LLM block types:

| Block          | Output            | Best for                                                    |
| -------------- | ----------------- | ----------------------------------------------------------- |
| LLM Text       | Free-form text    | Instructions, explanations, conversations, and descriptions |
| LLM Structured | JSON              | Output that need fixed fields and predictable structure     |
| LLM Code       | Code              | Python, SQL, Typescript and other code generation tasks     |
| LLM Judge      | Scored evaluation | Grading outputs with one or more user-defined score         |

#### Tool Profiles

{% columns %}
{% column %}
Tool profile blocks defines shared MCP based tool access for one or more LLM blocks. Use them when a generation step needs tools, such as looking up code documentation through `Context7`.

Image to the left shows Context7 MCP added and configured in Tool Profile block dialog:
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fu4GbfrjuQyiU7cN15fDY%2FScreenshot%202026-03-13%20at%2010.50.01.png?alt=media&amp;token=889a9425-bb40-4e41-9dab-5408b03bd3ca" alt="" width="375"><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

#### Validators

{% columns %}
{% column %}
Validor block primarly target LLM code block by running generated code outputs through Linter and syntax validation, this helps you keep bad or invalid code rows out of the final dataset by filtering them out. The built-in options cover Python, SQL, and JavaScript/TypeScript validation.
{% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FobyvYzcfyJkloHfHMyVC%2FScreenshot%202026-03-13%20at%2011-39-08%20Unsloth%20Studio.png?alt=media&amp;token=19c8dbfa-c876-4f6e-9e62-5b8df515dc7b" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

### Validate, preview and run

Once the recipe workflow is in place, the next step is execution. The reccomended pattern is: validate first, preview for quick feedback and inspect the generated data in executions view, then run the full dataset when you feel the output satisfies your plan.

Use the execution controls in third order:

{% stepper %}
{% step %}

#### Validate

Click **Validate** to catch configuration issues.
{% endstep %}

{% step %}

#### Preview

Run a preview to inspect sample rows and analysis
{% endstep %}

{% step %}

#### Refine

Refine prompts, references, seed settings, or validators.

Iterate untill you feel satisfied with generated data
{% endstep %}

{% step %}

#### Run the full dataset build

{% endstep %}
{% endstepper %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFCcEaVt8xsaNsMFi2MoZ%2Funsloth%20chef.png?alt=media&amp;token=0266aa36-4ba7-4364-be59-5fe57936ef7f" alt="" width="188"><figcaption></figcaption></figure>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/new/studio/data-recipe.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
