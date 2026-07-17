# syntax=docker/dockerfile:1.7
FROM docker.io/pytorch/pytorch:2.11.0-cuda12.8-cudnn9-runtime@sha256:eee11b3b3872a8c838e35ef48f08b2d5def2080902c7f666831310ca1a0ef2be AS runtime

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG LORA_SHA256=0000000000000000000000000000000000000000000000000000000000000000

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_BREAK_SYSTEM_PACKAGES=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/cache/huggingface \
    HF_HUB_CACHE=/cache/huggingface/hub \
    TRANSFORMERS_CACHE=/cache/huggingface/transformers \
    DIFFUSERS_CACHE=/cache/huggingface/diffusers \
    TORCH_HOME=/cache/torch \
    MEDIA_MODEL_ID=black-forest-labs/FLUX.2-klein-base-4B \
    MEDIA_MODEL_SLUG=flux2-klein-base-4b-lora \
    MEDIA_DEFAULT_STEPS=20 \
    MEDIA_DEFAULT_GUIDANCE_SCALE=3.5 \
    MEDIA_DEFAULT_MAX_SEQUENCE_LENGTH=256 \
    MEDIA_LORA_WEIGHTS=/opt/flux2/lora/adapter.safetensors \
    MEDIA_LORA_SHA256=$LORA_SHA256 \
    MEDIA_LORA_ADAPTER_NAME=adapter \
    MEDIA_LORA_SCALE=1.0 \
    MEDIA_FUSE_LORA=1 \
    MEDIA_VERIFY_ADAPTER=1 \
    MEDIA_DEVICE=cuda \
    PORT=8000

WORKDIR /opt/flux2/service

COPY requirements.lock.txt ./requirements.lock.txt
RUN python -m pip install --no-cache-dir --require-hashes --requirement requirements.lock.txt

COPY app ./app
COPY entrypoint.sh ./entrypoint.sh

RUN chmod 0555 ./entrypoint.sh \
    && mkdir -p /opt/flux2/lora /cache/huggingface /cache/torch \
    && chown -R 10001:10001 /opt/flux2 /cache

FROM runtime AS final

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG LORA_SHA256
ENV MEDIA_LORA_SHA256=$LORA_SHA256

# The adapter is supplied as a temporary BuildKit named context by
# scripts/build-image.sh. It is never copied into the Git build context.
# hadolint ignore=DL3022
COPY --from=adapter /adapter.safetensors /opt/flux2/lora/adapter.safetensors

RUN [[ "$LORA_SHA256" =~ ^[0-9a-f]{64}$ ]] \
    && [[ "$LORA_SHA256" != "0000000000000000000000000000000000000000000000000000000000000000" ]] \
    && echo "$LORA_SHA256  /opt/flux2/lora/adapter.safetensors" | sha256sum --check --strict \
    && chown 10001:10001 /opt/flux2/lora/adapter.safetensors

USER 10001:10001

EXPOSE 8000
ENTRYPOINT ["/opt/flux2/service/entrypoint.sh"]
