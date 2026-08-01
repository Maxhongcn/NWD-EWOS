from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LicenseInfo:
    valid: bool
    product: str
    edition: str
    licensee: str
    features: list[str]
    warnings: list[str]


def load_license(path: Path) -> LicenseInfo:
    warnings: list[str] = []

    if not path.exists():
        return LicenseInfo(
            valid=False,
            product="unknown",
            edition="unknown",
            licensee="unknown",
            features=[],
            warnings=[f"License file not found: {path}"],
        )

    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("product", "edition", "version", "licensee", "features"):
        if key not in data:
            warnings.append(f"Missing license field: {key}")

    return LicenseInfo(
        valid=not warnings,
        product=str(data.get("product", "unknown")),
        edition=str(data.get("edition", "unknown")),
        licensee=str(data.get("licensee", "unknown")),
        features=list(data.get("features", [])),
        warnings=warnings,
    )
