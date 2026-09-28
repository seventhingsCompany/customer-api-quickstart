"""Black-box checks against a local HTTP fixture, using each real SDK package."""

import argparse
import json
import os
import subprocess
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OBJECT_UUID = "00000000-0000-4000-8000-000000000001"
FILE_UUID = "00000000-0000-4000-8000-000000000002"
OBJECTS = [
    {"uuid": f"object-{i}", "custom_label": f"Laptop {i}", "custom_nested": {"active": True}}
    for i in range(101)
]
DEFINITIONS = [
    {
        "uuid": "field-1",
        "field_key": "custom_label",
        "field_type": {"name": "TEXT", "constraints": []},
        "label": "Custom label",
        "attributes": [{"type": "mandatory", "value": "yes"}],
        "relations": [],
    }
]


class Fixture(BaseHTTPRequestHandler):
    requests = []
    partial = False
    unauthorized = False

    def log_message(self, *args):
        pass

    def reply(self, body, status=200, headers=None):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data)

    def dispatch(self):
        url = urlsplit(self.path)
        query = parse_qs(url.query)
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        self.requests.append((self.command, url.path, query, body))
        prefix = "/customer-api/v1"
        path = url.path.removeprefix(prefix)
        if not url.path.startswith(prefix):
            return self.reply({"error": "Wrong API prefix"}, 404)
        if path == "/auth_token" and self.command == "POST":
            credentials = json.loads(body)
            if credentials != {
                "grant_type": "password",
                "username": "fixture-user",
                "password": "fixture-password",
                "client_id": "fixture-client",
            }:
                return self.reply({"error": "Wrong credentials"}, 401)
            return self.reply(
                {
                    "access_token": "fixture-token",
                    "refresh_token": "fixture-refresh",
                    "expires_in": 3600,
                    "token_type": "Bearer",
                    "user_id": 1,
                }
            )
        if path.rstrip("/") == "":
            return self.reply({"status": "ok", "description": "fixture"})
        if self.unauthorized or self.headers.get("Authorization") != "Bearer fixture-token":
            return self.reply({"error": "Unauthorized"}, 401)
        if self.command == "GET":
            if path == "/asset-tracking/asset/field-definitions":
                return self.reply(DEFINITIONS)
            if path == "/objects":
                page = int(query.get("page", [1])[0])
                size = int(query.get("per_page", [100])[0])
                return self.reply(
                    {
                        "items": OBJECTS[(page - 1) * size : page * size],
                        "page": page,
                        "per_page": size,
                        "total": len(OBJECTS),
                    }
                )
            if path == "/object/by-barcode/INV%2F001":
                return self.reply(OBJECTS[0])
            if path == f"/object/{OBJECT_UUID}/history":
                page = int(query.get("page", [1])[0])
                size = int(query.get("per_page", [100])[0])
                return self.reply(
                    {
                        "items": OBJECTS[(page - 1) * size : page * size],
                        "page": page,
                        "per_page": size,
                        "total": len(OBJECTS),
                    }
                )
        if self.command == "POST":
            if path == "/object":
                return self.reply({}, 201, {"Location": f"{prefix}/object/{OBJECT_UUID}"})
            if path == "/file" and b"fixture upload" in body and b'name="data"' in body:
                return self.reply(
                    {},
                    201,
                    {"Location-UUID": FILE_UUID, "Location": f"{prefix}/file/{FILE_UUID}/data"},
                )
            if path == f"/object/{OBJECT_UUID}/add-file":
                return self.reply(
                    {"results": [{"status": 400 if self.partial else 200}]},
                    207 if self.partial else 200,
                )
        if self.command == "PATCH" and path == f"/object/{OBJECT_UUID}":
            return self.reply({"uuid": OBJECT_UUID, **json.loads(body)})
        return self.reply({"error": f"Unhandled fixture request: {self.command} {path}"}, 404)

    do_GET = dispatch
    do_POST = dispatch
    do_PATCH = dispatch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("language", choices=["typescript", "python", "go", "php"])
    parser.add_argument("--python", help="Python interpreter containing the installed SDK")
    parser.add_argument("--php", default="php", help="PHP executable")
    args = parser.parse_args()
    starter = ROOT / "starters" / args.language
    with tempfile.TemporaryDirectory(prefix="customer-api-") as temporary:
        temp = Path(temporary)
        python = args.python or str(
            ROOT
            / "starters/python/.venv"
            / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        )
        commands = {
            "typescript": ["node", "dist/main.js"],
            "python": [python, "main.py"],
            "php": [args.php, "main.php"],
        }
        if args.language == "go":
            binary = str(temp / ("starter.exe" if os.name == "nt" else "starter"))
            subprocess.run(["go", "build", "-o", binary, "."], cwd=starter, check=True)
            commands["go"] = [binary]
        payload = temp / "payload.json"
        payload.write_text(json.dumps({"custom_label": "Created from fixture"}))
        upload = temp / "upload.txt"
        upload.write_text("fixture upload")
        env = {
            key: value for key, value in os.environ.items() if not key.startswith("SEVENTHINGS_")
        }
        server = ThreadingHTTPServer(("127.0.0.1", 0), Fixture)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        env.update(
            {
                "SEVENTHINGS_INSTANCE_URL": f"http://127.0.0.1:{server.server_port}",
                "SEVENTHINGS_TOKEN": "fixture-token",
                "SEVENTHINGS_OBJECT_UUID": OBJECT_UUID,
                "SEVENTHINGS_BARCODE": "INV/001",
                "SEVENTHINGS_PAYLOAD_FILE": str(payload),
                "SEVENTHINGS_FILE": str(upload),
                "SEVENTHINGS_ATTACHMENT_FIELD": "custom_documents",
                "NO_PROXY": "127.0.0.1,localhost",
                "no_proxy": "127.0.0.1,localhost",
            }
        )

        def run(action, success=True, overrides=None):
            Fixture.requests.clear()
            result = subprocess.run(
                commands[args.language] + [action],
                cwd=starter,
                env={**env, **(overrides or {})},
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
            assert (result.returncode == 0) == success, (
                f"{action}: exit {result.returncode}\n{result.stdout}\n{result.stderr}"
            )
            assert "fixture-password" not in result.stdout + result.stderr, "Password leaked"
            if not success:
                assert result.stderr.strip(), f"{action}: missing error diagnostic"
            return [json.loads(line) for line in result.stdout.splitlines() if line.strip()]

        try:
            hello = run("hello")[0]
            assert len(hello["objects"]) == 100 and len(hello["fieldDefinitions"]) == 1
            run(
                "hello",
                overrides={
                    "SEVENTHINGS_TOKEN": "",
                    "SEVENTHINGS_USERNAME": "fixture-user",
                    "SEVENTHINGS_PASSWORD": "fixture-password",
                    "SEVENTHINGS_CLIENT_ID": "fixture-client",
                },
            )
            assert Fixture.requests[0][1].endswith("/auth_token")
            assert (
                run(
                    "export",
                    overrides={
                        "SEVENTHINGS_FILTER_FIELD": "custom_label",
                        "SEVENTHINGS_FILTER_VALUE": "Laptop",
                    },
                )
                == OBJECTS
            )
            queries = [r[2] for r in Fixture.requests if r[1].endswith("/objects")]
            assert [q["page"] for q in queries] == [["1"], ["2"]]
            assert all(
                "custom_label" in json.dumps(q)
                and "Laptop" in json.dumps(q)
                and "like" in json.dumps(q)
                for q in queries
            )
            assert run("lookup") == [OBJECTS[0]]
            run("lookup", False, {"SEVENTHINGS_BARCODE": "missing"})
            assert run("create") == [{"uuid": OBJECT_UUID}]
            created = [r for r in Fixture.requests if r[0] == "POST"]
            assert json.loads(created[0][3]) == {"custom_label": "Created from fixture"}
            payload.write_text('{"custom_optional": "x"}')
            run("create", False)
            assert not any(r[0] == "POST" for r in Fixture.requests), (
                "Created despite missing mandatory fields"
            )
            assert run("update") == [{"uuid": OBJECT_UUID, "updated": True}]
            assert json.loads(Fixture.requests[-1][3]) == {"custom_optional": "x"}
            payload.write_text("[]")
            run("create", False)
            assert not any(r[0] == "POST" for r in Fixture.requests)
            attachment = run("attach")[0]
            assert attachment["status"] == 200 and attachment["fileUuid"] == FILE_UUID
            assert json.loads(Fixture.requests[-1][3]) == [
                {"field-key": "custom_documents", "file-uuid": FILE_UUID}
            ]
            Fixture.partial = True
            assert run("attach", False)[0]["status"] == 207
            Fixture.partial = False
            assert run("history") == OBJECTS
            assert len(Fixture.requests) == 2
            Fixture.unauthorized = True
            run("export", False)
            Fixture.unauthorized = False
            run("hello", False, {"SEVENTHINGS_INSTANCE_URL": ""})
            assert not Fixture.requests
            run("unknown", False)
            assert not Fixture.requests
            print(
                f"{args.language}: offline contract checks passed (auth, paging, filtering, lookup, writes, uploads, partial results, errors)"
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    main()
