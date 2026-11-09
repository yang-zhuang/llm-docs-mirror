> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/blog/fine-tuning-llms-with-nvidia-dgx-spark-and-unsloth.md).

# Fine-tuning LLMs with NVIDIA DGX Spark and Unsloth

Tutorial on how to fine-tune and do reinforcement learning (RL) with OpenAI gpt-oss on NVIDIA DGX Spark.

Unsloth enables local fine-tuning of LLMs with up to **200B parameters** on the NVIDIA DGX™ Spark. With 128 GB of unified memory, you can train massive models such as **gpt-oss-120b**, and run or deploy inference directly on DGX Spark.

As shown at [OpenAI DevDay](https://x.com/UnslothAI/status/1976284209842118714), gpt-oss-20b was trained with RL and Unsloth on DGX Spark to auto-win 2048. You can train using Unsloth in a Docker container or virtual environment on DGX Spark.

<div align="center" data-full-width="false"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-ff5c4752dccb8f922b937f8e3b0db58e2d836507%2Funsloth%20nvidia%20dgx%20spark.png?alt=media" alt="" width="375"><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-a8472482c49e1763378b609f8f537ca89df60260%2FNotebooks%20on%20dgx.png?alt=media" alt="" width="375"><figcaption></figcaption></figure></div>

In this tutorial, we’ll train gpt-oss-20b with RL using Unsloth notebooks after installing Unsloth on your DGX Spark. gpt-oss-120b will use around **68GB** of unified memory.

After 1,000 steps and 4 hours of RL training, the gpt-oss model greatly outperforms the original on 2048, and longer training would further improve results.

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-3bdcb0fda2ad188142e58f04c855b6dcfbd5ba94%2Fopenai%20devday%20unsloth%20feature.png?alt=media" alt="" width="375"><figcaption><p>You can watch Unsloth featured on OpenAI DevDay 2025 <a href="https://youtu.be/1HL2YHRj270?si=8SR6EChF34B1g-5r&#x26;t=1080">here</a>.</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-4a8bd4ecc7ee3d123c19158df5dfdcec35df8532%2FScreenshot%202025-10-13%20at%204.22.32%E2%80%AFPM.png?alt=media" alt="" width="375"><figcaption><p>gpt-oss trained with RL consistently outperforms on 2048.</p></figcaption></figure></div>

### ⚡ Step-by-Step Tutorial

{% stepper %}
{% step %}
**Start with Unsloth Docker image for DGX Spark**

First, build the Docker image using the DGX Spark Dockerfile which can be [found here](https://raw.githubusercontent.com/unslothai/notebooks/main/Dockerfile_DGX_Spark). You can also run the below in a Terminal in the DGX Spark:

```bash
sudo apt update && sudo apt install -y wget
wget -O Dockerfile "https://raw.githubusercontent.com/unslothai/notebooks/main/Dockerfile_DGX_Spark"
```

Then, build the training Docker image using saved Dockerfile:

```bash
docker build -f Dockerfile -t unsloth-dgx-spark .
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-7ebcf195c154b0e569115e1f9513cf002ee57b16%2Fdgx1.png?alt=media" alt="" width="563"><figcaption></figcaption></figure>

<details>

<summary>You can also click to see the full DGX Spark Dockerfile</summary>

```python
FROM nvcr.io/nvidia/pytorch:25.09-py3

# Set CUDA environment variables
ENV CUDA_HOME=/usr/local/cuda-13.0/
ENV CUDA_PATH=$CUDA_HOME
ENV PATH=$CUDA_HOME/bin:$PATH
ENV LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
ENV C_INCLUDE_PATH=$CUDA_HOME/include:$C_INCLUDE_PATH
ENV CPLUS_INCLUDE_PATH=$CUDA_HOME/include:$CPLUS_INCLUDE_PATH

# Install triton from source for latest blackwell support
RUN git clone https://github.com/triton-lang/triton.git && \
    cd triton && \
    git checkout c5d671f91d90f40900027382f98b17a3e04045f6 && \
    pip install -r python/requirements.txt && \
    pip install . && \
    cd ..

# Install xformers from source for blackwell support
RUN git clone --depth=1 https://github.com/facebookresearch/xformers --recursive && \
    cd xformers && \
    export TORCH_CUDA_ARCH_LIST="12.1" && \
    python setup.py install && \
    cd ..

# Install unsloth and other dependencies
RUN pip install unsloth unsloth_zoo bitsandbytes==0.48.0 transformers==4.56.2 trl==0.22.2

# Launch the shell
CMD ["/bin/bash"]
```

</details>
{% endstep %}

{% step %}
**Launch container**

Launch the training container with GPU access and volume mounts:

```bash
docker run -it \
    --gpus=all \
    --net=host \
    --ipc=host \
    --ulimit memlock=-1 \
    --ulimit stack=67108864 \
    -v $(pwd):$(pwd) \
    -v $HOME/.cache/huggingface:/root/.cache/huggingface \
    -w $(pwd) \
    unsloth-dgx-spark
```

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-a67c36494f5c4ab4017748d490fb258655cd2378%2Fdgx2.png?alt=media" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-b7758db087ab8b724049361781952b5ed154dfe8%2Fdgx5.png?alt=media" alt=""><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}
**Start Jupyter and Run Notebooks**

Inside the container, start Jupyter and run the required notebook. You can use the Reinforcement Learning gpt-oss 20b to win 2048 [notebook here](https://github.com/unslothai/notebooks/blob/main/nb/gpt_oss_\(20B\)_Reinforcement_Learning_2048_Game_DGX_Spark.ipynb). In fact all [Unsloth notebooks](https://docs.unsloth.ai/get-started/unsloth-notebooks) work in DGX Spark including the **120b** notebook! Just remove the installation cells.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-a8472482c49e1763378b609f8f537ca89df60260%2FNotebooks%20on%20dgx.png?alt=media" alt="" width="563"><figcaption></figcaption></figure>

The below commands can be used to run the RL notebook as well. After Jupyter Notebook is launched, open up the “`gpt_oss_20B_RL_2048_Game.ipynb`”

```bash
NOTEBOOK_URL="https://raw.githubusercontent.com/unslothai/notebooks/refs/heads/main/nb/gpt_oss_(20B)_Reinforcement_Learning_2048_Game_DGX_Spark.ipynb"
wget -O "gpt_oss_20B_RL_2048_Game.ipynb" "$NOTEBOOK_URL"

jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-0862eed0acf0656ff0cb802b6aebc30892997e3b%2Fdgx6.png?alt=media" alt="" width="563"><figcaption></figcaption></figure>

Don't forget Unsloth also allows you to [save and run](/docs/basics/inference-and-deployment.md) your models after fine-tuning so you can locally deploy them directly on your DGX Spark after.
{% endstep %}
{% endstepper %}

Many thanks to [Lakshmi Ramesh](https://www.linkedin.com/in/rlakshmi24/) and [Barath Anandan](https://www.linkedin.com/in/barathsa/) from NVIDIA for helping Unsloth’s DGX Spark launch and building the Docker image.

### Unified Memory Usage

gpt-oss-120b QLoRA 4-bit fine-tuning will use around **68GB** of unified memory. How your unified memory usage should look **before** (left) and **after** (right) training:

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-e079a9aa8d853b319520fe0f0fbcca2e85b31ea6%2Fdgx7.png?alt=media" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-c389a73a48ad059bbb92121b328fa7ccc61bee95%2Fdgx8.png?alt=media" alt=""><figcaption></figcaption></figure></div>

And that's it! Have fun training and running LLMs completely locally on your NVIDIA DGX Spark!

### Video Tutorials

Thanks to Tim from [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) for providing a great fine-tuning tutorial with Unsloth on DGX Spark:

{% embed url="<https://www.youtube.com/watch?t=962s&v=zs-J9sKxvoM>" %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/blog/fine-tuning-llms-with-nvidia-dgx-spark-and-unsloth.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
