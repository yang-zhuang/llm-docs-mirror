> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/basics/how-to-serve-local-llms-anywhere-secure-remote-access-with-cloudflare-and-unsloth.md).

# How to Serve Local LLMs Anywhere: Secure Remote Access with Cloudflare and Unsloth

Serve and deploy local AI models anywhere. You can securely access your local LLMs from another device over HTTPS using a Cloudflare tunnel via [Unsloth](https://github.com/unslothai/unsloth). No Cloudflare account, domain setup, or port forwarding is required. Run private AI models on your own hardware, servers, or cloud GPUs and connect from anywhere like your phone.

{% columns %}
{% column %}
Unsloth is an open-source project that allows you to train and run LLMs locally and with Cloudflare tunnel, you can access Unsloth from your mobile device, share access to a friend or coworker, host Unsloth on a server such as Google Colab, AWS, or even a personal server.

Unsloth can run 100% offline on your computer. Turn on remote access and you get a web link like `https://known-plates-desire-turkey.trycloudflare.com`. Open it on your phone, your laptop, or any browser, anywhere.
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FD2v8S0MkS1xAeEVersl2%2Fmobile_studio1.gif?alt=media&#x26;token=7cd8a534-d82f-4f05-8d5a-9b7277f7eac0" alt="" width="180"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

It is free. Nothing to sign up for or pay for and you never touch your router or firewall. Once Unsloth is installed, your computer reaches out to Cloudflare, and Cloudflare passes visitors back to it. The link is HTTPS, so the connection is encrypted.

Two ways to turn it on:

* **When you start Unsloth:** add `--secure` to your `unsloth studio` command
* **While Unsloth is running:** go to Settings → API → **Remote access** and press **Start**

Only one tunnel exists per Unsloth process, and only its owner can stop it.

### ⚡ Quickstart

Firstly we will need to download the [Unsloth Desktop](https://unsloth.ai/download) app.

1. Install the app for [macOS](https://unsloth.ai/download/mac), Windows, or [Linux](https://unsloth.ai/download/linux)
2. Launch the app
3. Then go to Settings → Remote & LAN → Remote access.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F31IAHABHEuWz1juiABBY%2Fimage.png?alt=media&#x26;token=b430b2f7-f91b-49e3-a4b6-c46bd688bbfc" alt=""><figcaption></figcaption></figure></div>

Use this when Unsloth is already running and you want it on your phone or another machine. Press **Start**, then copy the **Remote URL** or scan the **QR** code. `Online` means the link already answers, not just that it was requested.

Three things worth knowing:

* Anyone with the URL and the password can sign in. Remote browsers log in as `unsloth`, set that under **Remote password**.
* The URL is new on every start and cannot be pinned.
* A raw `0.0.0.0` port stays open. Only `--secure` closes it.

If **Start** is greyed out, the card says why, usually the admin password still needs changing, or the tunnel belongs to the launch command.

#### When Start is unavailable

<table><thead><tr><th width="292">Reason</th><th>Message shown</th></tr></thead><tbody><tr><td><code>server_starting</code></td><td>Unsloth is still starting.</td></tr><tr><td><code>admin_password_change_required</code></td><td>Set a remote password before exposing this server. <em>(desktop)</em> / Change the administrator password before exposing this server. In the desktop app, run <code>unsloth studio reset-password</code>. <em>(browser)</em></td></tr><tr><td><code>explicitly_disabled</code></td><td>This launch used <code>--no-cloudflare</code>. Restart without it to enable remote access.</td></tr><tr><td><code>launch_managed</code></td><td>This tunnel is managed by the launch command.</td></tr><tr><td><code>colab_managed</code></td><td>This tunnel is managed by the Colab runtime.</td></tr><tr><td><code>colab</code></td><td>Remote access settings are managed by the Colab runtime.</td></tr></tbody></table>

#### The tunnel URL in the rest of the UI

Once a tunnel is online, two places switch to it automatically:

* **Settings → API → Usage examples** grows a **Secure HTTPS** toggle. On, every curl/Python/JavaScript snippet and coding-agent command is rewritten against the `trycloudflare.com` base instead of `localhost`. If you did not launch with `--secure`, an info tooltip reminds you: *"The 0.0.0.0 port is still reachable globally. For full security, launch Unsloth with `--secure` to expose only this HTTPS link."*
* The **API monitor** page's **Base URL** readout shows the tunnel origin, so a snippet copied there works from the remote device, and every request arriving through the tunnel is listed live.

### CLI: HTTPS only method

After installing Unsloth manually, run in your terminal:

```bash
unsloth studio --secure -p 8888
```

Unsloth stays bound to `127.0.0.1` and is published **only** through the tunnel. If the tunnel cannot come up, Unsloth **exits instead of falling back** to a raw port. The banner prints:

```
🦥 Unsloth Studio is running (secure)
────────────────────────────────────────────────────
  Secure link access via Cloudflare: https://<random>.trycloudflare.com
  On this machine only: http://127.0.0.1:8888/
────────────────────────────────────────────────────
```

#### CLI: raw LAN port plus a public link

```bash
unsloth studio -H 0.0.0.0 --cloudflare -p 8888
```

The raw port stays reachable on your network *and* a public Cloudflare URL is published. The banner warns you about exactly this, because it is the least private mode.

#### UI: start a link on a server that is already running

1. Open **Settings → API**.
2. Find the **Remote access** card.
3. Click **Start**.
4. When the status reads **Online**, copy the **Remote URL** or scan the **QR** code with your phone.

### 🖥️ CLI reference

Both flags are accepted by `unsloth studio` (the plain-server path) and by `unsloth studio run`.

<table><thead><tr><th width="283">Flag</th><th width="100" align="center">Default</th><th>Effect</th></tr></thead><tbody><tr><td><code>--secure</code> / <code>--no-secure</code></td><td align="center">off</td><td>Publish <strong>only</strong> through Cloudflare. Forces a loopback bind, implies <code>--cloudflare</code>, and fails closed if the tunnel cannot start.</td></tr><tr><td><code>--cloudflare</code> / <code>--no-cloudflare</code></td><td align="center">off</td><td>Also publish a public Cloudflare URL for a <strong>non-<code>--api-only</code> wildcard bind</strong> (<code>0.0.0.0</code> or <code>::</code>). Has no effect on a loopback bind. <code>--no-cloudflare</code> forces it off but does <strong>not</strong> make a wildcard bind private.</td></tr></tbody></table>

Notes on flag handling:

* `--secure` ignores `-H`. If you pass another host it prints a note and binds `127.0.0.1` anyway.
* `--secure --no-cloudflare` is a contradiction and exits with code `2`.
* These flags belong to the plain-server path. Putting them *before* a subcommand (`unsloth studio --secure run ...`) exits `2` with the corrected command, because Typer would otherwise silently drop them. Use `unsloth studio run --secure ...`.
* The choice is carried across Unsloth's internal re-exec as a tri-state (`enabled` / `disabled` / `unset`), so a stale `Docker ENV` or `systemd Environment=` can never re-enable a tunnel you opted out of on this invocation.

#### What each launch actually exposes

<table><thead><tr><th width="391">Launch</th><th>Raw port</th><th>Public Cloudflare URL</th></tr></thead><tbody><tr><td><code>unsloth studio</code></td><td>this machine only</td><td>no</td></tr><tr><td><code>unsloth studio --cloudflare</code></td><td>this machine only</td><td>no, the flag is a no-op on loopback</td></tr><tr><td><code>unsloth studio -H 0.0.0.0</code></td><td>your network</td><td>no</td></tr><tr><td><code>unsloth studio -H 0.0.0.0 --cloudflare</code></td><td>your network</td><td><strong>yes</strong></td></tr><tr><td><code>unsloth studio --secure</code></td><td>this machine only</td><td><strong>yes</strong>, and it is the only way in</td></tr><tr><td><code>unsloth studio --api-only</code> (desktop backend)</td><td>as bound</td><td>no, unless <code>--secure</code></td></tr><tr><td>Google Colab</td><td>Colab proxy</td><td>only via <code>start(cloudflare=True)</code></td></tr></tbody></table>

The rule the backend applies: Colab never tunnels from the launch path; `--secure` always tunnels (even `--api-only`, for headless secure API serving); otherwise the tunnel starts only for a wildcard bind that is not `--api-only`.

#### `--secure` fails closed

If the tunnel does not come up, `--secure` refuses to keep running:

```
A secure Cloudflare link is not allowed, use --no-secure which provides a 0.0.0.0 link
```

and exits `1`. This is deliberate: `--secure` means "no raw public port", so silently degrading to a loopback-only server that you believe is published would be worse than stopping.

#### Startup banner lines

On a wildcard bind Unsloth always states the tunnel's status, so a network-reachable launch is never silent:

* Cloudflare tunnel: ON. This is a PUBLIC internet URL: anyone who has it can reach this Unsloth.
* Cloudflare tunnel: ON. This Cloudflare URL is PUBLIC, and the raw port is also publicly reachable.
* Cloudflare tunnel: requested but failed to start.
* Cloudflare tunnel: OFF (default). / OFF (--no-cloudflare). / OFF for this mode.

Each variant adapts to whether the raw port was independently found reachable from the internet. That reachability probe contacts `ifconfig.me` and `check-host.net`; set `UNSLOTH_STUDIO_DISABLE_PUBLIC_CHECK=1` to skip both.

#### The password gate

The first time a launch is about to publish Unsloth on a public URL while the admin account still holds its auto-generated bootstrap password, Unsloth stops and asks for a new one masked, confirmed, **before any server or tunnel exists**.

* **Terminal attached:** you are prompted. Aborting (Ctrl+C) refuses the launch.
* **No terminal:** Unsloth warns instead, never injects the bootstrap credential into the public page, and arms the bootstrap deadline, it shuts down after `UNSLOTH_STUDIO_BOOTSTRAP_TIMEOUT` (default 1 hour) unless the password is changed.
* **No terminal and no deadline** (`--api-only`, or `UNSLOTH_STUDIO_BOOTSTRAP_TIMEOUT=0`): the launch is refused outright, because nothing would protect it.
* **`--secure` with `cloudflared` provably unavailable:** refused with the seeded password preserved, so a failed tunnel cannot lock you out.

For headless setups, set the initial password non-interactively (only takes effect when none is set yet):

```bash
UNSLOTH_STUDIO_PASSWORD='your-strong-password' unsloth studio --secure
```

```bash
printf '%s\n' 'your-strong-password' | unsloth studio --secure --password -
```

A literal `--password VALUE` is visible in `ps` and shell history, so prefer the env var or stdin. Rotate later with `unsloth studio reset-password`.

### 📓 Google Colab

`run_server` suppresses the launch-path tunnel on Colab, since Colab already proxies the port. Ask for a shareable public link explicitly:

```python
start(cloudflare = True)
```

Colab refuses to open the link while the admin account still has its bootstrap password, that credential is visible to anyone who can load the page. Log in, change the password, then re-run. Any failure collapses to "no link" and the Colab proxy keeps working.

### 🔒 Security

Publishing Unsloth means anyone holding the URL **and** a credential can use it.

* **Server-side tools run as your user.** Web search, Python and terminal execution are on by default, so anyone reaching the server with your API key can run code on that machine. Pass `--disable-tools` when exposing Unsloth, and keep the API key private. Every network-reachable launch says this in the banner.
* **The admin password gate** above is not optional on a launch-managed tunnel.
* **Rate limiting stays per-visitor.** The tunnel terminates at `127.0.0.1`, so every tunneled caller would otherwise share one bucket. When the socket peer is loopback, Unsloth honours Cloudflare's `CF-Connecting-IP`, which the edge sets and a tunneled client cannot forge. Behind your own reverse proxy, opt into `X-Forwarded-For` with `UNSLOTH_STUDIO_TRUST_FORWARDED=1`.
* **Local stdio MCP servers are revoked while a tunnel is live.** stdio MCP is auto-enabled only as a loopback convenience; a remote connector breaks that trust boundary, so the auto-default turns itself off. An explicit `UNSLOTH_STUDIO_ALLOW_STDIO_MCP=1` still wins.
* **The URL is random and disposable.** Quick Tunnels get a new hostname on every start. Treat the URL itself as a secret, and remember there is no way to pin it.

### ❔ Troubleshooting

These are the exact statuses surfaced in the Remote access card. Anything else is collapsed to the generic `Cloudflare tunnel failed`.

| Error                                       | Meaning                                                                 | Fix                                                                                          |
| ------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `cloudflared is unavailable`                | Not on `PATH`, not cached, and the download failed.                     | Check outbound access to `github.com`, or install `cloudflared` yourself so it is on `PATH`. |
| `cloudflared did not produce a URL`         | The process exited before minting one.                                  | Usually no outbound network. Retry; check a proxy or egress filter.                          |
| `cloudflared did not register a connection` | URL minted, but no edge connection, after the `http2` retry.            | Your network blocks QUIC *and* HTTP/2 to Cloudflare's edge.                                  |
| `Cloudflare URL was not reachable`          | Registered, but the health probe never answered through the public URL. | Transient edge/DNS propagation; press Start again.                                           |
| `cloudflared exited`                        | The connector died while online.                                        | Start again; check for an OOM killer or a process supervisor reaping children.               |
| `cloudflared could not be stopped`          | Termination was never confirmed, so the slot is still held.             | Press Stop again; if it persists, restart Unsloth.                                           |

Other symptoms:

* **`--secure` exits immediately.** The tunnel failed; the message names `--no-secure` as the alternative. Fix connectivity first, since `--no-secure` publishes a raw port.
* **Start is greyed out in the UI.** Read the message under the card, it names the block reason from the table above.

### 🌱 Environment variables

| Variable                              | Purpose                                                                                                                                |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `UNSLOTH_STUDIO_HOME`                 | Install root; the `cloudflared` cache lives in `<root>/bin`.                                                                           |
| `UNSLOTH_STUDIO_BOOTSTRAP_TIMEOUT`    | Seconds before an unsecured public launch shuts itself down. Default `3600`; `0` disables (and makes a headless public launch refuse). |
| `UNSLOTH_STUDIO_PASSWORD`             | Initial admin password for headless launches.                                                                                          |
| `UNSLOTH_STUDIO_DISABLE_PUBLIC_CHECK` | `1` skips the third-party raw-port reachability probe on wildcard binds.                                                               |
| `UNSLOTH_STUDIO_TRUST_FORWARDED`      | `1` honours `X-Forwarded-For` behind your own reverse proxy.                                                                           |
| `UNSLOTH_STUDIO_ALLOW_STDIO_MCP`      | `1` keeps stdio MCP servers enabled even with a tunnel live; `0` force-disables.                                                       |

### 🌐 HTTP API

All four require a **UI session,** an API key is rejected with `403 Remote access requires a UI session.` A refused operation returns `409` with the block reason as the detail.

<table><thead><tr><th width="100">Method</th><th>Path</th><th>Purpose</th></tr></thead><tbody><tr><td><code>GET</code></td><td><code>/api/settings/remote-access</code></td><td>Current state, URL, owner, <code>can_start</code> / <code>can_stop</code>, <code>block_reason</code>.</td></tr><tr><td><code>POST</code></td><td><code>/api/settings/remote-access/start</code></td><td>Schedule a settings-owned start. Idempotent.</td></tr><tr><td><code>POST</code></td><td><code>/api/settings/remote-access/stop</code></td><td>Schedule a settings-owned stop. Does not change the auto-start preference.</td></tr><tr><td><code>PUT</code></td><td><code>/api/settings/remote-access/auto-start</code></td><td><code>{"enabled": true|false}</code>. Rejected on Colab.</td></tr></tbody></table>


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/basics/how-to-serve-local-llms-anywhere-secure-remote-access-with-cloudflare-and-unsloth.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
