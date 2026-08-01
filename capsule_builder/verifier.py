from __future__ import annotations

import hashlib
import io
import json
import os
import zipfile
from pathlib import Path
from typing import Any

from capsule_builder.builder import INTERNAL_MANIFEST, SOURCES_PREFIX
from capsule_builder.crypto import decrypt_bytes


def verify_capsule(capsule: Path) -> dict[str, Any]:
    if not capsule.is_file():
        raise FileNotFoundError(f"Capsule not found: {capsule}")

    data = capsule.read_bytes()
    encrypted = data.startswith(b"{")
    if encrypted:
        key = os.environ.get("EWOS_CAPSULE_KEY")
        if not key:
            raise RuntimeError("EWOS_CAPSULE_KEY is required to verify encrypted capsules")
        data = decrypt_bytes(json.loads(data.decode("utf-8")), key)

    with zipfile.ZipFile(io.BytesIO(data), "r") as archive:
        names = set(archive.namelist())
        if INTERNAL_MANIFEST not in names:
            raise ValueError("Capsule missing internal manifest")
        manifest = json.loads(archive.read(INTERNAL_MANIFEST).decode("utf-8"))
        source_files = manifest.get("source_files", [])
        for source_file in source_files:
            relative_path = source_file["path"]
            archive_path = SOURCES_PREFIX + relative_path
            if archive_path not in names:
                raise ValueError(f"Capsule missing source payload: {relative_path}")
            digest = hashlib.sha256(archive.read(archive_path)).hexdigest()
            if digest != source_file["sha256"]:
                raise ValueError(f"SHA-256 mismatch for source payload: {relative_path}")

    return {
        "capsule_id": manifest["capsule_id"],
        "capsule_version": manifest["capsule_version"],
        "format_version": manifest["format_version"],
        "source_file_count": len(source_files),
        "encrypted": encrypted,
        "verified": True,
    }
