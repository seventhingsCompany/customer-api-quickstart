# Create or update an object

AI prompt:

> Use the selected SDK to create an object from a JSON payload, discovering mandatory fields first. Also support patching an existing UUID without replacing unrelated fields.

1. Run `hello` and inspect the field definitions.
2. Prepare a JSON object using actual instance field keys. Set `SEVENTHINGS_PAYLOAD_FILE` to that file's path (relative to the current working directory or absolute).
3. Run `create`, or set `SEVENTHINGS_OBJECT_UUID` and run `update`.

`create` checks mandatory-field presence, then prints `{ "uuid": "..." }`. `update` sends only the payload's fields and prints the UUID with `updated: true`. The server still validates types, allowed values, and references. These commands perform actual writes; creation does not deduplicate or upsert.

Verification: the offline suite checks the creation payload, missing-required-field rejection before a write, invalid JSON-object shape, and partial updates that omit creation-required fields.

Implementations: [TypeScript](../starters/typescript/main.ts), [Python](../starters/python/main.py), [Go](../starters/go/main.go), [PHP](../starters/php/main.php), actions `create` and `update`.
