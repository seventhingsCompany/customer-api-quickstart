# Go starter

Requires Go 1.25+. First configure and export the variables from the root [environment template](../../.env.example), following the [root instructions](../../README.md).

From this directory:

```sh
go mod download
go vet ./...
go test ./...
go run . hello
```

Expected output: one JSON object with `ping`, `fieldDefinitions`, and `objects` (up to 100 records). An empty inventory is valid.

Replace `hello` with any [recipe action](../../README.md#runnable-recipes):

```sh
go run . export > inventory.jsonl
```

Check the exit status before treating the file as complete. The starter has a five-minute overall deadline; adjust it for long-running integrations.

Offline verification from the repository root (Python 3.10+ for the fixture runner):

```sh
python3 scripts/test-starter.py go
```

Copy this folder to start your own integration and change the `example.com/seventhings-quickstart` module path. See [Go guidance](../../context/languages/go.md) and [local SDK overrides](../../CONTRIBUTING.md).
