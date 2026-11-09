> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/lfm2.5.md).

# Liquid LFM2.5: How To Run & Fine-tune

Run and fine-tune LFM2.5 Instruct and Vision locally on your device!

Liquid AI releases LFM2.5, including their [instruct](#run-lfm2.5-1.2b-instruct) and [vision](#liquid-lfm2.5-1.2b-vl-guide) model. LFM2.5-1.2B-Instruct is a 1.17B parameter hybrid reasoning model trained on **28T tokens** and RL, delivering best-in-class performance at the 1B scale for instruction following, tool use, and agentic tasks. See [Hugging Face Jobs](/docs/basics/inference-and-deployment/deploying-llms-with-hugging-face-jobs.md) on using Codex to train LFM!

LFM2.5 runs on under **1GB RAM** and achieves **239 tok/s** decode on AMD CPU. You can also [**fine-tune** it locally](#fine-tuning-lfm2.5-with-unsloth) with Unsloth.

<a href="/pages/CixcWjfA7MpVVdwbzTmg#run-lfm2.5-1.2b-instruct" class="button primary">Text LFM2.5-Instruct</a><a href="/pages/CixcWjfA7MpVVdwbzTmg#liquid-lfm2.5-1.2b-vl-guide" class="button primary">Vision LFM2.5-VL</a>

| Dynamic GGUFs                                                                         | 16-bit Instruct                                                             |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [LFM2.5-1.2B-Instruct-GGUF](https://huggingface.co/unsloth/LFM2.5-1.2B-Instruct-GGUF) | [LFM2.5-1.2B-Instruct](https://huggingface.co/unsloth/LFM2.5-1.2B-Instruct) |

**Model Specifications:**

* **Parameters**: 1.17B
* **Architecture**: 16 layers (10 double-gated LIV convolution blocks + 6 GQA blocks)
* **Training Budget**: 28T tokens
* **Context Length**: 32,768 tokens
* **Vocabulary Size**: 65,536
* **Languages**: English, Arabic, Chinese, French, German, Japanese, Korean, Spanish

### ⚙️ Usage Guide

Liquid AI recommends these settings for inference:

* `temperature = 0.1`
* `top_k = 50`
* `top_p = 0.1`
* `repetition_penalty = 1.05`
* Maximum context length: `32,768`

#### Chat Template Format

LFM2.5 uses a ChatML-like format:

```python
tokenizer.apply_chat_template([
    {"role": "system", "content": "You are a helpful assistant trained by Liquid AI."},
    {"role": "user", "content": "What is C. elegans?"},
], add_generation_prompt=True, tokenize=False)
```

**LFM2.5 chat template:**

```
<|startoftext|><|im_start|>system
You are a helpful assistant trained by Liquid AI.<|im_end|>
<|im_start|>user
What is C. elegans?<|im_end|>
<|im_start|>assistant
```

#### Tool Use

LFM2.5 supports function calling with special tokens `<|tool_call_start|>` and `<|tool_call_end|>`. Provide tools as a JSON object in the system prompt:

```
<|startoftext|><|im_start|>system
List of tools: [{"name": "get_weather", "description": "Gets the current weather", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}}]<|im_end|>
<|im_start|>user
What's the weather in Paris?<|im_end|>
<|im_start|>assistant
<|tool_call_start|>[get_weather(city="Paris")]<|tool_call_end|>
```

### 🖥️ Run LFM2.5-1.2B-Instruct

#### 📖 llama.cpp Tutorial (GGUF)

**1. Build llama.cpp**

Obtain the latest `llama.cpp` from [GitHub](https://github.com/ggml-org/llama.cpp). Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-server
cp llama.cpp/build/bin/llama-* llama.cpp
```

**2. Run directly from Hugging Face**

```bash
./llama.cpp/llama-cli \
    -hf LiquidAI/LFM2.5-1.2B-Instruct-GGUF:Q4_K_M \
    --jinja --ctx-size 32768 \
    --temp 0.1 --top-k 50 --top-p 0.1 --repeat-penalty 1.05
```

**3. Or download the model first**

```python
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id="LiquidAI/LFM2.5-1.2B-Instruct-GGUF",
    local_dir="LiquidAI/LFM2.5-1.2B-Instruct-GGUF",
    allow_patterns=["*Q4_K_M*"],
)
```

**4. Run in conversation mode**

```bash
./llama.cpp/llama-cli \
    --model LiquidAI/LFM2.5-1.2B-Instruct-GGUF/LFM2.5-1.2B-Instruct-Q4_K_M.gguf \
    --ctx-size 32768 \
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.1 \
    --top-k 50 \
    --top-p 0.1 \
    --repeat-penalty 1.05 \
    --jinja
```

### 🦥 Fine-tuning LFM2.5 with Unsloth

Unsloth supports fine-tuning LFM2.5 models. The 1.2B model fits comfortably on a free Colab T4 GPU. Training is 2x faster with 50% less VRAM.

**Free Colab Notebook:**

* [LFM2.5-1.2B-Instruct SFT LoRA notebook](https://colab.research.google.com/drive/1vGRg4ksRj__6OLvXkHhvji_Pamv801Ss?usp=sharing)
* [LFM2.5-1.2B-Instruct GRPO LoRA notebook](https://colab.research.google.com/drive/1mIikXFaGvcW4vXOZXLbVTxfBRw_XsXa5?usp=sharing)
* [LFM2.5-1.2B-Base Continued Pretraining (text completion) notebook](https://colab.research.google.com/drive/10fm7eNMezs-DSn36mF7vAsNYlOsx9YZO?usp=sharing)
* [LFM2.5-1.2B-Base Continued Pretraining (translation) notebook](https://colab.research.google.com/drive/1gaP8yTle2_v35Um8Gpu9239fqbU7UgY8?usp=sharing)

LFM2.5 is recommended for agentic tasks, data extraction, RAG, and tool use. It is not recommended for knowledge-intensive tasks or programming.

#### Unsloth Config for LFM2.5

```python
from unsloth import FastLanguageModel
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="LiquidAI/LFM2.5-1.2B-Instruct",
    max_seq_length=4096,
    load_in_4bit=False,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules = ["q_proj", "k_proj", "v_proj", "out_proj", "in_proj",
                      "w1", "w2", "w3"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
)
```

#### Training Setup

```python
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import is_bfloat16_supported

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=4096,
    dataset_num_proc=2,
    packing=False,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=60,
        learning_rate=2e-4,
        fp16=not is_bfloat16_supported(),
        bf16=is_bfloat16_supported(),
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        output_dir="outputs",
    ),
)

trainer.train()
```

#### Save and Export

```python
# Save LoRA adapters
model.save_pretrained("lfm25_lora")
tokenizer.save_pretrained("lfm25_lora")

# Merge and save to 16bit
model.save_pretrained_merged("lfm25_merged", tokenizer, save_method="merged_16bit")

# Export to GGUF
model.save_pretrained_gguf("lfm25_gguf", tokenizer, quantization_method="q4_k_m")
```

### 🎉 llama-server Serving & Deployment

To deploy LFM2.5 for production with an OpenAI-compatible API:

```bash
./llama.cpp/llama-server \
    --model LiquidAI/LFM2.5-1.2B-Instruct-GGUF/LFM2.5-1.2B-Instruct-Q4_K_M.gguf \
    --alias "LiquidAI/LFM2.5-1.2B-Instruct" \
    --threads -1 \
    --n-gpu-layers 99 \
    --ctx-size 32768 \
    --port 8001 \
    --temp 0.1 \
    --top-k 50 \
    --top-p 0.1 \
    --repeat-penalty 1.05 \
    --jinja
```

**Test with OpenAI client:**

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8001/v1",
    api_key="sk-no-key-required",
)

completion = client.chat.completions.create(
    model="LiquidAI/LFM2.5-1.2B-Instruct",
    messages=[{"role": "user", "content": "What is 2+2?"}],
)
print(completion.choices[0].message.content)
```

### 📊 Benchmarks

LFM2.5-1.2B-Instruct delivers best-in-class performance at the 1B scale and offers fast CPU inference with low memory usage:

![](https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/dxnYF2fuLpulismtFSGFi.png) ![](https://cdn-uploads.huggingface.co/production/uploads/61b8e2ba285851687028d395/dbbI-15p9re2ROhAkqnZm.png)

## 💧 Liquid LFM2.5-1.2B-VL Guide

LFM2.5-VL-1.6B is a vision LLM built on top of [LFM2.5-1.2B-Base](https://huggingface.co/LiquidAI/LFM2.5-1.2B-Base) and tuned for stronger real-world performance. You can now **fine-tune** it locally with Unsloth.

<a href="/pages/CixcWjfA7MpVVdwbzTmg#run-lfm2.5-vl-1.6b" class="button primary">Running Tutorial</a><a href="/pages/CixcWjfA7MpVVdwbzTmg#fine-tuning-lfm2.5-with-unsloth-1" class="button primary">Fine-tuning Tutorial</a>

| Dynamic GGUFs                                                             | 16-bit Instruct                                                 |
| ------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [LFM2.5-VL-1.6B-GGUF](https://huggingface.co/unsloth/LFM2.5-VL-1.6B-GGUF) | [LFM2.5-VL-1.6B](https://huggingface.co/unsloth/LFM2.5-VL-1.6B) |

**Model Specifications:**

* **LM Backbone**: LFM2.5-1.2B-Base
* **Vision encoder**: SigLIP2 NaFlex shape-optimized 400M
* **Context length**: 32,768 tokens
* **Vocabulary size**: 65,536
* **Languages**: English, Arabic, Chinese, French, German, Japanese, Korean, and Spanish
* **Native resolution processing**: Handles images up to 512×512 pixels without upscaling and preserves non-standard aspect ratios without distortion
* **Tiling strategy**: Splits large images into non-overlapping 512×512 patches and includes thumbnail encoding for global context
* **Inference-time flexibility**: User-tunable maximum image tokens and tile count for speed/quality tradeoff without retraining

### :gear: Usage Guide

Liquid AI recommends these settings for inference:

* **Text**: `temperature=0.1`, `min_p=0.15`, `repetition_penalty=1.05`
* **Vision**: min\_image\_tokens=64, max\_image\_tokens=256, do\_image\_splitting=True

#### Chat Template Format

LFM2.5-VL uses a ChatML-like format:

```python
tokenizer.apply_chat_template([
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": "What's in this image?"}
        ]
    },
    {"role": "assistant", "content": "I can see a cat sitting on a couch."}
], tokenize=False)
```

**LFM2.5-VL chat template:**

```
<|startoftext|><|im_start|>system
You are a helpful multimodal assistant by Liquid AI.<|im_end|>
<|im_start|>user
<image>Describe this image.<|im_end|>
<|im_start|>assistant
This image shows a Caenorhabditis elegans (C. elegans) nematode.<|im_end|>
```

### 🖥️  Run LFM2.5-VL-1.6B

#### :book: llama.cpp Tutorial (GGUF)

**1. Build llama.cpp**

Obtain the latest llama.cpp from [GitHub](https://github.com/ggml-org/llama.cpp). Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-server
cp llama.cpp/build/bin/llama-* llama.cpp
```

**2. Run directly from Hugging Face**

```bash
./llama.cpp/llama-cli \
  -hf LiquidAI/LFM2.5-VL-1.6B-GGUF:Q4_0 \
  --image test_image.jpg \
  --image-max-tokens 64 \
  -p "What's in this image?" \
  -n 128
```

### :sloth: Fine-tuning LFM2.5-VL with Unsloth

Unsloth supports fine-tuning LFM2.5 models. The 1.6B model fits comfortably on a free Colab T4 GPU. Training is 2x faster with 50% less VRAM.

**Free Colab Notebook:**

* [LFM2.5-VL-1.6B SFT LoRA notebook](https://colab.research.google.com/drive/1FaR2HSe91YDe88TG97-JVxMygl-rL6vB?usp=sharing)

#### Unsloth Config for LFM2.5

```python
from unsloth import FastVisionModel
import torch

model, tokenizer = FastVisionModel.from_pretrained(
    model_name = "LiquidAI/LFM2.5-VL-1.6B",
    max_seq_length = 4096, 
    load_in_4bit = False, 
)

model = FastVisionModel.get_peft_model(
    model,
    finetune_vision_layers     = False, # Set to False for now
    finetune_language_layers   = True, # False if not finetuning language layers
    finetune_attention_modules = True, # False if not finetuning attention layers
    finetune_mlp_modules       = True, # False if not finetuning MLP layers
    r = 16,         
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
)
```

#### Training Setup

```python
from unsloth.trainer import UnslothVisionDataCollator
from trl import SFTTrainer, SFTConfig

FastVisionModel.for_training(model) # Enable for training!

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    data_collator = UnslothVisionDataCollator(model, tokenizer), # Must use!
    train_dataset = converted_dataset,
    args = SFTConfig(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 30,# num_train_epochs = 1, # Set this instead of max_steps for full train
        learning_rate = 2e-4,
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.001,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none",     # For Weights and Biases
        remove_unused_columns = False,
        dataset_text_field = "",
        dataset_kwargs = {"skip_prepare_dataset": True},
        max_length = 2048,
    ),
)

trainer.train()
```

#### Save and Export

```python
# Save LoRA adapters
model.save_pretrained("lfm25_lora")
tokenizer.save_pretrained("lfm25_lora")

# Merge and save to 16bit
model.save_pretrained_merged("lfm25_merged", tokenizer, save_method="merged_16bit")

# Export to GGUF
model.save_pretrained_gguf("lfm25_gguf", tokenizer, quantization_method="q4_k_m")
```

### :bar\_chart: Benchmarks

LFM2.5-VL-1.6B delivers best-in-class performance:

| Model              | MMStar | MM-IFEval | BLINK | InfoVQA (Val) | OCRBench (v2) | RealWorldQA | MMMU (Val) | MMMB (avg) | Multilingual MMBench (avg) |
| ------------------ | ------ | --------- | ----- | ------------- | ------------- | ----------- | ---------- | ---------- | -------------------------- |
| **LFM2.5-VL-1.6B** | 50.67  | 52.29     | 48.82 | 62.71         | 41.44         | 64.84       | 40.56      | 76.96      | 65.90                      |
| LFM2-VL-1.6B       | 49.87  | 46.35     | 44.50 | 58.35         | 35.11         | 65.75       | 39.67      | 72.13      | 60.57                      |
| InternVL3.5-1B     | 50.27  | 36.17     | 44.19 | 60.99         | 33.53         | 57.12       | 41.89      | 68.93      | 58.32                      |
| FastVLM-1.5B       | 53.13  | 24.99     | 43.29 | 23.92         | 26.61         | 61.56       | 38.78      | 64.84      | 50.89                      |

### 📚 Resources

* [Liquid AI Blog Post](https://www.liquid.ai/blog/introducing-lfm2-5-the-next-generation-of-on-device-ai)
* [LFM2 Technical Report (arXiv)](https://arxiv.org/abs/2511.23404)
* [Liquid AI Documentation](https://docs.liquid.ai/lfm)
* [Liquid Playground](https://playground.liquid.ai/)


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/lfm2.5.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
