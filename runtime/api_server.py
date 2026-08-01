from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from runtime.license_loader import LicenseInfo
from runtime.module_loader import Capsule, RESERVED_MODULES


class StanAIQuery(BaseModel):
    query: str
    context: dict[str, Any] = {}


@dataclass(frozen=True)
class RuntimeContext:
    version: str
    offline_mode: bool
    license: LicenseInfo
    capsules: list[Capsule]


def create_app(context: RuntimeContext) -> FastAPI:
    app = FastAPI(title="NWD-EWOS Runtime", version=context.version)

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "runtime": "NWD-EWOS",
            "version": context.version,
            "offline_mode": context.offline_mode,
        }

    @app.get("/runtime/status")
    def runtime_status() -> dict[str, Any]:
        return {
            "runtime": "NWD-EWOS",
            "version": context.version,
            "offline_mode": context.offline_mode,
            "license": {
                "valid": context.license.valid,
                "edition": context.license.edition,
                "licensee": context.license.licensee,
                "warnings": context.license.warnings,
            },
            "loaded_capsules": len(context.capsules),
        }

    @app.get("/modules")
    def modules() -> dict[str, Any]:
        loaded = [
            {
                "id": capsule.id,
                "name": capsule.name,
                "version": capsule.version,
                "type": capsule.type,
                "capabilities": capsule.capabilities,
                "enabled": True,
            }
            for capsule in context.capsules
        ]
        return {
            "loaded": loaded,
            "reserved": RESERVED_MODULES,
        }

    @app.post("/stanai/query")
    def stanai_query(payload: StanAIQuery) -> dict[str, Any]:
        return {
            "module": "stanai",
            "status": "placeholder",
            "query": payload.query,
            "context_received": bool(payload.context),
            "response": (
                "StanAI Berlin Demo placeholder response. "
                "Real local reasoning is reserved for a future task."
            ),
            "architecture_boundary": {
                "owns_enterprise_data": False,
                "direct_database_access": False,
                "role": "leadership_orchestrator",
            },
        }

    return app


def serialize_context(context: RuntimeContext) -> dict[str, Any]:
    return {
        "version": context.version,
        "offline_mode": context.offline_mode,
        "license": asdict(context.license),
        "capsules": [asdict(capsule) for capsule in context.capsules],
    }
