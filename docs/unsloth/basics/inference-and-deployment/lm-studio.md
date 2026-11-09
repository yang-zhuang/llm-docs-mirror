> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/inference-and-deployment/lm-studio.md).

# Deploying models to LM Studio

Saving models to GGUF so you can run and deploy them to LM Studio

You can run and deploy your fine-tuned LLM directly in LM Studio. [LM Studio](https://lmstudio.ai/) enables easy running and deployment of **GGUF** models (llama.cpp format).

You can use our [LM Studio notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/FunctionGemma_\(270M\)-LMStudio.ipynb) or follow the instructions below:

1. **Export your Unsloth fine-tuned model to `.gguf`**
2. **Import / download the GGUF into LM Studio**
3. **Load it in Chat** (or run it behind an OpenAI-compatible local API)

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FUZEwmNLcs5Oc7bIT7iXV%2Fprefinetune-unsloth.png?alt=media&amp;token=ceb701d3-1f32-406e-a5be-2a7bde4cb4b6" alt="" width="375"><figcaption><p>Before fine-tuning in LM Studio</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FvLEmVH22LQ4hjAA3SGIV%2Fpostfinetune-unsloth.png?alt=media&amp;token=5a473857-6700-4f0a-89c6-0c72c6b507c4" alt="" width="375"><figcaption><p>After fine-tuning in LM Studio</p></figcaption></figure></div>

### 1) Export to GGUF (from Unsloth)

If you already exported a `.gguf`, skip to **Importing into LM Studio**.

```python
# Save locally (creates GGUF artifacts in the folder)
model.save_pretrained_gguf("my_model_gguf", tokenizer, quantization_method = "q4_k_m")
# model.save_pretrained_gguf("my_model_gguf", tokenizer, quantization_method = "q8_0")
# model.save_pretrained_gguf("my_model_gguf", tokenizer, quantization_method = "f16")

# Or push GGUF to the Hugging Face Hub
model.push_to_hub_gguf("hf_username/my_model_gguf", tokenizer, quantization_method = "q4_k_m")
```

{% hint style="info" %}
`q4_k_m` is usually the default for local runs.

`q8_0` is the optimum for near full precision quality.

`f16` is largest / slowest, but original unquantized precision.
{% endhint %}

### 2) Import the GGUF into LM Studio

{% tabs %}
{% tab title="CLI Import (lms import)" %}
LM Studio provides a CLI called `lms` that can import a local `.gguf` into LM Studio’s models folder.

**Import a GGUF file:**

```bash
lms import /path/to/model.gguf
```

**Keep the original file (copy instead of move):**

```bash
lms import /path/to/model.gguf --copy
```

<details>

<summary><strong>Click for more customizable private settings</strong></summary>

**Keep the model where it is (symlink):**

This is helpful for large models stored on a dedicated drive.

```bash
lms import /path/to/model.gguf --symbolic-link
```

**Skip prompts and choose the target namespace yourself:**

```bash
lms import /path/to/model.gguf --user-repo my-user/my-finetuned-models
```

**Dry-run (shows what will happen):**

```bash
lms import /path/to/model.gguf --dry-run
```

</details>

After importing, the model should appear in LM Studio under **My Models**.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FqAgsPwtQv6sSLdRJi6vp%2Flms-modeldirectory-fxngemma.png?alt=media&amp;token=ea11eaed-5684-4a0d-91fc-d540e703a54c" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="From Hugging Face" %}
If you pushed your GGUF repo to Hugging Face, you can download it directly from within LM Studio.

**Option A: Use LM Studio’s in-app downloader**

1. Open LM Studio
2. Go to the **Discover** tab
3. Search for `hf_username/repo_name` (or paste the Hugging Face URL)
4. Download the quant you want (e.g. `Q4_K_M`)

**Option B: Use the CLI downloader**

```bash
# Download from HF by repo name
lms get hf_username/my_model_gguf

# Pick a quantization with @
lms get hf_username/my_model_gguf@Q4_K_M
```

{% endtab %}

{% tab title="Manual Import (folder structure)" %}
If you don’t want to use the CLI, you can place the `.gguf` file into LM Studio’s expected model directory structure.

LM Studio expects models to look like this:

```
~/.lmstudio/models/
└── publisher/
    └── model/
        └── model-file.gguf
```

Example:

```
~/.lmstudio/models/
└── my-name/
    └── my-finetune/
        └── my-finetune-Q4_K_M.gguf
```

Then open LM Studio and check **My Models**.

**Tip:** You can manage / verify your models directory from the **My Models** tab in LM Studio.
{% endtab %}
{% endtabs %}

### 3) Load and chat in LM Studio

1. Open LM Studio → **Chat**
2. Open the **model loader**
3. Select your imported model
4. (Optional) adjust load settings (GPU offload, context length, etc.)
5. Chat normally in the UI

### 4) Serve your fine-tuned model as a local API (OpenAI-compatible)

LM Studio can serve your loaded model behind an OpenAI-compatible API (handy for apps like Open WebUI, custom agents, scripts, etc.).

{% tabs %}
{% tab title="GUI (Developer tab)" %}

1. Load your model in LM Studio
2. Go to the **Developer** tab
3. Start the local server
4. Use the shown base URL (default is typically `http://localhost:1234/v1`)
   {% endtab %}

{% tab title="CLI (lms load + lms server start)" %}

#### 1) List available models

```bash
lms ls
```

#### 2) Load your model (optional flags)

```bash
lms load <model-identifier> --gpu=auto --context-length=8192
```

Notes:

* `--gpu=1.0` means “try to offload 100% to GPU”
* You can set a stable identifier:

```bash
lms load <model-identifier> --identifier="my-finetuned-model"
```

#### 3) Start the server

```bash
lms server start --port 1234
```

{% endtab %}
{% endtabs %}

**Quick test: list models**

```bash
curl http://localhost:1234/v1/models
```

**Python example (OpenAI SDK):**

{% code expandable="true" %}

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",  # LM Studio may not require a real key; this is a common placeholder
)

resp = client.chat.completions.create(
    model="model-identifier-from-lm-studio",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! What did I fine-tune you to do?"},
    ],
    temperature=0.7, # adjust temperature according to your model needs
)

print(resp.choices[0].message.content)
```

{% endcode %}

**cURL example (chat completions):**

{% code expandable="true" %}

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "model-identifier-from-lm-studio",
    "messages": [
      {"role": "user", "content": "Say this is a test!"}
    ],
    "temperature": 0.7 # adjust temperature according to your model needs
  }'
```

{% endcode %}

{% hint style="info" %}
**Debugging tip:** If you’re troubleshooting formatting/templates, you can inspect the *raw* prompt LM Studio sends to the model by running: `lms log stream`
{% endhint %}

### Troubleshooting

#### **Model runs in Unsloth, but LM Studio output is gibberish / repeats**

This is almost always a **prompt template / chat template mismatch**.

LM Studio will **auto-detect** the prompt template from the GGUF metadata when possible, but custom or incorrectly-tagged models may need a manual override.

**Fix:**

1. Go to **My Models** → click the gear ⚙️ next to your model
2. Find **Prompt Template** and set it to match the template you trained with
3. Alternatively, in the Chat sidebar: enable the **Prompt Template** box (you can force it to always show)

#### LM Studio doesn’t show my model in “My Models”

* Prefer `lms import /path/to/model.gguf`
* Or confirm the file is in the correct folder structure: `~/.lmstudio/models/publisher/model/model-file.gguf`

#### OOM / slow performance

* Use a smaller quant (ex: `Q4_K_M`)
* Reduce context length
* Adjust GPU offload (LM Studio “Per-model defaults” / load settings)

***

### More resources

* [LM Studio + Unsloth blog post](https://lmstudio.ai/blog/functiongemma-unsloth) (FunctionGemma walkthrough):&#x20;
* LM Studio [Import Models docs](https://lmstudio.ai/docs/app/advanced/import-model)
* LM Studio [Prompt Template docs](https://lmstudio.ai/docs/app/advanced/prompt-template)
* LM Studio [OpenAI-compatible API docs](https://lmstudio.ai/docs/developer/openai-compat)


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/inference-and-deployment/lm-studio.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
