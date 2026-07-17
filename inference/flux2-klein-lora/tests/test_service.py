import base64
import hashlib
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("MEDIA_VERIFY_ADAPTER", "0")

from app.config import DEFAULT_MODEL_ID, DEFAULT_MODEL_SLUG, Settings
from app.main import create_app


def settings() -> Settings:
    value = Settings(
        model_id=DEFAULT_MODEL_ID,
        model_slug=DEFAULT_MODEL_SLUG,
        lora_weights=Path("/not-used/adapter.safetensors"),
        lora_sha256="a" * 64,
        lora_adapter_name="adapter",
        lora_scale=1.0,
        fuse_lora=True,
        default_steps=20,
        default_guidance_scale=3.5,
        default_max_sequence_length=256,
        device="cuda",
        verify_adapter=False,
    )
    value.validate()
    return value


class FakeRuntime:
    ready = False
    request = None

    def load(self):
        self.ready = True

    def generate(self, **kwargs):
        self.request = kwargs
        return base64.b64encode(b"fake-png").decode("ascii"), 123.456


def test_health_and_standard_inference_contract():
    runtime = FakeRuntime()
    with TestClient(create_app(settings(), runtime)) as client:
        health = client.get("/v1/health/ready")
        assert health.status_code == 200
        assert health.json() == {
            "ready": True,
            "slug": DEFAULT_MODEL_SLUG,
            "kind": "image_diffusers",
            "model_id": DEFAULT_MODEL_ID,
            "device": "cuda",
            "lora_adapter_name": "adapter",
            "lora_fused": True,
            "lora_scale": 1.0,
        }

        response = client.post(
            f"/v1/inference/{DEFAULT_MODEL_SLUG}",
            json={"prompt": "adapter, a Golden Retriever", "seed": 42},
        )
        assert response.status_code == 200
        assert base64.b64decode(response.json()["data"][0]["b64_json"]) == b"fake-png"
        assert runtime.request["num_inference_steps"] == 20
        assert runtime.request["guidance_scale"] == 3.5
        assert runtime.request["max_sequence_length"] == 256
        assert runtime.request["seed"] == 42


@pytest.mark.parametrize("dimension", [255, 257, 1023, 2049])
def test_rejects_invalid_dimensions(dimension):
    with TestClient(create_app(settings(), FakeRuntime())) as client:
        response = client.post(
            f"/v1/inference/{DEFAULT_MODEL_SLUG}",
            json={"prompt": "dog", "width": dimension},
        )
        assert response.status_code == 422


def test_wrong_slug_is_not_routed():
    with TestClient(create_app(settings(), FakeRuntime())) as client:
        response = client.post("/v1/inference/wrong-model", json={"prompt": "dog"})
        assert response.status_code == 404


def test_adapter_verification_uses_configured_digest(tmp_path):
    adapter = tmp_path / "adapter.safetensors"
    adapter.write_bytes(b"adapter-fixture")
    digest = hashlib.sha256(adapter.read_bytes()).hexdigest()
    value = Settings(
        **{
            **settings().__dict__,
            "lora_weights": adapter,
            "lora_sha256": digest,
            "verify_adapter": True,
        }
    )
    value.validate()

    wrong = Settings(**{**value.__dict__, "lora_sha256": "b" * 64})
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        wrong.validate()
