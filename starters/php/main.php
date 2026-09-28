<?php
declare(strict_types=1);

require __DIR__ . '/vendor/autoload.php';

use Seventhings\Client;
use Seventhings\Models\Enums\AssetTrackingTemplate;
use Seventhings\Models\FileAttachment;
use Seventhings\Models\FilterEntry;
use Seventhings\Models\HistoryListOptions;
use Seventhings\Models\ListOptions;

function required(string $key): string {
    $value = getenv($key);
    if ($value === false || $value === '') { throw new RuntimeException("Set $key"); }
    return $value;
}
function output(mixed $value): void {
    echo json_encode($value, JSON_THROW_ON_ERROR) . PHP_EOL;
}
function main(string $action): void {
    if (!in_array($action, ['hello', 'export', 'lookup', 'create', 'update', 'attach', 'history'], true)) {
        throw new RuntimeException('Use hello, export, lookup, create, update, attach, or history');
    }
    $url = required('SEVENTHINGS_INSTANCE_URL');
    $token = getenv('SEVENTHINGS_TOKEN');
    $client = $token ? Client::withToken($url, $token) : Client::withCredentials(
        $url, required('SEVENTHINGS_USERNAME'), required('SEVENTHINGS_PASSWORD'), required('SEVENTHINGS_CLIENT_ID')
    );
    $filters = getenv('SEVENTHINGS_FILTER_FIELD') ? [FilterEntry::like(required('SEVENTHINGS_FILTER_FIELD'), required('SEVENTHINGS_FILTER_VALUE'))] : [];
    $options = new ListOptions(page: 1, perPage: 100, filters: $filters);
    switch ($action) {
        case 'hello':
            output(['ping' => $client->auth->ping(), 'fieldDefinitions' => $client->fieldDefinitions->list(AssetTrackingTemplate::Asset), 'objects' => $client->objects->list($options)]);
            break;
        case 'export':
            foreach ($client->objects->all($options) as $object) { output($object->data); }
            break;
        case 'lookup': output($client->objects->getByBarcode(required('SEVENTHINGS_BARCODE'))); break;
        case 'create':
        case 'update':
            $data = file_get_contents(required('SEVENTHINGS_PAYLOAD_FILE'));
            if ($data === false) { throw new RuntimeException('Cannot read payload file'); }
            $decoded = json_decode($data, false, 512, JSON_THROW_ON_ERROR);
            if (!$decoded instanceof stdClass) { throw new RuntimeException('Payload must be a JSON object'); }
            $fields = (array) $decoded;
            if ($action === 'create') {
                $missing = $client->fieldDefinitions->missingMandatoryFields(AssetTrackingTemplate::Asset, $fields);
                if ($missing) { throw new RuntimeException('Missing required fields: ' . implode(', ', $missing)); }
                output(['uuid' => $client->objects->create($fields)]);
            } else {
                $uuid = required('SEVENTHINGS_OBJECT_UUID');
                $client->objects->patch($uuid, $fields);
                output(['uuid' => $uuid, 'updated' => true]);
            }
            break;
        case 'attach':
            $uuid = required('SEVENTHINGS_OBJECT_UUID');
            $field = required('SEVENTHINGS_ATTACHMENT_FIELD');
            $path = required('SEVENTHINGS_FILE');
            $stream = fopen($path, 'rb');
            if ($stream === false) { throw new RuntimeException('Cannot open upload file'); }
            try { $fileUuid = $client->files->upload(basename($path), $stream); }
            finally { if (is_resource($stream)) { fclose($stream); } }
            $result = $client->objects->addFiles($uuid, [new FileAttachment($field, $fileUuid)]);
            output(['fileUuid' => $fileUuid, 'status' => $result->statusCode, 'body' => $result->json()]);
            if ($result->statusCode === 207) { throw new RuntimeException('Partial attachment result; inspect output before retrying'); }
            break;
        case 'history':
            $uuid = required('SEVENTHINGS_OBJECT_UUID');
            for ($page = 1; ; $page++) {
                $result = $client->objects->history($uuid, new HistoryListOptions(page: $page, perPage: 100));
                foreach ($result->items as $item) { output($item); }
                if ($result->page * $result->perPage >= $result->total || !$result->items) { break; }
            }
    }
}
try { main($argv[1] ?? 'hello'); }
catch (Throwable $error) { fwrite(STDERR, $error->getMessage() . PHP_EOL); exit(1); }
