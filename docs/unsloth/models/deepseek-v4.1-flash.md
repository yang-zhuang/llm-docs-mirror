> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/deepseek-v4.1-flash.md).

# DeepSeek-V4.1-Flash: Run Locally Guide

Run DeepSeek-V4.1-Flash-1017 locally with Unsloth GGUFs and Engram n-gram offloading.

**DeepSeek-V4.1-Flash-1017** is the new update to V4.1-Flash, making it the **strongest** open model to date for coding, agentic tasks and more. With 1M context, its **552B** backbone + **196B Engram** parameters support SSD offloading to reduce RAM/VRAM needs. This guide shows how to run DeepSeek-V4.1 locally with Unsloth [Dynamic V3.1](#dynamic-v3.1-update-october-30th-2026) GGUFs which has **10-15% increased accuracy** and **30% less token usage** vs other quants of the same size.

[Unsloth Desktop](/docs/desktop.md) + llama.cpp enables \~**3x faster** DeepSeek-V4.1 inference than other CPU/VRAM/ngram repos. DeepSeek and runs locally on 128GB+ RAM setups or 64GB RAM (slower). `UD-Q8_K_XL` (lossless) is **508.4 GB**, while `UD-Q4_K_XL` (near lossless) is **500.7 GB**. GGUF: [**DeepSeek-V4.1-Flash-1017-GGUF**](https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF)

<a href="/pages/P265CJSPfOXTtJ9qxh3j#run-deepseek-v4.1-flash-1017-tutorials" class="button primary">Run DeepSeek-V4.1 Tutorials</a>

### Dynamic V3.1 Update (November 2nd 2026)

We're releasing new DeepSeek-V4.1-Flash-1017 GGUFs which using our new [**Unsloth Dynamic**](/docs/basics/dynamic-3.0-ggufs.md) **V3.1 (preview) algorithm** which improves Unsloth quants on nearly all benchmarks and is the best in class vs other providers.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FXC2NHQCS4KKsMoY4IjpT%2Fimage.png?alt=media&amp;token=67fb9d55-8fbb-4f35-a13f-83465cee8475" alt="" width="563"><figcaption></figcaption></figure>

If we benchmark ISTA's Coder model as well, we see the pruned Coder model does much worse on Agentic tasks - Aider Polyglot can get 47.6% accuracy vs 78.2% and is only 20% smaller in size. This partially means every 1% decrease in size is associscated with a \~1% decrease in accuracy.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fe3HYFau6qEpkFwkLVwru%2FCoder%20benchmark.png?alt=media&amp;token=59e2ab09-3f42-4226-bd03-3b5a8d109e6a" alt="" width="563"><figcaption></figcaption></figure>

**We ran agentic benchmarks including Terminal Bench 2.1, DeepSWE v1.1,** Automation Bench v1.0.6, Aider Polyglot, and general benchmarks like SciCode, HLE Diamond (text-only), LiveCodeBench v6, GPQA Diamond, MMLU-Pro, AIME25, IFEval, MATH-500 (Level 5), HMMT 2025, HMMT 2026. We addressed some issues people mentioned with these new benchmarks:

* 32K context was too short - we did **512K context for agentic** + 128K for general tasks
* Saturated benchmarks - new **unsaturated agentic style ones** including Terminal Bench, DeepSWE and Automation Bench
* Benchmarks are noisy - we did **35.1B tokens of benchmarking vs 1.3B before so 27x more data**. See [#benchmark-runs-per-model](#benchmark-runs-per-model "mention") where we did 64x AIME 2025 runs, 3x DeepSWE, 3x TB runs and more.
* Our graders are wrong - we used [Math Verify](https://huggingface.co/blog/math_verify_leaderboard), improved graders, used gpt-6-luna xhigh for HLE, and all official graders for Terminal Bench (Harbor), DeepSWE and the rest. See [#graders](#graders "mention") and [#infrastructure-and-benchmark-issues-and-fixes](#infrastructure-and-benchmark-issues-and-fixes "mention")

Full benchmark results are provided as well, with the first plot being a percentage accuracy recovery from the baseline and averaged across all 14 benchmarks (not weighted). This approximately is a metric of what each quant retains in accuracy vs the DeepSeek baseline.

For a [full breakdown of our benchmarks, see here.](#gguf-benchmark-breakdown)

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQumjSkZM3UWgSRSa5taa%2Fimage.png?alt=media&amp;token=23092c27-abae-4376-b44a-7ae91f918705" alt=""><figcaption></figcaption></figure>

#### We still cannot reproduce GSQ-RCO's recovery numbers

GSQ-RCO IQ1\_M claims 98.7% recovery, but we measured 97.24 \[96.23, 98.21] with a **p-value of 0.0013** (statistically significant so extremly unlikely)

GSQ-RCO IQ2\_XS retaining 100% claimed recovery is possible with a p-value of 0.21. We measured 98.38% \[97.52, 99.22].

GSQ-RCO IQ2\_XXS claims 99.80% recovery but we measured 98.38 \[97.52, 99.22] with a **p-value of 0.0001 (extremey significant)**.

The claimed recovery tested directly against our measurement (the card's definition: sum of the 3 scores / the base's sum, vs official FP8/FP4): p (no loss) = paired sign-flip permutation test of recovery = 100%; p (recovery >= claim) = one-sided paired bootstrap over questions.

|                  | Claimed recovery | Measured recovery \[95% CI] | p (no loss) | p (recovery >= claim) |
| ---------------- | ---------------: | --------------------------: | ----------: | --------------------: |
| GSQ-RCO IQ1\_M   |            98.70 |       97.24 \[96.23, 98.21] |     0.00002 |                0.0013 |
| GSQ-RCO IQ2\_XXS |           100.00 |       98.38 \[97.52, 99.22] |      0.0003 |                0.0001 |
| GSQ-RCO IQ2\_XS  |            99.80 |      99.54 \[98.88, 100.18] |        0.16 |                  0.21 |

Claimed vs true recovery per benchmark, all against official FP8/FP4 (the card's baseline). Claimed = card score / card base; true = our mean over 12-64 samples per question / the official model's mean on the same questions, paired 95% bootstrap CI. p (true >= claim): one-sided paired bootstrap, the chance the true recovery reaches the claimed figure. p (no loss): two-sided paired permutation test of true recovery = 100% (each question's quant / official pair swapped at random). Unsloth quants (measured only) for reference at similar sizes.

| Model            |                   |                  AIME25 |                  GPQA-D |                  LCB v6 | 3 benchmarks (card definition) |
| ---------------- | ----------------- | ----------------------: | ----------------------: | ----------------------: | -----------------------------: |
| GSQ-RCO IQ1\_M   | claimed (card)    |                  100.00 |                   97.22 |                   98.73 |                          98.69 |
|                  | true (measured)   |   98.37 \[97.06, 99.53] |   96.83 \[94.60, 98.89] |   96.44 \[94.69, 98.08] |          97.24 \[96.24, 98.21] |
|                  | p (true >= claim) |                  0.0028 |                    0.38 |                  0.0027 |                         0.0014 |
|                  | p (no loss)       |                   0.019 |                  0.0041 |                 <0.0001 |                        <0.0001 |
| GSQ-RCO IQ2\_XXS | claimed (card)    |                  100.00 |                  100.00 |                  100.00 |                         100.00 |
|                  | true (measured)   |  99.53 \[98.84, 100.21] |   97.73 \[95.80, 99.61] |   97.80 \[96.08, 99.39] |          98.38 \[97.52, 99.23] |
|                  | p (true >= claim) |                     0.1 |                  0.0092 |                  0.0027 |                        <0.0001 |
|                  | p (no loss)       |                    0.25 |                   0.022 |                  0.0085 |                        0.00025 |
| GSQ-RCO IQ2\_XS  | claimed (card)    |                  100.00 |                   99.44 |                  100.00 |                          99.82 |
|                  | true (measured)   |  99.58 \[98.53, 100.47] |  99.45 \[98.12, 100.73] |  99.58 \[98.47, 100.70] |         99.54 \[98.88, 100.17] |
|                  | p (true >= claim) |                    0.21 |                    0.51 |                    0.24 |                           0.19 |
|                  | p (no loss)       |                    0.48 |                    0.43 |                    0.52 |                           0.17 |
| UD IQ1\_S        | true (measured)   |  99.58 \[98.96, 100.21] |   97.42 \[95.41, 99.39] | 100.21 \[99.03, 101.38] |          99.08 \[98.29, 99.85] |
|                  | p (no loss)       |                    0.26 |                   0.011 |                    0.73 |                          0.023 |
| UD IQ1\_M        | true (measured)   |  99.68 \[98.94, 100.42] |   98.37 \[96.95, 99.76] | 100.37 \[99.15, 101.61] |         99.48 \[98.82, 100.14] |
|                  | p (no loss)       |                    0.52 |                   0.025 |                    0.56 |                           0.13 |
| UD IQ2\_XXS      | true (measured)   | 100.00 \[99.32, 100.58] |  99.53 \[98.36, 100.68] | 100.47 \[99.27, 101.74] |        100.00 \[99.40, 100.58] |
|                  | p (no loss)       |                       1 |                    0.45 |                    0.46 |                              1 |
| UD Q2\_K\_XL     | true (measured)   |  99.79 \[99.16, 100.37] |  99.74 \[98.69, 100.77] | 100.89 \[99.90, 101.93] |        100.13 \[99.63, 100.65] |
|                  | p (no loss)       |                    0.63 |                    0.66 |                   0.076 |                           0.62 |
| UD-Q8\_K\_XL     | true (measured)   |  99.47 \[97.94, 100.53] | 100.28 \[99.52, 101.09] | 100.89 \[99.95, 101.95] |        100.19 \[99.53, 100.77] |
|                  | p (no loss)       |                    0.73 |                    0.48 |                   0.084 |                           0.59 |

#### AIME 2025 questions GSQ-RCO IQ1\_M got wrong

GSQ-RCO IQ1\_M scores 97.34% on AIME 2025 (51 wrong of 1,920 samples, 64 per question) and misses at least one sample on 15 of the 30 questions, so a 30/30 single run happens about 43% of the time. Every wrong answer is a genuinely wrong value (2 hit the 128K cap without a final answer). Other models' correct counts on the same questions for reference:

| Question (answer) | GSQ IQ1\_M wrong / samples | Wrong answers given                                   | Official correct | UD-Q8\_K\_XL correct | UD IQ1\_S correct | GSQ IQ2\_XS correct |
| ----------------- | -------------------------: | ----------------------------------------------------- | ---------------: | -------------------: | ----------------: | ------------------: |
| Q15 (735)         |                       9/64 | 637 x2, 833 x2, 271, 636, 613, 52, 539                |            31/32 |                60/64 |             59/64 |               56/64 |
| Q28 (248)         |                       8/64 | 888, 256, 608, 808, 632, 592, 136, 448                |            31/32 |                63/64 |             60/64 |               64/64 |
| Q22 (237)         |                       6/64 | 57, 993, 945, 249, 473, 125                           |            32/32 |                63/64 |             62/64 |               64/64 |
| Q13 (204)         |                       5/64 | \frac{587}{3}, 154, \frac{662}{3}, \frac{562}{3}, 179 |            31/32 |                64/64 |             63/64 |               63/64 |
| Q24 (149)         |                       5/64 | 150 x4, 145                                           |            30/32 |                48/64 |             63/64 |               55/64 |
| Q5 (279)          |                       4/64 | 9 x2, 135, 423                                        |            32/32 |                63/64 |             63/64 |               63/64 |
| Q4 (117)          |                       3/64 | 119 x3                                                |            31/32 |                64/64 |             62/64 |               64/64 |
| Q11 (259)         |                       2/64 | 23, 261                                               |            32/32 |                64/64 |             64/64 |               64/64 |
| Q14 (60)          |                       2/64 | no final answer (128K cap) x2                         |            31/32 |                64/64 |             63/64 |               64/64 |
| Q18 (82)          |                       2/64 | 106, 712                                              |            32/32 |                63/64 |             64/64 |               64/64 |
| Q2 (588)          |                       1/64 | 1176                                                  |            32/32 |                64/64 |             64/64 |               64/64 |
| Q3 (16)           |                       1/64 | 520                                                   |            31/32 |                63/64 |             62/64 |               63/64 |
| Q7 (821)          |                       1/64 | 271                                                   |            32/32 |                63/64 |             63/64 |               63/64 |
| Q19 (106)         |                       1/64 | 317                                                   |            32/32 |                63/64 |             63/64 |               63/64 |
| Q29 (104)         |                       1/64 | 55                                                    |            32/32 |                64/64 |             64/64 |               62/64 |

Q28 and Q22 are quantization damage (IQ1\_M misses 8 and 6 of 64; GSQ IQ2\_XS and the official model almost never do); Q15 and Q24 are hard for every model (UD-Q8\_K\_XL gets Q24 right 48/64, often answering 150 for 149).

### Dynamic V3.1 Update (October 30th 2026)

We ran AIME25, Aider Polyglot, LiveCodeBench v6, HMMT 2026, GPQA Diamond, MMLU-Pro, IFEval and more across all our quants for UDv3 and UD3.1 vs the GSQ-RCO variants which claims to recover 100% on AIME25 for all quants, but we could not reproduce those numbers.

We provide a full average of 6 benchmarks (excluding Aider Polyglot - if you include Aider it's even more pronounced), and show UD3.1 does great across nearly all tasks.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FOuLKE4mwn1xkCJchptDN%2Ftotal_ista.png?alt=media&amp;token=cdc15dba-6b30-4ca3-8318-94138acf6d27" alt=""><figcaption></figcaption></figure>

#### We cannot reproduce GSQ-RCO's numbers

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FgEHmQB9WBKLJ1vMssB6N%2Fclaims_ista.png?alt=media&amp;token=838ee657-1085-4c00-bcdb-66abbe2862c1" alt=""><figcaption></figcaption></figure>

The GSQ-RCO DeepSeek-V4.1-Flash-1017 quants which are created by ISTA-DASLab mentioned they scored 100% on AIME25 for all quants - we could not reproduce this, and show on AIME25 across multiple runs and after you average them, **GSQ-RCO retains 94.64% of the baseline (not 100%)**. We scaled all baseline numbers as well on the 2nd plot to account for methodology differences.

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FMFdsiPUHkPAXMYPblKDx%2Fgsq_rco_claims_vs_true_bars(1).png?alt=media&amp;token=99b6f559-52fe-481f-911a-92b559cfd01f" alt=""><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FDHa3imd8XoDXehkvATcC%2Fgsq_rco_claims_vs_true_bars_recovery.png?alt=media&amp;token=244b229c-1b23-47e3-bfa5-d0b9631f426b" alt=""><figcaption></figcaption></figure></div>

For AIME25 specifically ISTA reported 100% accuracy for all 3 quants, however when we tested it on AIME25 16 times per question for each quant: 30 problems \* 16 samples = 480 answers per quant with temperature 1.0, reasoning effort 50, we see a clear degradation for quants, and not 100% accuracy at all bit widths.&#x20;

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FtcF0k9ss042lXLgvDyIt%2Faime25.png?alt=media&amp;token=8025e417-e669-43cb-bf8f-ce69a9254aca" alt="" width="375"><figcaption></figcaption></figure>

The GSQ-RCO benchmarks are conducted with reasoning effort 50 as well as per the README.md

#### KLD is a reasonable metric

There are some recent claims that KLD is not a good metric. KL divergence (KLD) measures how far a quantized model's next-token predictions drift from a reference model's predictions on the same text.

$$
\text{min  } D\_{KL} \large( \theta, \hat{\theta}\large)
$$

**The primary goal of quantization is to minimize KLD to 0, whilst also reducing the disk space of the quantized model** (you can also include other items to optimize like generation speed for example).

If you have a KLD of 0, then the model has perfectly reconstructed the output logits, and so the quantized model creates 100% the same output as the original model.

You can see GSQ-RCO clearly having higher KLD and lower top-1% agreement vs even our old Unsloth v3 quants - v3.1 further improves it.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F0YkDIvosvnP6nRVlhNy5%2FKLD%20ISTA.png?alt=media&amp;token=a4601232-2858-4b8d-a618-8991a48eeb6d" alt=""><figcaption></figcaption></figure>

Some people say that KLD can be "gamed" or benchmaxed by cheating and running KLD on the test set, or using 1 dataset to run KLD on. To test this theory, we ran it across multiple held out tests, and show UDv3.1 does better than GSQ-RCO on all areas.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FBBJeFPqCiW0Al9IvGNsC%2Fsize_vs_kld_per_axis(2).png?alt=media&amp;token=08452280-2005-4fa9-bdc7-a37f162b49e7" alt=""><figcaption></figcaption></figure>

We also provide top-1% agreement for all held out tests as well:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FcCroCNVfybzFZ7lAMHVy%2Fsize_vs_top1_per_axis(2).png?alt=media&amp;token=a7f50164-e15c-45ef-911b-e73882436845" alt=""><figcaption></figcaption></figure>

#### Quantization increases reasoning lengths

We also tested if lower bit quants think for longer - we set all tests at a 32K context length and fail quants if they think for too long. We also ran Livecodebench for up to 128K tokens, and the results are similar. We provide the number of answers that are truncated across all 6 bechmarks, and show that Unsloth quants truncate much less than GSQ's quants (so we think less).

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FEKPO459yFA9vQwKohCR0%2Ftruncation.png?alt=media&amp;token=e8ddafad-7f4e-4891-a329-511ffd177365" alt=""><figcaption></figcaption></figure>

However this does show that quantization increases thinking reasoning lengths, so be prepared to have a higher reasoning budget for smaller bit quants.

#### Engram removal for benchmarks

We also removed the engram for graphing, but this does not change anything, as all low bit quants use IQ4\_NL as the engram - Q2\_K\_XL and IQ2\_XXS use Q5\_K.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fzggh3ij4y2HInPA0LU80%2Fremove%20engram.png?alt=media&amp;token=5900687a-ad79-4d69-8650-318fa3a17d61" alt=""><figcaption></figcaption></figure>

#### Full Benchmarking results

| Quant                    | Size GB | AIME25 | HMMT Feb26 | GPQA-D | MMLU-Pro | IFEval | LCB v6 (32K) | Avg of 6 | Aider pass\@1 | Truncated % (6) |
| ------------------------ | ------: | -----: | ---------: | -----: | -------: | -----: | -----------: | -------: | ------------: | --------------: |
| UD-Q8\_K\_XL (reference) |   508.4 |  97.08 |      68.94 |  90.47 |    88.61 |  95.10 |        85.90 |    87.68 |             - |            1.48 |
| UD-Q2\_K\_XL (v3.1)      |   334.8 |  97.50 |      69.89 |  89.58 |    88.28 |  94.92 |        84.76 |    87.49 |             - |            2.10 |
| UD-IQ2\_XXS (v3.1)       |   300.5 |  96.88 |      67.61 |  88.95 |    87.53 |  95.19 |        83.62 |    86.63 |         44.38 |            2.71 |
| UD-IQ1\_M (v3.1)         |   250.4 |  95.00 |      62.88 |  88.38 |    87.53 |  95.10 |        84.38 |    85.55 |         42.13 |            2.91 |
| UD-IQ1\_S (v3.1)         |   233.0 |  92.92 |      57.01 |  87.63 |    86.62 |  94.92 |        82.10 |    83.53 |         36.52 |            4.15 |
| GSQ-RCO IQ2\_XS          |   265.8 |  95.00 |      64.39 |  88.64 |    86.62 |  94.27 |        84.95 |    85.64 |         41.57 |            2.83 |
| GSQ-RCO IQ2\_XXS         |   248.8 |  95.21 |      57.95 |  85.80 |    86.53 |  93.72 |        82.86 |    83.68 |         36.52 |            4.00 |
| GSQ-RCO IQ1\_M           |   231.3 |  91.88 |      53.60 |  85.10 |    85.49 |  91.77 |        82.86 |    81.78 |         29.78 |            4.69 |

#### Full benchmarking methodologies

| Benchmark       | Source (revision)                          | Items |               Samples / item |       Max tokens | Seed base           | Prompt                                                                             | Grader                                                                 |
| --------------- | ------------------------------------------ | ----: | ---------------------------: | ---------------: | ------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| AIME25          | MathArena/aime\_2025 (c94da77e)            |    30 |                           16 |           32,768 | 20261029            | problem + "Please reason step by step, and put your final answer within \boxed{}." | math\_verify on the last \boxed{}, fallback exact integer              |
| HMMT Feb26      | MathArena/hmmt\_feb\_2026                  |    33 |                           16 |           32,768 | 20261029            | as AIME25                                                                          | math\_verify                                                           |
| GPQA-D          | Idavidrein/gpqa diamond (633f5ee8)         |   198 | 8 (4 + 4; earlier uploads 4) |           32,768 | 20261026 + 20261029 | OpenAI simple-evals multiple-choice template                                       | last "Answer: X", fallbacks \boxed{X}, "answer is (X)", lone letter    |
| MMLU-Pro        | 1,203-item stratified subset               | 1,203 |                            2 |           32,768 | 20261029            | simple-evals style, up to 10 options                                               | last "Answer: X"                                                       |
| IFEval          | google/IFEval                              |   541 |                            2 |           32,768 | 20261029            | raw prompt                                                                         | official instruction\_following\_eval, strict, prompt level            |
| LCB v6 (32K)    | livecodebench/code\_generation\_lite test6 |   175 |                            3 |           32,768 | 20261026            | official LCB system + user prompt                                                  | official extract\_code + run\_test, 6 s per test, sandboxed subprocess |
| Avg of 6        | All benchmarks above                       |       |                              |                  |                     |                                                                                    | mean of the 9 pass\@1 values                                           |
| Aider pass\@1   | Aider Polyglot                             |   225 |                      1 trial | 32,768 per reply | n/a                 | official aider benchmark in Docker                                                 | the exercise's unit tests                                              |
| Truncated % (6) | the 6 benchmarks                           |       |                              |           32,768 |                     |                                                                                    | share of answers ending at the token cap                               |

### ⚙️ Usage Guide

**DeepSeek-V4.1-Flash-1017** pairs MoE with **Engram conditional memory**: n-grams of up to four tokens access a few table rows per token, so the table need not stay in GPU memory. It's best to use Unsloth for inference as it enables up to **3x faster** DeepSeek-V4.1 inference than other CPU/VRAM/ngram-focused repos by optimizing ontop of llama.cpp.

1-bit `UD-IQ1_S` will work on 128GB RAM setups like a Macbook, DGX Spark or RTX Spark while 3-bit `UD-IQ3_XXS` will work on 256GB RAM setups like a Mac Studio.

Like the PLE / n-gram layers in our [Qwen3.8-Flash-Next](/docs/models/qwen3.8-next.md) guide, Engram’s 110.6–202.8 GB table can stay on SSD via mmap. Rows load on demand into the OS cache, saving RAM/VRAM while retaining the full disk requirement.

#### **DeepSeek-V4.1-Flash-1017 Requirements:**

**Table: Hardware requirements** (RAM + VRAM, or unified memory; Engram on SSD).

| 1-bit      | 2-bit      | 3-bit      | 4-bit  | 8-bit  |
| ---------- | ---------- | ---------- | ------ | ------ |
| 128–145 GB | 176–205 GB | 256–290 GB | 305 GB | 315 GB |

Estimates allow roughly 5–10 GB above non-Engram weights. Runtime and context can require more.

**n-gram storage:** Lookup formats and weight sizes appear below. Rest GB is the absolutely minimum amount of RAM/VRAM that is needed.

| Quant        | N-gram format / GB | Rest GB |
| ------------ | ------------------ | ------- |
| UD-IQ1\_S    | IQ4\_NL / 110.6    | 122.4   |
| UD-IQ1\_M    | IQ4\_NL / 110.6    | 139.8   |
| UD-IQ2\_XXS  | Q5\_K / 135.2      | 165.3   |
| UD-Q2\_K\_XL | Q5\_K / 135.2      | 199.6   |
| UD-IQ3\_XXS  | Q6\_K / 161.3      | 233.5   |
| UD-IQ3\_S    | Q6\_K / 161.3      | 262.3   |
| UD-Q3\_K\_XL | MXFP8 / 202.8      | 282.3   |
| UD-Q4\_K\_XL | MXFP8 / 202.8      | 297.9   |
| UD-Q8\_K\_XL | MXFP8 / 202.8      | 305.6   |

### Recommended Settings

DeepSeek recommends temperature = 1.0, top-p = 1.0 and disabling top-k and min-p:

| Parameter              | Setting            |
| ---------------------- | ------------------ |
| `temperature`          | `1.0`              |
| `top_p`                | `1.0`              |
| Maximum context window | `1,048,576` tokens |

DeepSeek recommends allowing **at least 256K output tokens** for its long-generation setup.

### 📊 Quantization Analysis

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FZbUjhpI7wJTjf3pM1uwu%2Fsize_vs_top1(1).png?alt=media&amp;token=4e133008-8026-4e93-baa7-d7f2e2b81ecc" alt=""><figcaption></figcaption></figure>

Results compare against DeepSeek’s official reference on wiki1100 and long17k. Lower KL means closer next-token probabilities; higher top-1 means more matching predictions.

DeepSeek mixes **MXFP4**, FP8 and BF16. Q4 and Q8 retain **MXFP4** experts and the same Engram table; their labels do not describe every tensor’s precision. Q4 stores many non-expert weights in Q8\_0; Q8 uses BF16.

We also show when we change the engram precision from IQ4\_NL to Q5\_K to Q6\_K and MXFP8 and we provide **standalone engrams which allow you to mix n match.**

| Quant        | Total size | wiki1100 KL / top-1 | long17k KL / top-1 |
| ------------ | ---------- | ------------------- | ------------------ |
| UD-IQ1\_S    | 233.0 GB   | 0.457 / 82.8%       | 0.364 / 85.1%      |
| UD-IQ1\_M    | 250.4 GB   | 0.314 / 87.1%       | 0.241 / 88.2%      |
| UD-IQ2\_XXS  | 300.5 GB   | 0.203 / 90.5%       | 0.142 / 91.2%      |
| UD-Q2\_K\_XL | 334.8 GB   | 0.138 / 91.5%       | 0.0879 / 93.3%     |
| UD-IQ3\_XXS  | 394.7 GB   | 0.0625 / 94.6%      | 0.043 / 95.1%      |
| UD-IQ3\_S    | 423.6 GB   | 0.0316 / 96.0%      | 0.0195 / 96.8%     |
| UD-Q3\_K\_XL | 485.1 GB   | 0.0204 / 96.5%      | 0.0114 / 97.4%     |
| UD-Q4\_K\_XL | 500.7 GB   | 9.00e-03 / 98.2%    | 4.46e-03 / 98.5%   |
| UD-Q8\_K\_XL | 508.4 GB   | 4.76e-03 / 98.5%    | 2.81e-03 / 98.7%   |

**Choosing a quant:** IQ1\_S saves about 54% disk space versus Q8. IQ1\_M adds 17.4 GB and improves top-1 agreement by 4.3 points on wiki1100 and 3.1 on long17k. IQ3 variants reach 94.6–96.8% agreement.

#### **Thinking effort**

Thinking is enabled by default, with `reasoning_effort=75` (“high”). You can set an integer from **1 to 100**. Higher values ask the model to reason more thoroughly; they are not a token limit. The included template also accepts `low` = 50, `medium` = 62, `high` = 75 and `max` = 100.

For example, add one of these options to your launch command:

```bash
# Default thinking effort
--chat-template-kwargs '{"reasoning_effort":75}'

# Maximum thinking effort
--chat-template-kwargs '{"reasoning_effort":100}'

# Disable thinking
--chat-template-kwargs '{"enable_thinking":false}'
```

## Run **DeepSeek-V4.1-Flash-1017** Tutorials:

For this tutorial, we use `UD-Q2_K_XL`. Unsloth automatically selects the near optimal DeepSeek-V4.1 offloading, ngram etc. configurations ensuring your setup gets the near best speed possible.

### 🦥 Unsloth Guide

[Unsloth Desktop](https://unsloth.ai/docs/desktop) is our open-source UI for local AI on macOS, Windows and Linux. You can search and download GGUFs, configure CPU and GPU offloading, adjust inference settings and connect tools from one app.

{% stepper %}
{% step %}

#### Install Unsloth

The easiest way to get started is by downloading the [Unsloth Desktop app](/docs/desktop.md). Works on [macOS](/docs/get-started/install/mac.md), [Windows](/docs/get-started/install/windows-installation.md), and [Linux](/docs/get-started/install/linux.md).

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

Or, if you prefer to install manually:
{% endstep %}

{% step %}

#### Search and download DeepSeek-V4.1-Flash-1017

Go to [Unsloth Chat](/docs/new/studio/chat.md) or Model hub, search for **DeepSeek-V4.1-Flash-1017** and select [unsloth/DeepSeek-V4.1-Flash-1017-GGUF](https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF). Download your desired quant using the sizes and memory requirements above.
{% endstep %}

{% step %}

#### Run DeepSeek-V4.1-Flash-1017

Thinking is enabled by default with `75`, you can change it in our toggle. Unsloth automatically selects the near optimal DeepSeek-V4.1 offloading, ngram etc. configurations ensuring your setup gets the near best speed possible.

For more information, you can view our [Unsloth inference guide](/docs/new/studio/chat.md).

With UD-IQ1\_S, the 233.0 GB download includes a 110.6 GB Engram n-gram table and 122.4 GB of other weights. Use Engram on-demand loading to keep the lookup table on SSD, with additional RAM/VRAM for cached rows, context and runtime buffers. Follow the Usage Guide above for memory requirements.
{% endstep %}

{% step %}

#### Serve DeepSeek-V4.1-Flash-1017 with Unsloth API

You can use `unsloth run` command and serve DeepSeek-V4.1-Flash-1017 via an API using `llama-server` runtime flags, including context sizing, GPU layers, threading, sampling, networking, and tool configuration. For more info see our [API docs](/docs/basics/api.md) or [unsloth start](/docs/integrations/unsloth-start.md).

{% code overflow="wrap" %}

```bash
unsloth run --model unsloth/DeepSeek-V4.1-Flash-1017-GGUF:UD-Q2_K_XL \
    --temp 1.0 \
    --top-p 1.0 \
    --min-p 0.0 \
    --chat-template-kwargs '{"reasoning_effort":75}'
```

{% endcode %}

Use a runtime with DeepSeek-V4.1-1017 and Engram on-demand loading support. Apply the SSD-offload and memory settings from the Usage Guide when keeping the n-gram table on disk.
{% endstep %}

{% step %}

#### Unsloth is now ready

You can connect DeepSeek-V4.1-Flash-1017 to your tools through Unsloth Desktop. Unsloth also supports the following workflows:

* **Connect tools:** [Claude Code](/docs/basics/claude-code.md), [Codex](/docs/basics/codex.md), [web search](/docs/new/studio/chat.md#advanced-web-search), [MCP](/docs/basics/mcp.md) and more
* **Train models:** Fine-tune other supported text, diffusion, [embedding](/docs/basics/embedding-finetuning.md), and more
* **Generate media:** Create and train [images](/docs/basics/diffusion-image.md), video, [TTS](/docs/basics/text-to-speech-tts-fine-tuning.md) locally

<div align="center"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FYShiiub5gs5pCQLX6d4U%2FScreenshot%202026-08-15%20at%2012.18.24%E2%80%AFAM.png?alt=media&amp;token=d6996797-a144-4113-b4c3-155cca6c39a0" alt="Unsloth Desktop Agents settings interface example" width="563"><figcaption><p>Unsloth Desktop’s Agents settings (interface example). Select DeepSeek-V4.1-Flash-1017 and your downloaded quant when connecting a tool.</p></figcaption></figure></div>
{% endstep %}
{% endstepper %}

### 🦙 Run DeepSeek-V4.1-Flash in llama.cpp

{% stepper %}
{% step %}
We need to use our specific llama.cpp PR [here](https://github.com/ggml-org/llama.cpp/pull/30817). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev git -y
git clone https://github.com/ggml-org/llama.cpp
git -C llama.cpp fetch origin pull/30817/head:deepseek41
git -C llama.cpp checkout deepseek41
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endstep %}

{% step %}
To run the model, you can do:

```bash
pip install -U "huggingface_hub[cli]"
hf download unsloth/DeepSeek-V4.1-Flash-1017-GGUF \
    --local-dir unsloth/DeepSeek-V4.1-Flash-1017-GGUF \
    --include "*UD-Q2_K_XL*"
```

Keep all seven shards in the same folder and point `--model` at the first shard. llama.cpp loads the remaining shards automatically.
{% endstep %}

{% step %}
Then to run it:

```bash
./llama.cpp/llama-cli \
    --model unsloth/DeepSeek-V4.1-Flash-1017-GGUF/UD-Q2_K_XL/DeepSeek-V4.1-Flash-1017-UD-Q2_K_XL-00001-of-00007.gguf \
    --temp 1.0 \
    --top-p 1.0 \
    --top-k 0 \
    --min-p 0.0 \
    --chat-template-kwargs '{"reasoning_effort":75}' \
    --load-mode mmap \
    --lazy-mode on \
    --override-tensor "per_layer_token_embd.weight=CPU"
```

This example loads the Engram n-gram table from SSD on demand. Keep `--load-mode mmap` and `--lazy-mode on` enabled for SSD offloading.
{% endstep %}
{% endstepper %}

### ⚡**DSpark** - Speculative Decoding

DeepSeek-V4.1 includes **DSpark**, a speculative decoding architecture that proposes multiple tokens before the main model verifies them. It is separate from the Engram n-gram lookup table: **Engram supplies learned memory; DSpark accelerates decoding**. The similarly named n-gram speculative decoding option is also a different feature.

For DSpark, pair the main model with a matching **V4.1-1017 drafter** and a runtime with DSpark support. Keep the drafter and main checkpoint versions matched, and reserve extra memory for the drafter. The CLI and server examples in this guide use ordinary decoding.

**DSpark enables inference for DeepSeek-V4.1-Flash-GGUF to be around 1.3 to 1.5x faster for decoding!**

We provide a Q8\_0 DSpark module at 8GB, and a full BF16 at 8.5GB.

### :checkered\_flag:Mix n matching the engram

You can also change the engram precision for DeepSeek-V4.1 to whatever you desire.

| Engram Precision | Size (GB) |
| ---------------- | --------- |
| MXFP8 (original) | 202.8 GB  |
| Q6\_K            | 161.3 GB  |
| Q5\_K            | 135.2 GB  |
| IQ4\_NL          | 110.6 GB  |

For example after downloading the dynamic 1-bit quant IQ1\_S which uses by default the IQ4\_NL engram, you can switch it out for the MXFP8 one by only downloading the MXFP8 engram at <https://huggingface.co/unsloth/DeepSeek-V4.1-Flash-1017-GGUF/tree/main/engram> called `DeepSeek-V4.1-Flash-1017-engram-MXFP8.gguf_file` To do this, follow the script below:

```bash
# 1. get the table + the script
hf download unsloth/DeepSeek-V4.1-Flash-1017-GGUF \
  --include "engram/*MXFP8*" "engram/set_split.py" --local-dir .

# 2. stamp it as shard 5 of 5 (UD-IQ1_S's table slot)
python engram/set_split.py engram/DeepSeek-V4.1-Flash-1017-engram-MXFP8.gguf_file 5 5

# 3. keep the old table aside, then rename the new one to the table shard's name
mv UD-IQ1_S/DeepSeek-V4.1-Flash-1017-UD-IQ1_S-00005-of-00005.gguf UD-IQ1_S/engram-IQ4_NL.bak
mv engram/DeepSeek-V4.1-Flash-1017-engram-MXFP8.gguf_file \
   UD-IQ1_S/DeepSeek-V4.1-Flash-1017-UD-IQ1_S-00005-of-00005.gguf

# 4. run as usual
llama-server -m UD-IQ1_S/DeepSeek-V4.1-Flash-1017-UD-IQ1_S-00001-of-00005.gguf
```

## 📊 Benchmarks

### **GGUF KLD and Top-1% Benchmarks**

Our quants span 82.8–98.5% top-1 agreement against the official F32 reference on wiki1100 and 85.1–98.7% on long17k. UD-Q4\_K\_XL saves 7.7 GB compared with UD-Q8\_K\_XL, with an agreement gap of 0.3 percentage points on wiki1100 and 0.2 on long17k. Q8 also has lower KL divergence on both sets.

**We also alter the engram table precision from IQ4\_NL to Q5\_K, Q6\_K and MXFP8, and show how KLD gets affected**

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FdIFvyiUQafZ2upn6VdhJ%2Fsize_vs_kld(1).png?alt=media&amp;token=e5d14eab-9143-4d0a-b1a6-f5427d995808" alt=""><figcaption></figcaption></figure>

### **Official Benchmarks**

DeepSeek reports the following results for **V4.1-Flash-1017** compared with the previous V4.1-Flash release. These are official model results, not measurements of the GGUFs in this guide. Source: [DeepSeek’s 1017 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017).

| Benchmark                   | V4.1-Flash-1017 | V4.1-Flash   |
| --------------------------- | --------------- | ------------ |
| HLE without tools           | 42.6 (44.0†)    | 36.8 (39.1†) |
| Terminal-Bench 4.0          | 42.3            | 31.2         |
| DeepSWE v1.1                | 77.0            | 74.2         |
| ProgramBench                | 29.1            | 20.3         |
| NL2Repo-Bench               | 68.2            | 65.4         |
| Automation-Bench v1.0.6     | 60.5            | 54.8         |
| Agents’ Last Exam           | 35.4            | 31.8         |
| Apex Bench v1.1             | 72.1            | 64.6         |
| Chartography (with tools)   | 83.0            | 78.9         |
| BabyVision (with tools)     | 92.5            | 89.6         |
| ZeroBench-main (with tools) | 51.0            | 49.0         |

† Text-only subset of HLE. DeepSeek uses the Claude Code harness for Terminal-Bench 4.0 and Mini-SWE-V2 for DeepSWE v1.1. Scores depend on the evaluation setup, reasoning effort and context budget.

### GGUF Benchmark Breakdown

#### Graders

See [Dynamic 3.1 GGUFs](/docs/basics/dynamic-3.0-ggufs/dynamic-3.1-ggufs.md#graders-used-for-benchmarks)

#### Infrastructure and benchmark issues and fixes

See [Dynamic 3.1 GGUFs](/docs/basics/dynamic-3.0-ggufs/dynamic-3.1-ggufs.md#infrastructure-and-benchmark-issues-and-fixes)

#### DeepSWE setup for benchmarks

See [Dynamic 3.1 GGUFs](/docs/basics/dynamic-3.0-ggufs/dynamic-3.1-ggufs.md#deepswe-setup-for-benchmarks)

#### Terminal Bench setup for benchmarks

See [Dynamic 3.1 GGUFs](/docs/basics/dynamic-3.0-ggufs/dynamic-3.1-ggufs.md#terminal-bench-setup-for-benchmarks)

#### Excluded Terminal Bench tasks due to issues

See [Dynamic 3.1 GGUFs](/docs/basics/dynamic-3.0-ggufs/dynamic-3.1-ggufs.md#excluded-terminal-bench-tasks-due-to-issues)

### Benchmark runs per model

We ran multiple runs to be fair - Terminal bench, DeepSWE 3x per quant. AIME 2025 64x per quant. LiveCodeBench 12x per quant and more. Some trials had to be re-run to fix infrastructure related issues (timeouts, CPU overload etc) - otherwise it'll be a fail - these only account for a few questions overall.

| Benchmark               |    UD IQ1\_S |    UD IQ1\_M |  UD IQ2\_XXS | UD Q2\_K\_XL |     Baseline |   GSQ IQ1\_M | GSQ IQ2\_XXS |  GSQ IQ2\_XS |
| ----------------------- | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: |
| Terminal Bench 2.1      |    242 (3/q) |    242 (3/q) |    242 (3/q) |    242 (3/q) |    324 (4/q) |    242 (3/q) |    245 (3/q) |    244 (3/q) |
| DeepSWE v1.1            |    338 (3/q) |    339 (3/q) |    338 (3/q) |    336 (3/q) |    451 (4/q) |    337 (3/q) |    338 (3/q) |    339 (3/q) |
| GPQA-Diamond            | 6,336 (32/q) | 6,336 (32/q) | 6,336 (32/q) | 6,336 (32/q) | 6,336 (32/q) | 6,336 (32/q) | 6,336 (32/q) | 6,336 (32/q) |
| MMLU-Pro                |  2,406 (2/q) |  2,406 (2/q) |  2,406 (2/q) |  2,406 (2/q) |  2,406 (2/q) |  2,406 (2/q) |  2,406 (2/q) |  2,406 (2/q) |
| AIME 2025               | 1,920 (64/q) | 1,920 (64/q) | 1,920 (64/q) | 1,920 (64/q) | 1,920 (64/q) | 1,920 (64/q) | 1,920 (64/q) | 1,920 (64/q) |
| IFEval                  |  1,082 (2/q) |  1,082 (2/q) |  1,082 (2/q) |  1,082 (2/q) |  1,082 (2/q) |  1,082 (2/q) |  1,082 (2/q) |  1,082 (2/q) |
| MATH-500 Level 5        | 2,144 (16/q) | 2,144 (16/q) | 2,144 (16/q) | 2,144 (16/q) | 2,144 (16/q) | 2,144 (16/q) | 2,144 (16/q) | 2,144 (16/q) |
| SciCode                 |    195 (3/q) |    195 (3/q) |    195 (3/q) |    195 (3/q) |    195 (3/q) |    195 (3/q) |    195 (3/q) |    195 (3/q) |
| HLE (text-only)         |    728 (1/q) |    728 (1/q) |    728 (1/q) |    728 (1/q) |    728 (1/q) |    728 (1/q) |    728 (1/q) |    728 (1/q) |
| LiveCodeBench v6        | 2,100 (12/q) | 2,100 (12/q) | 2,100 (12/q) | 2,100 (12/q) | 2,100 (12/q) | 2,100 (12/q) | 2,100 (12/q) | 2,100 (12/q) |
| Automation Bench v1.0.6 |    600 (1/q) |    600 (1/q) |    600 (1/q) |    600 (1/q) |    600 (1/q) |    600 (1/q) |    600 (1/q) |    600 (1/q) |
| HMMT Feb 2025           |   960 (32/q) |   960 (32/q) |   960 (32/q) |   960 (32/q) |   960 (32/q) |   960 (32/q) |   960 (32/q) |   960 (32/q) |
| HMMT Feb 2026           | 2,112 (64/q) | 2,112 (64/q) | 2,112 (64/q) | 2,112 (64/q) | 2,112 (64/q) | 2,112 (64/q) | 2,112 (64/q) | 2,112 (64/q) |
| Aider Polyglot          |    225 (1/q) |    225 (1/q) |    225 (1/q) |    225 (1/q) |    225 (1/q) |    225 (1/q) |    225 (1/q) |    225 (1/q) |
| **Total**               |   **21,387** |   **21,386** |   **21,389** |   **21,386** |   **21,583** |   **21,387** |   **21,391** |   **21,391** |


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/deepseek-v4.1-flash.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
