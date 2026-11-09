> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/devstral-2.md).

# Devstral 2 - How to Run Guide

Guide for local running Mistral Devstral 2 models: 123B-Instruct-2512 and Small-2-24B-Instruct-2512.

Devstral 2 are Mistral’s new coding and agentic LLMs for software engineering, available in [24B](#devstral-small-2-24b) and [123B](#devstral-2-123b) sizes. The 123B model achieves SOTA in SWE-bench, coding, tool-calling and agent use-cases. The 24B model fits in 25GB RAM/VRAM and 123B fits in 128GB.

{% hint style="success" %}
**13th December 2025 Update**

**We’ve resolved issues in Devstral’s chat template, and results should be significantly better. The 24B & 123B have been updated. Also install the latest llama.cpp as at 13th Dec 2025!**
{% endhint %}

Devstral 2 supports vision capabilities, a 256k context window and uses the same architecture as [Ministral 3](/docs/models/tutorials/ministral-3.md). You can now run and **fine-tune** both models locally with Unsloth.

All Devstral 2 uploads use our Unsloth [Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) methodology, delivering the best performance on [Aider Polyglot](/docs/basics/dynamic-3.0-ggufs/unsloth-dynamic-ggufs-on-aider-polyglot.md) and 5-shot MMLU benchmarks.

<a href="#devstral-small-2-24b" class="button primary">Devstral-Small-2-24B</a><a href="#devstral-2-123b" class="button primary">Devstral-2-123B</a>

#### **Devstral 2 - Unsloth Dynamic** GGUFs:

| Devstral-Small-2-24B-Instruct-2512                                                                                    | Devstral-2-123B-Instruct-2512                                                                               |
| --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [Devstral-Small-2-**24B**-Instruct-2512-GGUF](https://huggingface.co/unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF) | [Devstral-2-**123B**-Instruct-2512-GGUF](https://huggingface.co/unsloth/Devstral-2-123B-Instruct-2512-GGUF) |

## 🖥️ **Running Devstral 2**

See our step-by-step guides for running [Devstral 24B](#devstral-small-2-24b) and the large [Devstral 123B](#devstral-2-123b) models. Both models support vision support but currently **vision is not supported** in llama.cpp

### :gear: Usage Guide

Here are the recommended settings for inference:

* <mark style="background-color:blue;">**Temperature \~0.15**</mark>
* Min\_P of 0.01 (optional, but 0.01 works well, llama.cpp default is 0.1)
* **Use `--jinja` to enable the system prompt.**
* Max context length = 262,144
* Recommended minimum context: 16,384
* Install the latest llama.cpp since a [December 13th 2025 pull request](https://github.com/ggml-org/llama.cpp/pull/17945) fixes issues.

### :tophat:Devstral-Small-2-24B

The full precision (Q8) Devstral-Small-2-24B GGUF will fit in 25GB RAM/VRAM. Text only for now.

#### ✨ Run Devstral-Small-2-24B-Instruct-2512 in llama.cpp

1. Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

{% code overflow="wrap" %}

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endcode %}

2. If you want to use `llama.cpp` directly to load models, you can do the below: (:`Q4_K_XL`) is the quantization type. You can also directly pull from Hugging Face:

```bash
./llama.cpp/llama-cli \
    -hf unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL \
    --jinja -ngl 99 --ctx-size 16384 \
    --temp 0.15
```

3. Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD_Q4_K_XL` or other quantized versions.

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF",
    local_dir = "unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF",
    allow_patterns = ["*UD-Q4_K_XL*", "*mmproj-F16*"], # For Q4_K_XL
)
```

4. Run the model in conversation mode:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF/Devstral-Small-2-24B-Instruct-2512-UD-Q4_K_XL.gguf \
    --mmproj unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF/mmproj-F16.gguf \
    --ctx-size 16384 \
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.15 \
    --jinja
```

{% endcode %}

#### :eyes:Devstral and vision

1. To play with Devstral's image capabilities, let's first download a image like this [FP8 Reinforcement Learning with Unsloth](https://unsloth.ai/cgi/image/fp8grpolarge_KharloZxEEaHAY2X97CEX.png?width=3840\&quality=80\&format=auto) below:\
   ![](https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FVKuEX57zjziskMFnAuhY%2Fimage.png?alt=media\&token=83ef2463-888e-48f1-acf2-55b05a544b5f)
2. We get the image via `wget https://unsloth.ai/cgi/image/fp8grpolarge_KharloZxEEaHAY2X97CEX.png?width=3840%26quality=80%26format=auto -O unsloth_fp8.png` which will save the image as "unsloth\_fp8.png"
3. Then load the image in via `/image unsloth_fp8.png` after the model is loaded as seen below:\
   ![](https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F8BYfTecTXWUh1mqGwLYQ%2Fimage.png?alt=media\&token=d43ab46d-a075-402d-9a60-fba2c3d25869)
4. We then prompt it `Describe this image` and get the below:<br>

   <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQygUnKEB0sPfko5LH9ap%2Fimage.png?alt=media&amp;token=54a459e4-8f29-4e64-8fab-10e17156ad55" alt=""><figcaption></figcaption></figure>

### :truck:Devstral-2-123B

The full precision (Q8) Devstral-Small-2-123B GGUF will fit in 128GB RAM/VRAM. Text only for now.

#### :sparkles: Run Devstral-2-123B-Instruct-2512 Tutorial

1. Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference.

{% code overflow="wrap" %}

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endcode %}

2. You can directly pull from HuggingFace via:

```bash
./llama.cpp/llama-cli \
    -hf unsloth/Devstral-2-123B-Instruct-2512-GGUF:UD-Q2_K_XL \
    --jinja -ngl 99 --ctx-size 16384 \
    --temp 0.15
```

2. Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD_Q4_K_XL` or other quantized versions.

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Devstral-2-123B-Instruct-2512-GGUF",
    local_dir = "unsloth/Devstral-2-123B-Instruct-2512-GGUF",
    allow_patterns = ["*UD-Q2_K_XL*", "*mmproj-F16*"],
)
```

3. Run the model in conversation mode:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/Devstral-2-123B-Instruct-2512-GGUF/Devstral-2-123B-Instruct-2512-UD-Q2_K_XL.gguf \
    --mmproj unsloth/Devstral-2-123B-Instruct-2512-GGUF/mmproj-F16.gguf \
    --ctx-size 16384 \
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.15 \
    --jinja
```

{% endcode %}

## 🦥 Fine-tuning Devstral 2 with Unsloth

Just like [Ministral 3](/docs/models/tutorials/ministral-3.md), Unsloth supports Devstral 2 fine-tuning. Training is 2x faster, use 70% less VRAM and supports 8x longer context lengths. Devstral 2 fits comfortably in a 24GB VRAM L4 GPU.

Unfortunately, Devstral 2 slightly exceeds the memory limits of a 16GB VRAM, so fine-tuning it for free on Google Colab isn't possible for now. However, you *can* fine-tune the model for free using our [Kaggle notebook](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Magistral_\(24B\)-Reasoning-Conversational.ipynb\&accelerator=nvidiaTeslaT4), which offers access to dual GPUs. Just change the notebook's Magistral model name to the `unsloth/Devstral-Small-2-24B-Instruct-2512` model.

{% hint style="success" %}
We made free Unsloth notebooks to fine-tune Ministral 3, and directly supports Devstral 2, since they share the same architecture! Change the name to use the desired model.
{% endhint %}

* Ministral-3B-Instruct [Vision notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Ministral_3_VL_\(3B\)_Vision.ipynb) (vision) (Change model name to Devstral 2)
* Ministral-3B-Instruct [GRPO notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Ministral_3_\(3B\)_Reinforcement_Learning_Sudoku_Game.ipynb) (Change model name to Devstral 2)

{% columns %}
{% column %}
Devstral Vision finetuning notebook

{% embed url="<https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Ministral_3_VL_(3B)_Vision.ipynb>" %}
{% endcolumn %}

{% column %}
Devstral Sudoku GRPO RL notebook

{% embed url="<https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Ministral_3_(3B)_Reinforcement_Learning_Sudoku_Game.ipynb>" %}
{% endcolumn %}
{% endcolumns %}

### :sunglasses:Llama-server serving & deployment

To deploy Devstral 2 for production, we use `llama-server` In a new terminal say via tmux, deploy the model via:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-server \
    --model unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF/Devstral-Small-2-24B-Instruct-2512-UD-Q4_K_XL.gguf \
    --mmproj unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF/mmproj-F16.gguf \
    --alias "unsloth/Devstral-Small-2-24B-Instruct-2512" \
    --n-gpu-layers 999 \
    --prio 3 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --port 8001 \
    --jinja
```

{% endcode %}

When you run the above, you will get:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FJSTkWDCcHk5DI6otb72X%2Fimage.png?alt=media&amp;token=b685008e-e9ad-4dea-8f1d-af3fdade8e3b" alt=""><figcaption></figcaption></figure>

Then in a new terminal, after doing `pip install openai`, do:

{% code overflow="wrap" %}

```python
from openai import OpenAI
import json
openai_client = OpenAI(
    base_url = "http://127.0.0.1:8001/v1",
    api_key = "sk-no-key-required",
)
completion = openai_client.chat.completions.create(
    model = "unsloth/Devstral-Small-2-24B-Instruct-2512",
    messages = [{"role": "user", "content": "What is 2+2?"},],
)
print(completion.choices[0].message.content)
```

{% endcode %}

Which will simply print 4.

### :toolbox:Tool Calling with Devstral 2 Tutorial

After following [#llama-server-serving-and-deployment](#llama-server-serving-and-deployment "mention") we then can load up some tools and see Devstral in action! Let's make some tools - copy paste and execute them in Python.

{% code expandable="true" %}

```python
import json, subprocess, random
from typing import Any
def add_number(a: float | str, b: float | str) -> float:
    return float(a) + float(b)
def multiply_number(a: float | str, b: float | str) -> float:
    return float(a) * float(b)
def subtract_number(a: float | str, b: float | str) -> float:
    return float(a) - float(b)
def write_a_story() -> str:
    return random.choice([
        "A long time ago in a galaxy far far away...",
        "There were 2 friends who loved sloths and code...",
        "The world was ending because every sloth evolved to have superhuman intelligence...",
        "Unbeknownst to one friend, the other accidentally coded a program to evolve sloths...",
    ])
def terminal(command: str) -> str:
    if "rm" in command or "sudo" in command or "dd" in command or "chmod" in command:
        msg = "Cannot execute 'rm, sudo, dd, chmod' commands since they are dangerous"
        print(msg); return msg
    print(f"Executing terminal command `{command}`")
    try:
        return str(subprocess.run(command, capture_output = True, text = True, shell = True, check = True).stdout)
    except subprocess.CalledProcessError as e:
        return f"Command failed: {e.stderr}"
def python(code: str) -> str:
    data = {}
    exec(code, data)
    del data["__builtins__"]
    return str(data)
MAP_FN = {
    "add_number": add_number,
    "multiply_number": multiply_number,
    "subtract_number": subtract_number,
    "write_a_story": write_a_story,
    "terminal": terminal,
    "python": python,
}
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_number",
            "description": "Add two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "string",
                        "description": "The second number.",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multiply_number",
            "description": "Multiply two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "string",
                        "description": "The second number.",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "subtract_number",
            "description": "Subtract two numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "string",
                        "description": "The first number.",
                    },
                    "b": {
                        "type": "string",
                        "description": "The second number.",
                    },
                },
                "required": ["a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_a_story",
            "description": "Writes a random story.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "terminal",
            "description": "Perform operations from the terminal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command you wish to launch, e.g `ls`, `rm`, ...",
                    },
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "python",
            "description": "Call a Python interpreter with some Python code that will be ran.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The Python code to run",
                    },
                },
                "required": ["code"],
            },
        },
    },
]
```

{% endcode %}

We then ask a simple question from a random list of possible messages to test the model:

{% code overflow="wrap" %}

```python
import random
messages = [{
    "role": "user",
    "content": [random.choice([
        {"type": "text", "text": "Could you write me a story ?"},
        {"type": "text", "text": "What is today's date plus 3 days?"},
        {"type": "text", "text": "Get the current time in nanoseconds."},
        {"type": "text", "text": "Create a Fibonacci function in Python and find fib(20)."},
    ])],
}]
```

{% endcode %}

We then use the below functions (copy and paste and execute) which will parse the function calls automatically - Devstral 2 might make multiple in tandem!

```python
temperature = 0.15
from openai import OpenAI
openai_client = OpenAI(
    base_url = "http://127.0.0.1:8001/v1",
    api_key = "sk-no-key-required",
)
model_name = next(iter(openai_client.models.list())).id
print(f"Using model = {model_name}")
has_tool_calls = True
original_messages_len = len(messages)
while has_tool_calls:
    print(f"Current messages = {messages}")
    response = openai_client.chat.completions.create(
        model = model_name,
        messages = messages,
        temperature = temperature,
        tools = tools if tools else None,
        tool_choice = "auto" if tools else None,
    )
    tool_calls = response.choices[0].message.tool_calls or []
    content = response.choices[0].message.content or ""
    tool_calls_dict = [tc.to_dict() for tc in tool_calls] if tool_calls else tool_calls
    messages.append({"role": "assistant", "tool_calls": tool_calls_dict, "content": content,})
    for tool_call in tool_calls:
        fx, args, _id = tool_call.function.name, tool_call.function.arguments, tool_call.id
        out = MAP_FN[fx](**json.loads(args))
        messages.append({"role": "tool", "tool_call_id": _id, "name": fx, "content": str(out),})
    else:
        has_tool_calls = False
print(json.dumps(messages[original_messages_len:], indent = 2))
```

And after 1 minute, we get:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F3XsKXoOUJ1PAyrLfjZxH%2Fimage.png?alt=media&amp;token=ec1e125d-1326-4804-942f-2f41998099b6" alt=""><figcaption></figcaption></figure>

Or in JSON form:

```json
[
  {
    "role": "assistant",
    "tool_calls": [
      {
        "id": "JviLK0wUveWguuKQHgZdFdYI2adu85jy",
        "function": {
          "arguments": "{}",
          "name": "write_a_story"
        },
        "type": "function"
      }
    ],
    "content": null
  },
  {
    "role": "tool",
    "tool_call_id": "JviLK0wUveWguuKQHgZdFdYI2adu85jy",
    "name": "write_a_story",
    "content": "A long time ago in a galaxy far far away..."
  },
  {
    "role": "assistant",
    "tool_calls": null,
    "content": "In a distant galaxy, where the stars burned with an otherworldly glow, there was a planet named Eldoria. Eldoria was a world of stark contrasts\u2014vibrant cities nestled between towering mountains and vast deserts that stretched endlessly under twin suns. The people of Eldoria were known far and wide for their mastery of energy, particularly their legendary laser sabers.\n\nThese sabers were not mere weapons; they were extensions of their wielders' souls, forged from rare crystals that pulsed with the essence of the cosmos. Each saber was unique, its color and power reflecting the personality and spirit of its owner. The most skilled warriors, known as the Saberborn, could wield their sabers with such precision and grace that they seemed to dance with the very fabric of reality.\n\nAmong the Saberborn, there was a warrior named Kael. Kael was an outcast, a former guardian of the sacred Saber Temples who had been exiled for defying the council's orders. The council had sought to hoard the power of the laser sabers, using them to control the people of Eldoria. Kael believed that the sabers should be wielded by those who sought to protect, not dominate.\n\nOne day, Kael received a distress signal from a small village on the outskirts of the desert. The village was under attack by a rogue faction of Saberborn, led by a ruthless warlord named Vexis. Vexis sought to claim the village's ancient relic\u2014a crystal said to amplify the power of any laser saber tenfold. If Vexis succeeded, his army would become unstoppable, and Eldoria would fall into darkness.\n\nKael knew he had to act. He strapped on his saber\u2014a deep blue blade that hummed with the energy of the cosmos\u2014and set off across the desert. The journey was treacherous, with sandstorms and hidden traps set by Vexis's scouts. But Kael pressed on, driven by the memory of the people he had once sworn to protect.\n\nWhen he reached the village, the battle was already in full swing. Vexis's warriors wielded their sabers with brutal efficiency, cutting down defenders with ease. Kael leapt into the fray, his blue saber a blur of light as he disarmed and defeated one enemy after another. The villagers, seeing their savior arrive, rallied behind him, their own sabers flashing as they fought to reclaim their home.\n\nKael faced Vexis in the center of the village square. The warlord's saber was a sickly green, pulsing with dark energy. \"You are too late, Kael,\" Vexis sneered. \"The relic is mine, and with it, I will rule Eldoria.\" Kael stood his ground, his saber raised. \"Over my dead body,\" he replied.\n\nThe two warriors clashed, their sabers locking in a shower of sparks. Kael felt the raw power of the relic coursing through Vexis's blade, but he refused to back down. He channeled his own energy, his saber glowing brighter as he pushed back against Vexis's assault. With a final, desperate strike, Kael disarmed Vexis, sending his saber clattering to the ground.\n\nVexis snarled in defeat, but Kael did not kill him. Instead, he offered him a choice: \"Join me in protecting Eldoria, or leave and never return.\" Vexis, humbled and seeing the truth in Kael's words, chose to stand with him.\n\nWith Vexis's faction now allies, Kael and the villagers reclaimed the relic, using its power to restore balance to Eldoria. The Saber Temples were reformed, and the laser sabers were once again wielded by those who sought to protect, not control.\n\nKael's legend grew, and he became a symbol of hope for the people of Eldoria. His story reminded them that even in the darkest times, the light of courage and justice could prevail. And so, the Saberborn lived on, their laser sabers a beacon of strength and unity in a galaxy full of shadows."
  }
]
```


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/devstral-2.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
