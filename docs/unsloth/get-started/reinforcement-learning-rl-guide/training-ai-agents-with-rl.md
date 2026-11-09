> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/training-ai-agents-with-rl.md).

# Training AI Agents with RL

Learn how to train AI agents for real-world tasks using Reinforcement Learning (RL).

“Agentic” AI is becoming more popular over time. In this context, an “agent” is an LLM that is given a high-level goal and a set of tools to achieve it. Agents are also typically “multi-turn” — they can perform an action, see what effect it had on the environment, and then perform another action repeatedly, until they achieve their goal or fail trying.

Unfortunately, even very capable LLMs can have a hard time performing complex multi-turn agentic tasks reliably. Interestingly, we’ve found that training agents using an RL algorithm called [GRPO (Group Relative Policy Optimization)](/docs/get-started/reinforcement-learning-rl-guide/tutorial-train-your-own-reasoning-model-with-grpo.md) can make them far more reliable! In this guide, you will learn how to to build reliable AI agents using open-source tools.

## 🎨 Training RL Agents with ART

[ART (Agent Reinforcement Trainer)](https://github.com/openpipe/art) built on top of [Unsloth](https://github.com/unslothai/unsloth)’s GRPOTrainer, is a tool that makes training multi-turn agents possible and easy. If you’re already using Unsloth for GRPO and need to train agents that can handle complex, multi-turn interactions, ART simplifies the process.

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-c97e63a69ecd17685c6e09cb41fd625d43a3545d%2FScreenshot_2025-07-19_at_1.23.18_PM.webp?alt=media" alt="" width="375"><figcaption><p>Agent models trained with Unsloth+ART are often able to outperform prompted models on agentic workflows.</p></figcaption></figure></div>

### ART + Unsloth

ART builds on top of Unsloth’s memory- and compute-efficient GRPO implementation. In addition, it adds the following capabilities:

#### 1. Multi-Turn Agent Training

ART introduces the concept of a “trajectory”, which is built up as your agent executes. These trajectories can then be scored and used for GRPO. Trajectories can be complex, and even include non-linear histories, sub-agent calls, etc. They also support tool calls and responses.

#### 2. Flexible Integration into Existing Codebases

If you already have an agent working with a prompted model, ART tries to minimize the number of changes you need to make to wrap your existing agent loop and use it for training.

Architecturally, ART is split into a “frontend” client that lives in your codebase and communicates via API with a “backend” where the actual training happens (these can also be colocated on a single machine if you prefer using ART’s `LocalBackend`). This gives some key benefits:

* **Minimal setup required**: The ART frontend is has minimal dependencies and can be easily added to existing Python codebases.
* **Train from anywhere**: You can run the ART client on your laptop and let the ART server kick off an ephemeral GPU-enabled environment, or run on a local GPU
* **OpenAI-compatible API**: The ART backend serves your model undergoing training via an OpenAI-compatible API, which is compatible with most existing codebases.

#### 3. RULER: Zero-Shot Agent Rewards

ART also provides a built-in general-purpose reward function called [RULER](https://art.openpipe.ai/fundamentals/ruler) (Relative Universal LLM-Elicited Rewards), which can eliminate the need for hand-crafted reward functions. Surprisingly, agents RL-trained with the RULER automatic reward function often match or surpass the performance of agents trained using hand-written reward functions. This makes getting started with RL easier.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-b4168c3c380f6c8258c31083dcb65a5fcd2308b8%2FScreenshot_2025-07-19_at_1.21.08_PM.webp?alt=media" alt="" width="375"><figcaption></figcaption></figure>

```python
# Before: Hours of reward engineering
def complex_reward_function(trajectory):
    # 50+ lines of careful scoring logic...
    pass

# After: One line with RULER
judged_group = await ruler_score_group(group, "openai/o3")
```

### When to Choose ART

ART might be a good fit for projects that need:

1. **Multi-step agent capabilities**: When your use case involves agents that need to take multiple actions, use tools, or have extended conversations
2. **Rapid prototyping without reward engineering**: RULER’s automatic reward scoring can cut your project’s development time by 2-3x
3. **Integration with existing systems**: When you need to add RL capabilities to an existing agentic codebase with minimal changes

### Code Example: ART in Action

```python
import art
from art.rewards import ruler_score_group

# Initialize model with Unsloth-supported basemodel
model = art.TrainableModel(
    name="agent-001",
    project="my-agentic-task",
    base_model="Qwen/Qwen2.5-14B-Instruct",  # Any Unsloth-supported model
)

# Define your rollout function
async def rollout(model: art.Model, scenario: Scenario) -> art.Trajectory:
    openai_client = model.openai_client()
    trajectory = art.Trajectory(
        messages_and_choices=[
            {"role": "system", "content": "..."},
            {"role": "user", "content": "..."}
        ]
    )
    # Your agent logic here...    
    return trajectory

# Train with RULER for automatic rewards
groups = await art.gather_trajectory_groups(
    (
        art.TrajectoryGroup(rollout(model, scenario) for _ in range(8))
        for scenario in scenarios
    ),
    after_each=lambda group: ruler_score_group(
        group,
        "openai/o3",
        swallow_exceptions=True
    )
)

await model.train(groups)
```

### Getting Started

To add ART to your Unsloth-based project:

```bash
pip install openpipe-art # or `uv add openpipe-art`
```

Then check out the [example notebooks](https://art.openpipe.ai/getting-started/notebooks) to see ART in action with tasks like:

* Email retrieval agents that beat o3
* Game-playing agents (2048, Tic Tac Toe, Codenames)
* Complex reasoning tasks (Temporal Clue)


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide/training-ai-agents-with-rl.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
