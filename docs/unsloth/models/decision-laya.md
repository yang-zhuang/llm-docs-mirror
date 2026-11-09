> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/models/decision-laya.md).

# Run and Serve Decision Models Locally with Unsloth: Laya + Jev API

Serve and run decision models locally with Unsloth.

Run and serve decision models like **Laya** or **Clef**, open Jev alternatives, on your local **Mac**, **Windows** and **Linux** device with [Unsloth](https://github.com/unslothai/unsloth). Decision models turns text inputs into structured decisions your apps can act on - from routing support tickets, filtering emails to automated tags and classifications.

You can use the Unsloth GUI interface to expose Laya and Clef through a TypeSafe-compatible Jev API, so existing Jev integrations can work by pointing them at your local server.

All data stays on your device and **CPU**, **unified memory**, and **GPU** setups are all supported.

<div align="center"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FDvcVZXYF1Cepw6sw3UGs%2Flaya-demo-v2.gif?alt=media&amp;token=d550d7d8-d315-4e22-a9c2-eee2a0dbbf82" alt="Real time packing demo powered by local Laya through Unsloth’s Decision API: suitcase items update as you type and change your travel plans" width="563"><figcaption></figcaption></figure></div>

Send the decision model pieces of text, define the decisions you need (yes/no, choices, or scores), and get back calibrated probabilities.

### 🖥️  Recommended Settings

| Model                      | Minimum RAM | Size   | Best for                                                                    |
| -------------------------- | ----------- | ------ | --------------------------------------------------------------------------- |
| **Multilingual** (default) | 4GB RAM     | 678 MB | Most use-cases. 100+ languages, 1024 token context.                         |
| **English**                | 5GB RAM     | 846 MB | English only. Larger encoder, 512 token context.                            |
| **Typed decisions**        | 5GB RAM     | 846 MB | English only. Invoices, security incidents, customer service, agent traces. |

CPU is the default. Switch **Run on** GPU for faster answers. The GPU keeps the model in memory until you press **Unload** or restart Unsloth. If the GPU runs out of memory, Laya falls back to CPU and keeps answering.

### ⚡ Quickstart

{% stepper %}
{% step %}

#### **Setup Unsloth**

The easiest way to get started is by downloading the [Unsloth Desktop app](/docs/desktop.md). Works on [macOS](/docs/get-started/install/mac.md), [Windows](/docs/get-started/install/windows-installation.md), and [Linux](/docs/get-started/install/linux.md).

<a href="https://unsloth.ai/download" class="button primary" data-icon="down-to-bracket">Download Unsloth</a>

* <i class="fa-apple">:apple:</i> [Download for macOS](https://unsloth.ai/download/mac)
* <i class="fa-windows">:windows:</i> [Download for Windows](https://unsloth.ai/download/windows)
* <i class="fa-linux">:linux:</i> [Download for Linux](https://unsloth.ai/download/linux)

Or, if you prefer to install manually:

MacOS, Linux, WSL:

```bash
curl -fsSL https://unsloth.ai/install.sh | sh
```

Windows PowerShell:

```bash
irm https://unsloth.ai/install.ps1 | iex
```

{% endstep %}

{% step %}

#### Setup Laya

Go to Settings → API → **Decision API** and turn on **Serve requests**. The default Laya model (678 MB) will then start to download after confirming if you want to start the download.

Your API key is on the same page under Access tokens. Or turn on **Keyless API access** → **Chat and inference** and skip the key on localhost.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F0Mt4vrBDlZMpLIP4O4L2%2Fdecision-api-loaded.png?alt=media&amp;token=921d0ba2-c60f-4fc2-82f9-b44584454ba3" alt=""><figcaption></figcaption></figure></div>
{% endstep %}

{% step %}

#### Send a decision request

It's time to send a decision request. In this example, we classify a support ticket, detect refund requests, and score urgency.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F57Wcq0T86gBgHWMt8ISt%2FScreenshot%202026-09-28%20at%206.53.48%E2%80%AFPM.png?alt=media&amp;token=88c48aef-0454-485a-8a30-ec55b0b6ad0c" alt="" width="563"><figcaption></figcaption></figure>

```bash
curl http://localhost:8888/v1/systemone \
  -H "Authorization: Bearer sk-unsloth-YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "laya",
    "state": "Hi, I was charged twice for my March invoice (#4411). Please refund the duplicate today.",
    "questions": {
      "team": {
        "type": "choice",
        "instructions": "Which team should handle this?",
        "criteria": {
          "billing": "invoices, payments, refunds",
          "technical": "bugs, outages, errors",
          "sales": "pricing, new plans",
          "other": "everything else"
        }
      },
      "refund": {"type": "noul", "instructions": "Does the customer ask for a refund?"},
      "urgency": {"type": "score", "instructions": "How urgent is this?", "criteria": ["not urgent", "soon", "today"]}
    }
  }'
```

You get back:

```json
{
  "model": "laya-multilingual",
  "answers": {
    "team": {"type": "choice", "choice": "billing", "confidence": 1.0, "probabilities": {"billing": 1.0, "technical": 0.0, "sales": 0.0, "other": 0.0}},
    "refund": {"type": "noul", "noul": 0.9794},
    "urgency": {"type": "score", "score": 1.9005, "confidence": 0.698, "legend": {"0": "not urgent", "1": "soon", "2": "today"}, "probabilities": {"0": 0.004, "1": 0.0915, "2": 0.9045}}
  },
  "usage": {"input_tokens": 172, "output_tokens": 0}
}
```

The first request loads the model, which takes 10 to 20 seconds. After that, requests take well under a second on most CPUs.

`state` can be a string or any JSON. `model` accepts `laya`, `default`, or `jev-latest` for the model you picked in settings, or `laya-multilingual`, `laya-english`, `laya-typed-decisions` to name one.
{% endstep %}
{% endstepper %}

### ❓ Question types

| Type     | Use it for         | You get back                                        |
| -------- | ------------------ | --------------------------------------------------- |
| `noul`   | Yes or no          | The probability of yes, from 0 to 1                 |
| `choice` | Picking one option | The most likely option, and a probability for each  |
| `score`  | Rating on a scale  | Where the text falls on your scale, counting from 0 |

`noul` means yes/no. It returns the probability of “yes”: `0.98` means very likely, `0.5` means equally likely either way.

`choice` and `score` also return `confidence`. Close to `1` means one answer stands out. Close to `0` means the probabilities are spread evenly.

{% columns %}
{% column %}
To act on a choice, use its value in `probabilities`, not `confidence`. For example, only file a bug report when `technical` is above `0.8`. Laya and Jev calculate confidence differently, so don’t reuse your Jev confidence thresholds.

Each request supports up to **64 questions**, with up to **255 options per choice** and **10 levels per score**.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FlsX4Rv1JIcz1JuTkFIBO%2Fsuitcase-10mb.gif?alt=media&amp;token=1314fb64-166e-48b2-97cf-cb086d40fbe9" alt=""><figcaption><p>Real time packing demo powered by local Laya through Unsloth’s Decision API: suitcase items update as you type and change your travel plans</p></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

### 🔁 Migrating from Jev

Install the SDK with `pip install typesafe-sdk`, set two environment variables, and your existing code talks to Unsloth:

```bash
export TYPESAFE_BASE_URL=http://localhost:8888
export TYPESAFE_API_KEY=sk-unsloth-YOUR_KEY
```

The SDK's default model, `jev-latest`, maps to whichever model you picked in Settings.

Two things differ from Jev. `confidence` uses a different formula, so a threshold tuned on Jev won't transfer; threshold on `probabilities` instead. And options in a choice share a fixed token budget, so past about 20 described options the labels get trimmed.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/models/decision-laya.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
