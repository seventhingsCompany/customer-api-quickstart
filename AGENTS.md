# Customer API integration instructions

## Workflow

1. Identify the user's language and desired integration. If unspecified, ask which language fits their project.
2. Read `starters/<language>/README.md`, `context/languages/<language>.md`, and that starter's entry point.
3. Read the relevant recipe in `recipes/` and only the context needed for the task.
4. Use the installed SDK's public interfaces. Match the version in `sdk-manifest.json`; method names and return types differ across languages.
5. Implement in the selected starter or the user's existing integration. Run its checks and the offline contract suite described in `evals/README.md`.
6. Report the run command, required configuration, and checks actually completed.

## Context routing

- API concepts and pagination: `context/api-concepts.md`
- Authentication and configuration: `context/authentication.md`
- Instance-specific fields: `context/dynamic-fields.md`
- Errors and setup problems: `context/troubleshooting.md`
- API contract source and optional local snapshot: `reference/README.md`
- Source workspaces and dependency overrides: `CONTRIBUTING.md`

## Implementation rules

- Use SDK methods rather than recreating HTTP clients.
- Fetch field definitions; example field names are not a universal schema. Required-field helpers check presence, not value validity.
- Use SDK iterators for full object exports. A `list` call returns only one page. History uses explicit page metadata.
- Preserve unknown/custom fields in exported JSON. Do not infer business meaning from missing values.
- Pass raw barcodes to the SDK. Do not URL-encode them first.
- Keep configuration in environment variables. Do not include credentials in code, output, or committed examples.
- Inspect attachment response status and body; HTTP 207 is a partial result, not complete success. Avoid blindly repeating uploads or creates after ambiguous failures.
- Put machine-readable data on stdout and errors on stderr. Preserve nonzero exit codes.
- Use `hello` for live verification; use write recipes when the user's task calls for writes.

## Sources of truth

The versioned OpenAPI reference describes HTTP behavior. The matching installed SDK describes language interfaces. The starter commands and offline tests demonstrate integration behavior. The customer's field definitions describe their schema. If sources disagree, inspect the exact versions and report the mismatch rather than inventing an interface.
