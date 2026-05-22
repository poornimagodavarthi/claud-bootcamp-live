# Module 2 — CLI Task Manager

## Goal

Ship a CLI Task Manager (add, list, done, delete) with JSON persistence, using a Tech-Lead-grade GCOE prompt.

## Scenario

A teammate asks for a quick CLI to track personal tasks. They have not specified anything beyond "make it work". You translate that ask into a precise prompt and ship a working tool in one pass. Then you iterate one prompt edit and document the diff.

## Starter instructions

1. Pick your track:
   - **Track A — Python** (3.11, stdlib only, `argparse`).
   - **Track B — Node + TypeScript** (Node 20, `commander`, `tsx`).
2. Create `module-02/` for submission and a working folder for code.
3. Open Claude Code in the working folder.

## Claude Code prompt to use

```text
GOAL
Build a single-binary CLI Task Manager so a developer can manage TODOs from the terminal.

CONSTRAINTS
- Language: Python 3.11 (stdlib only) — OR — TypeScript on Node.js 20 with `commander` + `tsx`.
- Persistence: a single JSON file `tasks.json` in CWD.
- No background processes. No network calls.
- Exit code 0 on success, 1 on user error, 2 on internal error.
- All user-facing strings in English.

OUTPUT FORMAT
- One source file (Python) or `src/index.ts` + `package.json` (Node).
- A short README explaining install + the four commands.

EXAMPLES
- `task add "Write the spec"` → "Added task #1: Write the spec"
- `task list` → tabular: id, status, created_at, text
- `task done 1` → "Marked #1 as done"
- `task delete 99` → exit 1, "No task with id 99"
```

## Manual validation steps

**Python (track A):**

```bash
python3 task.py add "Write the spec"      # exit 0
python3 task.py list                      # shows the task
python3 task.py done 1                    # exit 0
python3 task.py delete 99                 # exit 1
```

**Node (track B):**

```bash
npx tsx src/index.ts add "Write the spec"
npx tsx src/index.ts list
npx tsx src/index.ts done 1
npx tsx src/index.ts delete 99            # exit 1
```

Confirm `tasks.json` round-trips state across runs.

## Expected deliverable

```text
module-02/
├── <source files for chosen track>
├── README.md
└── iteration-notes.md   # one prompt edit + the resulting diff summary
```

A reference solution covering both tracks lives at `solution/` once you've completed the lab.

## Definition of done

- [ ] All four commands return correct exit codes.
- [ ] `tasks.json` persists across runs.
- [ ] `iteration-notes.md` documents one prompt edit and what changed.
- [ ] Reference solution **not** consulted before completing.

## Stretch challenge

Add `task list --status open` and `task list --status done` filters. Document the prompt change in `iteration-notes.md`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `tasks.json` not created | Confirm CWD is writable; check Claude added file I/O. |
| Empty list after add | Round-trip bug — Claude likely forgot to flush; re-prompt with that constraint. |
| Node track: `tsx` not found | `npm i -D tsx`. |
| Python track: third-party deps appeared | Re-prompt with the "stdlib only" constraint reinforced. |
