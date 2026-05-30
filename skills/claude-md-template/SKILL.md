---
name: claude-md-template
description: Generate a high-quality CLAUDE.md tailored to a target project by reading its codebase and conventions.
---

## Purpose

Scans a project's files, structure, and tooling to produce a `CLAUDE.md`
that captures stack, conventions, commands, and do-nots — so Claude Code
and contributors share the same working assumptions from the first session.

## When to use it

- When starting work on a project that has no `CLAUDE.md` yet.
- After a significant refactor or tooling change that makes an existing `CLAUDE.md` stale.
- When onboarding a new AI assistant or team member who needs a reliable codebase reference.
- Before handing off a project to another engineer or team.

## Prompt body

```text
Generate a CLAUDE.md for this project.

Steps:
1. Read the project root: list all top-level files and directories.
2. Identify the stack (language, framework, package manager) from config files.
3. Identify the test runner and how to run tests.
4. Identify the linter/formatter and how to invoke it.
5. Identify the primary entry point and how to run the project locally.
6. Note any conventions visible in the code (naming, file layout, error handling).
7. Note anything that must NOT be done (e.g. committing secrets, editing generated files).

Output a CLAUDE.md with these sections in order:
# Stack
# Commands
# Conventions
# Do-not

Keep each section concise. Prefer bullet points. Do not invent facts —
only write what you can confirm by reading the files.
```

## Expected inputs

- Project root directory (Claude Code's working directory or a path passed by the user).
- No additional inputs required; the skill reads the codebase itself.

## Expected outputs

- A `CLAUDE.md` file written to the project root.
- Sections: `# Stack`, `# Commands`, `# Conventions`, `# Do-not`.

## Worked example

**Scenario:** A small Flask API project has no `CLAUDE.md`.

**Invocation:**
```
/claude-md-template
```

**Expected output (excerpt):**
```markdown
# Stack
- Python 3.11, Flask 3.x, SQLite (stdlib sqlite3)
- No package manager for exercises — stdlib only

# Commands
- Run: `python app.py`
- Test: `pytest tests/`
- Lint: `ruff check .`

# Conventions
- One endpoint = one function, snake_case names
- Errors raise `HTTPException`; never return raw exceptions

# Do-not
- Never commit `.env` or `*.db` files
- Never add third-party dependencies without updating requirements.txt
```
