# Go

Read `starters/go/main.go`. Module import paths use `github.com/SeventhingsCompany/customer-api-go/client` and `/models` (note capitalization). Go 1.25+.

- Construct with `client.NewWithToken` or `client.NewWithCredentials`.
- Every request uses a context. The starter applies a five-minute overall deadline; choose a task-appropriate deadline for larger exports.
- `ObjectsList` returns a slice; `ObjectsAll` is an iterator yielding `(models.Fields, error)`. Check every yielded error.
- `FieldDefinitionsList(ctx, "asset")` discovers fields.
- `ObjectPatch` returns only an error in the pinned release.
- Attachment responses expose `StatusCode` and a raw `Body`.

Checks: `go vet ./...`, `go test ./...`, and the shared offline suite. Run: `go run . <action>`. Set your own module path when copying the starter into a new project.
