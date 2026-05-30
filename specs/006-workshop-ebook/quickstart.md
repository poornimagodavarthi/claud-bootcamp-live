# Quickstart: Workshop Markdown Ebook

## Prerequisites

- Python 3.11+ on `PATH` (already required by the bootcamp pre-work)
- Bash (macOS / Linux / WSL2)
- No additional packages — standard library only

## Build the ebook

```bash
# From the repository root
scripts/build-ebook.sh
```

Output is written to (gitignored):

```text
book/dist/claude-code-bootcamp-ebook.md
```

Open that file in any Markdown viewer (VS Code preview, GitHub, Obsidian, etc.) and read the whole bootcamp end to end.

### Useful options

```bash
scripts/build-ebook.sh --output /tmp/bootcamp.md   # custom output path
scripts/build-ebook.sh --no-solutions              # omit solution appendices
```

## Validate the ebook

```bash
scripts/check-ebook.sh
```

Expected: `PASS` for assertions ST-1..ST-9 and exit code 0. This is the same gate wired into `scripts/validate.sh`.

## Regenerate after content changes

The ebook is fully derived from `slides/`, `exercises/`, and `README.md`. After editing any source content, just re-run the build — no manual editing of the book itself:

```bash
scripts/build-ebook.sh && scripts/check-ebook.sh
```

## What you get

- A single Markdown file: title page, introduction, table of contents.
- Chapters 01–11 as continuous prose (Marp slide chrome and speaker notes removed).
- Hands-on exercises embedded in chapters 01–10, with reference-solution appendices.
- Back matter: skills library overview and certification / next-steps.
- Zero broken internal links for an ebook-only reader.
