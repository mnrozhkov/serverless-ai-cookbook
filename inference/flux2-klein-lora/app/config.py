from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path


DEFAULT_MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
DEFAULT_MODEL_SLUG = "flux2-klein-base-4b-lora"
DEFAULT_LORA_PATH = Path("/opt/flux2/lora/adapter.safetensors")
UNSET_SHA256 = "0" * 64


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean value")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class Settings:
    model_id: str
    model_slug: str
    lora_weights: Path
    lora_sha256: str
    lora_adapter_name: str
    lora_scale: float
    fuse_lora: bool
    default_steps: int
    default_guidance_scale: float
    default_max_sequence_length: int
    device: str
    verify_adapter: bool

    @classmethod
    def from_env(cls) -> "Settings":
        settings = cls(
            model_id=os.getenv("MEDIA_MODEL_ID", DEFAULT_MODEL_ID),
            model_slug=os.getenv("MEDIA_MODEL_SLUG", DEFAULT_MODEL_SLUG),
            lora_weights=Path(
                os.getenv("MEDIA_LORA_WEIGHTS", str(DEFAULT_LORA_PATH))
            ),
            lora_sha256=os.getenv("MEDIA_LORA_SHA256", UNSET_SHA256),
            lora_adapter_name=os.getenv("MEDIA_LORA_ADAPTER_NAME", "adapter"),
            lora_scale=float(os.getenv("MEDIA_LORA_SCALE", "1.0")),
            fuse_lora=_bool_env("MEDIA_FUSE_LORA", True),
            default_steps=int(os.getenv("MEDIA_DEFAULT_STEPS", "20")),
            default_guidance_scale=float(
                os.getenv("MEDIA_DEFAULT_GUIDANCE_SCALE", "3.5")
            ),
            default_max_sequence_length=int(
                os.getenv("MEDIA_DEFAULT_MAX_SEQUENCE_LENGTH", "256")
            ),
            device=os.getenv("MEDIA_DEVICE", "cuda"),
            verify_adapter=_bool_env("MEDIA_VERIFY_ADAPTER", True),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if not self.model_id.strip():
            raise ValueError("MEDIA_MODEL_ID must not be empty")
        if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,127}", self.model_slug):
            raise ValueError("MEDIA_MODEL_SLUG contains unsupported characters")
        if not re.fullmatch(r"[A-Za-z0-9._-]{1,64}", self.lora_adapter_name):
            raise ValueError("MEDIA_LORA_ADAPTER_NAME contains unsupported characters")
        if not re.fullmatch(r"[0-9a-f]{64}", self.lora_sha256):
            raise ValueError("MEDIA_LORA_SHA256 must be 64 lowercase hex characters")
        if not 0 < self.lora_scale <= 4:
            raise ValueError("MEDIA_LORA_SCALE must be greater than 0 and at most 4")
        if not 1 <= self.default_steps <= 100:
            raise ValueError("MEDIA_DEFAULT_STEPS must be between 1 and 100")
        if not 0 <= self.default_guidance_scale <= 20:
            raise ValueError("MEDIA_DEFAULT_GUIDANCE_SCALE must be between 0 and 20")
        if not 1 <= self.default_max_sequence_length <= 512:
            raise ValueError(
                "MEDIA_DEFAULT_MAX_SEQUENCE_LENGTH must be between 1 and 512"
            )
        if self.verify_adapter:
            if self.lora_sha256 == UNSET_SHA256:
                raise ValueError("MEDIA_LORA_SHA256 is not configured")
            self.verify_adapter_identity()

    def verify_adapter_identity(self) -> None:
        if not self.lora_weights.is_file():
            raise ValueError(f"adapter file does not exist: {self.lora_weights}")
        digest = sha256_file(self.lora_weights)
        if digest != self.lora_sha256:
            raise ValueError(
                f"adapter SHA-256 mismatch: expected {self.lora_sha256}, got {digest}"
            )
