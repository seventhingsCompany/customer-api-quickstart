"""Update an SDK pin, source revision, and lockfile together (requires its toolchain)."""

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def main():
    path = ROOT / "sdk-manifest.json"
    manifest = json.loads(path.read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("language", choices=list(manifest["sdks"]))
    parser.add_argument("version", help="Stable version, e.g. 1.4.0, or latest")
    args = parser.parse_args()
    sdk = manifest["sdks"][args.language]
    tags = subprocess.check_output(["git", "ls-remote", "--tags", sdk["repository"]], text=True)
    revisions = {}
    for line in tags.splitlines():
        revision, ref = line.split()
        match = re.fullmatch(r"refs/tags/v?(\d+\.\d+\.\d+)(\^\{\})?", ref)
        if match:
            version = match[1]
            if version not in revisions or match[2]:
                revisions[version] = revision
    version = (
        max(revisions, key=lambda v: tuple(map(int, v.split("."))))
        if args.version == "latest"
        else args.version.removeprefix("v")
    )
    if version not in revisions:
        raise SystemExit(f"No stable release tag found for {version}")
    if version == sdk["version"] and revisions[version] == sdk["revision"]:
        print(f"{args.language}: already at {version}")
        return
    old_version = sdk["version"]
    starter = ROOT / sdk["starter"]
    if args.language == "typescript":
        package = starter / "package.json"
        data = json.loads(package.read_text())
        data["dependencies"][sdk["package"]] = version
        write_json(package, data)
        command = ["npm", "install", "--package-lock-only", "--ignore-scripts"]
    elif args.language == "python":
        (starter / "requirements.in").write_text(f"{sdk['package']}=={version}\n")
        command = [
            "uv",
            "pip",
            "compile",
            "requirements.in",
            "--python-version",
            "3.10",
            "--universal",
            "--generate-hashes",
            "--output-file",
            "requirements.txt",
        ]
    elif args.language == "go":
        module = starter / "go.mod"
        module.write_text(
            module.read_text().replace(
                f"{sdk['package']} v{old_version}", f"{sdk['package']} v{version}"
            )
        )
        command = ["go", "mod", "tidy"]
    else:
        package = starter / "composer.json"
        data = json.loads(package.read_text())
        data["require"][sdk["package"]] = version
        write_json(package, data)
        command = [
            "composer",
            "update",
            sdk["package"],
            "--with-all-dependencies",
            "--no-interaction",
        ]
    subprocess.run(command, cwd=starter, check=True)
    sdk.update(version=version, revision=revisions[version])
    write_json(path, manifest)
    print(f"{args.language}: {old_version} -> {version}. Run the starter checks before merging.")


if __name__ == "__main__":
    main()
