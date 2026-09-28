# Export inventory

AI prompt:

> Use the selected starter to export all objects matching a customer-selected field and substring as JSON Lines. Preserve custom fields and verify pagination with the offline suite.

1. Run `hello` to discover the instance's field keys.
2. Optionally set `SEVENTHINGS_FILTER_FIELD` and `SEVENTHINGS_FILTER_VALUE` together. Leave both empty to export all objects.
3. Run `export` using your [starter command](../README.md#start-here), redirecting stdout to `inventory.jsonl`.

Each line is one complete object. The implementation streams SDK iterator results instead of accumulating the entire inventory. Check the command exit status before consuming the export: a failure can leave a partial file. For recurring exports, write a temporary file and rename it only after success.

Verification: `python3 scripts/test-starter.py <language>` exercises a 101-object, two-page export, verifies filter propagation on both requests, and checks preservation of nested custom fields.

Implementations: [TypeScript](../starters/typescript/main.ts), [Python](../starters/python/main.py), [Go](../starters/go/main.go), [PHP](../starters/php/main.php), action `export`.
