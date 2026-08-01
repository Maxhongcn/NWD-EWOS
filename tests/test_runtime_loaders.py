from __future__ import annotations

import unittest
from pathlib import Path

from runtime.config_loader import load_runtime_config
from runtime.license_loader import load_license
from runtime.module_loader import load_capsules, require_stanai_capsule


ROOT = Path(__file__).resolve().parents[1]


class RuntimeLoaderTests(unittest.TestCase):
    def test_load_runtime_config(self) -> None:
        config = load_runtime_config(ROOT / "config/runtime.yaml", ROOT)

        self.assertEqual(config.name, "NWD-EWOS")
        self.assertEqual(config.version, "Berlin Demo v0.1")
        self.assertTrue(config.offline_mode)
        self.assertEqual(config.api_port, 8080)

    def test_load_license(self) -> None:
        license_info = load_license(ROOT / "config/license.json")

        self.assertTrue(license_info.valid)
        self.assertEqual(license_info.product, "NWD-EWOS")
        self.assertIn("runtime", license_info.features)

    def test_load_stanai_capsule(self) -> None:
        capsules = load_capsules(ROOT / "capsules")
        stanai = require_stanai_capsule(capsules)

        self.assertEqual(stanai.id, "stanai")
        self.assertFalse(stanai.manifest["direct_database_access"])


if __name__ == "__main__":
    unittest.main()
