# NWD Enterprise Wisdom Operating System (EWOS)

Version: Berlin Demo v0.1
Status: ACTIVE
Owner: NWD Team

---

## 1. Mission

This repository builds the first runnable version of the NWD Enterprise Wisdom Operating System (EWOS).

Target:

- Runs completely on Acer Local AI PC / AI Box.
- Has no cloud dependency for reasoning.
- Uses a modular architecture.
- Is Berlin Demo ready.
- Stays future-proof for Organization Brain, Decision Engine, and Value Engine.

This repository is NOT building a chatbot.

This repository is building a Local Enterprise Wisdom Runtime.

---

## 2. Product Vision

EWOS provides enterprise leadership intelligence through modular local execution.

The first implementation is StanAI.

Future implementations include:

- Organization Brain
- Decision Engine
- Value Engine
- Risk Engine
- Simulation Engine

StanAI remains the leadership layer.

Other modules provide capabilities.

---

## 3. Architecture

```text
                 User
                   |
                   v
             Acer Application
                   |
                   v
             EWOS Runtime
                   |
                   v
     StanAI Leadership Orchestrator
                   |
         +---------+---------+
         |         |         |
         v         v         v
 Decision      Value     Organization
  Engine       Engine        Brain
```

Rules:

- StanAI NEVER owns enterprise data.
- StanAI NEVER directly reads databases.
- StanAI orchestrates capabilities.
- Architecture decisions belong to the architect, not the implementation engineer.

---

## 4. First Milestone: Berlin Demo

Only implement the following:

- Runtime
- Module Loader
- Configuration Loader
- License Loader
- REST API
- StanAI Capsule Loader

Everything else remains placeholder.

Do NOT implement Decision Engine.

Do NOT implement Value Engine.

Do NOT implement Organization Brain.

Only reserve interfaces.

---

## 5. Repository Structure

```text
NWD-EWOS/
  runtime/
  capsules/
  config/
  specs/
  installer/
  schemas/
  logs/
  examples/
  docs/
```

---

## 6. Runtime Directory

```text
runtime/
  main.py
  api_server.py
  config_loader.py
  license_loader.py
  module_loader.py
  logger.py
```

---

## 7. Runtime Startup

```text
Start
  |
  v
Load Configuration
  |
  v
Verify License
  |
  v
Load Capsules
  |
  v
Register Capabilities
  |
  v
Initialize StanAI
  |
  v
Wait Request
```

---

## 8. Capsule Structure

Each module is packaged as one capsule.

Example:

```text
capsules/
  stanai/
    manifest.json
    persona.dat
    knowledge.dat
    workflow.dat
    assets/
```

A capsule contains:

- `manifest.json`
- `persona.dat`
- `knowledge.dat`
- `workflow.dat`
- `assets/`

Implementation details remain private.

Runtime only knows how to load a capsule manifest and register its declared capabilities.

---

## 9. Configuration

`config/runtime.yaml` contains:

- Runtime version
- Module path
- License path
- Logging
- API port
- Offline mode

No hardcoded values.

---

## 10. License

Berlin Demo uses local `config/license.json`.

Future versions may use a License Server.

Runtime API must not change.

---

## 11. Current Implementation Boundary

The Berlin Demo runtime must be able to:

- Load `config/runtime.yaml`.
- Load and lightly validate `config/license.json`.
- Scan `capsules/`.
- Load the StanAI capsule manifest.
- Expose the demo REST API.
- Return placeholder StanAI responses.

The Berlin Demo runtime must not:

- Call cloud AI services.
- Implement real enterprise reasoning.
- Read enterprise databases.
- Add unapproved modules.
- Rename architecture components.
