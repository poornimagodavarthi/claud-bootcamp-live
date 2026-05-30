# Implementation Plan: Workshop Markdown Ebook

**Branch**: `006-workshop-ebook` | **Date**: 29 May 2026 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/006-workshop-ebook/spec.md`

## Summary

Produce a single, self-contained Markdown ebook of the Claude Code Bootcamp by **assembling existing repository content** (the 11 Marp slide decks, the 10 exercise briefs + reference solutions, and course metadata from `README.md`/guides) into one ordered, readable book with front matter, per-part chapters, embedded exercises, and back matter. Assembly is performed by a **repeatable build script** (`scripts/build-ebook.sh` driving a Python transformer) so the ebook can be regenerated whenever source content changes. The transformer strips Marp-only artifacts (frontmatter, `<!-- directives -->`, speaker notes, HTML slide chrome, `---` separators) and rewrites cross-references so the output reads as continuous prose and contains no broken internal links. Output lands in a gitignored build directory; the committed source of truth is the script + a small manifest, never hand-edited consolidated prose.

## Technical Context

**Language/Version**: Bash (orchestration) + Python 3.11+ (text transformation) — both already mandated prerequisites; no new runtime dependency (Constitution Principle X).

**Primary Dependencies**: Python standard library only (`re`, `json`, `pathlib`, `argparse`). No third-party packages (the manifest is JSON, parsed with stdlib `json`, so no YAML dependency). No Marp/Chromium needed (Markdown-in → Markdown-out).

**Storage**: Filesystem. Inputs are existing repo files; output is a generated Markdown file (plus optional per-chapter intermediates) under a gitignored `book/dist/` directory.

**Testing**: Shell-based validation gate (`scripts/check-ebook.sh`) asserting the success criteria (all 11 parts present + ordered, no raw Marp markup, no broken internal links, exercises 01–10 present). Consistent with existing `scripts/check-*.sh` + `scripts/validate.sh` convention.

**Target Platform**: macOS / Linux / Windows-via-WSL2 (same support matrix as the repo).

**Project Type**: Content build tooling for a documentation/courseware repository (single project, no client/server split).

**Performance Goals**: Full ebook regeneration completes in under a few seconds on a clean machine (pure text processing over ~22 source files). Not latency-sensitive.

**Constraints**: Output MUST render in a standard Markdown viewer; MUST NOT leak Marp directives, speaker notes, or HTML slide chrome; MUST contain zero broken internal links for an ebook-only reader; MUST be fully regenerable without manual prose authoring.

**Scale/Scope**: 11 slide decks + 10 exercises + 10 solution sets + 3 guides → 1 consolidated ebook (~12 chapters incl. front/back matter). Markdown-only output; PDF/EPUB explicitly out of scope.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The ebook is a **derived/assembled** artifact, not a new teaching module, so the module-anatomy principles apply to the source it draws from, not to the ebook itself. Relevant gates:

- **I. Practical, Project-Based Learning** — PASS. The ebook surfaces existing project-based content (exercises 01–10 are embedded). No theory-only material is introduced.
- **III. Marp-Flavored Markdown for Slides** — PASS / respected. Slide decks remain the Marp source of truth; the ebook is a separate read-only derivation and does not alter or replace `slides/`.
- **VII. No Motivational Filler** — PASS. The transformer strips speaker notes and presentation chrome; it adds only structural connective text (chapter intros), no marketing copy.
- **IX. Cross-Artifact Consistency** — PASS / reinforced. Because the ebook is generated from canonical sources rather than re-authored, canonical names/timing/weighting cannot drift; regeneration keeps it in sync (FR-009, SC-006).
- **X. Minimal External Dependencies** — PASS. Uses only Bash + Python 3.11 stdlib (both existing prerequisites). No new runtime/SaaS dependency. Build output is gitignored like `slides/dist/`.

**Result**: No violations. Complexity Tracking not required.

## Project Structure

### Documentation (this feature)

```text
specs/006-workshop-ebook/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── ebook-structure.md   # Reader-facing ebook table-of-contents contract
│   └── build-cli.md         # build-ebook.sh / check-ebook.sh command contract
├── checklists/
│   └── requirements.md  # Spec quality checklist (already created)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created here)
```

### Source Code (repository root)

```text
scripts/
├── build-ebook.sh        # NEW: orchestrates ebook generation (bash front-end)
├── check-ebook.sh        # NEW: validation gate for the generated ebook
└── ebook/                # NEW: Python transformer + manifest
    ├── build_ebook.py    # slide/exercise → prose transformer + assembler
    └── manifest.json     # ordered chapter list + source mappings + metadata (stdlib json)

book/                     # NEW: generated output (gitignored)
└── dist/
    └── claude-code-bootcamp-ebook.md

slides/                   # EXISTING (read-only inputs): part-01..part-11 *.md
exercises/                # EXISTING (read-only inputs): part-01..part-10 README.md + solution/
README.md                 # EXISTING: source of course metadata for front matter
.gitignore                # UPDATED: ignore book/dist/
```

**Structure Decision**: Single-project content-tooling layout. New code lives under `scripts/ebook/` to match the existing `scripts/` + `slides/deploy-pptx.sh` convention. Generated output goes to a gitignored `book/dist/` directory, mirroring the `slides/dist/` precedent (Constitution Principle III/X). A declarative `manifest.json` (parsed with the Python stdlib `json` module — no YAML dependency, honoring Principle X) holds chapter order, source-file mappings, and metadata so reordering/relabeling never requires touching transformer logic.

## Complexity Tracking

> No constitution violations. Section intentionally empty.
