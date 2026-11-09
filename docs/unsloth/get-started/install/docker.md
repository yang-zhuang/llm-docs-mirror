> For the complete documentation index, see [llms.txt](https://unsloth.ai/docs/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://unsloth.ai/docs/get-started/install/docker.md).

# Install Unsloth via Docker

Install Unsloth using our official Docker container

Learn how to run and train models with the Unsloth Docker container. No setup required - all dependencies are pre-installed. Just pull the image and start running and training models on your local NVIDIA or AMD GPUs.

| **NVIDIA** Docker: [**`unsloth/unsloth`**](https://hub.docker.com/r/unsloth/unsloth) | **AMD** Docker: [**`unsloth/unsloth-rocm`**](https://hub.docker.com/r/unsloth/unsloth-rocm) |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |

{% hint style="success" %}
**NEW Sep 2026: Unsloth Docker container is now updated with Unsloth Studio and AMD.**

Unsloth shares the same cache as notebooks and scripts to avoid unnecessary re-downloads.
{% endhint %}

### Quickstart

This guide section applies to systems with NVIDIA GPUs. If you have [AMD see here](#amd-quickstart).

{% tabs %}
{% tab title="Linux / WSL" %}
To get Unsloth's Docker on NVIDIA GPUs, run the following in terminal:

```bash
docker run -d --name unsloth --gpus all --ipc=host \
  --ulimit memlock=-1 --ulimit stack=67108864 \
  -p 8000:8000 -p 8888:8888 \
  -e JUPYTER_PASSWORD="mypassword" \
  -v "$PWD":/workspace/host \
  -v "$HOME/.cache/huggingface":/workspace/.cache/huggingface \
  -v unsloth-studio:/opt/unsloth-studio \
  unsloth/unsloth
```

* Run it from your project folder, because that folder (`$PWD`) becomes `/workspace/host`.
* What the flags do: exposing ports 8000 (Unsloth Studio) and 8888 (JupyterLab); the three `-v` flags keep your files, models and Unsloth Studio data.
* Requirement: NVIDIA driver 570.26 or newer.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fz1bQUO7kRRL6jrzDKsRO%2FiShot_2026-09-17_16.30.18.png?alt=media&amp;token=1a5a23ee-e384-4bc7-b5f5-4cb934989094" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Windows (PowerShell)" %}
Run the following in Powershell:

```powershell
docker run -d --name unsloth --gpus all --ipc=host `
  --ulimit memlock=-1 --ulimit stack=67108864 `
  -p 8000:8000 -p 8888:8888 `
  -e JUPYTER_PASSWORD="mypassword" `
  -v "${PWD}:/workspace/host" `
  -v "${HOME}/.cache/huggingface:/workspace/.cache/huggingface" `
  -v "unsloth-studio:/opt/unsloth-studio" `
  unsloth/unsloth
```

* Run it from your project folder, because that folder (`${PWD}`) becomes `/workspace/host`.
* What the flags do: exposing ports 8000 (Unsloth Studio) and 8888 (JupyterLab); the three `-v` flags keep your files, models and Unsloth Studio data.
* Requirement: NVIDIA driver 570.26 or newer.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F70dKPYWYN9PrkPkMtbdg%2Fimage.png?alt=media&amp;token=5b4a4309-c97b-4e65-8daa-babb312a97ca" alt=""><figcaption></figcaption></figure>
{% endtab %}
{% endtabs %}

### Prerequisites

If you do not have Docker installed for NVIDIA Container Toolkit, follow the below:

{% tabs %}
{% tab title="Linux / WSL" %}
Install [Docker Engine](https://docs.docker.com/engine/install/) or [Docker Desktop](https://docs.docker.com/desktop/), if you haven't already:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
```

If you have an NVIDIA GPU, install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installation) if you haven't already:

```bash
curl -fsSL https://raw.githubusercontent.com/unslothai/unsloth/main/docker/install_nvidia_toolkit.sh -o install_nvidia_toolkit.sh && sudo -E bash install_nvidia_toolkit.sh
```

{% endtab %}

{% tab title="Windows" %}
**Install Docker Desktop and the NVIDIA driver.**

Install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) and the latest [NVIDIA Windows driver](https://www.nvidia.com/Download/index.aspx). \
Then update WSL in PowerShell:

```powershell
wsl --update
```

In Docker Desktop settings, select **General** and check that **Use the WSL 2 based engine** is enabled. Wait for the engine to start before continuing.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FNSQSDRFKVGyePWp7zKZA%2Fimage.png?alt=media&amp;token=0516785a-3fc1-41bc-8690-b98df7085fbf" alt=""><figcaption></figcaption></figure>

No separate NVIDIA Container Toolkit installation is needed. [Windows GPU troubleshooting](https://docs.docker.com/desktop/features/gpu/).
{% endtab %}
{% endtabs %}

### AMD Quickstart

This guide section applies to systems with AMD GPUs. If you have [NVIDIA see here](#quickstart).

{% tabs %}
{% tab title="Linux" %}
To get Unsloth's Docker on AMD GPUs, run the following in terminal:

```bash
GPU_FLAGS="--device /dev/kfd"
[ -e /dev/dri ] && GPU_FLAGS="$GPU_FLAGS --device /dev/dri"
for g in video render; do
  gid=$(getent group "$g" | cut -d: -f3)
  [ -n "$gid" ] && GPU_FLAGS="$GPU_FLAGS --group-add $gid"
done
docker run -d --name unsloth \
  $GPU_FLAGS \
  --ipc=host \
  --ulimit memlock=-1 --ulimit stack=67108864 \
  -p 8000:8000 -p 8888:8888 \
  -e JUPYTER_PASSWORD="mypassword" \
  -v "$PWD":/workspace/host \
  -v "$HOME/.cache/huggingface":/workspace/.cache/huggingface \
  -v unsloth-studio:/opt/unsloth-studio \
  unsloth/unsloth-rocm
```

* Run it from your project folder, because that folder (`$PWD`) becomes `/workspace/host`.
* What the flags do: `$GPU_FLAGS` passes the GPU device nodes and group ids; ports 8000 (Unsloth Studio) and 8888 (JupyterLab); the three `-v` flags keep your files, models and Unsloth Studio data.
* Requirement: a working `amdgpu` driver. Built against ROCm 7.2, covers RDNA1 and newer, plus CDNA.
  {% endtab %}

{% tab title="WSL" %}
In WSL, AMD GPUs are reached through WSL2's DXG bridge. Run this inside your WSL2 distro, not PowerShell, WSL2 has no `/dev/kfd` so the GPU is passed as `/dev/dxg` instead:

```bash
docker run -d --name unsloth --device /dev/dxg --ipc=host \
  --ulimit memlock=-1 --ulimit stack=67108864 \
  -e HSA_ENABLE_DXG_DETECTION=1 \
  -e LD_LIBRARY_PATH=/usr/lib/wsl/lib:/opt/rocm/lib \
  -p 8000:8000 -p 8888:8888 \
  -e JUPYTER_PASSWORD="mypassword" \
  -v /usr/lib/wsl/lib:/usr/lib/wsl/lib:ro \
  -v "$PWD":/workspace/host \
  -v "$HOME/.cache/huggingface":/workspace/.cache/huggingface \
  -v unsloth-studio:/opt/unsloth-studio \
  unsloth/unsloth-rocm
```

* Run it from inside WSL2 (`wsl -d Ubuntu`), from your project folder, because that folder (`$PWD`) becomes `/workspace/host`.
* What the flags do: `--device /dev/dxg` and the `/usr/lib/wsl/lib` mount pass the GPU through WSL2; ports 8000 (Unsloth Studio) and 8888 (JupyterLab); the three `-v` flags keep your files, models and Unsloth Studio data.
* Requirement: the AMD Windows driver with WSL2 support on the host
  {% endtab %}

{% tab title="Windows (PowerShell)" %}
Run the following in PowerShell:

```powershell
docker run -d --name unsloth --device /dev/dxg --ipc=host `
  --ulimit memlock=-1 --ulimit stack=67108864 `
  -e HSA_ENABLE_DXG_DETECTION=1 `
  -e LD_LIBRARY_PATH=/usr/lib/wsl/lib:/opt/rocm/lib `
  -p 8000:8000 -p 8888:8888 `
  -e JUPYTER_PASSWORD="mypassword" `
  -v "/usr/lib/wsl/lib:/usr/lib/wsl/lib:ro" `
  -v "${PWD}:/workspace/host" `
  -v "${HOME}/.cache/huggingface:/workspace/.cache/huggingface" `
  -v "unsloth-studio:/opt/unsloth-studio" `
  unsloth/unsloth-rocm
```

* Run it from your project folder, because that folder (`${PWD}`) becomes `/workspace/host`.
* Requirement: an AMD Windows driver with WSL2 support, and Docker Desktop using the WSL 2 engine.
  {% endtab %}
  {% endtabs %}

If you do not have Docker installed, run the following command:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
```

AMD needs no container toolkit, only the `amdgpu` driver on the host. On Windows, install Docker Desktop and the AMD driver with WSL2 support.

### 📖 Usage Guides

#### Unsloth Studio Setup

Unsloth Studio comes pre-installed, so you can chat with models, fine-tune them and generate images from the same Docker container.

{% stepper %}
{% step %}
**Start the Unsloth container.** \
Run the full `docker run` command for your OS in **Quickstart** and allow about a minute for startup. Skip this if your container is already running.

```bash
docker start unsloth
```

{% endstep %}

{% step %}
**Find your passwords.** \
If you don’t already know your password, check the container logs:

```bash
docker logs -f unsloth
```

Look for **Unsloth container ready** for links and password details. Press **Ctrl+C** to stop following the logs; the container keeps running.
{% endstep %}

{% step %}
**Sign in**

Open [`http://localhost:8000`](http://localhost:8000) and sign in as `unsloth`. On first setup, use the generated password and choose a new one when prompted. Otherwise, use your existing password.
{% endstep %}

{% step %}
**Forgot your password?**

```bash
docker exec unsloth unsloth studio reset-password --username unsloth
```

This generates a new password, signs out existing sessions and revokes API keys. No restart is needed. These commands assume your container is named `unsloth`. If needed, run `docker ps` to find its name or ID.

{% hint style="info" %}
If Docker runs on another machine (like a cloud GPU or a server), `localhost` means your own computer. You must forward the ports before you open the links. Run `ssh -L 8000:localhost:8000 -L 8888:localhost:8888 user@your-server`. See the [Security Notes](#security-notes) section for details.
{% endhint %}
{% endstep %}
{% endstepper %}

#### **Chat with a model**

{% hint style="info" %}
Unsloth Studio and JupyterLab share the same GPU. A model loaded in Unsloth keeps its GPU memory until you unload it. If you run out of memory, unload the model in Unsloth or stop the notebook kernel.
{% endhint %}

{% stepper %}
{% step %}
**Choose and download a model**

Open **Select model** at the top of the page. Browse **Recommended**, or enter a model name and click **Search Hub** to search Hugging Face. You can also browse models in **Model hub**.

For GGUF models, choose a quantization that fits your available RAM and VRAM. Avoid variants marked **OOM**.

Wait for the model to finish downloading and loading before sending your first message. You can select downloaded models again from **On Device**.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FgyDczCQqKkgh7ap2PuNU%2Fimage.png?alt=media&amp;token=740ee435-e68f-4811-8bb6-aa093526f74f" alt="Unsloth Studio model selector with Hugging Face search and recommended GGUF models." width="375"><figcaption><p>Browse recommended models or search by name.</p></figcaption></figure>

{% hint style="info" %}
Downloaded models are stored in `/workspace/.cache/huggingface`. With the Quickstart volume mount, this cache is shared with notebooks and stays on your computer even if you remove the container.
{% endhint %}
{% endstep %}

{% step %}
**Send a message**

Once the model is ready, type a message and press **Enter**. Try:

> Explain how Docker containers differ from virtual machines.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FKfzGAT0DLWirgWvkfK1x%2Fimage.png?alt=media&amp;token=afff9dd2-06d4-4f7b-bba5-8a4835143090" alt=""><figcaption></figcaption></figure>

See the [Unsloth Studio Chat](/docs/new/studio/chat.md) guide for web search and more chat settings.
{% endstep %}
{% endstepper %}

#### **Train a model**

You can train models across text, [vision](https://unsloth.ai/docs/basics/vision-fine-tuning) and [audio](https://unsloth.ai/docs/basics/text-to-speech-tts-fine-tuning), with support for [embeddings](https://unsloth.ai/docs/basics/embedding-finetuning) and image diffusion too. All from the same Docker image.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F66Vvgt0l5iqAkAksIRYF%2Fimage.png?alt=media&amp;token=8fcb1ad6-2b53-4128-87fa-a47bcd1deab4" alt="" width="563"><figcaption></figcaption></figure>

**Choose a model and dataset**

Select **Train** and open **Configure**. Choose a model and training method, then select a Hugging Face dataset or upload your own.

**Start training**

Review **Parameters** in **Simple** or **Advanced** mode, then click **Start Training**. Track progress, loss and GPU usage in **Current Run**.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FD7qpbGJLY5YMv0E0QgrB%2Ftrainingrun_LLM-unsloth.gif?alt=media&amp;token=feb766a7-1a7b-4f47-b5f4-b38e3a0d1470" alt=""><figcaption></figcaption></figure>

**Try your trained model**

When training finishes, click **Compare in Chat**. Test the original and fine-tuned models with the same prompts to see how their responses differ.

See the [Studio training guide](https://unsloth.ai/docs/new/studio/start) for more detail, or use [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe) to prepare your dataset.

#### **Generate images**

{% stepper %}
{% step %}
**Open Images and choose a model**

Select **Images** in the sidebar. The **Create** workflow opens by default.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F6WVNnM49nQoTBfv57RAs%2Fimage%20(529).png?alt=media&amp;token=ff61651a-4560-4473-9232-d06024cb216e" alt="Unsloth Studio Images page with Create selected in the sidebar and prompt controls." width="375"><figcaption><p>Open Images to create an image from a text prompt.</p></figcaption></figure>

Open **Select image model** and choose from **Recommended**, such as Z-Image-Turbo. For GGUF models, pick a quantization that fits your device. **TIGHT** may run slowly; **OOM** is unlikely to fit.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2F1gPBEymJifbpIE9lGfvd%2Fimage%20(530).png?alt=media&amp;token=6f1b3e41-2c5a-4c5a-9c75-f624c6f4ede6" alt="Image model selector showing Z-Image-Turbo-GGUF and available quantizations." width="375"><figcaption><p>Choose an image model and a quantization for your device.</p></figcaption></figure>
{% endstep %}

{% step %}
**Enter a prompt and generate**

Describe the image you want to create. For example:

> Top-down shot of a koi pond in a Japanese garden, dozens of orange, white and black koi swimming in tight formation, water clear enough to see the stone bottom, red maple leaves floating on the surface. Bright midday light, saturated colour, crisp reflections. Realistic photo, 50mm.

Leave the image settings at their defaults and click **Generate**.

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2Fy0qucNcG7XQlDVvv3XZE%2Fimage%20(493).png?alt=media&amp;token=47888a19-5384-4ace-b5d7-f90cf4fb9b0f" alt="Unsloth Studio Create images page with Z-Image-Turbo loaded, a koi pond prompt, a generated image, and Recipe and Download controls." width="563"><figcaption><p>An example generation with Z-Image-Turbo.</p></figcaption></figure>

Open your image in the gallery and click **Download** to save it, or **Recipe** to reuse its prompt and settings.

**Transform**, **Inpaint** and **Edit** depend on the loaded model. See the [image diffusion guide](https://unsloth.ai/docs/basics/diffusion-image) for supported workflows and settings.
{% endstep %}
{% endstepper %}

#### **Access JupyterLab**

{% columns %}
{% column %}
The Unsloth Docker image includes JupyterLab and ready-to-use notebooks.

Open [`http://localhost:8888`](http://localhost:8888) and sign in. Use the `JUPYTER_PASSWORD` you chose when starting the container. If you did not set one, use the generated password printed in the container log.

{% hint style="info" %}
JupyterLab passwords are set when the container is created. To change it, remove and recreate the container with a new password.
{% endhint %}
{% endcolumn %}

{% column %}

<figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FQapcJDBCYgxaEfG5zEEn%2Fimage.png?alt=media&amp;token=8eb72fbd-8ca1-43f6-9c6a-e45cb7a06da0" alt="" width="375"><figcaption></figcaption></figure>
{% endcolumn %}
{% endcolumns %}

After signing in, you’ll see **Unsloth Notebooks**, with folders grouped by model and task.

These folders contain shortcuts to the notebook files in `/workspace/unsloth-notebooks`. Each time the container starts, the notebooks are refreshed from GitHub without overwriting\
your edits.

Double-click **01 Main Notebooks** to browse examples, or choose a category such as vision, speech or reinforcement learning.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FXceIgyo451mqw1hchpXR%2Fimage.png?alt=media&amp;token=b32a2968-0e94-4eff-b6a5-ed9f9b617ca4" alt="" width="563"><figcaption></figcaption></figure></div>

#### **Fine-tune a model in a notebook**

Unload any model loaded in Unsloth Studio before you start training, so the notebook has the GPU memory it needs.

Open a notebook in **01 Main Notebooks** and follow its instructions. Press **Shift+Enter** to run each cell in order. The first run downloads the model into the Hugging Face cache.

For example, `Gemma3_(4B)-Vision.ipynb` guides you through fine-tuning Gemma 3 4B to turn images of equations into LaTeX.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FyLdWCorjvMlW0OPkE2v4%2Fimage.png?alt=media&amp;token=ca2e62b5-5857-4cbf-89f4-735030f1123b" alt="" width="563"><figcaption></figcaption></figure></div>

After training, test your model using the notebook's **Inference** section. It tests the trained model on an equation image. The equation is below, recreated at higher resolution here for readability.

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FGJdMUUr0ig4NQL5TMk2I%2Fimage.png?alt=media&amp;token=fa1eb118-dcbd-4ad3-a8f4-48e47659c143" alt="" width="563"><figcaption></figcaption></figure></div>

The model generates LaTeX from the original dataset image. It prints the LaTeX result below the cell.

#### **Save and export your model**

Follow the notebook's Saving section to save your trained LoRA adapters or export your merged model.

A relative path like `"gemma_3_lora"` saves next to the notebook, inside `/workspace/Unsloth Notebooks/...`. That folder is inside the container, so it is deleted when you remove the container. To keep your results on your computer, save under `/workspace/host`.

* **Save LoRA adapters locally:** This cell runs by default. Change the path to `/workspace/host`.

  ```python
  model.save_pretrained("/workspace/host/gemma_3_lora")
  processor.save_pretrained("/workspace/host/gemma_3_lora")
  ```
* **Export merged 16-bit model:** In the export cell, change `if False:` to `if True:` for the option you want. Only pick one.

  ```python
  if True: model.save_pretrained_merged("/workspace/host/unsloth_finetune", processor)
  ```

<div data-with-frame="true"><figure><img src="https://3215535692-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FxhOjnexMCB3dmuQFQ2Zq%2Fuploads%2FERw6laeLKXj5mLtoWB8y%2Fimage.png?alt=media&amp;token=5d43449b-cc98-4448-93f5-79599d39148f" alt="" width="563"><figcaption></figcaption></figure></div>

* **Upload to Hugging Face:** You need a token with write access to upload. Replace the `YOUR_USERNAME` and `YOUR_HF_TOKEN` placeholders with your own details.

For more guidance, see our [Fine-tuning Guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide), [RL Guide](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide), and [notebook collection](https://github.com/unslothai/notebooks).

#### Stop, restart and update the container

Commands take the container name or id, not the image name `unsloth/unsloth`.

Shut down the container but keep it:

```bash
docker stop unsloth
```

Bring it back in the same state:

```bash
docker start unsloth
```

Find your container again, running or not:

```bash
docker ps -a
```

Stop and delete the container:

```bash
docker rm -f unsloth
```

Deleting the container does not delete your models, your host files (`/workspace/host`), or Unsloth Studio data (accounts, chats, and exports). A new container with the same `-v` flags continues where you left off, and your Unsloth password stays the same. Anything else written inside the container is lost.

To delete Unsloth Studio's data permanently, remove its volume:

```bash
docker volume rm unsloth-studio
```

To update to the latest Unsloth version, pull the new image:

```bash
#NVIDIA GPUS
docker pull unsloth/unsloth
#AMD GPUS
docker pull unsloth/unsloth-rocm
```

Then remove the old container and run the Quickstart command again with the same flags. Your models, files and Unsloth Studio data carry over.

```bash
docker rm -f unsloth
```

#### **Connect over SSH**

SSH is off unless you set `SSH_KEY` or `PUBLIC_KEY`. You connect as the `root` user with key-only authentication on port 22 inside the container.

Generate an SSH key:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/container_key
```

The SSH key is applied when the container is created, so you must recreate the container to add it. Use this full command to map the SSH port to 2222 on your host, set your passwords, and mount your volumes.

{% tabs %}
{% tab title="NVIDIA" %}

```bash
docker run -d --name unsloth --gpus all --ipc=host \
  --ulimit memlock=-1 --ulimit stack=67108864 \
  -p 8000:8000 -p 8888:8888 -p 2222:22 \
  -e JUPYTER_PASSWORD="choose-a-jupyter-password" \
  -e UNSLOTH_STUDIO_PASSWORD="choose-a-studio-password" \
  -e SSH_KEY="$(cat ~/.ssh/container_key.pub)" \
  -v "$PWD":/workspace/host \
  -v "$HOME/.cache/huggingface":/workspace/.cache/huggingface \
  -v unsloth-studio:/opt/unsloth-studio \
  unsloth/unsloth
```

{% endtab %}

{% tab title="AMD" %}

```bash
GPU_FLAGS="--device /dev/kfd"
[ -e /dev/dri ] && GPU_FLAGS="$GPU_FLAGS --device /dev/dri"
for g in video render; do
  gid=$(getent group "$g" | cut -d: -f3)
  [ -n "$gid" ] && GPU_FLAGS="$GPU_FLAGS --group-add $gid"
done
docker run -d --name unsloth $GPU_FLAGS --ipc=host \
  --ulimit memlock=-1 --ulimit stack=67108864 \
  -p 8000:8000 -p 8888:8888 -p 2222:22 \
  -e JUPYTER_PASSWORD="choose-a-jupyter-password" \
  -e UNSLOTH_STUDIO_PASSWORD="choose-a-studio-password" \
  -e SSH_KEY="$(cat ~/.ssh/container_key.pub)" \
  -v "$PWD":/workspace/host \
  -v "$HOME/.cache/huggingface":/workspace/.cache/huggingface \
  -v unsloth-studio:/opt/unsloth-studio \
  unsloth/unsloth-rocm
```

{% endtab %}
{% endtabs %}

`UNSLOTH_STUDIO_PASSWORD` applies only the first time the `unsloth-studio` volume is used. See [Advanced Settings](#advanced-settings) below for all environment variables, volumes and ports.

Connect to the container:

```bash
ssh -i ~/.ssh/container_key -p 2222 root@localhost
```

#### 📂 Container Structure

* `/workspace/host/` — Your mounted work directory
* `/workspace/.cache/huggingface` — Model and dataset downloads
* `/workspace/.cache/triton` — Compiled Triton kernels
* `/workspace/unsloth-notebooks/` — Example fine-tuning notebooks, including your edits
* `/workspace/Unsloth Notebooks` — Example fine-tuning notebooks grouped by topic, rebuilt on each start
* `/opt/unsloth-studio` — Unsloth Studio's accounts, chats, outputs, exports and runs

### Troubleshooting

#### **Unsloth not detecting or using my GPU**

If the model is not using your GPU specifically for Docker, try:

Pulling the latest image manually:

```bash
 #NVIDIA GPUS
 docker pull unsloth/unsloth:latest
 #AMD GPUS
 docker pull unsloth/unsloth-rocm:latest
```

* Start the container with GPU access:
  * `docker run`: `--gpus all`
  * Docker Compose: `capabilities: [gpu]`
  * AMD: `--device /dev/kfd --device /dev/dri` plus the `--group-add` ids (the `$GPU_FLAGS` block in Quickstart)
* On Linux (NVIDIA), make sure the NVIDIA Container Toolkit is installed, and docker is restarted after installing it.
* On Windows (NVIDIA):
  * Run `docker exec unsloth nvidia-smi`. If it lists your GPU, the container can see it.
  * Follow [Docker's guide](< https://docs.docker.com/desktop/features/gpu/>)
* On AMD: run `docker exec unsloth rocm-smi`. If it lists your GPU, the container can see it. A permission error on `/dev/kfd` means the `--group-add` ids were missing.

#### Port is already allocated

Change the host side port, e.g. `-p 8001:8000`, then open [http://localhost:8001](http://localhost:8001/).

#### Unsloth Studio stopped responding after an hour

Unsloth Studio auto shuts down if the auto generated password is not changed. Run `docker restart unsloth` to start it again and change password.

#### Files in your project folder are owned by root

The container runs as root, so use `sudo chown`, or `core` with `--user`.

### ⚙️ Advanced Settings

#### Environment variables

Pass any of these to `docker run` with `-e NAME=value` or `--env-file`. These apply to both `unsloth/unsloth` and `unsloth/unsloth-rocm`.

| Variable                           | Description                                                                       | Default                                            |
| ---------------------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------- |
| `UNSLOTH_STUDIO_PASSWORD`          | Initial Unsloth Studio password for user `unsloth`                                | Unset: generated once and printed in `docker logs` |
| `JUPYTER_PASSWORD`                 | JupyterLab password                                                               | Unset: generated once and printed in `docker logs` |
| `JUPYTER_PORT`                     | JupyterLab port inside container                                                  | `8888`                                             |
| `UNSLOTH_STUDIO_PORT`              | Unsloth Studio port inside the container                                          | `8000`                                             |
| `UNSLOTH_STUDIO_BOOTSTRAP_TIMEOUT` | Seconds before Unsloth Studio shuts down if the generated password is not changed | `3600`                                             |
| `SSH_KEY` or `PUBLIC_KEY`          | SSH public key for `root` login                                                   | Unset: SSH off                                     |
| `UNSLOTH_ALLOW_CPU`                | Allow the container to start without a GPU                                        | `1`, Unset when a GPU is visible                   |
| `UNSLOTH_STUDIO_SECURE`            | Serve Unsloth Studio only through a public Cloudflare HTTPS link                  | `0`                                                |
| `UNSLOTH_STUDIO_CLOUDFLARE`        | Share Unsloth Studio through a public Cloudflare link                             | `0`                                                |
| `UNSLOTH_JUPYTER_CLOUDFLARE`       | Share JupyterLab through a public Cloudflare link                                 | `0`                                                |
| `UNSLOTH_SKIP_NOTEBOOK_REFRESH`    | Skip updating the example notebooks from GitHub                                   | `0`                                                |
| `UNSLOTH_SKIP_NOTEBOOK_SYNC`       | Skip setting up the example notebooks                                             | `0`                                                |
| `HF_TOKEN`                         | Hugging Face access token                                                         | Unset                                              |
| `WANDB_API_KEY`                    | Weights & Biases API key                                                          | Unset                                              |

#### Volume

{% hint style="warning" %}
**Important**: Use volume mounts to preserve your work between container runs.
{% endhint %}

Anything not on a volume is lost when the container is removed. Mount these with `-v <host path or volume name>:<container path>`.

| Container path                  | Description                                                      | Suggested mount                                                 |
| ------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------- |
| `/workspace/host`               | Your project files                                               | Your project folder, e.g. `"$PWD"`                              |
| `/workspace/.cache/huggingface` | Downloaded models and datasets                                   | Your host Hugging Face cache, e.g. `"$HOME/.cache/huggingface"` |
| `/opt/unsloth-studio`           | Unsloth Studio accounts, chats, trained models, exports and runs | Named volume `unsloth-studio`                                   |
| `/workspace/unsloth-notebooks`  | Example notebooks, including your edits                          | Optional                                                        |
| `/workspace/.cache/triton`      | Compiled GPU kernels                                             | Optional, speeds up restarts                                    |

* `/workspace` is the working directory and the folder JupyterLab opens in.
* Use a named volume for `/opt/unsloth-studio`, not a host folder. Unsloth Studio needs symlinks there, and a Windows or macOS host folder may not allow them, which stops the container at start.
* To give Unsloth Studio or JupyterLab more of your files, mount more folders under `/workspace`, e.g. `-v /data/datasets:/workspace/datasets`, and refer to them by that container path.

#### Ports

| Port   | Service                          |
| ------ | -------------------------------- |
| `8000` | Unsloth Studio                   |
| `8888` | JupyterLab                       |
| `22`   | SSH (only when `SSH_KEY` is set) |

Map a container port to any free host port with `-p <host>:<container>`. For example, to enable SSH on host port `2222`:

{% tabs %}
{% tab title="NVIDIA" %}

```bash
docker run -d --name unsloth --gpus all \
  -p 8000:8000 -p 8888:8888 -p 2222:22 \
  -e SSH_KEY="$(cat ~/.ssh/id_ed25519.pub)" \
  -v "$PWD":/workspace/host \
  -v "$HOME/.cache/huggingface":/workspace/.cache/huggingface \
  -v unsloth-studio:/opt/unsloth-studio \
  unsloth/unsloth
```

{% endtab %}

{% tab title="AMD" %}

```bash
GPU_FLAGS="--device /dev/kfd"
[ -e /dev/dri ] && GPU_FLAGS="$GPU_FLAGS --device /dev/dri"
for g in video render; do
  gid=$(getent group "$g" | cut -d: -f3)
  [ -n "$gid" ] && GPU_FLAGS="$GPU_FLAGS --group-add $gid"
done
docker run -d --name unsloth $GPU_FLAGS \
  -p 8000:8000 -p 8888:8888 -p 2222:22 \
  -e SSH_KEY="$(cat ~/.ssh/id_ed25519.pub)" \
  -v "$PWD":/workspace/host \
  -v "$HOME/.cache/huggingface":/workspace/.cache/huggingface \
  -v unsloth-studio:/opt/unsloth-studio \
  unsloth/unsloth-rocm
```

{% endtab %}
{% endtabs %}

### **🔒 Security Notes**

* The container runs as root. Use `unsloth/unsloth:core` with `--user <uid>:<gid>` if you need mounted files owned by your host user.
* SSH is off unless `SSH_KEY` or `PUBLIC_KEY` is set. It is key-only, as root, on port 22.
* Published ports listen on every interface. On a cloud host, bind to `127.0.0.1` or use `-e UNSLOTH_STUDIO_SECURE=1`.
* JupyterLab is a full shell. Anyone who can log in to JupyterLab can run any command in the container. Unsloth Studio and JupyterLab serve plain HTTP, so do not expose them to the internet directly.
* Unsloth Studio tools can run code. Studio's server-side tools are on by default and can run commands inside the container. Only mount host folders you are comfortable giving the container access to.
* Environment variables are visible to Docker users. Values passed with `-e` or `--env-file`, including tokens and passwords, show up in `docker inspect`. Anyone with access to the Docker daemon can read them.


---

# Agent Instructions
This documentation is published with GitBook. GitBook is the documentation platform designed so that both humans and AI agents can read, navigate, and reason over technical content effectively. Learn more at gitbook.com.

## Querying This Documentation
If you need additional information that is not directly available in this page, you can query the documentation by asking a question.

Perform an HTTP GET request on the following URL with the `ask` and `goal` query parameters:

```
GET https://unsloth.ai/docs/get-started/install/docker.md?ask=<question>&goal=<user_goal>
```

`ask` is the immediate question: it should be specific, self-contained, and written in natural language.
`goal` is what the user is ultimately trying to achieve, the reason they need the answer. Sharing it helps GitBook give you a better, more relevant answer. A goal is most helpful when it describes the outcome the user wants rather than restating the question. For example, with `ask=how do I create an API token`, a goal like `automate deployments from our CI pipeline` lets GitBook tailor the answer to that use case.

The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.
