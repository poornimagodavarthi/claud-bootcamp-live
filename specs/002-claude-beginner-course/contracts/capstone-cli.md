# Contract — Capstone CLI (`notes.py`)

**Feature**: `002-claude-beginner-course`  
**Applies to**: `exercises/beginner/part-08/solution/notes.py` (reference) and every learner-built `notes.py`  
**Enforced by**: `scripts/check-beginner-capstone.sh` (FR-045)  
**Spec**: Clarifications Q3, FR-033

---

## Invocation

```text
python notes.py add <text>
python notes.py list
python notes.py delete <id>
```

`python` MUST refer to a Python 3.11+ interpreter. The script MUST work whether invoked as `python notes.py …` or `python3 notes.py …`.

## Subcommand contracts

### `add <text>`

- Takes exactly one positional argument: the note text (may contain spaces if the caller quoted it).
- Reads `./notes.json` if it exists; treats absence or empty file as an empty list.
- Assigns `id = max(existing_ids) + 1`, or `1` if the list is empty.
- Appends `{"id": <id>, "text": <text>}` to the list.
- Writes the list back to `./notes.json` as a JSON array (UTF-8, with a trailing newline).
- Prints exactly one line to stdout: `added: <id>` (e.g. `added: 1`).
- Exit code: `0`.

### `list`

- Reads `./notes.json` (empty list if missing).
- Prints one line per note to stdout in id order: `<id>\t<text>` (tab-separated).
- If the list is empty, prints nothing (no headers, no "no notes" message).
- Exit code: `0`.

### `delete <id>`

- Takes exactly one positional argument: an integer id.
- Reads `./notes.json`.
- If `id` is missing or malformed, or no note with that id exists: prints `error: no note with id <id>` to stderr, exit `1`.
- Otherwise removes that note, writes the file back, prints `deleted: <id>` to stdout, exit `0`.

### Unknown subcommand or no args

- Prints a one-line usage message to stderr: `usage: notes.py {add <text>|list|delete <id>}`.
- Exit code: `2`.

## Persistence format

`./notes.json` is a JSON array of objects:

```json
[
  {"id": 1, "text": "buy milk"},
  {"id": 3, "text": "call mom"}
]
```

Ids are NOT renumbered after deletes (deleted ids are not reused). This keeps `delete <id>` idempotent across runs.

## Constraints

- Single file `notes.py`.
- Total LOC ≤ 100 (advisory; the grader does not fail on this, but PR review does).
- Imports limited to: `sys`, `json`, `pathlib`. No third-party packages. No `argparse`, no `click`.
- No shebang required (invocation goes through `python …`).
- Must run on Python 3.11+ on macOS, Linux, and WSL2.

## Worked example (grader's expected trace)

```text
$ python notes.py add "hello"
added: 1
$ python notes.py list
1	hello
$ python notes.py delete 1
deleted: 1
$ python notes.py list
$ echo "exit $?"
exit 0
```

The grader's PASS condition is exactly this sequence (with `hello` substituted by the grader's chosen test string).

## Reference solution skeleton

```python
import json, sys
from pathlib import Path

STORE = Path("notes.json")

def _load() -> list:
    if not STORE.exists() or STORE.stat().st_size == 0:
        return []
    return json.loads(STORE.read_text(encoding="utf-8"))

def _save(items: list) -> None:
    STORE.write_text(json.dumps(items, ensure_ascii=False) + "\n", encoding="utf-8")

def cmd_add(text: str) -> int:
    items = _load()
    nid = (max((i["id"] for i in items), default=0)) + 1
    items.append({"id": nid, "text": text})
    _save(items)
    print(f"added: {nid}")
    return 0

def cmd_list() -> int:
    for item in _load():
        print(f"{item['id']}\t{item['text']}")
    return 0

def cmd_delete(arg: str) -> int:
    try:
        target = int(arg)
    except ValueError:
        print(f"error: no note with id {arg}", file=sys.stderr)
        return 1
    items = _load()
    kept = [i for i in items if i["id"] != target]
    if len(kept) == len(items):
        print(f"error: no note with id {target}", file=sys.stderr)
        return 1
    _save(kept)
    print(f"deleted: {target}")
    return 0

def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: notes.py {add <text>|list|delete <id>}", file=sys.stderr)
        return 2
    cmd, rest = argv[1], argv[2:]
    if cmd == "add" and len(rest) >= 1:
        return cmd_add(" ".join(rest))
    if cmd == "list" and not rest:
        return cmd_list()
    if cmd == "delete" and len(rest) == 1:
        return cmd_delete(rest[0])
    print("usage: notes.py {add <text>|list|delete <id>}", file=sys.stderr)
    return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

Above is ~50 LOC — comfortably within the 100-LOC budget — and is the file that ships under `exercises/beginner/part-08/solution/notes.py`.
