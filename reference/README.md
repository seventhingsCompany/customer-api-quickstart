# Versioned API reference

[`endpoints.json`](endpoints.json) is a compact, generated operation index containing the API info, source revision, URL, and full-source SHA-256. Use it to locate an endpoint without loading the entire specification into an agent's context. It is an index, not a replacement for request/response schemas.

The source is the normalized OpenAPI document from `customer-api-docs`, pinned in `sdk-manifest.json`. That repository transforms the canonical API specification and uses it for its documentation site. The SDK and API reference version numbers are independent; the index is not a claim that every operation exists in every deployed instance.

The full schema is committed as `reference/customer-api.json`, so customer onboarding requires no access to the source documentation repository. Read only the relevant paths and referenced components when implementing a task.

Maintainers can regenerate from the repository root, using Python 3.10+ and a docs checkout with the pinned commit:

```sh
python3 scripts/refresh-reference.py --checkout ../customer-api-docs
```

Without `--checkout`, the script attempts the pinned GitHub raw URL; this requires the source to be publicly accessible. The docs source currently is not anonymously accessible. The script reads the exact Git revision, even if the local checkout has uncommitted changes. The published current specification is also available at https://api.seventhings.com/customer-api.json, but may describe a different release.

To update, pass `--revision <full-commit-sha>` with `--checkout`, inspect the generated diff, and run `python3 scripts/check.py`. The manifest revision is updated after successful regeneration. SDK release updates are separate reviewed changes.
