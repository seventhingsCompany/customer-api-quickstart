# Troubleshooting

| Symptom | Check |
| --- | --- |
| `Set SEVENTHINGS_...` | Export the variable in the same shell used to run the command; `.env` is not auto-loaded. |
| Login failure / 401 | Instance URL, token expiry, username/password, and assigned client ID. |
| 403 | Account permissions for the requested resource/action. |
| 404 on every endpoint | Use the instance root, without a duplicated `/customer-api/v1`. |
| Barcode not found | Pass the raw barcode; lookup includes archived objects. Treat a missing object separately from auth/network failures in application logic. |
| Missing required fields / validation error | Fetch that instance's field definitions; verify field keys, values, and constraints. |
| Only 100 exported rows | Use `export`, not `hello`; `hello` intentionally fetches one page. |
| Attachment exits nonzero with status 207 | Inspect the printed result, then rerun `attach` with `SEVENTHINGS_FILE_UUID` set to the printed `fileUuid` to repair the link without uploading again. |
| `lookup` exits 3 | No object has that barcode (archived objects included). Exit 1 means an authentication, network, or other API error. |
| `Set SEVENTHINGS_FILTER_...` | Set both filter variables, or clear both to export everything. |
| 429 Too Many Requests | Another client or process is using the same instance. Read the error's Retry-After value, wait, and resend only idempotent reads automatically. Lower the client's rate limit for concurrent jobs. |
| Export or batch slower than expected | The SDK paces requests at 200 per minute by default. Allow time for the page count, and extend task deadlines (the Go starter uses five minutes). |
| PHP platform requirement failure | Use PHP 8.5+; the pinned SDK requires it. It is available through Packagist. |
| Go method differs from a README snippet | Follow the installed SDK version and compiled starter; return types can differ from older snippets. |
| Export stops early with an error | stdout may contain a partial export. Check the exit status before consuming it as a complete snapshot. |

Errors are sent to stderr; stdout is JSON or JSON Lines. When reporting failures, include the language, pinned version, action, HTTP status, and a redacted error. Avoid attaching full customer exports or credentials.
