> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/qwen-image-2.1.md).

# Qwen-Image-2.1: How to Run Locally

Run Qwen-Image-2.1 locally with Unsloth FP8 and GGUF quants.

**Qwen-Image-2.1** and **Qwen-Image-2.1-Turbo** generate and [edit images](#image-editing). Qwen-Image-2.1 has 7B parameters and needs **11GB VRAM** with GGUFs or 24GB with INT8/FP8.

{% columns %}
{% column width="50%" %}
Qwen-Image-2.1 combines a 7B image generator with a **Qwen3-VL 8B encoder**. The model supports native 2K generation, text rendering, transparent images and editing with up to 10 reference images.

The quants use [Unsloth Dynamic](https://unsloth.ai/docs/basics/dynamic-3.0-ggufs) which upcasts important layers to higher precision for more accuracy. Run in [Unsloth Desktop](/docs/desktop.md), diffusers, stable-diffusion.cpp and more.

* Qwen-Image-2.&#x31;**:** [GGUF](https://huggingface.co/unsloth/Qwen-Image-2.1-GGUF) • [FP8](https://huggingface.co/unsloth/Qwen-Image-2.1-FP8)
* Qwen-Image-2.1-**Turbo**: [GGUF](https://huggingface.co/unsloth/Qwen-Image-2.1-Turbo-GGUF) • [FP8](https://huggingface.co/unsloth/Qwen-Image-2.1-Turbo-FP8)
  {% endcolumn %}

{% column width="50%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F8E4zaQZmeYBhYIXkvveM%2F01-2edit-multi-image.webp?alt=media&amp;token=ad7d102c-b304-4c75-b66d-4a68cd518a37" alt=""><figcaption><p>Image editing by FP8 Qwen-Image-1.2 via Unsloth</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

### 🖥️  Memory requirements

Use the table below to choose a starting configuration for your hardware. Generate one image at the listed resolution, then increase it if memory allows.

FP8 quants are recommended for GPUs with 24 GB of VRAM or more. It may also be preferable for any setup with a GPU, as it can offer faster inference than GGUF models even with offloading. Just ensure you have enough RAM for offloading.

Use GGUF models mostly if you have CPU RAM, or use a unified-memory system such as a Mac.

**Memory figures are estimates, not tested minimums.** Memory usage varies with resolution and offloading settings.

| Available hardware                          | Starting configuration                                                                     |
| ------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **12–16 GB VRAM**                           | GGUF **Q4\_K\_M**, 1024×1024, batch 1                                                      |
| **24 GB VRAM**                              | <p><strong>INT8/FP8:</strong> 512 × 512<br><strong>GGUF Q4\_K\_M:</strong> 1024 × 1024</p> |
| **6GB VRAM**                                | You can run FP8 **on just 6GB of VRAM using offloading**. Inference will be <2x slower.    |
| **CPU-only: 12–16 GB RAM**                  | GGUF **Q4\_K\_M** with the Q4\_K\_XL text encoder                                          |
| **Apple Silicon: 12–16 GB+ unified memory** | GGUF with a compatible native backend                                                      |

CPU offloading can help when VRAM is limited, but requires additional system RAM and may slow generation.

### Quantization Analysis

We show that INT8 has the lowest reasonable LPIPS (lower is better) than even FP8, so we default to using INT8.

| scheme | file size | LPIPS mean | LPIPS max | SSIM mean |
| ------ | --------- | ---------: | --------: | --------: |
| int8   | 7.26 GB   |      0.064 |     0.167 |     0.936 |
| fp8    | 7.12 GB   |      0.112 |     0.329 |     0.899 |

### ⚡ Quickstart

{% stepper %}
{% step %}

#### Setup Unsloth

The easiest way to get started is by downloading the [Unsloth Desktop app](/docs/desktop.md). Works on [macOS](/docs/get-started/install/mac.md), [Windows](/docs/get-started/install/windows-installation.md), and [Linux](/docs/get-started/install/linux.md).

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

Or, if you prefer to install manually:

MacOS, Linux, WSL:

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

Windows PowerShell:

```bash
irm https://unsloth.ai/install.ps1 | iex
```

{% endstep %}

{% step %}

#### Setup Qwen-Image-2.1

In this release, Qwen-Image-2.1 is available in Unsloth for text-to-image generation only.

Select **Images** from the sidebar. The **Create** an image workflow opens by default.

Open Select image model in there or go to Model hub and search for your desired Qwen-Image-2.1 GGUF or FP8 quant from the selector which will download the model.

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FEFCApsTzrL81lOcdd298%2Fimage.png?alt=media&amp;token=07fa0438-55f4-46ec-b055-2f4b6532df96" alt="" width="563"><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FHjN84g8IYe9eRSRO4wGe%2Fqwenimage2.1.png?alt=media&amp;token=73f99133-f0d0-47c8-aaa4-a0097b5ff7b4" alt="" width="563"><figcaption></figcaption></figure></div>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FuWMvSNEkp7lnr2es7v32%2FScreenshot%202026-09-22%20at%206.23.20%E2%80%AFAM.png?alt=media&amp;token=570e743c-b6b9-4fa2-b06d-b6e4c955424a" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Generate your image

Describe the image you want to generate. You can keep the recommended settings for your first image.

Click **Generate**. The first generation may take longer while the model downloads and loads. Your result will appear in the gallery, where you can view its settings or download it.

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FrX8YDJ91NTwNVtFpERXX%2Fimage.png?alt=media&amp;token=fee9d4b5-cca3-4054-ad50-6aa1beba5a50" alt="" width="563"><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F0JAa73bhb2PAD0692XqI%2F1000007556.jpg?alt=media&amp;token=c725d011-01c2-4a56-96bb-31034ecb77cf" alt="" width="375"><figcaption></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### Image Editing

You can easily also edit photos with transparent backgrounds using Qwen-Image-2.1. Remove elements, add elements, change the vibe while keeping the same foundation/structure. Just select the Edit tab inside of Unsloth and write your prompt.

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNA6VP3yqmBZhR4qVE90I%2F02-localized-annotation.webp?alt=media&amp;token=a42e809a-f4ea-4779-9213-606c772e9422" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FS0j84jGUey0dnoQgEQzm%2F03-transparent-edit.webp?alt=media&amp;token=ce337489-f698-4c25-9c3b-3fd77bc2e48d" alt=""><figcaption></figcaption></figure></div>

### ⚙️ Recommended settings

**Use the recipe for the backend actually running the model**, not just its FP8/GGUF file extension.

| Setting                  | Unsloth GPU / Diffusers                       | Native stable-diffusion.cpp                      |
| ------------------------ | --------------------------------------------- | ------------------------------------------------ |
| **Steps**                | **40** - Qwen/Diffusers baseline              | **20** - CLI default and Unsloth's recorded test |
| **Guidance / CFG**       | **1.0** - CFG disabled                        | **6.0** - upstream sd.cpp example                |
| **Negative prompt**      | Leave blank; set guidance to `1.0` explicitly | Leave blank to reproduce the example             |
| **Sampler / scheduler**  | Keep the model's pipeline scheduler           | **Euler**                                        |
| **Flow shift**           | Keep the pipeline's scheduler configuration   | **Automatic; omit `--flow-shift`**               |
| **First-run resolution** | `1024×1024`                                   | `1024×1024`                                      |
| **Batch size**           | `1`                                           | `1`                                              |
| **Seed**                 | `42`, or another fixed comparison seed        | `42`, or another fixed comparison seed           |

#### Resolution and aspect ratios

Use dimensions divisible by **32**. Qwen's [native presets](https://huggingface.co/Qwen/Qwen-Image-2.1#supported-aspect-ratios) include:

| Shape               | Smaller test size | Qwen native preset |
| ------------------- | ----------------- | ------------------ |
| **Square**          | `1024×1024`       | `2048×2048`        |
| **Landscape 4:3**   | `1152×864`        | `2400×1792`        |
| **Portrait 3:4**    | `864×1152`        | `1792×2400`        |
| **Photo 3:2**       | `1248×832`        | `2528×1696`        |
| **Portrait 2:3**    | `832×1248`        | `1696×2528`        |
| **Widescreen 16:9** | `1536×864`        | `2752×1536`        |
| **Vertical 9:16**   | `864×1536`        | `1536×2752`        |

Unsloth supports dimensions up to **2048 pixels per side**. Start at **1024 × 1024** and increase the resolution if memory allows. Lowering the step count speeds up generation but may not resolve memory limits.

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
GET https://unsloth.ai/docs/models/qwen-image-2.1.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
