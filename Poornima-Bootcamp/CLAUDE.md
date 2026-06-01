# Stack
- Exercises are Python **3.11+, standard library only** — never add a third-party import.
- No package manager for exercises: nothing to `pip install`, no venv, no lockfile.
- Course tooling (slides, ebook) is Bash + Marp/Node under `scripts/` and `slides/`.

# Conventions
- One exercise = one self-contained file in `module-NN/` (e.g. `module-02/task.py`). Don't split into a package.
- Functions are snake_case; CLI subcommand handlers are named `cmd_<name>`.
- Raise `UserError` for bad input; let it map to exit code 1 at a single top-level try/except.
- CLI exit codes: `0` ok, `1` user error, `2` internal error. Keep this contract.
- Use `argparse` subparsers with `set_defaults(func=...)`; type-hint signatures (`list[dict]`, etc.).
- Persist data as JSON in the CWD: `json.dumps(..., indent=2, ensure_ascii=False)` plus a trailing `"\n"`.
- Timestamps: `datetime.now(timezone.utc).isoformat(timespec="seconds")`.
- Lint with ruff; suppress only inline as `# noqa: <CODE>` with a one-line reason.

# Commands
- Run an exercise: `python3 module-NN/<script>.py <args>` (e.g. `python3 module-02/task.py list`).
- Lint: `ruff check module-NN/`.
- There is no test harness — verify by running the CLI and asserting output + exit code (`echo $?`).
- Build course artifacts only when asked: `scripts/build-ebook.sh`, `scripts/build-leanpub.sh`.
- Validate course content: `scripts/validate.sh` and `scripts/gates/*`.

# Do-not
- Never add a dependency, `requirements.txt`, `pyproject.toml`, or venv to an exercise — stdlib only.
- Never edit `slides/`, `specs/`, `book/`, `.specify/`, or `assessments/` to solve a coding exercise.
- Never commit generated data (`tasks.json`, `*.log`, `slides/dist/` caches) — respect `.gitignore`.
- Never write exercise solutions outside their own `module-NN/` directory.
- Don't reformat or restructure already-passing module code unless the task is about that file.

# Glossary
- **module-NN** — the workspace for bootcamp lesson NN; new work goes in `module-03/`.
- **The loop** — Plan → Implement → Test → Review → Commit; never skip Review (read the diff line by line).
- **gate** — a validation script in `scripts/gates/`; run before publishing course content, not for exercises.
- **spec** — a feature folder under `specs/` using spec-kit (`.specify`): `spec.md` / `plan.md` / `tasks.md`.
