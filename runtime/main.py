from __future__ import annotations

import os
from pathlib import Path

from runtime.api_server import RuntimeContext, create_app
from runtime.config_loader import load_runtime_config
from runtime.license_loader import load_license
from runtime.logger import configure_logging
from runtime.module_loader import load_capsules, require_stanai_capsule


def build_runtime_context(root: Path | None = None) -> RuntimeContext:
    project_root = root or Path(os.environ.get("EWOS_ROOT", Path.cwd()))
    config = load_runtime_config(project_root / "config/runtime.yaml", project_root)
    configure_logging(config.log_level, config.log_path)

    license_info = load_license(config.license_path)
    capsules = load_capsules(config.modules_path)
    require_stanai_capsule(capsules)

    return RuntimeContext(
        version=config.version,
        offline_mode=config.offline_mode,
        license=license_info,
        capsules=capsules,
    )


app = create_app(build_runtime_context())


def main() -> None:
    try:
        import uvicorn
    except ImportError as exc:
        raise SystemExit("Install dependencies with: pip install -r requirements.txt") from exc

    root = Path(os.environ.get("EWOS_ROOT", Path.cwd()))
    config = load_runtime_config(root / "config/runtime.yaml", root)
    uvicorn.run(app, host=config.api_host, port=config.api_port)


if __name__ == "__main__":
    main()
