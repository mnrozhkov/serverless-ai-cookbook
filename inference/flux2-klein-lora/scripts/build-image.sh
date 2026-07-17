#!/usr/bin/env bash
set -Eeuo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
root_dir=$(cd -- "$script_dir/.." && pwd)

usage() {
  cat <<'EOF'
usage: build-image.sh --image IMAGE:UNIQUE_TAG --adapter-file PATH \
  --adapter-sha256 SHA256 [--push] [--platform linux/amd64] \
  [--metadata-out PATH]

The adapter is staged in a private temporary directory and passed to BuildKit
as a named context. Push mode refuses latest, digest targets, and existing tags.
EOF
}

image=""
adapter_file=""
adapter_sha256=""
platform="linux/amd64"
metadata_out="$root_dir/build-metadata.json"
push=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --image) image=${2:?missing value}; shift 2 ;;
    --adapter-file) adapter_file=${2:?missing value}; shift 2 ;;
    --adapter-sha256) adapter_sha256=${2:?missing value}; shift 2 ;;
    --platform) platform=${2:?missing value}; shift 2 ;;
    --metadata-out) metadata_out=${2:?missing value}; shift 2 ;;
    --push) push=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -n "$image" && -n "$adapter_file" && -n "$adapter_sha256" ]] || {
  usage >&2
  exit 2
}
[[ -f "$adapter_file" ]] || { echo "adapter is not a regular file" >&2; exit 1; }
[[ "$adapter_sha256" =~ ^[0-9a-f]{64}$ ]] || {
  echo "--adapter-sha256 must be 64 lowercase hex characters" >&2
  exit 2
}
[[ "$adapter_sha256" != "0000000000000000000000000000000000000000000000000000000000000000" ]] || {
  echo "the all-zero adapter digest is not valid" >&2
  exit 2
}
[[ "$image" != *@* ]] || { echo "build to a unique tag, not a digest target" >&2; exit 2; }
[[ "$image" =~ ^[^[:space:]@]+:[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$ ]] || {
  echo "image must include an explicit valid tag" >&2
  exit 2
}
[[ "${image##*:}" != "latest" ]] || { echo "the latest tag is forbidden" >&2; exit 2; }

for command in docker jq sha256sum; do
  command -v "$command" >/dev/null || { echo "missing command: $command" >&2; exit 1; }
done

umask 077
temp_dir=$(mktemp -d "${TMPDIR:-/tmp}/flux2-klein-lora-build.XXXXXX")
cleanup() {
  rm -rf -- "$temp_dir"
}
trap cleanup EXIT

staged_adapter="$temp_dir/adapter.safetensors"
install -m 0600 -- "$adapter_file" "$staged_adapter"
actual_sha256=$(sha256sum -- "$staged_adapter" | awk '{print $1}')
[[ "$actual_sha256" == "$adapter_sha256" ]] || {
  echo "adapter SHA-256 does not match the expected training artifact" >&2
  exit 1
}

if $push; then
  command -v crane >/dev/null || { echo "push mode requires crane" >&2; exit 1; }
  lookup_error="$temp_dir/lookup-error"
  if crane digest "$image" >/dev/null 2>"$lookup_error"; then
    echo "refusing to overwrite existing registry tag: $image" >&2
    exit 1
  fi
  if ! grep -Eqi 'manifest unknown|name unknown|not found|404' "$lookup_error"; then
    echo "cannot prove the target tag is unused; check registry access" >&2
    exit 1
  fi
fi

build_metadata="$temp_dir/build-metadata.json"
build_args=(
  build
  --platform "$platform"
  --build-context "adapter=$temp_dir"
  --build-arg "LORA_SHA256=$adapter_sha256"
  --metadata-file "$build_metadata"
  --provenance=false
  --tag "$image"
)
if $push; then
  build_args+=(--push)
else
  build_args+=(--load)
fi
build_args+=("$root_dir")

docker buildx "${build_args[@]}"

digest=$(jq -r '.["containerimage.digest"] // empty' "$build_metadata")
jq -n \
  --arg image "$image" \
  --arg digest "$digest" \
  --arg platform "$platform" \
  --arg adapter_sha256 "$adapter_sha256" \
  --argjson pushed "$push" \
  '{image:$image,digest:$digest,platform:$platform,pushed:$pushed,adapter_sha256:$adapter_sha256}' \
  >"$metadata_out"
chmod 0644 "$metadata_out"
jq . "$metadata_out"
