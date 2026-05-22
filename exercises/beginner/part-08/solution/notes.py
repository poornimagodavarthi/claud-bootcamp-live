"""notes.py — reference capstone solution.

Three subcommands: add, list, delete. Persists to ./notes.json.
Stdlib only. IDs are monotonic across the lifetime of the store.
"""

import json
import sys
from pathlib import Path

STORE = Path("notes.json")


def _load():
    if not STORE.exists():
        return {"next_id": 1, "notes": []}
    data = json.loads(STORE.read_text())
    if "next_id" not in data:
        existing = [n["id"] for n in data.get("notes", [])]
        data["next_id"] = (max(existing) + 1) if existing else 1
    return data


def _save(data):
    STORE.write_text(json.dumps(data))


def _usage():
    print("usage: notes.py <add TEXT | list | delete ID>", file=sys.stderr)
    return 2


def cmd_add(text):
    data = _load()
    new_id = data["next_id"]
    data["notes"].append({"id": new_id, "text": text})
    data["next_id"] = new_id + 1
    _save(data)
    print(f"added: {new_id}")
    return 0


def cmd_list():
    data = _load()
    for n in data["notes"]:
        print(f"{n['id']}\t{n['text']}")
    return 0


def cmd_delete(id_str):
    try:
        target = int(id_str)
    except ValueError:
        return _usage()
    data = _load()
    before = len(data["notes"])
    data["notes"] = [n for n in data["notes"] if n["id"] != target]
    if len(data["notes"]) == before:
        print(f"no such id: {target}", file=sys.stderr)
        return 1
    _save(data)
    print(f"deleted: {target}")
    return 0


def main(argv):
    if not argv:
        return _usage()
    cmd = argv[0]
    if cmd == "add" and len(argv) == 2:
        return cmd_add(argv[1])
    if cmd == "list" and len(argv) == 1:
        return cmd_list()
    if cmd == "delete" and len(argv) == 2:
        return cmd_delete(argv[1])
    return _usage()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
