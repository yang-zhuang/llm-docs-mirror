> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/deepseek-v3-0324-how-to-run-locally.md).

# DeepSeek-V3-0324: How to Run Locally

How to run DeepSeek-V3-0324 locally using our dynamic quants which recovers accuracy

{% hint style="info" %}
Please see <https://docs.unsloth.ai/basics/deepseek-r1-0528-how-to-run-locally> (May 28th 2025 update) to learn on how to run DeepSeek faster and more efficiently!
{% endhint %}

DeepSeek is at it again! After releasing V3, R1 Zero and R1 back in December 2024 and January 2025, DeepSeek updated their checkpoints / models for V3, and released a March update!

According to DeepSeek, MMLU-Pro jumped +5.3% to 81.2%. **GPQA +9.3% points**. AIME + 19.8% and LiveCodeBench + 10.0%! They provided a plot showing how they compared to the previous V3 checkpoint and other models like GPT 4.5 and Claude Sonnet 3.7. <mark style="background-color:blue;">**But how do we run a 671 billion parameter model locally?**</mark>

<table data-full-width="true"><thead><tr><th>MoE Bits</th><th>Type</th><th>Disk Size</th><th>Accuracy</th><th>Link</th><th>Details</th></tr></thead><tbody><tr><td>1.78bit</td><td>IQ1_S</td><td><strong>173GB</strong></td><td>Ok</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3-0324-GGUF/tree/main/UD-IQ1_S">Link</a></td><td>2.06/1.56bit</td></tr><tr><td>1.93bit</td><td>IQ1_M</td><td><strong>183GB</strong></td><td>Fair</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3-0324-GGUF/tree/main/UD-IQ1_M">Link</a></td><td>2.5/2.06/1.56</td></tr><tr><td>2.42bit</td><td>IQ2_XXS</td><td><strong>203GB</strong></td><td><mark style="background-color:blue;"><strong>Suggested</strong></mark></td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3-0324-GGUF/tree/main/UD-IQ2_XXS">Link</a></td><td>2.5/2.06bit</td></tr><tr><td>2.71bit</td><td>Q2_K_XL</td><td><strong>231GB</strong></td><td><mark style="background-color:purple;"><strong>Suggested</strong></mark></td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3-0324-GGUF/tree/main/UD-Q2_K_XL">Link</a></td><td>3.5/2.5bit</td></tr><tr><td>3.5bit</td><td>Q3_K_XL</td><td><strong>320GB</strong></td><td>Great</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3-0324-GGUF/tree/main/UD-Q3_K_XL">Link</a></td><td>4.5/3.5bit</td></tr><tr><td>4.5bit</td><td>Q4_K_XL</td><td><strong>406GB</strong></td><td>Best</td><td><a href="https://huggingface.co/unsloth/DeepSeek-V3-0324-GGUF/tree/main/UD-Q4_K_XL">Link</a></td><td>5.5/4.5bit</td></tr></tbody></table>

{% hint style="success" %}
DeepSeek V3's original upload is in float8, which takes 715GB. Using Q4\_K\_M halves the file size to 404GB or so, and our dynamic 1.78bit quant fits in around 151GB. **We suggest using our 2.7bit quant to balance size and accuracy! The 2.4bit one also works well!**
{% endhint %}

## :gear: Official Recommended Settings

According to [DeepSeek](https://huggingface.co/deepseek-ai/DeepSeek-V3-0324), these are the recommended settings for inference:

* <mark style="background-color:blue;">**Temperature of 0.3**</mark> (Maybe 0.0 for coding as [seen here](https://api-docs.deepseek.com/quick_start/parameter_settings))
* Min\_P of 0.00 (optional, but 0.01 works well, llama.cpp default is 0.1)
* Chat template: `<｜User｜>Create a simple playable Flappy Bird Game in Python. Place the final game inside of a markdown section.<｜Assistant｜>`
* A BOS token of `<｜begin▁of▁sentence｜>` is auto added during tokenization (do NOT add it manually!)
* DeepSeek mentioned using a <mark style="background-color:green;">**system prompt**</mark> as well (optional) - it's in Chinese: `该助手为DeepSeek Chat，由深度求索公司创造。\n今天是3月24日，星期一。` which translates to: `The assistant is DeepSeek Chat, created by DeepSeek.\nToday is Monday, March 24th.`
* <mark style="background-color:orange;">**For KV cache quantization, use 8bit, NOT 4bit - we found it to do noticeably worse.**</mark>

## 📖 Tutorial: How to Run DeepSeek-V3 in llama.cpp

1. Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

{% hint style="warning" %}
NOTE using `-DGGML_CUDA=ON` for GPUs might take 5 minutes to compile. CPU only takes 1 minute to compile. You might be interested in llama.cpp's precompiled binaries.
{% endhint %}

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

2. Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose `UD-IQ1_S`(dynamic 1.78bit quant) or other quantized versions like `Q4_K_M` . <mark style="background-color:green;">**I recommend using our 2.7bit dynamic quant**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**`UD-Q2_K_XL`**</mark><mark style="background-color:green;">**&#x20;**</mark><mark style="background-color:green;">**to balance size and accuracy**</mark>. More versions at: <https://huggingface.co/unsloth/DeepSeek-V3-0324-GGUF>

{% code overflow="wrap" %}

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/DeepSeek-V3-0324-GGUF-UD",
    local_dir = "unsloth/DeepSeek-V3-0324-GGUF-UD",
    allow_patterns = ["*UD-Q2_K_XL*"], # Dynamic 2.7bit (230GB) Use "*UD-IQ_S*" for Dynamic 1.78bit (151GB)
)
```

{% endcode %}

3. Run Unsloth's Flappy Bird test as described in our 1.58bit Dynamic Quant for DeepSeek R1.
4. Edit `--threads 32` for the number of CPU threads, `--ctx-size 16384` for context length, `--n-gpu-layers 2` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.

<pre class="language-bash" data-overflow="wrap"><code class="lang-bash">./llama.cpp/llama-cli \
    --model unsloth/DeepSeek-V3-0324-GGUF-UD/blob/main/UD-Q2_K_XL/DeepSeek-V3-0324-UD-Q2_K_XL-00001-of-00006.gguf \
    <a data-footnote-ref href="#user-content-fn-1">--cache-type-k q8_0 </a>\
    <a data-footnote-ref href="#user-content-fn-2">--threads 20</a> \
    <a data-footnote-ref href="#user-content-fn-3">--n-gpu-layers 2</a> \
    -no-cnv \
    --prio 3 \
    --temp 0.3 \
    --min-p 0.01 \
    <a data-footnote-ref href="#user-content-fn-4">--ctx-size 4096</a> \
    --seed 3407 \
    --prompt "&#x3C;｜User｜>Create a Flappy Bird game in Python. You must include these things:\n1. You must use pygame.\n2. The background color should be randomly chosen and is a light shade. Start with a light blue color.\n3. Pressing SPACE multiple times will accelerate the bird.\n4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.\n5. Place on the bottom some land colored as dark brown or yellow chosen randomly.\n6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.\n7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.\n8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.\nThe final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.&#x3C;｜Assistant｜>"
</code></pre>

<details>

<summary>If we run the above, we get 2 very different results.<br><br><strong>Standard 2-bit version:</strong> Click to view result <em><mark style="color:red;"><strong>(seizure warning!)</strong></mark></em><br><strong>Dynamic 2-bit version:</strong> See the result below:</summary>

<img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-5ab85f63c9fb12f0ce701dd3cfd540aa1503a636%2FOld.gif?alt=media" alt="" data-size="original">

Standard 2-bit. Fails with background, fails with collision

</details>

<div align="center"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-97735d09e3d399cf74f8e7112eef8ca56b0e10e9%2FNew.gif?alt=media" alt="" width="240"><figcaption><p>Dynamic 2-bit. Succeeds in creating a playable game.</p></figcaption></figure></div>

5. Like DeepSeek-R1, V3 has 61 layers. For example with a 24GB GPU or 80GB GPU, you can expect to offload after rounding down (reduce by 1 if it goes out of memory):

| Quant   | File Size | 24GB GPU | 80GB GPU | 2x80GB GPU |
| ------- | --------- | -------- | -------- | ---------- |
| 1.73bit | 173GB     | 5        | 25       | 56         |
| 2.22bit | 183GB     | 4        | 22       | 49         |
| 2.51bit | 212GB     | 2        | 19       | 32         |

### Running on Mac / Apple devices

For Apple Metal devices, be careful of `--n-gpu-layers`. If you find the machine going out of memory, reduce it. For a 128GB unified memory machine, you should be able to offload 59 layers or so.

```bash
./llama.cpp/llama-cli \
    --model DeepSeek-R1-GGUF/DeepSeek-V3-0324-UD-IQ1_S/DeepSeek-V3-0324-UD-IQ1_S-00001-of-00003.gguf \
    --cache-type-k q4_0 \
    --threads 16 \
    --prio 2 \
    --temp 0.6 \
    --ctx-size 8192 \
    --seed 3407 \
    --n-gpu-layers 59 \
    -no-cnv \
    --prompt "<｜User｜>Create a Flappy Bird game in Python.<｜Assistant｜>"
```

## :8ball: Heptagon Test

We also test our dynamic quants via [r/Localllama](https://www.reddit.com/r/LocalLLaMA/comments/1j7r47l/i_just_made_an_animation_of_a_ball_bouncing/) which tests the model on creating a basic physics engine to simulate balls rotating in a moving enclosed heptagon shape.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-1371de5a93c6c5b0e43e8bb51980d84554b199f4%2Fsnapshot.jpg?alt=media" alt="" width="563"><figcaption><p>The goal is to make the heptagon spin, and the balls in the heptagon should move.</p></figcaption></figure>

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli \
    --model unsloth/DeepSeek-V3-0324-GGUF-UD/blob/main/UD-Q2_K_XL/DeepSeek-V3-0324-UD-Q2_K_XL-00001-of-00006.gguf \
    --cache-type-k q8_0 \
    --threads 20 \
    --n-gpu-layers 2 \
    -no-cnv \
    --prio 3 \
    --temp 0.3 \
    --min-p 0.01 \
    --ctx-size 4096 \
    --seed 3407 \
    --prompt "<｜User｜>Write a Python program that shows 20 balls bouncing inside a spinning heptagon:\n- All balls have the same radius.\n- All balls have a number on it from 1 to 20.\n- All balls drop from the heptagon center when starting.\n- Colors are: #f8b862, #f6ad49, #f39800, #f08300, #ec6d51, #ee7948, #ed6d3d, #ec6800, #ec6800, #ee7800, #eb6238, #ea5506, #ea5506, #eb6101, #e49e61, #e45e32, #e17b34, #dd7a56, #db8449, #d66a35\n- The balls should be affected by gravity and friction, and they must bounce off the rotating walls realistically. There should also be collisions between balls.\n- The material of all the balls determines that their impact bounce height will not exceed the radius of the heptagon, but higher than ball radius.\n- All balls rotate with friction, the numbers on the ball can be used to indicate the spin of the ball.\n- The heptagon is spinning around its center, and the speed of spinning is 360 degrees per 5 seconds.\n- The heptagon size should be large enough to contain all the balls.\n- Do not use the pygame library; implement collision detection algorithms and collision response etc. by yourself. The following Python libraries are allowed: tkinter, math, numpy, dataclasses, typing, sys.\n- All codes should be put in a single Python file.<｜Assistant｜>"
```

{% endcode %}

<table data-view="cards"><thead><tr><th></th><th data-type="files"></th><th data-hidden data-card-cover data-type="files"></th></tr></thead><tbody><tr><td>Non Dynamic 2bit. Fails - <mark style="background-color:red;">SEIZURE WARNING</mark> again!</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-0e0d101cc282b869a97fc679da5a9e98141c6f62%2Funsloth-q2_k_rotate.txt?alt=media">unsloth-q2_k_rotate.txt</a></td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-d2579e8d1145572548ed69b0e335925f47130ba3%2FInShot_20250325_185636426.gif?alt=media">InShot_20250325_185636426.gif</a></td></tr><tr><td>Dynamic 2bit. Actually solves the heptagon puzzle correctly!!</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-96202dad58c0d0004cdb51408332ac78b425138f%2Funsloth-q2_k_xl_rotate.txt?alt=media">unsloth-q2_k_xl_rotate.txt</a></td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-669f5b08b6bf220a38dce445d4830fcd80d52be3%2FInShot_20250325_181710554.gif?alt=media">InShot_20250325_181710554.gif</a></td></tr><tr><td>Original float8</td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-902430fe71d14f19cd31d3fe271f9a636e91304e%2Ffp8-heptagon.txt?alt=media">fp8-heptagon.txt</a></td><td><a href="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-4501a6aef616d02057b89e96baa9c1d5ed57666f%2FInShot_20250325_181423756.gif?alt=media">InShot_20250325_181423756.gif</a></td></tr></tbody></table>

The dynamic 2.7 bit quant which is only 230GB in size actually manages to solve the heptagon puzzle! The full output for all 3 versions (including full fp8) is below:

<details>

<summary>Dynamic 2bit Heptagon code</summary>

```python
import tkinter as tk
import math
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Constants
HEPTAGON_RADIUS = 300
BALL_RADIUS = 20
GRAVITY = 0.2
FRICTION = 0.99
BOUNCE_FACTOR = 0.8
ROTATION_SPEED = 360 / 5  # degrees per second
SPIN_FRICTION = 0.98
BALL_COLORS = [
    "#f8b862", "#f6ad49", "#f39800", "#f08300", "#ec6d51",
    "#ee7948", "#ed6d3d", "#ec6800", "#ec6800", "#ee7800",
    "#eb6238", "#ea5506", "#ea5506", "#eb6101", "#e49e61",
    "#e45e32", "#e17b34", "#dd7a56", "#db8449", "#d66a35"
]

@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    number: int
    spin: float = 0.0
    color: str = "#000000"

@dataclass
class Wall:
    x1: float
    y1: float
    x2: float
    y2: float

class BouncingBalls:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=800, bg="white")
        self.canvas.pack()
        self.balls: List[Ball] = []
        self.walls: List[Wall] = []
        self.heptagon_angle = 0
        self.last_time = 0
        
        self.setup_balls()
        self.setup_heptagon()
        
        self.root.after(16, self.update)
        self.root.bind("<space>", self.reset_balls)
    
    def setup_balls(self):
        for i in range(20):
            ball = Ball(
                x=400,
                y=400,
                vx=np.random.uniform(-5, 5),
                vy=np.random.uniform(-5, 5),
                number=i+1,
                color=BALL_COLORS[i]
            )
            self.balls.append(ball)
    
    def setup_heptagon(self):
        # Create initial heptagon walls
        self.update_heptagon_walls(0)
    
    def update_heptagon_walls(self, angle):
        self.walls = []
        center_x, center_y = 400, 400
        angle_rad = math.radians(angle)
        
        for i in range(7):
            angle1 = angle_rad + 2 * math.pi * i / 7
            angle2 = angle_rad + 2 * math.pi * (i + 1) / 7
            
            x1 = center_x + HEPTAGON_RADIUS * math.cos(angle1)
            y1 = center_y + HEPTAGON_RADIUS * math.sin(angle1)
            x2 = center_x + HEPTAGON_RADIUS * math.cos(angle2)
            y2 = center_y + HEPTAGON_RADIUS * math.sin(angle2)
            
            self.walls.append(Wall(x1, y1, x2, y2))
    
    def reset_balls(self, event=None):
        for ball in self.balls:
            ball.x = 400
            ball.y = 400
            ball.vx = np.random.uniform(-5, 5)
            ball.vy = np.random.uniform(-5, 5)
            ball.spin = np.random.uniform(-5, 5)
    
    def update(self):
        current_time = self.root.after_idle(self.root.after, 16, self.update)
        if self.last_time == 0:
            self.last_time = current_time
            return
        
        # Calculate delta time (approximate)
        dt = 0.016  # Assuming ~60 FPS
        
        # Update heptagon rotation
        self.heptagon_angle += ROTATION_SPEED * dt
        self.update_heptagon_walls(self.heptagon_angle)
        
        # Update balls
        for ball in self.balls:
            # Apply gravity
            ball.vy += GRAVITY
            
            # Apply friction
            ball.vx *= FRICTION
            ball.vy *= FRICTION
            ball.spin *= SPIN_FRICTION
            
            # Move ball
            ball.x += ball.vx
            ball.y += ball.vy
            
            # Check collisions with walls
            self.check_wall_collisions(ball)
            
            # Check collisions with other balls
            for other in self.balls:
                if other.number != ball.number:
                    self.check_ball_collision(ball, other)
        
        # Draw everything
        self.draw()
    
    def check_wall_collisions(self, ball):
        for wall in self.walls:
            # Find closest point on wall segment to ball
            closest = self.closest_point_on_segment(
                wall.x1, wall.y1, wall.x2, wall.y2, ball.x, ball.y
            )
            
            # Calculate distance to wall
            dx = ball.x - closest[0]
            dy = ball.y - closest[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < BALL_RADIUS:
                # Collision detected
                # Calculate normal vector
                nx = dx / distance
                ny = dy / distance
                
                # Calculate relative velocity along normal
                v_rel = ball.vx * nx + ball.vy * ny
                
                if v_rel < 0:  # Moving toward the wall
                    # Calculate impulse
                    j = -(1 + BOUNCE_FACTOR) * v_rel
                    
                    # Apply impulse
                    ball.vx += j * nx
                    ball.vy += j * ny
                    
                    # Add some spin based on collision
                    ball.spin += (ball.vx * ny - ball.vy * nx) * 0.1
                    
                    # Move ball out of collision
                    penetration = BALL_RADIUS - distance
                    ball.x += penetration * nx
                    ball.y += penetration * ny
    
    def check_ball_collision(self, ball1, ball2):
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < 2 * BALL_RADIUS:
            # Collision detected
            nx = dx / distance
            ny = dy / distance
            
            # Calculate relative velocity
            v_rel_x = ball2.vx - ball1.vx
            v_rel_y = ball2.vy - ball1.vy
            v_rel = v_rel_x * nx + v_rel_y * ny
            
            if v_rel < 0:  # Moving toward each other
                # Calculate impulse
                j = -(1 + BOUNCE_FACTOR) * v_rel / 2
                
                # Apply impulses
                ball1.vx -= j * nx
                ball1.vy -= j * ny
                ball2.vx += j * nx
                ball2.vy += j * ny
                
                # Add spin based on collision
                ball1.spin += (ball1.vx * ny - ball1.vy * nx) * 0.05
                ball2.spin += (ball2.vx * ny - ball2.vy * nx) * 0.05
                
                # Move balls apart
                penetration = 2 * BALL_RADIUS - distance
                ball1.x -= penetration * nx * 0.5
                ball1.y -= penetration * ny * 0.5
                ball2.x += penetration * nx * 0.5
                ball2.y += penetration * ny * 0.5
    
    @staticmethod
    def closest_point_on_segment(x1, y1, x2, y2, x, y):
        # Vector from point to segment start
        dx = x - x1
        dy = y - y1
        
        # Segment vector
        sx = x2 - x1
        sy = y2 - y1
        
        # Projection of point onto segment
        dot = dx * sx + dy * sy
        len_sq = sx * sx + sy * sy
        param = dot / len_sq if len_sq != 0 else -1
        
        if param < 0:
            return x1, y1
        elif param > 1:
            return x2, y2
        else:
            return x1 + param * sx, y1 + param * sy
    
    def draw(self):
        self.canvas.delete("all")
        
        # Draw heptagon
        points = []
        for wall in self.walls:
            points.extend([wall.x1, wall.y1])
        self.canvas.create_polygon(points, fill="", outline="black", width=2)
        
        # Draw balls
        for ball in self.balls:
            # Draw ball
            self.canvas.create_oval(
                ball.x - BALL_RADIUS, ball.y - BALL_RADIUS,
                ball.x + BALL_RADIUS, ball.y + BALL_RADIUS,
                fill=ball.color, outline="black"
            )
            
            # Draw number with rotation based on spin
            angle = ball.spin * 10  # Scale spin for visual effect
            self.canvas.create_text(
                ball.x, ball.y,
                text=str(ball.number),
                font=("Arial", 12, "bold"),
                angle=angle
            )

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bouncing Balls in Spinning Heptagon")
    app = BouncingBalls(root)
    root.mainloop()
```

</details>

<details>

<summary>Non Dynamic 2bit Heptagon code</summary>

```python
import tkinter as tk
import math
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional
import sys

# Constants
WIDTH, HEIGHT = 800, 800
HEPTAGON_RADIUS = 300
BALL_RADIUS = 15
GRAVITY = 0.5
FRICTION = 0.999
ELASTICITY = 0.8
ROTATION_SPEED = 2 * math.pi / 5  # 360 degrees per 5 seconds
SPIN_DECAY = 0.99

# Colors for the balls
BALL_COLORS = [
    "#f8b862", "#f6ad49", "#f39800", "#f08300", "#ec6d51",
    "#ee7948", "#ed6d3d", "#ec6800", "#ec6800", "#ee7800",
    "#eb6238", "#ea5506", "#ea5506", "#eb6101", "#e49e61",
    "#e45e32", "#e17b34", "#dd7a56", "#db8449", "#d66a35"
]

@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    radius: float
    color: str
    number: int
    spin: float = 0.0

@dataclass
class Heptagon:
    center_x: float
    center_y: float
    radius: float
    angle: float = 0.0

class BouncingBalls:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()
        
        self.heptagon = Heptagon(WIDTH//2, HEIGHT//2, HEPTAGON_RADIUS)
        self.balls = []
        self.setup_balls()
        
        self.root.after(0, self.update)
        self.root.mainloop()
    
    def setup_balls(self):
        center_x, center_y = WIDTH//2, HEIGHT//2
        for i in range(20):
            self.balls.append(Ball(
                x=center_x,
                y=center_y,
                vx=0,
                vy=0,
                radius=BALL_RADIUS,
                color=BALL_COLORS[i],
                number=i+1,
                spin=0
            ))
    
    def update(self):
        self.canvas.delete("all")
        
        # Update heptagon angle
        self.heptagon.angle += ROTATION_SPEED / 60  # Assuming 60 FPS
        
        # Draw heptagon
        self.draw_heptagon()
        
        # Update and draw balls
        for ball in self.balls:
            # Apply gravity
            ball.vy += GRAVITY
            
            # Update position
            ball.x += ball.vx
            ball.y += ball.vy
            
            # Apply friction
            ball.vx *= FRICTION
            ball.vy *= FRICTION
            
            # Apply spin decay
            ball.spin *= SPIN_DECAY
            
            # Check collision with heptagon walls
            self.check_heptagon_collision(ball)
            
            # Check collision with other balls
            for other in self.balls:
                if other != ball:
                    if self.check_ball_collision(ball, other):
                        self.resolve_ball_collision(ball, other)
            
            # Draw the ball
            self.draw_ball(ball)
        
        self.root.after(16, self.update)  # ~60 FPS
    
    def draw_heptagon(self):
        center_x, center_y = self.heptagon.center_x, self.heptagon.center_y
        points = []
        for i in range(7):
            angle = self.heptagon.angle + i * 2 * math.pi / 7
            x = center_x + self.heptagon.radius * math.cos(angle)
            y = center_y + self.heptagon.radius * math.sin(angle)
            points.append((x, y))
        
        # Draw heptagon
        self.canvas.create_polygon(
            [points[0], points[1], points[2], points[3], 
             points[4], points[5], points[6]],
            outline="black", fill="", width=2
        )
    
    def draw_ball(self, ball):
        self.canvas.create_oval(
            ball.x - ball.radius,
            ball.y - ball.radius,
            ball.x + ball.radius,
            ball.y + ball.radius,
            fill=ball.color,
            outline="black"
        )
        
        # Draw the number
        self.canvas.create_text(
            ball.x, ball.y,
            text=str(ball.number),
            fill="black"
        )
    
    def check_heptagon_collision(self, ball):
        center_x, center_y = WIDTH//2, HEIGHT//2
        
        # Check distance from center
        dx = ball.x - center_x
        dy = ball.y - center_y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist + ball.radius > self.heptagon.radius:
            # Find the normal vector from center to ball
            angle = math.atan2(dy, dx)
            normal_x = math.cos(angle)
            normal_y = math.sin(angle)
            
            # Move ball back inside heptagon
            overlap = (dist + ball.radius) - self.heptagon.radius
            ball.x -= overlap * normal_x
            ball.y -= overlap * normal_y
            
            # Reflect velocity
            dot_product = ball.vx * normal_x + ball.vy * normal_y
            ball.vx -= 2 * dot_product * normal_x * ELASTICITY
            ball.vy -= 2 * dot_product * normal_y * ELASTICITY
    
    def check_ball_collision(self, ball1, ball2):
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y
        distance = math.sqrt(dx**2 + dy**2)
        return distance < (ball1.radius + ball2.radius)
    
    def resolve_ball_collision(self, ball1, ball2):
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Normal vector
        nx = dx / distance
        ny = dy / distance
        
        # Relative velocity
        dvx = ball2.vx - ball1.vx
        dvy = ball2.vy - ball1.vy
        
        # Calculate impulse
        impulse = 2 * (dvx * nx + dvy * ny) / 2
        impulse *= ELASTICITY
        
        # Apply impulse
        ball1.vx -= impulse * nx
        ball1.vy -= impulse * ny
        ball2.vx += impulse * nx
        ball2.vy += impulse * ny
        
        # Separate the balls to prevent sticking
        overlap = (ball1.radius + ball2.radius) - distance
        ball1.x -= overlap * nx / 2
        ball1.y -= overlap * ny / 2
        ball2.x += overlap * nx / 2
        ball2.y += overlap * ny / 2
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bouncing Balls in a Spinning Heptagon")
    app = BouncingBalls(root)
    app.run()
```

</details>

<details>

<summary>Float8 Heptagon code</summary>

```python
import tkinter as tk
import math
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Constants
WIDTH, HEIGHT = 800, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
GRAVITY = 0.2
FRICTION = 0.99
BALL_RADIUS = 15
HEPTAGON_RADIUS = 300
ROTATION_SPEED = 360 / 5  # degrees per second
ELASTICITY = 0.8
SPIN_FRICTION = 0.98

# Colors for the balls
BALL_COLORS = [
    '#f8b862', '#f6ad49', '#f39800', '#f08300', '#ec6d51',
    '#ee7948', '#ed6d3d', '#ec6800', '#ec6800', '#ee7800',
    '#eb6238', '#ea5506', '#ea5506', '#eb6101', '#e49e61',
    '#e45e32', '#e17b34', '#dd7a56', '#db8449', '#d66a35'
]

@dataclass
class Ball:
    x: float
    y: float
    vx: float
    vy: float
    radius: float
    color: str
    number: int
    spin: float = 0.0

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += GRAVITY
        self.vx *= FRICTION
        self.vy *= FRICTION
        self.spin *= SPIN_FRICTION

    def collide_with_ball(self, other: 'Ball'):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.hypot(dx, dy)
        
        if distance < self.radius + other.radius:
            # Calculate collision normal
            nx = dx / distance
            ny = dy / distance
            
            # Calculate relative velocity
            dvx = other.vx - self.vx
            dvy = other.vy - self.vy
            
            # Calculate impulse
            impulse = 2 * (dvx * nx + dvy * ny) / (1/self.radius + 1/other.radius)
            
            # Apply impulse
            self.vx += impulse * nx / self.radius
            self.vy += impulse * ny / self.radius
            other.vx -= impulse * nx / other.radius
            other.vy -= impulse * ny / other.radius
            
            # Separate balls to prevent sticking
            overlap = (self.radius + other.radius - distance) / 2
            self.x -= overlap * nx
            self.y -= overlap * ny
            other.x += overlap * nx
            other.y += overlap * ny
            
            # Transfer some spin
            transfer = impulse * 0.01
            self.spin -= transfer
            other.spin += transfer

class HeptagonBounceSimulator:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
        self.canvas.pack()
        
        self.balls = self.create_balls()
        self.heptagon_angle = 0
        self.last_time = 0
        self.running = True
        
        self.root.bind('<space>', self.toggle_pause)
        self.root.bind('<Escape>', lambda e: root.destroy())
        
        self.last_time = self.root.after(0, self.update)
    
    def create_balls(self) -> List[Ball]:
        balls = []
        for i in range(20):
            # Start all balls at center with small random velocity
            angle = np.random.uniform(0, 2 * math.pi)
            speed = np.random.uniform(0.5, 2)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            balls.append(Ball(
                x=CENTER_X,
                y=CENTER_Y,
                vx=vx,
                vy=vy,
                radius=BALL_RADIUS,
                color=BALL_COLORS[i],
                number=i+1,
                spin=np.random.uniform(-2, 2)
            ))
        return balls
    
    def toggle_pause(self, event):
        self.running = not self.running
        if self.running:
            self.last_time = self.root.after(0, self.update)
    
    def get_heptagon_vertices(self) -> List[Tuple[float, float]]:
        vertices = []
        for i in range(7):
            angle = math.radians(self.heptagon_angle + i * 360 / 7)
            x = CENTER_X + HEPTAGON_RADIUS * math.cos(angle)
            y = CENTER_Y + HEPTAGON_RADIUS * math.sin(angle)
            vertices.append((x, y))
        return vertices
    
    def check_ball_heptagon_collision(self, ball: Ball):
        vertices = self.get_heptagon_vertices()
        closest_dist = float('inf')
        closest_normal = (0, 0)
        closest_edge = None
        
        # Check collision with each edge of the heptagon
        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]
            
            # Vector from p1 to p2
            edge_x = p2[0] - p1[0]
            edge_y = p2[1] - p1[1]
            edge_length = math.hypot(edge_x, edge_y)
            
            # Normalize edge vector
            edge_x /= edge_length
            edge_y /= edge_length
            
            # Normal vector (perpendicular to edge, pointing inward)
            nx = -edge_y
            ny = edge_x
            
            # Vector from p1 to ball
            ball_to_p1_x = ball.x - p1[0]
            ball_to_p1_y = ball.y - p1[1]
            
            # Project ball onto edge normal
            projection = ball_to_p1_x * nx + ball_to_p1_y * ny
            
            # If projection is negative, ball is outside the heptagon
            if projection < ball.radius:
                # Find closest point on edge to ball
                edge_proj = ball_to_p1_x * edge_x + ball_to_p1_y * edge_y
                edge_proj = max(0, min(edge_length, edge_proj))
                closest_x = p1[0] + edge_proj * edge_x
                closest_y = p1[1] + edge_proj * edge_y
                
                # Distance from ball to closest point on edge
                dist = math.hypot(ball.x - closest_x, ball.y - closest_y)
                
                if dist < closest_dist:
                    closest_dist = dist
                    closest_normal = (nx, ny)
                    closest_edge = (p1, p2)
        
        if closest_dist < ball.radius:
            # Calculate bounce response
            dot_product = ball.vx * closest_normal[0] + ball.vy * closest_normal[1]
            
            # Apply bounce with elasticity
            ball.vx -= (1 + ELASTICITY) * dot_product * closest_normal[0]
            ball.vy -= (1 + ELASTICITY) * dot_product * closest_normal[1]
            
            # Add some spin based on impact
            edge_vec = (closest_edge[1][0] - closest_edge[0][0], 
                        closest_edge[1][1] - closest_edge[0][1])
            edge_length = math.hypot(edge_vec[0], edge_vec[1])
            if edge_length > 0:
                edge_vec = (edge_vec[0]/edge_length, edge_vec[1]/edge_length)
                # Cross product of velocity and edge direction
                spin_effect = (ball.vx * edge_vec[1] - ball.vy * edge_vec[0]) * 0.1
                ball.spin += spin_effect
            
            # Move ball outside the heptagon to prevent sticking
            penetration = ball.radius - closest_dist
            ball.x += penetration * closest_normal[0]
            ball.y += penetration * closest_normal[1]
    
    def update(self):
        if not self.running:
            return
        
        # Clear canvas
        self.canvas.delete('all')
        
        # Update heptagon rotation
        self.heptagon_angle += ROTATION_SPEED / 60  # Assuming ~60 FPS
        
        # Draw heptagon
        vertices = self.get_heptagon_vertices()
        self.canvas.create_polygon(vertices, outline='black', fill='', width=2)
        
        # Update and draw balls
        for i, ball in enumerate(self.balls):
            # Move ball
            ball.move()
            
            # Check collisions with heptagon
            self.check_ball_heptagon_collision(ball)
            
            # Draw ball
            self.canvas.create_oval(
                ball.x - ball.radius, ball.y - ball.radius,
                ball.x + ball.radius, ball.y + ball.radius,
                fill=ball.color, outline='black'
            )
            
            # Draw number with rotation based on spin
            angle = ball.spin * 10  # Scale spin for visible rotation
            self.canvas.create_text(
                ball.x, ball.y,
                text=str(ball.number),
                font=('Arial', 10, 'bold'),
                angle=angle
            )
        
        # Check ball-ball collisions
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                self.balls[i].collide_with_ball(self.balls[j])
        
        # Schedule next update
        self.last_time = self.root.after(16, self.update)  # ~60 FPS

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Bouncing Balls in a Spinning Heptagon')
    simulator = HeptagonBounceSimulator(root)
    root.mainloop()
```

</details>

## :detective: Extra Findings & Tips

1. We find using lower KV cache quantization (4bit) seems to degrade generation quality via empirical tests - more tests need to be done, but we suggest using `q8_0` cache quantization. The goal of quantization is to support longer context lengths since the KV cache uses quite a bit of memory.
2. We found the `down_proj` in this model to be extremely sensitive to quantitation. We had to redo some of our dyanmic quants which used 2bits for `down_proj` and now we use 3bits as the minimum for all these matrices.
3. Using `llama.cpp` 's Flash Attention backend does result in somewhat faster decoding speeds. Use `-DGGML_CUDA_FA_ALL_QUANTS=ON` when compiling. Note it's also best to set your CUDA architecture as found in <https://developer.nvidia.com/cuda-gpus> to reduce compilation times, then set it via `-DCMAKE_CUDA_ARCHITECTURES="80"`
4. Using a `min_p=0.01`is probably enough. `llama.cpp`defaults to 0.1, which is probably not necessary. Since a temperature of 0.3 is used anyways, we most likely will very unlikely sample low probability tokens, so removing very unlikely tokens is a good idea. DeepSeek recommends 0.0 temperature for coding tasks.

[^1]: MUST USE 8bit - not 4bit

[^2]: CPU threads your machine has

[^3]: Approx 2 for 24GB GPU. Approx 18 for 80GB GPU.

[^4]: Context length


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/deepseek-v3-0324-how-to-run-locally.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
