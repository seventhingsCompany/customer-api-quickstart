# Find an object by barcode

AI prompt:

> Use the selected SDK to look up an object by its raw barcode. Handle a missing object separately from authentication or network failures.

Set `SEVENTHINGS_BARCODE` to the raw barcode and run `lookup`. The SDK handles encoding; a barcode containing `/` must not be pre-encoded. Archived objects are included by this endpoint.

Success prints one JSON record. The starter exits nonzero for missing objects and other API errors. In a larger integration, inspect the SDK's status-aware error type to implement the application's not-found behavior rather than treating all failures as missing data.

Verification: the offline suite checks `INV/001` reaches the encoded lookup route and that an absent barcode fails.

Implementations: [TypeScript](../starters/typescript/main.ts), [Python](../starters/python/main.py), [Go](../starters/go/main.go), [PHP](../starters/php/main.php), action `lookup`.
