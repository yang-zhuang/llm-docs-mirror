> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/inference-and-deployment/lm-studio/how-to-install-lm-studio-cli-in-linux-terminal.md).

# How to install LM Studio CLI in Linux Terminal

LM Studio CLI installation guide without a UI in a terminal instance.

1. Open a new terminal to run LM Studio CLI, or use `tmux`
2. Get [LM Studio](https://lmstudio.ai/download) or run below (1GB or so download size)

{% code overflow="wrap" %}

```bash
wget https://lmstudio.ai/download/latest/linux/x64?format=AppImage -O 'LM_Studio.AppImage'
chmod u+x ./LM_Studio.AppImage
```

{% endcode %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FtAXPNUc4awU1GkNTklzG%2Fimage.png?alt=media&amp;token=6b8929fc-2e93-48d9-8bda-b88c59b5e2fc" alt=""><figcaption></figcaption></figure>

2. Run LM Studio via

```bash
./LM_Studio.AppImage
```

You might see below:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FMqjblgskH96SUt7up3iQ%2Fimage.png?alt=media&amp;token=c4713e00-9c1d-45be-b949-22cc7443484f" alt=""><figcaption></figcaption></figure>

{% code overflow="wrap" %}

```
[802435:0215/073628.027773:FATAL:sandbox/linux/suid/client/setuid_sandbox_host.cc:166] The SUID sandbox helper binary was found, but is not configured correctly. Rather than run without sandboxing I'm aborting now.
```

{% endcode %}

If so, do the below instead:

```bash
./LM_Studio.AppImage --no-sandbox
```

3. You then might see the below, especially if you are in a cloud instance with no desktop:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F0Wub7SZjdOtKjJYuEj30%2Fimage.png?alt=media&amp;token=2f7ec9c7-6f9b-4ebe-9c4d-a0bd871e6ca5" alt=""><figcaption></figcaption></figure>

{% code overflow="wrap" %}

```
[807101:0215/073740.801969:ERROR:ui/ozone/platform/x11/ozone_platform_x11.cc:249] Missing X server or $DISPLAY
[807101:0215/073740.802000:ERROR:ui/aura/env.cc:257] The platform failed to initialize.  Exiting.
Segmentation fault (core dumped)
```

{% endcode %}

If so, install a "fake" desktop simulator within the terminal:

```bash
sudo apt-get install xvfb
```

4. Then use `xvfb` and launch LM Studio:

```bash
xvfb-run --auto-servernum ./LM_Studio.AppImage --no-sandbox
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FU04faEKimBth2FPP0WJI%2Fimage.png?alt=media&amp;token=005eb027-beed-4b71-8221-c527e670ed8a" alt=""><figcaption></figcaption></figure>

5. Then get LM Studio's LMS / CLI in another terminal, or after CTRL+B+D for `tmux`

```bash
~/.lmstudio/bin/lms bootstrap
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F6kw89TOhe3ZaOmBY9SUH%2Fimage.png?alt=media&amp;token=2ddb7550-3a61-45e0-a157-085e76862338" alt=""><figcaption></figcaption></figure>

6. Open a new terminal or `tmux`  then run:

```bash
lms
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fa5znXk9udpntbNEX4VWW%2Fimage.png?alt=media&amp;token=6315b12b-5401-4ff6-9ef4-729c0a84447b" alt="" width="375"><figcaption></figcaption></figure>

If you see `-bash: lms: command not found` please run `lms` in a new terminal window!

7. Now download a model like [Qwen3-Coder-Next](/docs/models/qwen3-coder-next.md) like below. If downloads get stuck, see [Hugging Face Hub, XET debugging](/docs/basics/troubleshooting-and-faqs/hugging-face-hub-xet-debugging.md)

{% code overflow="wrap" %}

```bash
pip install -U huggingface_hub
hf download unsloth/Qwen3-Coder-Next-GGUF \
    --local-dir unsloth/Qwen3-Coder-Next-GGUF \
    --include "*UD-Q4_K_XL*"
```

{% endcode %}

8. We then import the model via:

{% code overflow="wrap" %}

```bash
lms import \
    unsloth/Qwen3-Coder-Next-GGUF/Qwen3-Coder-Next-UD-Q4_K_XL.gguf \
    --symbolic-link --user-repo "unsloth/Qwen3-Coder-Next-GGUF" -y
```

{% endcode %}

You might see `EEXIST: file already exists, symlink 'unsloth/Qwen3-Coder-Next-GGUF/UD-Q6_K_XL/Qwen3-Coder-Next-UD-Q6_K_XL-00001-of-00003.gguf' -> '~/.lmstudio/models/unsloth/Qwen3-Coder-Next-GGUF/Qwen3-Coder-Next-UD-Q6_K_XL-00001-of-00003.gguf'` which just means you already have the model loaded in LM Studio.

You can also check all LM Studio models via:

```bash
ls ~/.lmstudio/models
```

8. You can also get models via `lms get` via below:

```bash
lms get https://huggingface.co/unsloth/Qwen3-Coder-Next-GGUF@Q4_K_XL
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FK74SkUxvalZHx8t3E43F%2Fimage.png?alt=media&amp;token=a55fcb8c-9988-4715-8c0c-6734e64f7950" alt=""><figcaption></figcaption></figure>

You will then see:

```
Finalizing download...
Download completed. You can load the model with: 
lms load qwen3-coder-next
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FLTu3kzRayo9EizGePnDC%2Fimage.png?alt=media&amp;token=bfe7b31b-3f91-40b2-b7c3-3fd1e0a59597" alt=""><figcaption></figcaption></figure>

Then load `lms load qwen3-coder-next`:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FwaFO6LrId5ApBwAzYWAv%2Fimage.png?alt=media&amp;token=89e9546e-cf8d-4ce8-aa87-c529c786b848" alt=""><figcaption></figcaption></figure>

9. Then start up LM Studio's server:

```bash
lms server start --port 8001 --bind 127.0.0.1
```

You will see `Success! Server is now running on port 8001`

9. Then in a new terminal, use the model via the OpenAI compatible endpoint:

```python
from openai import OpenAI
import json
openai_client = OpenAI(
    base_url = "http://127.0.0.1:8001/v1",
    api_key = "null",
)
model_name = next(iter(openai_client.models.list())).id
print(model_name)
completion = openai_client.chat.completions.create(
    model = model_name,
    messages = [{"role": "user", "content": "What is 2+2?"},],
)
print(completion.choices[0].message.content)
```

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FufkusKj9R9amo7lb9JxM%2Fimage.png?alt=media&amp;token=4f4e90ab-0cf6-4215-b7db-7f08e40719d1" alt=""><figcaption></figcaption></figure>

And we're done!


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/inference-and-deployment/lm-studio/how-to-install-lm-studio-cli-in-linux-terminal.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
