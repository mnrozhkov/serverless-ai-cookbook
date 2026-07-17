from __future__ import annotations

import time
from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from starlette.concurrency import run_in_threadpool

from .config import Settings
from .runtime import ModelRuntime


class InferenceRequest(BaseModel):
    prompt: Annotated[str, Field(min_length=1, max_length=4096)]
    width: int = Field(default=1024, ge=256, le=2048)
    height: int = Field(default=1024, ge=256, le=2048)
    num_inference_steps: int | None = Field(default=None, ge=1, le=100)
    guidance_scale: float | None = Field(default=None, ge=0, le=20)
    max_sequence_length: int | None = Field(default=None, ge=1, le=512)
    seed: int = Field(default=42, ge=0, le=9_223_372_036_854_775_807)

    @field_validator("width", "height")
    @classmethod
    def dimensions_are_multiples_of_16(cls, value: int) -> int:
        if value % 16:
            raise ValueError("image dimensions must be multiples of 16")
        return value


def create_app(
    settings: Settings | None = None,
    runtime: ModelRuntime | None = None,
) -> FastAPI:
    configured = settings or Settings.from_env()
    model_runtime = runtime or ModelRuntime(configured)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        await run_in_threadpool(model_runtime.load)
        yield

    application = FastAPI(
        title="FLUX.2 Klein base 4B LoRA",
        version="1.0.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan,
    )

    @application.get("/v1/health/live")
    async def live() -> dict[str, bool]:
        return {"live": True}

    @application.get("/v1/health/ready")
    async def ready() -> dict[str, Any]:
        if not model_runtime.ready:
            raise HTTPException(status_code=503, detail="model is not ready")
        return {
            "ready": True,
            "slug": configured.model_slug,
            "kind": "image_diffusers",
            "model_id": configured.model_id,
            "device": configured.device,
            "lora_adapter_name": configured.lora_adapter_name,
            "lora_fused": configured.fuse_lora,
            "lora_scale": configured.lora_scale,
        }

    @application.post("/v1/inference/{model_slug}")
    async def infer(model_slug: str, request: InferenceRequest) -> dict[str, Any]:
        if model_slug != configured.model_slug:
            raise HTTPException(status_code=404, detail="unknown model slug")
        if not model_runtime.ready:
            raise HTTPException(status_code=503, detail="model is not ready")

        image_b64, model_time_ms = await run_in_threadpool(
            model_runtime.generate,
            prompt=request.prompt,
            width=request.width,
            height=request.height,
            num_inference_steps=(
                request.num_inference_steps or configured.default_steps
            ),
            guidance_scale=(
                request.guidance_scale
                if request.guidance_scale is not None
                else configured.default_guidance_scale
            ),
            max_sequence_length=(
                request.max_sequence_length
                or configured.default_max_sequence_length
            ),
            seed=request.seed,
        )
        return {
            "created": int(time.time()),
            "data": [{"b64_json": image_b64}],
            "metrics": {"model_time_ms": round(model_time_ms, 3)},
        }

    return application


app = create_app()
