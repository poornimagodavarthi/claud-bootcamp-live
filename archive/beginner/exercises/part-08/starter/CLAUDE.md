# Project: notes

Tiny CLI for personal notes. Single file, no dependencies.

## Stack
- Python 3.11+, standard library only.

## Commands
- Run: `python3 notes.py <add|list|delete> ...`.
- Grade: `scripts/check-beginner-capstone.sh notes.py`.

## Conventions
- One file: `notes.py`. Do not split.
- Persistence: `notes.json` in the current directory.
- IDs are monotonic: deleting an id does NOT free it for reuse.
- No third-party packages. Ever.
