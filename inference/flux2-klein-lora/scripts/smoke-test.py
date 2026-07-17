#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import stat
import struct
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"


def read_token(path: Path) -> str:
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        raise ValueError("token file must not be readable by group or others")
    token = path.read_text().strip()
    if not token:
        raise ValueError("token file is empty")
    return token


def request_json(
    url: str,
    *,
    token: str,
    payload: dict[str, Any] | None,
    timeout: int,
) -> tuple[dict[str, Any], float]:
    headers = {"Accept": "application/json", "Authorization": f"Bearer {token}"}
    body = None
    method = "GET"
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(payload).encode()
        method = "POST"
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        parsed = json.loads(response.read())
    return parsed, time.perf_counter() - started


def wait_for_ready(
    base_url: str,
    *,
    token: str,
    wait_seconds: int,
    request_timeout: int,
) -> tuple[dict[str, Any], float]:
    deadline = time.monotonic() + wait_seconds
    last_error = "not attempted"
    while time.monotonic() < deadline:
        try:
            health, latency = request_json(
                f"{base_url}/v1/health/ready",
                token=token,
                payload=None,
                timeout=request_timeout,
            )
            if health.get("ready") is True:
                return health, latency
            last_error = "readiness response did not contain ready=true"
        except urllib.error.HTTPError as error:
            if error.code in {401, 403}:
                raise RuntimeError(
                    f"readiness authentication failed with HTTP {error.code}"
                ) from error
            last_error = f"HTTP {error.code}"
        except (OSError, ValueError) as error:
            last_error = type(error).__name__
        time.sleep(10)
    raise TimeoutError(f"readiness did not pass: {last_error}")


def png_dimensions(png: bytes) -> tuple[int, int]:
    if len(png) < 24 or png[:8] != b"\x89PNG\r\n\x1a\n" or png[12:16] != b"IHDR":
        raise ValueError("response payload is not a PNG")
    return struct.unpack(">II", png[16:24])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--token-file", required=True, type=Path)
    parser.add_argument("--model-slug", default="flux2-klein-base-4b-lora")
    parser.add_argument("--adapter-name", default="adapter")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--wait-seconds", type=int, default=3600)
    parser.add_argument("--request-timeout", type=int, default=900)
    args = parser.parse_args()

    token = read_token(args.token_file)
    base_url = args.base_url.rstrip("/")
    args.output_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(args.output_dir, 0o700)

    health, health_latency = wait_for_ready(
        base_url,
        token=token,
        wait_seconds=args.wait_seconds,
        request_timeout=args.request_timeout,
    )
    if health.get("model_id") != DEFAULT_MODEL_ID:
        raise RuntimeError(f"unexpected model_id: {health.get('model_id')}")
    if health.get("slug") != args.model_slug:
        raise RuntimeError(f"unexpected model slug: {health.get('slug')}")
    if health.get("lora_adapter_name") != args.adapter_name:
        raise RuntimeError("readiness reported an unexpected LoRA adapter")
    if health.get("lora_fused") is not True:
        raise RuntimeError("readiness did not report a fused LoRA")

    payload = {
        "prompt": args.prompt,
        "width": 1024,
        "height": 1024,
        "num_inference_steps": 20,
        "guidance_scale": 3.5,
        "max_sequence_length": 256,
        "seed": 42,
    }
    response, inference_latency = request_json(
        f"{base_url}/v1/inference/{args.model_slug}",
        token=token,
        payload=payload,
        timeout=args.request_timeout,
    )
    try:
        png = base64.b64decode(response["data"][0]["b64_json"], validate=True)
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise RuntimeError("response did not contain valid data[0].b64_json") from error
    width, height = png_dimensions(png)
    if (width, height) != (1024, 1024):
        raise RuntimeError(f"unexpected image dimensions: {width}x{height}")

    summary = {
        "health_latency_seconds": round(health_latency, 6),
        "inference_latency_seconds": round(inference_latency, 6),
        "model_time_ms": (response.get("metrics") or {}).get("model_time_ms"),
        "payload": payload,
        "png_sha256": hashlib.sha256(png).hexdigest(),
        "png_bytes": len(png),
        "image": {"width": width, "height": height},
    }
    outputs = {
        "health.json": json.dumps(health, indent=2) + "\n",
        "payload.json": json.dumps(payload, indent=2) + "\n",
        "inference-summary.json": json.dumps(summary, indent=2) + "\n",
    }
    for filename, content in outputs.items():
        path = args.output_dir / filename
        path.write_text(content)
        path.chmod(0o600)
    image_path = args.output_dir / "output.png"
    image_path.write_bytes(png)
    image_path.chmod(0o600)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
