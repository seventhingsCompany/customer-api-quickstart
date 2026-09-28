"""Generate the pinned API schema and a compact, versioned endpoint index."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkout",
        type=Path,
        help="Local docs Git checkout; reads the pinned committed revision, not working files",
    )
    parser.add_argument(
        "--revision",
        help="New full Git commit SHA; updates the manifest after successful regeneration",
    )
    args = parser.parse_args()
    manifest_path = ROOT / "sdk-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    reference = manifest["reference"]
    if args.revision:
        if not re.fullmatch(r"[0-9a-f]{40}", args.revision):
            raise SystemExit("--revision must be a full 40-character lowercase Git commit SHA")
        reference["revision"] = args.revision
    repository = reference["repository"].removeprefix("https://github.com/").removesuffix(".git")
    url = f"https://raw.githubusercontent.com/{repository}/{reference['revision']}/{reference['path']}"
    if args.checkout:
        raw = subprocess.check_output(
            ["git", "show", f"{reference['revision']}:{reference['path']}"], cwd=args.checkout
        )
    else:
        with urlopen(url, timeout=30) as response:
            raw = response.read()
    schema = json.loads(raw)
    if "openapi" not in schema or "paths" not in schema:
        raise SystemExit("Source is not an OpenAPI document")
    endpoints = []
    for path, methods in sorted(schema["paths"].items()):
        for method, operation in sorted(methods.items()):
            if method not in {"get", "post", "put", "patch", "delete", "head", "options", "trace"}:
                continue
            endpoints.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "summary": operation.get("summary", ""),
                    "operationId": operation.get("operationId", ""),
                    "tags": operation.get("tags", []),
                }
            )
    result = {
        "source": url,
        "revision": reference["revision"],
        "sha256": hashlib.sha256(raw).hexdigest(),
        "info": schema["info"],
        "endpoints": endpoints,
    }
    (ROOT / "reference/endpoints.json").write_text(json.dumps(result, indent=2) + "\n")
    (ROOT / "reference/customer-api.json").write_bytes(raw)
    if args.revision:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Indexed {len(endpoints)} operations from {reference['revision']}")


if __name__ == "__main__":
    main()
