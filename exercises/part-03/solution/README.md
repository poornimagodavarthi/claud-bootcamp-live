# Reference solution — Module 3

> **Stop**: only open this after you have authored your own `module-03/CLAUDE.md`.

This module produces a **document**, not running code, so the reference solution is a worked `CLAUDE.md` you can diff against.

```text
module-03/
├── CLAUDE.md          # your project brain file
└── before-after.md    # 2-paragraph note: what changed in Claude's behaviour after CLAUDE.md was added
```

## Reference `CLAUDE.md` skeleton

Use this skeleton as a starting comparison. Your version should be **shorter and more specific** to your repo.

```markdown
# Project brain file

## What this repo is
One paragraph. What the codebase does. Who uses it.

## House rules
- Tests live in `tests/`. Run them with `pytest -q`.
- Conventional Commits; no `Co-authored-by: Claude`.
- Never commit to `main` directly.

## Architecture pointers
- Entry point: `src/main.py`.
- Public surface: `src/api/`.
- Datastore: SQLite at `data/app.db`; schema in `src/db/schema.sql`.

## What to do, what NOT to do
- DO ask before adding a dependency.
- DO not introduce a new framework. Use the existing stack.
- DO produce a plan before any change > 50 lines.

## Skills to invoke
- `code-review` before any commit.
- `release-readiness` before any tag.
```

## Definition of done

- [ ] All five `## ` sections present.
- [ ] Specific to your repo (no generic placeholders).
- [ ] `before-after.md` names one concrete behavioural change you observed.
