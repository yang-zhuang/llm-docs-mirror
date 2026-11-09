> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/muse-spark-open.md).

# Meta Muse Spark Open - Run Locally Guide

Learn how to run the new Muse Spark Open model from Meta.

Muse Spark Open is Meta’s new **816B-parameter** MoE model (\~42.7B active), built for multimodal coding and agentic workflows. Muse-Spark-Open-**816B-A42B** supports **text, image, video, and audio inputs**, text output, and a **1M-token context window**.

This guide covers running Meta Superintelligence Labs’ Muse Spark Open with Unsloth [Dynamic GGUFs](https://sites.gitbook.com/preview/site_mXXTe/~/revisions/OKhxydnrrRuNu350geRP/basics/dynamic-3.0-ggufs) for optimal performance via [Unsloth Desktop](https://sites.gitbook.com/preview/site_mXXTe/~/revisions/OKhxydnrrRuNu350geRP/models/muse-spark-1.2#unsloth-guide) or llama.cpp. The 2-bit quant fits on devices with 256GB of RAM, VRAM or unified memory. Thanks Meta for Unsloth day-zero access. [**Muse-Spark-Open-816B-A42B-GGUF**](https://huggingface.co/unsloth/Muse-Spark-Open-816B-A42B-GGUF)

### Usage Guide

Muse Spark Open is a natively multimodal reasoning model with tool-use and test-time reasoning. Muse Spark Open was additionally trained on long-horizon coding tasks including whole-repository generation, large end-to-end projects and auto-research.

The **2-bit** `UD-IQ2_XXS` quant will fit on 256GB RAM and 8-bit requires 900GB RAM.

#### Hardware requirements

Muse Spark Open uses approximately **1.63 TB for full precision BF16 language-model weights** before runtime overhead. Unsloth Dynamic quantization supports MoE architectures and uses model-specific quantization schemes to preserve accuracy while reducing memory requirements.

**Table: Muse Spark Open hardware requirements** (units = total memory: RAM + VRAM, or unified memory).

| 1-bit      | 2-bit      | 3-bit      | 4-bit  | 6-bit  | 8-bit      |
| ---------- | ---------- | ---------- | ------ | ------ | ---------- |
| 180-212 GB | 250-316 GB | 346-410 GB | 512 GB | 640 GB | 870-950 GB |

{% hint style="info" %}
As a rule of thumb, your total available memory should at least exceed the size of the quantized model you download. llama.cpp can use partial RAM / disk offload when it does not, but generation will be slower. Higher context lengths also require additional memory.
{% endhint %}

#### Recommended Settings <a href="#thinking-settings" id="thinking-settings"></a>

Muse Spark Open is a reasoning model and supports low, medium, high and xhigh reasoning efforts.

Recommended inference parameters for Muse Spark Open:

* `temperature = 1.0`
* `top_p = 1.0`
* `top_k = 0 or disabled`

**Maximum context length**: `1,048,576`

## Run Muse Spark Open Tutorials

Because quantized **Muse-Spark-Open-816B-A42B** comes in several sizes, the recommended starting point for the models is [**Dynamic**](/docs/basics/dynamic-3.0-ggufs.md) &#x32;**-bit**. Muse-Spark-Open-816B-A42B[ GGUFs](https://huggingface.co/unsloth/Muse-Spark-Open-816B-A42B-GGUF).

<a href="/docs/models/muse-glimmer.md#unsloth-guide" class="button primary">🦥 Unsloth Guide</a><a href="/pages/1hXO5DDKxmP1zKUUnBnA#llama.cpp-guide" class="button primary">🦙 Llama.cpp Guide</a>

### 🦥 Unsloth Guide

Muse Spark Open can now be run and fine-tuned in Unsloth Desktop, our new open-source desktop app for local AI. Unsloth lets you run models locally on **MacOS, Windows**, Linux and:

* Search, download, [run GGUFs](/docs/new/studio.md#run-models-locally) and safetensor models
* [**Self-healing** tool calling](/docs/new/studio.md#execute-code--heal-tool-calling) + **web search**
* [**Code execution**](/docs/new/studio.md#run-models-locally) (Python, Bash)
* [Automatic inference](https://unsloth.ai/docs/desktop#feature-deep-dive) parameter tuning (temp, top-p, etc.)
* Fast CPU + GPU inference via llama.cpp
* [Train LLMs](/docs/new/studio.md#no-code-training) 2x faster with 70% less VRAM

{% stepper %}
{% step %}

#### **Setup Unsloth**

The easiest way to get started is by downloading the [Unsloth Desktop app](/docs/desktop.md).

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

You can also install manually:

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

#### Launch Unsloth and Search and download Muse Spark Open

On first launch go to the Model hub tab and search for Muse Spark Open in the search bar and download your desired model and quant.
{% endstep %}

{% step %}

#### Run Muse Spark Open

Inference parameters should be auto-set when using Unsloth Desktop, however you can still change it manually. You can also edit the context length, chat template and other settings. You can run GGUFs, safetensors and MLX files.

For more information, you can view our [Unsloth inference guide](/docs/new/studio/chat.md).

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F2pHPTTp37UsjRmbCAzfM%2Fimage.png?alt=media&amp;token=f0840bf7-e08b-4b73-bdec-24caae22a29d" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}

#### Serve Muse Spark Open with Unsloth API

You can use `unsloth run` command and serve Muse Spark Open via an API using `llama-server` runtime flags, including context sizing, GPU layers, threading, sampling, networking, and tool configuration. For more info see our [API docs](/docs/basics/api.md) or [unsloth start](/docs/integrations/unsloth-start.md).

```bash
unsloth run --model unsloth/Muse-Spark-Open-816B-A42B-GGUF:UD-IQ2_XXS
```

{% endstep %}

{% step %}

#### Unsloth is now ready

You can also do many other things with Muse Spark Open via Unsloth Desktop like:

* **Connect tools:** [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md), [web search](/docs/new/studio/chat.md#advanced-web-search), [MCP](/docs/basics/mcp.md) and more
* **Train models:** Fine-tune text, diffusion, [embedding](/docs/basics/embedding-finetuning.md), and more
* **Generate media:** Create and train [images](/docs/basics/diffusion-image.md), video, [TTS](/docs/basics/text-to-speech-tts-fine-tuning.md) locally
  {% endstep %}
  {% endstepper %}

### KLD Benchmarks

We ran KLD benchmarks for Muse Spark Open GGUFs for general tasks and also chat tasks. Our UD-3 quants for Muse show UD-Q4\_K\_XL as having very small KLD (the lower the better). Q3\_K\_XL also is quite reasonable.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FwQAj1r2xtQU78NJLxAce%2Fmuse_spark_open_816b_kld_vs_disk.png?alt=media&amp;token=2a97b134-0deb-414b-b855-56d25a7fd1d6" alt=""><figcaption></figcaption></figure>

For top-1% accurracy, we also ran it on general tasks and chat tasks - quants below UD-IQ2\_S do degrade for general tasks, so we generally recommend using UD-IQ2\_S as the minimum quant to use for agentic tasks. Chat style tasks work fine with the smallest quants.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FwcFg5X5xzxrMiTzzzZIA%2Fmuse_spark_open_816b_top1_vs_disk.png?alt=media&amp;token=3125af4a-4ecd-47eb-8a00-12960c1239b4" alt=""><figcaption></figcaption></figure>

### 🦙 Llama.cpp Guide

For this guide we will be utilizing Dynamic 2-bit for Muse-Spark-Open-816B-A42B. See: [Muse-Spark-Open-816B-A42B GGUF](https://huggingface.co/unsloth/Muse-Spark-Open-816B-A42B-GGUF)

{% stepper %}
{% step %}
Install the specific version of llama.cpp. You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.\
\
Note <https://github.com/ggml-org/llama.cpp/pull/30616> needs to be merged for building from main to work - otherwise utilize our prebuilts at <https://github.com/unslothai/llama.cpp>

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endstep %}

{% step %}
To run the model, you can do:

{% code overflow="wrap" %}

```bash
pip install -U "huggingface_hub[cli]"
hf download unsloth/Muse-Spark-Open-816B-A42B-GGUF \
    --local-dir unsloth/Muse-Spark-Open-816B-A42B-GGUF \
    --include "*UD-IQ2_XXS*" # Use "*IQ2_XXS*" for 2-bit
```

{% endcode %}
{% endstep %}

{% step %}
Then to run it:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/Muse-Spark-Open-816B-A42B-GGUF/UD-IQ2_XXS/Muse-Spark-Open-816B-A42B-UD-IQ2_XXS-00001-of-00006.gguf \
    --temp 1.0 \
    --top-p 1.0 \
    --top-k 64
```

{% endcode %}
{% endstep %}
{% endstepper %}

### Official Benchmarks

Meta compares Muse Spark Open to other leading open-weight models of similar size and architecture. For Muse Spark Open, xhigh reasoning is enabled with, temperature = 1.0, top\_p=1.0, top\_k=disabled across benchmarks.

<table><thead><tr><th width="177.9913330078125" align="center">Benchmark</th><th>Muse Spark Open (xhigh)</th><th>Inkling (xhigh)</th><th>Nemotron 3 Ultra (think)</th><th>Beam</th><th>Mistral Large 4</th><th>Qwen3.8-2.4T-A95B (xhigh)</th><th>GLM 5.3 (max)</th><th>Kimi K3 (max)</th></tr></thead><tbody><tr><td align="center"><strong>General</strong></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td align="center"><strong>Agentic</strong></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td align="center"><strong>JobBench</strong></td><td><strong>61.8</strong></td><td>31.1</td><td>27.2</td><td>-</td><td>-</td><td>52.7</td><td>61.4</td><td>54.3</td></tr><tr><td align="center"><strong>MCP-Atlas</strong></td><td><strong>89.2</strong></td><td>76.0</td><td>63.1</td><td>78.7</td><td>-</td><td>84.5</td><td>84.2</td><td>82.3</td></tr><tr><td align="center"><strong>GDPVal-AA v2</strong></td><td>1401</td><td>1079</td><td>1016</td><td>-</td><td>1424</td><td>1613</td><td><strong>1653</strong></td><td>1537</td></tr><tr><td align="center"><strong>Artificial Analysis Intelligence Index</strong></td><td>39</td><td>26</td><td>23</td><td>-</td><td>38</td><td>40</td><td><strong>45</strong></td><td>44</td></tr><tr><td align="center"><strong>OSWorld Verified</strong></td><td>80.4</td><td>40.1</td><td>-</td><td><strong>-</strong></td><td>-</td><td>-</td><td>-</td><td><strong>84.8</strong></td></tr><tr><td align="center"><strong>Toolathlon Verified</strong></td><td>72.8</td><td>45.5</td><td>34.3</td><td><strong>-</strong></td><td>-</td><td>72.5</td><td>73.0</td><td><strong>76.5</strong></td></tr><tr><td align="center"><strong>Knowledge &#x26; Reasoning</strong></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td align="center"><strong>HLE-Diamond (no tools)</strong></td><td><strong>26.1</strong></td><td>11.2</td><td>8.9</td><td>-</td><td>-</td><td>17.3</td><td>16.4</td><td>22.2</td></tr><tr><td align="center"><strong>AA Omniscience</strong></td><td><strong>25</strong></td><td>2</td><td>0</td><td>13</td><td>-5</td><td>4</td><td>14</td><td>20</td></tr><tr><td align="center"><strong>SciCode</strong></td><td>58.5</td><td>47.0</td><td>40.3</td><td>49.7</td><td>54.2</td><td>54.1</td><td>59.0</td><td><strong>59.5</strong></td></tr><tr><td align="center"><strong>HLE (w/ tools)</strong></td><td>61.0</td><td>46.0</td><td>37.4</td><td>51.2</td><td>-</td><td>56.2</td><td><strong>62.5</strong></td><td>56.0</td></tr><tr><td align="center"><strong>GPQA Diamond</strong></td><td>89.0</td><td>87.2</td><td>86.7</td><td>90.5</td><td>-</td><td><strong>93.5</strong></td><td>91.7</td><td><strong>93.5</strong></td></tr><tr><td align="center"><strong>Coding</strong></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td align="center"><strong>DeepSWE 1.1</strong> Preferred harness</td><td>60</td><td>-</td><td>-</td><td>44</td><td>62</td><td>57</td><td>67</td><td><strong>68</strong></td></tr><tr><td align="center"><strong>SWE-Atlas-QnA</strong> Preferred harness</td><td>58</td><td>-</td><td>-</td><td>35</td><td>59</td><td>62</td><td>59</td><td><strong>66</strong></td></tr><tr><td align="center"><strong>Terminal-Bench 2.1</strong> Terminus 2 agent</td><td>76.4</td><td>55.1</td><td>53.9</td><td>80.1</td><td>-</td><td>82.0</td><td>83.9</td><td><strong>85.0</strong></td></tr><tr><td align="center"><strong>Multimodal</strong></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td align="center"><strong>ZeroBench (w/ tools)</strong></td><td><strong>50.0</strong></td><td>14.0</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>41.0</td></tr><tr><td align="center"><strong>BabyVision (w/ tools)</strong></td><td>80.2</td><td>34.2</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td><strong>85.7</strong></td></tr><tr><td align="center"><strong>SimpleVQA (w/ tools)</strong></td><td><strong>73.6</strong></td><td>52.3</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>71.9</td></tr><tr><td align="center"><strong>WorldVQA (w/ tools)</strong></td><td>49.4</td><td>18.0</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td><strong>51.0</strong></td></tr><tr><td align="center"><strong>IntPhys2</strong></td><td><strong>68.3</strong></td><td>55.2</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>60.3</td></tr><tr><td align="center"><strong>VideoMMEv2</strong></td><td>61.5</td><td>36.9</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td><strong>65.4</strong></td></tr><tr><td align="center"><strong>Safety</strong></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td align="center"><strong>FORTRESS adversarial (static)</strong> lower is better</td><td>ARS: 5.8 ORS: 17.4</td><td>ARS: 25.0 ORS: 7.4</td><td>ARS: 26.4 ORS: 13.3</td><td>-</td><td>-</td><td>ARS: 21.6 ORS: 12.8</td><td>ARS: 28.2 ORS: 3.2</td><td>ARS: 26.7 ORS: 2.7</td></tr><tr><td align="center"><strong>StrongREJECT v2 (adaptive)</strong> lower is better</td><td><strong>0.5</strong></td><td>86.4</td><td>80.7</td><td>-</td><td>-</td><td>65.6</td><td>62.9</td><td>66.6</td></tr></tbody></table>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/muse-spark-open.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
