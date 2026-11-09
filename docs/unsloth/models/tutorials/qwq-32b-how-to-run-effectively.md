> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/qwq-32b-how-to-run-effectively.md).

# QwQ-32B: How to Run effectively

How to run QwQ-32B effectively with our bug fixes and without endless generations + GGUFs.

Qwen released QwQ-32B - a reasoning model with performance comparable to DeepSeek-R1 on many [benchmarks](https://qwenlm.github.io/blog/qwq-32b/). However, people have been experiencing **infinite generations**, **many repetitions**, \<think> token issues and finetuning issues. We hope this guide will help debug and fix most issues!

{% hint style="info" %}
Our model uploads with our bug fixes work great for fine-tuning, vLLM and Transformers. If you're using llama.cpp and engines that use llama.cpp as backend, follow our [instructions here](#tutorial-how-to-run-qwq-32b) to fix endless generations.
{% endhint %}

**Unsloth QwQ-32B uploads with our bug fixes:**

| [GGUF](https://huggingface.co/unsloth/QwQ-32B-GGUF) | [Dynamic 4-bit](https://huggingface.co/unsloth/QwQ-32B-unsloth-bnb-4bit) | [BnB 4-bit](https://huggingface.co/unsloth/QwQ-32B-bnb-4bit) | [16-bit](https://huggingface.co/unsloth/QwQ-32B) |
| --------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------ |

## :gear: Official Recommended Settings

According to [Qwen](https://huggingface.co/Qwen/QwQ-32B), these are the recommended settings for inference:

* Temperature of 0.6
* Top\_K of 40 (or 20 to 40)
* Min\_P of 0.00 (optional, but 0.01 works well, llama.cpp default is 0.1)
* Top\_P of 0.95
* Repetition Penalty of 1.0. (1.0 means disabled in llama.cpp and transformers)
* Chat template: `<|im_start|>user\nCreate a Flappy Bird game in Python.<|im_end|>\n<|im_start|>assistant\n<think>\n`

{% hint style="warning" %}
`llama.cpp` uses `min_p = 0.1`by default, which might cause issues. Force it to 0.0.
{% endhint %}

## :thumbsup: Recommended settings for llama.cpp

We noticed many people use a `Repetition Penalty` greater than 1.0. For example 1.1 to 1.5. This actually interferes with llama.cpp's sampling mechanisms. The goal of a repetition penalty is to penalize repeated generations, but we found this doesn't work as expected.

Turning off `Repetition Penalty` also works (ie setting it to 1.0), but we found using it to be useful to penalize endless generations.

To use it, we found you must also edit the ordering of samplers in llama.cpp to before applying `Repetition Penalty`, otherwise there will be endless generations. So add this:

```bash
--samplers "top_k;top_p;min_p;temperature;dry;typ_p;xtc"
```

By default, llama.cpp uses this ordering:

```bash
--samplers "dry;top_k;typ_p;top_p;min_p;xtc;temperature"
```

We reorder essentially temperature and dry, and move min\_p forward. This means we apply samplers in this order:

```bash
top_k=40
top_p=0.95
min_p=0.0
temperature=0.6
dry
typ_p
xtc
```

If you still encounter issues, you can increase the`--repeat-penalty 1.0 to 1.2 or 1.3.`

Courtesy to [@krist486](https://x.com/krist486/status/1897885598196654180) for bringing llama.cpp sampling directions to my attention.

## :sunny: Dry Repetition Penalty

We investigated usage of `dry penalty` as suggested in <https://github.com/ggml-org/llama.cpp/blob/master/examples/main/README.md> using a value of 0.8, but we actually found this to **rather cause syntax issues especially for coding**. If you still encounter issues, you can increase the`dry penalty to 0.8.`

Utilizing our swapped sampling ordering can also help if you decide to use `dry penalty`.

## :llama: Tutorial: How to Run QwQ-32B in Ollama

1. Install `ollama` if you haven't already!

```bash
apt-get update
apt-get install pciutils -y
curl -fsSL https://ollama.com/install.sh | sh
```

2. Run run the model! Note you can call `ollama serve`in another terminal if it fails! We include all our fixes and suggested parameters (temperature, min\_p etc) in `param` in our Hugging Face upload!

```bash
ollama run hf.co/unsloth/QwQ-32B-GGUF:Q4_K_M
```

## 📖 Tutorial: How to Run QwQ-32B in llama.cpp

1. Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=ON -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split
cp llama.cpp/build/bin/llama-* llama.cpp
```

2. Download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose Q4\_K\_M, or other quantized versions (like BF16 full precision). More versions at: <https://huggingface.co/unsloth/QwQ-32B-GGUF>

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/QwQ-32B-GGUF",
    local_dir = "unsloth-QwQ-32B-GGUF",
    allow_patterns = ["*Q4_K_M*"], # For Q4_K_M
)
```

3. Run Unsloth's Flappy Bird test, which will save the output to `Q4_K_M_yes_samplers.txt`
4. Edit `--threads 32` for the number of CPU threads, `--ctx-size 16384` for context length, `--n-gpu-layers 99` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference.
5. We use `--repeat-penalty 1.1` and `--dry-multiplier 0.5` which you can adjust.

```bash
./llama.cpp/llama-cli \
    --model unsloth-QwQ-32B-GGUF/QwQ-32B-Q4_K_M.gguf \
    --threads 32 \
    --ctx-size 16384 \
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.6 \
    --repeat-penalty 1.1 \
    --dry-multiplier 0.5 \
    --min-p 0.01 \
    --top-k 40 \
    --top-p 0.95 \
    -no-cnv \
    --samplers "top_k;top_p;min_p;temperature;dry;typ_p;xtc" \
    --prompt "<|im_start|>user\nCreate a Flappy Bird game in Python. You must include these things:\n1. You must use pygame.\n2. The background color should be randomly chosen and is a light shade. Start with a light blue color.\n3. Pressing SPACE multiple times will accelerate the bird.\n4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.\n5. Place on the bottom some land colored as dark brown or yellow chosen randomly.\n6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.\n7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.\n8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.\nThe final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.<|im_end|>\n<|im_start|>assistant\n<think>\n"  \
        2>&1 | tee Q4_K_M_yes_samplers.txt
```

The full input from our <https://unsloth.ai/blog/deepseekr1-dynamic> 1.58bit blog is:

```
<|im_start|>user
Create a Flappy Bird game in Python. You must include these things:
1. You must use pygame.
2. The background color should be randomly chosen and is a light shade. Start with a light blue color.
3. Pressing SPACE multiple times will accelerate the bird.
4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.
5. Place on the bottom some land colored as dark brown or yellow chosen randomly.
6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.
7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.
8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.
The final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.<|im_end|>
<|im_start|>assistant
<think>
```

The beginning and the end of the final Python output after removing the thinking parts:

```python
import pygame
import random
import sys

pygame.init()
### Continues

class Bird:
    def __init__(self):
        ### Continues

def main():
    best_score = 0
    current_score = 0
    game_over = False
    pipes = []
    first_time = True  # Track first game play

    # Initial setup
    background_color = (173, 216, 230)  # Light blue initially
    land_color = random.choice(land_colors)
    bird = Bird()

    while True:
        for event in pygame.event.get():
            ### Continues

        if not game_over:
            # Update bird and pipes
            bird.update()
            ### Continues

        # Drawing
        ### Continues
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
```

<details>

<summary>Full final Python output (removed thinking parts):</summary>

{% code fullWidth="false" %}

```python
import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")
clock = pygame.time.Clock()

# Colors
pipe_colors = [(0, 100, 0), (210, 180, 140), (50, 50, 50)]
land_colors = [(139, 69, 19), (255, 255, 0)]

# Game constants
GRAVITY = 0.5
PIPE_SPEED = 5
BIRD_SIZE = 30
LAND_HEIGHT = 50
PIPE_WIDTH = 50
PIPE_GAP = 150

class Bird:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.velocity = 0
        self.shape = random.choice(['square', 'circle', 'triangle'])
        self.color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        self.rect = pygame.Rect(self.x - BIRD_SIZE//2, self.y - BIRD_SIZE//2, BIRD_SIZE, BIRD_SIZE)
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y - BIRD_SIZE//2
        self.rect.x = self.x - BIRD_SIZE//2  # Keep x centered
    
    def draw(self):
        if self.shape == 'square':
            pygame.draw.rect(screen, self.color, self.rect)
        elif self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (self.rect.centerx, self.rect.centery), BIRD_SIZE//2)
        elif self.shape == 'triangle':
            points = [
                (self.rect.centerx, self.rect.top),
                (self.rect.left, self.rect.bottom),
                (self.rect.right, self.rect.bottom)
            ]
            pygame.draw.polygon(screen, self.color, points)

def spawn_pipe():
    pipe_x = WIDTH
    top_height = random.randint(50, HEIGHT - PIPE_GAP - LAND_HEIGHT)
    rect_top = pygame.Rect(pipe_x, 0, PIPE_WIDTH, top_height)
    bottom_y = top_height + PIPE_GAP
    bottom_height = (HEIGHT - LAND_HEIGHT) - bottom_y
    rect_bottom = pygame.Rect(pipe_x, bottom_y, PIPE_WIDTH, bottom_height)
    color = random.choice(pipe_colors)
    return {
        'rect_top': rect_top,
        'rect_bottom': rect_bottom,
        'color': color,
        'scored': False
    }

def main():
    best_score = 0
    current_score = 0
    game_over = False
    pipes = []
    first_time = True  # Track first game play

    # Initial setup
    background_color = (173, 216, 230)  # Light blue initially
    land_color = random.choice(land_colors)
    bird = Bird()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # Reset the game
                        bird = Bird()
                        pipes.clear()
                        current_score = 0
                        if first_time:
                            # First restart after initial game over
                            background_color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
                            first_time = False
                        else:
                            background_color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
                        land_color = random.choice(land_colors)
                        game_over = False
                    else:
                        # Jump the bird
                        bird.velocity = -15  # Initial upward velocity

        if not game_over:
            # Update bird and pipes
            bird.update()

            # Move pipes left
            remove_pipes = []
            for pipe in pipes:
                pipe['rect_top'].x -= PIPE_SPEED
                pipe['rect_bottom'].x -= PIPE_SPEED
                # Check if bird passed the pipe
                if not pipe['scored'] and bird.rect.x > pipe['rect_top'].right:
                    current_score += 1
                    pipe['scored'] = True
                # Check if pipe is offscreen
                if pipe['rect_top'].right < 0:
                    remove_pipes.append(pipe)
            # Remove offscreen pipes
            for p in remove_pipes:
                pipes.remove(p)

            # Spawn new pipe if needed
            if not pipes or pipes[-1]['rect_top'].x < WIDTH - 200:
                pipes.append(spawn_pipe())

            # Check collisions
            land_rect = pygame.Rect(0, HEIGHT - LAND_HEIGHT, WIDTH, LAND_HEIGHT)
            bird_rect = bird.rect
            # Check pipes
            for pipe in pipes:
                if bird_rect.colliderect(pipe['rect_top']) or bird_rect.colliderect(pipe['rect_bottom']):
                    game_over = True
                    break
            # Check land and top
            if bird_rect.bottom >= land_rect.top or bird_rect.top <= 0:
                game_over = True

            if game_over:
                if current_score > best_score:
                    best_score = current_score

        # Drawing
        screen.fill(background_color)
        # Draw pipes
        for pipe in pipes:
            pygame.draw.rect(screen, pipe['color'], pipe['rect_top'])
            pygame.draw.rect(screen, pipe['color'], pipe['rect_bottom'])
        # Draw land
        pygame.draw.rect(screen, land_color, (0, HEIGHT - LAND_HEIGHT, WIDTH, LAND_HEIGHT))
        # Draw bird
        bird.draw()
        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {current_score}', True, (0, 0, 0))
        screen.blit(score_text, (WIDTH - 150, 10))
        # Game over screen
        if game_over:
            over_text = font.render('Game Over!', True, (255, 0, 0))
            best_text = font.render(f'Best: {best_score}', True, (255, 0, 0))
            restart_text = font.render('Press SPACE to restart', True, (255, 0, 0))
            screen.blit(over_text, (WIDTH//2 - 70, HEIGHT//2 - 30))
            screen.blit(best_text, (WIDTH//2 - 50, HEIGHT//2 + 10))
            screen.blit(restart_text, (WIDTH//2 - 100, HEIGHT//2 + 50))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
```

{% endcode %}

</details>

6. When running it, we get a runnable game!

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-1740ecd246c7f62c363bc0ba1e0f1099b2f9b2a4%2Fimage.png?alt=media" alt=""><figcaption></figcaption></figure>

7. Now try the same without our fixes! So remove `--samplers "top_k;top_p;min_p;temperature;dry;typ_p;xtc"` This will save the output to `Q4_K_M_no_samplers.txt`

```bash
./llama.cpp/llama-cli \
    --model unsloth-QwQ-32B-GGUF/QwQ-32B-Q4_K_M.gguf \
    --threads 32 \
    --ctx-size 16384 \
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.6 \
    --repeat-penalty 1.1 \
    --dry-multiplier 0.5 \
    --min-p 0.01 \
    --top-k 40 \
    --top-p 0.95 \
    -no-cnv \
    --prompt "<|im_start|>user\nCreate a Flappy Bird game in Python. You must include these things:\n1. You must use pygame.\n2. The background color should be randomly chosen and is a light shade. Start with a light blue color.\n3. Pressing SPACE multiple times will accelerate the bird.\n4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.\n5. Place on the bottom some land colored as dark brown or yellow chosen randomly.\n6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.\n7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.\n8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.\nThe final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.<|im_end|>\n<|im_start|>assistant\n<think>\n"  \
        2>&1 | tee Q4_K_M_no_samplers.txt
```

You will get some looping, but **problematically incorrect Python syntax** and many other issues. For example the below looks correct, but is wrong! Ie line 39 `pipes.clear() ### <<< NameError: name 'pipes' is not defined. Did you forget to import 'pipes'?`

{% code overflow="wrap" lineNumbers="true" %}

```python
import pygame
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GROUND_HEIGHT = 20
GRAVITY = 0.7
PIPE_SPEED = -3
BIRD_SIZE = 45
MIN_GAP = 130
MAX_GAP = 200
PIPE_COLORS = [(0, 96, 0), (205, 133, 63), (89, 97, 107)]
DARK_BROWN = (94, 72, 4)
YELLOW = (252, 228, 6)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def random_light_color():
    return (
        random.randint(180, 230),
        random.randint(190, 300),
        random.randint(250, 255)
    )

def reset_game():
    global bird_x, bird_y
    global pipes, score
    global background_color, land_color
    global bird_shape, bird_color

    # Bird properties
    bird_x = WIDTH * 0.3
    bird_y = HEIGHT // 2
    bird_vel = -5  # Initial upward thrust

    pipes.clear() ### <<< NameError: name 'pipes' is not defined. Did you forget to import 'pipes'?
```

{% endcode %}

8. If you use `--repeat-penalty 1.5`, it gets even worse and more obvious, with actually totally incorrect syntax.

```python
import pygame
from random import randint  # For generating colors/shapes/positions randomly 
pygame.init()

# Constants:
WIDTH, HEIGHT =456 ,702   #
BACKGROUND_COLOR_LIGHTS=['lightskyblue']
GAP_SIZE=189           #

BIRD_RADIUS=3.  
PIPE_SPEED=- ( )    ? 
class Game():
def __init__(self):
        self.screen_size=( )

def reset_game_vars():
    global current_scor e
   # set to zero and other initial states.

# Main game loop:
while running :
     for event in pygame.event.get() : 
        if quit ... etc

pygame.quit()
print("Code is simplified. Due time constraints, full working version requires further implementation.")
```

9. You might be wondering maybe it's Q4\_K\_M? B16 ie full precision should work fine right? Incorrect - the outputs again fail if we do not use our fix of -`-samplers "top_k;top_p;min_p;temperature;dry;typ_p;xtc"` when using a Repetition Penalty.

## :sunrise\_over\_mountains: Still doesn't work? Try Min\_p = 0.1, Temperature = 1.5

According to the Min\_p paper <https://arxiv.org/pdf/2407.01082>, for more creative and diverse outputs, and if you still see repetitions, try disabling top\_p and top\_k!

```bash
./llama.cpp/llama-cli --model unsloth-QwQ-32B-GGUF/QwQ-32B-Q4_K_M.gguf \
    --threads 32 --n-gpu-layers 99 \
    --ctx-size 16384 \
    --temp 1.5 \
    --min-p 0.1 \
    --top-k 0 \
    --top-p 1.0 \
    -no-cnv \
    --prompt "<|im_start|>user\nCreate a Flappy Bird game in Python. You must include these things:\n1. You must use pygame.\n2. The background color should be randomly chosen and is a light shade. Start with a light blue color.\n3. Pressing SPACE multiple times will accelerate the bird.\n4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.\n5. Place on the bottom some land colored as dark brown or yellow chosen randomly.\n6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.\n7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.\n8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.\nThe final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.<|im_end|>\n<|im_start|>assistant\n<think>\n"
```

Another approach is to disable `min_p` directly, since llama.cpp by default uses `min_p = 0.1`!

```bash
./llama.cpp/llama-cli --model unsloth-QwQ-32B-GGUF/QwQ-32B-Q4_K_M.gguf \
    --threads 32 --n-gpu-layers 99 \
    --ctx-size 16384 \
    --temp 0.6 \
    --min-p 0.0 \
    --top-k 40 \
    --top-p 0.95 \
    -no-cnv \
    --prompt "<|im_start|>user\nCreate a Flappy Bird game in Python. You must include these things:\n1. You must use pygame.\n2. The background color should be randomly chosen and is a light shade. Start with a light blue color.\n3. Pressing SPACE multiple times will accelerate the bird.\n4. The bird's shape should be randomly chosen as a square, circle or triangle. The color should be randomly chosen as a dark color.\n5. Place on the bottom some land colored as dark brown or yellow chosen randomly.\n6. Make a score shown on the top right side. Increment if you pass pipes and don't hit them.\n7. Make randomly spaced pipes with enough space. Color them randomly as dark green or light brown or a dark gray shade.\n8. When you lose, show the best score. Make the text inside the screen. Pressing q or Esc will quit the game. Restarting is pressing SPACE again.\nThe final game should be inside a markdown section in Python. Check your code for errors and fix them before the final markdown section.<|im_end|>\n<|im_start|>assistant\n<think>\n"
```

## :thinking: \<think> token not shown?

Some people are reporting that because \<think> is default added in the chat template, some systems are not outputting the thinking traces correctly. You will have to manually edit the Jinja template from:

{% code overflow="wrap" %}

```
```

{% endcode %}

to another by removing the `<think>\n` at the end. The model will now have to manually add `<think>\n` during inference, which might not always succeed. DeepSeek also edited all models to default add a `<think>` token to force the model to go into reasoning model.

So change `{%- if add_generation_prompt %} {{- '<|im_start|>assistant\n<think>\n' }} {%- endif %}` to `{%- if add_generation_prompt %} {{- '<|im_start|>assistant\n' }} {%- endif %}`

ie remove `<think>\n`

<details>

<summary>Full jinja template with removed &#x3C;think>\n part</summary>

{% code overflow="wrap" %}

```
```

{% endcode %}

</details>

## Extra Notes

We first thought maybe:

1. QwQ's context length was not natively 128K, but rather 32K with YaRN extension. For example in the readme file for <https://huggingface.co/Qwen/QwQ-32B>, we see:

```json
{
  ...,
  "rope_scaling": {
    "factor": 4.0,
    "original_max_position_embeddings": 32768,
    "type": "yarn"
  }
}
```

We tried overriding llama.cpp's YaRN handling, but nothing changed.

{% code overflow="wrap" %}

```bash
--override-kv qwen2.context_length=int:131072 \
--override-kv qwen2.rope.scaling.type=str:yarn \
--override-kv qwen2.rope.scaling.factor=float:4 \
--override-kv qwen2.rope.scaling.original_context_length=int:32768 \
--override-kv qwen2.rope.scaling.attn_factor=float:1.13862943649292 \
```

{% endcode %}

2. We also thought maybe the RMS Layernorm epsilon was wrong - not 1e-5 but maybe 1e-6. For example [this](https://huggingface.co/Qwen/Qwen2.5-32B-Instruct/blob/main/config.json) has `rms_norm_eps=1e-06`, whilst [this](https://huggingface.co/Qwen/Qwen2.5-32B/blob/main/config.json) has `rms_norm_eps=1e-05` . We also overrided it, but it did not work:

{% code overflow="wrap" %}

```bash
--override-kv qwen2.attention.layer_norm_rms_epsilon=float:0.000001 \
```

{% endcode %}

3. We also tested if tokenizer IDs matched between llama.cpp and normal Transformers courtesy of [@kalomaze](https://x.com/kalomaze/status/1897875332230779138). They matched, so this was not the culprit.

We provide our experimental results below:

{% file src="/files/Fb8C7pMzEAt2EMk6Y5Nv" %}
BF16 full precision with no sampling fix
{% endfile %}

{% file src="/files/Tza2MHehZX5GVoEgrsQj" %}
BF16 full precision with sampling fix
{% endfile %}

{% file src="/files/Q4ssXKESlEecT7UFam80" %}
Q4\_K\_M precision with no sampling fix
{% endfile %}

{% file src="/files/df2EQ852zfpf0oIdYi40" %}
Q4\_K\_M precision with sampling fix
{% endfile %}

## :pencil2: Tokenizer Bug Fixes

* We found a few issues as well specifically impacting finetuning! The EOS token is correct, but the PAD token should probably rather be `"<|vision_pad|>`" We updated it in: <https://huggingface.co/unsloth/QwQ-32B/blob/main/tokenizer_config.json>

```
"eos_token": "<|im_end|>",
"pad_token": "<|endoftext|>",
```

## :tools: Dynamic 4-bit Quants

We also uploaded dynamic 4bit quants which increase accuracy vs naive 4bit quantizations! We attach the QwQ quantization error plot analysis for both activation and weight quantization errors:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fgit-blob-16157f53eff143c179be571a43f8b55000d94290%2FQwQ%20quantization%20errors.png?alt=media" alt=""><figcaption></figcaption></figure>

We uploaded dynamic 4-bit quants to: <https://huggingface.co/unsloth/QwQ-32B-unsloth-bnb-4bit>

Since vLLM 0.7.3 (2025 February 20th) <https://github.com/vllm-project/vllm/releases/tag/v0.7.3>, vLLM now supports loading Unsloth dynamic 4bit quants!

All our GGUFs are at <https://huggingface.co/unsloth/QwQ-32B-GGUF>!


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/qwq-32b-how-to-run-effectively.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
