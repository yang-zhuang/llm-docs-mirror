> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/how-to-run-llms-with-docker.md).

# How to Run Local LLMs with Docker: Step-by-Step Guide

Learn how to run Large Language Models (LLMs) with Docker & Unsloth on your local device.

You can now run any model, including Unsloth [Dynamic GGUFs](/docs/basics/dynamic-3.0-ggufs.md), on Mac, Windows or Linux with a single line of code or **no code** at all. We collabed with Docker to simplify model deployment, and Unsloth now powers most GGUF models on Docker.

Before you start, make sure to look over [hardware requirements](#hardware-info--performance) and [our tips](#hardware-info--performance) for optimizing performance when running LLMs on your device.

<a href="/docs/models/tutorials/how-to-run-llms-with-docker.md#method-1-docker-terminal" class="button primary">Docker Terminal Tutorial</a><a href="#method-2-docker-desktop-no-code" class="button primary">Docker no-code Tutorial</a>

To get started, run OpenAI [gpt-oss](/docs/models/gpt-oss-how-to-run-and-fine-tune.md) with a single command:

```bash
docker model run ai/gpt-oss:20B
```

Or to run a specific [Unsloth model](/docs/get-started/unsloth-model-catalog.md) / quant from Hugging Face:

```bash
docker model run hf.co/unsloth/gpt-oss-20b-GGUF:F16
```

{% hint style="success" %}
You don’t need Docker Desktop, Docker CE is enough to run models.
{% endhint %}

#### **Why Unsloth + Docker?**

We collab with model labs like Google Gemma to fix model bugs and boost accuracy. Our Dynamic GGUFs consistently outperform other quant methods, giving you high-accuracy, efficient inference.

If you use Docker, you can run models instantly with zero setup. Docker uses [Docker Model Runner](https://github.com/docker/model-runner) (DMR), which lets you run LLMs as easily as containers with no dependency issues. DMR uses Unsloth models and `llama.cpp` under the hood for fast, efficient, up-to-date inference.

## :gear: Hardware Info + Performance

For the best performance, aim for your VRAM + RAM combined to be at least equal to the size of the quantized model you're downloading. If you have less, the model will still run, but significantly slower.

Make sure your device also has enough disk space to store the model. If your model only barely fits in memory, you can expect around \~5 tokens/s, depending on model size.

Having extra RAM/VRAM available will improve inference speed, and additional VRAM will enable the biggest performance boost (provided the entire model fits)

{% hint style="info" %}
**Example:** If you're downloading gpt-oss-20b (F16) and the model is 13.8 GB, ensure that your disk space and RAM + VRAM > 13.8 GB.
{% endhint %}

**Quantization recommendations:**

* For models under 30B parameters, use at least 4-bit (Q4).
* For models 70B parameters or larger, use a minimum of 2-bit quantization (e.g., UD\_Q2\_K\_XL).

## ⚡ Step-by-Step Tutorials

Below are **two ways** to run models with Docker: one using the [terminal](#method-1-docker-terminal), and the other using [Docker Desktop](#method-2-docker-desktop-no-code) with no code:

### Method #1: Docker Terminal

{% stepper %}
{% step %}

#### Install Docker

Docker Model Runner is already available in **both** [Docker Desktop](https://docs.docker.com/ai/model-runner/get-started/#docker-desktop) and [**Docker CE**](https://docs.docker.com/ai/model-runner/get-started/#docker-engine)**.**
{% endstep %}

{% step %}

#### Run the model

Decide on a model to run, then run the command via terminal.

* Browse the verified catalog of trusted models available on [Docker Hub](https://hub.docker.com/r/ai) or [Unsloth's Hugging Face](https://huggingface.co/unsloth) page.
* Go to Terminal to run the commands. To verify if you have `docker` installed, you can type 'docker' and enter.
* Docker Hub defaults to running Unsloth Dynamic 4-bit, however you can select your own quantization level (see step #3).

For example, to run OpenAI `gpt-oss-20b` in a single command:

```bash
docker model run ai/gpt-oss:20B
```

Or to run a specific [Unsloth](/docs/get-started/unsloth-model-catalog.md) gpt-oss quant from Hugging Face:

```bash
docker model run hf.co/unsloth/gpt-oss-20b-GGUF:UD-Q8_K_XL
```

**This is how running gpt-oss-20b should look via CLI:**

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNQQGqQfLuX2a40i07Es1%2Funknown.png?alt=media&amp;token=6006e370-a298-4e5f-af9f-5c4e8c4a0fc8" alt="" width="563"><figcaption><p>gpt-oss-20b from Docker Hub</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFtzowkLonKo4N2LzEnhe%2Fgptoss%20ud8kxl.png?alt=media&amp;token=08eb6244-0626-4ad8-adbe-f5c4e5aa6d72" alt="" width="563"><figcaption><p>gpt-oss-20b with Unsloths' UD-Q8_K_XL quantization</p></figcaption></figure></div>
{% endstep %}

{% step %}

#### To run a specific quantization level:

If you want to run a specific quantization of a model, append `:` and the quantization name to the model (e.g., `Q4` for Docker or `UD-Q4_K_XL`). You can view all available quantizations on each model’s Docker Hub page. e.g. see the listed quantizations for gpt-oss [here](https://hub.docker.com/r/ai/gpt-oss#gptoss).

The same applies to Unsloth quants on Hugging Face: visit the [model’s HF page](https://huggingface.co/unsloth/gpt-oss-20b-GGUF?show_file_info=gpt-oss-20b-Q2_K_L.gguf), choose a quantization, then run something like: `docker model run hf.co/unsloth/gpt-oss-20b-GGUF:Q2_K_L`

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FI7MrphUugkU8eZ1f7lJz%2FScreenshot%202025-11-16%20at%2010.52.25%E2%80%AFPM.png?alt=media&amp;token=ae777fdb-258e-46d0-b06e-b68434f7fa58" alt="" width="563"><figcaption><p>gpt-oss quantization levels on <a href="https://hub.docker.com/r/ai/gpt-oss#gptoss">Docker Hub</a></p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F73UWIs9VAZ6Iz1omgZSm%2FScreenshot%202025-11-16%20at%2010.54.53%E2%80%AFPM.png?alt=media&amp;token=e8dee7f3-1b8b-4dda-a455-26df58102d16" alt="" width="563"><figcaption><p>Unsloth gpt-oss quantization levels on<a href="https://huggingface.co/unsloth/gpt-oss-20b-GGUF"> Hugging Face</a></p></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### Method #2: Docker Desktop (no code)

{% stepper %}
{% step %}

#### Install Docker Desktop

Docker Model Runner is already available in [Docker Desktop](https://docs.docker.com/ai/model-runner/get-started/#docker-desktop).

1. Decide on a model to run, open Docker Desktop, then click on the models tab.
2. Click 'Add models +' or Docker Hub. Search for the model.

Browse the verified model catalog available on [Docker Hub](https://hub.docker.com/r/ai).

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F6R8uxbedMklVHsriLgpZ%2FScreenshot%202025-11-16%20at%206.36.49%E2%80%AFAM.png?alt=media&amp;token=0fb849f5-bc72-4883-9b25-1a756334ab4b" alt=""><figcaption><p>#1. Click 'Models' tab then 'Add models +'</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fj7I69xgxDeHXkvVbjemq%2FScreenshot%202025-11-16%20at%206.46.47%E2%80%AFAM.png?alt=media&amp;token=3e25d495-f34b-47d6-9185-f145610eed10" alt=""><figcaption><p>#2. Search for your desired model.</p></figcaption></figure></div>
{% endstep %}

{% step %}

#### Pull the model

Click the model you want to run to see available quantizations.

* Quantizations range from 1–16 bits. For models under 30B parameters, use at least 4-bit (`Q4`).
* Choose a size that fits your hardware: ideally, your combined unified memory, RAM, or VRAM should be equal to or greater than the model size. For example, an 11GB model runs well on 12GB unified memory.

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FdQnwVwsMhYtWTzAGFih3%2FScreenshot%202025-11-16%20at%206.47.26%E2%80%AFAM.png?alt=media&amp;token=b1f0e29a-b3de-4d96-b79a-931441744565" alt=""><figcaption><p>#3. Select which quantization you would like to pull.</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFGMZEXgQjBdVqP0vFTX3%2FScreenshot%202025-11-16%20at%206.54.09%E2%80%AFAM.png?alt=media&amp;token=b7f0c0d8-ebef-4e7e-99a9-c44c4c5f0844" alt=""><figcaption><p>#4. Wait for model to finish downloading, then Run it.</p></figcaption></figure></div>
{% endstep %}

{% step %}

#### Run the model

Type any prompt in the 'Ask a question' box and use the LLM like you would use ChatGPT.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F9nVjWcVsYK9CeT8gk3nQ%2FScreenshot%202025-11-16%20at%206.54.50%E2%80%AFAM.png?alt=media&amp;token=d7e5b63d-9c3e-42b0-882c-de046bbcfc9a" alt="" width="563"><figcaption><p>An example of running Qwen3-4B <code>UD-Q8_K_XL</code></p></figcaption></figure>
{% endstep %}
{% endstepper %}

#### **To run the latest models:**

You can run any new model on Docker as long as it’s supported by `llama.cpp` or `vllm` and available on Docker Hub.

### What Is the Docker Model Runner?

The Docker Model Runner (DMR) is an open-source tool that lets you pull and run AI models as easily as you run containers. GitHub: <https://github.com/docker/model-runner>

It provides a consistent runtime for models, similar to how Docker standardized app deployment. Under the hood, it uses optimized backends (like `llama.cpp`) for smooth, hardware-efficient inference on your machine.

Whether you’re a researcher, developer, or hobbyist, you can now:

* Run open models locally in seconds.
* Avoid dependency hell, everything is handled in Docker.
* Share and reproduce model setups effortlessly.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/how-to-run-llms-with-docker.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
