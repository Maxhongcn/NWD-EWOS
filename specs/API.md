# API Specification

## GET /health

Returns runtime health.

## GET /runtime/status

Returns runtime version, offline mode, license status, and loaded capsule count.

## GET /modules

Returns loaded capsules and reserved future modules.

## POST /stanai/query

Accepts:

```json
{
  "query": "string",
  "context": {}
}
```

Returns a placeholder StanAI response in Berlin Demo v0.1.
