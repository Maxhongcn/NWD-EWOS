from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Capsule:
    id: str
    name: str
    version: str
    type: str
    capabilities: list[str]
    path: Path
    manifest: dict[str, Any]


RESERVED_MODULES = [
    {
        "id": "decision_engine",
        "name": "Decision Engine",
        "type": "reserved_interface",
        "enabled": False,
    },
    {
        "id": "value_engine",
        "name": "Value Engine",
        "type": "reserved_interface",
        "enabled": False,
    },
    {
        "id": "organization_brain",
        "name": "Organization Brain",
        "type": "reserved_interface",
        "enabled": False,
    },
]


def load_capsules(capsules_path: Path) -> list[Capsule]:
    if not capsules_path.exists():
        return []

    capsules: list[Capsule] = []
    for child in sorted(capsules_path.iterdir()):
        manifest_path = child / "manifest.json"
        if not child.is_dir() or not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        capsules.append(
            Capsule(
                id=str(manifest["id"]),
                name=str(manifest["name"]),
                version=str(manifest["version"]),
                type=str(manifest["type"]),
                capabilities=list(manifest.get("capabilities", [])),
                path=child,
                manifest=manifest,
            )
        )
    return capsules


def require_stanai_capsule(capsules: list[Capsule]) -> Capsule:
    for capsule in capsules:
        if capsule.id == "stanai":
            return capsule
    raise RuntimeError("StanAI capsule is required for Berlin Demo v0.1")
