from __future__ import annotations

import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from capsule_builder.builder import build_capsule
from capsule_builder.verifier import verify_capsule


class CapsuleBuilderTests(unittest.TestCase):
    def test_build_and_verify_unencrypted_demo_capsule(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _create_source_fixture(root)
            output = root / "dist/stanai.cap"

            build_result = build_capsule(source, output, allow_unencrypted_demo=True)
            verify_result = verify_capsule(output)

            self.assertEqual(build_result["capsule_id"], "nwd.stanai.leadership")
            self.assertEqual(verify_result["capsule_version"], "1.0.0-berlin")
            self.assertEqual(verify_result["source_file_count"], 16)
            self.assertTrue(verify_result["verified"])

    def test_build_fails_without_key_or_demo_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _create_source_fixture(root)
            output = root / "dist/stanai.cap"

            previous_key = os.environ.pop("EWOS_CAPSULE_KEY", None)
            try:
                with self.assertRaises(RuntimeError):
                    build_capsule(source, output)
            finally:
                if previous_key is not None:
                    os.environ["EWOS_CAPSULE_KEY"] = previous_key

    def test_build_and_verify_encrypted_capsule(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _create_source_fixture(root)
            output = root / "dist/stanai.cap"
            previous_key = os.environ.get("EWOS_CAPSULE_KEY")
            os.environ["EWOS_CAPSULE_KEY"] = "local-test-key"
            try:
                build_result = build_capsule(source, output)
                verify_result = verify_capsule(output)
            finally:
                if previous_key is None:
                    os.environ.pop("EWOS_CAPSULE_KEY", None)
                else:
                    os.environ["EWOS_CAPSULE_KEY"] = previous_key

            self.assertTrue(build_result["encrypted"])
            self.assertTrue(verify_result["encrypted"])
            self.assertTrue(verify_result["verified"])

    def test_missing_required_source_fails_without_content_leak(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _create_source_fixture(root)
            secret_file = source / "knowledge/KB00-StanAI-Index-Router.txt"
            secret_file.unlink()

            with self.assertRaises(FileNotFoundError) as raised:
                build_capsule(source, root / "dist/stanai.cap", allow_unencrypted_demo=True)

            message = str(raised.exception)
            self.assertIn("KB00-StanAI-Index-Router.txt", message)
            self.assertNotIn("fixture-secret-content", message)

    def test_package_preserves_source_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = _create_source_fixture(root)
            output = root / "dist/stanai.cap"

            build_capsule(source, output, allow_unencrypted_demo=True)

            expected = (source / "knowledge/KB13-Workshop-Mode.md").read_bytes()
            with zipfile.ZipFile(output, "r") as archive:
                actual = archive.read("sources/knowledge/KB13-Workshop-Mode.md")
            self.assertEqual(actual, expected)


def _create_source_fixture(root: Path) -> Path:
    source = root / "founder-source/stanai"
    instructions = source / "instructions"
    knowledge = source / "knowledge"
    instructions.mkdir(parents=True)
    knowledge.mkdir(parents=True)

    (source / "source-manifest.yaml").write_text(_manifest_text(), encoding="utf-8")
    (instructions / "stanai-instructions.md").write_bytes(b"fixture-secret-content: instructions\n")
    for filename in _knowledge_files():
        (knowledge / filename).write_bytes(f"fixture-secret-content: {filename}\n".encode("utf-8"))
    return source


def _knowledge_files() -> list[str]:
    return [
        "KB00-StanAI-Index-Router.txt",
        "KB01-Brand-Identity.txt",
        "KB02-New-WangDao-Core.txt",
        "KB03-Multilingual-Tone.txt",
        "KB04-Decision-Interface.txt",
        "KB05-Stan-Shih-Authority.txt",
        "KB06-Assembly-Safety.txt",
        "KB07-Japan-Market.txt",
        "KB08-English-Spanish.txt",
        "KB09-Scenario-Pack.txt",
        "KB10-Demo-Pack.txt",
        "KB11-User-Manual.txt",
        "KB12-QA-Gate.txt",
        "KB13-Workshop-Mode.md",
        "BIO-StanAI-Memory-Cards.txt",
    ]


def _manifest_text() -> str:
    return """capsule_id: nwd.stanai.leadership
capsule_version: 1.0.0-berlin
format_version: "0.1"
entrypoint:
  type: leadership_orchestrator
  name: StanAI
required_sources:
  instructions:
    - instructions/stanai-instructions.md
  knowledge:
    - knowledge/KB00-StanAI-Index-Router.txt
    - knowledge/KB01-Brand-Identity.txt
    - knowledge/KB02-New-WangDao-Core.txt
    - knowledge/KB03-Multilingual-Tone.txt
    - knowledge/KB04-Decision-Interface.txt
    - knowledge/KB05-Stan-Shih-Authority.txt
    - knowledge/KB06-Assembly-Safety.txt
    - knowledge/KB07-Japan-Market.txt
    - knowledge/KB08-English-Spanish.txt
    - knowledge/KB09-Scenario-Pack.txt
    - knowledge/KB10-Demo-Pack.txt
    - knowledge/KB11-User-Manual.txt
    - knowledge/KB12-QA-Gate.txt
    - knowledge/KB13-Workshop-Mode.md
    - knowledge/BIO-StanAI-Memory-Cards.txt
reserved_capabilities:
  - decision
  - value
  - organization_brain
runtime:
  execution_mode: local
  cloud_reasoning_required: false
  offline_capable: true
"""


if __name__ == "__main__":
    unittest.main()
