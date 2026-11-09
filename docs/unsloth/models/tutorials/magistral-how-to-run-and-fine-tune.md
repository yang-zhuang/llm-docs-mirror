> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/magistral-how-to-run-and-fine-tune.md).

# Magistral: How to Run & Fine-tune

Meet Magistral - Mistral's new reasoning models.

**Magistral-Small-2509** is a reasoning LLM developed by Mistral AI. It excels at coding and mathematics and supports multiple languages. Magistral supports a 128k token context window and was finetuned from [**Mistral-Small-3.2**](https://huggingface.co/unsloth/Mistral-Small-3.2-24B-Instruct-2506). Magistral runs perfectly well locally on a single RTX 4090 or a Mac with 16 to 24GB RAM.

<a href="#running-magistral" class="button primary">Running Magistral Tutorial</a> <a href="#fine-tuning-magistral-with-unsloth" class="button secondary">Fine-tuning Magistral</a>

{% hint style="success" %}
Update: **Magistral-2509** new update is out as of September, 2025!\
\
Now with Vision support! We worked with Mistral again with the release of Magistral. Make sure to download Mistral's official uploads or Unsloth's uploads to get the correct implementation (ie correct system prompt, correct chat template etc.)

**If you're using llama.cpp, please use `--jinja` to enable the system prompt!**
{% endhint %}

All uploads use Unsloth [Dynamic 2.0](/docs/basics/dynamic-3.0-ggufs.md) for SOTA 5-shot MMLU and KL Divergence performance, meaning you can run & fine-tune quantized Mistral LLMs with minimal accuracy loss.

#### Magistral-Small **- Unsloth Dynamic** uploads:

<table><thead><tr><th width="255.64999389648438">Dynamic 2.0 GGUF (to run)</th><th width="305.25">Dynamic 4-bit (to finetune/deploy)</th><th>Dynamic Float8</th></tr></thead><tbody><tr><td><ul><li><a href="https://huggingface.co/unsloth/Magistral-Small-2509-GGUF">Magistral-Small-2509-GGUF</a> - new</li><li><a href="https://huggingface.co/unsloth/Magistral-Small-2507-GGUF">Magistral-Small-2507-GGUF</a></li><li><a href="https://huggingface.co/unsloth/Magistral-Small-2506-GGUF">Magistral-Small-2506-GGUF</a></li></ul></td><td><ul><li><a href="https://huggingface.co/unsloth/Magistral-Small-2509-unsloth-bnb-4bit">Magistral-Small-2509-unsloth-bnb-4bit</a> - new</li><li><a href="https://huggingface.co/unsloth/Magistral-Small-2507-unsloth-bnb-4bit">Magistral-Small-2507-unsloth-bnb-4bit</a></li><li><a href="https://huggingface.co/unsloth/Magistral-Small-2506-unsloth-bnb-4bit">Magistral-Small-2506-unsloth-bnb-4bit</a></li></ul></td><td><ul><li><a href="https://huggingface.co/unsloth/Magistral-Small-2509-FP8-Dynamic">Magistral-Small-2509-FP8-Dynamic</a></li><li><a href="https://huggingface.co/unsloth/Magistral-Small-2509-FP8-torchao">Magistral-Small-2509-FP8-torchao</a></li></ul></td></tr></tbody></table>

## 🖥️ **Running Magistral**

### :gear: Official Recommended Settings

According to Mistral AI, these are the recommended settings for inference:

* <mark style="background-color:blue;">**Temperature of: 0.7**</mark>
* Min\_P of: 0.01 (optional, but 0.01 works well, llama.cpp default is 0.1)
* Set <mark style="background-color:green;">**top\_p to: 0.95**</mark>
* A 128k context window is supported, **but** performance might degrade past **40k**. So we recommend setting the maximum length to 40k if you see bad performance.

**This is the recommended system prompt for Magistral 2509, 2507:**

{% code overflow="wrap" %}

```
First draft your thinking process (inner monologue) until you arrive at a response. Format your response using Markdown, and use LaTeX for any mathematical equations. Write both your thoughts and the response in the same language as the input.

Your thinking process must follow the template below:[THINK]Your thoughts or/and draft, like working through an exercise on scratch paper. Be as casual and as long as you want until you are confident to generate the response. Use the same language as the input.[/THINK]Here, provide a self-contained response.
```

{% endcode %}

**This is the recommended system prompt for Magistral 2506:**

```
A user will ask you to solve a task. You should first draft your thinking process (inner monologue) until you have derived the final answer. Afterwards, write a self-contained summary of your thoughts (i.e. your summary should be succinct but contain all the critical steps you needed to reach the conclusion). You should use Markdown to format your response. Write both your thoughts and summary in the same language as the task posed by the user. NEVER use \boxed{} in your response.

Your thinking process must follow the template below:
<think>
Your thoughts or/and draft, like working through an exercise on scratch paper. Be as casual and as long as you want until you are confident to generate a correct answer.
</think>

Here, provide a concise summary that reflects your reasoning and presents a clear final answer to the user. Don't mention that this is a summary.

Problem:
```

{% hint style="success" %}
Our dynamic uploads have the '`UD`' prefix in them. Those without are not dynamic however still utilize our calibration dataset.
{% endhint %}

* **Multilingual:** Magistral supports many languages including: English, French, German, Greek, Hindi, Indonesian, Italian, Japanese, Korean, Malay, Nepali, Polish, Portuguese, Romanian, Russian, Serbian, Spanish, Swedish, Turkish, Ukrainian, Vietnamese, Arabic, Bengali, Chinese, and Farsi.

### :question:Testing the model

Mistral has their own vibe checking prompts which can be used to evaluate Magistral. Keep in mind these tests are based on running the full unquantized version of the model, however you could also test them on quantized versions:

**Easy -** *Make sure they always work*

```py
prompt_1 = 'How many "r" are in strawberry?'

prompt_2 = 'John is one of 4 children. The first sister is 4 years old. Next year, the second sister will be twice as old as the first sister. The third sister is two years older than the second sister. The third sister is half the ago of her older brother. How old is John?'

prompt_3 = '9.11 and 9.8, which is greater?'
```

**Medium** - *Should most of the time be correct*

```py
prompt_4 = "Think about 5 random numbers. Verify if you can combine them with addition, multiplication, subtraction or division to 133"

prompt_5 = "Write 4 sentences, each with at least 8 words. Now make absolutely sure that every sentence has exactly one word less than the previous sentence."

prompt_6 = "If it takes 30 minutes to dry 12 T-shirts in the sun, how long does it take to dry 33 T-shirts?"
```

**Hard** - *Should sometimes get them right*

```py
prompt_7 = "Pick 5 random words each with at least 10 letters. Print them out. Reverse each word and print it out. Then extract letters that are alphabetically sorted smaller than "g" and print them. Do not use code."

prompt_8 = "Exactly how many days ago did the French Revolution start? Today is June 4th, 2025."
```

<mark style="color:green;">**We provide some**</mark> [<mark style="color:green;">**example outputs**</mark>](#sample-outputs) <mark style="color:green;">**at the end of the blog.**</mark>

## :llama: Tutorial: How to Run Magistral in Ollama

1. Install `ollama` if you haven't already!

```bash
apt-get update
apt-get install pciutils -y
curl -fsSL https://ollama.com/install.sh | sh
```

2. Run the model with our dynamic quant. We did not set the context length automatically, so it will just use Ollama's default set context length.\
   Note you can call `ollama serve &`in another terminal if it fails! We include all suggested parameters (temperature etc) in `params` in our Hugging Face upload!
3. Also Magistral supports 40K context lengths, so best to enable [**KV cache quantization**](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-set-the-quantization-type-for-the-kv-cache). We use 8bit quantization which saves 50% memory usage. You can also try `"q4_0"` or `"q8_0"`
4. **Ollama also sets the default context length to 4096**, as [mentioned here](https://github.com/ollama/ollama/blob/main/docs/faq.md#how-can-i-specify-the-context-window-size). Use `OLLAMA_CONTEXT_LENGTH=8192` to change it to 8192. Magistral supports up to 128K, but 40K (40960) is tested most.

```bash
export OLLAMA_KV_CACHE_TYPE="f16"
OLLAMA_CONTEXT_LENGTH=8192 ollama serve &
ollama run hf.co/unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL
```

## 📖 Tutorial: How to Run Magistral in llama.cpp

1. Obtain the latest `llama.cpp` on [GitHub here](https://github.com/ggml-org/llama.cpp). You can follow the build instructions below as well. Change `-DGGML_CUDA=ON` to `-DGGML_CUDA=OFF` if you don't have a GPU or just want CPU inference. **For Apple Mac / Metal devices**, set `-DGGML_CUDA=OFF` then continue as usual - Metal support is on by default.

```bash
apt-get update
apt-get install pciutils build-essential cmake curl libcurl4-openssl-dev -y
git clone https://github.com/ggml-org/llama.cpp
cmake llama.cpp -B llama.cpp/build \
    -DBUILD_SHARED_LIBS=OFF -DGGML_CUDA=ON -DLLAMA_CURL=ON
cmake --build llama.cpp/build --config Release -j --clean-first --target llama-quantize llama-cli llama-gguf-split llama-mtmd-cli
cp llama.cpp/build/bin/llama-* llama.cpp
```

2. If you want to use `llama.cpp` directly to load models, you can do the below: (:Q4\_K\_XL) is the quantization type. You can also download via Hugging Face (point 3). This is similar to `ollama run`

{% code overflow="wrap" %}

```bash
./llama.cpp/llama-cli -hf unsloth/Magistral-Small-2509-GGUF:UD-Q4_K_XL --jinja --temp 0.7 --top-k -1 --top-p 0.95 -ngl 99
```

{% endcode %}

{% hint style="warning" %}
In llama.cpp, please use `--jinja` to enable the system prompt!
{% endhint %}

3. **OR** download the model via (after installing `pip install huggingface_hub hf_transfer` ). You can choose UD-Q4\_K\_XL, (Unsloth Dynamic), Q4\_K\_M, or other quantized versions (like BF16 full precision).

```python
# !pip install huggingface_hub hf_transfer
import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id = "unsloth/Magistral-Small-2509-GGUF",
    local_dir = "unsloth/Magistral-Small-2509-GGUF",
    allow_patterns = ["*UD-Q4_K_XL*"], # For UD-Q4_K_XL
)
```

4. Run the model.
5. Edit `--threads -1` for the maximum CPU threads, `--ctx-size 40960` for context length (Magistral supports 40K context length!), `--n-gpu-layers 99` for GPU offloading on how many layers. Try adjusting it if your GPU goes out of memory. Also remove it if you have CPU only inference. We also use 8bit quantization for the K cache to reduce memory usage.
6. For conversation mode:

<pre class="language-bash"><code class="lang-bash">./llama.cpp/llama-cli \
    --model unsloth/Magistral-Small-2509-GGUF/Magistral-Small-2509-UD-Q4_K_XL.gguf \
    --ctx-size 40960 \
    <a data-footnote-ref href="#user-content-fn-1">--cache-type-k f16</a> \
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.7 \
<strong>    --repeat-penalty 1.0 \
</strong>    --min-p 0.01 \
    --top-k -0 \
    --top-p 0.95 \
    <a data-footnote-ref href="#user-content-fn-2">--jinja</a>
</code></pre>

{% hint style="warning" %}
Remember to remove \<bos> since Magistral auto adds a \<bos>
{% endhint %}

## Sample outputs

<details>

<summary>How many "r" are in strawberry? [Correct answer = 3]</summary>

{% code overflow="wrap" lineNumbers="true" fullWidth="true" %}

```
<think>
Alright, I have a problem to solve: "How many 'r's are in strawberry?"

First, I need to understand the problem. It's asking for the count of the letter 'r' in the word "strawberry".

Step 1: Write down the word and look at each letter.
The word is: s t r a w b e r r y

Step 2: Identify the 'r's in the word.
Let's go through each letter one by one:
1. s - not an r
2. t - not an r
3. r - that's one r
4. a - not an r
5. w - not an r
6. b - not an r
7. e - not an r
8. r - that's another r
9. r - and another one
10. y - not an r

So, I see the letter 'r' appears at positions 3, 8, and 9.

Step 3: Count the number of 'r's.
From the above, there are three 'r's in "strawberry".

But wait, I should double-check to make sure I didn't miss anything or count incorrectly.

Let me write the word again: strawberry.

Looking at it:
- The third letter is 'r' (s-t-r)
- Then later, we have 'e-r-r' which is two more 'r's.

Yes, that's three 'r's in total.

But just to be thorough, sometimes letters can be hidden or the word might have silent letters, but in this case, all letters are pronounced in "strawberry", and 'r' is clearly pronounced in the third, eighth, and ninth positions.

So, the count is indeed three.

But wait, is it possible that the 'r's are not all pronounced? For example, in some accents or dialects, letters might be silent or pronounced differently. However, in standard pronunciation, all these 'r's are pronounced.

But the question is about the number of 'r's in the word, not about pronunciation. It's about the written form. So, regardless of pronunciation, we're counting the letters in the word "strawberry".

Let me write it out again and count:

s (1)
t (2)
r (3) - first r
a (4)
w (5)
b (6)
e (7)
r (8) - second r
r (9) - third r
y (10)

Yes, three 'r's.

But just to be sure, maybe I should think about the spelling. Sometimes letters can be part of digraphs or other combinations, but in "strawberry", the 'r's are all standalone letters.

Let me think about the spelling breakdown:
- "straw" has one 'r' (the third letter)
- "berry" has two 'r's (the second and third letters in "berry", but in the full word, it's the eighth and ninth letters)

So, "straw" has 1 'r', "berry" has 2 'r's, totaling 3 'r's in "strawberry".

I think I'm confident now. The word "strawberry" has three 'r's.

But before finalizing, I recall that sometimes letters can be repeated or there might be a trick. Let me see:

The word is: s-t-r-a-w-b-e-r-r-y.

Counting the 'r's:
1. The 'r' in the third position.
2. The 'r' in the eighth position.
3. The 'r' in the ninth position.

No other 'r's are present.

Therefore, the total number of 'r's in "strawberry" is three.

But just to cross-verify, perhaps I can write the word and highlight the 'r's:

s t r a w b e r r y
   r     r r

Yes, three 'r's.

Is there any chance I'm missing something? Maybe considering uppercase and lowercase? But the problem is case-insensitive since it's about the letter 'r', not 'R'. The word is given in lowercase, but even if it were uppercase, 'R' is the same letter as 'r' in terms of counting.

So, final count is three.

But wait, is "strawberry" spelled correctly? Let me check the spelling.

I think it's s-t-r-a-w-b-e-r-r-y. Yes, that seems correct.

Therefore, the number of 'r's is indeed three.

But just to be extra sure, maybe I can think of the word in a different way. For example, breaking it down:

"straw" + "berry" = "strawberry"

"straw" has one 'r' (the third letter: s-t-r)
"berry" has two 'r's (the second and third letters: b-e-r-r-y, but actually, 'berry' is b-e-r-r-y, so 'r' is the third and fourth letters? Wait, let's see:

'berry' is b-e-r-r-y. Wait, no:

b (1)
e (2)
r (3)
r (4)
y (5)

So, 'berry' has 'r's at positions 3 and 4, which are two 'r's.

'straw' is s-t-r-a-w, so 'r' is at position 3, one 'r'.

Combined, 'strawberry' is 'straw' + 'berry' = s-t-r-a-w-b-e-r-r-y, which has 'r's at positions 3, 3+5+1=9? Wait, no, let's index:

'straw' is positions 1-5 (s-t-r-a-w)
'berry' is positions 6-10 (b-e-r-r-y)

So 'r's in 'straw' are at position 3.
'r's in 'berry' are at positions 8 and 9 (since 'berry' starts at position 6: b(6), e(7), r(8), r(9), y(10)).

Thus, total 'r's are at positions 3, 8, and 9: three 'r's.

Yes, consistent again.

Is there any other way to approach this? Maybe counting the total letters and seeing how many are 'r's.

"strawberry" has 10 letters: s, t, r, a, w, b, e, r, r, y.

Counting 'r's: positions 3, 8, 9 → 3 'r's.

Alternatively, I could write out the word and replace non-'r's with another character to see how many 'r's are left.

Original: s t r a w b e r r y
Replace non-r: x x r x x x x r r x
Now count 'r's: positions 2 (but original was 3rd letter), wait no, in the replaced string, 'r's are at positions 3 (original position 3), and then after replacing others, the next 'r's are at positions... Wait, let's see:

Original positions:
1: s → x
2: t → x
3: r → r
4: a → x
5: w → x
6: b → x
7: e → x
8: r → r
9: r → r
10: y → x

So replaced string: x x r x x x x r r x
Now count 'r's: positions 3, 8, 9 in original correspond to positions 3, 8, 9 in replaced (but replaced has x's in other positions, so 'r's are still at 3,8,9). Wait, in replaced string, 'r's are at positions 3,8,9, but the length is still 10, so positions are same as original. So count is same: 3 'r's.

Another method: write the word and cross out non-'r's.

Original: s t r a w b e r r y
Cross out non-r: x x r x x x x r r x
Now count 'r's: there are three 'r's remaining.

All methods confirm that there are three 'r's in "strawberry".

But just to think outside the box, is there any ambiguity in the question? For example, is it asking for uppercase 'R' or lowercase 'r'? The problem says "r", lowercase, so we're counting lowercase 'r's. In the word "strawberry", all letters are lowercase (assuming the input is in lowercase; if it were mixed case, we'd have to consider, but since it's given as "strawberry", which is all lowercase, we're good).

Also, is it possible that some 'r's are part of a digraph or trigraph? For example, in some languages, 'rr' might be considered a single sound or letter, but in English orthography, 'rr' is two separate 'r's. So in "strawberry", the 'rr' is two 'r's.

Therefore, the count remains three.

Is there any other interpretation? Maybe considering that sometimes letters can represent different sounds or that 'r' might be silent, but as mentioned earlier, the question is about the written letter 'r', not pronunciation.

Final confirmation: let's write the word and count 'r's aloud:

s (no), t (no), r (1), a (no), w (no), b (no), e (no), r (2), r (3), y (no).

Yes, three 'r's.

Therefore, the number of 'r's in "strawberry" is three.

But before finalizing, let me think if there's any trick or if I'm missing something obvious. For example, sometimes questions like this have hidden complexities, like counting 'r's in the word's spelling or pronunciation, or considering that 'r' might appear in other forms, like in 'rr' which is two 'r's together, but we've already accounted for that.

Alternatively, is the question about the number of times the letter 'r' appears in the spelling of "strawberry"? Yes, that's how I interpreted it, and my count is three.

Is there any chance the word is spelled differently? For example, in some countries or dialects, is "strawberry" spelled differently? In American English and British English, it's spelled the same way: s-t-r-a-w-b-e-r-r-y.

Let me check the spelling again: s, t, r, a, w, b, e, r, r, y. Yes, that's correct.

Therefore, the number of 'r's is indeed three.

But just to be absolutely sure, perhaps I can think of the word in a sentence or see it written out:

Example sentence: "I ate a strawberry." The word is "strawberry", and in it, the 'r's are in the middle and at the end.

Looking at the spelling: s-t-r-a-w-b-e-r-r-y. Counting:

1. s
2. t
3. r (1)
4. a
5. w
6. b
7. e
8. r (2)
9. r (3)
10. y

Yes, three 'r's.

I think I've exhausted all possible ways to verify this count. Therefore, the number of 'r's in "strawberry" is three.

But wait, the user might have intended the question differently. Could it be about the number of times the sound 'r' appears in pronunciation? For example, sometimes letters are silent or combined in pronunciation, but the question asks for the count of the letter 'r', not the sound.

In pronunciation, "strawberry" is /ˈstroʊbɛri/ or similar, where the 'r's are pronounced as in the spelling. But since the question is about the letter count, not phonemes, we stick with the written form.

Therefore, the count remains three.

Is there any other interpretation? For example, counting uppercase 'R's if the word were capitalized? But the word is given in lowercase, and the question asks for 'r', lowercase, so it's consistent.

Final answer: there are three 'r's in "strawberry".

But just to double-check, perhaps I can list the letters with their positions:

Position: 1 2 3 4 5 6 7 8 9 10
Letter:   s t r a w b e r r y

Now, pick out the 'r's: positions 3, 8, 9. That's three 'r's.

Alternatively, write the word and circle the 'r's:

Strawberry: s t r a w b e r r y
The 'r's are in positions 3, 8, and 9. So, three 'r's.

No other interpretations seem plausible. Therefore, the answer is three.

But before finalizing, let me think if there's any ambiguity in the word itself. Could "strawberry" be misspelled or is there another spelling variant?

In English, "strawberry" is consistently spelled with two 'r's at the end: "berry" is spelled with two 'r's (b-e-r-r-y), and "straw" has one 'r' (s-t-r-a-w). So total is three 'r's.

Is there any other word that might be confused with "strawberry"? For example, "strawberi" or similar, but no, "strawberry" is the correct spelling with three 'r's.

Therefore, the final count is three.

But just to be thorough, perhaps I can think of the word in another language. For example, in Spanish, "strawberry" is "fresas" or "fresa", which don't have 'r's, but the question is about the English word "strawberry".

In English, as confirmed, there are three 'r's in "strawberry".

Is there any other angle? For example, if the word were in uppercase, like "STRAWBERRY", the count would still be the same since 'R' is the uppercase counterpart of 'r'. But the problem specifies 'r', lowercase, and the word is given in lowercase, so it's consistent.

Therefore, the number of 'r's in "strawberry" is three.

But just to think differently, perhaps the word is being considered in a different context, like in a code or cipher where letters might represent something else. But the problem is straightforward: count the number of times the letter 'r' appears in the word "strawberry".

So, after all this careful consideration, the answer is clearly three.

But before finalizing, let me think if I've made any mistake in counting. Let me recount:

Word: s t r a w b e r r y

Positions:
1: s
2: t
3: r (1)
4: a
5: w
6: b
7: e
8: r (2)
9: r (3)
10: y

Yes, three 'r's at positions 3, 8, and 9.

No mistake in counting.

Therefore, the final answer is that there are three 'r's in the word "strawberry".

But wait, the user might expect a different answer if they're considering something else, but based on the straightforward interpretation, it's three.

Perhaps the user expects us to count only the distinct 'r's or something, but all 'r's are identical letters in this context.

Alternatively, maybe the question is a trick question implying that 'r's are pronounced differently or not at all, but again, the question is about the count of the letter 'r' in the spelling, not pronunciation.

Thus, the answer is three.

But just to be sure, let me think of the word "strawberry" and say it aloud: "strawberry". The 'r's are clearly pronounced as in the spelling.

No hidden complexities here. The count is three.

Final verification: write the word and count 'r's:

s t r a w b e r r y

'r' appears in the 3rd, 8th, and 9th positions. That's three times.

Therefore, the number of 'r's in "strawberry" is three.

But before concluding, let me think if there's any other interpretation where the answer could be different. For example, if the word were written in a different font or if there were any hidden letters, but in standard writing, it's clear.

Alternatively, if the word were in a different language with different spelling, but "strawberry" is the English word, and in English, it's spelled with three 'r's.

Another thought: is it possible that the 'w' or another letter is sometimes considered an 'r'? No, in English alphabet, 'w' is a separate letter from 'r'.

No other interpretations seem valid. The answer is three.

But just to be extra cautious, perhaps the word is misspelled in the question, but assuming it's correctly spelled as "strawberry", the count is three.

Therefore, after thorough consideration, the number of 'r's in "strawberry" is three.

But wait, looking back at the word: strawberry. Let me write it and count:

s, t, r, a, w, b, e, r, r, y.

Let me list them:

1. s
2. t
3. r
4. a
5. w
6. b
7. e
8. r
9. r
10. y

So, 'r's are at positions 3, 8, and 9. That's three 'r's.

Is there any chance I'm miscounting positions? Let me recount:

1: s
2: t
3: r (1st r)
4: a
5: w
6: b
7: e
8: r (2nd r)
9: r (3rd r)
10: y

Yes, three 'r's.

Therefore, the final answer is that there are three 'r's in the word "strawberry".

But just to ensure completeness, perhaps the word is being considered in uppercase or another case, but since the question is about 'r' (lowercase) and the word is given in lowercase, it's consistent.

Alternatively, if the word were "Strawberry" (with a capital S), does that affect the count? The question asks for 'r' (lowercase), and in "Strawberry", the 'S' is uppercase, but the 'r's are lowercase (assuming standard title case where only the first letter is capitalized). But since the question specifies 'r' (lowercase), and the 'r's in "Strawberry" are lowercase (unless it's all caps or something), but the given word is "strawberry" all lowercase, so it's three 'r's.

But even if it were "Strawberry", the 'r's are still lowercase (assuming standard capitalization), so count remains the same.

But since the given word is "strawberry" in all lowercase, the count is three.

Therefore, the number of 'r's in "strawberry" is three.

But just to think of edge cases, what if the word had a silent 'r'? But as discussed earlier, the question is about the written letter, not pronunciation.

Alternatively, if the word were in a different font where 'r' looks like something else, but in standard fonts, it's clear.

No other possibilities seem to alter the count.

Thus, the final answer is three.

But before finalizing, let me think if the word could be written differently, like with a different spelling variant. For example, in some dialects or historical contexts, words might be spelled differently, but modern English spells "strawberry" with three 'r's (one in 'straw' and two in 'berry').

Therefore, the count is three.

After all this careful consideration and multiple verification methods, I am confident that the number of 'r's in "strawberry" is three.

But to ensure that I haven't missed anything, perhaps I can think of the word's origin or related words. For example, "straw" has one 'r', "berry" has two 'r's, combining gives three 'r's in "strawberry". This also confirms the count.

Therefore, the answer is three.

However, sometimes such questions are trick questions expecting a different answer. For example, if the question was about the number of times the letter 'r' appears in the word "strawberry" when spelled out, but that seems convoluted and unlikely.

Alternatively, counting the number of closed areas in the letter 'r' when written in a certain font, but that's not relevant here.

Another possibility is that the question expects us to count the number of times the sound 'r' appears in pronunciation, but again, the question asks for the count of the letter 'r', not sounds.

In pronunciation, "strawberry" has the 'r' sound in "straw" and in "berry", but since 'berry' has two 'r's in spelling, both are pronounced in standard English, so the count would still relate to the spelling, which is three 'r's.

But since the question is about the letter count in writing, not pronunciation, the answer remains three.

Therefore, after all this thorough checking, the number of 'r's in "strawberry" is three.

But just to be sure, perhaps I can ask myself: if I were to type the word "strawberry" and count how many times I press the 'r' key, it would be three times (assuming I don't make any typos while typing).

Thus, confirming again: three 'r's.

Therefore, the final answer is:

There are 3 'r's in the word "strawberry".

But to present it neatly, perhaps as a count:

The word "strawberry" spelled out: s-t-r-a-w-b-e-r-r-y.

Counting 'r's:
1. The third letter: r
2. The eighth letter: r
3. The ninth letter: r

Total: 3 'r's.

Therefore, the number of 'r's in "strawberry" is 3.

But to ensure completeness, let me think of the word's length: "strawberry" has 10 letters. The positions are:

1: s
2: t
3: r (1st r)
4: a
5: w
6: b
7: e
8: r (2nd r)
9: r (3rd r)
10: y

Thus, three 'r's at positions 3, 8, and 9.

No other 'r's present.

Therefore, the final count is three.

But to present it in a structured way:

Word: s t r a w b e r r y
Positions of 'r': 3, 8, 9
Number of 'r's: 3

Thus, the answer is 3.

But just to think if there's any other interpretation where the answer could be different, perhaps considering that in some fonts, 'r' might look like another letter, but in standard fonts, it's distinct.

Alternatively, if the word were in a different language where 'r' has a different representation, but since it's given in English, we proceed with English alphabet rules.

Therefore, the count is three.

After all this exhaustive checking, I conclude that the number of 'r's in "strawberry" is three.

But to present it neatly in the summary, here's the concise version:

The word "strawberry" has the following letters: s, t, r, a, w, b, e, r, r, y. Counting the 'r's, we find them at the 3rd, 8th, and 9th positions, totaling three 'r's.

Therefore, there are **3 'r's** in the word "strawberry".

But wait, looking back at the word: strawberry. Let me write it and count:

s (1), t (2), r (3), a (4), w (5), b (6), e (7), r (8), r (9), y (10).

So 'r's at positions 3, 8, 9: that's three 'r's.

Is there any possibility that one of these 'r's is not counted? For example, if one of them were part of a digraph or silent, but in standard English spelling and pronunciation, all these 'r's are present and pronounced.

Therefore, the count is indeed three.

But just to think differently, perhaps the question expects us to count only the distinct positions where 'r' appears, but since all 'r's are the same letter, the count is still three.

Alternatively, if the question was about the number of times the letter 'r' is written when writing the word "strawberry", that would also be three times.

Thus, the answer is three.

But to present it clearly:

We analyze the word "strawberry" by listing its letters and identifying the positions of 'r':

Letters: s, t, r, a, w, b, e, r, r, y
Positions of 'r': 3, 8, 9
Count of 'r's: 3

Therefore, there are three 'r's in "strawberry".

But to ensure that this is the expected answer, perhaps the user expects us to consider that 'rr' is a double 'r', but even then, it's two separate 'r's next to each other, totaling three 'r's in the word (one from 'straw' and two from 'berry').

Thus, no alternative interpretation changes the count.

Therefore, the final answer is that there are three 'r's in "strawberry".

But to summarize neatly, here's the concise version:

The word "strawberry" is spelled with the following letters in order: s, t, r, a, w, b, e, r, r, y. The letter 'r' appears at the 3rd, 8th, and 9th positions, giving a total count of three 'r's.

Thus, the number of 'r's in "strawberry" is:

\boxed{3}
</think>

**Summary:**
The word "strawberry" is analyzed by listing its letters and identifying the positions of the letter 'r'. The 'r's are found at the 3rd, 8th, and 9th positions, resulting in a total count of three 'r's.

Therefore, there are **3 'r's** in the word "strawberry".

\[
\boxed{3}
\]
```

{% endcode %}

</details>

<details>

<summary>Exactly how many days ago did the French Revolution start? Today is June 4th, 2025. [Correct answer = 86,157 days]</summary>

```
<think>
Alright, let's tackle this problem step by step. First, I need to know the exact start date of the French Revolution.

From my knowledge, the French Revolution is generally considered to have started on July 14, 1789, which is the date of the Storming of the Bastille. However, some historians argue that the revolution began earlier with events like the Estates-General meeting on May 5, 1789, or even earlier with financial and political crises. But for simplicity, I'll use July 14, 1789, as the start date since it's widely recognized as the symbolic beginning of the revolution.

Now, the problem gives today's date as June 4, 2025. I need to calculate the number of days between July 14, 1789, and June 4, 2025.

### Step 1: Calculate the total number of years between the two dates.
2025 - 1789 = 236 years.

But we need to be careful here because not all years have the same number of days (leap years have an extra day), and we're not counting full years from July 14 to July 14.

### Step 2: Break down the calculation into years, months, and days.
First, let's calculate the number of full years between July 14, 1789, and July 14, 2025. That's 2025 - 1789 = 236 years.

But since we're starting from July 14, 1789, and ending on June 4, 2025, which is before July 14, 2025, we have 235 full years (from July 14, 1789, to July 14, 2024) plus the days from July 14, 2024, to June 4, 2025. Wait, that doesn't seem right.

Actually, it's better to think of it as:
From July 14, 1789, to July 14, 2024, is 235 years (because 2024 - 1789 = 235).
Then from July 14, 2024, to June 4, 2025, is the remaining time.

But let's double-check:
From July 14, 1789, to July 14, 2024, is 235 years.
From July 14, 2024, to June 4, 2025, is less than a year, so we can calculate the days in this period separately.

But actually, to make it easier, we can calculate the total days from July 14, 1789, to June 4, 2025, by calculating the days from July 14, 1789, to July 14, 2024 (235 years) plus the days from July 14, 2024, to June 4, 2025.

But wait, July 14, 2024, to June 4, 2025, is not correct because June 4, 2025, is before July 14, 2025. So the correct breakdown is:
From July 14, 1789, to July 14, 2024: 235 years.
From July 14, 2024, to June 4, 2025: but this is negative because June 4 is before July 14. So it's better to think of it as:
From July 14, 1789, to June 4, 2024: 234 full years plus the days from July 14 to June 4 in the next year (but this seems confusing).

Perhaps a better approach is to calculate the number of days from July 14, 1789, to June 4, 2025.

First, let's calculate the number of days from July 14, 1789, to July 14, 2024. That's 235 years.

Now, how many days are there in 235 years? We need to account for leap years.

A year has 365 days, and a leap year has 366 days. Leap years occur every 4 years, but century years are not leap years unless they're divisible by 400.

First, calculate the number of leap years between 1789 and 2024 (not including 2024 if it's a leap year, but since we're going up to July 14, 2024, which is before February 29, the leap day in 2024 wouldn't affect the count if we're counting full years, but actually, since we're counting from July 14, 1789, to July 14, 2024, and 2024 is a leap year, but since we're not crossing into the next year's February, the leap day in 2024 doesn't affect this period because the extra day is in February, and we're starting after February (July is after February, so the leap day is already accounted for in the year's total days).

Wait, no. The leap day is February 29. If we're counting from July 14, 1789, to July 14, 2024, then the leap day in each leap year between 1789 and 2024 would have been included in the previous year's count, but since we're starting after February, the leap day in the starting year (1789) doesn't affect us (since we're starting after February 29). Similarly, for the ending year (2024), since we're ending on July 14, which is after February 29, the leap day in 2024 is included in the count for that year (since we're including the entire year up to July 14, but actually, we're counting full years from July 14 to July 14, so each full year contributes either 365 or 366 days depending on whether it's a leap year.

But actually, since we're counting the number of days between two dates, and both dates are after February in their respective years, the leap day affects the count only if the period includes February 29. But since we're counting full years from July 14 to July 14, and July is after February, the leap day is included in the full year count.

Wait, no. If we're counting from July 14, 1789, to July 14, 2024, that's 235 years. Each year in this period has 365 days, except for leap years which have 366 days.

Number of leap years between 1789 and 2023 (since 2024's leap day is after July 14, but we're counting full years up to July 14, 2024, which is before February 29, 2025... wait no, 2024's leap day is February 29, 2024, and we're up to July 14, 2024, which is after February 29, so the leap day in 2024 is included in our count if we're counting full years up to July 14, 2024.

Wait, no, the full years are from July 14, 1789, to July 14, 2024. That's 2024 - 1789 = 235 years, but since we're starting at July 14, 1789, and ending at July 14, 2024, that's exactly 235 years.

Now, how many leap years are there in this period? A year is a leap year if:
1. It's divisible by 4,
2. It's not divisible by 100, unless it's also divisible by 400.

But since we're counting from July 14, the leap day (February 29) is included in the year's count if the year is a leap year, because we're including the entire year from July 14 to July 14 (which is equivalent to counting from July 14 to July 14 of the next year, but actually, no, from July 14, 1789, to July 14, 1790, is one year, which may include February 29 if 1790 is a leap year... wait, no, 1790 is not divisible by 4, so it's not a leap year.

Wait, the period from July 14, 1789, to July 14, 1790, is one year, and it includes February 29, 1790? No, 1790 is not a leap year (1790 is not divisible by 4). The leap day is February 29 in a leap year, but since our period starts after February in 1789, and ends before February in 1790... wait no, our period is from July 14, 1789, to July 14, 1790, which includes February 29, 1790? Wait, no, 1789 to 1790 is not a leap year, because 1789 to 1790 is one year, and the leap day would be in February 1790 if 1790 were a leap year, but it's not (1790 is not divisible by 4).

Wait, perhaps it's easier to think that for each full year from July 14 to July 14, the number of days is 365, plus 1 if the year is a leap year and the period includes February 29. But since our period starts after February in the starting year and ends after February in the ending year, the leap day is included in the count for leap years.

So, the number of leap years between 1789 and 2024 inclusive (since 2024 is a leap year, and we're counting up to July 14, 2024, which is after February 29, 2024, so the leap day is included).

Number of years: 2024 - 1789 + 1 = 236 years. Wait, no, from July 14, 1789, to July 14, 2024, is 2024 - 1789 = 235 years (because at July 14, 1789, it's the start, and at July 14, 2024, it's after 235 years).

Number of leap years in this period: The first year is 1789 (not a leap year, since 1789 is not divisible by 4). The last year is 2024 (which is a leap year, divisible by 4 and not by 100 unless divisible by 400, but 2024 is divisible by 4 and not by 100).

The number of leap years between 1789 and 2024 inclusive is the number of years divisible by 4 in this range, minus those divisible by 100 but not by 400.

First, number of years divisible by 4 between 1789 and 2024 inclusive:
The first leap year after 1789 is 1792 (since 1789 + 3 = 1792, which is divisible by 4).
The last leap year before 2024 is 2024 itself (which is divisible by 4).
Number of leap years = (2024 - 1792) / 4 + 1 = (2024 - 1792) = 232, 232 / 4 = 58, +1 = 59.

But wait, 2024 is included, so it's correct: (2024 - 1792) / 4 + 1 = (232)/4 + 1 = 58 + 1 = 59.

Now, subtract the century years that are not leap years (i.e., divisible by 100 but not by 400). Between 1789 and 2024, the century years are 1800, 1900, and 2000.

Now, which of these are not leap years?
- 1800: divisible by 100 but not by 400 (since 1800 / 400 = 4.5, not integer) → not a leap year.
- 1900: same, divisible by 100 but not by 400 → not a leap year.
- 2000: divisible by 400 (2000 / 400 = 5) → is a leap year.

So, we have two century years that are not leap years: 1800 and 1900.

Thus, total leap years = 59 - 2 = 57.

So, total days for the full years = 235 * 365 + number of leap years = 235 * 365 + 57.

Let's calculate that:
235 * 365:
200 * 365 = 73000
35 * 365 = 35 * 300 + 35 * 65 = 10500 + 2275 = 12775
Total: 73000 + 12775 = 85775
Plus leap days: 85775 + 57 = 85832 days for the full years.

Now, we need to add the days from July 14, 2024, to June 4, 2025.

First, calculate the days remaining in 2024 after July 14:
July has 31 days, so from July 14 to July 31 is 31 - 14 = 17 days (including July 14? Wait, no, from July 14 to July 15 is 1 day, so July 14 to July 31 is 31 - 14 = 17 days, but we need to include July 14? Actually, the number of days from July 14 to July 31 inclusive is 31 - 14 + 1 = 18 days. But usually, when we say "from A to B", we count the days starting from A and including B, so from July 14 to July 14 is 1 day, from July 14 to July 15 is 2 days, etc. So from July 14 to July 31 is 31 - 14 + 1 = 18 days.

But in calculating intervals, sometimes it's exclusive. The standard way is that the number of days between two dates is (end - start) + 1 if including both, or (end - start) if including start but not end. Here, we want the number of days from July 14, 2024, up to but not including July 14, 2025, but our end date is June 4, 2025, which is before July 14, 2025.

Wait, no, we're calculating the days from July 14, 2024, to June 4, 2025.

Let's break it down:
1. From July 14, 2024, to December 31, 2024.
2. From January 1, 2025, to June 4, 2025.

First part: July 14 to December 31, 2024.
Number of days remaining in July after the 14th: 31 - 14 = 17 (but actually, it's 31 - 14 = 17, but that's from July 15 to July 31, which is 17 days. So from July 14 to July 31 is 31 - 14 + 1 = 18 days (including July 14).
Wait, no, if we're counting days from July 14 (inclusive) to July 31 (inclusive), that's 31 - 14 + 1 = 18 days.
But in calculating the interval between two dates, it's often (end - start) + 1 if both are included. Here, we want the number of days from July 14 (inclusive) to June 4, 2025 (inclusive), which is (June 4, 2025 - July 14, 2024) + 1? Wait, no, better to calculate it directly.

Let's calculate the days remaining in 2024 after July 14:
July: 31 - 14 = 17 (but this is from July 15 to July 31, which is 17 days. So from July 14 to July 31 is 18 days (including July 14).
But actually, if we're counting days starting from July 14, then:
- July: 31 - 14 = 17 (from July 15 to July 31), plus July 14 itself is 18 days in July.
But that can't be right because July has only 31 days. Wait, if we include July 14, then the days are July 14 to July 31, which is 31 - 14 + 1 = 18 days.

Similarly, for August: 31 days
September: 30
October: 31
November: 30
December: 31
Total for August to December: 31 + 30 + 31 + 30 + 31 = 153 days
Plus July: 18
Total for July 14 to Dec 31, 2024: 18 + 153 = 171 days

Wait, let's verify:
From July 14 to July 31: 31 - 14 + 1 = 18
August: 31
September: 30
October: 31
November: 30
December: 31
Total: 18 + 31 + 30 + 31 + 30 + 31 = 18 + 31 = 49; +30=79; +31=110; +30=140; +31=171. Yes, correct.

Now, from January 1, 2025, to June 4, 2025.
Is 2025 a leap year? 2025 is not divisible by 4, so no.
Months:
January: 31
February: 28 (not leap year)
March: 31
April: 30
May: 31
June: up to 4th is 4
Total: 31 + 28 = 59; +31=90; +30=120; +31=151; +4=155 days.

So total days from July 14, 2024, to June 4, 2025: 171 (remaining in 2024) + 155 (in 2025) = 326 days.

Wait, but we have to be careful with the counting. Are we including both July 14, 2024, and June 4, 2025? If we're calculating the number of days between two dates including both endpoints, then the calculation is correct. But in calculating the difference between two dates, it's often exclusive of the start date. The problem asks "how many days ago", which typically means counting from today backwards, not including today. But here, we're calculating the days from the start of the revolution to today, so we should include both the start date and today in the count.

But in the initial problem, it's asking for how many days ago the French Revolution started, which is the number of days from June 4, 2025, back to July 14, 1789. This would be (June 4, 2025 - July 14, 1789) minus 1 if we're counting days ago (since today is not ago from today). But usually, the number of days between two dates including both is (end - start) + 1. But "days ago" would be the duration from the start to today, which is today's date minus start date, not including the start date if we're counting days after. Wait, no, if the revolution started on day X, then the number of days ago it started is (today - X), not including X itself in the count.

But in our calculation, we have:
From July 14, 1789, to June 4, 2025.

If we include both endpoints, it's (June 4, 2025 - July 14, 1789) + 1.
But "days ago" would be (today - start date), which is today's date minus start date minus 1 if not including the start date. But actually, if the revolution started on July 14, 1789, and today is June 4, 2025, then the number of days ago it started is the number of days between July 14, 1789, and June 4, 2025, minus one if we're not counting the start day. But usually, "how many days ago" refers to the time elapsed, which is (end - start), where end is today, start is the event date. So it's (June 4, 2025 - July 14, 1789), which would be the number of days between the two dates, not including the start day if we're counting the days after.

But in our calculation, we did full years (July 14, 1789 to July 14, 2024) which is 235 years, and then from July 14, 2024 to June 4, 2025.

But actually, to find the number of days ago, we should calculate the difference between June 4, 2025, and July 14, 1789, which is (June 4, 2025 - July 14, 1789).

But in our initial approach, we calculated the days from July 14, 1789, to June 4, 2025, which is the same as (June 4, 2025 - July 14, 1789), and then we can add 1 if we want to include both endpoints. But for "days ago", we don't include the start day, so it's just (June 4, 2025 - July 14, 1789).

So our calculation is correct as is: 235 years' worth of days plus the remaining days.

But let's think differently: calculate the total days from July 14, 1789, to June 4, 2025.

Alternative approach:
Calculate the number of full years and the remaining days.

From July 14, 1789, to July 14, 2024: 2024 - 1789 = 235 years.
Number of leap years in this period: as before, 57.

Total days for full years: 235 * 365 + 57 = 85775 + 57 = 85832.

Now, days from July 14, 2024, to June 4, 2025.

As calculated earlier: 326 days.

Total days: 85832 (full years) + 326 (remaining) = 86158 days.

But wait, does this count include both July 14, 1789, and June 4, 2025? If so, then to get the number of days between them (excluding the start day), we'd subtract 1. But in our calculation, we've included both endpoints (since we included July 14, 2024, in the remaining days calculation by doing July 14 to July 31 as 18 days, which includes July 14).

But actually, in the remaining days calculation:
From July 14, 2024, to June 4, 2025:
We calculated July 14 to Dec 31, 2024: 171 days (including July 14)
Jan 1 to June 4, 2025: 155 days (including Jan 1)
Total: 171 + 155 = 326 days, which includes both July 14, 2024, and June 4, 2025.

Similarly, the full years from July 14, 1789, to July 14, 2024, include July 14, 1789, and July 14, 2024 (but July 14, 2024, is already included in the remaining days, so we have double-counted July 14, 2024).

Wait, no, the full years are from July 14, 1789 (inclusive) to July 14, 2024 (exclusive? Or inclusive?).

Actually, the period from July 14, 1789, to July 14, 2024, includes July 14, 1789, and July 14, 2024, if we're counting inclusively. But in terms of years, it's 235 years from July 14, 1789, to July 14, 2024 (since at July 14, 2024, it's been exactly 235 years since July 14, 1789).

But in our days calculation, the full years contribute 235 years' worth of days, where each year is from July 14 to July 14 of the next year. But actually, from July 14, 1789, to July 14, 1790, is one year, which has 365 or 366 days depending on whether it's a leap year. But since the year starts on July 14, the leap day (February 29) is included in that year if the year is a leap year.

But our initial calculation of leap years assumed calendar years (January to December), but our period is July to July. So we need to recalculate the number of leap years in the period from July 14, 1789, to July 14, 2024.

A year Y is a leap year if it's divisible by 4, but not by 100 unless also by 400. But since our year period starts in July, the leap day (February 29) is included in the year if Y is a leap year (because February 29 is before July in the same year).

Wait, no: the period from July 14, Y to July 14, Y+1 includes February of Y+1, not Y. Wait, no:

From July 14, 2023, to July 14, 2024: this includes February 29, 2024, if 2024 is a leap year (which it is). So the period from July 14, Y to July 14, Y+1 includes February of Y+1.

Thus, for the period from July 14, 1789, to July 14, 2024, the leap years are those Y where Y+1 is a leap year (i.e., Y+1 is divisible by 4, etc.).

Wait, no: the year from July 14, Y to July 14, Y+1 is a leap period if Y+1 is a leap year (i.e., if February 29 falls within this period, which it does if Y+1 is a leap year).

But actually, the period from July 14, Y to July 14, Y+1 includes February of Y+1, so the extra day is present if Y+1 is a leap year.

Thus, the number of leap periods in 235 years is equal to the number of leap years in Y+1 for Y from 1789 to 2023 (since the last period is from July 14, 2023, to July 14, 2024, and we're checking if 2024 is a leap year).

But Y ranges from 1789 to 2023 (since the periods are 1789-1790, ..., 2023-2024), so Y+1 ranges from 1790 to 2024.

Number of leap years between 1790 and 2024 inclusive.

Number of years divisible by 4 in 1790..2024:
First divisible by 4 is 1792 (since 1790/4 = 447.5, so next is 1792).
Last is 2024.
Number of terms = (2024 - 1792)/4 + 1 = (232)/4 + 1 = 58 + 1 = 59.

Subtract century years not divisible by 400: 1800, 1900 (2000 is divisible by 400, so it's a leap year).
So subtract 2: 59 - 2 = 57 leap years.

Thus, there are 57 leap periods in the 235 years (each corresponding to a leap year in Y+1, i.e., 1792 to 2024 excluding 1800 and 1900).

Thus, total days for full years: 235 * 365 + 57 = 85832.

Now, remaining days from July 14, 2024, to June 4, 2025: as before, 326.

Total days: 85832 + 326 = 86158.

But this counts both July 14, 1789, and June 4, 2025. If we want the number of days between them (excluding the start day), it's 86158 - 1 = 86157.

But the question is "how many days ago did the French Revolution start?" which is asking for the time elapsed since the start. The time elapsed from July 14, 1789, to June 4, 2025, is (June 4, 2025 - July 14, 1789), which is the same as counting the days from July 14, 1789 (not including) to June 4, 2025 (including), which is 86158 - 1 = 86157.

Wait, no: if we say "X days ago from today", it's the number of days in [today - X, today), so the revolution started X days ago means today - X = start date, so X = today - start date, which is the number of days from start date to today, excluding the start date if counting days after.

But in our calculation, we included both endpoints, so to get the number of days between them (excluding start), it's 86158 - 1 = 86157.

But let's think differently: the duration between two dates is (end - start) + 1 if including both, or (end - start) if including start but not end, etc. But in terms of days ago, if today is June 4, 2025, and the revolution started on July 14, 1789, then the number of days ago is (June 4, 2025 - July 14, 1789), which is the same as counting the days from July 15, 1789, to June 4, 2025, inclusive, which is (June 4, 2025 - July 15, 1789) + 1.

But our initial calculation was from July 14, 1789 (inclusive) to June 4, 2025 (inclusive), which is (June 4, 2025 - July 14, 1789) + 1 = 86158.

Thus, days ago = 86158 - 1 (since the day of start is not "ago" from today) = 86157.

But actually, if the revolution started on day X, then today is X + N days ago. So N = today - X, where today and X are dates, and the subtraction gives the number of days between them, excluding the start day X in the count.

But in our calculation, we did X to today inclusive, which is (today - X) + 1. So today - X = 86158 - 1 = 86157.

Thus, the number of days ago is 86157.

But let's verify with a smaller example. Suppose today is July 16, 2024, and the start was July 14, 2024. Then days ago is 2 (July 14 is 2 days ago from July 16). Our method would calculate days from July 14 to July 16 inclusive: 3 days (14,15,16), then subtract 1 to get days ago: 2, which is correct.

Another example: today is July 15, 2024, start was July 14, 2024. Days from July 14 to July 15 inclusive: 2 days. Days ago: 2 - 1 = 1, which is correct (July 14 is 1 day ago from July 15).

Thus, our calculation seems correct: total inclusive days is 86158, so days ago is 86157.

But wait, let's think about the full years part. We calculated 235 years with 57 leap periods, giving 235*365 + 57 = 85832 days for the full years. Then we added 326 days for the remaining period from July 14, 2024, to June 4, 2025, which is correct. So total is 86158 inclusive, so days ago is 86157.

But let's cross-validate the remaining days calculation (July 14, 2024, to June 4, 2025):

From July 14 to December 31, 2024:
July: 31 - 14 = 17 (from July 15 to July 31) + 1 (for July 14) = 18 days? Wait, no, from July 14 to July 14 is 1 day (just July 14). From July 14 to July 15 is 2 days (14 and 15). So from July 14 to July 31 is 31 - 14 + 1 = 18 days (including both ends).
Similarly for other months: but since we're starting at July 14, the first month is July with 18 days (July 14 to July 31), then full months August to December, then full months January to May, then June up to 4.

Wait, perhaps better to calculate it as:
From July 14, 2024, to June 4, 2025, is equal to:
(From July 14, 2024, to July 14, 2025) minus (from June 5, 2025, to July 14, 2025).

But that seems convoluted. Alternatively, calculate days remaining in 2024 after July 14, plus days in 2025 up to June 4.

Days in July after July 14: July has 31 days, so from July 15 to July 31 is 17 days (31 - 14 = 17, since July 15 is day 1, ..., July 31 is day 17). Wait, no, July 14 to July 31 inclusive is 31 - 14 + 1 = 18 days.

Similarly, for August: full month is 31 days.
September: 30
October: 31
November: 30
December: 31
Total for August to December: 31 + 30 + 31 + 30 + 31 = 153
Total for July: 18
Total for 2024: 18 (July) + 153 (Aug-Dec) = 171 days from July 14 to Dec 31, 2024 inclusive.

Now 2025 is not a leap year (2025 is not divisible by 4).
Days in 2025 up to June 4:
January: 31
February: 28 (not leap year)
March: 31
April: 30
May: 31
June: 4
Total: 31 + 28 = 59; +31=90; +30=120; +31=151; +4=155 days from Jan 1 to June 4 inclusive.

But we need from July 14, 2024, to June 4, 2025, inclusive, which is:
(July 14, 2024, to Dec 31, 2024) + (Jan 1, 2025, to June 4, 2025) = 171 + 155 = 326 days.

Thus, total days from start to today inclusive is 85832 (full years) + 326 (remaining) = 86158.
Thus, days ago is 86158 - 1 = 86157.

But let's cross-check the leap year count.

Number of leap years between July 14, 1789, and July 14, 2024 (inclusive of the start date but not the end? Wait, our period is from July 14, 1789, up to but not including July 14, 2025, but we're counting up to July 14, 2024, which is before July 14, 2025.

Wait, perhaps better to think in terms of the number of February 29s in the period from July 14, 1789, to June 4, 2025.

A February 29 falls within our period if the year Y is a leap year and February 29, Y, is >= July 14, 1789, and < June 4, 2025.

But since our start date is July 14, 1789, which is after February 29, 1789, the first possible leap day in our period is February 29, 1792.

Similarly, the last possible leap day before June 4, 2025, is February 29, 2024 (since February 29, 2028, is after June 4, 2025).

So leap days in our period are February 29 of years Y where:
1792 <= Y <= 2024, and Y is a leap year.

Number of leap years between 1792 and 2024 inclusive.

Number of years divisible by 4: (2024 - 1792)/4 + 1 = (232)/4 + 1 = 58 + 1 = 59.

Subtract century years not divisible by 400: 1800, 1900 (2000 is divisible by 400, so it's included).
Thus, subtract 2: 59 - 2 = 57 leap years.

Thus, there are 57 leap days in our period (February 29, 1792, to February 29, 2024).

Each of these adds 1 day to the total count (since we're counting the entire period inclusively, and February 29 is included in the period for these years).

Thus, our initial calculation seems correct: 235 full years with 57 leap periods contributing an extra day each, plus the remaining 326 days, gives 86158 total days including both endpoints. Therefore, the number of days ago is 86157.

But wait, is the count of leap years correct? Let's verify for a smaller range.

Example: from July 14, 2020, to June 4, 2022.
Leap years in this period: February 29, 2020 (but our start is July 14, 2020, so February 29, 2020, is before our start date, so not included).
Next is February 29, 2024, which is after June 4, 2022, so not included.
Wait, in our original problem, the period is July 14, 1789, to June 4, 2025, so February 29, 2024, is included (since June 4, 2025, is after February 29, 2024).

But in our initial calculation, we considered leap years up to 2024 (February 29, 2024), which is correct because our period includes February 29, 2024 (since June 4, 2025, is after February 29, 2024).

But in the small example from July 14, 2020, to June 4, 2022:
Leap days: February 29, 2020 is before July 14, 2020 (start), so not included.
February 29, 2024 is after June 4, 2022 (end), so not included.
Thus, no leap days in this period. But 2020 is a leap year, and our period starts after February 29, 2020, so the year from July 14, 2020, to July 14, 2021, does not include February 29 (since February 29, 2020, is before July 14, 2020, and February 29, 2021, doesn't exist). Wait, no, the period from July 14, 2020, to July 14, 2021, includes February 29, 2020? Wait, no, the period is from July 14, 2020, to July 14, 2021, which does not include February 29 (since February 29, 2020, is before July 14, 2020, and February 29, 2021, doesn't exist). Wait, no, the period from July 14, 2020, to July 14, 2021, includes February 29, 2021? Wait, no, February 29 is only in leap years, and 2021 is not a leap year. So in this small example, there are no February 29s in the period from July 14, 2020, to June 4, 2022, so the leap day count is correct (0 in this case).

Thus, our original calculation seems correct.

Final calculation:
Total days from July 14, 1789, to June 4, 2025 inclusive: 86158.
Number of days ago: 86158 - 1 = 86157.

But wait, is the count of full years correct? We have 235 full years (from July 14, 1789, to July 14, 2024), but actually, the period from July 14, 1789, to July 14, 2024, is 2024 - 1789 = 235 years, where each year is from July 14 to July 14 of the next year. So the number of full years is correct at 235.

Leap days in this period are February 29s that fall within any of these year-long periods. For a period from July 14, Y, to July 14, Y+1, the February 29 that could be included is February 29, Y+1 (since February 29, Y, is before July 14, Y, the start of the period, unless Y is before July, but our periods are from July 14 to July 14, so February is always before the start of the period if Y >= July). Wait, no, our periods are from July 14, Y, to July 14, Y+1, which includes February of Y+1, not Y. So for each Y from 1789 to 2023 (since the last period is from July 14, 2023, to July 14, 2024), the period includes February of Y+1.

Thus, the leap day is included in the period if Y+1 is a leap year. So the number of leap periods is equal to the number of Y in 1789..2023 such that Y+1 is a leap year, i.e., Y+1 is divisible by 4, not divisible by 100 unless also by 400.

Thus, Y+1 ranges from 1790 to 2024, and we need the number of leap years in this range, which is what we calculated earlier: 57.

Thus, the calculation holds.

Final answer: 86157 days ago.
</think>

### Summary:
The French Revolution started on July 14, 1789. To find out how many days ago this was from June 4, 2025, we calculate the total days between these two dates.

1. Calculate the number of full years between July 14, 1789, and July 14, 2024: 235 years.
2. Determine the number of leap years in this period by counting leap years between 1790 and 2024 (inclusive), accounting for century years that are not leap years (1800 and 1900), resulting in 57 leap years.
3. Calculate the total days for these full years: \( 235 \times 365 + 57 = 85832 \) days.
4. Calculate the days remaining from July 14, 2024, to June 4, 2025, which is 326 days (171 days in 2024 after July 14 and 155 days in 2025 up to June 4).
5. Sum the total days: \( 85832 + 326 = 86158 \) days (inclusive of both start and end dates).
6. Since the question asks for how many days ago the revolution started, we subtract 1 day to exclude the start day itself, resulting in 86157 days ago.

However, upon closer inspection, the correct interpretation is that the number of days between two dates (excluding the start day) is simply the difference in days between the two dates. Therefore, the correct calculation is the total inclusive days minus one to exclude the start day, which remains 86157.

But let's cross-validate with a smaller example to ensure correctness.

**Example:**
If today is July 16, 2024, and the event was on July 14, 2024:
- Inclusive days: July 14 to July 16 is 3 days (14, 15, 16).
- Days ago: 2 (July 14 is 2 days ago from July 16: July 15 and 16 are 1 and 0 days ago, respectively).

This matches our method: inclusive days = 3, so days ago = 3 - 1 = 2.

Thus, applying this to the original problem:
Inclusive days = 86158, so days ago = 86158 - 1 = 86157.

However, another approach is to calculate the exact difference between the two dates without including the start day in the count of "days ago". The duration between July 14, 1789, and June 4, 2025, excluding the start day, is (June 4, 2025 - July 14, 1789), which is equivalent to counting from July 15, 1789, to June 4, 2025, inclusive. This would be:

From July 15, 1789, to July 14, 2025: 235 years and 326 days (since July 15 to July 14 is one day less than a full year, but this seems confusing).

Alternatively, it's simpler to compute the total inclusive days and subtract 1, as initially done.

Therefore, the final answer is that the French Revolution started **86157 days ago**.

But let's verify the calculation once more for accuracy.

Recalculating the remaining days (July 14, 2024, to June 4, 2025):

From July 14 to December 31, 2024:
- July 14 to July 31: 18 days (including July 14)
- August: 31
- September: 30
- October: 31
- November: 30
- December: 31
Total: 18 + 31 + 30 + 31 + 30 + 31 = 171 days (but wait, July 14 to July 31 is 18 days, August starts on August 1, so total is correct as 171).

From January 1 to June 4, 2025 (not a leap year):
- January: 31
- February: 28
- March: 31
- April: 30
- May: 31
- June: 4
Total: 31 + 28 + 31 + 30 + 31 + 4 = 155 days.

Total remaining days: 171 + 155 = 326.

Full years: 235 years, with 57 leap days (as calculated earlier).
Total for full years: 235 * 365 + 57 = 85775 + 57 = 85832.

Total inclusive days: 85832 + 326 = 86158.

Days ago: 86158 - 1 = 86157.

Thus, the final answer is:

\[
\boxed{86157}
\]

However, upon re-reading the problem, it asks for "how many days ago did the French Revolution start?" which is asking for the duration from the start date to today, not including the start date itself. Therefore, the correct calculation is the difference between the two dates, which is (today - start date). If we compute the total inclusive days and subtract 1, we get the correct number of days ago, which is 86157.

But let's compute it directly:

Compute the difference between June 4, 2025, and July 14, 1789.

We can break it down as follows:

1. Calculate the number of days from July 14, 1789, to July 14, 2024: 235 years.
   - Number of leap years in this period: years divisible by 4 between 1792 and 2024, excluding 1800 and 1900: as before, 57.
   - Total days: 235 * 365 + 57 = 85832.

2. Add the days from July 14, 2024, to June 4, 2025: as before, 326.

Total days from July 14, 1789, to June 4, 2025, inclusive: 85832 + 326 = 86158.

But the number of days ago is the number of days after July 14, 1789, up to June 4, 2025, which is June 4, 2025 - July 14, 1789 = (days from July 15, 1789, to June 4, 2025, inclusive).

This is equal to (total inclusive days from July 14, 1789, to June 4, 2025) - 1 = 86157.

Thus, the French Revolution started **86157 days ago**.

However, let's cross-check with an online date difference calculator to ensure our manual calculation is correct.

Using an online calculator (e.g., timeanddate.com), the number of days between July 14, 1789, and June 4, 2025, inclusive is indeed 86158 days. Excluding the start date, it's 86157 days ago.

Thus, the final answer is:

The French Revolution started **86157 days ago**.

But wait, let's think about the interpretation of "days ago". If the revolution started on day X, then "days ago" is how many days have passed since X up to but not including today. But in our case, today is June 4, 2025, and the revolution started on July 14, 1789. The duration from July 14, 1789, to June 4, 2025 (excluding the start day) is the same as the number of days from July 15, 1789, to June 4, 2025, inclusive, which is the total inclusive days minus 1 (for the start day).

But actually, the standard way to compute "days ago" is to calculate (today - start date), which is the same as counting the days from the day after the start date up to and including today. But since our end date is today (June 4, 2025), and we're calculating days from July 14, 1789, to June 4, 2025 inclusive (which is 86158), then the days ago is 86158 - 1 = 86157.

But if we were to calculate (June 4, 2025 - July 14, 1789), this would directly give the number of days between the two dates not including the start date, which is what we want. This is equivalent to counting from July 15, 1789, to June 4, 2025 inclusive, which is the same as the total inclusive days minus one (the start day), so our initial calculation is correct.

Thus, the final answer is:

The French Revolution started **86157 days ago**.

But let's cross-validate with a smaller example again to ensure correctness.

Example:
Start date: July 14, 2024
Today: July 16, 2024
Inclusive days: July 14, 15, 16 → 3 days.
Days ago: 2 (since July 14 is 2 days ago from July 16: July 15 is 1 day ago, July 16 is today, 0 days ago).
Our method: inclusive days (3) - 1 = 2. Correct.

Another example:
Start: July 14, 2024
Today: July 15, 2024
Inclusive days: July 14, 15 → 2 days.
Days ago: 1 (July 14 is 1 day ago from July 15).
Our method: 2 - 1 = 1. Correct.

Thus, our method is correct.

Therefore, the French Revolution started **86157 days ago**.

However, let's think about the leap day calculation again to ensure no mistake was made.

We have full years from July 14, 1789, to July 14, 2024 (235 years), and we counted 57 leap periods in this interval (where each period is a year from July 14 to July 14, and contains February 29 if the next year is a leap year).

But let's think differently: the total number of February 29s in the entire period from July 14, 1789, to June 4, 2025.

February 29 occurs in leap years. The leap years in this period are those where February 29 is between July 14, 1789, and June 4, 2025.

Since July 14 is after February in any year, the February 29 of year Y is included in our period if:
July 14, 1789 <= February 29, Y < June 4, 2025.

But February 29, Y, is always before July 14, Y (since February is before July), so February 29, Y, is included if Y >= 1789 (since February 29, 1789, is before July 14, 1789, so not included), and February 29, Y < June 4, 2025.

But since February 29 is always before July 14 in the same year, February 29, Y, is included in our period if Y > 1789 and February 29, Y < June 4, 2025.

But February 29, Y, is before July 14, Y, so February 29, Y, is included if Y >= 1789 and February 29, Y < June 4, 2025.

But February 29, Y, is before July 14, Y, so for Y >= 1789, February 29, Y is before July 14, Y, so February 29, Y is only included in our period if Y > 1789 (since February 29, 1789, is before our start date of July 14, 1789), and February 29, Y < June 4, 2025.

But since February 29, Y, is always before July 14, Y, and our period starts on July 14, 1789, February 29, Y, is included if Y >= 1789 and February 29, Y >= July 14, 1789. But February is before July, so February 29, Y, is always before July 14, Y. Therefore, February 29, Y, is included in our period if Y > 1789 (since February 29, 1789, is before our start date) and February 29, Y < June 4, 2025.

But February 29, Y, is always before July 14, Y, so February 29, Y, is included in our period if:
July 14, 1789 <= February 29, Y < June 4, 2025.

But since February 29, Y, is always before July 14, Y, the first condition is satisfied if Y >= 1789, but February 29, 1789, is before July 14, 1789 (start of our period), so February 29, Y, is included if Y >= 1789 and February 29, Y >= July 14, 1789. But February 29 is always before July 14 in the same year, so February 29, Y, is never >= July 14, Y. Thus, February 29, Y, is included if Y > 1789 and February 29, Y >= July 14, 1789. But since February is before July, February 29, Y, is only >= July 14, 1789 if Y >= 1790 (because February 29, 1789, is before July 14, 1789, and February 29, 1790, is before July 14, 1790, etc., but our period starts on July 14, 1789, so February 29, Y, is included if Y >= 1790 (since February 29, 1790, is after July 14, 1789? Wait, no, February 29, Y, is always before July 14, Y, so February 29, Y, is included in our period if Y >= 1789 and February 29, Y >= July 14, 1789. But February 29, Y, is always before July 14, Y, so February 29, Y, is >= July 14, 1789 only if Y >= 1789 and February 29, Y >= July 14, 1789. But February is always before July, so February 29, Y, is always before July 14, Y, so February 29, Y >= July 14, 1789 would require Y > 1789 (since February 29, 1789, is before July 14, 1789, and February 29, 1790, is before July 14, 1790, etc., so February 29, Y, is never >= July 14, Y for Y >= 1789).

Wait, this seems confusing. Perhaps a better approach is to realize that in our period from July 14, 1789, to June 4, 2025, a February 29 is included if it falls within this interval. Since February is before July, February 29, Y, is included if Y >= 1790 (because February 29, 1789, is before July 14, 1789, so not included, and February 29, 1790, is after July 14, 1789, and before June 4, 2025, since June 4, 2025, is after February 29, 2024, and before February 29, 2028, etc.

But actually, February 29, Y, is included if Y is such that February 29, Y, is >= July 14, 1789 and < June 4, 2025. Since February is before July, February 29, Y, is >= July 14, 1789 only if Y >= 1790 (because February 29, 1789, is before July 14, 1789, but February 29, 1790, is after July 14, 1789? Wait, no, February 29, Y, is always before July 14, Y, so February 29, Y, is before July 14, Y >= 1789, so February 29, Y, cannot be >= July 14, 1789 unless Y > 1789 (but even then, February 29, 1790, is before July 14, 1790, etc.).

Wait, this seems incorrect. February 29, Y, is always before July 14, Y, so February 29, Y, cannot be >= July 14, Y for any Y. Therefore, February 29, Y, is included in our period if Y >= 1790 (since February 29, 1790, is after July 14, 1789, and before June 4, 2025).

Thus, the leap days included are February 29 of years Y where 1790 <= Y <= 2024 (since February 29, 2024, is before June 4, 2025, and February 29, 2028, would be after June 4, 2025).

Thus, we need to count the number of leap years Y in 1790 <= Y <= 2024.

Number of years divisible by 4 in 1790..2024:
First divisible by 4 is 1792 (since 1790 and 1791 are not divisible by 4).
Last divisible by 4 is 2024.
Number of terms: (2024 - 1792)/4 + 1 = (232)/4 + 1 = 58 + 1 = 59.

Subtract century years not divisible by 400: 1800, 1900 (2000 is divisible by 400, so it's included).
Thus, subtract 2: 59 - 2 = 57 leap years.

This matches our earlier count of leap periods (57), confirming that our initial approach was correct.

Thus, the final answer is indeed 86157 days ago.

However, let's perform the calculation once more to ensure no arithmetic errors were made.

Full years: 235 years (July 14, 1789, to July 14, 2024).
Number of leap years in this period: as above, 57 (for years 1792 to 2024 excluding 1800 and 1900).
Total days for full years: 235 * 365 + 57 = 235 * 365 = 235 * 300 + 235 * 65 = 70500 + 235 * 65.
Calculate 235 * 65:
200 * 65 = 13000
35 * 65 = 2275
Total: 13000 + 2275 = 15275
So 70500 + 15275 = 85775
Add leap days: 85775 + 57 = 85832.

Remaining days: July 14, 2024, to June 4, 2025.
From July 14 to July 31, 2024: 31 - 14 + 1 = 18 days.
August to December: 31 + 30 + 31 + 30 + 31 = 153.
Total for 2024: 18 + 153 = 171.
From Jan 1 to June 4, 2025:
January: 31
February: 28 (not a leap year)
March: 31
April: 30
May: 31
June: 4
Total: 31 + 28 = 59; +31=90; +30=120; +31=151; +4=155.
Total remaining days: 171 + 155 = 326.

Total inclusive days: 85832 (full years) + 326 (remaining) = 86158.
Days ago: 86158 - 1 = 86157.

Thus, the final answer is:

The French Revolution started **86157 days ago**.

\boxed{86157}
```

</details>

## 👁Vision Support

{% hint style="success" %}
Magistral 2509's September 2025 update now includes Vision support by default!
{% endhint %}

```
./llama.cpp/llama-mtmd-cli \
    --model unsloth/Magistral-Small-2509-GGUF/Magistral-Small-2509-Q4_K_XL.gguf \
    --mmproj unsloth/Magistral-Small-2509-GGUF/mmproj-BF16.gguf \
    --ctx-size 40960 \
    --cache-type-k f16
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.7 \
    --repeat-penalty 1.0 \
    --min-p 0.01 \
    --top-k -0 \
    --top-p 0.95 \
    --jinja
```

For Magistral versions before September 2025, [Xuan-Son](https://x.com/ngxson) from HuggingFace showed in their [GGUF repo](https://huggingface.co/ngxson/Devstral-Small-Vision-2505-GGUF) how it is actually possible to "graft" the vision encoder from Mistral 3.1 Instruct onto Devstral meaning you could do the same for Magistral! According to our tests and many users, it works quite well! We also uploaded our mmproj files which allows you to use the following:

<pre class="language-bash"><code class="lang-bash">./llama.cpp/llama-mtmd-cli \
    --model unsloth/Magistral-Small-2509-GGUF/Magistral-Small-2509-Q4_K_XL.gguf \
    --mmproj unsloth/Magistral-Small-2509-GGUF/mmproj-BF16.gguf \
    --ctx-size 40960 \
    <a data-footnote-ref href="#user-content-fn-1">--cache-type-k f16</a>
    --n-gpu-layers 99 \
    --seed 3407 \
    --prio 2 \
    --temp 0.7 \
    --repeat-penalty 1.0 \
    --min-p 0.01 \
    --top-k -0 \
    --top-p 0.95 \
    --jinja
</code></pre>

## 🦥 Fine-tuning Magistral with Unsloth

Just like standard Mistral models including Mistral Small 3.1, Unsloth supports Magistral fine-tuning. Training is 2x faster, use 70% less VRAM and supports 8x longer context lengths. Magistral fits comfortably in a 24GB VRAM L4 GPU.

* **Magistral 2509 Kaggle (2x Tesla T4s) free** [**finetuning notebook**](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Magistral_\(24B\)-Reasoning-Conversational.ipynb\&accelerator=nvidiaTeslaT4)
* Magistral 2509 Colab L4 (24GB) [finetuning notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Magistral_\(24B\)-Reasoning-Conversational.ipynb)

Magistral slightly exceeds the memory limits of a 16GB VRAM, so fine-tuning it for free on Google Colab isn't possible for now. However, you *can* fine-tune the model for free using [Kaggle](https://www.kaggle.com/danielhanchen/code), which offers access to dual GPUs.

**To finetune on new reasoning traces, you can use our free** [**Kaggle notebook for Magistral**](https://www.kaggle.com/notebooks/welcome?src=https://github.com/unslothai/notebooks/blob/main/nb/Kaggle-Magistral_\(24B\)-Reasoning-Conversational.ipynb\&accelerator=nvidiaTeslaT4)

```python
!pip install --upgrade unsloth
from unsloth import FastLanguageModel
import torch
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Magistral-Small-2509-unsloth-bnb-4bit",
    max_seq_length = 2048,   # Context length - can be longer, but uses more memory
    load_in_4bit = True,     # 4bit uses much less memory
    load_in_8bit = False,    # A bit more accurate, uses 2x memory
    full_finetuning = False, # We have full finetuning now!
    device_map = "balanced", # Uses 2x Telsa T4s
    # token = "hf_...",      # use one if using gated models
)
```

If you have an old version of Unsloth and/or are fine-tuning locally, install the latest version of Unsloth:

```
pip install --upgrade --force-reinstall --no-cache-dir unsloth unsloth_zoo
```

## :diamond\_shape\_with\_a\_dot\_inside:Dynamic Float8 Checkpoints

We also provide 2 popular formats for float8 checkpoints, which also utilizes some of our dynamic methodology to retain maximum accuracy:

* [vLLM's Float8 format](https://huggingface.co/unsloth/Magistral-Small-2509-FP8-Dynamic)
* [TorchAO's Float8 format](https://huggingface.co/unsloth/Magistral-Small-2509-FP8-torchao)

Both are fantastic to deploy via vLLM. Read up on using TorchAO based FP8 quants in vLLM [here](https://docs.vllm.ai/en/latest/features/quantization/torchao.html).

[^1]: K quantization to reduce memory use. Can be f16, q8\_0, q4\_0

[^2]: Must use --jinja to enable system prompt


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/magistral-how-to-run-and-fine-tune.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
