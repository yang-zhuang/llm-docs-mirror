> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/advanced-rl-documentation/rl-reward-hacking.md).

# RL Reward Hacking

Learn what is Reward Hacking in Reinforcement Learning and how to counter it.

The ultimate goal of RL is to maximize some reward (say speed, revenue, some metric). But RL can **cheat.** When the RL algorithm learns a trick or exploits something to increase the reward, without actually doing the task at end, this is called "**Reward Hacking**".

It's the reason models learn to modify unit tests to pass coding challenges, and these are critical blockers for real world deployment. Some other good examples are from [Wikipedia](https://en.wikipedia.org/wiki/Reward_hacking).

<div align="center"><figure><img src="https://i.pinimg.com/originals/55/e0/1b/55e01b94a9c5546b61b59ae300811c83.gif" alt="" width="188"><figcaption></figcaption></figure></div>

**Can you counter reward hacking? Yes!** In our [free gpt-oss RL notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/gpt-oss-\(20B\)-GRPO.ipynb) we explore how to counter reward hacking in a code generation setting and showcase tangible solutions to common error modes. We saw the model edit the timing function, outsource to other libraries, cache the results, and outright cheat. After countering, the result is our model generates genuinely optimized matrix multiplication kernels, not clever cheats.

## :trophy: Reward Hacking Overview

Some common examples of reward hacking during RL include:

#### Laziness

RL learns to use Numpy, Torch, other libraries, which calls optimized CUDA kernels. We can stop the RL algorithm from calling optimized code by inspecting if the generated code imports other non standard Python libraries.

#### Caching & Cheating

RL learns to cache the result of the output and RL learns to find the actual output by inspecting Python global variables.

We can stop the RL algorithm from using cached data by wiping the cache with a large fake matrix. We also have to benchmark carefully with multiple loops and turns.

#### Cheating

RL learns to edit the timing function to make it output 0 time as passed. We can stop the RL algorithm from using global or cached variables by restricting it's `locals` and `globals`. We are also going to use `exec` to create the function, so we have to save the output to an empty dict. We also disallow global variable access via `types.FunctionType(f.__code__, {})`\\


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/advanced-rl-documentation/rl-reward-hacking.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
