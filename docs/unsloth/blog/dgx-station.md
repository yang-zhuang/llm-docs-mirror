> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/blog/dgx-station.md).

# Fine-Tuning LLMs on NVIDIA DGX Station with Unsloth

NVIDIA DGX Station tutorial on how to fine-tune with notebooks from Unsloth.

You can now train LLMs locally on your NVIDIA DGX Station with [Unsloth](https://github.com/unslothai/unsloth). DGX Station has more than **\~200GB VRAM** and over **700GB of unified GPU / CPU memory** and combines a Grace CPU and a Blackwell GPU in a tightly connected system designed for large-scale AI workloads. Linked by NVLink-C2C, the CPU and GPU remain distinct but work together far more efficiently than in a traditional CPU-GPU setup.

In this guide, we’ll use Unsloth notebooks train [Qwen3.5](#qwen3.5-35b-a3b-fine-tuning) and [gpt-oss-120b](#gpt-oss-120b-fine-tuning) on DGX Station. Thank you to NVIDIA for providing some early access DGX Station hardware to test Unsloth on!

### Quickstart

You will need `python3` installed and in particular the dev headers are needed. On our system we have `python 3.12` so we will install the 3.12 dev headers.

```bash
sudo apt update
sudo apt install python3.12-dev
```

Then create a fresh virtual environment to install [Unsloth](https://github.com/unslothai/unsloth). This way we minimize dependency conflicts and preserve the state of the current working environment.&#x20;

{% code overflow="wrap" %}

```bash
python3 -m venv .unsloth
source .unsloth/bin/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130
```

{% endcode %}

{% hint style="warning" %}
First install `torch` from the `cuda 13` index otherwise we could get the CPU version or a mismatch in architecture and capabilities!
{% endhint %}

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fw04Su0JZriUaQxD31wf0%2Funknown.png?alt=media&amp;token=83e61cdb-74c3-42c4-a1ff-18cec3752c9e" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F9bs6h6YxI2hqnqOz1bU0%2Funknown.png?alt=media&amp;token=e3e261b5-be18-4d49-9f38-526012add332" alt=""><figcaption></figcaption></figure></div>

Now we can install Unsloth:

```bash
pip install unsloth
```

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FhQZznPQ8O9Wh3At6FclO%2Funknown.png?alt=media&amp;token=34c8de6e-bef8-414c-8e1b-2913589c4b10" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FdLZCFmln5LaUWtO6eC4A%2Funknown.png?alt=media&amp;token=ce04e025-32c7-4847-ac35-bee1baf6259f" alt=""><figcaption></figcaption></figure></div>

Now lets install `xformers` and optionally build `flash-attention` from source. Both packages take time so please be patient while they build.

{% code overflow="wrap" expandable="true" %}

```bash
pip install --no-deps --no-build-isolation xformers==0.0.33.post1
# Optionally flash-attn
# Clone and build (targets sm_100 for B300) 
git clone https://github.com/Dao-AILab/flash-attention
cd flash-attention 
# B300 = sm_100, set arch explicitly 
TORCH_CUDA_ARCH_LIST="10.0" MAX_JOBS=8 pip install . --no-build-isolation
cd ..
```

{% endcode %}

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FnyczIn3YvXAPx5oIfZQQ%2Funknown.png?alt=media&amp;token=1a2c5f7b-13c5-4f5e-b4c4-61df8d5fc653" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FoupUFzx2pOG6l5B91Pw4%2Funknown.png?alt=media&amp;token=009d2c73-5992-4593-8fd0-e7d813eda3ff" alt=""><figcaption></figcaption></figure></div>

{% columns %}
{% column %}
For Qwen 3.5 MoE we’ll want to download two kernel packages `flash-linear-attention` and `causal-conv1d` to make it fast.

{% code overflow="wrap" expandable="true" %}

```bash
pip install --no-build-isolation flash-linear-attention causal_conv1d==1.6.0
```

{% endcode %}
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F4xEY8k3jzxfOgMWAgJD7%2Funknown.png?alt=media&amp;token=2b8bd62e-23cd-4bcf-a0af-6d161d1ec1a1" alt="" width="375"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

If you don’t already have a notebook client, install one. For this guide we will use Jupyter Notebook:

{% code overflow="wrap" expandable="true" %}

```bash
cd ..
pip install notebook
pip install ipywidgets
```

{% endcode %}

Finally we download the actual Unsloth notebooks to run. There are 250+ notebooks for LLM Training as well as Python scripts.

{% code overflow="wrap" expandable="true" %}

```bash
git clone https://github.com/unslothai/notebooks.git
cd notebooks
```

{% endcode %}

### Training Tutorials

{% columns %}
{% column %}
Now we can launch Jupyter Notebook and navigate to the UI on a browser.

{% code overflow="wrap" expandable="true" %}

```bash
jupyter notebook
```

{% endcode %}
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FP2seywdWvLHHQkdP8DGy%2Funknown.png?alt=media&amp;token=ca1b5390-5eb8-416b-a3e9-d9df9b27fb0b" alt="" width="375"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}
Copy and paste the `localhost` site with token parameter and paste into your browser. You should see something like:

The `nb` folder has all the notebooks to run.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FSxN976oDM4WaG5EtpSc9%2Funknown.png?alt=media&amp;token=7113ba12-5bcc-4bc6-9777-b9d4c440d0bf" alt="" width="375"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

#### Qwen3.5-35B-A3B Training

{% columns %}
{% column %}
Open the file `nb/Qwen3_5_MoE.ipynb`. Skip past the installation section since we already installed everything we need beforehand. Navigate to the Unsloth section and start executing cells from there.

{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fif8mAvc1au9Hl83IZzNm%2FDGX%20Station.png?alt=media&amp;token=1011c8a9-c6ba-48df-a726-d3bc3bc8e947" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}
The notebook covers model setup, dataset preparation, and trainer configuration. Each step can take some time as we are downloading a very large model, initializing billions of weights, and further optimizing to make it run fast.&#x20;
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F4v0NmHdhiYCHFll8U8OD%2Funknown.png?alt=media&amp;token=69e3d279-4d59-4439-802f-11bd02fe39d3" alt="" width="375"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

Training is very fast with the default setting. On the DGX Station there is plenty of memory so you can play with the default training hyper parameters to really push the memory and compute. Once done training you can save the model for later, push the model to Hugging Face Hub to share with others, or export to a quantized format.

#### gpt-oss-120b Training

{% columns %}
{% column %}
Open the file `nb/gpt-oss-(120B)_A100-Fine-tuning.ipynb`. Skip past the installation section since we already installed the prerequisites and navigate to the Unsloth section. We can start running the notebook from there. The notebook will use around 72 GB of GPU memory and take about 10 minutes.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F8jYYievlemxDJBatevNV%2FDGX%20Station%202.png?alt=media&amp;token=efef1a26-a170-4690-972f-1a7cde67e9ea" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column %}
Each cell can take some time to run as we need to download the model, initialize the weights, and further optimize for a fast experience. The notebook goes through dataset preprocessing and trainer setup. Once we get to the `trainer.train()` cell and execute training begins.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FOxuma3ZZeEbxZrAWIgnq%2FDGX%20Station%203.png?alt=media&amp;token=17beb84e-eb56-4357-aee2-078c4db3eb84" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

Now that it’s complete we can save the model for later use, push to Hugging Face Hub to share with the world, or export it to GGUF format.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fy1UxtQ01avFK5BIkofwt%2Fimage.png?alt=media&amp;token=8d137818-a3a6-4d00-a9fd-1e41ed0483a5" alt=""><figcaption></figcaption></figure>

Read more about NVIDIA's DGX Station at <https://www.nvidia.com/en-us/products/workstations/dgx-station/>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/blog/dgx-station.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
