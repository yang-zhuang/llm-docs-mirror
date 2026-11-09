> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/qwen3-coder-next.md).

# Qwen3-Coder-Next: How to Run Locally

Guide to run Qwen3-Coder-Next locally on your device!

Qwen releases Qwen3-Coder-Next, an 80B MoE model (3B active parameters) with **256K context** for fast agentic coding and local use. It is comparable to the performance of models with 10–20× more active parameters.

It runs on **46GB RAM**/VRAM/unified memory (85GB for 8-bit), is non-reasoning for ultra-quick code responses. The model excels at long-horizon reasoning, complex tool use, and recovery from execution failures.

{% hint style="success" %}
**Feb 19 update**: Tool-calling should now be even better after llama.cpp fixes parsing.

**NEW!** See [quantization benchmarks](#gguf-quantization-benchmarks) for our Dynamic GGUFs!

**Feb 4:** `llama.cpp` fixed a bug correcting the calculation for `vectorized key_gdiff.` This fixes previous looping and output issues. We updated the GGUFs - please **re-download** and **UPDATE** `llama.cpp` for better outputs.
{% endhint %}

You’ll also learn to run the model on Codex & Claude Code. For **fine-tuning**, Qwen3-Next-Coder fits on a single B200 GPU for bf16 LoRA in Unsloth.

Qwen3-Coder-Next Unsloth [Dynamic GGUFs](/docs/basics/dynamic-3.0-ggufs.md) to run: [unsloth/Qwen3-Coder-Next-GGUF](https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF)

<a href="/docs/models/qwen3-coder-next.md#run-qwen3-coder-next" class="button primary">Run GGUF Tutorial</a><a href="https://unsloth.ai/docs/models/qwen3-coder-next#claude-codex" class="button secondary">Codex & Claude Code</a><a href="/docs/models/qwen3-coder-next.md#fp8-qwen3-coder-next-in-vllm" class="button secondary">FP8 vLLM Tutorial</a>

### ⚙️ Usage Guide

Don't have 46GB RAM or unified memory? No worries you can run our smaller quants like 3-bit. It is best to have the model size = to the sum of your compute ( **`disk space + RAM + VRAM ≥ size of quant).`** If your quant fully fits on your device, expect 20+ tokens/s. If it doesn't fit, it'll still work by offloading but it will be slower.

To achieve optimal performance, Qwen recommends these settings:

* <mark style="background-color:blue;">`Temperature = 1.0`</mark>
* `Top_P = 0.95`
* `Top_K = 40`
* `Min_P = 0.01` (llama.cpp's default is 0.05)
* `repeat penalty` = disabled or 1.0

Supports up to `262,144` context natively but you can set it to `32,768` tokens for less memory use.

### 🖥️ Run Qwen3-Coder-Next

Depending on your use-case you will need to use different settings. Because this guide uses 4-bit, you will need around 46GB RAM/unified memory. We recommend using at least 3-bit precision for best performance.

#### 🦥 Unsloth Studio Guide

Qwen3-Coder-Next can be run and fine-tuned in [Unsloth Studio](/docs/new/studio.md), our new open-source web UI for local AI. With Unsloth Studio, you can run models locally on **MacOS, Windows**, Linux and:

{% columns %}
{% column %}

* Search, download, [run GGUFs](/docs/new/studio.md#run-models-locally) and safetensor models
* [**Self-healing** tool calling](/docs/new/studio.md#execute-code--heal-tool-calling) + **web search**
* [**Code execution**](/docs/new/studio.md#run-models-locally) (Python, Bash)
* [Automatic inference](https://unsloth.ai/docs/desktop#feature-deep-dive) parameter tuning (temp, top-p, etc.)
* Fast CPU + GPU inference via llama.cpp
* [Train LLMs](/docs/new/studio.md#no-code-training) 2x faster with 70% less VRAM
  {% endcolumn %}

{% column %}

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FFeQ0UUlnjXkDdqhcWglh%2Fskinny%20studio%20chat.png?alt=media&amp;token=c2ee045f-c243-4024-a8e4-bb4dbe7bae79" alt=""><figcaption></figcaption></figure></div>
{% endcolumn %}
{% endcolumns %}

{% stepper %}
{% step %}
**Install Unsloth**

Run in your terminal:

MacOS, Linux, WSL:

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

Windows PowerShell:

```bash
irm https://unsloth.ai/install.ps1 | iex
```

{% hint style="success" %}
**Installation will be quick and take approx 1-2 mins.**
{% endhint %}
{% endstep %}

{% step %}
**Launch Unsloth**

MacOS, Linux, WSL and Windows:

```bash
unsloth studio -H 0.0.0.0 -p 8888
```

Then open `http://localhost:8888` in your browser.
{% endstep %}

{% step %}
**Search and download Qwen3-Coder-Next**

On first launch you will need to create a password to secure your account and sign in again later. You’ll then see a brief onboarding wizard to choose a model, dataset, and basic settings. You can skip it at any time and go directly to chat.

Then go to the [Unsloth Chat](/docs/new/studio/chat.md) tab and search for **Qwen3-Coder-Next** in the search bar and download your desired model and quant.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fit06amlW1KexxlYARKNV%2FScreenshot%202026-04-02%20at%201.57.55%E2%80%AFAM.png?alt=media&amp;token=74fb6c0f-fbd1-4506-be76-050f27de8d02" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}
**Run Qwen3-Coder-Next**

Inference parameters should be auto-set when using Unsloth Studio, however you can still change it manually. You can also edit the context length, chat template and other settings.

For more information, you can view our [Unsloth Studio inference guide](/docs/new/studio/chat.md).

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FXPQGEEr1YoKofrTatAKK%2Ftoolcallingif.gif?alt=media&amp;token=25d68698-fb13-4c46-99b2-d39fb025df08" alt="" width="563"><figcaption></figcaption></figure></div>
{% endstep %}
{% endstepper %}

#### Llama.cpp Tutorial (GGUF):

Instructions to run in llama.cpp (note we will be using 4-bit to fit most devices):

{% stepper %}
{% step %}
Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

{% code overflow="wrap" %}

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-cli llama-mtmd-cli llama-server llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

{% endcode %}
{% endstep %}

{% step %}
You can directly pull from Hugging Face. You can increase the context to 256K if your RAM/VRAM can fit it. Using `--fit on` will also auto determine the context length.

You can use the recommended parameters: `temperature=1.0`, `top_p=0.95`, `top_k=40`

```bash
./llama.cpp/llama-cli \
    -hf unsloth/Qwen3-Coder-Next-GGUF:UD-Q4_K_XL \
    --ctx-size 16384 \
    --temp 1.0 --top-p 0.95 --min-p 0.01 --top-k 40
```

{% endstep %}

{% step %}
Download the model via (after installing `pip install huggingface_hub`). You can choose `UD-Q4_K_XL` or other quantized versions. If downloads get stuck, see [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

{% code overflow="wrap" %}

```bash
pip install -U huggingface_hub
hf download unsloth/Qwen3-Coder-Next-GGUF \
    --local-dir unsloth/Qwen3-Coder-Next-GGUF \
    --include "*UD-Q4_K_XL*"
```

{% endcode %}
{% endstep %}

{% step %}
Then run the model in conversation mode:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/Qwen3-Coder-Next-GGUF/Qwen3-Coder-Next-UD-Q4_K_XL.gguf \
    --seed 3407 \
    --temp 1.0 \
    --top-p 0.95 \
    --min-p 0.01 \
    --top-k 40
```

{% endcode %}

Also, adjust **context window** as required, up to `262,144`

{% hint style="info" %}
NOTE: This model supports only non-thinking mode and does not generate `<think></think>` blocks in its output. So specifying `enable_thinking=False` is no longer required.
{% endhint %}
{% endstep %}
{% endstepper %}

### 🦙Llama-server serving & deployment

To deploy Qwen3-Coder-Next for production, we use `llama-server` In a new terminal say via tmux. Then, deploy the model via:

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-server \
    --model unsloth/Qwen3-Coder-Next-GGUF/Qwen3-Coder-Next-UD-Q4_K_XL.gguf \
    --alias "unsloth/Qwen3-Coder-Next" \
    --seed 3407 \
    --temp 1.0 \
    --top-p 0.95 \
    --min-p 0.01 \
    --top-k 40 \
    --port 8001
```

{% endcode %}

Then in a new terminal, after doing `pip install openai`, we can run the model:

{% code overflow="wrap" %}

```python
from openai import OpenAI
import json
openai_client = OpenAI(
    base_url = "http://127.0.0.1:8001/v1",
    api_key = "sk-no-key-required",
)
completion = openai_client.chat.completions.create(
    model = "unsloth/Qwen3-Coder-Next",
    messages = [{"role": "user", "content": "Create a Flappy Bird game in HTML"},],
)
print(completion.choices[0].message.content)
```

{% endcode %}

Which will output:

{% columns %}
{% column width="66.66666666666666%" %}
{% code overflow="wrap" expandable="true" %}

````markdown
Here is a complete, working Flappy Bird game contained in a single file.

I have used **HTML5 Canvas** for the graphics and **JavaScript** for the physics (gravity, collision detection, and scoring). No external images or downloads are required; the game draws the bird and pipes using code.

### How to run this:
1.  Copy the code block below.
2.  Create a new file on your computer named `game.html`.
3.  Paste the code into that file and save it.
4.  Double-click `game.html` to open it in your web browser.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Flappy Bird</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #333;
            font-family: 'Courier New', Courier, monospace;
            color: white;
        }

        h1 {
            margin-bottom: 10px;
        }

        #game-container {
            position: relative;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }

        canvas {
            display: block;
            background-color: #70c5ce; /* Sky blue */
            border: 4px solid #000;
        }

        #ui-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none; /* Let clicks pass through to canvas */
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .message {
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            color: #333;
        }

        #score-board {
            position: absolute;
            top: 20px;
            width: 100%;
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: white;
            text-shadow: 2px 2px 0 #000;
            z-index: 10;
        }
    </style>
</head>
<body>

    <h1>Flappy Bird Clone</h1>
    
    <div id="game-container">
        <div id="score-board">0</div>
        <canvas id="birdCanvas" width="320" height="480"></canvas>
        
        <div id="ui-layer">
            <div id="start-screen" class="message">
                <h2>Ready to Fly?</h2>
                <p>Press <strong>Space</strong> or <strong>Click</strong> to Jump</p>
                <p>Press Space to Start</p>
            </div>
            <div id="game-over-screen" class="message" style="display: none;">
                <h2>Game Over</h2>
                <p>Score: <span id="final-score">0</span></p>
                <p>Best: <span id="best-score">0</span></p>
                <p>Press <strong>Space</strong> to Restart</p>
            </div>
        </div>
    </div>

    <script>
        // --- Configuration ---
        const canvas = document.getElementById('birdCanvas');
        const ctx = canvas.getContext('2d');
        const scoreElement = document.getElementById('score-board');
        const startScreen = document.getElementById('start-screen');
        const gameOverScreen = document.getElementById('game-over-screen');
        const finalScoreSpan = document.getElementById('final-score');
        const bestScoreSpan = document.getElementById('best-score');

        // Game Variables
        let frames = 0;
        let score = 0;
        let highScore = localStorage.getItem('flappyHighScore') || 0;
        let gameState = 'START'; // START, PLAYING, GAMEOVER
        const gravity = 0.25;
        const speed = 2; // Speed of pipes moving left

        // --- The Bird Object ---
        const bird = {
            x: 50,
            y: 150,
            width: 30,
            height: 30,
            velocity: 0,
            jumpStrength: 4.5,
            radius: 15,
            draw: function() {
                ctx.fillStyle = "#FFD700"; // Gold color
                ctx.beginPath();
                ctx.arc(this.x + this.radius, this.y + this.radius, this.radius, 0, Math.PI * 2);
                ctx.fill();
                ctx.lineWidth = 2;
                ctx.stroke();

                // Eye
                ctx.fillStyle = "white";
                ctx.beginPath();
                ctx.arc(this.x + this.radius + 5, this.y + this.radius - 5, 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = "black";
                ctx.beginPath();
                ctx.arc(this.x + this.radius + 7, this.y + this.radius - 5, 2, 0, Math.PI * 2);
                ctx.fill();
                
                // Beak
                ctx.fillStyle = "orange";
                ctx.beginPath();
                ctx.moveTo(this.x + this.radius + 10, this.y + this.radius);
                ctx.lineTo(this.x + this.radius + 20, this.y + this.radius + 5);
                ctx.lineTo(this.x + this.radius + 10, this.y + this.radius + 10);
                ctx.fill();
                ctx.stroke();
            },
            update: function() {
                this.velocity += gravity;
                this.y += this.velocity;

                // Floor Collision
                if (this.y + this.height >= canvas.height) {
                    this.y = canvas.height - this.height;
                    gameOver();
                }
                
                // Ceiling Collision (Optional: prevents flying over pipes)
                if (this.y < 0) {
                    this.y = 0;
                    this.velocity = 0;
                }
            },
            jump: function() {
                this.velocity = -this.jumpStrength;
            },
            reset: function() {
                this.y = 150;
                this.velocity = 0;
            }
        };

        // --- The Pipes Array ---
        const pipes = {
            position: [],
            width: 50,
            gap: 120, // Space between top and bottom pipe
            dx: 2, // Movement speed

            draw: function() {
                for (let i = 0; i < this.position.length; i++) {
                    let p = this.position[i];
                    let topY = p.y;
                    let bottomY = p.y + this.gap;

                    ctx.fillStyle = "#228B22"; // Forest Green

                    // Top Pipe
                    ctx.fillRect(p.x, 0, this.width, topY);
                    ctx.strokeRect(p.x, 0, this.width, topY);

                    // Bottom Pipe
                    ctx.fillRect(p.x, bottomY, this.width, canvas.height - bottomY);
                    ctx.strokeRect(p.x, bottomY, this.width, canvas.height - bottomY);
                }
            },

            update: function() {
                // Add new pipe every 120 frames (approx 2 seconds)
                if (frames % 120 === 0) {
                    // Random height for top pipe
                    // Min height 50, Max height canvas - gap - 50
                    let maxY = canvas.height - this.gap - 50;
                    let randomY = Math.floor(Math.random() * (maxY - 50 + 1) + 50);
                    
                    this.position.push({
                        x: canvas.width,
                        y: randomY
                    });
                }

                for (let i = 0; i < this.position.length; i++) {
                    let p = this.position[i];
                    p.x -= this.dx;

                    // Collision Detection
                    // Logic: Check if bird X is within pipe X range
                    if (bird.x + bird.width > p.x && bird.x < p.x + this.width) {
                        // Logic: Check if bird Y is hitting Top Pipe OR Bottom Pipe
                        if (bird.y < p.y || bird.y + bird.height > p.y + this.gap) {
                            gameOver();
                        }
                    }

                    // Score Update (when bird passes pipe)
                    if (p.x + this.width < bird.x && !p.passed) {
                        score++;
                        scoreElement.innerText = score;
                        p.passed = true;
                    }

                    // Remove pipes that have gone off screen
                    if (p.x + this.width <= 0) {
                        this.position.shift();
                        // Decrement i because array length changed
                        i--; 
                    }
                }
            },
            
            reset: function() {
                this.position = [];
            }
        };

        // --- Background (Clouds/Grass) ---
        const background = {
            draw: function() {
                // Draw Grass
                ctx.fillStyle = "#7cfc00"; // Lawn Green
                ctx.fillRect(0, canvas.height - 20, canvas.width, 20);
                ctx.beginPath();
                ctx.moveTo(0, canvas.height - 20);
                ctx.lineTo(canvas.width, canvas.height - 20);
                ctx.stroke();
            }
        };

        // --- Game Control Functions ---

        function loop() {
            // Clear Canvas
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw Background
            background.draw();

            if (gameState === 'START') {
                bird.draw();
                // Draw a ground line
                ctx.fillStyle = "#ded895";
                ctx.fillRect(0, canvas.height - 10, canvas.width, 10);
            } 
            else if (gameState === 'PLAYING') {
                bird.update();
                bird.draw();
                pipes.update();
                pipes.draw();
                frames++;
            } 
            else if (gameState === 'GAMEOVER') {
                pipes.draw();
                bird.draw();
                // Don't update frames or position, just freeze
            }

            requestAnimationFrame(loop);
        }

        function startGame() {
            gameState = 'PLAYING';
            startScreen.style.display = 'none';
            gameOverScreen.style.display = 'none';
            score = 0;
            frames = 0;
            scoreElement.innerText = score;
            bird.reset();
            pipes.reset();
        }

        function gameOver() {
            gameState = 'GAMEOVER';
            
            // Update High Score
            if (score > highScore) {
                highScore = score;
                localStorage.setItem('flappyHighScore', highScore);
            }

            finalScoreSpan.innerText = score;
            bestScoreSpan.innerText = highScore;
            gameOverScreen.style.display = 'block';
        }

        // --- Input Handling ---

        function handleInput(e) {
            // Prevent default scrolling behavior for Space
            if (e.type === 'keydown' && e.code === 'Space') {
                e.preventDefault();
            }

            if (e.code === 'Space' || e.type === 'mousedown' || e.type === 'touchstart') {
                switch (gameState) {
                    case 'START':
                        startGame();
                        bird.jump();
                        break;
                    case 'PLAYING':
                        bird.jump();
                        break;
                    case 'GAMEOVER':
                        startGame();
                        bird.jump();
                        break;
                }
            }
        }

        window.addEventListener('keydown', handleInput);
        canvas.addEventListener('mousedown', handleInput);
        canvas.addEventListener('touchstart', handleInput);

        // Initialize
        loop();

    </script>
</body>
</html>
```

### Features in this version:
1.  **Physics:** Realistic gravity and jumping mechanics.
2.  **Collision Detection:** The game ends if you hit the pipes, the floor, or the ceiling.
3.  **Scoring System:** You get 1 point for every pipe you pass.
4.  **High Score:** Uses your browser's LocalStorage to remember your best score even if you refresh the page.
5.  **Responsive Controls:** Works with the **Spacebar**, **Mouse Click**, or **Touch** (for mobile devices).
6.  **Graphics:** The bird is drawn with code (including an eye and beak) and the pipes have borders, so no broken image links will occur.
````

{% endcode %}

We extracted the HTML and ran it, and the example Flappy Bird game it generated worked well!
{% endcolumn %}

{% column width="33.33333333333334%" %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F7ATJWz7O4jMxpVI6I1Wk%2Fimage.png?alt=media&amp;token=a81548fa-843b-499d-9db6-6f215ad5fb99" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

### 👾 OpenAI Codex & Claude Code <a href="#claude-codex" id="claude-codex"></a>

To run the model via local coding agentic workloads, you can follow our guide. Use the `llama-server` we just set up just then, and set the model name to the exact id it reports at `GET /v1/models` (the `--alias` value above, `unsloth/Qwen3-Coder-Next`). Follow the correct Qwen3-Coder-Next parameters and usage instructions.

{% columns %}
{% column %}
{% content-ref url="/pages/w020xJgdCTBtTvfHtvye" %}
[Claude Code](/docs/basics/claude-code.md)
{% endcontent-ref %}
{% endcolumn %}

{% column %}
{% content-ref url="/pages/PCjZ57h5pE0QccKyJMYD" %}
[OpenAI Codex](/docs/basics/codex.md)
{% endcontent-ref %}
{% endcolumn %}
{% endcolumns %}

After following the instructions for Claude Code for example you will see:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fup2DMSMPjNR8BM9pgR0v%2Fimage.png?alt=media&amp;token=152e9ee0-2491-4379-af18-8fca0789b19d" alt="" width="563"><figcaption></figcaption></figure>

We can then ask say `Create a Python game for Chess` :

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F9TfMAoKSdMpb8OHKNnHH%2Fimage.png?alt=media&amp;token=771df3aa-91ab-4c1e-8676-1830058001ca" alt="" width="563"><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FWP3lI5mQW2EHB79qqgDz%2Fimage.png?alt=media&amp;token=55cf3189-e100-419c-a615-024b45948284" alt="" width="563"><figcaption></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fn8DZddDODQZGCP8giKYY%2Fimage.png?alt=media&amp;token=996c8cb9-d199-4045-90f0-408690e02667" alt="" width="563"><figcaption></figcaption></figure></div>

If you see `API Error: 400 {"error":{"code":400,"message":"request (16582 tokens) exceeds the available context size (16384 tokens), try increasing it","type":"exceed_context_size_error","n_prompt_tokens":16582,"n_ctx":16384}}` that means you need to increase the context length or see [#how-to-fit-long-context-256k-to-1m](#how-to-fit-long-context-256k-to-1m "mention")

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FP6anV1XewSWIovaH3f7c%2Fimage.png?alt=media&amp;token=285a540b-f6fc-4541-b807-bf4f6dc3807b" alt=""><figcaption></figcaption></figure>

### 🎱 FP8 Qwen3-Coder-Next in vLLM

You can now use our new [FP8 Dynamic quant](https://huggingface.co/unsloth/Qwen3-Coder-Next-FP8-Dynamic) of the model for premium and fast inference. First install vLLM from nightly. Change `--extra-index-url https://wheels.vllm.ai/nightly/cu130` to your CUDA version found via `nvidia-smi` - only `cu129` and `cu130` are currently supported.

{% hint style="success" %}
If using vLLM / SGLang, try using our FP8-Dynamic quants which can boost throughput by 25% or more! See [#fp8-qwen3-coder-next-in-vllm](#fp8-qwen3-coder-next-in-vllm "mention")
{% endhint %}

{% code overflow="wrap" %}

```bash
# Install uv if you don't have it for faster environment installs
curl -LsSf https://astral.sh/uv/install.sh | sh

# Make a new Python environment - not needed if you want to change your whole system
uv venv unsloth_fp8 --python 3.12 --seed
source unsloth_fp8/bin/activate

uv pip install --upgrade --force-reinstall vllm --torch-backend=auto --extra-index-url https://wheels.vllm.ai/nightly/cu130
uv pip install --upgrade --force-reinstall git+https://github.com/huggingface/transformers.git
uv pip install --force-reinstall numba
```

{% endcode %}

Then serve [Unsloth's dynamic FP8 version](https://huggingface.co/unsloth/Qwen3-Coder-Next-FP8-Dynamic) of the model. You can also enable FP8 to reduce KV cache memory usage by 50% by adding `--kv-cache-dtype fp8` We served it on on 4 GPUs, but if you have 1 GPU, use `CUDA_VISIBLE_DEVICES='0'` and set `--tensor-parallel-size 1` or remove this argument. Use `tmux` to launch the below in a new terminal then CTRL+B+D - use `tmux attach-session -t0` to return back to it.

```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:False
CUDA_VISIBLE_DEVICES='0,1,2,3' vllm serve unsloth/Qwen3-Coder-Next-FP8-Dynamic \
    --served-model-name unsloth/Qwen3-Coder-Next \
    --tensor-parallel-size 4 \
    --tool-call-parser qwen3_coder \
    --enable-auto-tool-choice \
    --dtype bfloat16 \
    --seed 3407 \
    --max-model-len 200000 \
    --gpu-memory-utilization 0.93 \
    --port 8001
```

You should see something like below. See [#tool-calling-with-qwen3-coder-next](#tool-calling-with-qwen3-coder-next "mention") for how to actually use Qwen3-Coder-Next using the OpenAI API and tool calling - this works for vLLM and llama-server.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FxRdgnzg1gz3lBLPvftRx%2Fimage.png?alt=media&amp;token=4f43796b-397f-4ffb-86d2-68afd14994f9" alt=""><figcaption></figcaption></figure>

### :wrench:Tool Calling with Qwen3-Coder-Next

In a new terminal, we create some tools like adding 2 numbers, executing Python code, executing Linux functions and much more:

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

Now we'll showcase multiple methods of running tool-calling for many different use-cases below:

#### Execute generated Python code

{% code overflow="wrap" %}

```python
messages = [{
    "role": "user",
    "content": [{"type": "text", "text": "Create a Fibonacci function in Python and find fib(20)."}],
}]
unsloth_inference(messages, temperature = 1.0, top_p = 0.95, top_k = 40, min_p = 0.00)
```

{% endcode %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F7fY3LSeNCjHXNjBwQkbI%2Fimage.png?alt=media&amp;token=50eba62e-f8b2-424a-833b-be56696b4710" alt=""><figcaption></figcaption></figure>

#### Execute arbitrary terminal functions

{% code overflow="wrap" %}

```python
messages = [{
    "role": "user",
    "content": [{"type": "text", "text": "Write 'I'm a happy Sloth' to a file, then print it back to me."}],
}]
messages = unsloth_inference(messages, temperature = 1.0, top_p = 1.0, top_k = 40, min_p = 0.00)
```

{% endcode %}

We confirm the file was created and it was!

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FabplwVbEMlsCEJTmxzSA%2Fimage.png?alt=media&amp;token=eb27f30a-c91e-4aec-8fb0-f4a35921d3db" alt=""><figcaption></figcaption></figure>

See [Tool Calling Guide](/docs/basics/tool-calling-guide-for-local-llms.md) for more examples for tool calling.

## :triangular\_ruler:Benchmarks

### GGUF Quantization Benchmarks

Here are some quantization benchmarks conducted by third-party assessors.

<div><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FAc5D3rcKmF6NjlyoLCXJ%2Fqwen3-coder-next-oddly-usable-at-aggressive-quantization-v0-q9q4nsw11rkg1.webp?alt=media&amp;token=a92049ff-0bc2-4afa-a281-82bbacbfe42b" alt="" width="563"><figcaption><p>Aider Polyglot Benchmarks</p></figcaption></figure> <figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Ftbfnqq8ppzwFbeqPhnw0%2FHAfMRrrXQAALkQb.png?alt=media&amp;token=9730d4e1-3d4a-4ae6-92bf-32aa6724ab86" alt="" width="450"><figcaption><p>Benjamine Marie Benchmarks (<a href="https://x.com/bnjmn_marie/status/2019809651387514947/photo/1">Source</a>)</p></figcaption></figure></div>

{% columns %}
{% column %}
Benchmarks were run by third-party contributors on the Aider Polyglot server, comparing Unsloth GGUF quantizations on the Aider Polyglot benchmark (score vs. VRAM). Notably, the 3-bit **`UD-IQ3_XXS`** quant comes close to **BF16** performance, making **3-bit a sensible minimum** for most use cases.

**NVFP4** slightly outperforms the BF16 reference, which may be sampling noise due to limited runs; however, the overall pattern for: **1-bit → 2-bit → 3-bit → 6-bit** steadily improving, suggests the benchmark is capturing meaningful quality differences across Unsloth GGUFs. The **non-Unsloth** FP8 seems to perform worse than both **`UD-IQ3_XXS`** and **`UD-Q6_K_XL`**, which could reflect differences in the quantization pipeline or, again, insufficient sampling.
{% endcolumn %}

{% column %}
[Benjamin Marie (third-party) benchmarked](https://x.com/bnjmn_marie/status/2019809651387514947/photo/1) **Qwen3-Coder-Next** using Unsloth and Qwen GGUFs on a **750-prompt mixed suite** (LiveCodeBench v6, MMLU Pro, GPQA, Math500), reporting both **overall accuracy** and **relative error increase** (how much more often the quantized model makes mistakes vs. the original).

The graphs clearly show the Unsloth's Q4\_K\_M quants perform better than standard Q4\_K\_M. Q3\_K\_M expectedly performs worse on Live Code Bench v6, but surprisingly much better on HumanEval than standard Q4\_K\_M.\
\
It seems to run with the most efficiecy, using at least Q4\_K\_M is advised.
{% endcolumn %}
{% endcolumns %}

### Qwen3-Coder-Next Benchmarks

Qwen3-Coder-Next is the best performing model for its size, and its performance is comparable to models with 10–20× more active parameters.

<table data-full-width="true"><thead><tr><th>Benchmark</th><th align="right">Qwen3-Coder-Next (80B)</th><th align="right">DeepSeek-V3.2 (671B)</th><th align="right">GLM-4.7 (358B)</th><th align="right">MiniMax M2.1 (229B)</th></tr></thead><tbody><tr><td>SWE-Bench Verified (w/ SWE-Agent)</td><td align="right">70.6</td><td align="right">70.2</td><td align="right">74.2</td><td align="right">74.8</td></tr><tr><td>SWE-Bench Multilingual (w/ SWE-Agent)</td><td align="right">62.8</td><td align="right">62.3</td><td align="right">63.7</td><td align="right">66.2</td></tr><tr><td>SWE-Bench Pro (w/ SWE-Agent)</td><td align="right">44.3</td><td align="right">40.9</td><td align="right">40.6</td><td align="right">34.6</td></tr><tr><td>Terminal-Bench 2.0 (w/ Terminus-2 json)</td><td align="right">36.2</td><td align="right">39.3</td><td align="right">37.1</td><td align="right">32.6</td></tr><tr><td>Aider</td><td align="right">66.2</td><td align="right">69.9</td><td align="right">52.1</td><td align="right">61.0</td></tr></tbody></table>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F0M7glBoWyRQjHUgaVEev%2Fbenchmarks.png?alt=media&amp;token=d215bbcb-358e-41c4-9f27-66df8d3d94d8" alt=""><figcaption></figcaption></figure>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FKxPCUD7NhqHFwFcsmgfb%2Fswebench_pro.png?alt=media&amp;token=eb895603-6176-43d4-aa4d-9d127ef61381" alt="" width="563"><figcaption></figcaption></figure>

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FxsChrrfjcNVTXN2R0ZRL%2Fqwencodermas.png?alt=media&amp;token=081a28bb-003c-4c92-b086-e2bef1ab91c2" alt=""><figcaption></figcaption></figure>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/qwen3-coder-next.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
