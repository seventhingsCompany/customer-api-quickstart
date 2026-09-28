"""Run a Customer API recipe; configuration is read from the environment."""

import dataclasses
import json
import os
import sys
from pathlib import Path

from seventhings import Client
from seventhings.models import FileAttachment, HistoryListOptions, ListOptions, like


def required(key):
    value = os.environ.get(key)
    if not value:
        raise ValueError(f"Set {key}")
    return value


def output(value):
    def encode(obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        raise TypeError(f"Cannot serialize {type(obj).__name__}")

    print(json.dumps(value, default=encode))


def run(client, action):
    options = ListOptions(page=1, per_page=100)
    if os.environ.get("SEVENTHINGS_FILTER_FIELD"):
        options = options.where(
            like(required("SEVENTHINGS_FILTER_FIELD"), required("SEVENTHINGS_FILTER_VALUE"))
        )
    if action == "hello":
        output(
            {
                "ping": client.ping(),
                "fieldDefinitions": client.field_definitions.list("asset"),
                "objects": client.objects.list(options),
            }
        )
    elif action == "export":
        for obj in client.objects.all(options):
            output(dict(obj))
    elif action == "lookup":
        output(client.objects.get_by_barcode(required("SEVENTHINGS_BARCODE")))
    elif action in ("create", "update"):
        fields = json.loads(Path(required("SEVENTHINGS_PAYLOAD_FILE")).read_text())
        if not isinstance(fields, dict):
            raise ValueError("Payload must be a JSON object")
        if action == "create":
            missing = client.field_definitions.missing_mandatory_fields("asset", fields)
            if missing:
                raise ValueError(f"Missing required fields: {', '.join(missing)}")
            output({"uuid": client.objects.create(fields)})
        else:
            uuid = required("SEVENTHINGS_OBJECT_UUID")
            client.objects.patch(uuid, fields)
            output({"uuid": uuid, "updated": True})
    elif action == "attach":
        uuid = required("SEVENTHINGS_OBJECT_UUID")
        field = required("SEVENTHINGS_ATTACHMENT_FIELD")
        path = Path(required("SEVENTHINGS_FILE"))
        with path.open("rb") as stream:
            file_uuid = client.files.upload(path.name, stream)
        result = client.objects.add_files(uuid, [FileAttachment(field, file_uuid)])
        output({"fileUuid": file_uuid, "status": result.status_code, "body": result.json()})
        if result.status_code == 207:
            raise ValueError("Partial attachment result; inspect output before retrying")
    elif action == "history":
        uuid = required("SEVENTHINGS_OBJECT_UUID")
        page = 1
        while True:
            result = client.objects.history(uuid, HistoryListOptions(page=page, per_page=100))
            for item in result.items:
                output(item)
            if result.page * result.per_page >= result.total or not result.items:
                break
            page += 1


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "hello"
    if action not in ("hello", "export", "lookup", "create", "update", "attach", "history"):
        raise ValueError("Use hello, export, lookup, create, update, attach, or history")
    url = required("SEVENTHINGS_INSTANCE_URL")
    token = os.environ.get("SEVENTHINGS_TOKEN")
    client = (
        Client(url, token=token)
        if token
        else Client.with_credentials(
            url,
            required("SEVENTHINGS_USERNAME"),
            required("SEVENTHINGS_PASSWORD"),
            required("SEVENTHINGS_CLIENT_ID"),
        )
    )
    with client:
        run(client, action)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
