# ClawBio scRNA

<!-- factory:deploy -->
[![Create Job](../assets/create-job.svg)](https://console.nebius.com/serverless/job/create?image=docker.io%2Fmnrozhkov%2Fclawbio-scrna%3Ade9ae05&command=%2Fapp%2Frun.sh&platform=gpu-l40s-a&preset=1gpu-8vcpu-32gb&diskSize=500Gi&shmSize=16Gi&timeout=1&preemptible=true&public=false)
<!-- /factory:deploy -->

<!-- factory:intro -->
ClawBio scRNA Orchestrator runs a Scanpy QC/clustering demo on a preemptible GPU job and writes report.md plus figures to the mounted volume.

**License:** [MIT](https://github.com/ClawBio/ClawBio/blob/main/LICENSE) · **Source:** [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio)
<!-- /factory:intro -->

## Test request

1. Click **Create Job**. Keep the pre-filled image, L40S preset, disk, shm, timeout, and command (`/app/run.sh`). Do **not** add env vars — `--demo` uses bundled PBMC3k (synthetic fallback) and needs no Token Factory key.
2. Wait until the job is **COMPLETED** (Scanpy can take several minutes after the image pull).

### Check results

In logs, look for `CLAWBIO_SCRNA_OK`:

```bash
nebius ai job logs <job-id>
```

Artifacts land on the job disk under:

`/workspace/data/output/run-YYYYMMDD-HHMMSS/`

| File | What it is |
| --- | --- |
| `report.md` | QC, clustering, marker summary |
| `result.json` | Machine-readable metrics |
| `figures/` | UMAP / QC plots |
| `tables/` | Cluster and marker tables |

Open those paths from the job’s files view in the console, or copy them off the volume after the run.

> ⚠️ When you are done testing, **delete the job** so it stops billing — see
> [How to delete a job](https://docs.nebius.com/serverless/jobs/manage#how-to-delete-a-job).

<!-- factory:cli -->
## CLI alternative

```bash
nebius ai job create \
  --image docker.io/mnrozhkov/clawbio-scrna:de9ae05 \
  --platform gpu-l40s-a \
  --preset 1gpu-8vcpu-32gb \
  --preemptible \
  --shm-size 16Gi \
  --disk-size 500Gi \
  --timeout 1h \
  --command '/app/run.sh'
```
<!-- /factory:cli -->

## Troubleshooting

- **Job still RUNNING** — wait for `CLAWBIO_SCRNA_OK`; first boot also pulls the image.
- **Missing `report.md`** — the job failed before the marker. Inspect logs for Scanpy / Leiden / download errors.
- **OOM / NER** — confirm `gpu-l40s-a` / `1gpu-8vcpu-32gb` and `shm_size` 16 Gi. Try fallback `1gpu-24vcpu-96gb`.
- **Want MCP tools instead** — deploy [`endpoint-clawbio`](../endpoint-clawbio/README.md) on CPU.

## Optional configuration

Skip this section for `--demo`. The Create Job button does not carry env vars.

> **Research / educational use only.** ClawBio is not a medical device. Demo data is public/synthetic. Do not process real patient genotypes without appropriate safeguards.

| Variable | Default | When to set |
| --- | --- | --- |
| `CLAWBIO_OUTPUT_DIR` | `/workspace/data/output` | Different writable root |
| `CLAWBIO_INPUT_DIR` | unset | Own `.h5ad` / 10x directory after a volume mount (not `--demo`) |
| `CLAWBIO_RUN_TIMEOUT` | `1800` | Seconds passed to `clawbio run --timeout` |

Non-demo input: mount your data, set `CLAWBIO_INPUT_DIR`, and change the container command to `clawbio run scrna --input … --output …` (see [scRNA Orchestrator](https://docs.clawbio.ai/skills/scrna-orchestrator/)).

## Build the image yourself

```bash
cd templates/job-clawbio-scrna
docker build -t <your-registry>/clawbio-scrna:1 .
docker push <your-registry>/clawbio-scrna:1
```
