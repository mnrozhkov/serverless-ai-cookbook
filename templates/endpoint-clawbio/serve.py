"""ClawBio MCP over Streamable HTTP for Nebius serverless endpoints.

Exposes upstream ClawBio tools plus GET /health and POST /demo/pharmgx.

Runtime env (console or image defaults):
  MCP_DEMO_ONLY       — restrict MCP to bundled demo data (default true)
  CLAWBIO_INPUT_DIR   — optional read-only input root when demo-only is off
  CLAWBIO_OUTPUT_DIR  — optional default output root when demo-only is off
  NEBIUS_API_KEY      — Token Factory key; copied to LLM_API_KEY for ClawBio LLM clients
  LLM_BASE_URL        — Token Factory OpenAI base URL
  CLAWBIO_MODEL       — model id for in-container LLM clients
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from clawbio.mcp_server import describe_skill, list_skills, run_skill
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
DEFAULT_LLM_BASE_URL = "https://api.tokenfactory.nebius.com/v1/"
DEFAULT_MODEL = "meta-llama/Meta-Llama-3.1-8B-Instruct"


def _truthy(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes"}


def apply_runtime_env() -> None:
    """Normalize console/image env before MCP tools start."""
    key = os.environ.get("NEBIUS_API_KEY", "").strip()
    if key and not os.environ.get("LLM_API_KEY"):
        os.environ["LLM_API_KEY"] = key
    os.environ.setdefault("LLM_BASE_URL", DEFAULT_LLM_BASE_URL)
    os.environ.setdefault("CLAWBIO_MODEL", DEFAULT_MODEL)
    if _truthy("MCP_DEMO_ONLY", "true"):
        os.environ.pop("CLAWBIO_MCP_ALLOW_LOCAL_FILES", None)
    else:
        os.environ["CLAWBIO_MCP_ALLOW_LOCAL_FILES"] = "1"


def demo_only() -> bool:
    return _truthy("MCP_DEMO_ONLY", "true")


def _run_skill(
    skill: str,
    *,
    demo: bool = False,
    input_path: str | None = None,
    output_dir: str | None = None,
    extra_args: list[str] | None = None,
) -> dict[str, Any]:
    if demo_only():
        return run_skill(skill, demo=True, extra_args=extra_args)
    out = output_dir or os.environ.get("CLAWBIO_OUTPUT_DIR") or None
    inp = input_path
    root = os.environ.get("CLAWBIO_INPUT_DIR", "").strip()
    if inp and root:
        path = Path(inp)
        if not path.is_absolute():
            inp = str(Path(root) / path)
    return run_skill(
        skill,
        demo=demo,
        input_path=inp,
        output_dir=out,
        extra_args=extra_args,
    )


def enabled_skills() -> list[dict[str, Any]]:
    """Runnable catalog entries (compact) for /health and /skills."""
    return list_skills("")


def _summary_from_result(result: dict[str, Any]) -> dict[str, Any] | None:
    output_dir = result.get("output_dir")
    if not output_dir:
        return None
    summary_path = Path(str(output_dir)) / "summary.json"
    if not summary_path.is_file():
        return None
    return json.loads(summary_path.read_text(encoding="utf-8"))


def create_mcp() -> FastMCP:
    apply_runtime_env()
    app = FastMCP(
        "clawbio",
        host=HOST,
        port=PORT,
        streamable_http_path="/mcp",
        sse_path="/sse",
    )

    @app.tool()
    def clawbio_list_skills(query: str = "") -> list[dict[str, Any]]:
        """Search the ClawBio bioinformatics skill library. Empty query lists everything."""
        return list_skills(query)

    @app.tool()
    def clawbio_describe_skill(name: str) -> dict[str, Any]:
        """Read a ClawBio skill SKILL.md contract: inputs, outputs, safety rules."""
        return describe_skill(name)

    @app.tool()
    def clawbio_run_skill(
        skill: str,
        demo: bool = False,
        input_path: str | None = None,
        output_dir: str | None = None,
        extra_args: list[str] | None = None,
    ) -> dict[str, Any]:
        """Run a ClawBio skill. Demo data always works when MCP_DEMO_ONLY is true."""
        return _run_skill(
            skill,
            demo=demo,
            input_path=input_path,
            output_dir=output_dir,
            extra_args=extra_args,
        )

    @app.custom_route("/health", methods=["GET"])
    async def health(_: Request) -> JSONResponse:
        skills = enabled_skills()
        return JSONResponse(
            {
                "status": "ok",
                "service": "clawbio-mcp",
                "mcp": "/mcp",
                "skills_enabled": len(skills),
                "skills": [
                    {
                        "name": s.get("name"),
                        "cli_alias": s.get("cli_alias"),
                        "runnable": s.get("runnable"),
                    }
                    for s in skills
                ],
                "demo_only": demo_only(),
                "llm_base_url": os.environ.get("LLM_BASE_URL") or None,
                "model": os.environ.get("CLAWBIO_MODEL") or None,
                "has_api_key": bool(
                    os.environ.get("NEBIUS_API_KEY") or os.environ.get("LLM_API_KEY")
                ),
                "input_dir": os.environ.get("CLAWBIO_INPUT_DIR") or None,
                "output_dir": os.environ.get("CLAWBIO_OUTPUT_DIR") or None,
            }
        )

    @app.custom_route("/skills", methods=["GET"])
    async def skills_index(_: Request) -> JSONResponse:
        return JSONResponse({"skills": enabled_skills()})

    @app.custom_route("/demo/pharmgx", methods=["POST"])
    async def demo_pharmgx(_: Request) -> Response:
        result = _run_skill("pharmgx", demo=True)
        summary = _summary_from_result(result)
        payload = {
            "success": bool(result.get("success")),
            "skill": result.get("skill", "pharmgx"),
            "output_dir": result.get("output_dir"),
            "files": result.get("files") or [],
            "summary": summary,
        }
        if not result.get("success"):
            payload["stderr"] = result.get("stderr", "")
            return JSONResponse(payload, status_code=500)
        if not summary:
            return JSONResponse(
                {"error": "PharmGx demo finished but summary.json is missing", **payload},
                status_code=500,
            )
        return JSONResponse(payload)

    return app


def main() -> None:
    create_mcp().run(transport="streamable-http")


if __name__ == "__main__":
    main()
