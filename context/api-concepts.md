# API concepts

The SDK takes an instance root such as `https://example.seventhings.com` and appends `/customer-api/v1`. Resources include objects/assets, rooms, locations, persons, users, tasks, rentals, files, reports, field definitions, and CircularityHub.

Object records have an instance-defined schema. Preserve arbitrary field keys and values. `asset` is the field-definition template corresponding to objects.

## Lists and filters

The four SDKs' object `list` methods return arrays of records, not page metadata. Their `all` iterators walk pages lazily and expose field wrappers (Go yields a record and an error). An iterator stops on a short/empty page. The starters use a page size of 100 and the SDK's `like` filter for substring searches.

Object history returns `items`, `page`, `per_page`, and `total` on the wire. Language SDKs map these names differently. The history recipe loops until the page metadata reaches the total, with an empty-page termination condition. History entries are dynamic maps and newest first.

Pagination is not a consistent snapshot: records can change while an export is running. Define ordering and reconciliation requirements when building a recurring synchronization.

## Writes

Creation returns the new UUID. Patch returns differ by SDK; starters emit a uniform `{uuid, updated: true}` after a successful request. Patch only the fields you intend to change. Creation is not an upsert and the examples do not assume idempotency guarantees.

File attachment is two operations: upload bytes, then link the resulting file UUID to a configured attachment field. Inspect HTTP 207 bodies for per-item failures. The starter prints the upload UUID and response so a failed link can be diagnosed without uploading again.
