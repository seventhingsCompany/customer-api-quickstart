# PHP

Read `starters/php/main.php`. Package: `seventhings/customer-api-php` on Packagist. PHP 8.5+, Composer 2, Guzzle 7 through the SDK.

- Construct with `Client::withToken` or `Client::withCredentials`.
- Ping lives on `$client->auth`, unlike the other starters.
- `$client->objects->list($options)` returns arrays; `all($options)` yields `Fields` with public `data`.
- Use `AssetTrackingTemplate::Asset` for field definitions.
- Use `FilterEntry::like` and named `ListOptions` arguments.
- Attachment responses expose `statusCode` and `json()`.

Checks: `composer validate --no-check-publish`, `composer check`, and the shared offline suite. Run: `php main.php <action>`. Install with `composer install`; no GitHub SSH repository entry is needed.
