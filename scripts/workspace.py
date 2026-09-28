"""Fetch selected SDK source at the manifest revision into .workspace/."""

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "sdk-manifest.json").read_text())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("languages", nargs="+", choices=list(manifest["sdks"]))
    args = parser.parse_args()
    for language in args.languages:
        sdk = manifest["sdks"][language]
        destination = ROOT / ".workspace" / language
        if destination.exists():
            raise SystemExit(
                f"Already exists: {destination}. Reuse it or choose a new checkout manually; existing work is never reset."
            )
        destination.parent.mkdir(exist_ok=True)
        subprocess.run(
            ["git", "clone", "--no-checkout", sdk["repository"], str(destination)], check=True
        )
        subprocess.run(
            ["git", "checkout", "--detach", sdk["revision"]], cwd=destination, check=True
        )
        print(f"{language}: {destination} at {sdk['revision']}")


if __name__ == "__main__":
    main()
