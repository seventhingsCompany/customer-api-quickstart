# seventhings Customer API quickstart

Build an integration with the **TypeScript, Python, Go, or PHP SDK**, with runnable examples and context for your AI coding tool.

## Choose your SDK

**Prefer the language your team already uses.** For a new project, choose based on the integration you want to build and maintain.

| Your situation | Good starting choice | Why |
| --- | --- | --- |
| Data exports, reporting, data cleanup, exploratory scripts | **Python** | Strong data-processing ecosystem and quick iteration |
| Web applications, dashboards, Node.js backends | **TypeScript** | Fits web stacks and provides compile-time feedback |
| Standalone CLI tools, scheduled services, deployable integration binaries | **Go** | Straightforward binary deployment and explicit concurrency |
| Existing Laravel, Symfony, or other PHP applications | **PHP** | Integrates naturally into the application you already maintain |

These are starting points, not exclusive capabilities: all four SDKs cover the same API areas, and all four languages can run scheduled integrations. For example, keep a nightly export in PHP if your existing Laravel application already handles scheduling and deployment.

With no existing stack, **Python is a reasonable default for a small script**, and **TypeScript is a reasonable default for a web-oriented project**. Check the runtime requirements below, the libraries you need, where the integration will run, and who will maintain it. For a dashboard, a TypeScript frontend can work with a backend in any of these languages; service credentials belong on the backend.

AI coding tools can help with every language, but your team still needs to understand, test, and maintain the result. Describe your goal, existing stack, hosting environment, and team experience when asking an AI to recommend a starter.

Read the [full language selection guide](https://api.seventhings.com/guides/sdks/choosing-a-language/) for tradeoffs and examples, then follow your selected starter below.

## Start here

1. Clone this repository and open it in your editor or AI coding tool.
2. Choose a starter using the [guide above](#choose-your-sdk). You only need that language's runtime and package manager.

| Language | Requirements | Setup and run |
| --- | --- | --- |
| [TypeScript](starters/typescript/README.md) | Node.js 22+, npm | `npm ci && npm run build && npm start -- hello` |
| [Python](starters/python/README.md) | Python 3.10+ | Create a virtual environment, install `requirements.txt`, run `python main.py hello` |
| [Go](starters/go/README.md) | Go 1.25+ | `go run . hello` |
| [PHP](starters/php/README.md) | PHP 8.5+, Composer 2 | `composer install && php main.php hello` |

Run these commands **inside the selected starter directory** after configuring your environment.

3. Copy [`.env.example`](.env.example) to `.env` in the repository root. Set your instance URL and either a token or username, password, and client ID. The URL is the instance root, without `/customer-api/v1`.
4. Export the variables into your terminal. The programs read environment variables; they do not automatically load `.env`.

```sh
# POSIX shells, from the repository root. Quote values containing spaces or shell characters.
set -a
. ./.env
set +a
```

In PowerShell use `$env:SEVENTHINGS_INSTANCE_URL = 'https://your-instance.seventhings.com'` and set the authentication variables the same way.

5. Run `hello` using the selected starter's instructions. It prints JSON containing a ping result, your instance's asset field definitions, and up to 100 objects. An empty object list is a valid result.

## Build with AI

Open this repository and ask:

> Read AGENTS.md. Use the Python starter to export all inventory objects matching my filter as JSON Lines. Discover my instance's field keys rather than guessing them. Explain how to configure and run the integration, and run the offline checks.

Replace the language and goal as needed. [AGENTS.md](AGENTS.md) routes the agent to the relevant context and tested code. [CLAUDE.md](CLAUDE.md) and the [Copilot instructions](.github/copilot-instructions.md) point to the same source.

## Runnable recipes

All four starters accept the same action names and environment variables:

| Action | Purpose | Additional inputs |
| --- | --- | --- |
| `hello` | Connectivity, field discovery, one page of objects | Optional filter pair |
| `export` | [Export all matching objects](recipes/export-inventory.md) as JSON Lines | Optional filter pair |
| `lookup` | [Find by raw barcode](recipes/find-by-barcode.md) | `SEVENTHINGS_BARCODE` |
| `create` / `update` | [Create or patch an object](recipes/create-or-update.md) | `SEVENTHINGS_PAYLOAD_FILE`; UUID for update |
| `attach` | [Upload and attach a file](recipes/attach-file.md) | UUID, `SEVENTHINGS_FILE`, `SEVENTHINGS_ATTACHMENT_FIELD` |
| `history` | [Read all object history](recipes/change-history.md) as JSON Lines | `SEVENTHINGS_OBJECT_UUID` |

Filter pair: `SEVENTHINGS_FILTER_FIELD` and `SEVENTHINGS_FILTER_VALUE` (substring matching). Paths are relative to your current directory. `create`, `update`, and `attach` perform writes; `hello` performs reads. Commands return nonzero on failure, including partial attachment responses.

## Make it your own

Copy the selected starter into your integration project, adapt its entry point, and keep its dependency manifest and lockfile. Copy the relevant context with it if you want AI guidance outside this repository. Use your own application name and module path. Runtime credentials stay in environment variables; `.env` is ignored by Git. Examples are [MIT licensed](LICENSE); include the license when copying them.

## Development and maintenance

- [Internal workspace and local SDK overrides](CONTRIBUTING.md)
- [Troubleshooting](context/troubleshooting.md)
- [Offline verification and AI evaluation](evals/README.md)
- [SDK versions and source revisions](sdk-manifest.json)
- [API reference provenance](reference/README.md)

The SDKs retain independent release cycles. This repository pins a known dependency set; CI exercises the released packages against an offline HTTP fixture. Live smoke checks run by executing `hello` with your own test-instance configuration.
