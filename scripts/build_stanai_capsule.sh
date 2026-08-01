#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python -m capsule_builder build \
  --source founder-source/stanai \
  --output dist/stanai.cap \
  "$@"
