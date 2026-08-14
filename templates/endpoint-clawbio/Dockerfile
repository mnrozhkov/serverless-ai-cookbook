# ClawBio MCP HTTP server. Pinned package — rebuild on CLAWBIO_VERSION bump.
FROM python:3.12-slim-bookworm

ARG CLAWBIO_VERSION=0.6.1

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    MCP_DEMO_ONLY=true \
    LLM_BASE_URL=https://api.tokenfactory.nebius.com/v1/ \
    CLAWBIO_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
      "clawbio[mcp]==${CLAWBIO_VERSION}" \
      uvicorn==0.34.0

WORKDIR /app
COPY serve.py /app/serve.py

EXPOSE 8000
CMD ["python", "serve.py"]
