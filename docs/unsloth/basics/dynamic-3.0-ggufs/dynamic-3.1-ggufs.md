> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/dynamic-3.0-ggufs/dynamic-3.1-ggufs.md).

# Dynamic 3.1 GGUFs

A preview of our new methods to make quants smaller and maximize agentic performance

### DeepSeek-V4.1-Flash-1017

We're releasing new DeepSeek-V4.1-Flash-1017 GGUFs which using our new [**Unsloth Dynamic**](/docs/basics/dynamic-3.0-ggufs.md) **V3.1 (preview) algorithm** which improves Unsloth quants on nearly all benchmarks and is the best in class vs other providers. See [DeepSeek-V4.1-Flash](/docs/models/deepseek-v4.1-flash.md) for more details.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fe3HYFau6qEpkFwkLVwru%2FCoder%20benchmark.png?alt=media&amp;token=59e2ab09-3f42-4226-bd03-3b5a8d109e6a" alt=""><figcaption></figcaption></figure>

### Qwen3.8-Flash-Next

We also provided new quants for Qwen3.8-Flash-Next as well, and show our quants do the best across the board:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FqdXHweLFGzUhUcqj7jZX%2Ffinal%20key%204.png?alt=media&amp;token=8e3249b1-e26c-4a04-82ba-7cfdef952fe6" alt=""><figcaption></figcaption></figure>

### Graders used for Benchmarks

<table><thead><tr><th width="269.95001220703125">Benchmark</th><th width="172.35003662109375">What is graded</th><th>Grader</th></tr></thead><tbody><tr><td>DeepSWE v1.1</td><td>final repo patch</td><td>task's fail-to-pass + pass-to-pass tests in its container; pass = all pass (validated: gold patch 113/113 pass, empty patch 0/113)</td></tr><tr><td>Terminal-Bench 2.1</td><td>container state when the agent stops</td><td>each task's own verifier tests (harbor); infra failures rerun, not scored</td></tr><tr><td>AutomationBench v1.0.6</td><td>app state after the episode</td><td>each task's own checks; aborted episodes excluded and rerun</td></tr><tr><td>Aider Polyglot</td><td>edited files</td><td>exercise unit tests, pass@2 (one retry after seeing the failing test output)</td></tr><tr><td>LiveCodeBench v6</td><td>code between the last two ``` fences (official LCB extraction)</td><td>official LCB <code>run_test</code> on the hidden tests; sandbox with per-test timeouts, 8 GB memory cap, no network, scrubbed env</td></tr><tr><td>AIME 2025, HMMT Feb 2025 / 2026, MATH-500 L5</td><td>last <code>\boxed{}</code></td><td><code>math_verify</code> (HF leaderboard verifier), then exact-form normalisation (fix 4), then integer / normalised string match</td></tr><tr><td>SciCode</td><td>function per sub-step</td><td>official test cases (inspect_ai), no background; main problem = all sub-steps pass (reference solutions validated)</td></tr><tr><td>HLE text-only</td><td>final answer</td><td>LLM judge, official HLE judge prompt, gpt-6-luna xhigh</td></tr><tr><td>GPQA-Diamond</td><td>letter A-D</td><td>last <code>Answer: X</code>, then boxed letter, then "answer is X", then a bare final line</td></tr><tr><td>MMLU-Pro</td><td>letter A-J</td><td>same chain over the item's option letters</td></tr><tr><td>IFEval</td><td>response</td><td>Google <code>instruction_following_eval</code>, prompt-level strict (loose stored too)</td></tr></tbody></table>

### Infrastructure and benchmark issues and fixes

1. LiveCodeBench: Many runs had a `Time Limit Exceeded` issue, and we found CPUs were too heavily utilized on our machines - we regraded with full CPU affinity, flipping 385 answers from wrong to right
2. LiveCodeBench: Official harness's `stdin.buffer` mock returned the first line on every readline and captured stdout had no `.buffer` . We fixed it with faithful stdin / stdout replacements. 468 answers flipped from wrong to right.
3. AIME / HMMT / MATH-500: `math_verify` timeouts use `signal.alarm`, which fails off the main thread; the threaded grader fell back to exact string match (`\frac14` vs `\frac{1}{4}` wrong). We fixed it with no timeouts off the main thread. 8,520 answers flipped from wrong to right (HMMT26 4,196, MATH-500 2,949, HMMT25 1,375)
4. MATH-500 / HMMT: exact forms math\_verify cannot parse (matrix spacing, `\displaystyle`, trailing punctuation, thousands separators, `a = b` chains, inequality vs interval, column vector vs tuple). We fixed it with exact rewrites only, never approximations; 18 fixture tests. This flipped 309 (MATH-500 198, HMMT25 89, HMMT26 22) answers from wrong to right.

### DeepSWE setup for benchmarks

<table><thead><tr><th width="199.79998779296875"></th><th width="245.699951171875">Official (Pier + mini-swe-agent, task.toml)</th><th>Ours</th></tr></thead><tbody><tr><td>Agent / config</td><td>mini-swe-agent, Pier's default <code>mini.yaml</code> (native bash tool calls)</td><td>same agent and config; runs on the host and drives the task container via <code>docker exec</code> (Pier installs it inside)</td></tr><tr><td>Step limit</td><td>none (<code>step_limit: 0</code>)</td><td>500 (longest run 334 steps, never reached)</td></tr><tr><td>Agent wall clock</td><td>10,800 s per task</td><td>86,400 s (longest run 3,509 s, so 10,800 s never binds)</td></tr><tr><td>Network / grading</td><td>agent offline; separate offline verifier (tests + grader.py)</td><td>same</td></tr><tr><td>Command timeout</td><td>30 s (mini default)</td><td>30 s</td></tr><tr><td>Sampling</td><td>not specified</td><td>temperature 1.0, top_p 0.95, 65,536 tokens per reply, 512K context, reasoning effort 50</td></tr><tr><td>Tasks / passes</td><td>113</td><td>113 x 3 passes minimum</td></tr></tbody></table>

### Terminal Bench setup for benchmarks

|                               | Official TB 2.1                          | DeepSeek V4.1 report (sec 5.3.4) | Ours                                                                           |
| ----------------------------- | ---------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------ |
| Agent                         | any (leaderboard mostly Terminus 2)      | mini-swe-agent                   | mini-swe-agent 2.4.6, native tool calls                                        |
| Step limit                    | none                                     | 500                              | 150 (Unsloth quants hit max 5% of trials at timeout vs GSQ 7%)                 |
| Agent wall clock              | per task, 600 to 12,000 s (median 900 s) | not stated                       | none (86,400 s)                                                                |
| Internet during the agent run | allowed                                  | none                             | none (setup and verifier keep internet)                                        |
| Tasks                         | 89                                       | 89                               | 82 (7 oracle-unsolvable on this host excluded)                                 |
| Sampling                      | n/a                                      | T 1.0, top\_p 0.95               | T 1.0, top\_p 0.95, 65,536 tokens per reply, 512K context, reasoning effort 50 |
| Attempts                      | 1+                                       | not stated                       | 3 per task. infra failures rerun                                               |

### Excluded Terminal Bench tasks due to issues

<table><thead><tr><th width="201.25">Excluded task</th><th>Why the reference solution fails here</th></tr></thead><tbody><tr><td>qemu-alpine-ssh</td><td>the verifier's <code>apt-get install curl</code> returns 404 (Debian bullseye security packages superseded), so its test tooling cannot install</td></tr><tr><td>qemu-startup</td><td>same 404</td></tr><tr><td>mcmc-sampling-stan</td><td>the reference needs RcppParallel, which needs cmake; the image has no cmake, so rstan cannot be installed</td></tr><tr><td>protein-assembly</td><td>the reference fails with dnachisel <code>NoSolutionError</code> (EnforceTranslation): dependency drift since the task was written</td></tr><tr><td>build-cython-ext</td><td>after the reference build, the upstream pyknotid test suite fails 1 of 18 tests</td></tr><tr><td>install-windows-3.11</td><td>the reference QEMU build is OOM-killed (the build runs one job per host core, 192, in a 4 GB container)</td></tr><tr><td>torch-pipeline-parallelism</td><td>the verifier exceeds its own 900 s timeout (both runs)</td></tr></tbody></table>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/dynamic-3.0-ggufs/dynamic-3.1-ggufs.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
