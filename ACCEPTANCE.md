# ACCEPTANCE

## Berlin Demo v0.1 Acceptance

The repository is accepted when:

- `PROJECT.md` is the single source of truth.
- `TASKS.md` identifies the current implementation task.
- Runtime starts from local configuration.
- License verification is local and lightweight.
- Capsules are discovered from the configured capsule path.
- StanAI capsule manifest loads successfully.
- REST API exposes:
  - `GET /health`
  - `GET /runtime/status`
  - `GET /modules`
  - `POST /stanai/query`
- Decision Engine, Value Engine, and Organization Brain are represented only as future placeholders.
- No cloud dependency is introduced.
- Tests pass locally.

## Non-Acceptance

The repository is not accepted if:

- Runtime requires internet access to start.
- StanAI directly reads enterprise data.
- New architecture modules are invented outside `PROJECT.md`.
- Existing architecture names are renamed.
- Placeholder engines are implemented prematurely.
