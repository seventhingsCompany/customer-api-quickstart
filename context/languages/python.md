# Python

Read `starters/python/main.py`. Distribution: `seventhings-customer-api`; import: `seventhings`. Python 3.10+.

- The starter uses synchronous `Client` as a context manager to close connections.
- `client.objects.list(options)` returns dictionaries; `all(options)` yields dictionary-like `Fields`.
- Use `ListOptions(...).where(like(field, value))`; option names use `per_page`.
- `client.field_definitions.list('asset')` returns dataclasses.
- Attachment responses expose `status_code` and `json()`.
- For async applications use `AsyncClient`, `await` SDK calls, and `async for` on iterators; do not mix sync network calls into an async request handler.

Install `requirements.txt` in a virtual environment. Compile check: `python -m compileall -q main.py`. Run: `python main.py <action>`. Use the shared offline suite for actual request/response verification.
