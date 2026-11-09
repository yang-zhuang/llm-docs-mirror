> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/nemotron-3-nano-omni.md).

# NVIDIA Nemotron 3 Nano Omni - How To Run Locally

Run & fine-tune Nemotron-3-Nano-Omni-30B-A3B locally on your device!

NVIDIA Nemotron-3-Nano-Omni-30B-A3B is an open 30B parameter, 3B active hybrid reasoning MoE model built for multimodal agentic workloads including **audio**, **video**, text, images and docs as input, with text output. The model runs on **25GB RAM** for 4-bit and 36GB for 8-bit.

With a **256K context**, Nemotron 3 Nano Omni is the **strongest omni** model for its size and the highest-efficiency open multimodal model. We collaborated with NVIDIA for day zero support!\
**GGUF:** [Nemotron-3-Nano-Omni-30B-A3B-Reasoning](https://huggingface.co/unsloth/Nemotron-3-Nano-30B-A3B-GGUF)

### ⚙️ Usage Guide

NVIDIA recommends these settings for inference:

{% columns %}
{% column %}
**Thinking mode:**

* `temperature = 0.6`
* `top_p = 0.95`
  {% endcolumn %}

{% column %}
**Instruct mode:**

* `temperature = 0.2`
  {% endcolumn %}
  {% endcolumns %}

### Run Nemotron-3-Nano-Omni

Depending on your use-case you will need to use [different settings](#usage-guide). Some GGUFs end up similar in size because the model architecture (like [gpt-oss](/docs/models/gpt-oss-how-to-run-and-fine-tune.md)) has dimensions not divisible by 128, so parts can’t be quantized to lower bits. **GGUF:** [Nemotron-3-Nano-Omni-30B-A3B-Reasoning](https://huggingface.co/unsloth/Nemotron-3-Nano-30B-A3B-GGUF)

The 4-bit versions of the model requires \~25GB RAM. 8-bit requires 36GB. For these guides, we will be using `UD-Q4-K-XL` which is a good balance between size and accuracy.

<a href="/docs/models/nemotron-3-nano-omni.md#unsloth-studio-guide" class="button primary">Run in Unsloth Studio</a><a href="/pages/GEABCCTb5KV7QKOeL4YY#llama.cpp-tutorial" class="button secondary">Run in llama.cpp</a>

{% hint style="warning" %}
Currently no multimodal/vision GGUF works in **Ollama** due to separate `mmproj` vision files. Use llama.cpp compatible backends.

Do NOT use **CUDA 13.2** as you may get gibberish outputs. NVIDIA is working on a fix.
{% endhint %}

### 🦥 Unsloth Studio Guide

For this tutorial, we will be using [Unsloth Studio](/docs/new/studio.md), which is our new web UI for running and training LLMs. With Unsloth Studio, you can run models and input **audio**, image and text locally on **Mac, Windows**, and Linux and:

{% columns %}
{% column %}

* Search, download, [run GGUFs](/docs/new/studio.md#run-models-locally) and safetensor models
* **Compare** models **side-by-side**
* [**Self-healing** tool calling](/docs/new/studio.md#execute-code--heal-tool-calling) + **web search**
* [**Code execution**](/docs/new/studio.md#run-models-locally) (Python, Bash)
* [Automatic inference](https://unsloth.ai/docs/desktop#feature-deep-dive) parameter tuning (temp, top-p, etc.)
* [Train LLMs](/docs/new/studio.md#no-code-training) 2x faster with 70% less VRAM
  {% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFeQ0UUlnjXkDdqhcWglh%2Fskinny%20studio%20chat.png?alt=media&amp;token=c2ee045f-c243-4024-a8e4-bb4dbe7bae79" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% stepper %}
{% step %}

#### Install Unsloth

**MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows PowerShell:**

```bash
irm https://unsloth.ai/install.ps1 | iex
```

{% endstep %}

{% step %}

#### Setup Unsloth Studio (one time)

Setup automatically installs Node.js (via nvm), builds the frontend, installs all Python dependencies, and builds llama.cpp with CUDA support.

{% hint style="info" %}
**WSL users:** you will be prompted for your `sudo` password to install build dependencies (`cmake`, `git`, `libcurl4-openssl-dev`).
{% endhint %}
{% endstep %}

{% step %}

#### Launch Unsloth

**MacOS, Linux, WSL:**

```bash
source unsloth_studio/bin/activate
unsloth studio -H 0.0.0.0 -p 8888
```

**Windows Powershell:**

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fd1yMMNa65Ccz50Ke0E7r%2FScreenshot%202026-03-17%20at%2012.32.38%E2%80%AFAM.png?alt=media&amp;token=9369cfe7-35b1-4955-b8cb-42f7ecb43780" alt="" width="375"><figcaption></figcaption></figure></div>

Then open `http://127.0.0.1:8888` in your browser.
{% endstep %}

{% step %}

#### Search and download NVIDIA-Nemotron-3-Nano-30B-A3B-Omni

On first launch you will need to create a password to secure your account and sign in again later. Then go to the [Unsloth Chat](/docs/new/studio/chat.md) tab and search for Nemotron-3-Nano-Omni in the search bar and download your desired model and quant.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQUTU2gI4DNuscVEuiT8f%2FScreenshot%202026-03-20%20at%201.28.50%E2%80%AFAM.png?alt=media&amp;token=74d5fd9e-a229-4ddc-a96d-abe68e1ca6a3" alt="" width="375"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}

#### Run Nemotron-3-Nano-30B-A3B-Omni

Inference parameters should be auto-set when using Unsloth Studio, however you can still change it manually. You can also edit the context length, chat template and other settings.

For more information, you can view our [Unsloth Studio inference guide](/docs/new/studio/chat.md).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FXPQGEEr1YoKofrTatAKK%2Ftoolcallingif.gif?alt=media&amp;token=25d68698-fb13-4c46-99b2-d39fb025df08" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### 🦙 Llama.cpp Tutorial:

Instructions to run in llama.cpp (note we will be using 4-bit to fit most devices):

{% stepper %}
{% step %}
Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

{% code overflow="wrap" %}

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endcode %}
{% endstep %}

{% step %}
**Let's first get an image!** You can also upload images as well. We shall use <https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/unsloth%20made%20with%20love.png>, which is just our mini logo showing how finetunes are made with Unsloth:

{% code overflow="wrap" %}

```bash
wget https://raw.githubusercontent.com/unslothai/unsloth/refs/heads/main/images/unsloth%20made%20with%20love.png -O unsloth.png
```

{% endcode %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-9bf7ec93680f889d7602e5f56a8d677d6a58ae6a%2Funsloth%20made%20with%20love.png?alt=media" alt="" width="188"><figcaption></figcaption></figure>

Let's get the 2nd image at <https://files.worldwildlife.org/wwfcmsprod/images/Sloth_Sitting_iStock_3_12_2014/story_full_width/8l7pbjmj29_iStock_000011145477Large_mini__1_.jpg>

{% code overflow="wrap" %}

```bash
wget https://files.worldwildlife.org/wwfcmsprod/images/Sloth_Sitting_iStock_3_12_2014/story_full_width/8l7pbjmj29_iStock_000011145477Large_mini__1_.jpg -O picture.png
```

{% endcode %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-4b30cc86b2c75edf95ee1ec6fe0c51fb30afd6c0%2F8l7pbjmj29_iStock_000011145477Large_mini__1_.jpg?alt=media" alt="" width="188"><figcaption></figcaption></figure>
{% endstep %}

{% step %}
Now let's download the model manually. We can do this via the code below (after installing pip install huggingface\_hub). If downloads get stuck, see: [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

{% code overflow="wrap" %}

```bash
pip install huggingface_hub
hf download unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF \
    --local-dir unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF \
    --include "*mmproj-BF16*" \
    --include "*UD-Q4_K_XL*" # Use "*UD-Q2_K_XL*" for Dynamic 2bit
```

{% endcode %}
{% endstep %}

{% step %}
Then run the model in conversation mode:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-UD-Q4_K_XL.gguf \
    --mmproj unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF/mmproj-BF16.gguf \
    --temp 0.6 \
    --top-p 0.95 \
    --min-p 0.01
```

{% endcode %}
{% endstep %}

{% step %}
You will then see the below:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FiocWqkHECR9o9Fufepqs%2Fimage.png?alt=media&amp;token=f9ec7bc5-2d80-4fff-94ef-0aaf9c80a095" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}
Then use `/image` to load both images in and ask "What is this image":

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FHn6j4OoFDiIth4sBDGBF%2Fimage.png?alt=media&amp;token=b4d1e448-73e9-4942-b465-ee9b80361447" alt="" width="563"><figcaption></figcaption></figure>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FvwqETRkGCwWUgpYqoEnZ%2Fimage.png?alt=media&amp;token=39e0fd0f-d7c2-4689-b3b1-3f8003a94dad" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}

{% step %}
And for the sloth image:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FnlL5IizsVPiO655YHkYx%2Fimage.png?alt=media&amp;token=e414e213-e64d-4167-a5ae-7f52fa19b635" alt="" width="563"><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

#### Llama-server serving & deployment

To deploy Nemotron 3 Nano Omni locally, use `llama-server`. In a new terminal, for example via `tmux`, deploy the model:

```bash
./llama.cpp/llama-server \
    -hf unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF:UD-Q4_K_XL \
    --alias "unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning" \
    --prio 3 \
    --temp 0.6 \
    --top-p 0.95 \
    --port 8001
```

If you downloaded the model manually, use:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-server \
    --model unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-UD-Q4_K_XL.gguf \
    --mmproj unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning-GGUF/mmproj-BF16.gguf \
    --alias "unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning" \
    --prio 3 \
    --temp 0.6 \
    --top-p 0.95 \
    --port 8001
```

{% endcode %}

Then in a new terminal, after installing the OpenAI client with `pip install openai`:

```python
from openai import OpenAI
openai_client = OpenAI(
    base_url = "http://127.0.0.1:8001/v1",
    api_key = "sk-no-key-required",
)
completion = openai_client.chat.completions.create(
    model = "unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning",
    messages = [
        {"role": "user", "content": "What is 2+2?"},
    ],
)
print(completion.choices[0].message.reasoning_content)
print(completion.choices[0].message.content)
```

Which will show something like the below:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F7Y9vyJDtdxkMlYMcS9PT%2Fimage.png?alt=media&amp;token=a1b46fb5-ed87-4f22-b035-de935a6ac7d3" alt="" width="563"><figcaption></figcaption></figure>

#### Image input through the OpenAI-compatible server

Let's use `picture.png` which was the sloth image like in [#llama.cpp-tutorial](#llama.cpp-tutorial "mention")

{% code expandable="true" %}

```python
from openai import OpenAI
import base64
import mimetypes
image_link = "picture.png"

def file_to_data_url(path: str) -> str:
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

openai_client = OpenAI(
    base_url = "http://127.0.0.1:8001/v1",
    api_key = "sk-no-key-required",
)

completion = openai_client.chat.completions.create(
    model = "unsloth/NVIDIA-Nemotron-3-Nano-Omni-30B-A3B-Reasoning",
    messages = [ {
        "role": "user",
        "content": [
            { "type": "text", "text": "What is this image?", },
            {
                "type": "image_url",
                "image_url": { "url": file_to_data_url(image_link), },
            },
        ],
    } ],
)
print(completion.choices[0].message.reasoning_content)
print(completion.choices[0].message.content)
```

{% endcode %}

Which will show something like below:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FhPQNQGHicFdRXkThKapE%2Fimage.png?alt=media&amp;token=1a77fc30-0afb-4e37-b4b0-9d38bdf7decd" alt=""><figcaption></figcaption></figure>

### 🦥 Fine-tuning Nemotron 3 Nano Omni

Unsloth supports the entire [Nemotron](/docs/models/nemotron-3.md) model family. Nemotron 3 Nano Omni is useful for multimodal agent datasets. You can train on audio, vision or text via Unsloth. **Video input** fine-tuning is currently not supported.

For text-only and notebooks, you can start from the existing [Nemotron 3 Nano fine-tuning flow](/docs/models/nemotron-3.md#fine-tuning-nemotron-3-and-rl). For multimodal adapters, make sure your dataset includes the modality your agent actually needs:

* **Computer use:** screenshots, UI state, cursor/context, expected next action
* **Document intelligence:** PDFs, screenshots, charts, tables, structured extraction targets
* **Audio understanding:** audio clips, sampled frames, summaries, timestamps, events and follow-up questions
* **Agent loops:** observation → reasoning → action → validation examples

For Omni, do not blindly reuse text-only VRAM numbers. Multimodal encoders, projector weights, image tokens, audio chunks and long context all increase memory use. Start with shorter contexts and smaller batch sizes, then scale up.

### Benchmarks

Nemotron 3 Nano Omni is the strongest omni model for its size. It is also the highest-efficiency open multimodal model with leading accuracy. The model surpasses Qwen3-Omni-30B-A3B on every benchmark.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FVeilBuCszSJr4yoJDaGm%2Funnamed.png?alt=media&amp;token=5fe8205c-6f2b-40c3-a0e2-ef254a357d2b" alt="" width="563"><figcaption></figcaption></figure></div>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/nemotron-3-nano-omni.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
