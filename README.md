# api-diff-sentinel

Compare two OpenAPI specs (JSON) and report **breaking** vs **non-breaking** changes. Built for CI.

```bash
pip install api-diff-sentinel
api-diff old-openapi.json new-openapi.json
api-diff old.json new.json --fail-on-breaking   # exit code 1 if breaking
api-diff old.json new.json --json               # machine-readable
```

**Example output**
```
Verdict: BREAKING CHANGES DETECTED
  Removed endpoint: `/v1/orders`
  Added new required parameter `org_id` to `GET /v1/users` (Breaking)
  Added new endpoint: `/v1/products`
```

## GitHub Actions
```yaml
- run: pip install api-diff-sentinel
- run: api-diff base/openapi.json head/openapi.json --fail-on-breaking
```

## What it detects
Breaking: removed endpoints, removed methods, removed parameters, new **required** parameters.
Non-breaking: new endpoints, new methods, new optional parameters.

## Limitations (v1)
- Compares `paths`, methods and parameters only. It does **not** yet diff request/response schemas, types, enums or auth.
- JSON specs only (convert YAML first); `$ref` parameters are not resolved.

MIT licensed.
