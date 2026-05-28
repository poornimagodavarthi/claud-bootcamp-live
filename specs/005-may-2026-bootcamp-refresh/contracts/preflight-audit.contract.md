# Contract — `scripts/preflight.sh`

**Feature**: 005-may-2026-bootcamp-refresh
**Date**: 2026-05-28
**Status**: Contract (not yet implemented).

The pre-flight audit is the **single externally-observable interface** this feature ships. Instructors invoke it; CI may invoke it; humans read its output. Everything else (slides, exercises, skills, assessments) is content already addressable by URL.

## Synopsis

```text
scripts/preflight.sh [--quick] [--verbose] [--gate <name>]
```

| Flag | Meaning | Default |
|---|---|---|
| `--quick` | Skip slow gates (`audit.slide-overflow` which renders HTML) | off |
| `--verbose` | Print per-gate trace | off |
| `--gate <name>` | Run a single gate by name (e.g., `audit.cross-links`) | run all |

## Exit codes

| RC | Meaning |
|---|---|
| 0 | All `block`-severity gates passed; any `warn` gates emitted only warnings |
| 1 | One or more `block`-severity gates failed |
| 2 | Tooling / setup error (e.g., bash too old, file system not writable) |
| 64 | Invalid invocation (unknown flag / unknown `--gate`) |

## Output contract

Stdout: human-readable report (no colour by default; ANSI when `--verbose` and stdout is a TTY). Stderr: tooling errors only.

```text
preflight  bootcamp=Training-Claude-Code-Extended  feature=005  2026-05-28T12:34:56Z

[PASS] audit.module-bundle         (10/10 modules complete)
[PASS] audit.slide-anatomy         (11 decks × 14 required sections present)
[PASS] audit.slide-theme           (theme=wow-beginner on every deck)
[FAIL] audit.duration-sum          sum=247 expected=240±5
       slides/part-09-skills-workflows.md: 22 min  (too long? cut Pillar 4 slide)
[PASS] audit.exercise-anatomy
[FAIL] audit.cross-links
       README.md:L48  -> ./exercises/part-11/  (does not exist)
       slides/part-06-git-workflows.md:L78 -> ../skills/release-readiness/  (does not exist)
[PASS] audit.bundle-coverage       (Skills · MCP · Hooks · GitHub Actions · Multi-agent all ≥1 in slides AND exercises)
[WARN] audit.dist-freshness        2 sources newer than dist artefacts (part-09, part-10) — rebuild before delivery
...

Result: 2 BLOCK gates failed, 1 WARN.  RC=1.
```

## Gate definitions (the wire contract)

Each gate is a function `gate_<name>` inside `scripts/preflight.sh` (or sourced from `scripts/gates/`) with this signature:

```bash
# Inputs: $REPO_ROOT (absolute path), $VERBOSE (0|1)
# Outputs:
#   - prints "[PASS] audit.<name>  <one-line summary>"
#     OR     "[FAIL] audit.<name>" followed by ≥1 indented offender lines
#     OR     "[WARN] audit.<name>  <one-line summary>" (+ indented details)
# Returns:
#   0 on PASS or WARN
#   1 on FAIL
gate_<name>() { ... }
```

### `audit.module-bundle` (block)

- For NN in 01..10: assert `slides/part-NN-*.md`, `exercises/part-NN/README.md`, `exercises/part-NN/solution/` all exist.
- Offender format: `module-NN: missing <component>`.

### `audit.slide-anatomy` (block)

- For each `slides/part-*.md` (incl. part-11): assert all 14 canonical H2 sections appear at least once.
- Offender: `<deck>: missing section "<H2 title>"`.

### `audit.slide-theme` (block)

- For each `slides/part-*.md`: assert frontmatter contains `theme: wow-beginner`.
- Implementation: wrap existing `scripts/check-verbatim-blocks.sh` FR-002 check.

### `audit.slide-overflow` (block, slow)

- Delegate to `scripts/check-slide-overflow.sh --budget 22 slides/dist/html`.
- Skipped by `--quick`.

### `audit.duration-sum` (block)

- Sum `<!-- duration: NN min -->` across part-01..10. Assert `235 ≤ Σ ≤ 245`.
- Offender: `sum=<actual>  expected=240±5`.

### `audit.exercise-anatomy` (block)

- For each `exercises/part-NN/README.md`: assert all 9 canonical H2 sections present.
- Offender: `exercises/part-NN: missing section "<H2 title>"`.

### `audit.solution-presence` (block)

- For each `exercises/part-NN/`: assert `solution/` exists and contains at least one of: `README.md`, `run.sh`, `solution.py`, `solution.js`, `solution.ts`, `solution.md`.
- Offender: `exercises/part-NN/solution: empty or missing`.

### `audit.skill-contract` (block)

- For each `skills/<slug>/SKILL.md`: validate against `specs/001-bootcamp-course-materials/contracts/skill.contract.md` (frontmatter `name`+`description`; 6 H2 sections; no `module-NN/` paths).
- Catalogue check: assert exactly the 12 expected slugs present (10 existing + `release-readiness` + `mcp-context-brief`).
- Offender: `skills/<slug>: <reason>`.

### `audit.assessment-coverage` (block)

- Assert `assessments/{knowledge-quiz,practical-task,code-review-reflection,rubric,answer-key}.md` exist.
- Assert `rubric.md` references each module 01–10 at least once.
- Assert ≥1 assessment item mentions each of: Skills, MCP, Hooks, GitHub Actions, Multi-agent (case-insensitive, word-boundary).
- Offender: `<file>: missing coverage for <topic>`.

### `audit.cross-links` (block)

- For every `.md` file under repo (excluding `.git/`, `node_modules/`, `slides/dist/`): extract markdown links of the form `(./...)`, `(../...)`, `(path/...)`; resolve against the link source; for fragment links `(#anchor)` skip; for external `(http://...)` / `(https://...)` skip (R-003).
- Offender: `<file>:<line> -> <link>` for each unresolved.

### `audit.bundle-coverage` (block)

- For each May-2026 headline upgrade { Skills, MCP, Hooks, GitHub Actions, Multi-agent }: assert ≥1 occurrence (case-insensitive) in `slides/part-*.md` AND ≥1 occurrence in `exercises/part-*/README.md`.
- Offender: `<topic>: not landed in <slides|exercises>`.

### `audit.no-clarifications-in-published` (block)

- Grep for `\[NEEDS CLARIFICATION` and `^TODO\b` in `README.md`, all `slides/part-*.md`, all `exercises/part-*/README.md`, all `skills/*/SKILL.md`.
- Offender: `<file>:<line>: <match>`.

### `audit.archive-isolation` (block)

- If `archive/` exists: scan README + all `slides/part-*.md` + all `exercises/part-*/README.md` + `student-guide.md` + `instructor-guide.md` for markdown links into `archive/`.
- A link is OK only if it appears in the **single dedicated section** in README titled exactly `## Optional pre-bootcamp warm-up (archived)`.
- Offender: `<file>:<line> -> archive/...  (link from primary navigation)`.

### `audit.dist-freshness` (warn)

- For each `slides/part-*.md`: compare `mtime` of source with `slides/dist/pdf/<basename>.pdf`. If source newer: WARN.
- Never fails the audit (severity=warn).

### `audit.contrast` (block)

- Delegate to existing `scripts/check-contrast.sh`.

## Invocation examples

```bash
# Standard pre-delivery check
scripts/preflight.sh

# Fast iteration during authoring
scripts/preflight.sh --quick

# Single-gate debug
scripts/preflight.sh --gate audit.cross-links --verbose

# CI usage (future):
scripts/preflight.sh || { echo "::error::pre-flight failed"; exit 1; }
```

## Non-goals (NOT enforced by this contract)

- External URL checking (R-003).
- Spelling / grammar.
- Reference-solution runtime verification (manual dress rehearsal — SC-009).
- Image alt-text quality (only presence is verified by `audit.contrast`).
- Reading-level / Lexile score.
