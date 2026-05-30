# Module 2 — Python Reference Solution

Single-file CLI Task Manager. Python 3.11+, stdlib only.

## Run

```bash
python3 task.py add "Write the spec"
python3 task.py list
python3 task.py list --status open
python3 task.py done 1
python3 task.py delete 99
```

`delete 99` exits 1 (unknown id); the other commands exit 0. State persists to `tasks.json` in CWD.

## Exit codes

- `0` success
- `1` user error (missing id, empty text)
- `2` internal error (corrupt JSON)
