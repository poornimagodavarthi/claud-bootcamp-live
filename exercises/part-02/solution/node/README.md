# Module 2 — Node + TypeScript Reference Solution

CLI Task Manager. Node 20+, `commander` + `tsx`.

## Install

```bash
npm install
```

## Run

```bash
npm run task -- add "Write the spec"
npm run task -- list
npm run task -- list --status open
npm run task -- done 1
npm run task -- delete 99
```

`delete 99` exits 1 (unknown id); the other commands exit 0. State persists to `tasks.json` in CWD.

## Full expected output

A complete session (start from an empty directory with no `tasks.json`). The `created_at` timestamps will differ — only the shape matters. `npm run task --` prints its own banner line first; the task output follows.

```text
$ npm run task -- add "Write the spec"
Added task #1: Write the spec

$ npm run task -- add "Review the PR"
Added task #2: Review the PR

$ npm run task -- list
id  status  created_at                 text
 1  open    2026-05-30T10:12:16.123Z   Write the spec
 2  open    2026-05-30T10:12:16.456Z   Review the PR

$ npm run task -- done 1
Marked #1 as done

$ npm run task -- list --status open
id  status  created_at                 text
 2  open    2026-05-30T10:12:16.456Z   Review the PR

$ npm run task -- delete 99
No task with id 99            # → stderr, exit code 1
```

Empty list and empty-text cases:

```text
$ npm run task -- list            # no tasks.json yet
(no tasks)

$ npm run task -- add ""          # empty text
error: text must not be empty     # → stderr, exit code 1
```

## Exit codes

- `0` success
- `1` user error
- `2` internal error
