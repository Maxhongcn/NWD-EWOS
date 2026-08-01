# NWD-EWOS

NWD Enterprise Wisdom Operating System Berlin Demo runtime scaffold.

Read `PROJECT.md` first. It is the source of truth for architecture and implementation boundaries.

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn runtime.main:app --host 127.0.0.1 --port 8080
```

## Test

```bash
python -m unittest discover tests
```
