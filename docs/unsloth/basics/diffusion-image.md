> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/diffusion-image.md).

# How to Run Image Diffusion Models Locally with Unsloth

Generate and edit AI images on your own computer using diffusion models without writing code or setting up a complex workflow. With Unsloth, you can run models like **MiniMax-H3**, [**Qwen-Image-2.1**](/docs/models/qwen-image-2.1.md)**, Z-Image** and **FLUX** locally with support for **GGUFs**, **FP8**, **LoRAs**, reference images, and more. Start with a text prompt or an existing image, then create, transform, edit, extend, upscale, or fine-tune images using the tools and workflows supported by each model.

Choose from **MiniMax-H3**, [**Qwen-Image-2.1**](/docs/models/qwen-image-2.1.md)**,** **Z-Image, LTX, FLUX, SDXL and more**.

To create your own LoRA, fine-tune a supported model on your dataset. See <mark style="color:blue;">Fine-tune an image model</mark> to learn more.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FmG2HFa4hRVF1LA8AWcZc%2Fimage.png?alt=media&amp;token=250f56c3-ac31-4e7c-a733-8024a4e4fc3f" alt="" width="563"><figcaption></figcaption></figure></div>

### ⚡ Quickstart

{% stepper %}
{% step %}

### **Install or update**

The desktop app is the easiest way to get started.

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth Desktop</a>

Follow the installer, then open the app from your applications. If you already have it installed, make sure it is up to date before continuing.

**Command line**

Prefer the terminal? Run the command for your operating system. The same command will update an existing installation.

**MacOS, Linux, WSL:**

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

**Windows PowerShell:**

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

#### Launch Unsloth

Once the installation finishes, launch Unsloth:

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

Open `http://localhost:8888` if it does not open automatically.
{% endstep %}

{% step %}

### Open Images

Select **Images** from the sidebar. The **Create** workflow opens by default.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FEFCApsTzrL81lOcdd298%2Fimage.png?alt=media&amp;token=07fa0438-55f4-46ec-b055-2f4b6532df96" alt="" width="375"><figcaption></figcaption></figure></div>

Now we are ready to move onto the next step.
{% endstep %}

{% step %}

### Choose a model

Open **Select image model** and choose a model from the selector.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F9rVVPAiJKVsY01x1oKYL%2Fimage.png?alt=media&amp;token=4d523fdd-7bb3-493f-9377-e12dd989c865" alt="" width="375"><figcaption></figcaption></figure></div>

The **Recommended** tab is a good place to start.\
\
For GGUF models, the best size for your device is also marked **recommended**. Sizes that may run slowly or not fit are marked **TIGHT** or **OOM**.
{% endstep %}

{% step %}

### Enter a prompt

Describe the image you want to generate.

For example:

> Top-down shot of a tranquil koi pond in a Japanese garden, orange, white and black koi swimming beneath the clear water, surrounded by moss-covered stepping stones and small wooden bridges, with red maple leaves floating on the surface. Bright midday light, saturated colour, crisp reflections. Whimsical cartoon illustration, 50mm.

You can keep the recommended settings for your first image.
{% endstep %}

{% step %}

### Generate your first image

Select **Generate**. The first generation may take longer while the model downloads and loads.

Your result will appear in the gallery, where you can view its settings or download it.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FT7kNykpOms4GymzxY4jT%2Fimage.png?alt=media&amp;token=8a2bf1bb-26d2-4f5c-a43f-6f5fec9005dc" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### ⭐ Features

The available workflows depend on the model you load. Unsupported workflows are hidden automatically.

#### Create and edit images

* **Create:** Generate an image from a text prompt.
* **Transform:** Use an existing image as the starting point for a new generation.
* **Inpaint:** Select and regenerate part of an image.
* **Extend:** Generate content beyond the original canvas.
* **Upscale:** Increase the resolution of an image.
* **Reference:** Guide a generation with one or more reference images.
* **Edit:** Describe the changes you want to make to an image.

**Edit** requires a compatible model such as Qwen-Image-Edit or FLUX.1 Kontext.

#### LoRAs and ControlNet

Load compatible LoRAs to add a character, subject or visual style to your generations. Adjust the LoRA weight to control how strongly it affects the result.

Supported models can also use ControlNet to guide the structure of an image. Adjust its strength to control how closely the result follows the guidance image.

#### Gallery

Generated images are saved to the local gallery. Open a result to view its prompt and settings, select **Recipe** to restore its generation setup or download the image.

### Supported models and workflows

| What you want to do          | Models to start with              |
| ---------------------------- | --------------------------------- |
| Generate or transform images | Z-Image, Qwen-Image, FLUX.1, SDXL |
| Edit using instructions      | Qwen-Image-Edit, FLUX.1 Kontext   |
| Use reference images         | FLUX.2 klein                      |

More models are available in the model picker. Formats and workflows vary by model, and unsupported workflows are hidden automatically.

### Generation settings

The default settings are a good starting point. However, it is possible to adjust settings to get the best result, these are the main parameters you may want to change:

| Setting                         | What it changes                                                                              |
| ------------------------------- | -------------------------------------------------------------------------------------------- |
| **Prompt**                      | Describes the image you want to create. In **Edit**, this becomes the instruction to follow. |
| **Aspect ratio and resolution** | Set the shape and size of the image. Larger images use more memory and take longer.          |
| **Steps**                       | Control how long the model spends generating. More steps do not always improve the result.   |
| **Guidance**                    | Controls how strongly the prompt guides the result. Some models work best at `0`.            |
| **Seed**                        | Helps recreate a result. Leave it empty to use a random seed.                                |

<details>

<summary>Advanced generation settings</summary>

These controls change how the model runs on your device. Adjust them to reduce memory usage, improve performance or troubleshoot generation.

| Setting         | What it changes                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Speed**       | Controls compilation and performance optimizations. Compiled modes may take longer during the first generation.                                  |
| **Precision**   | Changes the numerical format used to run the model. Lower precision can reduce memory usage. Available options depend on the model and hardware. |
| **Attention**   | Selects the attention implementation used during generation.                                                                                     |
| **Memory**      | Balances generation speed against GPU memory usage. Try **Low VRAM** if a model is close to your memory limit.                                   |
| **Step cache**  | Reuses some calculations between diffusion steps to improve generation speed.                                                                    |
| **CPU offload** | Moves parts of the model into system memory. This reduces GPU memory usage but may make generation slower.                                       |

</details>

### ⚠️ Troubleshooting

<details>

<summary>Images does not appear</summary>

Update to the latest version, then restart the app. See [Updating Unsloth](https://unsloth.ai/docs/get-started/install/updating) for instructions.

</details>

<details>

<summary>A model will not download or load</summary>

Some image models are large and take time to download. Check that you have enough free storage and a stable internet connection.

Some models also require you to accept their licence on Hugging Face and add a Hugging Face token before downloading them.

</details>

<details>

<summary>The model runs out of memory</summary>

Try a smaller GGUF quantization or a 4-bit version of the model. For GGUF models, start with the size marked **recommended**.

You can also:

* Lower the image resolution.
* Keep the batch size at `1`.
* Close other applications using the GPU.
* Choose a smaller model.

A **TIGHT** model may use system memory and run more slowly. A model marked **OOM** is unlikely to fit.

</details>

<details>

<summary>A workflow is missing</summary>

The available workflows depend on the loaded model. Unsupported workflows will not appear.

For example, instruction-based editing requires a model such as Qwen-Image-Edit or FLUX.1 Kontext.

</details>

### ❓ FAQ

<details>

<summary>Does image generation run locally?</summary>

Yes. Once a model is downloaded, image generation runs on your device.

</details>

<details>

<summary>What is the difference between Transform and Edit?</summary>

**Transform** redraws an existing image using a prompt that describes the complete result.

**Edit** follows instructions such as changing a background or adding an object. It requires a compatible editing model.

</details>

<details>

<summary>Can I train my own image LoRA?</summary>

Yes. Fine-tune a supported model on your own images, then load the finished LoRA in **Create**.

See Fine-tune an image model to learn more.

</details>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/diffusion-image.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
