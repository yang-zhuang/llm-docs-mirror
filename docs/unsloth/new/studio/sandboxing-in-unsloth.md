> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/new/studio/sandboxing-in-unsloth.md).

# Sandboxing in Unsloth

Unsloth uses bubblewrap on Linux, Seatbelt on macOS, and MXC on Windows.

Unsloth now has OS level sandboxing which means Python and shell commands can run in an isolated workspace. Unsloth has 2 modes - **“low”** and **“high” sandbox security** - low employs Unsloth's software sandbox methods which are sophisticated string, AST and regex checks for those commands (disabling dangerous rm -rf, exfiltrate tokens etc). High is true OS level sandboxing, which we have for all platforms.

| Operating System                            | Sandbox Software           | Latency per call |
| ------------------------------------------- | -------------------------- | ---------------- |
| <i class="fa-windows">:windows:</i> Windows | **MXC** (Windows official) | 164ms            |
| <i class="fa-linux">:linux:</i> Linux       | Bubblewrap / Bwrap         | 50ms             |
| <i class="fa-apple">:apple:</i> Mac         | Seatbelt (Mac internal)    | 110ms            |

To enable OS level sandboxing:

* **Windows - MXC is pre-installed** for Windows 11 24H2 and higher. Select **High** and follow the setup instructions if prompted.
* **Linux** - Bwrap will need to be installed - select "High" and we will install it for you
* **Mac - Seatbelt is pre-installed**, so Unsloth auto enables Seatbelt

To check if OS Sandboxing is Low or High, click on the permissions button:

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FBdWF0MbLoJLwTeFVhX7j%2FScreenshot%202026-10-08%20at%207.00.50%E2%80%AFAM.png?alt=media&amp;token=a592513a-9f45-4e0b-80d4-b8a6456e37ac" alt="" width="563"><figcaption></figcaption></figure></div>

If you click "Learn More", you will head to the Sandbox Settings page, and you can see if you have software sandboxing enabled, and also how to install bwrap, MXC as well:

<div align="left"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FfDEvjiXwBf1Fmftsp28q%2FScreenshot%202026-10-08%20at%206.56.34%E2%80%AFAM.png?alt=media&amp;token=b2c99b4c-67ea-4c50-bb98-4a710e0eafee" alt="" width="563"><figcaption></figcaption></figure></div>

For all 3 operating systems, you can see how OS level sandboxing is enabled:

{% columns %}
{% column %}
Windows:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FLnxxpIwGpSjut6R6kLn8%2FScreenshot%202026-10-08%20at%206.53.26%E2%80%AFAM.png?alt=media&amp;token=85be4503-5279-4716-a1d0-1efbb8126129" alt=""><figcaption></figcaption></figure>
{% endcolumn %}

{% column %}
Mac:

<img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FRNZyuJL7xkrXJwYxofto%2FScreenshot%202026-10-08%20at%206.51.19%E2%80%AFAM.png?alt=media&amp;token=04ee3ff8-209c-41f6-bed2-8c64173ea77f" alt="" width="375">
{% endcolumn %}

{% column %}
Linux:

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FesfsF7INvYB1MpIQF3cn%2FScreenshot%202026-10-08%20at%206.53.20%E2%80%AFAM.png?alt=media&amp;token=33f9f7cd-df4e-4e74-89c4-0c482c64e3c5" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

{% columns %}
{% column width="50%" %}
You can see the sandbox in action where it blocks accesses outside of the workspace:

### Latency of sandboxing

We optimized software and hardware OS level sandboxing a lot, but OS level sandboxing definitely has a latency addon. See below for a table:
{% endcolumn %}

{% column width="50%" %}
![](https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FcyBycXfercRlu0iEttel%2Fnew%20sandbox.png?alt=media\&token=d9064a88-e5c8-4e1d-a261-e93f20739ea6)
{% endcolumn %}
{% endcolumns %}

| Operating System                            | Sandbox Software           | Low Sandbox | High Sandbox |
| ------------------------------------------- | -------------------------- | ----------- | ------------ |
| <i class="fa-windows">:windows:</i> Windows | **MXC** (Windows official) | 8ms         | 164ms        |
| <i class="fa-linux">:linux:</i> Linux       | Bubblewrap / Bwrap         | 3ms         | 50ms         |
| <i class="fa-apple">:apple:</i> Mac         | Seatbelt (Mac internal)    | 10ms        | 110ms        |

{% columns %}
{% column %}

### Disable Sandboxing / Bypass Permissions / Full Access

To disable sandboxing (both software low and OS level high), simply press "Full Access", and now Unsloth can now access your entire computer with 0 constraints.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F6YpMXm0gOsM7lPaygu4T%2FScreenshot%202026-10-08%20at%206.45.21%E2%80%AFAM.png?alt=media&amp;token=b7f308f5-ac0b-4852-9eeb-961e6cc575ef" alt=""><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

### Software Sandboxing Approach

Software Sandboxing in Unsloth is a bunch of regular expressions, string checks and more - we add about **1-2ms of extra latency** per tool call, and we block the following:

* Deleting and disk tools: `rm, dd, mkfs, fdisk, mount, umount`
* Permissions and privilege: chmod, `chown, sudo, su, doas, pkexec, passwd`
* Network: `curl, wget, nc, ncat, netcat, socat, ssh, scp, sftp, rsync`
* Processes and power: `kill, killall, pkill, shutdown, reboot, halt, poweroff`
* Running another script's contents unseen: `eval, source`
* Windows only: `rmdir, takeown, icacls, runas, powershell, pwsh`

Python code, by reading the code before it runs:

* Shell escapes: `os.system`, and `subprked` command, or a non-literal command (for example pip install through su)
* Network calls: `requests, urllib`, raw socket connections
* Some sensitive system reads, such as `/etc/passwd`
* Tampering with signals or timeouts,used to dodge them.

Applied to every call in both modes:

* Secret environment variables are stripped.
* Studio's own credential files are refused
* Limits on processes, file size (100 MB), memory (8 GB) and CPU time (600 s), so a fork bomb hits the process limit, plus the call timeout

#### Windows MXC Partnership

Thank you to the Windows team for partnering with Unsloth on making MXC work well in Unsloth! [See here](https://blogs.windows.com/windowsexperience/2026/10/07/building-windows-for-hybrid-intelligence/) for the launch blog post

#### Getting sandboxing in Unsloth

Simply update Unsloth to the latest and you will get sandboxing!


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/new/studio/sandboxing-in-unsloth.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
