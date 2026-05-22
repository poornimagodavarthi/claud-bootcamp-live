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
npm run task -- delete 99      # exit 1
```

State persists to `tasks.json` in CWD.

## Exit codes

- `0` success
- `1` user error
- `2` internal error
