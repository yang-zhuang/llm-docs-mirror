> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide.md).

# Fine-tuning LLMs Guide

Learn all the basics and best practices of fine-tuning. Beginner-friendly.

## 1. What Is Fine-tuning?

Fine-tuning / training / post-training models customizes its behavior, enhances + injects knowledge, and optimizes performance for domains and specific tasks. For example:

* OpenAI’s **GPT-5** was post-trained to improve instruction following and helpful chat behavior.
* The standard method of post training is called Supervised Fine-Tuning (SFT). Other methods include preference optimization (DPO, ORPO), distillation and [Reinforcement Learning (RL)](/docs/get-started/reinforcement-learning-rl-guide.md) (GRPO, GSPO), where an "agent" learns to make decisions by interacting with an environment and receiving **feedback** in the form of **rewards** or **penalties**.

With [Unsloth](https://github.com/unslothai/unsloth), you can fine-tune or do RL for free on Colab, Kaggle, or locally with just 3GB VRAM by using our [notebooks](https://docs.unsloth.ai/get-started/unsloth-notebooks). By fine-tuning a pre-trained model on a dataset, you can:

* **Update + Learn New Knowledge**: Inject and learn new domain-specific information.
* **Customize Behavior**: Adjust the model’s tone, personality, or response style.
* **Optimize for Tasks**: Improve accuracy and relevance for specific use cases.

**Example fine-tuning or RL use-cases**:

* Enables LLMs to predict if a headline impacts a company positively or negatively.
* Can use historical customer interactions for more accurate and custom responses.
* Fine-tune LLM on legal texts for contract analysis, case law research, and compliance.

You can think of a fine-tuned model as a specialized agent designed to do specific tasks more effectively and efficiently. **Fine-tuning can replicate all of RAG's capabilities**, but not vice versa.

{% columns %}
{% column %}

#### :question:What is LoRA/QLoRA?

In LLMs, we have model weights. Llama 70B has 70 billion numbers. Instead of changing all 70B numbers, we instead add thin matrices A and B to each weight, and optimize those. This means we only optimize 1% of weights. LoRA is when the original model is 16-bit unquantized while QLoRA quantizes to 4-bit to save 75% memory.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-715b6260aae497f160d7f9a1019bcfa472675dcf%2Fimage%20(7)%20(1)%20(1).png?alt=media" alt=""><figcaption><p>Instead of optimizing Model Weights (yellow), we optimize 2 thin matrices A and B.</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

#### Fine-tuning misconceptions:

You may have heard that fine-tuning does not make a model learn new knowledge or RAG performs better than fine-tuning. That is **false**. You can train a specialized coding model with fine-tuning and RL while RAG can’t change the model’s weights and only augments what the model sees at inference time. Read more FAQ + misconceptions [here](https://unsloth.ai/docs/get-started/pages/HP82bIzgldwxWk3OSzVy#fine-tuning-vs.-rag-whats-the-difference):

{% content-ref url="/pages/HP82bIzgldwxWk3OSzVy" %}
[FAQ + Is Fine-tuning Right For Me?](/docs/get-started/fine-tuning-for-beginners/faq-+-is-fine-tuning-right-for-me.md)
{% endcontent-ref %}

> [**Introducing Unsloth Studio:** ](/docs/new/studio.md) Our new open-source web UI for training and running models. This means you can now fine-tune models with no-code and have observability and automatic dataset creation features.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FxV1PO5DbF3ksB51nE2Tw%2Fmore%20cropped%20ui%20for%20homepage.png?alt=media&amp;token=f75942c9-3d8d-4b59-8ba2-1a4a38de1b86" alt="" width="563"><figcaption></figcaption></figure></div>

## 2. Choose the Right Model + Method

If you're a beginner, it is best to start with a small instruct model like Llama 3.1 (8B) and experiment from there. You'll also need to decide between normal fine-tuning, RL, QLoRA or LoRA training:

* **Reinforcement Learning (RL)** is used when you need a model to excel at a specific behavior (e.g., tool-calling) using an environment and reward function rather than labeled data. We have several [notebook examples](/docs/get-started/unsloth-notebooks.md#grpo-reasoning-rl-notebooks), but for most use-cases, standard SFT is sufficient.
* **LoRA** is a parameter efficient training method that typically keeps the base model’s weights frozen and trains a small set of added low-rank adapter weights (in 16-bit precision).
* **QLoRA** combines LoRA with 4-bit precision to handle very large models with minimal resources.
* Unsloth also supports full fine-tuning (FFT) and pretraining, which require significantly more resources, but FFT is usually unnecessary. When done correctly, LoRA can match FFT.
* Unsloth **all types models**: [text-to-speech](/docs/basics/text-to-speech-tts-fine-tuning.md), [embedding](/docs/basics/embedding-finetuning.md), GRPO, RL, [vision](/docs/basics/vision-fine-tuning.md), multimodal and more.

{% hint style="info" %}
Research shows that **training and serving in the same precision** helps preserve accuracy. This means if you want to serve in 4-bit, train in 4-bit and vice versa.
{% endhint %}

We recommend starting with QLoRA, as it is one of the most accessible and effective methods for training models. Our [dynamic 4-bit](https://unsloth.ai/blog/dynamic-4bit) quants, the accuracy loss for QLoRA compared to LoRA is now largely recovered.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-cfc51c261e6d24df3aa967d9b9a482313465cbc1%2Fmodel%20name%20change.png?alt=media" alt="" width="563"><figcaption></figcaption></figure>

You can change the model name to whichever model you like by matching it with model's name on Hugging Face e.g. '`unsloth/llama-3.1-8b-unsloth-bnb-4bit`'.

We recommend starting with **Instruct models**, as they allow direct fine-tuning using conversational chat templates (ChatML, ShareGPT etc.) and require less data compared to **Base models** (which uses Alpaca, Vicuna etc). Learn more about the differences between [instruct and base models here](/docs/get-started/fine-tuning-llms-guide/what-model-should-i-use.md#instruct-or-base-model).

* Model names ending in **`unsloth-bnb-4bit`** indicate they are [**Unsloth dynamic 4-bit**](https://unsloth.ai/blog/dynamic-4bit) **quants**. These models consume slightly more VRAM than standard BitsAndBytes 4-bit models but offer significantly higher accuracy.
* If a model name ends with just **`bnb-4bit`**, without "unsloth", it refers to a standard BitsAndBytes 4-bit quantization.
* Models with **no suffix** are in their original **16-bit or 8-bit formats**. While they are the original models from the official model creators, we sometimes include important fixes - such as chat template or tokenizer fixes. So it's recommended to use our versions when available.

There are other settings which you can toggle:

* **`max_seq_length = 2048`** – Controls context length. While Llama-3 supports 8192, we recommend 2048 for testing. Unsloth enables 4× longer context fine-tuning.
* **`dtype = None`** – Defaults to None; use `torch.float16` or `torch.bfloat16` for newer GPUs.
* **`load_in_4bit = True`** – Enables 4-bit quantization, reducing memory use 4× for fine-tuning. Disabling it enables LoRA 16-bit fine-tuning. You can also enable 16-bit LoRA with `load_in_16bit = True`
* To enable full fine-tuning (FFT), set `full_finetuning = True`. For 8-bit fine-tuning, set `load_in_8bit = True`.
* **Note:** Only one training method can be set to `True` at a time.

{% hint style="info" %}
A common mistake is jumping straight into full fine-tuning (FFT), which is compute-heavy. Start by testing with LoRA or QLoRA first, if it won’t work there, it almost certainly won’t work with FFT. And if LoRA fails, don’t assume FFT will magically fix it.
{% endhint %}

You can also do [Text-to-speech (TTS)](/docs/basics/text-to-speech-tts-fine-tuning.md), [reasoning (GRPO)](/docs/get-started/reinforcement-learning-rl-guide.md), [vision](/docs/basics/vision-fine-tuning.md), [RL](/docs/get-started/reinforcement-learning-rl-guide/preference-dpo-orpo-and-kto.md) (GRPO, DPO), [continued pretraining](/docs/basics/continued-pretraining.md), text completion and other training methodologies with Unsloth.

{% columns %}
{% column %}
Read our guide on choosing models:

{% content-ref url="/pages/BSShKhLoFNlGWO5cN8VJ" %}
[What Model Should I Use?](/docs/get-started/fine-tuning-llms-guide/what-model-should-i-use.md)
{% endcontent-ref %}
{% endcolumn %}

{% column %}
For inidivudal tutorials on models:

{% content-ref url="/pages/BAeSP6aOxvSeDUzCgKOK" %}
[Complete LLM Directory](/docs/models/tutorials.md)
{% endcontent-ref %}
{% endcolumn %}
{% endcolumns %}

## 3. Your Dataset

For LLMs, datasets are collections of data that can be used to train our models. In order to be useful for training, text data needs to be in a format that can be tokenized.

* You will need to create a dataset usually with 2 columns - question and answer. The quality and amount will largely reflect the end result of your fine-tune so it's imperative to get this part right.
* You can [synthetically generate data](/docs/get-started/fine-tuning-llms-guide/datasets-guide.md#synthetic-data-generation) and structure your dataset (into QA pairs) using ChatGPT or local LLMs.
* You can also use our new Synthetic Dataset notebook which automatically parses documents (PDFs, videos etc.), generates QA pairs and auto cleans data using local models like Llama 3.2. [Access the notebook here.](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Meta_Synthetic_Data_Llama3_2_\(3B\).ipynb)
* Fine-tuning can learn from an existing repository of documents and continuously expand its knowledge base, but just dumping data alone won’t work as well. For optimal results, curate a well-structured dataset, ideally as question-answer pairs. This enhances learning, understanding, and response accuracy.
* But, that's not always the case, e.g. if you are fine-tuning a LLM for code, just dumping all your code data can actually enable your model to yield significant performance improvements, even without structured formatting. So it really depends on your use case.

***Read more about creating your dataset:***

{% content-ref url="/pages/XgcpRfamZHmHnRHBnVE4" %}
[Datasets Guide](/docs/get-started/fine-tuning-llms-guide/datasets-guide.md)
{% endcontent-ref %}

For most of our notebook examples, we utilize the [Alpaca dataset](https://docs.unsloth.ai/basics/tutorial-how-to-finetune-llama-3-and-use-in-ollama#id-6.-alpaca-dataset) however other notebooks like Vision will use different datasets which may need images in the answer ouput as well.

### 4. Understand Training Hyperparameters

Learn how to choose the right [hyperparameters](/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide.md) using best practices from research and real-world experiments - and understand how each one affects your model's performance.

**For a complete guide on how hyperparameters affect training, see:**

{% content-ref url="/pages/y6obKRSk8TwyjIrCjuGE" %}
[Hyperparameters Guide](/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide.md)
{% endcontent-ref %}

## 5. Install + Requirements

You can use Unsloth via two main ways, our free notebooks or locally.

### Unsloth Notebooks

We would recommend beginners to utilise our pre-made [notebooks](/docs/get-started/unsloth-notebooks.md) first as it's the easiest way to get started with guided steps. You can later export the notebooks to use locally.

Unsloth has step-by-step notebooks for [text-to-speech](/docs/basics/text-to-speech-tts-fine-tuning.md), [embedding](/docs/basics/embedding-finetuning.md), GRPO, RL, [vision](/docs/basics/vision-fine-tuning.md), multimodal, different use-cases and more.

### Local Installation

You can also install Unsloth locally via [Docker](/docs/get-started/install/docker.md) or `pip install unsloth` (with Linux, WSL or [Windows](/docs/get-started/install/windows-installation.md)). Also depending on the model you're using, you'll need enough VRAM and resources.

Installing Unsloth will require a Windows or Linux device. Once you install Unsloth, you can copy and paste our notebooks and use them in your own local environment. See:

{% columns %}
{% column %}
{% content-ref url="/pages/odJXZM9jv284RKqZ2Pna" %}
[Unsloth Requirements](/docs/get-started/fine-tuning-for-beginners/unsloth-requirements.md)
{% endcontent-ref %}
{% endcolumn %}

{% column %}
{% content-ref url="/pages/WbSfE0ITQYsNqERZwnbZ" %}
[Installation](/docs/get-started/install.md)
{% endcontent-ref %}
{% endcolumn %}
{% endcolumns %}

## 6. Training + Evaluation

Once you have everything set, it's time to train! If something's not working, remember you can always change hyperparameters, your dataset etc.

You’ll see a log of numbers during training. This is the training loss, which shows how well the model is learning from your dataset. For many cases, a loss around 0.5 to 1.0 is a good sign, but it depends on your dataset and task. If the loss is not going down, you might need to adjust your settings. If the loss goes to 0, that could mean overfitting, so it's important to check validation too.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-feb9b0f5763d41cecaec9a3a9cd227ad918f0ca7%2Fimage.png?alt=media" alt="" width="375"><figcaption><p>The training loss will appear as numbers</p></figcaption></figure>

We generally recommend keeping the default settings unless you need longer training or larger batch sizes.

* **`per_device_train_batch_size = 2`** – Increase for better GPU utilization but beware of slower training due to padding. Instead, increase `gradient_accumulation_steps` for smoother training.
* **`gradient_accumulation_steps = 4`** – Simulates a larger batch size without increasing memory usage.
* **`max_steps = 60`** – Speeds up training. For full runs, replace with `num_train_epochs = 1` (1–3 epochs recommended to avoid overfitting).
* **`learning_rate = 2e-4`** – Lower for slower but more precise fine-tuning. Try values like `1e-4`, `5e-5`, or `2e-5`.

#### Evaluation

In order to evaluate, you could do manually evaluation by just chatting with the model and see if it's to your liking. You can also enable evaluation for Unsloth, but keep in mind it can be time-consuming depending on the dataset size. To speed up evaluation you can: reduce the evaluation dataset size or set `evaluation_steps = 100`.

For testing, you can also take 20% of your training data and use that for testing. If you already used all of the training data, then you have to manually evaluate it. You can also use automatic eval tools but keep in mind that automated tools may not perfectly align with your evaluation criteria.

## 7. Running + Deploying the model

Now let's run the model after we completed the training process! You can edit the yellow underlined part! In fact, because we created a multi turn chatbot, we can now also call the model as if it saw some conversations in the past like below:

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-f2d5f23fa62ec89e06bf20fea433f9a1e42a2fe3%2Fimage.png?alt=media" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-cdf5d779635901dce7793df92531dbf3caf0fb0a%2Fimage%20(47).png?alt=media" alt=""><figcaption></figcaption></figure></div>

Reminder Unsloth itself provides **2x faster inference** natively as well, so always do not forget to call `FastLanguageModel.for_inference(model)`. If you want the model to output longer responses, set `max_new_tokens = 128` to some larger number like 256 or 1024. Notice you will have to wait longer for the result as well!

### Saving + Deployment

For saving and deploying your model in desired inference engines like Ollama, vLLM, Open WebUI, you will need to use the LoRA adapter on top of the base model. We have designated guides for each framework:

{% content-ref url="/pages/gEugERiAw2ztDNt98JVR" %}
[Inference & Deployment](/docs/basics/inference-and-deployment.md)
{% endcontent-ref %}

{% columns %}
{% column %}
If you’re running inference on a single device (like a laptop or Mac), use llama.cpp to convert to GGUF format to use in Ollama, llama.cpp, LM Studio etc:

{% content-ref url="/pages/T7ZPf3SNAwDykZNgXptE" %}
[GGUF & llama.cpp](/docs/basics/inference-and-deployment/saving-to-gguf.md)
{% endcontent-ref %}
{% endcolumn %}

{% column %}
If you’re deploying an LLM for enterprise or multi-user inference for FP8, AWQ, use vLLM:

{% content-ref url="/pages/fhJtaLFFXVsGnbMUiACo" %}
[vLLM](/docs/basics/inference-and-deployment/vllm-guide.md)
{% endcontent-ref %}
{% endcolumn %}
{% endcolumns %}

We can now save the fine-tuned model as a small 100MB file called a LoRA adapter like below. You can instead push to the Hugging Face hub as well if you want to upload your model! Remember to get a Hugging Face [token](https://huggingface.co/settings/tokens) and add your token!

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-8c577103f7c4fe883cabaf35c8437307c6501686%2Fimage.png?alt=media" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-1a1be852ca551240bdce47cf99e6ccd7d31c1326%2Fimage.png?alt=media" alt=""><figcaption></figcaption></figure></div>

After saving the model, we can again use Unsloth to run the model itself! Use `FastLanguageModel` again to call it for inference!

## 8. We're done!

You've successfully fine-tuned a language model and exported it to your desired inference engine with Unsloth!

To learn more about fine-tuning tips and tricks, head over to our blogs which provide tremendous and educational value: <https://unsloth.ai/blog/>

If you need any help on fine-tuning, you can also join our Discord server [here](https://discord.gg/unsloth) or [Reddit r/unsloth](https://www.reddit.com/r/unsloth/). Thanks for reading and hopefully this was helpful!

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-69482ba90d417f7bf98dddaf83795cdd3eb20efc%2Fsloth%20sparkling%20square.png?alt=media" alt="" width="188"><figcaption></figcaption></figure>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/fine-tuning-llms-guide.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
