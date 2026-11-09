> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/multi-gpu-training-with-unsloth/ddp.md).

# Multi-GPU Fine-tuning with Distributed Data Parallel (DDP)

Learn how to use the Unsloth CLI to train on multiple GPUs with Distributed Data Parallel (DDP)!

Let’s assume we have multiple GPUs, and we want to fine-tune a model using all of them! To do so, the most straightforward strategy is to use Distributed Data Parallel (DDP), which creates one copy of the model on each GPU device, feeding each copy distinct samples from the dataset during training and aggregating their contributions to weight updates per optimizer step.

Why would we want to do this? Well, as we add more GPUs into the training process, we scale the number of samples our models train on per step, making each gradient update more stable and increasing our training throughput dramatically with each added GPU.

Here’s a step-by-step guide on how to do this using Unsloth’s command-line interface (CLI)!

**Note:** Unsloth DDP will work with any of your training scripts, not just via our CLI! More details below.

#### Install Unsloth from source

We’ll clone Unsloth from GitHub and install it. Please consider using a [virtual environment](https://docs.python.org/3/tutorial/venv.html); we like to use `uv venv –python 3.12 && source .venv/bin/activate`, but any virtual environment creation tooling will do.

```bash
git clone https://github.com/unslothai/unsloth.git
cd unsloth
pip install .
```

#### Choose target model and dataset for finetuning

In this demo, we will fine-tune [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) on the [yahma/alpaca-cleaned](https://huggingface.co/datasets/yahma/alpaca-cleaned) chat dataset. This is a Supervised Fine-Tuning (SFT) workload that is commonly used when attempting to adapt a base model to a desired conversational style, or improve the model’s performance on a downstream task.

### Use the Unsloth CLI!

First, let’s take a look at the help message built-in to the CLI (we’ve abbreviated here with “...” in various places for brevity):

{% code expandable="true" %}

```bash
$ python unsloth-cli.py --help
usage: unsloth-cli.py [-h] [--model_name MODEL_NAME] [--max_seq_length MAX_SEQ_LENGTH] [--dtype DTYPE]
                      [--load_in_4bit] [--dataset DATASET] [--r R] [--lora_alpha LORA_ALPHA]
                      [--lora_dropout LORA_DROPOUT] [--bias BIAS]
                      [--use_gradient_checkpointing USE_GRADIENT_CHECKPOINTING]
…

🦥 Fine-tune your llm faster using unsloth!

options:
  -h, --help            show this help message and exit

🤖 Model Options:
  --model_name MODEL_NAME
                        Model name to load
  --max_seq_length MAX_SEQ_LENGTH
                        Maximum sequence length, default is 2048. We auto support RoPE Scaling
                        internally!
…

🧠 LoRA Options:
  These options are used to configure the LoRA model.

  --r R                 Rank for Lora model, default is 16. (common values: 8, 16, 32, 64, 128)
  --lora_alpha LORA_ALPHA
                        LoRA alpha parameter, default is 16. (common values: 8, 16, 32, 64, 128)
…

🎓 Training Options:
  --per_device_train_batch_size PER_DEVICE_TRAIN_BATCH_SIZE
                        Batch size per device during training, default is 2.
  --per_device_eval_batch_size PER_DEVICE_EVAL_BATCH_SIZE
                        Batch size per device during evaluation, default is 4.
  --gradient_accumulation_steps GRADIENT_ACCUMULATION_STEPS
                        Number of gradient accumulation steps, default is 4.
…
```

{% endcode %}

This should give you a sense of what options are available for you to pass into the CLI for training your model!

For multi-GPU training (DDP in this case), we will use the [torchrun](https://docs.pytorch.org/docs/stable/elastic/run.html) launcher, which allows you to spin up multiple distributed training processes in single-node or multi-node settings. In our case, we will focus on the single-node (i.e., one machine) case with two H100 GPUs.

Let’s also check our GPUs’ status by using the `nvidia-smi` command-line tool:

{% code expandable="true" %}

```bash
$ nvidia-smi
Mon Nov 24 12:53:00 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.95.05              Driver Version: 580.95.05      CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA H100 80GB HBM3          On  |   00000000:04:00.0 Off |                    0 |
| N/A   32C    P0             69W /  700W |       0MiB /  81559MiB |      0%      Default |
|                                         |                        |             Disabled |
+-----------------------------------------+------------------------+----------------------+
|   1  NVIDIA H100 80GB HBM3          On  |   00000000:05:00.0 Off |                    0 |
| N/A   30C    P0             68W /  700W |       0MiB /  81559MiB |      0%      Default |
|                                         |                        |             Disabled |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

{% endcode %}

Great! We have two H100 GPUs, as expected. Both are sitting at 0MiB memory usage as we’re currently not training anything, or have any model loaded into memory.

To start your training run, issue a command like the following:

{% code expandable="true" %}

```bash
# required:
#   --model_name
#   --dataset
# optional; experiment with these:
#   --learning_rate, --max_seq_length, --per_device_train_batch_size, --gradient_accumulation_steps, --max_steps
# to save the model at the end of training:
#   --save_model

torchrun --nproc_per_node=2 unsloth-cli.py \
  --model_name=Qwen/Qwen3-8B \
  --dataset=yahma/alpaca-cleaned \
  --learning_rate=2e-5 \
  --max_seq_length=2048 \
  --per_device_train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --max_steps=1000 \
  --save_model
```

{% endcode %}

If you have more GPUs, you may set `--nproc_per_node` accordingly to utilize them.

**Note:** You can use the `torchrun` launcher with any of your Unsloth training scripts, including the [scripts](https://github.com/unslothai/notebooks/tree/main/python_scripts) converted from our free Colab notebooks, and DDP will be auto-enabled when training with >1 GPU!

Taking a look again at `nvidia-smi` while training is in-flight:

{% code expandable="true" %}

```bash
$ nvidia-smi
Mon Nov 24 12:58:42 2025
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.95.05              Driver Version: 580.95.05      CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA H100 80GB HBM3          On  |   00000000:04:00.0 Off |                    0 |
| N/A   38C    P0            193W /  700W |   18903MiB /  81559MiB |     25%      Default |
|                                         |                        |             Disabled |
+-----------------------------------------+------------------------+----------------------+
|   1  NVIDIA H100 80GB HBM3          On  |   00000000:05:00.0 Off |                    0 |
| N/A   37C    P0            199W /  700W |   18905MiB /  81559MiB |     28%      Default |
|                                         |                        |             Disabled |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A            4935      C   ...und/unsloth/.venv/bin/python3      18256MiB |
|    0   N/A  N/A            4936      C   ...und/unsloth/.venv/bin/python3        630MiB |
|    1   N/A  N/A            4935      C   ...und/unsloth/.venv/bin/python3        630MiB |
|    1   N/A  N/A            4936      C   ...und/unsloth/.venv/bin/python3      18258MiB |
+-----------------------------------------------------------------------------------------+
```

{% endcode %}

We can see that both GPUs are now using \~19GB of VRAM per H100 GPU!

Inspecting the training logs, we see that we’re able to train at a rate of \~1.1 iterations/s. This training speed is \~constant even as we add more GPUs, so our training throughput increases \~linearly with the number of GPUs!

### Training metrics

We ran a few short rank-16 LoRA fine-tunes on [unsloth/Llama-3.2-1B-Instruct](https://huggingface.co/unsloth/Llama-3.2-1B-Instruct) on the [yahma/alpaca-cleaned](https://huggingface.co/datasets/yahma/alpaca-cleaned) dataset to demonstrate the improved training throughput when using DDP training with multiple GPUs.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FdySJnhNUzVD3gsWmPqHR%2Funknown.png?alt=media&amp;token=9905cccb-04c8-45b1-bfb1-680823713319" alt="" width="375"><figcaption></figcaption></figure>

The above figure compares training loss between two Llama-3.2-1B-Instruct LoRA fine-tunes over 500 training steps, with single GPU training (pink) vs. multi-GPU DDP training (blue).

Notice that the loss curves match in scale and trend, but otherwise are a *bit* different, since *the multi-GPU training processes twice as much training data per step*. This results in a slightly different training curve with less variability on a step-by-step basis.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fz4XgknzMgljaFInMEzHc%2Funknown.png?alt=media&amp;token=4e28e2b1-8bc8-4049-983d-e4f980f3f4cf" alt="" width="375"><figcaption></figcaption></figure>

The above figure plots training progress for the same two fine-tunes.

Notice that the multi-GPU DDP training progresses through an epoch of the training data in half as many steps as single GPU training. This is because each GPU can process a distinct batch (of size `per_device_train_batch_size`) per step. However, the per-step timing for DDP training is slightly slower due to distributed communication for the model weight updates. As you increase the number of GPUs, the training throughput will continue to increase \~linearly (but with a small, but increasing penalty for the distributed comms).

These same loss and training epoch progress behaviors hold for QLoRA fine-tunes, in which we loaded the base models in 4-bit precision in order to save additional GPU memory. This is particularly useful for training large models on limited amounts of GPU VRAM:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FUrCEgA7OBVhc8ICkMaP6%2Funknown.png?alt=media&amp;token=0f5de3df-77df-4ee5-bf7a-68dead857c9a" alt="" width="375"><figcaption></figcaption></figure>

Training loss comparison between two Llama-3.2-1B-Instruct QLoRA fine-tunes over 500 training steps, with single GPU training (orange) vs. multi-GPU DDP training (purple).

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F8cG6rjmjeznNfgWrYdnG%2Funknown.png?alt=media&amp;token=d1c2c1fe-c117-49b5-8e9d-fdc01154cc01" alt="" width="375"><figcaption></figcaption></figure>

Training progress comparison for the same two fine-tunes.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/multi-gpu-training-with-unsloth/ddp.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
