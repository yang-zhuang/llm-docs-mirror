> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/glm-4.7.md).

# GLM-4.7: How to Run Locally Guide

A guide on how to run Z.ai GLM-4.7 model on your own local device!

GLM-4.7 is Z.ai’s latest thinking model, delivering stronger coding, agent, and chat performance than [GLM-4.6](/docs/models/tutorials/glm-4.6-how-to-run-locally.md). It achieves SOTA performance on on SWE-bench (73.8%, +5.8), SWE-bench Multilingual (66.7%, +12.9), and Terminal Bench 2.0 (41.0%, +16.5).

The full 355B parameter model requires **400GB** of disk space, while the Unsloth Dynamic 2-bit GGUF reduces the size to **134GB** (-**75%)**. [**GLM-4.7-GGUF**](https://huggingface.co/unsloth/GLM-4.7-GGUF)

All uploads use Unsloth [Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) for SOTA 5-shot MMLU and Aider performance, meaning you can run & fine-tune quantized GLM LLMs with minimal accuracy loss.

### :gear: Usage Guide

The 2-bit dynamic quant UD-Q2\_K\_XL uses 135GB of disk space - this works well in a **1x24GB card and 128GB of RAM** with MoE offloading. The 1-bit UD-TQ1 GGUF also **works natively in Ollama**!

{% hint style="info" %}
You must use `--jinja` for llama.cpp quants - this uses our [fixed chat templates](#chat-template-bug-fixes) and enables the correct template! You might get incorrect results if you do not use `--jinja`
{% endhint %}

The 4-bit quants will fit in a 1x 40GB GPU (with MoE layers offloaded to RAM). Expect around 5 tokens/s with this setup if you have bonus 165GB RAM as well. It is recommended to have at least 205GB RAM to run this 4-bit. For optimal performance you will need at least 205GB unified memory or 205GB combined RAM+VRAM for 5+ tokens/s. To learn how to increase generation speed and fit longer contexts, [read here](#improving-generation-speed).

{% hint style="success" %}
Though not a must, for best performance, have your VRAM + RAM combined equal to the size of the quant you're downloading. If not, hard drive / SSD offloading will work with llama.cpp, just inference will be slower. Also use `--fit on` in `llama.cpp` to auto enable maximum GPU usage!
{% endhint %}

### Recommended Settings

Use distinct settings for different use cases. Recommended settings for default and multi-turn agentic use cases:

| Default Settings (Most Tasks)                                      | Terminal Bench, SWE Bench Verified                                 |
| ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| <mark style="background-color:green;">**temperature = 1.0**</mark> | <mark style="background-color:green;">**temperature = 0.7**</mark> |
| <mark style="background-color:green;">**top\_p = 0.95**</mark>     | <mark style="background-color:green;">**top\_p = 1.0**</mark>      |
| `131072` **max new tokens**                                        | `16384` **max new tokens**                                         |

* Use `--jinja` for llama.cpp variants - we **fixed some chat template issues as well!**
* **Maximum context window:** `131,072`

## Run GLM-4.7 Tutorials:

See our step-by-step guides for running GLM-4.7 in [Ollama](#run-in-ollama) and [llama.cpp](#run-in-llama.cpp).

### ✨ Run in llama.cpp

{% stepper %}
{% step %}
Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endstep %}

{% step %}
If you want to use `llama.cpp` directly to load models, you can do the below: (:Q2\_K\_XL) is the quantization type. You can also download via Hugging Face (point 3). This is similar to `ollama run` . Use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location. Remember the model has only a maximum of 128K context length.

```bash
export LLAMA_CACHE="unsloth/GLM-4.7-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/GLM-4.7-GGUF:UD-Q2_K_XL \
    --jinja \
    --ctx-size 16384 \
    --flash-attn on \
    --temp 1.0 \
    --top-p 0.95 \
    --fit on
```

{% hint style="info" %}
**Use `--fit on` introduced 15th Dec 2025 for maximum usage of your GPU and CPU.**

Optionally, try `-ot ".ffn_.*_exps.=CPU"` to offload all MoE layers to the CPU! This effectively allows you to fit all non MoE layers on 1 GPU, improving generation speeds. You can customize the regex expression to fit more layers if you have more GPU capacity.

If you have a bit more GPU memory, try `-ot ".ffn_(up|down)_exps.=CPU"` This offloads up and down projection MoE layers.

Try `-ot ".ffn_(up)_exps.=CPU"` if you have even more GPU memory. This offloads only up projection MoE layers.

And finally offload all layers via `-ot ".ffn_.*_exps.=CPU"` This uses the least VRAM.

You can also customize the regex, for example `-ot "\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU"` means to offload gate, up and down MoE layers but only from the 6th layer onwards.
{% endhint %}
{% endstep %}

{% step %}
Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD-`Q2\_K\_XL (dynamic 2bit quant) or other quantized versions like `Q4_K_XL` . We <mark style="background-color:green;">**recommend using our 2.7bit dynamic quant**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**`UD-Q2_K_XL`**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**to balance size and accuracy**</mark>.

```bash
pip install -U huggingface_hub
hf download unsloth/GLM-4.7-GGUF \
    --local-dir unsloth/GLM-4.7-GGUF \
    --include "*UD-Q2_K_XL*" # Use "*UD-TQ1_0*" for Dynamic 1bit
```

{% endstep %}

{% step %}
You can edit `--threads 32` for the number of CPU threads, `--ctx-size 16384` for context length, `--n-gpu-layers 2` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/GLM-4.7-GGUF/UD-Q2_K_XL/GLM-4.7-UD-Q2_K_XL-00001-of-00003.gguf \
    --jinja \
    --temp 1.0 \
    --top-p 0.95 \
    --ctx-size 16384 \
    --seed 3407 \
    --fit on
```

{% endcode %}
{% endstep %}
{% endstepper %}

### :llama: Run in Ollama

{% stepper %}
{% step %}
Install `ollama` if you haven't already! To run more variants of the model, [see here](https://unsloth.ai/docs/models/tutorials/pages/eK0BfjMHNrfvfe4HI6Pk#run-in-llama.cpp).

```bash
apt-get update
apt-get install pciutils -y
curl -fsSL https://ollama.com/install.sh | sh
```

{% endstep %}

{% step %}
Run the model! Note you can call `ollama serve`in another terminal if it fails! We include all our fixes and suggested parameters (temperature etc) in `params` in our Hugging Face upload!

```bash
OLLAMA_MODELS=unsloth ollama serve &

OLLAMA_MODELS=unsloth ollama run hf.co/unsloth/GLM-4.7-GGUF:TQ1_0
```

{% endstep %}

{% step %}
To run other quants, you need to first merge the GGUF split files into 1 like the code below. Then you will need to run the model locally.

```bash
./llama.cpp/llama-gguf-split --merge \
  GLM-4.7-GGUF/GLM-4.7-UD-Q2_K_XL/GLM-4.7-UD-Q2_K_XL-00001-of-00003.gguf \
	merged_file.gguf
```

```bash
OLLAMA_MODELS=unsloth ollama serve &

OLLAMA_MODELS=unsloth ollama run merged_file.gguf
```

{% endstep %}
{% endstepper %}

### ✨ Deploy with llama-server and OpenAI's completion library

To use llama-server for deployment, use the following command:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-server \
    --model unsloth/GLM-4.7-GGUF/UD-Q2_K_XL/GLM-4.7-UD-Q2_K_XL-00001-of-00003.gguf \
    --alias "unsloth/GLM-4.7" \
    --fit on \
    --prio 3 \
    --temp 1.0 \
    --top-p 0.95 \
    --ctx-size 16384 \
    --port 8001 \
    --jinja
```

{% endcode %}

Then use OpenAI's Python library after `pip install openai` :

```python
from openai import OpenAI
import json
openai_client = OpenAI(
    base_url = "http://127.0.0.1:8001/v1",
    api_key = "sk-no-key-required",
)
completion = openai_client.chat.completions.create(
    model = "unsloth/GLM-4.7",
    messages = [{"role": "user", "content": "What is 2+2?"},],
)
print(completion.choices[0].message.content)
```

### :hammer:Tool Calling with GLM 4.7

See [Tool Calling Guide](/docs/basics/tool-calling-guide-for-local-llms.md) for more details on how to do tool calling. In a new terminal (if using tmux, use CTRL+B+D), we create some tools like adding 2 numbers, executing Python code, executing Linux functions and much more:

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

We then use the below functions (copy and paste and execute) which will parse the function calls automatically and call the OpenAI endpoint for any model:

{% code overflow="wrap" expandable="true" %}

```python
from openai import OpenAI
def unsloth_inference(
    messages,
    temperature = 0.7,
    top_p = 0.95,
    top_k = 40,
    min_p = 0.01,
    repetition_penalty = 1.0,
):
    messages = messages.copy()
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
            top_p = top_p,
            tools = tools if tools else None,
            tool_choice = "auto" if tools else None,
            extra_body = {"top_k": top_k, "min_p": min_p, "repetition_penalty" :repetition_penalty,}
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
    return messages
```

{% endcode %}

After launching GLM 4.7 via `llama-server` like in [#deploy-with-llama-server-and-openais-completion-library](#deploy-with-llama-server-and-openais-completion-library "mention") or see [Tool Calling Guide](/docs/basics/tool-calling-guide-for-local-llms.md) for more details, we then can do some tool calls:

**Tool Call for mathematical operations for GLM 4.7**

{% code overflow="wrap" %}

```python
messages = [{
    "role": "user",
    "content": [{"type": "text", "text": "What is today's date plus 3 days?"}],
}]
unsloth_inference(messages, temperature = 0.7, top_p = 1.0, top_k = -1, min_p = 0.00)
```

{% endcode %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FoFkZ20QOSGdzT4iz2SOB%2Fimage.png?alt=media&amp;token=e4ca30b0-dcec-4a26-b019-dd33f0600949" alt=""><figcaption></figcaption></figure>

**Tool Call to execute generated Python code for GLM 4.7**

{% code overflow="wrap" %}

```python
messages = [{
    "role": "user",
    "content": [{"type": "text", "text": "Create a Fibonacci function in Python and find fib(20)."}],
}]
unsloth_inference(messages, temperature = 0.7, top_p = 1.0, top_k = -1, min_p = 0.00)
```

{% endcode %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FhS8sWtZwjwerElezCc2C%2Fimage.png?alt=media&amp;token=39032ef8-386e-4837-8dd2-c552c80a3ee3" alt=""><figcaption></figcaption></figure>

### :snowboarder: Improving generation speed

**Use `--fit on` introduced 15th Dec 2025 for maximum usage of your GPU and CPU. See** [**https://github.com/ggml-org/llama.cpp/pull/16653**](https://github.com/ggml-org/llama.cpp/pull/16653) **`--fit on` auto offloads as much of the model as possible to the GPU, then places the rest on CPU.**

If you have more VRAM, you can try offloading more MoE layers, or offloading whole layers themselves.

Normally, `-ot ".ffn_.*_exps.=CPU"` offloads all MoE layers to the CPU! This effectively allows you to fit all non MoE layers on 1 GPU, improving generation speeds. You can customize the regex expression to fit more layers if you have more GPU capacity.

If you have a bit more GPU memory, try `-ot ".ffn_(up|down)_exps.=CPU"` This offloads up and down projection MoE layers.

Try `-ot ".ffn_(up)_exps.=CPU"` if you have even more GPU memory. This offloads only up projection MoE layers.

You can also customize the regex, for example `-ot "\.(6|7|8|9|[0-9][0-9]|[0-9][0-9][0-9])\.ffn_(gate|up|down)_exps.=CPU"` means to offload gate, up and down MoE layers but only from the 6th layer onwards.

Llama.cpp also introduces high throughput mode. Use `llama-parallel`. Read more about it [here](https://github.com/ggml-org/llama.cpp/tree/master/examples/parallel). You can also **quantize the KV cache to 4bits** for example to reduce VRAM / RAM movement, which can also make the generation process faster.

### 📐How to fit long context (full 128K)

To fit longer context, you can use **KV cache quantization** to quantize the K and V caches to lower bits. This can also increase generation speed due to reduced RAM / VRAM data movement. The allowed options for K quantization (default is `f16`) include the below.

`--cache-type-k f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1`

You should use the `_1` variants for somewhat increased accuracy, albeit it's slightly slower. For eg `q4_1, q5_1`

You can also quantize the V cache, but you will need to **compile llama.cpp with Flash Attention** support via `-DGGML_CUDA_FA_ALL_QUANTS=ON`, and use `--flash-attn` to enable it. Then you can use together with `--cache-type-k` :

`--cache-type-v f32, f16, bf16, q8_0, q4_0, q4_1, iq4_nl, q5_0, q5_1`


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/glm-4.7.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
