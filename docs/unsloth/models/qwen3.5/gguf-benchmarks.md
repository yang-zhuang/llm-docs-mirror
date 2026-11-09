> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/qwen3.5/gguf-benchmarks.md).

# Qwen3.5 GGUF Benchmarks

See how Unsloth Dynamic GGUFs perform + analysis of perplexity, KL divergence & MXFP4.

We updated all [Qwen3.5](/docs/models/qwen3.5.md) Unsloth Dynamic quants **being SOTA** on nearly all bits. We did over 150 KL Divergence benchmarks, totally **9TB of GGUFs**. We uploaded all research artifacts.

We also fixed a **tool calling** chat template issue **(affects all quant uploaders and types regardless where you're using it or where it's from)**.

{% hint style="success" %}
[**Mar 5 Update**](#id-4-march-5th-2026-update-more-robustness)**:** Redownload Qwen3.5-**35B**, **27B,** **122B** and **397B.**

* All GGUFs now updated with an **improved quantization** algorithm.
* All use our **new imatrix data**. See some improvements in chat, coding, long context, and tool-calling use-cases.

**New benchmarks** for Qwen3.5-122B-A10B and 35-A3B out now!
{% endhint %}

{% hint style="info" %}
Want to see how to run the model + hardware requirements? Read our [inference guide](/docs/models/qwen3.5.md).
{% endhint %}

**99.9% KL Divergence shows SOTA** on Pareto Frontier for [Unsloth Dynamic](/docs/basics/dynamic-3.0-ggufs.md) `Q4_K_XL`, `IQ3_XXS` etc.:

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F1XLNe1MoxtF1ODs5gDej%2F122b%20final.png?alt=media&amp;token=9eee5d8d-f16c-4c3f-8e36-18856e5609aa" alt="" width="563"><figcaption><p>Qwen3.5-<strong>122B-A10B</strong> Benchmarks</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FAeecRAsAA3lxJ36HI8pO%2Fhoriztonal%20plot.png?alt=media&amp;token=173d4050-9442-4d2b-9f1b-ee8bd0d423df" alt="" width="563"><figcaption><p>Qwen3.5-<strong>35B-A3B</strong> Benchmarks</p></figcaption></figure></div>

* Imatrix definitely helps reduce KLD & PPL, at the cost of 5-10% slower inference.
* We tested our GGUFs against many other providers
* Quantizing ssm\_out (Mamba layers) is not a good idea, and ffn\_down\_exps.
* **Retiring MXFP4** from all GGUF quants: Q2\_K\_XL, Q3\_K\_XL and Q4\_K\_XL, except for pure MXFP4\_MOE.

| [Qwen3.5-35B-A3B](https://huggingface.co/unsloth/Qwen3.5-35B-A3B-GGUF) | [Qwen3.5-27B](https://huggingface.co/unsloth/Qwen3.5-27B-GGUF) | [Qwen3.5-122B-A10B](https://huggingface.co/unsloth/Qwen3.5-122B-A10B-GGUF) | [Qwen3.5-397B-A17B](https://huggingface.co/unsloth/Qwen3.5-397B-A17B-GGUF) |
| ---------------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FHq3gIokmPZJRYlnKVFmH%2FHCp7gV9XgAEP5og.png?alt=media&amp;token=a1268383-1648-45f8-996d-c89c7dde3706" alt="" width="563"><figcaption><p>New Qwen3.5-9B GGUF Benchmarks conducted by Benjamin Marie</p></figcaption></figure>

### 1) **Some tensors are very sensitive to quantization**

* We made over 9TB of research artifacts available for the community to investigate further on our [Experiments page](https://huggingface.co/unsloth/Qwen3.5-35B-A3B-Experiments-GGUF). It includes KLD metrics and all 121 configs we tested.
* We varied bit widths across each tensor type, and generated a best and worst Pareto Frontier plot below vs 99.9% KLD.
* For the best items to quantize, ffn\_up\_exps and ffn\_gate\_exps are generally ok to quantize to 3bit. ffn\_down\_exps is slightly more sensitive.
* For the worst items, ssm\_out dramatically increases KLD and the disk space savings is minuscule. For example, ssm\_out at q2\_k does dramatically worse. **Quantizing any attn\_\* is especially sensitive** for hybrid architectures, and so leaving them in higher precision works well.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F485gYwcqz2az5Pm9v3u3%2Fnew-qwen3-5-35b-a3b-unsloth-dynamic-ggufs-benchmarks-v0-pakdmbv1n2mg1.webp?alt=media&amp;token=2eeb55ca-51f3-402a-ae30-ea078c7554da" alt="" width="563"><figcaption></figcaption></figure>

{% columns %}
{% column %}
**Tensor type vs bits on 99.9% KL Divergence**

* We plot all quant levels vs 99.9% KLD, and sort from worst KLD to best. Quantizing ffn\_\* layers too heavily down is not a good idea.
* However, **some bit widths are good, especially 3bit**. - for example leaving ffn\_\* (down, up, gate) at around iq3\_xxs seems to be best compromise on disk space and 99.9% KLD change. 2 bits cause more degradation.
  {% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FcE0WAmPVddczWC3dQsWS%2Fnew-qwen3-5-35b-a3b-unsloth-dynamic-ggufs-benchmarks-v0-squz1jz4n2mg1.webp?alt=media&amp;token=3a31adf1-7c4c-446c-91a7-48e63d223189" alt="" width="188"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

**MXFP4 is much worse on many tensors** - attn\_gate, attn\_q, ssm\_beta, ssm\_alpha using MXFP4 is not a good idea, and rather Q4\_K is better - also MXFP4 uses 4.25 bits per weight, whilst Q4\_K uses 4.5 bits per weight. It's better to use Q4\_K than MXFP4 when choosing between them.

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FH8FliHXsetx9lLoKelPX%2Fnew-qwen3-5-35b-a3b-unsloth-dynamic-ggufs-benchmarks-v0-xgugdgzmv2mg1.webp?alt=media&amp;token=f0c49e94-571e-4883-84fe-2c4634d425eb" alt="" width="563"><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FEWsX87d1Ig42Uk81fpJo%2Ffixed%20the%20grapg.png?alt=media&amp;token=323932fd-8344-4f6c-b8c3-47cc1b1f6ccf" alt="" width="563"><figcaption><p>As you can see MXFP4 is unusually high</p></figcaption></figure></div>

### **2) Imatrix works very well**

* Imatrix definitely helps weight the quantization process in the right way. For example previously ssm\_out at 2bits was really bad, however imatrix reduces the 99.9% KLD by a lot.
* Imatrix generally helps on lower bits, and works on all quants and bit widths.
*

```
<figure><img src="/files/XupSDj6NIkVMlHERvgTI" alt=""><figcaption></figcaption></figure>
```

I quants (iq3\_xxs, iq2\_s etc) makes inference 5-10% slower, they're definitely better in terms of efficiency, but there is a tradeoff.

| Type     | pp512 (≈) | tg128 (≈) |
| -------- | --------- | --------- |
| mxfp4    | 1978.69   | 90.67     |
| q4\_k    | 1976.44   | 90.38     |
| q3\_k    | 1972.61   | 91.36     |
| q6\_k    | 1964.55   | 90.50     |
| q2\_k    | 1964.20   | 90.77     |
| q8\_0    | 1964.17   | 90.33     |
| q5\_k    | 1947.74   | 90.72     |
| iq3\_xxs | 2030.94   | 85.68     |
| iq2\_xxs | 1997.64   | 85.79     |
| iq3\_s   | 1990.12   | 84.37     |
| iq2\_xs  | 1967.85   | 85.19     |
| iq2\_s   | 1952.50   | 85.04     |

### **3) Perplexity & KLD can be misleading**

Perplexity and KLD can be misleading as they’re highly influenced by calibration. Most GGUFs are evaluated on Wiki-test with 512 context windows, so results shift a lot if the GGUF’s imatrix calibration set includes Wikipedia-like and 512 context samples (as most GGUFs do). That’s why our GGUFs sometimes show higher perplexity as our imatrix data rather uses long-context chat and tool-calling examples instead.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FhfO2gsbz2lWrZXg3ojyE%2FHCGBTzgboAASv_A.png?alt=media&amp;token=7d6334ca-4f3c-4946-aacd-d55527375fce" alt="" width="563"><figcaption></figcaption></figure>

[Benjamin’s recent MiniMax‑M2.5 analysis](https://x.com/bnjmn_marie/status/2027043753484021810) shows a case how perplexity and KLD can be very misleading. Unsloth Dynamic IQ2\_XXS performs better than AesSedai’s IQ3\_S on real world evals (LiveCodeBench v6, MMLU Pro) despite being 11GB smaller. Yet, AesSedai’s perplexity and KLD benchmarks suggest the opposite. (PPL: 0.3552 vs 0.2441; KLD: 9.0338 vs 8.2849 - lower is better).

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F7csgZI82adnvKmQQVlp1%2F01_kld_vs_filesize_pareto.png?alt=media&amp;token=d907a2c0-7df5-4e6a-9d9b-0524c8e6ae77" alt="" width="188"><figcaption><p>KL Divergence - AesSedai</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fd8KBa3uNhkDEZzq32v7q%2F02_ppl_vs_filesize_pareto.png?alt=media&amp;token=d471fce1-7482-4fde-bc98-2d10503253a4" alt="" width="188"><figcaption><p>Perplexity - AesSedai</p></figcaption></figure></div>

This mismatch shows how lower perplexity or KLD doesn’t necessarily translate to better real-world performance. The graph also shows UD‑Q4-K‑XL outperforming other Q4 quants, while being \~8GB smaller. This doesn’t mean perplexity or KLD is useless, as they provide a rough signal. So, going forward, we’ll publish perplexity and KLD for every quant so the community has some sort of reference.

### 4) March 5th 2026 Update - more robustness

We further enhanced our quantization method for Qwen3.5 MoEs to reduce Maximum KLD directly. 99.9% is what is generally used, but for massive outliers, Maximum KLD can be useful. Our New method generally pushes the Maximum KLD quite a much down vs the pre March 5th update.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fqxt3Dv8HIOWG8y3RvNYf%2FCode_Generated_Image(11).png?alt=media&amp;token=54e20159-4243-42cf-89de-d2c9d7b6409b" alt=""><figcaption></figcaption></figure>

| Quant        | Old GB     | New GB       | Old Max KLD | New Max KLD        |
| ------------ | ---------- | ------------ | ----------- | ------------------ |
| UD-Q2\_K\_XL | 12.0       | ***11.3***   | 8.237       | ***8.155***        |
| UD-Q3\_K\_XL | 16.1       | ***15.5***   | 5.505       | ***5.146***        |
| UD-Q4\_K\_XL | ***19.2*** | 20.7 (+7.8%) | 5.894       | ***2.877 (-51%)*** |
| UD-Q5\_K\_XL | ***23.2*** | 24.6 (+6%)   | 5.536       | ***3.210 (-42%)*** |

### Full Benchmarks

| Quantizer | Quant Level      | Disk Space (GB) | PPL    | KLD 99.9% | Mean KLD |
| --------- | ---------------- | --------------- | ------ | --------- | -------- |
| AesSedai  | IQ3\_S           | 12.65           | 6.9152 | 1.8669    | 0.0613   |
| AesSedai  | IQ4\_XS          | 16.4            | 6.6447 | 0.8067    | 0.0235   |
| AesSedai  | Q4\_K\_M         | 20.62           | 6.5665 | 0.3171    | 0.0096   |
| AesSedai  | Q5\_K\_M         | 24.45           | 6.5356 | 0.21      | 0.0058   |
| Ubergarm  | Q4\_0            | 19.79           | 6.5784 | 0.4829    | 0.0142   |
| Unsloth   | IQ2\_XXS         | 9.09            | 7.716  | 4.2221    | 0.1846   |
| Unsloth   | Q2\_K\_XL        | 12.04           | 7.0438 | 2.9092    | 0.097    |
| Unsloth   | IQ3\_XXS         | 13.12           | 6.7829 | 1.5296    | 0.0501   |
| Unsloth   | IQ3\_S           | 14.13           | 6.7715 | 1.4193    | 0.0457   |
| Unsloth   | Q3\_K\_M         | 15.54           | 6.732  | 0.9726    | 0.0324   |
| Unsloth   | Q3\_K\_XL        | 16.06           | 6.7245 | 0.9539    | 0.0308   |
| Unsloth   | MXFP4\_MOE       | 18.17           | 6.6    | 0.7789    | 0.0272   |
| Unsloth   | Q4\_K\_M         | 18.49           | 6.6053 | 0.5478    | 0.0192   |
| Unsloth   | Q4\_K\_L         | 18.82           | 6.5905 | 0.4828    | 0.015    |
| Unsloth   | Q4\_K\_XL        | 19.17           | 6.5918 | 0.4097    | 0.0137   |
| Unsloth   | Q5\_K\_XL        | 23.22           | 6.5489 | 0.236     | 0.0069   |
| Unsloth   | Q6\_K\_S         | 26.56           | 6.5456 | 0.2226    | 0.0065   |
| Unsloth   | Q6\_K\_XL        | 28.22           | 6.5392 | 0.1437    | 0.0041   |
| Unsloth   | Q8\_K\_XL        | 36.04           | 6.5352 | 0.1033    | 0.0026   |
| bartowski | Qwen\_IQ2\_XXS   | 8.15            | 9.3427 | 6.0607    | 0.3457   |
| bartowski | Qwen\_Q2\_K\_L   | 11.98           | 7.5504 | 3.8095    | 0.1559   |
| bartowski | Qwen\_IQ3\_XXS   | 12.94           | 7.0938 | 2.1563    | 0.0851   |
| bartowski | Qwen\_Q3\_K\_M   | 14.95           | 6.772  | 1.7779    | 0.0585   |
| bartowski | Qwen\_Q3\_K\_XL  | 15.97           | 6.8245 | 1.7516    | 0.0627   |
| bartowski | Qwen\_IQ4\_XS    | 17.42           | 6.6234 | 0.7265    | 0.0234   |
| bartowski | Qwen\_Q4\_K\_M   | 19.77[^1]       | 6.6097 | 0.5771    | 0.0182   |
| bartowski | Qwen\_Q5\_K\_M   | 23.11           | 6.5828 | 0.3549    | 0.0106   |
| noctrex   | MXFP4\_MOE\_BF16 | 20.55           | 6.5948 | 0.7939    | 0.0248   |
| noctrex   | MXFP4\_MOE\_F16  | 20.55           | 6.5937 | 0.7614    | 0.0247   |

[^1]: Bartowski's Q4\_K\_M is 1Gb bigger than Unsloth's


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/qwen3.5/gguf-benchmarks.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
