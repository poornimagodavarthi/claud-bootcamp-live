# Project: notes

Tiny CLI for personal notes. Single file, no dependencies.

## Stack
- Python 3.11+, standard library only.
- Tests: `pytest -q`.

## Commands
- Run: `python notes.py <subcommand>`.
- Test: `pytest -q`.
- Lint: `python -m py_compile notes.py`.

## Conventions
- One file: `notes.py`. Do not split.
- Persistence: `notes.json` in the current directory.
- No third-party packages. Ever.
