# Upload and attach a file

AI prompt:

> Use the selected SDK to upload a file and attach it to an object's configured attachment field. Preserve the uploaded UUID and inspect partial-success responses.

Set `SEVENTHINGS_OBJECT_UUID`, `SEVENTHINGS_FILE` (local file path), and `SEVENTHINGS_ATTACHMENT_FIELD` (actual field key discovered from field definitions). Run `attach`.

The command uploads the bytes and links the returned file UUID. It prints `fileUuid`, `status`, and `body`. HTTP 207 is printed but exits nonzero, since the link may have partially failed. Inspect individual results before retrying. Reuse an already uploaded UUID to repair a link rather than running the whole command again. A transport failure between upload and link can also leave an uploaded file; build reconciliation into production workflows.

Verification: the offline suite checks multipart bytes, correct attachment keys, successful linking, and nonzero exit on a 207 response.

Implementations: [TypeScript](../starters/typescript/main.ts), [Python](../starters/python/main.py), [Go](../starters/go/main.go), [PHP](../starters/php/main.php), action `attach`.
