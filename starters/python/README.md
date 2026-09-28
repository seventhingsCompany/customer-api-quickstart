# Python starter

Requires Python 3.10+. First configure and export the variables from the root [environment template](../../.env.example), following the [root instructions](../../README.md).

From this directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --require-hashes -r requirements.txt
python -m compileall -q main.py
python main.py hello
```

Windows: use `py -m venv .venv` and `.venv\Scripts\Activate.ps1` in PowerShell.

Expected output: one JSON object with `ping`, `fieldDefinitions`, and `objects` (up to 100 records). An empty inventory is valid.

Replace `hello` with any [recipe action](../../README.md#runnable-recipes):

```sh
python main.py export > inventory.jsonl
```

Check the exit status before treating the file as complete. Offline verification from the repository root:

```sh
python3 scripts/test-starter.py python
# Or select an already configured interpreter:
python3 scripts/test-starter.py python --python /path/to/python
```

Copy this folder to start your own integration. Edit `main.py`. `requirements.in` pins the SDK; `requirements.txt` locks transitive dependencies and hashes for reproducible installs. See [Python guidance](../../context/languages/python.md) and [local SDK overrides](../../CONTRIBUTING.md).
