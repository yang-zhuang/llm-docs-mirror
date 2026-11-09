> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/embeddinggemma-2.md).

# EmbeddingGemma 2 - Run Locally

Run EmbeddingGemma 2 locally and fine-tune the model with Unsloth.

**EmbeddingGemma 2** is Google’s new embedding model for text, code, images, video and audio. The model has **740M parameters**, combining a **270M** parameter **text** model with modular **vision (170M)** and **audio (300M)** encoders. It supports an Apache 2.0 license, **100+ languages** and an **8K context window** for tasks like semantic search, RAG and classification. For text and code only, you can load the smaller **270M text model**.

You can run EmbeddingGemma 2 locally via our **GGUFs** using [**Unsloth Desktop**](#use-embeddinggemma-2-in-unsloth-desktop) or even **fine-tune the model** via Unsloth. [**embeddinggemma-2-GGUF**](https://huggingface.co/unsloth/embeddinggemma-2-GGUF)

<a href="/docs/models/embeddinggemma-2.md#use-embeddinggemma-2-in-unsloth-desktop" class="button primary">Run EmbeddingGemma 2 Guide</a><a href="/docs/models/embeddinggemma-2.md#fine-tune-embeddinggemma-2-with-unsloth" class="button secondary">Fine-tuning Guide</a>

### ⚙️ Usage Guide

| Feature              | EmbeddingGemma 2                                                                        |
| -------------------- | --------------------------------------------------------------------------------------- |
| Parameters           | <p>740M total (can choose which to use):</p><p>270M text + 170M vision + 300M audio</p> |
| Inputs               | Text, code, images, video, audio and mixed inputs                                       |
| Context length       | 8,192 tokens, shared across all inputs                                                  |
| Embedding dimensions | 768, 512, 256 or 128                                                                    |

#### Recommended Settings

* **Precision:** BF16 on supported hardware, or FP32 elsewhere.
* **Dimensions:** Start with **768**. Use **512 or 256** to reduce vector storage; evaluate **128** for text workloads.
* **Normalization:** L2-normalize vectors, including after truncating them.
* **Prompts:** Use a search prompt for queries and document formatting for the content you index.

{% hint style="warning" %}
**Do not use FP16.** EmbeddingGemma 2 can produce NaN or degraded embeddings in FP16. Use BF16 or FP32, including a compatible compute dtype when loading quantized weights.
{% endhint %}

### Run EmbeddingGemma 2 Guide

<a href="/docs/models/embeddinggemma-2.md#use-embeddinggemma-2-in-unsloth-desktop" class="button primary">Unsloth Desktop Tutorial</a><a href="/pages/hj6zQkX4eMxnihJuV4CD#run-embeddinggemma-2-ggufs-in-llama.cpp" class="button secondary">Llama.cpp Tutorial</a>

#### 🦥 Use EmbeddingGemma 2 in Unsloth Desktop

Use EmbeddingGemma 2 to index and search your documents locally on **macOS, Windows and Linux**.

{% stepper %}
{% step %}

#### Install Unsloth

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

#### Search the embedding model

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FA5YLVJdX7p1jXPhQ7MMr%2Fimage.png?alt=media&amp;token=b32b20b1-3c65-4c0e-b561-93f66eb30e60" alt="" width="563"><figcaption></figcaption></figure></div>

In **Settings**, open **General** and scroll to **Documents & RAG**. Choose **EmbeddingGemma 2** from the **Embedding model** dropdown, then click **Download** if needed.

You can also use our GGUF upload if needed.
{% endstep %}

{% step %}

#### Add your documents

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fo3Mu42tY5xZ9XtitMgSq%2Fimage.png?alt=media&amp;token=823216c4-1d79-432e-b428-dacc76497fc7" alt="" width="563"><figcaption></figcaption></figure></div>

Open a chat, click **+**, and enable **Chat with Files**. Then click **Add files to chat with** and choose your documents.

Unsloth uses your selected embedding model to make the documents searchable.

{% hint style="info" %}
Changing the embedding model only affects newly indexed documents. Re-upload existing documents to use the new model.
{% endhint %}
{% endstep %}
{% endstepper %}

For more ways to run EmbeddingGemma 2 with Unsloth, follow the **Python** or **GGUF** guides below.

### 📓 Try our notebooks

Run and train EmbeddingGemma 2 in Google Colab with our step-by-step notebooks.

| Notebook                                                                                                                                          | What you can do                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| [Multimodal search](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/EmbeddingGemma2_%28300M%29-Multimodal_Search.ipynb) | Try search across text, images, video and audio.              |
| [Text fine-tuning](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/EmbeddingGemma2_%28300M%29.ipynb)                    | Fine-tune text embeddings for your data.                      |
| [Image-text fine-tuning](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/EmbeddingGemma2_%28300M%29-Image_Text.ipynb)   | Train on images and captions, then compare retrieval quality. |
| [Audio fine-tuning](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/EmbeddingGemma2_%28300M%29-Audio.ipynb)             | Train on audio and captions, then compare retrieval quality.  |

#### 🦙 Run EmbeddingGemma 2 GGUFs in llama.cpp

Run EmbeddingGemma 2 locally with [Unsloth GGUFs](https://huggingface.co/unsloth/embeddinggemma-2-GGUF). Use a llama.cpp build containing [EmbeddingGemma 2 support](https://github.com/ggml-org/llama.cpp/pull/30054); the commands below build the latest source for text and code embeddings.

{% stepper %}
{% step %}
**Build llama.cpp and download your GGUF**

Install Git, CMake and a C++ compiler, then run these commands in a new working directory. They build the latest llama.cpp source and download Unsloth’s 176 MB UD-Q4\_K\_XL GGUF:

```bash
git clone https://github.com/ggml-org/llama.cpp.git
cmake -S llama.cpp -B llama.cpp/build -DCMAKE_BUILD_TYPE=Release
cmake --build llama.cpp/build --config Release -j 8 --target llama-server

pip install -U huggingface_hub

hf download unsloth/embeddinggemma-2-GGUF embeddinggemma-2-UD-Q4_K_XL.gguf \
  --local-dir embeddinggemma2-gguf
```

{% endstep %}

{% step %}
**Start the embedding server**

This example serves **text and code embeddings**, starting with a 2,048-token context:

```bash
./llama.cpp/build/bin/llama-server \
  --model "embeddinggemma2-gguf/embeddinggemma-2-UD-Q4_K_XL.gguf" \
  --alias embeddinggemma2 \
  --embeddings \
  --pooling mean \
  --ctx-size 2048 \
  --batch-size 2048 \
  --ubatch-size 2048 \
  --parallel 1 \
  --host 127.0.0.1 \
  --port 8080
```

For inputs longer than 2,048 tokens, increase `--ctx-size`, `--batch-size` and `--ubatch-size` together, up to `8192`. Each input must fit in a single physical batch.
{% endstep %}

{% step %}
**Request embeddings**

Add the task prefixes yourself when calling the API:

```bash
curl http://127.0.0.1:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "embeddinggemma2",
    "input": [
      "task: search result | query: How do I reset my password?",
      "title: none | text: Select Forgot password to receive a reset link."
    ],
    "encoding_format": "float"
  }'
```

The embeddings endpoint returns normalized vectors. Check that each vector has 768 finite values before building your index.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
Use a GGUF and runtime that preserve EmbeddingGemma 2's learned embedding projection. For images, video or audio, use a runtime with explicit support for those encoders and their processor files. The command above covers text embeddings.
{% endhint %}

### 🛠️ Fine-tune EmbeddingGemma 2 with Unsloth

Fine-tuning can improve search for your documents, code and terminology. Train with pairs of questions and relevant documents, then compare search results before and after training.

Run and train EmbeddingGemma 2 in Google Colab with our free step-by-step notebooks.

| Notebook                                                                                                                                          | What you can do                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| [Multimodal search](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/EmbeddingGemma2_%28300M%29-Multimodal_Search.ipynb) | Try search across text, images, video and audio.              |
| [Text fine-tuning](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/EmbeddingGemma2_%28300M%29.ipynb)                    | Fine-tune text embeddings for your data.                      |
| [Image-text fine-tuning](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/EmbeddingGemma2_%28300M%29-Image_Text.ipynb)   | Train on images and captions, then compare retrieval quality. |
| [Audio fine-tuning](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/EmbeddingGemma2_%28300M%29-Audio.ipynb)             | Train on audio and captions, then compare retrieval quality.  |

#### Prepare the model

Save the text model from the Python example:

```python
text_model.save_pretrained("embeddinggemma2-text")
```

Start a fresh Python session and import Unsloth first. Load the saved model in 4-bit and add LoRA adapters for training:

```python
from unsloth import FastSentenceTransformer
import torch

model = FastSentenceTransformer.from_pretrained(
    model_name = "embeddinggemma2-text",
    max_seq_length = 1024,
    dtype = torch.bfloat16,
    load_in_4bit = True,
    load_in_16bit = False,
    full_finetuning = False,
)

model = FastSentenceTransformer.get_peft_model(
    model,
    r = 16,
    target_modules = [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_alpha = 32,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",
    random_state = 3407,
    task_type = "FEATURE_EXTRACTION",
)
```

#### Train and evaluate

Follow our [embedding fine-tuning guide](https://unsloth.ai/docs/basics/embedding-finetuning) to prepare your dataset and run `SentenceTransformerTrainer`.

* Apply the query and document prefixes once, as in the Python search example.
* Start with `MultipleNegativesRankingLoss` and a batch sampler that avoids duplicates.
* Set `bf16=True` and `fp16=False`.
* Test search quality on queries you kept out of training.

The guide’s **EmbeddingGemma 300M notebook** covers the earlier model. Use it as a workflow reference.

#### Save your adapters

After training, save the LoRA adapters:

```python
model.save_pretrained("embeddinggemma2-lora")
```

See the linked guide for merging adapters into a standalone model. Training on images, video or audio requires a separate workflow.

### 🚀 Run EmbeddingGemma 2 in Python

This example searches three documents and ranks them by how closely they match your question. It loads only the text model to save memory.

Install SentenceTransformers and Transformers with EmbeddingGemma 2 support:

```bash
pip install -U sentence-transformers transformers
```

The example automatically selects your device and a supported precision.

```python
import torch
from sentence_transformers import SentenceTransformer

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = (
    torch.bfloat16
    if device == "cuda" and torch.cuda.is_bf16_supported()
    else torch.float32
)

text_model = SentenceTransformer(
    "unsloth/embeddinggemma-2",
    device = device,
    model_kwargs = {"torch_dtype": dtype},
    config_kwargs = {"vision_config": None, "audio_config": None},
)

query = "How do I reset my password?"
documents = [
    "Select Forgot password on the sign-in page to receive a reset link.",
    "Update your billing details from the account settings page.",
    "Enable two-factor authentication to protect your account.",
]
embedding_dim = 768

query_embedding = text_model.encode(
    [query],
    prompt_name = "SearchQuery",
    truncate_dim = embedding_dim,
    normalize_embeddings = True,
)
document_embeddings = text_model.encode(
    documents,
    prompt_name = "Document",
    truncate_dim = embedding_dim,
    normalize_embeddings = True,
)

scores = text_model.similarity(query_embedding, document_embeddings)[0]
for idx in scores.argsort(descending = True).tolist():
    print(f"{scores[idx].item():.4f} | {documents[idx]}")
```

Higher scores mean a closer match. Replace the question and documents with your own content.

#### Adjust your embeddings

**Save storage:** Set `embedding_dim` to **256** to use one-third of the embedding storage, with some loss in search accuracy. Use the same dimension for queries and documents.

**Choose a prompt:** The example uses `SearchQuery` for the question and `Document` for searchable content. For code searches, use `CodeRetrieval` for the query. To compare two texts for similarity, use `SentenceSimilarity` for both.

### 🖼️ Embed images, video and audio

Combine text and media into one searchable item. This example creates a single embedding for a product description, two photos and a video.

Run it after the setup above, replacing the filenames with your own files. Your installation also needs the model processor’s image and video dependencies.

```python
multimodal_model = SentenceTransformer(
    "unsloth/embeddinggemma-2",
    device = device,
    model_kwargs = {"torch_dtype": dtype},
    config_kwargs = {"audio_config": None},
)

listing_embedding = multimodal_model.encode(
    {
        "text": "Trail running shoes. <|image|> Mesh upper. <|image|> Grip test: <|video|>",
        "image": ["shoe.jpg", "mesh.jpg"],
        "video": "demo.mp4",
    },
    prompt = "",
    normalize_embeddings = True,
)
```

Replace the filenames with your own images and video, keeping the placeholders in the same order. The model combines them into one embedding you can search with text.

{% hint style="info" %}
Audio is disabled to save memory. To include it, remove `config_kwargs` and add an `audio` input with a `<|audio|>` placeholder. Use mono audio at 16 kHz.
{% endhint %}

Text and media share the **8K context limit**. Images, video and audio don’t need task prefixes.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/embeddinggemma-2.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
