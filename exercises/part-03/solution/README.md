# Reference solution — Module 3

> **Stop**: only open this after you have authored your own `module-03/CLAUDE.md`.

This module produces a **document**, not running code, so the reference solution is a worked `CLAUDE.md` you can diff against.

```text
module-03/
├── CLAUDE.md   # your project brain file (copy of the one committed to the repo root)
└── proof.png   # screenshot of Claude obeying one convention in a fresh chat
```

## Worked example `CLAUDE.md`

This is a real, corrected `CLAUDE.md` generated for this training repo. It keeps the five required H1 sections (`Stack`, `Conventions`, `Commands`, `Do-not`, `Glossary`) and stays well under 80 lines. Yours should be **shorter and more specific** to your own repo.

````markdown
# Stack

- Python 3.11+ (stdlib only — no external runtime dependencies)
- JSON for data files (indent: 2 spaces)
- Git for version control

# Conventions

Python files:
- Shebang: `#!/usr/bin/env python3`
- Docstrings: one-line only (e.g., `"""Load tasks from JSON file."""`)
- Argv parsing: use `argparse` with subcommands (not Click or Fire)
- CLI exit codes: 0 (success), 1 (user error), 2 (internal error)
- Timestamps: ISO 8601 UTC (`datetime.now(timezone.utc).isoformat()`)

Layout:
- `module-NN/task.py` — the reference solution
- `module-NN/README.md` — usage docs for that solution
- `module-NN/tasks.json` — sample data file

Format/lint: `black` and `ruff` are dev-only tools (allowed; they are not shipped deps).

# Commands

```bash
python3 module-02/task.py list      # run the CLI
python3 -m pytest -q                # run tests
ruff check .                        # lint
```

# Do-not

- Never add external *runtime* dependencies — solutions stay stdlib-only.
- Never commit non-template data files; `.gitignore` generated `tasks.json`.
- Don't change the `module-NN/` layout without updating `instructor-guide.md`.

# Glossary

- Reference solution — working implementation of an exercise (lives in `module-NN/`).
- Module — numbered bootcamp part (01–11); each has slides, an exercise, and a solution.
- Bootcamp — the live virtual event; students work modules in order during the session.
````

## Review checklist — common AI deviations

A first-pass generated `CLAUDE.md` (especially from a faster/weaker model) usually needs editing before you commit it. These are the issues caught in the example above — use them during the **Review** step:

1. **Self-contradicting exclusion list.** "use `argparse` … (not Click, **argparse**, or fire)" listed `argparse` in its own do-not list. Fixed to `(not Click or Fire)`.
2. **Tooling vs the no-deps rule.** The draft named `black` as the formatter while `Do-not` said "stdlib-only, no external dependencies." Scope the rule to *runtime* deps so dev tools (`black`, `ruff`) are allowed — or drop them.
3. **Thin `Commands` section.** The spec asks for build/test/run/**lint**. The draft only had `chmod` + a manual run; add real `pytest`/`ruff` commands so a future prompt like "how do I run tests?" is answerable.
4. **Grammar bug.** "`*.json` … should .gitignore'd" → "should be `.gitignore`d".
5. **Over-meta content.** A draft may describe the *bootcamp* rather than the repo you actually work in. Keep lines that change Claude's behaviour on real edits; cut pure documentation.

> Teaching point: every line must *change behaviour on a future prompt*. The `Conventions` section here is the highest-value (exit codes, timestamp format, docstrings); `Glossary` is the weakest — a good candidate for the trim test's "name one line you could delete and why."

## Definition of done

- [ ] All five H1 sections present: `Stack`, `Conventions`, `Commands`, `Do-not`, `Glossary`.
- [ ] ≤ 80 lines, specific to your repo (no generic placeholders).
- [ ] `CLAUDE.md` committed to the underlying repo (not just the submission folder).
- [ ] `proof.png` shows Claude obeying one convention in a fresh chat.
- [ ] You can name one line you deleted in the trim test, and why.
