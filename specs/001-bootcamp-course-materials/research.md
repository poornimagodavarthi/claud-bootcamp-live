# Phase 0 Research: Claude Code Bootcamp — Course Materials Repository

**Branch**: `001-bootcamp-course-materials`
**Date**: 2026-05-21
**Status**: Complete (no NEEDS CLARIFICATION items remained from spec)

This document records best-practice decisions that lock authoring
conventions before content production. Each entry follows the
Decision / Rationale / Alternatives format.

---

## R1. Marp authoring conventions

**Decision**: Use Marp's default theme with a global front-matter block
in every deck:

```yaml
---
marp: true
theme: default
paginate: true
size: 16:9
title: <Module title>
description: <One-line module promise>
---
```

Code fences use language tags (`bash`, `python`, `typescript`,
`markdown`, `text`); no custom Marp themes for v1; images for module 7
are referenced as `![w:600](./../exercises/part-07/wireframe.png)` from
the slide deck.

**Rationale**: Default theme renders consistently across PPTX/PDF/HTML
without custom CSS, eliminating one class of build failures. Pagination
is required for premium delivery. 16:9 matches Zoom/Teams full-screen.
Frontmatter `title`/`description` populate PPTX metadata.

**Alternatives considered**:

- *Custom theme*: rejected — adds maintenance burden; not needed for v1.
- *Per-deck local images*: rejected for module 7 wireframe to avoid
  duplication; canonical asset lives under `exercises/part-07/`.
- *MathJax / Mermaid*: rejected for v1 — neither needed by content;
  reduces Chromium pain.

---

## R2. Claude Code SKILL.md packaging

**Decision**: Each skill is a directory `skills/<kebab-name>/` containing
a single `SKILL.md` with this frontmatter:

```yaml
---
name: <kebab-name>
description: <one-line, ≤120 chars, action-oriented; appears in Claude's skill picker>
---
```

The body uses the 6 mandated H2 sections in this exact order:
`## Purpose`, `## When to use it`, `## Prompt body`, `## Expected
inputs`, `## Expected outputs`, `## Worked example`. No additional
frontmatter fields (e.g., `version`, `tags`) for v1.

**Rationale**: Matches the established Claude Code skill convention
visible in the user's local `assets/prompts/skills/` examples (each
skill = directory + `SKILL.md` + frontmatter `name` + `description`).
Auto-discoverable when `skills/` is dropped into a project.

**Alternatives considered**:

- *Single flat `skills/<name>.md` file*: rejected — breaks Claude Code's
  directory-based discovery; loses ability to ship companion files
  (templates, sample inputs) in future versions.
- *YAML `tags` array in frontmatter*: deferred — not used by Claude
  Code's matcher today; YAGNI for v1.

---

## R3. Python project skeletons for labs

**Decision**:

- **Module 2 CLI Task Manager**: pure Python 3.11+ stdlib (`argparse`,
  JSON file persistence at `~/.tasks.json`). No third-party deps.
- **Module 4 Notes App API**: FastAPI + uvicorn + Pydantic v2; SQLite
  via `sqlite3` stdlib (no SQLAlchemy). Single-file `main.py` skeleton.
- **Module 5 Tests + Bug Fixes**: builds tests for the module 4 API
  output using `pytest` + `httpx.AsyncClient` for endpoint tests; uses
  the same FastAPI/SQLite stack.
- **Module 7 Dashboard UI**: FastAPI server + Jinja2 templates +
  vanilla HTML/CSS (no React/Vue). Static-served chart via Chart.js
  CDN. One `requirements.txt`.
- **Module 8 Refactor**: refactor target is a deliberately-tangled
  ~150-line Python single-file script (mixed concerns) shipped under
  the exercise's starter; learner refactors into a 3-module package
  with tests intact.

All Python labs target 3.11+ and pin minimal dependencies in a
`requirements.txt` per `solution/` directory. No virtualenv tooling
prescription (students may use venv, uv, or poetry — guides note venv
as default).

**Rationale**: FastAPI is industry-standard, has excellent OpenAPI
support (relevant to module 4 Best-of-N comparisons), and learners can
read the type-hinted code easily. SQLite + stdlib avoids ORM teaching.
pytest is the de-facto Python test runner. Vanilla HTML/CSS for module
7 keeps the multimodal lab focused on the *Claude Code prompt → UI*
loop, not on a JS framework.

**Alternatives considered**:

- *Flask*: rejected — less idiomatic for new APIs in 2026, weaker type
  story.
- *Django*: rejected — too heavy for a 35-minute lab.
- *React for module 7*: rejected — adds a framework to learn that has
  nothing to do with the multimodal teaching point.
- *unittest*: rejected — pytest is now standard.

---

## R4. Node.js (TypeScript) parallel skeletons (modules 2, 4, 5)

**Decision**:

- **Module 2 (CLI)**: Node 20+ with `commander`; JSON file persistence;
  `tsx` for run-from-source (no build step).
- **Module 4 (API)**: Node 20+ with `hono` + `zod` + `better-sqlite3`;
  one `src/main.ts`.
- **Module 5 (Tests)**: `vitest` against the module 4 API.

All Node tracks ship a `package.json` with locked minor versions. No
ESLint/Prettier prescription beyond `npm run lint` if added later.

**Rationale**: Hono is small, fast, has Zod-friendly validation, and
works well for a 35-minute lab. `commander` is the most teachable Node
CLI library. `tsx` removes the build step. `vitest` matches the Python
side's mental model (single command, fast).

**Alternatives considered**:

- *Express + Joi*: rejected — heavier, less teachable type story than
  Hono + Zod.
- *NestJS*: rejected — out of scope for a 35-minute lab.
- *jest*: rejected — slower startup, ESM friction; vitest is the modern
  default.
- *Native `node --test`*: considered — viable but less ergonomic for
  HTTP testing than vitest + supertest-equivalents.

---

## R5. Cross-artifact validation strategy

**Decision**: A single Bash script `scripts/validate.sh` (POSIX-friendly,
runs under bash 4+) performs these structural checks; all are blocking
on release:

1. Each `slides/part-NN-*.md` contains all 14 required H1/H2 markers
   (presence-only; ordering enforced via a fixed sequence list).
2. Each `exercises/part-NN/README.md` contains all 9 required H2
   sections.
3. Each `skills/*/SKILL.md` has YAML frontmatter with `name` and
   `description` and 6 required body H2 sections.
4. Code-producing modules (2, 4, 5, 7, 8) have a `solution/` directory
   with at least one runnable file; modules 2, 4, 5 also have
   `solution/python/` AND `solution/node/`.
5. The 10-project list (canonical names) is identical across
   `README.md`, every slide deck (in the Title slide), and
   `assessments/rubric.md`.
6. Module instruction times parsed from slide frontmatter (or a
   conventional `<!-- duration: NN min -->` HTML comment) sum to 240
   minutes ±5.
7. `slides/dist/` is gitignored.
8. `LICENSE` and `skills/LICENSE` exist; `README.md` mentions both.

Reviewer checks (NOT scripted): tone (no motivational filler), prompt
quality, "Common mistakes" coverage, "Instructor notes" sufficiency.

**Rationale**: Bash + grep/awk/sed handles structural checks without
introducing Python-as-tooling. The script is ~200 lines, fast, and
runs in CI later if added. Subjective reviews stay with humans.

**Alternatives considered**:

- *Python validator*: rejected — adds a dev-time runtime; bash is
  sufficient and aligns with constitution Principle X.
- *Node validator (e.g., remark-lint)*: rejected — heavier, slower,
  adds npm dev deps to the *content* repo.
- *Markdownlint only*: insufficient — doesn't enforce section presence
  by name.

---

## R6. Marp build performance & PPTX/Chromium fallbacks

**Decision**: `slides/deploy-pptx.sh` keeps its current shape:

- Default mode = PPTX only, output to `slides/dist/pptx/`.
- Flags: `--pdf` (adds PDF), `--html` (adds HTML), `--all`, `--clean`.
- Auto-detects global `marp`; falls back to
  `npx --yes @marp-team/marp-cli@latest`.
- Documents `CHROME_PATH` for users with existing Chrome/Edge/Brave
  installs.
- Adds a `--check` flag that runs `marp --validate` (or equivalent)
  without producing output, for CI use.

**Rationale**: Existing script already meets FR-002/FR-003. The
`--check` addition closes the loop for `scripts/validate.sh` to invoke
build verification without paying the Chromium cost.

**Alternatives considered**:

- *Pre-bundling Chromium*: rejected — license + size issues.
- *Replacing Marp with Slidev*: rejected — Marp is the constitution-
  mandated tool (Principle III).

---

## R7. License templating

**Decision**:

- Top-level `LICENSE`: verbatim text of [Creative Commons
  Attribution-NonCommercial-ShareAlike 4.0
  International](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.txt)
  (the legal-code text). A short human-readable summary in the
  `README.md` License section links to the deed.
- `skills/LICENSE`: standard MIT License text (SPDX `MIT`) with copyright
  line `Copyright (c) 2026 Luca Berton`.
- `README.md` License section explicitly states the split and the
  rationale: "Course materials are CC BY-NC-SA 4.0 to protect the paid
  workshop; the `skills/` directory is MIT so graduates can ship
  skills in commercial work."

**Rationale**: Direct from the FR-005a clarification. CC BY-NC-SA 4.0
legal-code (not just the deed) is required for unambiguous enforcement.
MIT for skills aligns with normal OSS expectations and lets graduates
adopt skills without legal review.

**Alternatives considered**:

- *Apache 2.0 for skills*: viable; MIT chosen for simplicity and zero
  patent-language overhead for prompt files.
- *CC0 for skills*: rejected — strips attribution, which we want for
  brand reach.

---

## R8. Pre-work smoke-test design

**Decision**: Pre-work smoke test is a 4-step checklist students run
before the live session:

1. `python3 --version` shows 3.11+ (and Node 20+ for those opting into
   modules 2/4/5 Node track).
2. `git --version` shows ≥ 2.40.
3. `claude --version` (or equivalent Claude Code CLI invocation)
   succeeds and shows authenticated account.
4. In the cloned repo: run a one-liner Claude Code prompt
   (`/skills` or equivalent) that asks Claude to read `README.md` and
   reply with the workshop title. Student copies Claude's reply into
   their pre-work checklist and brings it to the session.

The full checklist, expected outputs, and troubleshooting lives in
`student-guide.md` under the **Pre-work** heading. Module 1's live 5-
minute verification asks students to confirm they completed all four
steps.

**Rationale**: A single end-to-end smoke test catches the most common
blocking issues (missing runtime, unauthenticated CLI, repo not
cloned, Claude Code not actually working) in 5 minutes. Capturing the
output gives the instructor an objective verification artifact rather
than relying on self-report.

**Alternatives considered**:

- *Asking students to run a unit test*: rejected — too heavy for
  pre-work; risks blocking on Python deps unrelated to Claude Code.
- *Just "ensure Claude Code works"*: rejected — too vague; not
  verifiable.

---

## Summary

8 research topics resolved. No NEEDS CLARIFICATION items remain. All
decisions are compatible with the constitution (no Complexity Tracking
entries needed). Authoring may begin immediately.
