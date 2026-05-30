# Contract: Build & Validation CLI

Defines the command-line interface for generating and validating the ebook. These are the executable contracts the implementation must satisfy.

## `scripts/build-ebook.sh`

Bash front-end that runs the Python transformer.

```text
Usage:
  scripts/build-ebook.sh [--output PATH] [--no-solutions] [--manifest PATH]

Options:
  --output PATH      Output Markdown file. Default: book/dist/claude-code-bootcamp-ebook.md
  --no-solutions     Exclude reference-solution appendices (overrides manifest include_solutions).
  --manifest PATH    Manifest file. Default: scripts/ebook/manifest.yml
  -h, --help         Print usage and exit 0.

Behavior:
  - Self-locates repo root from the script directory (like deploy-pptx.sh).
  - Creates the output directory if missing.
  - Invokes: python3 scripts/ebook/build_ebook.py --manifest <m> --output <o> [--no-solutions]
  - Exit 0 on success; non-zero on any error (missing source, write failure).

Stdout:
  - One summary line: chapters assembled, output path, byte size.
```

## `scripts/ebook/build_ebook.py`

```text
Usage:
  python3 scripts/ebook/build_ebook.py --manifest PATH --output PATH [--no-solutions]

Contract:
  - Reads the manifest; fails fast (exit 2) if any non-null source path is missing.
  - For each chapter: load slide → strip Marp artifacts → demote/scope headings →
    rewrite links → append exercise (if present) → append solution (unless excluded).
  - Prepend front matter (title page, intro, prerequisites, generated TOC).
  - Append back matter (skills appendix, certification/next-steps appendix).
  - Write the single Markdown file to --output.
  - Uses only the Python standard library.

Exit codes:
  0  success
  2  missing/invalid source or manifest
  1  unexpected error
```

## `scripts/check-ebook.sh`

Validation gate; safe to call from `scripts/validate.sh`.

```text
Usage:
  scripts/check-ebook.sh [--manifest PATH]

Behavior:
  - Builds the ebook to a temporary path (does not require a prior build).
  - Asserts every structural assertion ST-1..ST-9 from contracts/ebook-structure.md.
  - Prints PASS/FAIL per assertion.

Exit codes:
  0  all assertions pass
  1  one or more assertions failed (prints which)
```

## Integration

- Add `book/dist/` to `.gitignore`.
- Add an invocation of `scripts/check-ebook.sh` to `scripts/validate.sh` so release readiness enforces the ebook contract.
