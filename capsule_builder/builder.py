from __future__ import annotations

import hashlib
import io
import json
import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from capsule_builder.crypto import encrypt_bytes
from capsule_builder.manifest import load_source_manifest

INTERNAL_MANIFEST = "capsule-manifest.json"
SOURCES_PREFIX = "sources/"


def build_capsule(source: Path, output: Path, allow_unencrypted_demo: bool = False) -> dict[str, Any]:
    manifest = load_source_manifest(source / "source-manifest.yaml")
    required_files = _required_source_files(manifest)
    _validate_required_files(source, required_files)

    source_entries = []
    for relative_path in required_files:
        data = (source / relative_path).read_bytes()
        source_entries.append(
            {
                "path": relative_path.as_posix(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": len(data),
            }
        )

    capsule_key = os.environ.get("EWOS_CAPSULE_KEY")
    internal_manifest = {
        "capsule_id": manifest["capsule_id"],
        "capsule_version": manifest["capsule_version"],
        "format_version": manifest["format_version"],
        "build_timestamp": datetime.now(timezone.utc).isoformat(),
        "source_files": source_entries,
        "entrypoint": manifest.get("entrypoint", {}),
        "reserved_capabilities": manifest.get("reserved_capabilities", []),
        "runtime": manifest.get("runtime", {}),
        "container": "zip",
        "encrypted": bool(capsule_key),
    }

    zip_bytes = _build_zip_bytes(source, required_files, internal_manifest)

    if capsule_key:
        payload = encrypt_bytes(zip_bytes, capsule_key)
        payload["capsule_id"] = manifest["capsule_id"]
        payload["capsule_version"] = manifest["capsule_version"]
        payload["format_version"] = manifest["format_version"]
        output_bytes = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    elif allow_unencrypted_demo:
        output_bytes = zip_bytes
    else:
        raise RuntimeError(
            "EWOS_CAPSULE_KEY is required. Use --allow-unencrypted-demo only for temporary Berlin demo builds."
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(output_bytes)
    return {
        "capsule_id": manifest["capsule_id"],
        "capsule_version": manifest["capsule_version"],
        "source_file_count": len(required_files),
        "encrypted": bool(capsule_key),
        "output": str(output),
    }


def _build_zip_bytes(source: Path, required_files: list[Path], internal_manifest: dict[str, Any]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(INTERNAL_MANIFEST, json.dumps(internal_manifest, indent=2, sort_keys=True))
        for relative_path in required_files:
            archive.write(source / relative_path, SOURCES_PREFIX + relative_path.as_posix())
    return buffer.getvalue()


def _required_source_files(manifest: dict[str, Any]) -> list[Path]:
    required_sources = manifest.get("required_sources", {})
    files: list[Path] = []
    for group in ("instructions", "knowledge"):
        for value in required_sources.get(group, []):
            files.append(Path(value))
    return files


def _validate_required_files(source: Path, required_files: list[Path]) -> None:
    missing = [relative_path.as_posix() for relative_path in required_files if not (source / relative_path).is_file()]
    if missing:
        joined = ", ".join(missing)
        raise FileNotFoundError(f"Missing required StanAI source file(s): {joined}")
