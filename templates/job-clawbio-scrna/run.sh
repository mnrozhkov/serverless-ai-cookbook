#!/usr/bin/env bash
# ClawBio scRNA Orchestrator demo. Writes clustering/report artifacts to the
# job volume (or CLAWBIO_OUTPUT_DIR). Prints CLAWBIO_SCRNA_OK on success.
set -euo pipefail

OUT_ROOT="${CLAWBIO_OUTPUT_DIR:-/workspace/data/output}"
RUN_ID="run-$(date +%Y%m%d-%H%M%S)"
OUT="${OUT_ROOT}/${RUN_ID}"
TIMEOUT="${CLAWBIO_RUN_TIMEOUT:-1800}"

mkdir -p "$OUT"
echo "CLAWBIO_SCRNA_OUT=$OUT"

clawbio run scrna --demo --output "$OUT" --timeout "$TIMEOUT"

test -s "$OUT/report.md"
test -s "$OUT/result.json"

echo "CLAWBIO_SCRNA_ARTIFACTS=$(find "$OUT" -type f | wc -l | tr -d ' ') files"
ls -la "$OUT" || true
ls -la "$OUT/figures" 2>/dev/null || true
ls -la "$OUT/tables" 2>/dev/null || true

echo CLAWBIO_SCRNA_OK
