# StanAI Capsule Builder

Builds and verifies the Berlin Demo StanAI capsule without printing source content.

## Source Location

Place the existing StanAI source files under:

```text
founder-source/stanai/
```

Required files are declared in:

```text
founder-source/stanai/source-manifest.yaml
```

## Build Encrypted Capsule

```bash
EWOS_CAPSULE_KEY="replace-with-local-secret" python -m capsule_builder build \
  --source founder-source/stanai \
  --output dist/stanai.cap
```

## Build Temporary Unencrypted Berlin Demo Capsule

```bash
python -m capsule_builder build \
  --source founder-source/stanai \
  --output dist/stanai.cap \
  --allow-unencrypted-demo
```

## Verify Capsule

```bash
python -m capsule_builder verify \
  --capsule dist/stanai.cap
```

Encrypted capsule verification also requires `EWOS_CAPSULE_KEY`.

The verifier reports capsule metadata and hash status only. It does not print source content.
