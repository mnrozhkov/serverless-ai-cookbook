# ClawBio scRNA Orchestrator job. Pinned package — rebuild on CLAWBIO_VERSION bump.
# Built for linux/amd64 (Nebius serverless).
FROM python:3.12-slim-bookworm

ARG CLAWBIO_VERSION=0.6.1

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      git \
      libgomp1 \
      libglpk40 \
      libxml2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
      "clawbio==${CLAWBIO_VERSION}" \
      "scanpy==1.11.4" \
      "anndata==0.11.4" \
      "leidenalg==0.10.2" \
      "igraph==0.11.8"

WORKDIR /app
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

CMD ["bash", "/app/run.sh"]
