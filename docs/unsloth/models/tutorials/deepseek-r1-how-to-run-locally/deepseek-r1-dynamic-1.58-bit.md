> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/tutorials/deepseek-r1-how-to-run-locally/deepseek-r1-dynamic-1.58-bit.md).

# DeepSeek-R1 Dynamic 1.58-bit

See performance comparison tables for Unsloth's Dynamic GGUF Quants vs Standard IMatrix Quants.

Read our full DeepSeek-R1 blogpost here: [unsloth.ai/blog/deepseekr1-dynamic](https://unsloth.ai/blog/deepseekr1-dynamic)

### 1-bit (Small) - Dynamic vs. Basic

<table data-full-width="true"><thead><tr><th>GGUF Type</th><th>Quant</th><th>Size (GB)</th><th>Seed</th><th>Pygame</th><th>Background</th><th>Accelerate SPACE</th><th>Bird shape</th><th>Land</th><th>Top right score</th><th>Pipes</th><th>Best Score</th><th>Quit</th><th>Runnable</th><th>Score</th><th>Avg Score</th><th width="214">Errors</th><th width="421">Notes</th></tr></thead><tbody><tr><td>Dynamic</td><td>IQ1_S</td><td>131</td><td>3407</td><td>1</td><td>0.5</td><td>1</td><td>0.5</td><td>0.5</td><td>1</td><td>0.5</td><td>1</td><td>1</td><td>0</td><td>7</td><td></td><td>score =!inc SyntaxError: invalid syntax</td><td>Selects random shapes and colors at the start, but doesn't rotate across trials</td></tr><tr><td>Dynamic</td><td>IQ1_S</td><td>131</td><td>3408</td><td>1</td><td>1</td><td>0.25</td><td>1</td><td>0.5</td><td>1</td><td>0.5</td><td>1</td><td>1</td><td>0</td><td>7.25</td><td></td><td>score =B4 NameError: name 'B4' is not defined</td><td>Better - selects pipe colors randomnly, but all are just 1 color - should be different. Dropping to ground fails to reset acceleration.</td></tr><tr><td>Dynamic</td><td>IQ1_S</td><td>131</td><td>3409</td><td>1</td><td>0.5</td><td>0.5</td><td>0.5</td><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>6.5</td><td>6.92</td><td>score =3D 0 SyntaxError: invalid decimal literal</td><td>Too hard to play - acceleration too fast. Pipe colors now are random, but bird shape not changing. Land collison fails.</td></tr><tr><td>Basic</td><td>IQ1_S</td><td>133</td><td>3407</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td></td><td>No code</td><td>Fully failed. Repeats "with Dark Colurs" forever</td></tr><tr><td>Basic</td><td>IQ1_S</td><td>133</td><td>3408</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td></td><td>No code</td><td>Fully failed. Repeats "Pygame's" forever</td></tr><tr><td>Basic</td><td>IQ1_S</td><td>133</td><td>3409</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>No code</td><td>Fully failed. Repeats "pipe_x = screen_height<br>pipe_x = screen_height<br>pipe_height = screen_height - Pipe_height" forever.</td></tr></tbody></table>

### 1-bit (Medium) - Dynamic vs. Basic

<table data-full-width="true"><thead><tr><th>GGUF Type</th><th>Quant</th><th>Size (GB)</th><th>Seed</th><th>Pygame</th><th>Background</th><th>Accelerate SPACE</th><th>Bird shape</th><th>Land</th><th>Top right score</th><th>Pipes</th><th>Best Score</th><th>Quit</th><th>Runnable</th><th>Score</th><th>Avg Score</th><th width="268">Errors</th><th width="284">Notes</th></tr></thead><tbody><tr><td>Dynamic</td><td>IQ1_M</td><td>158</td><td>3407</td><td>1</td><td>1</td><td>0.75</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>9.75</td><td></td><td>None</td><td>A bit fast and hard to play.</td></tr><tr><td>Dynamic</td><td>IQ1_M</td><td>158</td><td>3408</td><td>1</td><td>1</td><td>0.5</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>9.5</td><td></td><td>None</td><td>Very good - land should be clearer. Acceleration should be slower.</td></tr><tr><td>Dynamic</td><td>IQ1_M</td><td>158</td><td>3409</td><td>1</td><td>0.5</td><td>1</td><td>0.5</td><td>0.5</td><td>1</td><td>0.5</td><td>1</td><td>1</td><td>1</td><td>8</td><td>9.08</td><td>None</td><td>Background color does not change across trials.Pipes do not touch the top. No land is seen.</td></tr><tr><td>Basic</td><td>IQ1_M</td><td>149</td><td>3407</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2</td><td></td><td>if game_over: NameError: name 'game_over' is not defined</td><td>Fully failed. Black screen only</td></tr><tr><td>Basic</td><td>IQ1_M</td><td>149</td><td>3408</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>2</td><td></td><td>No code</td><td>Fully failed. Black screen then closes.</td></tr><tr><td>Basic</td><td>IQ1_M</td><td>149</td><td>3409</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1.67</td><td>window.fill((100, 100, 255)) Light Blue SyntaxError: invalid syntax &#x26;&#x26; main() NameError: name 'main' is not defined.</td><td>Fully failed.</td></tr></tbody></table>

### 2-bit (Extra extra Small) - Dynamic vs. Basic

<table data-full-width="true"><thead><tr><th>GGUF Type</th><th>Quant</th><th>Size (GB)</th><th>Seed</th><th>Pygame</th><th>Background</th><th>Accelerate SPACE</th><th>Bird shape</th><th>Land</th><th>Top right score</th><th>Pipes</th><th>Best Score</th><th>Quit</th><th>Runnable</th><th>Score</th><th>Avg Score</th><th width="330">Errors</th><th width="260">Notes</th><th></th></tr></thead><tbody><tr><td>Dynamic</td><td>IQ2_XXS</td><td>183</td><td>3407</td><td>1</td><td>1</td><td>0.5</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>9.5</td><td></td><td>None</td><td>Too hard to play - acceleration too slow. Lags</td><td></td></tr><tr><td>Dynamic</td><td>IQ2_XXS</td><td>183</td><td>3408</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0.5</td><td>0.5</td><td>1</td><td>0</td><td>8</td><td></td><td>global best_score SyntaxError: name 'best_score' is assigned to before global declaration</td><td>Had to edit 2 lines - remove global best_score, and set pipe_list = []</td><td></td></tr><tr><td>Dynamic</td><td>IQ2_XXS</td><td>183</td><td>3409</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>10</td><td>9.17</td><td>None</td><td>Extremely good. Even makes pipes have random distances between them.</td><td></td></tr><tr><td>Basic</td><td>IQ2_XXS</td><td>175</td><td>3407</td><td>1</td><td>0.5</td><td>0.5</td><td>0.5</td><td>1</td><td>0</td><td>0.5</td><td>1</td><td>0</td><td>0</td><td>5</td><td></td><td>pipe_color = random.choice([(34, 139, 34), (139, 69, 19), (47, 47, 47)) SyntaxError: closing parenthesis ')' does not match opening parenthesis '[' &#x26;&#x26; pygame.draw.polygon(screen, bird_color, points) ValueError: points argument must contain more than 2 points</td><td>Fails quiting. Same color. Collison detection a bit off. No score</td><td></td></tr><tr><td>Basic</td><td>IQ2_XXS</td><td>175</td><td>3408</td><td>1</td><td>0.5</td><td>0.5</td><td>0.5</td><td>1</td><td>1</td><td>0.5</td><td>1</td><td>0</td><td>0</td><td>6</td><td></td><td>pipes.append({'x': SCREEN_WIDTH, 'gap_y': random.randint(50, SCREEN_HEIGHT - 150)) SyntaxError: closing parenthesis ')' does not match opening parenthesis '{'</td><td>Acceleration weird. Chooses 1 color per round. Cannot quit.</td><td></td></tr><tr><td>Basic</td><td>IQ2_XXS</td><td>175</td><td>3409</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0.5</td><td>0</td><td>7.5</td><td>6.17</td><td>screen = pygame.display.set_mode((SCREEN_WIDTH, SCREENHEIGHT)) NameError: name 'SCREENHEIGHT' is not defined. Did you mean: 'SCREEN_HEIGHT'?</td><td>OK. Colors change. Best score does not update. Quit only ESC not Q.</td><td></td></tr></tbody></table>

### **Dynamic Quantization trial output**

{% tabs %}
{% tab title="IQ1\_S code" %}
{% file src="/files/lhdwLrRjoyxL2ldYhPxu" %}

{% file src="/files/DtUWlLcTKdSCfUbbtgZR" %}

{% file src="/files/DDNKmAaalnlnEM5jRbg8" %}
{% endtab %}

{% tab title="IQ1\_M code" %}
{% file src="/files/hHRiMbIGdY46iwSTPe1b" %}

{% file src="/files/Rtx9xWIBjjKRrrzu2CG2" %}

{% file src="/files/8JEm5DHJCgA88hsCoFhi" %}
{% endtab %}

{% tab title="IQ2\_XXS code" %}
{% file src="/files/mz4oALXadBvCtHguz3yp" %}

{% file src="/files/0qtRS8oIwuPzSSEyltfz" %}

{% file src="/files/etx6UqoSp06eUA1QFJLB" %}
{% endtab %}
{% endtabs %}

### Non Dynamic Quantization trial output

{% tabs %}
{% tab title="IQ1\_S basic code" %}
{% file src="/files/w1ns6l9VftZdYwuzJknB" %}

{% file src="/files/blG94CHcCAzXomVvOjJm" %}

{% file src="/files/3Lvf4jH7b9WDlGZXoSLZ" %}
{% endtab %}

{% tab title="IQ1\_M basic code" %}
{% file src="/files/rtT6jQe7SDuap1diCINq" %}

{% file src="/files/HCqDRClY6WfcsyEuq9LG" %}

{% file src="/files/Oy2Qj1vRPqENGfqhMvwp" %}
{% endtab %}

{% tab title="IQ2\_XXS basic code" %}
{% file src="/files/UY2CMIdGxFSuv1SzUPFm" %}

{% file src="/files/jvMphveTauL4A2wUyziV" %}

{% file src="/files/nJIxMdGX3Yv60kIFyFHW" %}
{% endtab %}
{% endtabs %}


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/tutorials/deepseek-r1-how-to-run-locally/deepseek-r1-dynamic-1.58-bit.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
