# TypeScript

Read `starters/typescript/main.ts`. Package: `@seventhingscompany/customer-api`, pinned in `package.json` and `package-lock.json`. Node.js 22+; ESM and strict TypeScript.

- Construct `SeventhingsClient` with a token or await `withCredentials`.
- `client.objects.list(options)` returns records; `all(options)` is an async iterable of `Fields`. Export `field.data`.
- `Filter.like(field, value)` constructs a filter; options use `perPage`.
- `client.fieldDefinitions.list('asset')` returns definitions.
- `client.objects.history(uuid, options)` returns camelCase pagination fields.
- `client.objects.addFiles` returns `{status, body}`; inspect status 207.

Checks: `npm ci`, `npm run check`, `npm run build`. Run with `npm start -- <action>`; for clean JSON redirection use `node dist/main.js <action>`.

For additional methods inspect `node_modules/@seventhingscompany/customer-api/dist/index.d.ts` and the version-matched SDK README.
