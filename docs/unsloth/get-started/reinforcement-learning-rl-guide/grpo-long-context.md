> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/grpo-long-context.md).

# Reinforcement Learning GRPO with 7x Longer Context

Learn how Unsloth enables ultra long context RL fine-tuning.

Reinforcement learning's (RL) biggest challenge is supporting long reasoning traces. We're introducing new batching algorithms to enable \~**7x longer context** (can be more than 12x) RL training with no accuracy or speed degradation vs. other optimized setups that use FA3, kernels & chunked losses.

* Unsloth now trains gpt-oss QLoRA with **380K context** on a single 192GB NVIDIA B200 GPU
* [Qwen3](/docs/models/tutorials/qwen3-how-to-run-and-fine-tune.md#fine-tuning-qwen3-with-unsloth)-8B GRPO reaches **110K context** on an 80GB VRAM H100 via [vLLM](#vllm-for-rl) and QLoRA, and **65K** for [gpt-oss](/docs/models/gpt-oss-how-to-run-and-fine-tune/gpt-oss-reinforcement-learning.md) with BF16 LoRA.
* On 24GB VRAM, gpt-oss reaches 20K context and 32K for [Qwen3-VL](/docs/models/tutorials/qwen3-how-to-run-and-fine-tune/qwen3-vl-how-to-run-and-fine-tune.md)-8B QLoRA
* Unsloth GRPO RL runs with Llama, Gemma & all models auto support longer contexts

Our new data-movement and batching kernels and algorithms unlocks more context by:

* Dynamic [flattened sequence chunking](#flattened-sequence-length-chunking) to avoid materializing massive logit tensors and
* [Offloading log softmax](#offloading-activations-for-log-softmax) activations which prevents silent memory growth over time.

{% hint style="info" %}
**You can combine all features in Unsloth together:**

1. Unsloth's [weight-sharing](/docs/get-started/reinforcement-learning-rl-guide/memory-efficient-rl.md) feature with [vLLM](https://github.com/vllm-project/vllm) and our Standby Feature in [Memory Efficient RL](/docs/get-started/reinforcement-learning-rl-guide/memory-efficient-rl.md)
2. Unsloth's [Flex Attention](/docs/models/gpt-oss-how-to-run-and-fine-tune/long-context-gpt-oss-training.md) for long context gpt-oss and our [500K Context Training](/docs/blog/500k-context-length-fine-tuning.md)
3. Float8 training in [FP8 RL](/docs/get-started/reinforcement-learning-rl-guide/fp8-reinforcement-learning.md) and Unsloth's [async gradient checkpointing](https://unsloth.ai/blog/long-context) and much more
   {% endhint %}

### :tada:Getting started

To get started, you can use any existing [GRPO notebooks](/docs/get-started/unsloth-notebooks.md#grpo-reasoning-rl-notebooks) (or update Unsloth if local):

{% columns %}
{% column width="33.33333333333333%" %}
[**gpt-oss-20b**](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-\(20B\)-GRPO.ipynb) GSPO

{% embed url="<https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-(20B)-GRPO.ipynb>" %}
{% endcolumn %}

{% column width="33.33333333333333%" %}
[**Qwen3-VL-8B**](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_VL_\(8B\)-Vision-GRPO.ipynb) Vision RL

{% embed url="<https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_VL_(8B)-Vision-GRPO.ipynb>" %}
{% endcolumn %}

{% column width="33.33333333333333%" %}
[Qwen3-8B - **FP8**](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_8B_FP8_GRPO.ipynb) L4 GPU

{% embed url="<https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_8B_FP8_GRPO.ipynb>" %}
{% endcolumn %}
{% endcolumns %}

Adopting Unsloth for your RL tasks provides a robust framework for managing large-scale models efficiently. To effectively utilize Unsloth's enhancements:

* **Hardware Recommendations**: Use of NVIDIA H100 or equivalent for optimal VRAM utilization.
* **Configuration Tips**: Ensure `batch_size` and `gradient_accumulation_steps` settings align with your computational resources for best performance.

{% hint style="success" %}
Update Unsloth to the latest Pypi release to get the latest updates:

```
pip install --upgrade --no-cache-dir unsloth unsloth_zoo
```

{% endhint %}

Our benchmarks highlight the memory savings achieved in comparison to earlier versions for GPT OSS and Qwen3-8B. Both plots below (without [standby](/docs/get-started/reinforcement-learning-rl-guide/memory-efficient-rl.md)) were run with `batch_size = 4` and `gradient_accumulation_steps=2` , since standby by design uses all VRAM.

For our benchmarks, we compare BF16 GRPO to Hugging Face with all optimizations enabled (all kernels in kernels library, Flash Attention 3, chunked loss kernels, etc):

### :1234:Flattened sequence length chunking

Previously, Unsloth reduced memory usage of RL by avoiding the full materialization of the logits tensor through chunking over the batch dimension. A rough estimate of the VRAM required to materialize logits during the forward pass is shown in Equation (1).

$$
\text{Equation 1: } \text{Logit Memory (GB)} = \frac{\text{batch size} \times\text{context length} \times \text{vocab dim}}{1024^3}
$$

Using this formulation, a configuration with `batch_size = 4`, `context_length = 8192`, and `vocab_dim = 128,000` would require approximately **3.3 GB of VRAM** to store the logits tensor.

Via [Long Context gpt-oss](/docs/models/gpt-oss-how-to-run-and-fine-tune/long-context-gpt-oss-training.md) last year, we then introduced a fused loss approach for GRPO. This approach ensures that only a single batch sample is processed at a time, significantly reducing peak memory usage. Under the same configuration, VRAM usage drops to approximately **0.83 GB**, as reflected in Equation (2).

$$
\text{Equation 2: }\text{Logit Memory (GB)} = \frac{\text{context length} \times \text{vocab dim}}{1024^3}
$$

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fy1TkzxySrNAeeSWJSVLU%2Funsloth_vs_trl_gpt_oss.png?alt=media&amp;token=0303423d-1454-4410-8be8-7d6110ac1df0" alt="" width="375"><figcaption><p>Figure 1: gpt-oss BF16 GRPO LoRA (Unsloth vs. HF with all optimizations on)</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FmfKhenN0TGRDlMcuxob6%2Fqwen38b%20long%20context%20grpo.png?alt=media&amp;token=22883f90-5bf0-4478-91a9-6a191c920f12" alt="" width="375"><figcaption><p>Figure 2: Qwen3-8B QLoRA GRPO LoRA (Unsloth vs. HF with all optimizations on)</p></figcaption></figure></div>

In this update, we extend the same idea further by introducing chunking across the **sequence dimension** as well. Instead of materializing logits for the entire `(batch_size × context_length)` space at once, we flatten these dimensions and process them in smaller chunks using a configurable multiplier. This allows Unsloth to support substantially longer contexts without increasing peak memory usage.

In Figure 5 below, we use a multiplier of `max(4, context_length // 4096)`, though any multiplier can be specified depending on the desired memory–performance tradeoff. With this setting, the same example configuration (`batch_size = 4`, `context_length = 8192`, `vocab_dim = 128,000`) now requires only **0.207 GB of VRAM** for logits materialization.

$$
\text{Equation 3: }\text{Logit Memory (GB)} = \frac{\frac{\text{context length}}{\text{multiplier}} \times \text{vocab dim}}{1024^3}
$$

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FWFTbejdIn3T6E6yHgF1Z%2FCode_Generated_Image%20(2).png?alt=media&amp;token=790a1ee4-2814-4b29-afcb-bb9ffd1eb729" alt="" width="375"><figcaption><p>Figure 3: gpt-oss-20b (H100) Unsloth new vs. old</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fi4QipufoavtPKyeRU0Vv%2FCode_Generated_Image%20(3).png?alt=media&amp;token=226c5a3c-a0a4-458d-a0df-8c84523b04b5" alt="" width="375"><figcaption><p>Figure 4: Qwen3-8B (H100) Unsloth new vs. old</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FkSIh5DIWvKGemnNHowPs%2FCode_Generated_Image_4.png?alt=media&amp;token=0a3dfe85-ae8c-4280-bc0a-6c1f1523c90e" alt="" width="375"><figcaption><p>Figure 5: gpt-oss-20b (H100)</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FRP1RPiOeIYOt82L1Ifkc%2FCode_Generated_Image_5.png?alt=media&amp;token=4ce06b0f-2464-41fd-8795-e5bf0dbf4327" alt="" width="375"><figcaption><p>Figure 6: Qwen3-8B (B200)</p></figcaption></figure></div>

This update is reflected in the compiled `chunked_hidden_states_selective_log_softmax` below, which now supports chunking across both the batch and sequence dimensions. To preserve the logits tensor (`[batch_size, context_length, vocab_dim]`), it is always chunked across the batch dimension. Additional sequence chunking is controlled via `unsloth_logit_chunk_multiplier` in the GRPO configuration; if unset, it defaults to `max(4, context_length // 4096)`. In the example below, `input_ids_chunk[0]` corresponds to the size of the hidden states mini batches in optimization 2.

```python
logprobs_chunk = chunked_hidden_states_selective_log_softmax(
    new_hidden_states_chunk, 
    lm_head, 
    completion_ids, 
    chunks=input_ids_chunk.shape[0]*multiplier, 
    logit_scale_multiply=logit_scale_multiply,
    logit_scale_divide=logit_scale_divide,
    logit_softcapping=logit_softcapping,
    temperature=temperature,                
)
```

1. We utilize torch.compile with custom compile options to reduce VRAM and increase speed.
2. All chunked logits are upcasted in float32 to preserve accuracy.
3. We support logit softcapping, temperature scaling and all other features.

### :ghost:Hidden States Chunking

We also observed that at longer context lengths, hidden states can become a significant contributor to memory usage. For demonstration, we will assume `hidden_states_dim=4096`. The corresponding memory usage follows a similar formulation to the logits case, shown below.&#x20;

$$
\text{Hidden States Memory (GB)} = \frac{\text{batch size} \times\text{context length} \times \text{hidden states dim}}{1024^3}
$$

With a `batch_size = 8` and `context_length = 64000`, this would result in a VRAM usage of approximately **2 GB**. In this release, we introduce optional chunking over the batch dimension for the hidden states tensor during log-probability computation. This would cause the VRAM usage to be divided by the batch size or in this case be **0.244 GB**.This reduces the peak VRAM required to materialize hidden states, as reflected in the updated equation below:

$$
\text{Hidden States Memory (GB)} = \frac{\text{context length} \times \text{hidden states dim}}{1024^3}
$$

Similar to our cross entropy loss in our [500K Context Training](/docs/blog/500k-context-length-fine-tuning.md) release, the new implementation **automatically tunes hidden state batching**. Users can also control this behavior via `unsloth_grpo_mini_batch`. However, increasing `unsloth_grpo_mini_batch` beyond the optimal value can introduce slight performance increase or slowdown (usually faster) compared to the previous loss function.

However, during a GPT-OSS run (`context_length = 8192, batch_size = 4, gradient_accumulation_steps = 2`), setting `unsloth_grpo_mini_batch = 1` and `unsloth_logit_chunk_multiplier = 4` results in **little to no speed degradation while reducing VRAM usage by approximately 5 GB** compared to older versions of Unsloth.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FYZsgoKpZKyJKrNmbvehR%2FCode_Generated_Image%20(4).png?alt=media&amp;token=5d3c0605-9ed8-4d4a-a722-a85132510222" alt="" width="375"><figcaption></figcaption></figure>

{% hint style="success" %}
**Note:** In Figures 3 and 4, we use the maximum effective batch size, which is 8 in this setup. The effective batch size is computed as `batch_size × gradient_accumulation_steps`, giving `4 × 2 = 8`. For a deeper explanation of how effective batch sizes work in RL, see our [advanced RL documentation](/docs/get-started/reinforcement-learning-rl-guide/advanced-rl-documentation.md).&#x20;
{% endhint %}

### :cactus:Offloading activations for log softmax

During the development of this release, we discovered that when tiling across the batch dimension for hidden states, the activations were not being offloaded after the fused logits and logprobs computation. Because logits are computed one batch at a time using `hidden_states[i] @ lm_head`, the existing activation offloading and gradient checkpointing logic, designed to operate within the model’s forward pass did not apply in this case.

To address this, we added explicit logic to offload these activations outside the model’s forward pass, as shown in the Python pseudocode below:

```python
class Unsloth_Offloaded_Log_Softmax(torch.autograd.Function):
    def forward(...):
        with torch.no_grad():
            output = chunked_hidden_states_selective_log_softmax(hidden_states, lm_head, ...)
        return output
    def backward(ctx, grad_output):
        hidden_states = ctx.saved_hidden_states
        hidden_states.requires_grad_(True)
        with torch.enable_grad():
            output = chunked_hidden_states_selective_log_softmax(hidden_states, lm_head, ...)
        torch.autograd.backward(output, grad_output)
        return ...
```

{% hint style="success" %}
**Note:** This feature is only effective when chunking across the batch dimension or when `unsloth_grpo_mini_batch > 1`. If all hidden states are materialized at once during the forward pass (i.e., `unsloth_grpo_mini_batch = 1`), the backward pass requires the same amount of memory in the GPU regardless of whether activations are offloaded. Since activation offloading introduces a slight performance slowdown without reducing memory usage in this case, it provides no benefit.
{% endhint %}

### :sparkles:Configuring parameters:

If you do not configure `unsloth_grpo_mini_batch` and `unsloth_logit_chunk_multiplier`, we will **automatically tune these two parameters** for you based on your available VRAM and depending on the size of your context length. Below however is how you can change these variables in your GRPO run:

```python
training_args = GRPOConfig(
    ...
    unsloth_grpo_mini_batch = 3
    unsloth_logit_chunk_multiplier = 2
    ...
)
```

A visualization of the optimizations and `unsloth_grpo_mini_batch` and `unsloth_logit_chunk_multiplier` can be seen in the diagram below.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F2OmZA297HzG3CdRzi3X5%2FLogit%20Chunking%20(1).png?alt=media&amp;token=b953a62b-fefa-43f2-a9ce-108675b8735f" alt="" width="375"><figcaption></figcaption></figure>

The 3 matrices represent the overall larger batch or `unsloth_grpo_mini_batch` (represented by the number of black brackets) and the rows of each of the matrices represents the context length that the `unsloth_logit_chunk_multiplier`  chunks the sequence length by (represented by the number of red brackets).&#x20;

### :vhs:vLLM for RL

**For RL workflows, the inference/generation phase is the main bottleneck**. To address this, we utilize [vLLM](https://github.com/vllm-project/vllm), which has accelerated generation by up to 11x compared to normal generation. Since GRPO was popularized last year, vLLM has been a core component of most RL frameworks including Unsloth. We want to extend our gratitude to the vLLM team and all its contributors for their work as they play a pivotal role in making Unsloth’s RL better!

To try longer context RL, you can use any existing [GRPO notebooks](/docs/get-started/unsloth-notebooks.md#grpo-reasoning-rl-notebooks) (or update Unsloth if local):

{% columns %}
{% column width="33.33333333333333%" %}
[**gpt-oss-20b**](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-\(20B\)-GRPO.ipynb) - GSPO

{% embed url="<https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-(20B)-GRPO.ipynb>" %}
{% endcolumn %}

{% column width="33.33333333333333%" %}
[**Qwen3-VL-8B**](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_VL_\(8B\)-Vision-GRPO.ipynb) Vision RL

{% embed url="<https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_VL_(8B)-Vision-GRPO.ipynb>" %}
{% endcolumn %}

{% column width="33.33333333333333%" %}
[Qwen3-8B - **FP8**](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_8B_FP8_GRPO.ipynb) L4 GPU

{% embed url="<https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Qwen3_8B_FP8_GRPO.ipynb>" %}
{% endcolumn %}
{% endcolumns %}

Acknowledgements: A huge thank you to the Hugging Face team and libraries for powering Unsloth and making this possible.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/grpo-long-context.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
