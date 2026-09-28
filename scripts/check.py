"""Check local documentation links, reference provenance, and SDK version consistency."""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"node_modules", ".venv", "vendor", ".workspace", ".git", "dist"}


def main():
    manifest = json.loads((ROOT / "sdk-manifest.json").read_text())
    for language, sdk in manifest["sdks"].items():
        starter = ROOT / sdk["starter"]
        assert (starter / "README.md").is_file(), f"Missing {language} README"
        assert re.fullmatch(r"[0-9a-f]{40}", sdk["revision"]), f"Invalid {language} revision"
        version = sdk["version"]
        if language == "typescript":
            assert (
                json.loads((starter / "package.json").read_text())["dependencies"][sdk["package"]]
                == version
            )
            assert (
                json.loads((starter / "package-lock.json").read_text())["packages"][
                    f"node_modules/{sdk['package']}"
                ]["version"]
                == version
            )
        elif language == "python":
            for name in ["requirements.in", "requirements.txt"]:
                assert f"{sdk['package']}=={version}" in (starter / name).read_text()
        elif language == "go":
            assert f"{sdk['package']} v{version}" in (starter / "go.mod").read_text()
        elif language == "php":
            assert (
                json.loads((starter / "composer.json").read_text())["require"][sdk["package"]]
                == version
            )
            packages = json.loads((starter / "composer.lock").read_text())["packages"]
            assert (
                next(p for p in packages if p["name"] == sdk["package"])["version"].lstrip("v")
                == version
            )
    index = json.loads((ROOT / "reference/endpoints.json").read_text())
    assert index["revision"] == manifest["reference"]["revision"]
    assert (
        index["sha256"]
        == hashlib.sha256((ROOT / "reference/customer-api.json").read_bytes()).hexdigest()
    )
    count = 0
    for document in ROOT.rglob("*.md"):
        if EXCLUDED.intersection(document.relative_to(ROOT).parts):
            continue
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", document.read_text()):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            path = target.split("#", 1)[0]
            assert (document.parent / path).exists(), (
                f"Broken link: {document.relative_to(ROOT)} -> {target}"
            )
            count += 1
    print(f"Manifest, locks, reference checksum, and {count} local links passed")


if __name__ == "__main__":
    main()
