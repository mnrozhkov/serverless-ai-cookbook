# Nebius Serverless Templates

<!-- catalog:generated — HTML tables with fixed column widths; do not auto-format -->

Templates are quick-start configurations to help you serve models and run jobs in a few clicks. Click a **Deploy** link (Create Endpoint / Create Job) to open the Nebius Console create form with fields pre-filled. You can manually adjust fields if needed.

**License policy:** Apache-2.0, MIT, BSD, [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).

---

## Endpoints

### 🎨 Text-to-Image

<table width="960" border="1" cellpadding="8" cellspacing="0" style="table-layout:fixed;width:960px;min-width:960px;border-collapse:collapse;">
<colgroup>
  <col width="220">
  <col width="210">
  <col width="530">
</colgroup>
<thead>
<tr>
  <th width="220" align="left">Template</th>
  <th width="210" align="center">Deploy</th>
  <th width="530" align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/6215ca5692c0ecfba9186921/hrRM50-6XcdWgg2AKpENG.jpeg" width="20" height="20" alt="Qwen-Image">&nbsp;<a href="endpoint-qwen-image/README.md"><strong>Qwen-Image</strong></a></td>
  <td width="210" valign="middle">

[![Create Endpoint](assets/create-endpoint.svg)](https://console.eu.nebius.com/serverless/endpoint/create?image=vllm%2Fvllm-omni%3Alatest&command=vllm%20serve%20Qwen%2FQwen-Image%20--omni%20--host%200.0.0.0%20--port%208000&targetPort=8000&platform=gpu-h100-sxm&preset=1gpu-16vcpu-200gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">Qwen-Image is an Apache-2.0 multimodal image generation model with strong text rendering, served on preemptible H100 via vLLM-Omni.</td>
</tr>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/62b4b5beb25cb80fcf278354/SIddx3hYu5rWXA4-O3Oaj.jpeg" width="20" height="20" alt="Sana">&nbsp;<a href="endpoint-sana/README.md"><strong>Sana</strong></a></td>
  <td width="210" valign="middle">

[![Create Endpoint](assets/create-endpoint.svg)](https://console.eu.nebius.com/serverless/endpoint/create?image=docker.io%2Fmnrozhkov%2Fsana-serve&targetPort=8000&platform=gpu-l40s-a&preset=1gpu-8vcpu-32gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">Sana 1.6B is a fast Apache-2.0 1024px text-to-image model (~9GB weights) for single-L40S Diffusers serving.</td>
</tr>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/64379d79fac5ea753f1c10f3/fxHO6QoYjdv9_LTyiUD3g.jpeg" width="20" height="20" alt="Z-Image-Turbo">&nbsp;<a href="endpoint-z-image-turbo/README.md"><strong>Z-Image-Turbo</strong></a></td>
  <td width="210" valign="middle">

[![Create Endpoint](assets/create-endpoint.svg)](https://console.eu.nebius.com/serverless/endpoint/create?image=vllm%2Fvllm-omni%3Alatest&command=vllm%20serve%20Tongyi-MAI%2FZ-Image-Turbo%20--omni%20--host%200.0.0.0%20--port%208000&targetPort=8000&platform=gpu-h100-sxm&preset=1gpu-16vcpu-200gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">Z-Image-Turbo is a 6B Apache-2.0 text-to-image model distilled for 8-step generation, served on preemptible H100 via vLLM-Omni.</td>
</tr>
</tbody>
</table>

### 🖼️ Image-to-Image

<table width="960" border="1" cellpadding="8" cellspacing="0" style="table-layout:fixed;width:960px;min-width:960px;border-collapse:collapse;">
<colgroup>
  <col width="220">
  <col width="210">
  <col width="530">
</colgroup>
<thead>
<tr>
  <th width="220" align="left">Template</th>
  <th width="210" align="center">Deploy</th>
  <th width="530" align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/6215ca5692c0ecfba9186921/hrRM50-6XcdWgg2AKpENG.jpeg" width="20" height="20" alt="Qwen-Image-Edit-2511">&nbsp;<a href="endpoint-qwen-image-edit-2511/README.md"><strong>Qwen-Image-Edit-2511</strong></a></td>
  <td width="210" valign="middle">

[![Create Endpoint](assets/create-endpoint.svg)](https://console.eu.nebius.com/serverless/endpoint/create?image=vllm%2Fvllm-omni%3Alatest&command=vllm%20serve%20Qwen%2FQwen-Image-Edit-2511%20--omni%20--host%200.0.0.0%20--port%208000&targetPort=8000&platform=gpu-h100-sxm&preset=1gpu-16vcpu-200gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">Qwen-Image-Edit-2511 is an Apache-2.0 image-to-image editor for instruction-based edits, served on preemptible H100 via vLLM-Omni.</td>
</tr>
</tbody>
</table>

### 🎬 Text-to-Video

<table width="960" border="1" cellpadding="8" cellspacing="0" style="table-layout:fixed;width:960px;min-width:960px;border-collapse:collapse;">
<colgroup>
  <col width="220">
  <col width="210">
  <col width="530">
</colgroup>
<thead>
<tr>
  <th width="220" align="left">Template</th>
  <th width="210" align="center">Deploy</th>
  <th width="530" align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/67b610677ea7952def8b29c6/N6jQbbeaa_FcUY-wI1dgG.png" width="20" height="20" alt="Wan2.1-T2V-1.3B">&nbsp;<a href="endpoint-wan21-t2v-1-3b/README.md"><strong>Wan2.1-T2V-1.3B</strong></a></td>
  <td width="210" valign="middle">

[![Create Endpoint](assets/create-endpoint.svg)](https://console.eu.nebius.com/serverless/endpoint/create?image=vllm%2Fvllm-omni%3Alatest&command=vllm%20serve%20Wan-AI%2FWan2.1-T2V-1.3B-Diffusers%20--omni%20--host%200.0.0.0%20--port%208000&targetPort=8000&platform=gpu-h100-sxm&preset=1gpu-16vcpu-200gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">Wan2.1-T2V-1.3B is a compact Apache-2.0 text-to-video Diffusers checkpoint for short clips on preemptible H100 via vLLM-Omni.</td>
</tr>
</tbody>
</table>

### 🎥 Image-to-Video

<table width="960" border="1" cellpadding="8" cellspacing="0" style="table-layout:fixed;width:960px;min-width:960px;border-collapse:collapse;">
<colgroup>
  <col width="220">
  <col width="210">
  <col width="530">
</colgroup>
<thead>
<tr>
  <th width="220" align="left">Template</th>
  <th width="210" align="center">Deploy</th>
  <th width="530" align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/67b610677ea7952def8b29c6/N6jQbbeaa_FcUY-wI1dgG.png" width="20" height="20" alt="Wan2.2-I2V-A14B">&nbsp;<a href="endpoint-wan22-i2v-a14b/README.md"><strong>Wan2.2-I2V-A14B</strong></a></td>
  <td width="210" valign="middle">

[![Create Endpoint](assets/create-endpoint.svg)](https://console.eu.nebius.com/serverless/endpoint/create?image=vllm%2Fvllm-omni%3Alatest&command=vllm%20serve%20Wan-AI%2FWan2.2-I2V-A14B-Diffusers%20--omni%20--host%200.0.0.0%20--port%208000&targetPort=8000&platform=gpu-h100-sxm&preset=1gpu-16vcpu-200gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">Wan2.2-I2V-A14B is a flagship Apache-2.0 image-to-video model (~35GB) for 480p clips on preemptible H100 via vLLM-Omni.</td>
</tr>
</tbody>
</table>

### 🗣️ Text-to-Speech

<table width="960" border="1" cellpadding="8" cellspacing="0" style="table-layout:fixed;width:960px;min-width:960px;border-collapse:collapse;">
<colgroup>
  <col width="220">
  <col width="210">
  <col width="530">
</colgroup>
<thead>
<tr>
  <th width="220" align="left">Template</th>
  <th width="210" align="center">Deploy</th>
  <th width="530" align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/6000a0456a2a91af974298cf/qmxSbcVBCwUtVez918IkQ.png" width="20" height="20" alt="Chatterbox">&nbsp;<a href="endpoint-chatterbox/README.md"><strong>Chatterbox</strong></a></td>
  <td width="210" valign="middle">

[![Create Endpoint](assets/create-endpoint.svg)](https://console.eu.nebius.com/serverless/endpoint/create?image=docker.io%2Fmnrozhkov%2Fchatterbox-serve&targetPort=8000&platform=gpu-h100-sxm&preset=1gpu-16vcpu-200gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">Chatterbox is a MIT expressive English TTS model with bundled preset voices and an OpenAI-compatible speech API on preemptible H100.</td>
</tr>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/6629552c96f529a39bac7c89/EaoEz4WH2VoE5twl2oJie.png" width="20" height="20" alt="Kokoro-82M">&nbsp;<a href="endpoint-kokoro-82m/README.md"><strong>Kokoro-82M</strong></a></td>
  <td width="210" valign="middle">

[![Create Endpoint](assets/create-endpoint.svg)](https://console.eu.nebius.com/serverless/endpoint/create?image=docker.io%2Fmnrozhkov%2Fkokoro-serve&targetPort=8000&platform=gpu-l40s-a&preset=1gpu-8vcpu-32gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">Kokoro-82M is an 82M-parameter Apache-2.0 text-to-speech model with an OpenAI-compatible speech API on a single L40S.</td>
</tr>
</tbody>
</table>

### 🎵 Text-to-Audio

<table width="960" border="1" cellpadding="8" cellspacing="0" style="table-layout:fixed;width:960px;min-width:960px;border-collapse:collapse;">
<colgroup>
  <col width="220">
  <col width="210">
  <col width="530">
</colgroup>
<thead>
<tr>
  <th width="220" align="left">Template</th>
  <th width="210" align="center">Deploy</th>
  <th width="530" align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/6209bb6ede1c3ff3ec37620c/xk4TNYgu3UPz74tAgzTrA.jpeg" width="20" height="20" alt="ACE-Step 1.5">&nbsp;<a href="endpoint-ace-step-1-5/README.md"><strong>ACE-Step 1.5</strong></a></td>
  <td width="210" valign="middle">

[![Create Endpoint](assets/create-endpoint.svg)](https://console.eu.nebius.com/serverless/endpoint/create?image=docker.io%2Fmnrozhkov%2Facestep-serve&targetPort=8000&platform=gpu-h100-sxm&preset=1gpu-16vcpu-200gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">ACE-Step 1.5 is an MIT text-to-audio (music) model with a sync OpenAI-shaped generation API on preemptible H100.</td>
</tr>
</tbody>
</table>

### 💬 Large Language Models

<table width="960" border="1" cellpadding="8" cellspacing="0" style="table-layout:fixed;width:960px;min-width:960px;border-collapse:collapse;">
<colgroup>
  <col width="220">
  <col width="210">
  <col width="530">
</colgroup>
<thead>
<tr>
  <th width="220" align="left">Template</th>
  <th width="210" align="center">Deploy</th>
  <th width="530" align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/6215ca5692c0ecfba9186921/hrRM50-6XcdWgg2AKpENG.jpeg" width="20" height="20" alt="Qwen3-0.6B">&nbsp;<a href="endpoint-vllm-qwen3-0-6b/README.md"><strong>Qwen3-0.6B</strong></a></td>
  <td width="210" valign="middle">

[![Create Endpoint](assets/create-endpoint.svg)](https://console.eu.nebius.com/serverless/endpoint/create?image=vllm%2Fvllm-openai%3Alatest&command=python3%20-m%20vllm.entrypoints.openai.api_server%20--model%20Qwen%2FQwen3-0.6B%20--host%200.0.0.0%20--port%208000&targetPort=8000&platform=gpu-l40s-a&preset=1gpu-8vcpu-32gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">Qwen3-0.6B is a compact Apache-2.0 chat LLM served OpenAI-compatibly via vLLM on a single L40S.</td>
</tr>
</tbody>
</table>

## Jobs

### 🏋️ Fine-tuning

<table width="960" border="1" cellpadding="8" cellspacing="0" style="table-layout:fixed;width:960px;min-width:960px;border-collapse:collapse;">
<colgroup>
  <col width="220">
  <col width="210">
  <col width="530">
</colgroup>
<thead>
<tr>
  <th width="220" align="left">Template</th>
  <th width="210" align="center">Deploy</th>
  <th width="530" align="left">Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td width="220" valign="top"><img src="https://cdn-avatars.huggingface.co/v1/production/uploads/6215ca5692c0ecfba9186921/hrRM50-6XcdWgg2AKpENG.jpeg" width="20" height="20" alt="Axolotl">&nbsp;<a href="job-axolotl-finetune/README.md"><strong>Axolotl</strong></a></td>
  <td width="210" valign="middle">

[![Create Job](assets/create-job.svg)](https://console.eu.nebius.com/serverless/job/create?image=docker.io%2Faxolotlai%2Faxolotl%3Amain-20260309-py3.11-cu128-2.9.1&command=curl%20-fsSL%20https%3A%2F%2Fraw.githubusercontent.com%2Fnebius%2Fserverless-ai-cookbook%2Fmain%2Ftraining%2Faxolotl-finetuning%2Fsrc%2Fconfig.yaml%20-o%20%2Fworkspace%2Fdata%2Fconfig.yaml%20%26%26%20export%20RUN_ID%3Drun-%24%28date%20%2B%25Y%25m%25d-%25H%25M%25S%29%20%26%26%20axolotl%20train%20%2Fworkspace%2Fdata%2Fconfig.yaml%20%26%26%20mkdir%20-p%20%2Fworkspace%2Fdata%2Foutput%2F%24RUN_ID%20%26%26%20cp%20-r%20%2Fworkspace%2Foutput%2F.%20%2Fworkspace%2Fdata%2Foutput%2F%24RUN_ID&platform=gpu-h100-sxm&preset=1gpu-16vcpu-200gb&volume=%2Fworkspace%2Fdata&diskSize=500Gi&shmSize=16Gi&preemptible=true)

  </td>
  <td width="530" valign="top">Axolotl finetunes Qwen2.5-0.5B (Apache-2.0) on a preemptible H100 using the cookbook train config.</td>
</tr>
</tbody>
</table>
