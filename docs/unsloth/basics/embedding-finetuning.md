> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/embedding-finetuning.md).

# Fine-tuning Embedding Models with Unsloth Guide

Learn how to easily fine-tune embedding models with Unsloth.

Fine-tuning embedding models can largely improve retrieval and RAG performance on specific tasks. It aligns the model's vectors with your domain and the kind of 'similarity' that matters for your use case, which improves search, RAG, clustering, and recommendations on your data.

Example: The headlines “Google launches Pixel 10” and “Qwen releases Qwen3” might be embedded as similar if you’re just labeling both as 'Tech,' but not similar if you’re doing semantic search because they’re about different things. Fine-tuning helps the model make the 'right' kind of similarity for your use case, reducing errors and improving results.

[**Unsloth**](https://github.com/unslothai/unsloth) now supports training embedding, **classifier**, **BERT**, **reranker** models [**\~1.8-3.3x faster**](#unsloth-benchmarks) with 20% less memory and 2x longer context than other Flash Attention 2 implementations - no accuracy degradation. EmbeddingGemma-300M works on just **3GB VRAM**. You can use your trained **model anywhere**: transformers, LangChain, Ollama, vLLM, llama.cpp etc.

Unsloth uses [SentenceTransformers](https://github.com/huggingface/sentence-transformers) to support compatible models like Qwen3-Embedding, BERT and more. **Even if there's no notebook or upload, it’s still supported.**

**We created free fine-tuning notebooks, with 3 main use-cases:**

| [EmbeddingGemma (300M)](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/EmbeddingGemma_\(300M\).ipynb)   | [Qwen3-Embedding 4B](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_Embedding_\(4B\).ipynb) • [0.6B](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_Embedding_\(0_6B\).ipynb) | [BGE M3](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/BGE_M3.ipynb)                        |
| ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| [ModernBERT](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/bert_classification.ipynb) - classification | [All-MiniLM-L6-v2](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/All_MiniLM_L6_v2.ipynb)                                                                                                                            | [ModernBERT-large](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/bert_classification.ipynb) |

* `All-MiniLM-L6-v2`: produce compact, domain-specific sentence embeddings for semantic search, retrieval, and clustering, tuned on your own data.
* `tomaarsen/miriad-4.4M-split`: embed medical questions and biomedical papers for high-quality medical semantic search and RAG.
* `electroglyph/technical`: better capture meaning and semantic similarity in technical text (docs, specs, and engineering discussions).

You can view the rest of our uploaded models in [our collection here](https://huggingface.co/collections/unsloth/embedding-models).

> A huge thanks to Unsloth contributor [**electroglyph**](https://github.com/unslothai/unsloth/pull/3719), whose work was significant to support this. You can check out electroglyph’s custom models on Hugging Face [here](https://huggingface.co/electroglyph).

### 🦥 Unsloth Features

* LoRA/QLoRA or full fine-tuning for embeddings, without needing to rewrite your pipeline
* Best support for encoder-only `SentenceTransformer` models (with a `modules.json`)
* Cross-encoder models are confirmed to train properly even under the fallback path
* This release also supports `transformers v5`

There is limited support for models without `modules.json` (we’ll auto-assign default `SentenceTransformers` pooling modules). If you’re doing something custom (custom heads, nonstandard pooling), double-check outputs like the pooled embedding behavior.

Some models needed custom additions such as MPNet or DistilBERT were enabled by patching gradient checkpointing into the `transformers` models.

### 🛠️ Fine-tuning Workflow

The new fine-tuning flow is centered around `FastSentenceTransformer`.

Main save/push methods:

* `save_pretrained()` Saves **LoRA adapters** to a local folder
* `save_pretrained_merged()` Saves the **merged model** to a local folder
* `push_to_hub()` Pushes **LoRA adapters** to Hugging Face
* `push_to_hub_merged()` Pushes the **merged model** to Hugging Face

**And one very important detail: Inference loading requires `for_inference=True`**

`from_pretrained()` is similar to Lacker’s other fast classes, with **one exception**:

* To load a model for **inference** using `FastSentenceTransformer`, you **must** pass: `for_inference=True`

So your inference loads should look like:

```python
model = FastSentenceTransformer.from_pretrained(
    "sentence-transformers/all-MiniLM-L6-v2",
    for_inference=True,
)
```

For Hugging Face authorization, if you run:

```
hf auth login
```

inside the same virtualenv before calling the hub methods, then:

* `push_to_hub()` and `push_to_hub_merged()` **don’t require a token argument**.

### ✅ Inference and Deploy Anywhere! <a href="#docs-internal-guid-c10bfa80-7fff-446e-714d-732eebcd72d6" id="docs-internal-guid-c10bfa80-7fff-446e-714d-732eebcd72d6"></a>

Your fine-tuned Unsloth model can be used and deployed with all major tools: transformers, LangChain, Weaviate,  sentence-transformers, Text Embeddings Inference (TEI), vLLM, and llama.cpp, custom embedding API, pgvector, FAISS/vector databases, and any RAG framework.

There is no lock in as the fine-tuned model can later be downloaded locally on your own device.

```python
# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("<your-unsloth-finetuned-model")

query = "Which planet is known as the Red Planet?"
documents = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet."
]

# 2. Encode via encode_query and encode_document to automatically use the right prompts, if needed
query_embedding = model.encode_query(query)
document_embedding = model.encode_document(documents)
print(query_embedding.shape, document_embedding.shape)

# 3. Compute similarity, e.g. via the built-in similarity helper function
similarity = model.similarity(query_embedding, document_embedding)
print(similarity)
```

### 📊 Unsloth Benchmarks

Unsloth's advantages include speed for embedding fine-tuning! We show we are consistently **1.8 to 3.3x faster** on a wide variety of embedding models and on different sequence lengths from 128 to 2048 and longer.

EmbeddingGemma-300M QLoRA works on just **3GB VRAM** and LoRA works on 6GB VRAM.

Below are our Unsloth benchmarks in a heatmap vs. `SentenceTransformers` + Flash Attention 2 (FA2) for 4bit QLoRA. **For 4bit QLoRA, Unsloth is 1.8x to 2.6x faster:**

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQqagyYR6DebgX768A0HV%2Foutput(16).png?alt=media&amp;token=e3ea6510-b129-401a-83ae-301d01865547" alt=""><figcaption></figcaption></figure>

Below are our Unsloth benchmarks in a heatmap vs. `SentenceTransformers` + Flash Attention 2 (FA2) for 16bit LoRA. **For 16bit LoRA, Unsloth is 1.2x to 3.3x faster:**

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FTl12zuBg68ZPSyOC9hUe%2Foutput(15).png?alt=media&amp;token=47d7cade-7eac-4366-8011-7034de087431" alt=""><figcaption></figcaption></figure>

### 🔮 Model Support

Here are some popular embedding models Unsloth supports (not all models are listed here):

```
Alibaba-NLP/gte-modernbert-base
BAAI/bge-large-en-v1.5
BAAI/bge-m3
BAAI/bge-reranker-v2-m3
Qwen/Qwen3-Embedding-0.6B
answerdotai/ModernBERT-base
answerdotai/ModernBERT-large
google/embeddinggemma-300m
intfloat/e5-large-v2
intfloat/multilingual-e5-large-instruct
mixedbread-ai/mxbai-embed-large-v1
sentence-transformers/all-MiniLM-L6-v2
sentence-transformers/all-mpnet-base-v2
Snowflake/snowflake-arctic-embed-l-v2.0
```

Most [common models](https://huggingface.co/models?library=sentence-transformers) are already supported. If there’s an encoder-only model you’d like that isn’t, feel free to open a [GitHub issue](https://github.com/unslothai/unsloth/issues) requesting it.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/embedding-finetuning.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
