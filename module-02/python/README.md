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

## Review checklist — common AI deviations

When you generate this CLI yourself, the model output often *runs* but quietly drifts from the spec. A weaker/faster model (e.g. Haiku) frequently produces all five of these. Use this list during the **Review** step to catch them:

1. **Wrong status value.** Spec uses `"open"`; models often emit `"pending"`. This also silently breaks the `list --status open` filter.
2. **Missing `--status` filter.** The `list` command should accept `--status open|done`. Generated versions frequently omit it entirely.
3. **Truncated `created_at` in `list`.** Storing a full ISO timestamp but printing `created_at[:10]` drops the time — the table shows only the date. Show the full timestamp.
4. **Header casing / divider.** Spec asks for lowercase columns `id, status, created_at, text`. Watch for `ID/Status/Created/Text` and hardcoded rules like `"-" * 100` that overflow the terminal.
5. **Silent corrupt-file handling (data-loss bug).** A corrupt `tasks.json` must exit `2`. Models often `except (json.JSONDecodeError, IOError): return {...}` — swallowing the error and treating the file as empty, so the next `add` **overwrites** the corrupt file and loses data. The reference exits `2` instead.

> Teaching point: the generated code can look finished and even run end-to-end, yet still miss the spec in 4–5 places and hide a data-loss bug. This is exactly why *skipping the Review step is the most common failure mode* (Part 1). Diff your output against the **Full expected output** above before declaring done.
