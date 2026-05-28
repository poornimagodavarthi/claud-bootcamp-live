import json
import sys
from pathlib import Path

STORE = Path("notes.json")


def main(argv):
    if not argv:
        print("usage: notes.py <add|list|delete> ...", file=sys.stderr)
        return 2
    cmd = argv[0]
    data = json.loads(STORE.read_text()) if STORE.exists() else []
    if cmd == "add" and len(argv) == 2:
        new_id = (max((n["id"] for n in data), default=0) + 1)
        data.append({"id": new_id, "text": argv[1]})
        STORE.write_text(json.dumps(data))
        print(f"added: {new_id}")
        return 0
    print("usage: notes.py <add|list|delete> ...", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
