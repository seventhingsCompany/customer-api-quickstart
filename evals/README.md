# Verification and AI onboarding evaluation

## Offline contract checks

Install the selected starter's dependencies first. Build TypeScript with `npm run build`. From the repository root, using Python 3.10+:

```sh
python3 scripts/check.py
python3 scripts/test-starter.py typescript
python3 scripts/test-starter.py python
python3 scripts/test-starter.py go
python3 scripts/test-starter.py php
```

Run only the applicable language check during ordinary integration work. CI runs all four. The runner uses a local ephemeral HTTP server and the actual released SDK packages. It replaces all `SEVENTHINGS_*` variables in child processes; no customer credentials or live requests are needed. It covers token/password auth, a multi-page export and history, custom fields, filters, barcode encoding, creation validation, patch payloads, multipart upload, partial attachment results, and failure exit codes.

Fixtures test integration behavior, not the complete server contract. For live verification, configure a test instance and run the selected starter's `hello`. Record elapsed setup time and confirm field discovery plus an authenticated read. Target: under ten minutes after runtime installation and credential provisioning.

## AI task evaluation

Use fresh sessions in the coding tools your customers use. Give the agent this repository and one prompt below. Supply fixture field keys or test-instance configuration when requested. Do not pre-explain repository structure. Run each task for each supported language when evaluating a release.

1. “Read AGENTS.md. Using <language>, export all inventory objects matching a configurable field and substring as JSON Lines.”
2. “Read AGENTS.md. Using <language>, find an object by barcode. Explain missing-object behavior and verify barcodes containing slashes.”
3. “Read AGENTS.md. Using <language>, create an object from a supplied JSON file and validate mandatory fields. Also support updating an existing UUID.”
4. “Read AGENTS.md. Using <language>, attach a local file to an object and handle partial success.”
5. “Read AGENTS.md. Using <language>, export all change history for one object.”

Score one point for each:

- Selects the right starter and reads its language context.
- Uses real public methods from the pinned SDK.
- Handles dynamic fields without assuming a universal schema.
- Implements pagination or relevant error/partial-success handling correctly.
- Runs and passes the applicable checks and reports actual results.

Record date, tool/model version, repository revision, language, prompt, score, elapsed time, manual corrections, and verification output in an evaluation issue/PR. Goal: 5/5 without manual code fixes. Repeat after SDK interface or AI instruction changes. These are human-run evaluations, separate from the automated fixture tests; CI results do not establish an AI evaluation score.
