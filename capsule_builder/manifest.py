from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


REQUIRED_MANIFEST_FIELDS = ("capsule_id", "capsule_version", "format_version", "required_sources")


def load_source_manifest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Source manifest not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Source manifest must be a mapping")
    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in data:
            raise ValueError(f"Source manifest missing required field: {field}")
    return data
