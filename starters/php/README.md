# PHP starter

Requires PHP 8.5+ and Composer 2. First configure and export the variables from the root [environment template](../../.env.example), following the [root instructions](../../README.md).

From this directory:

```sh
composer install
composer validate --no-check-publish
composer check
php main.php hello
```

The SDK is installed from Packagist. Expected output: one JSON object with `ping`, `fieldDefinitions`, and `objects` (up to 100 records). An empty inventory is valid.

Replace `hello` with any [recipe action](../../README.md#runnable-recipes):

```sh
php main.php export > inventory.jsonl
```

Check the exit status before treating the file as complete. Offline verification from the repository root (Python 3.10+ for the fixture runner):

```sh
python3 scripts/test-starter.py php
```

Copy this folder to start your own integration. Edit `main.php`, give your project its own Composer package name, and keep the lockfile. See [PHP guidance](../../context/languages/php.md) and [local SDK overrides](../../CONTRIBUTING.md).
