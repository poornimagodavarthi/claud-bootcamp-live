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

## Full expected output

A complete session (start from an empty directory with no `tasks.json`). The `created_at` timestamps will differ — only the shape matters.

```text
$ python3 task.py add "Write the spec"
Added task #1: Write the spec

$ python3 task.py add "Review the PR"
Added task #2: Review the PR

$ python3 task.py list
 id  status  created_at                 text
  1  open    2026-05-30T10:12:16+00:00  Write the spec
  2  open    2026-05-30T10:12:16+00:00  Review the PR

$ python3 task.py done 1
Marked #1 as done

$ python3 task.py list --status open
 id  status  created_at                 text
  2  open    2026-05-30T10:12:16+00:00  Review the PR

$ python3 task.py delete 99
No task with id 99            # → stderr, exit code 1
```

Empty list and corrupt-file cases:

```text
$ python3 task.py list            # no tasks.json yet
(no tasks)

$ python3 task.py add ""          # empty text
error: text must not be empty     # → stderr, exit code 1
```

## Exit codes

- `0` success
- `1` user error (missing id, empty text)
- `2` internal error (corrupt JSON)
