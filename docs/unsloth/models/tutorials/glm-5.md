> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/glm-5.md).

# GLM-5: How to Run Locally Guide

Run the new GLM-5 model by Z.ai on your own local device!

GLM-5 is Z.ai’s latest reasoning model, delivering stronger coding, agent, and chat performance than [GLM-4.7](/docs/models/tutorials/glm-4.7.md), and is designed for long context reasoning. It increases performance on benchmarks such as Humanity's Last Exam 50.4% (+7.6%), BrowseComp 75.9% (+8.4%) and Terminal-Bench-2.0 61.1% (+28.3%).

The full 744B parameter (40B active) model has a **200K context** window and was pre-trained on 28.5T tokens. The full GLM-5 model requires **1.65TB** of disk space, while the Unsloth Dynamic 2-bit GGUF reduces the size to **241GB** **(-85%)**, and dynamic **1-bit is 176GB (-89%):** [**GLM-5-GGUF**](https://huggingface.co/unsloth/GLM-5-GGUF)

All uploads use Unsloth [Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) for SOTA quantization performance - so 1-bit has important layers upcasted to 8 or 16-bit. Thank you Z.ai for providing Unsloth with day zero access.

### :gear: Usage Guide

The 2-bit dynamic quant UD-IQ2\_XXS uses **241GB** of disk space - this can directly fit on a **256GB unified memory Mac**, and also works well in a **1x24GB card and 256GB of RAM** with MoE offloading. The **1-bit** quant will fit on a 180GB RAM and 8-bit requires 805GB RAM.

{% hint style="success" %}
For best performance, make sure your total available memory (VRAM + system RAM) exceeds the size of the quantized model file you’re downloading. If it doesn’t, llama.cpp can still run via SSD/HDD offloading, but inference will be slower.
{% endhint %}

### Recommended Settings

Use distinct settings for different use cases:

| Default Settings (Most Tasks)    | SWE Bench Verified               |
| -------------------------------- | -------------------------------- |
| temperature = 1.0                | temperature = 0.7                |
| top\_p = 0.95                    | top\_p = 1.0                     |
| max new tokens = 131072          | max new tokens = 16384           |
| repeat penalty = disabled or 1.0 | repeat penalty = disabled or 1.0 |

* `Min_P = 0.01` (llama.cpp's default is 0.05)
* **Maximum context window:** `202,752`.
* For multi-turn agentic tasks (τ²-Bench and Terminal Bench 2), please turn on Preserved\
  Thinking mode.

## Run GLM-5 Tutorials:

#### ✨ Run in llama.cpp

{% stepper %}
{% step %}
Obtain the latest `llama.cpp` **on** [**GitHub here**](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endstep %}

{% step %}
If you want to use `llama.cpp` directly to load models, you can do the below: (:IQ2\_XXS) is the quantization type. You can also download via Hugging Face (point 3). This is similar to `ollama run` . Use `export LLAMA_CACHE="folder"` to force `llama.cpp` to save to a specific location. Remember the model has only a maximum of 200K context length.

Follow this for **general instruction** use-cases:

```bash
export LLAMA_CACHE="unsloth/GLM-5-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/GLM-5-GGUF:UD-IQ2_XXS \
    --ctx-size 16384 \
    --flash-attn on \
    --temp 0.7 \
    --top-p 1.0 \
    --min-p 0.01
```

Follow this for **tool-calling** use-cases:

```bash
export LLAMA_CACHE="unsloth/GLM-5-GGUF"
./llama.cpp/llama-cli \
    -hf unsloth/GLM-5-GGUF:UD-IQ2_XXS \
    --ctx-size 16384 \
    --flash-attn on \
    --temp 1.0 \
    --top-p 0.95 \
    --min-p 0.01
```

{% endstep %}

{% step %}
Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD-Q2_K_XL` (dynamic 2bit quant) or other quantized versions like `UD-Q4_K_XL` . We <mark style="background-color:green;">**recommend using our 2bit dynamic quant**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**`UD-Q2_K_XL`**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**to balance size and accuracy**</mark>. If downloads get stuck, see [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

```bash
pip install -U huggingface_hub
hf download unsloth/GLM-5-GGUF \
    --local-dir unsloth/GLM-5-GGUF \
    --include "*UD-IQ2_XXS*" # Use "*UD-TQ1_0*" for Dynamic 1bit
```

{% endstep %}

{% step %}
You can edit `--threads 32` for the number of CPU threads, `--ctx-size 16384` for context length, `--n-gpu-layers 2` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/GLM-5-GGUF/UD-IQ2_XXS/GLM-5-UD-IQ2_XXS-00001-of-00006.gguf \
    --temp 1.0 \
    --top-p 0.95 \
    --min-p 0.01 \
    --ctx-size 16384 \
    --seed 3407
```

{% endcode %}
{% endstep %}
{% endstepper %}

### 🦙 Llama-server serving & OpenAI's completion library

To deploy GLM-5 for production, we use `llama-server` In a new terminal say via tmux, deploy the model via:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-server \
    --model unsloth/GLM-5-GGUF/UD-IQ2_XXS/GLM-5-UD-IQ2_XXS-00001-of-00006.gguf \
    --alias "unsloth/GLM-5" \
    --prio 3 \
    --temp 1.0 \
    --top-p 0.95 \
    --ctx-size 16384 \
    --port 8001
```

{% endcode %}

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
    model = "unsloth/GLM-5",
    messages = [{"role": "user", "content": "Create a Snake game."},],
)
print(completion.choices[0].message.content)
```

{% endcode %}

And you will get the following example of a Snake game:

{% columns %}
{% column width="58.333333333333336%" %}
{% code expandable="true" %}

````markdown
Here is a complete, playable Snake game contained within a single HTML file. You can copy this code, save it as an `.html` file (e.g., `snake.html`), and open it in your web browser to play.

### The Code

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Classic Snake Game</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #222;
            color: white;
            font-family: Arial, sans-serif;
        }

        #gameCanvas {
            border: 2px solid #fff;
            background-color: #000;
        }

        h1 {
            margin-bottom: 10px;
        }

        #scoreBoard {
            font-size: 20px;
            margin-bottom: 10px;
        }

        #gameOverMenu {
            position: absolute;
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: rgba(0, 0, 0, 0.85);
            padding: 20px;
            border-radius: 10px;
            border: 2px solid red;
        }

        button {
            margin-top: 15px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
        }
        
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>

    <h1>Snake Game</h1>
    <div id="scoreBoard">Score: 0</div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>

    <div id="gameOverMenu">
        <h2 style="color: red; margin: 0;">Game Over!</h2>
        <p id="finalScore">Final Score: 0</p>
        <button onclick="resetGame()">Play Again</button>
    </div>

    <script>
        // Game Constants
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const scoreBoard = document.getElementById('scoreBoard');
        const gameOverMenu = document.getElementById('gameOverMenu');
        const finalScoreDisplay = document.getElementById('finalScore');

        const gridSize = 20; // Size of each square
        const tileCount = canvas.width / gridSize; // Number of squares per row/column

        // Game Variables
        let dx = 0; // Horizontal velocity
        let dy = 0; // Vertical velocity
        let score = 0;
        let snake = [];
        let foodX, foodY;
        let gameInterval;
        let isGameRunning = false;

        // Initialize the game
        function initGame() {
            snake = [
                {x: 10, y: 10}, 
                {x: 9, y: 10}, 
                {x: 8, y: 10}
            ];
            score = 0;
            scoreBoard.innerText = 'Score: ' + score;
            dx = 1; // Start moving right immediately
            dy = 0;
            placeFood();
            isGameRunning = true;
            gameOverMenu.style.display = 'none';
            
            // Start the game loop
            if (gameInterval) clearInterval(gameInterval);
            gameInterval = setInterval(gameLoop, 100); // Run game loop every 100ms
        }

        // Main game loop
        function gameLoop() {
            if (!isGameRunning) return;

            moveSnake();
            if (checkGameOver()) {
                endGame();
                return;
            }
            checkFoodCollision();
            draw();
        }

        // Move the snake
        function moveSnake() {
            // Create new head based on current direction
            const head = {x: snake[0].x + dx, y: snake[0].y + dy};
            
            // Add new head to the beginning of the array
            snake.unshift(head);

            // Remove the tail (last element) unless food is eaten
            // Note: We handle removing the tail in checkFoodCollision
            snake.pop(); 
        }

        // Check if snake eats food
        function checkFoodCollision() {
            const head = snake[0];
            
            if (head.x === foodX && head.y === foodY) {
                // Grow snake: add a tail piece (duplicate the last one)
                snake.push({...snake[snake.length - 1]});
                score += 10;
                scoreBoard.innerText = 'Score: ' + score;
                placeFood();
            }
        }

        // Check for collisions (walls or self)
        function checkGameOver() {
            const head = snake[0];

            // Wall collision
            if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
                return true;
            }

            // Self collision (start checking from the 4th segment because head can't hit the first 3)
            for (let i = 4; i < snake.length; i++) {
                if (head.x === snake[i].x && head.y === snake[i].y) {
                    return true;
                }
            }

            return false;
        }

        // Draw everything
        function draw() {
            // Clear canvas
            ctx.fillStyle = 'black';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw Food
            ctx.fillStyle = 'red';
            ctx.fillRect(foodX * gridSize, foodY * gridSize, gridSize - 2, gridSize - 2);

            // Draw Snake
            ctx.fillStyle = 'lime';
            for (let i = 0; i < snake.length; i++) {
                // Draw the head slightly different or just standard
                const part = snake[i];
                ctx.fillRect(part.x * gridSize, part.y * gridSize, gridSize - 2, gridSize - 2);
            }
        }

        // Place food at random position
        function placeFood() {
            foodX = Math.floor(Math.random() * tileCount);
            foodY = Math.floor(Math.random() * tileCount);

            // Ensure food doesn't spawn on the snake body
            for (let part of snake) {
                if (part.x === foodX && part.y === foodY) {
                    placeFood(); // Recursively find a new spot
                    return;
                }
            }
        }

        // End game logic
        function endGame() {
            isGameRunning = false;
            clearInterval(gameInterval);
            finalScoreDisplay.innerText = 'Final Score: ' + score;
            gameOverMenu.style.display = 'flex';
        }

        // Reset game logic
        function resetGame() {
            initGame();
        }

        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            // Prevent reversing direction (can't go left if going right)
            switch(e.key) {
                case 'ArrowUp':
                    if (dy !== 1) { dx = 0; dy = -1; }
                    break;
                case 'ArrowDown':
                    if (dy !== -1) { dx = 0; dy = 1; }
                    break;
                case 'ArrowLeft':
                    if (dx !== 1) { dx = -1; dy = 0; }
                    break;
                case 'ArrowRight':
                    if (dx !== -1) { dx = 1; dy = 0; }
                    break;
                case ' ':
                    if (!isGameRunning && gameOverMenu.style.display !== 'flex') {
                        initGame();
                    }
                    break;
            }
        });

        // Start the game on load
        initGame();
    </script>
</body>
</html>
```

### How to Play
1.  **Copy the code** above.
2.  Create a new file on your computer named `snake.html`.
3.  **Paste the code** into that file and save it.
4.  **Double-click `snake.html`** to open it in your browser.

### Controls
*   **Arrow Keys**: Move Up, Down, Left, Right.
*   **Spacebar**: Starts the game (if it hasn't started yet).
*   **Play Again Button**: Appears when you crash to restart the game.

### Features of this Version
*   **Grid-based movement**: Classic retro feel.
*   **Score tracking**: Updates in real-time.
*   **Game Over Screen**: Displays your final score and allows you to restart easily.
*   **Collision Detection**: Ends the game if you hit the walls or yourself.
*   **Self-Collision Safety**: The code prevents the snake from accidentally eating itself immediately after eating food due to "tail skipping" logic commonly found in simple tutorials.
````

{% endcode %}
{% endcolumn %}

{% column width="41.666666666666664%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FsdUp9wbpqDx0Lhp00xZ0%2Fimage.png?alt=media&amp;token=a5e67ac2-65bf-43e0-8c13-4aef9a7d269e" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

### :computer: vLLM Deployment

You can now serve Z.ai's FP8 version of the model via vLLM. You need 860GB VRAM or more, so 8xH200 (141x8 = 1128GB) is at least recommended. 8xB200 works well. Firstly, install vllm nightly:

{% code overflow="wrap" %}

```bash
uv pip install --upgrade --force-reinstall vllm --torch-backend=auto --extra-index-url https://wheels.vllm.ai/nightly/cu130
uv pip install --upgrade --force-reinstall git+https://github.com/huggingface/transformers.git
uv pip install --force-reinstall numba
```

{% endcode %}

To disable FP8 KV Cache (reduces memory usage by 50%), remove `--kv-cache-dtype fp8`

```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:False
vllm serve unsloth/GLM-5-FP8 \
    --served-model-name unsloth/GLM-5-FP8 \
    --kv-cache-dtype fp8 \
    --tensor-parallel-size 8 \
    --tool-call-parser glm47 \
    --reasoning-parser glm45 \
    --enable-auto-tool-choice \
    --dtype bfloat16 \
    --seed 3407 \
    --max-model-len 200000 \
    --gpu-memory-utilization 0.93 \
    --max_num_batched_tokens 4096 \
    --speculative-config.method mtp \
    --speculative-config.num_speculative_tokens 1 \
    --port 8001
```

You can then call the served model via the OpenAI API:

```python
from openai import AsyncOpenAI, OpenAI
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8001/v1"
client = OpenAI( # or AsyncOpenAI
    api_key = openai_api_key,
    base_url = openai_api_base,
)
```

### :hammer:Tool Calling with GLM 5

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
    temperature = 1.0,
    top_p = 0.95,
    top_k = -1,
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

After launching GLM 5 via `llama-server` like in [#deploy-with-llama-server-and-openais-completion-library](#deploy-with-llama-server-and-openais-completion-library "mention") or see [Tool Calling Guide](/docs/basics/tool-calling-guide-for-local-llms.md) for more details, we then can do some tool calls.

### 📊 Benchmarks

You can view further below for benchmarks in table format:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F3QI8akFZoQFXsZ2ojtgK%2Fglm5%20bench.jpg?alt=media&amp;token=0fb5d73f-4dc4-46f5-bd76-206c26ff5e96" alt="" width="375"><figcaption></figcaption></figure>

<table data-full-width="true"><thead><tr><th>Benchmark</th><th>GLM-5</th><th>GLM-4.7</th><th>DeepSeek-V3.2</th><th>Kimi K2.5</th><th>Claude Opus 4.5</th><th>Gemini 3 Pro</th><th>GPT-5.2 (xhigh)</th></tr></thead><tbody><tr><td>HLE</td><td>30.5</td><td>24.8</td><td>25.1</td><td>31.5</td><td>28.4</td><td>37.2</td><td>35.4</td></tr><tr><td>HLE (w/ Tools)</td><td>50.4</td><td>42.8</td><td>40.8</td><td>51.8</td><td>43.4*</td><td>45.8*</td><td>45.5*</td></tr><tr><td>AIME 2026 I</td><td>92.7</td><td>92.9</td><td>92.7</td><td>92.5</td><td>93.3</td><td>90.6</td><td>-</td></tr><tr><td>HMMT Nov. 2025</td><td>96.9</td><td>93.5</td><td>90.2</td><td>91.1</td><td>91.7</td><td>93.0</td><td>97.1</td></tr><tr><td>IMOAnswerBench</td><td>82.5</td><td>82.0</td><td>78.3</td><td>81.8</td><td>78.5</td><td>83.3</td><td>86.3</td></tr><tr><td>GPQA-Diamond</td><td>86.0</td><td>85.7</td><td>82.4</td><td>87.6</td><td>87.0</td><td>91.9</td><td>92.4</td></tr><tr><td>SWE-bench Verified</td><td>77.8</td><td>73.8</td><td>73.1</td><td>76.8</td><td>80.9</td><td>76.2</td><td>80.0</td></tr><tr><td>SWE-bench Multilingual</td><td>73.3</td><td>66.7</td><td>70.2</td><td>73.0</td><td>77.5</td><td>65.0</td><td>72.0</td></tr><tr><td>Terminal-Bench 2.0 (Terminus 2)</td><td>56.2 / 60.7 †</td><td>41.0</td><td>39.3</td><td>50.8</td><td>59.3</td><td>54.2</td><td>54.0</td></tr><tr><td>Terminal-Bench 2.0 (Claude Code)</td><td>56.2 / 61.1 †</td><td>32.8</td><td>46.4</td><td>-</td><td>57.9</td><td>-</td><td>-</td></tr><tr><td>CyberGym</td><td>43.2</td><td>23.5</td><td>17.3</td><td>41.3</td><td>50.6</td><td>39.9</td><td>-</td></tr><tr><td>BrowseComp</td><td>62.0</td><td>52.0</td><td>51.4</td><td>60.6</td><td>37.0</td><td>37.8</td><td>-</td></tr><tr><td>BrowseComp (w/ Context Manage)</td><td>75.9</td><td>67.5</td><td>67.6</td><td>74.9</td><td>67.8</td><td>59.2</td><td>65.8</td></tr><tr><td>BrowseComp-Zh</td><td>72.7</td><td>66.6</td><td>65.0</td><td>62.3</td><td>62.4</td><td>66.8</td><td>76.1</td></tr><tr><td>τ²-Bench</td><td>89.7</td><td>87.4</td><td>85.3</td><td>80.2</td><td>91.6</td><td>90.7</td><td>85.5</td></tr><tr><td>MCP-Atlas (Public Set)</td><td>67.8</td><td>52.0</td><td>62.2</td><td>63.8</td><td>65.2</td><td>66.6</td><td>68.0</td></tr><tr><td>Tool-Decathlon</td><td>38.0</td><td>23.8</td><td>35.2</td><td>27.8</td><td>43.5</td><td>36.4</td><td>46.3</td></tr><tr><td>Vending Bench 2</td><td>$4,432.12</td><td>$2,376.82</td><td>$1,034.00</td><td>$1,198.46</td><td>$4,967.06</td><td>$5,478.16</td><td>$3,591.33</td></tr></tbody></table>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/glm-5.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
