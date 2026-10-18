# Go

Read `starters/go/main.go`. Module import paths use `github.com/SeventhingsCompany/customer-api-go/client` and `/models` (note capitalization). Go 1.25+.

- Construct with `client.NewWithToken` or `client.NewWithCredentials`.
- Every request uses a context. The starter applies a five-minute overall deadline; choose a task-appropriate deadline for larger exports; the default rate limit spaces requests 300 ms apart.
- `client.WithRateLimit(n)` sets requests per minute (default `client.DefaultRequestsPerMinute`, 200; zero disables). `*models.APIError` exposes `Header` and `RetryAfter(time.Now())`.
- `ObjectsList` returns a slice; `ObjectsAll` is an iterator yielding `(models.Fields, error)`. Check every yielded error.
- `FieldDefinitionsList(ctx, "asset")` discovers fields.
- `ObjectPatch` returns only an error in the pinned release.
- Attachment responses expose `StatusCode` and a raw `Body`.
- OAuth authorization-code/PKCE login is not available; it was briefly added in 1.5.0 and removed in 1.5.1.

Checks: `go vet ./...`, `go test ./...`, and the shared offline suite. Run: `go run . <action>`. Set your own module path when copying the starter into a new project.
