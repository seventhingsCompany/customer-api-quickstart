# Maintaining the quickstart

## Ownership and release process

The Customer API SDK maintainers own this repository's version manifest, starters, and recipes. Changes to a recipe require review by a maintainer familiar with each affected language. API documentation maintainers own reference provenance and schema updates. Repository administrators should assign these responsibilities to the actual GitHub users/teams when publishing the repository.

For an SDK release:

1. Publish the SDK package and source tag.
2. Update the pin and source revision together using the command below. Inspect runtime requirements and interface changes.
3. Run the affected starter checks, the shared offline suite, and `scripts/check.py`.
4. Run relevant [AI onboarding evaluations](evals/README.md) when interfaces/instructions change.
5. Merge the reviewed update. CI verifies the dependency set; customers receive it on their next quickstart update.

```sh
python3 scripts/update-sdk.py typescript 1.4.0
# Or discover the newest stable source tag:
python3 scripts/update-sdk.py python latest
```

The selected package manager must be installed. Python lock regeneration requires `uv`; customer execution only requires Python/pip. Scheduled automation runs these updates and opens a single reviewed PR. GitHub's “Allow GitHub Actions to create and approve pull requests” setting must permit PR creation. Bot-created PRs may not trigger a separate workflow with the default token, so the update workflow runs the complete offline checks before creating the PR. Failed updates are not published as PRs.

## Optional SDK source workspace

Customers normally install released packages. Internal SDK development can fetch only the relevant sources:

```sh
python3 scripts/workspace.py typescript python
```

Sources appear in ignored `.workspace/<language>` at the manifest's exact revision, detached. The command refuses to overwrite existing directories. Create a branch in the selected SDK before editing it. SDK changes belong in the SDK repository; quickstart examples/instructions belong here.

### Local overrides

From `starters/typescript`, after building `.workspace/typescript` with `npm ci && npm run build` inside that SDK:

```sh
npm install --no-save --package-lock=false ../../.workspace/typescript
```

Restore released dependencies with `npm ci`.

From `starters/python`, in its active virtual environment:

```sh
python -m pip install -e ../../.workspace/python
```

Restore with `python -m pip install --force-reinstall --require-hashes -r requirements.txt`.

From `starters/go`:

```sh
go mod edit -replace=github.com/SeventhingsCompany/customer-api-go=../../.workspace/go
```

Restore with `go mod edit -dropreplace=github.com/SeventhingsCompany/customer-api-go` and `go mod tidy`. Do not commit local replace directives.

From `starters/php`, make an ignored local Composer manifest and select it for the override:

```sh
cp composer.json composer.local.json
COMPOSER=composer.local.json composer config repositories.local path ../../.workspace/php
COMPOSER=composer.local.json composer require 'seventhings/customer-api-php:@dev' --with-all-dependencies
```

The local package's source version must satisfy the local manifest; use Composer's path repository `options.versions` if working from an untagged branch. The generated local manifest and lockfile are ignored. Restore released dependencies using `composer install` with the normal `composer.json`.

Run the affected offline suite with the override installed. Reinstall the released dependency before committing changes to the quickstart's lockfiles.

## Reference updates

Follow [reference/README.md](reference/README.md) to regenerate from a pinned docs commit. A manual reference-update workflow accepts the revision and creates a reviewed PR. If the documentation repository is private, configure `SDK_DOCS_READ_TOKEN` with read access to it. The committed schema means customers need no such token.

## Publishing checklist

- Publish this directory as `customer-api-quickstart` and enable its workflows.
- Enable the repository's template option if customers should use “Use this template”.
- Add the quickstart URL to the four SDK READMEs and the documentation site's getting-started/SDK navigation through their normal review process.
- Record the first fresh-clone authenticated-read timing and AI evaluation scores.

Package/runtime checks are automated. Live smoke tests and AI evaluations require an actual test-instance configuration and chosen AI tools; record those outcomes separately from fixture results.

Python tooling and the Python starter use Ruff (`uvx ruff@0.16.9 check scripts starters/python/main.py` and `uvx ruff@0.16.9 format --check scripts starters/python/main.py`). Go uses `gofmt`. Keep lockfiles committed and generated reference files byte-for-byte consistent with their recorded provenance.
