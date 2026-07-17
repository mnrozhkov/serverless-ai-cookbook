#!/usr/bin/env bash
set -Eeuo pipefail

: "${NEBIUS_CLI:=/usr/local/bin/nebius}"
: "${NEBIUS_PROFILE:?NEBIUS_PROFILE is required}"
: "${STATE_DIR:=${XDG_STATE_HOME:-$HOME/.local/state}/flux2-klein-lora}"

confirm=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --confirm) confirm=${2:?missing value}; shift 2 ;;
    *) echo "usage: $0 --confirm ENDPOINT_ID" >&2; exit 2 ;;
  esac
done

[[ -s "$STATE_DIR/endpoint-id" ]] || { echo "STATE_DIR has no endpoint ID" >&2; exit 2; }
endpoint_id=$(tr -d '\n' <"$STATE_DIR/endpoint-id")
[[ "$confirm" == "$endpoint_id" ]] || {
  echo "--confirm must exactly match endpoint ID $endpoint_id" >&2
  exit 2
}

temp=$(mktemp "${TMPDIR:-/tmp}/flux2-klein-lora-delete.XXXXXX")
trap 'rm -f -- "$temp" "$temp.error"' EXIT
"$NEBIUS_CLI" ai endpoint delete \
  --profile "$NEBIUS_PROFILE" \
  --id "$endpoint_id" \
  --format json >"$temp"
jq '{operation_id:(.metadata.id // .id // null),description:(.description // null)}' "$temp"

for _ in $(seq 1 80); do
  if "$NEBIUS_CLI" ai endpoint get \
    --profile "$NEBIUS_PROFILE" \
    --id "$endpoint_id" \
    --format json >/dev/null 2>"$temp.error"; then
    sleep 5
    continue
  fi
  if grep -Eqi 'NotFound|not found' "$temp.error"; then
    rm -f -- "$STATE_DIR/endpoint-id" "$STATE_DIR/endpoint-public.json"
    echo "endpoint deleted and local state removed: $endpoint_id"
    exit 0
  fi
  echo "status check failed for a reason other than NotFound; local state retained" >&2
  exit 1
done
echo "delete was requested but the endpoint still resolves; inspect the operation" >&2
exit 1
