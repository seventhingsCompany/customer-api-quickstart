# Find an object by barcode

AI prompt:

> Use the selected SDK to look up an object by its raw barcode. Handle a missing object separately from authentication or network failures.

Set `SEVENTHINGS_BARCODE` to the raw barcode and run `lookup`. The SDK handles encoding; a barcode containing `/` must not be pre-encoded. Archived objects are included by this endpoint.

Success prints one JSON record and exits 0. A missing object (HTTP 404) prints a message to stderr and exits 3; authentication, network, and other API errors exit 1. The starters detect not-found with the SDK's status-aware error type; do the same in a larger integration rather than treating all failures as missing data. A wrong instance URL also produces 404s, so verify the configuration with `hello` first.

Verification: the offline suite checks `INV/001` reaches the encoded lookup route, that an absent barcode exits 3, and that an authentication failure exits 1.

Implementations: [TypeScript](../starters/typescript/main.ts), [Python](../starters/python/main.py), [Go](../starters/go/main.go), [PHP](../starters/php/main.php), action `lookup`.
