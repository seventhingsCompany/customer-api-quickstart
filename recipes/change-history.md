# Read object change history

AI prompt:

> Use the selected SDK to export an object's entire change history as JSON Lines, preserving dynamic event fields and following page metadata.

Set `SEVENTHINGS_OBJECT_UUID` and run `history`. Each line is one event, in the server's newest-first order. The command requests pages of 100 until the response metadata reaches `total`, or a page is empty. An empty history succeeds with no stdout.

Object history entries have varying shapes (asset, task, rental case, merge). Do not assume every event has the same properties. Other resource histories may use typed models and JSON-encoded `details`; consult the matching SDK before adapting this recipe.

Verification: the offline suite returns 101 events over two pages and verifies that the output preserves every record.

Implementations: [TypeScript](../starters/typescript/main.ts), [Python](../starters/python/main.py), [Go](../starters/go/main.go), [PHP](../starters/php/main.php), action `history`.
