from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RuntimeConfig:
    name: str
    version: str
    modules_path: Path
    license_path: Path
    log_level: str
    log_path: Path
    api_host: str
    api_port: int
    offline_mode: bool


def load_runtime_config(config_path: Path, root: Path) -> RuntimeConfig:
    raw_config = _parse_simple_yaml(config_path)

    runtime = raw_config.get("runtime", {})
    modules = raw_config.get("modules", {})
    license_config = raw_config.get("license", {})
    logging = raw_config.get("logging", {})
    api = raw_config.get("api", {})

    return RuntimeConfig(
        name=str(runtime.get("name", "NWD-EWOS")),
        version=str(runtime.get("version", "Berlin Demo v0.1")),
        modules_path=_resolve(root, modules.get("path", "capsules")),
        license_path=_resolve(root, license_config.get("path", "config/license.json")),
        log_level=str(logging.get("level", "INFO")),
        log_path=_resolve(root, logging.get("path", "logs/runtime.log")),
        api_host=str(api.get("host", "127.0.0.1")),
        api_port=int(api.get("port", 8080)),
        offline_mode=bool(raw_config.get("offline_mode", True)),
    )


def _resolve(root: Path, value: Any) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    return root / path


def _parse_simple_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Runtime config not found: {path}")

    result: dict[str, Any] = {}
    current_section: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        if not line.startswith(" "):
            key, value = _split_key_value(line)
            if value is None:
                result[key] = {}
                current_section = key
            else:
                result[key] = _coerce_scalar(value)
                current_section = None
            continue

        if current_section is None:
            raise ValueError(f"Nested value without section in {path}: {line}")

        key, value = _split_key_value(line.strip())
        if value is None:
            raise ValueError(f"Berlin Demo config supports one nested level only: {line}")
        section = result.setdefault(current_section, {})
        section[key] = _coerce_scalar(value)

    return result


def _split_key_value(line: str) -> tuple[str, str | None]:
    if ":" not in line:
        raise ValueError(f"Invalid config line: {line}")
    key, value = line.split(":", 1)
    value = value.strip()
    return key.strip(), value if value else None


def _coerce_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value
