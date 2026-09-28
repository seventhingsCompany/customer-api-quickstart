# Instance-specific fields

Use `hello` to inspect `fieldDefinitions`, then select field keys for filters, writes, and file attachments. `inventory_name`, `barcode`, and `documents` are illustrative keys, not guaranteed fields on every instance.

Before creation, each starter invokes its SDK's missing-required-fields helper for the `asset` template. This excludes system-managed keys and catches absent/null required values. It does **not** validate types, constraints, references, or allowed values. Inspect the definitions and handle server validation errors as well.

For updates, send a JSON object containing only the changed fields. Partial updates need not repeat every creation-required field. Do not invent defaults for unknown required fields; obtain the intended values from the integration's inputs.

Exports retain every returned key. SDK field wrappers offer typed accessors when transforming values, but missing or mismatched values should remain distinguishable from valid empty/zero values.
