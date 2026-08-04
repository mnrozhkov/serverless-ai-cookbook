from __future__ import annotations

import base64
import io
import threading
import time
from typing import Any

from .config import Settings


class ModelRuntime:
    """Own one FLUX pipeline and serialize requests to a single GPU."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.pipeline: Any | None = None
        self._lock = threading.Lock()

    @property
    def ready(self) -> bool:
        return self.pipeline is not None

    def load(self) -> None:
        import torch
        from diffusers import Flux2KleinPipeline

        if self.settings.device == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but torch.cuda.is_available() is false")

        pipeline = Flux2KleinPipeline.from_pretrained(
            self.settings.model_id,
            torch_dtype=torch.bfloat16,
        )
        pipeline.load_lora_weights(
            str(self.settings.lora_weights.parent),
            weight_name=self.settings.lora_weights.name,
            adapter_name=self.settings.lora_adapter_name,
        )
        if self.settings.fuse_lora:
            pipeline.fuse_lora(
                components=["transformer"],
                lora_scale=self.settings.lora_scale,
                adapter_names=[self.settings.lora_adapter_name],
                safe_fusing=True,
            )
        pipeline.to(self.settings.device)
        pipeline.set_progress_bar_config(disable=True)
        self.pipeline = pipeline

    def generate(
        self,
        *,
        prompt: str,
        width: int,
        height: int,
        num_inference_steps: int,
        guidance_scale: float,
        max_sequence_length: int,
        seed: int,
    ) -> tuple[str, float]:
        if self.pipeline is None:
            raise RuntimeError("model is not ready")

        import torch

        generator = torch.Generator(device=self.settings.device).manual_seed(seed)
        start = time.perf_counter()
        with self._lock, torch.inference_mode():
            output = self.pipeline(
                prompt=prompt,
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                max_sequence_length=max_sequence_length,
                generator=generator,
            )
        elapsed_ms = (time.perf_counter() - start) * 1000
        image = output.images[0]
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("ascii"), elapsed_ms
