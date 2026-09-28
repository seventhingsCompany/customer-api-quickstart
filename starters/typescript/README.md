# TypeScript starter

Requires Node.js 22+ and npm. First configure and export the variables from the root [environment template](../../.env.example), following the [root instructions](../../README.md).

From this directory:

```sh
npm ci
npm run check
npm run build
node dist/main.js hello
```

Expected output: one JSON object with `ping`, `fieldDefinitions`, and `objects` (up to 100 records). An empty inventory is valid.

Replace `hello` with any [recipe action](../../README.md#runnable-recipes). For example:

```sh
node dist/main.js export > inventory.jsonl
```

Check the exit status before treating a redirected file as complete. `npm start -- hello` also works, but use `node` directly when redirecting JSON output to avoid npm's command banner.

Offline verification from the repository root (Python 3.10+ for the fixture runner):

```sh
python3 scripts/test-starter.py typescript
```

Copy this folder to start your own integration. Edit `main.ts`, rebuild after changes, and keep the package lockfile. See [TypeScript guidance](../../context/languages/typescript.md) and [local SDK overrides](../../CONTRIBUTING.md).
