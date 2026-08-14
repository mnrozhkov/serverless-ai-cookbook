# ClawBio

<!-- factory:deploy -->
[![Create Endpoint](../assets/create-endpoint.svg)](https://console.nebius.com/serverless/endpoint/create?image=docker.io%2Fmnrozhkov%2Fclawbio-serve%3A99040b2&targetPort=8000&platform=cpu-d3&preset=8vcpu-32gb&diskSize=500Gi)
<!-- /factory:deploy -->

<!-- factory:intro -->
ClawBio is a bioinformatics skill library exposed as a remote MCP server on CPU. Connect Cursor or Claude Desktop, use Nebius Token Factory for agent reasoning, and run the PharmGx pharmacogenomics demo in minutes.

**License:** [MIT](https://github.com/ClawBio/ClawBio/blob/main/LICENSE) · **Source:** [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio)
<!-- /factory:intro -->

## Test request

1. Click **Create Endpoint**. Keep the pre-filled image, CPU preset, and disk. Do **not** add env vars for this smoke — demo data and MCP defaults are in the image.
2. Wait until the endpoint is **READY**, then copy the public URL (`BASE_URL`). Authentication is off so you can call it without a bearer token.

**First boot:** Nebius can show RUNNING while ClawBio installs skill dependencies. `GET /health` may return `502 failed to connect to local service` until port 8000 binds. Wait for `/health` JSON before the PharmGx demo.

### curl

```bash
export BASE_URL='https://…'   # Public endpoints URL from the console

curl -sS "$BASE_URL/health"
# {"status":"ok","skills_enabled":8,…}

curl -sS "$BASE_URL/skills"

curl -sS -X POST "$BASE_URL/demo/pharmgx" \
  -H "Content-Type: application/json" \
  -d '{}' | tee pharmgx-demo.json

python3 - <<'PY'
import json
data = json.load(open("pharmgx-demo.json"))
summary = data.get("summary") or {}
print("summary keys:", sorted(summary.keys()))
assert summary, "expected non-empty summary.json from PharmGx demo"
PY
```

### Python

```python
import json
import os
import time
import urllib.request

base = os.environ["BASE_URL"].rstrip("/")

for _ in range(40):
    try:
        with urllib.request.urlopen(f"{base}/health", timeout=30) as resp:
            if resp.status == 200:
                break
    except OSError:
        pass
    print("waiting for /health…")
    time.sleep(15)
else:
    raise SystemExit("timed out waiting for /health")

req = urllib.request.Request(
    f"{base}/demo/pharmgx",
    data=b"{}",
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=600) as resp:
    payload = json.loads(resp.read())
summary = payload.get("summary") or {}
print(json.dumps(summary, indent=2)[:2000])
assert summary, "expected PharmGx summary.json"
```

### MCP client (Cursor)

Project `.cursor/mcp.json` (Streamable HTTP):

```json
{
  "mcpServers": {
    "clawbio": {
      "url": "https://<BASE_URL>/mcp",
      "transport": "streamable-http"
    }
  }
}
```

Restart Cursor, then try: *“List ClawBio skills and run the PharmGx demo.”*

> ⚠️ **Delete the endpoint after testing** to avoid ongoing charges.
> [How to delete an endpoint](https://docs.nebius.com/serverless/endpoints/manage#how-to-delete-an-endpoint)

<!-- factory:cli -->
## CLI alternative

```bash
nebius ai endpoint create \
  --image docker.io/mnrozhkov/clawbio-serve:99040b2 \
  --public \
  --platform cpu-d3 \
  --preset 8vcpu-32gb \
  --container-port 8000 \
  --disk-size 500Gi
```
<!-- /factory:cli -->

## Troubleshooting

- **502 on first request** — wait for `/health` JSON; cold start can take several minutes on CPU.
- **PharmGx demo fails** — check endpoint logs for missing Python deps; rebuild the image after a `CLAWBIO_VERSION` bump in the Dockerfile.
- **MCP client shows no tools** — confirm the URL ends with `/mcp` and transport is `streamable-http`.
- **Token Factory 401** — that is a Cursor/client or in-container LLM call. `/health` and `/demo/pharmgx` do not use the key.
- **Wrong platform** — this template uses `cpu-d3` / `8vcpu-32gb` (no `--preemptible`).

## Optional configuration

Skip this section for the PharmGx smoke. The Create Endpoint button does not carry env vars; add them in the console only if you need the overrides below.

**MCP tools run inside the container and do not call Token Factory.** Set `NEBIUS_API_KEY` on the endpoint only if ClawBio inside the container should call Token Factory. Cursor / Claude Desktop use Token Factory on the **client**.

> **Research / educational use only.** ClawBio is not a medical device. Demo data is synthetic. Do not upload real patient genotypes without appropriate safeguards.

| Variable | Default (image) | When to set |
| --- | --- | --- |
| `MCP_DEMO_ONLY` | `true` | `false` to allow local files instead of bundled `--demo` data |
| `NEBIUS_API_KEY` | unset | Secret; copied to `LLM_API_KEY` for in-container LLM clients |
| `LLM_BASE_URL` | `https://api.tokenfactory.nebius.com/v1/` | Override Token Factory base URL |
| `CLAWBIO_MODEL` | `meta-llama/Meta-Llama-3.1-8B-Instruct` | Override in-container model id |
| `CLAWBIO_INPUT_DIR` | unset | e.g. `/mnt/ref` after a volume mount (`MCP_DEMO_ONLY=false`) |
| `CLAWBIO_OUTPUT_DIR` | unset | e.g. `/workspace/data/output` when writing non-demo outputs |

For GPU batch Scanpy, use [`job-clawbio-scrna`](../job-clawbio-scrna/README.md).

## Build the image yourself

```bash
cd templates/endpoint-clawbio
docker build -t <your-registry>/clawbio-serve:1 .
docker push <your-registry>/clawbio-serve:1
```
