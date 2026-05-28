# Reference solution — Module 2

> **Stop**: only open this after you have produced `module-02/cli.py` (or `cli.js`) and `PROMPT.md`.

Two parallel tracks ship under this directory. Pick the one matching your stack and diff your work against it:

| Track | Path | Run |
|---|---|---|
| Python (primary) | [`python/`](python/) | `python3 python/cli.py add "first task"` |
| Node.js (secondary) | [`node/`](node/) | `node node/cli.js add "first task"` |

Both implement the same CLI Task Manager spec from `../README.md`. They are not byte-identical: differences highlight where Best-of-N (Module 4) would choose between them.

## What to compare

1. **`PROMPT.md` shape** — does yours follow GCOE (Goal · Constraints · Output · Examples)?
2. **Command surface** — `add`, `list`, `done`, `delete`, `--help`.
3. **Persistence** — both use a single JSON file (`tasks.json`) in the project root.
4. **Error paths** — empty input, missing ID, broken JSON.

## Definition of done

See `../README.md` — the rubric is unchanged.
