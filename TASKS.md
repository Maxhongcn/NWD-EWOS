# TASKS

## TASK-0001: Scaffold Berlin Demo Runtime

Status: DONE

Goal:

Create the first repository scaffold for the NWD Enterprise Wisdom Operating System Berlin Demo runtime.

Scope:

- Create architecture-first project documents.
- Create runtime package structure.
- Create configuration, module, license, and capsule loaders.
- Create REST API endpoints.
- Create StanAI placeholder capsule.
- Create local config, module, license, and root manifest files.
- Create schemas and acceptance criteria.
- Add basic tests.
- Initialize git and commit the scaffold.

Out of scope:

- Decision Engine implementation.
- Value Engine implementation.
- Organization Brain implementation.
- Real model inference.
- Cloud service integration.
- Production license encryption.

Completion note:

TASK-0001 is complete when the repository can load local configuration, validate the local demo license, discover the StanAI capsule, expose the API contract, and pass the included tests.

## TASK-0002: Implement StanAI Query Adapter

Status: TODO

Goal:

Replace placeholder StanAI query response with a local adapter contract.

Architect notes:

- Do not select the model runtime yet.
- Do not add cloud dependencies.
- Keep the public API unchanged.
