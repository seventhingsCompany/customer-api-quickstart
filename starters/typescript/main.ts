import { readFile } from 'node:fs/promises';
import { basename } from 'node:path';
import { SeventhingsClient, Filter, type ListOptions } from '@seventhingscompany/customer-api';

function required(key: string): string {
  const value = process.env[key];
  if (!value) throw new Error(`Set ${key}`);
  return value;
}
const output = (value: unknown) => console.log(JSON.stringify(value));

async function main() {
  const action = process.argv[2] ?? 'hello';
  if (!['hello', 'export', 'lookup', 'create', 'update', 'attach', 'history'].includes(action)) {
    throw new Error('Use hello, export, lookup, create, update, attach, or history');
  }
  const instanceUrl = required('SEVENTHINGS_INSTANCE_URL');
  const token = process.env.SEVENTHINGS_TOKEN;
  const client = token
    ? new SeventhingsClient({ instanceUrl, token })
    : await SeventhingsClient.withCredentials({ instanceUrl, username: required('SEVENTHINGS_USERNAME'), password: required('SEVENTHINGS_PASSWORD'), clientId: required('SEVENTHINGS_CLIENT_ID') });
  const options: ListOptions = { page: 1, perPage: 100 };
  if (process.env.SEVENTHINGS_FILTER_FIELD) {
    options.filters = [Filter.like(required('SEVENTHINGS_FILTER_FIELD'), required('SEVENTHINGS_FILTER_VALUE'))];
  }
  switch (action) {
    case 'hello':
      output({ ping: await client.ping(), fieldDefinitions: await client.fieldDefinitions.list('asset'), objects: await client.objects.list(options) });
      break;
    case 'export':
      for await (const obj of client.objects.all(options)) output(obj.data);
      break;
    case 'lookup': output(await client.objects.getByBarcode(required('SEVENTHINGS_BARCODE'))); break;
    case 'create':
    case 'update': {
      const fields: unknown = JSON.parse(await readFile(required('SEVENTHINGS_PAYLOAD_FILE'), 'utf8'));
      if (!fields || typeof fields !== 'object' || Array.isArray(fields)) throw new Error('Payload must be a JSON object');
      const record = fields as Record<string, unknown>;
      if (action === 'create') {
        const missing = await client.fieldDefinitions.missingMandatoryFields('asset', record);
        if (missing.length) throw new Error(`Missing required fields: ${missing.join(', ')}`);
        output({ uuid: await client.objects.create(record) });
      } else {
        const uuid = required('SEVENTHINGS_OBJECT_UUID');
        await client.objects.patch(uuid, record);
        output({ uuid, updated: true });
      }
      break;
    }
    case 'attach': {
      const uuid = required('SEVENTHINGS_OBJECT_UUID');
      const fieldKey = required('SEVENTHINGS_ATTACHMENT_FIELD');
      const path = required('SEVENTHINGS_FILE');
      const fileUuid = await client.files.upload(basename(path), await readFile(path));
      const result = await client.objects.addFiles(uuid, [{ fieldKey, fileUuid }]);
      output({ fileUuid, ...result });
      if (result.status === 207) throw new Error('Partial attachment result; inspect output before retrying');
      break;
    }
    case 'history': {
      const uuid = required('SEVENTHINGS_OBJECT_UUID');
      for (let page = 1; ; page++) {
        const result = await client.objects.history(uuid, { page, perPage: 100 });
        for (const item of result.items) output(item);
        if (result.page * result.perPage >= result.total || !result.items.length) break;
      }
    }
  }
}
main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
