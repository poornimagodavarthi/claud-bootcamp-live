---

description: "Task list for Workshop Markdown Ebook"
---

# Tasks: Workshop Markdown Ebook

**Input**: Design documents from `/specs/006-workshop-ebook/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/](contracts/), [quickstart.md](quickstart.md)

**Tests**: No TDD unit tests were requested. The plan's testing approach is a single shell-based **validation gate** (`scripts/check-ebook.sh`) that asserts the structural contract (ST-1..ST-9). It is treated as build infrastructure, not per-story unit tests.

**Organization**: Tasks are grouped by user story (US1=P1, US2=P2, US3=P3) so each can be implemented and validated independently.

> **Manifest format note**: The plan/data-model illustrate a `manifest.yml`. To honor Constitution Principle X (stdlib-only, no new dependencies — Python stdlib has no YAML parser), the implementation uses **`scripts/ebook/manifest.json`** parsed with the stdlib `json` module. This supersedes the `.yml` illustration; all structure/fields are unchanged.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story the task belongs to
- All paths are repository-root-relative

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project scaffolding and the declarative manifest.

- [X] T001 Create the tooling directory `scripts/ebook/` and the gitignored output directory `book/dist/` (add a `book/dist/.gitkeep` only if needed locally; do not commit generated output).
- [X] T002 [P] Add `book/dist/` to [.gitignore](.gitignore) (mirror the existing `slides/dist/` precedent).
- [X] T003 [P] Create `scripts/ebook/manifest.json` per [data-model.md](data-model.md): `metadata` (title, subtitle, instructor, edition, include_solutions), `front_matter.source`, ordered `chapters[]` (parts 01–11 with `slide`/`exercise`/`solution` paths; part 11 has null exercise/solution), and `back_matter[]` (`skills/README.md`).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Reusable transformer primitives every user story depends on. No chapter/front/back-matter assembly here — only the building blocks.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T004 Create `scripts/ebook/build_ebook.py` skeleton: `argparse` CLI (`--manifest`, `--output`, `--no-solutions`) and a `main()` returning the exit codes from [contracts/build-cli.md](contracts/build-cli.md) (0 success, 2 missing/invalid source, 1 unexpected).
- [X] T005 [US-shared] Implement manifest loading + fail-fast source validation in `scripts/ebook/build_ebook.py`: parse `manifest.json` with stdlib `json`, and exit 2 if any non-null `slide`/`exercise`/`solution`/`front_matter.source`/`back_matter` path is missing.
- [X] T006 [P] Implement the Marp-stripping function(s) in `scripts/ebook/build_ebook.py` per research Decision 3: remove leading YAML frontmatter, all `<!-- ... -->` comment blocks (directives + multi-line SPEAKER NOTES), unwrap/drop HTML slide chrome (`<span class=...>`, `<img class=...>`, other class-bearing tags), and convert standalone `---` slide separators to soft paragraph breaks.
- [X] T007 [P] Implement heading normalization in `scripts/ebook/build_ebook.py` per research Decision 4: demote each deck's headings beneath a single chapter `##`, and generate chapter-scoped slug anchors (e.g., `01-...`) that stay unique across repeated subheadings.
- [X] T028 [P] Implement content image + diagram handling in `scripts/ebook/build_ebook.py` (FR-010, spec Edge Cases): preserve content images as standard Markdown `![]()` (rewriting relative `src` to repo-absolute paths/URLs) and preserve fenced ```mermaid``` blocks; drop only decorative slide chrome (`hero-icon` etc.). Diagrams that cannot render MUST degrade to readable text, not raw HTML.
- [X] T008 Implement the link map + link-rewriting in `scripts/ebook/build_ebook.py` per research Decision 5: build path→anchor map from the manifest; rewrite relative cross-file links to in-document anchors when the target is included, else to absolute repo URLs or plain text (depends on T005, T007).
- [X] T009 Create `scripts/build-ebook.sh` Bash wrapper per [contracts/build-cli.md](contracts/build-cli.md): self-locate repo root, parse `--output`/`--no-solutions`/`--manifest`/`--help`, create the output dir, invoke `python3 scripts/ebook/build_ebook.py ...`, print the one-line summary, and `chmod +x`.

**Checkpoint**: Transformer primitives and the build entrypoint exist; assembly can now be layered per story.

---

## Phase 3: User Story 1 - Read the whole workshop as one self-contained ebook (Priority: P1) 🎯 MVP

**Goal**: A single Markdown file with a title page, a working table of contents, and all 11 parts in order as clean prose.

**Independent Test**: Run `scripts/build-ebook.sh`; open `book/dist/claude-code-bootcamp-ebook.md` and confirm one H1 title, a TOC whose links resolve, and chapters `## 01.`..`## 11.` in order as readable prose with no raw Marp markup.

### Implementation for User Story 1

- [X] T010 [US1] Implement chapter assembly in `scripts/ebook/build_ebook.py`: for each manifest chapter, load its `slide`, apply Marp-stripping (T006), heading normalization (T007), and link rewriting (T008), and emit a `## NN. Title` chapter using the slide frontmatter `title:`.
- [X] T011 [US1] Implement a minimal front matter block in `scripts/ebook/build_ebook.py`: single `#` book title + title-page metadata (title, subtitle, instructor, edition) from `metadata`.
- [X] T012 [US1] Implement table-of-contents generation in `scripts/ebook/build_ebook.py`: list all 11 chapters in order with links to their chapter-scoped anchors (FR-003, ST-2, ST-3).
- [X] T013 [US1] Implement the document writer in `scripts/ebook/build_ebook.py`: concatenate front matter + TOC + ordered chapters and write to `--output` (default `book/dist/claude-code-bootcamp-ebook.md`); print the summary line.
- [X] T014 [US1] Run `scripts/build-ebook.sh` and manually verify ST-1, ST-2, ST-3, ST-6 against [contracts/ebook-structure.md](contracts/ebook-structure.md) (one H1, ordered chapters, working TOC, no surviving Marp markup).

**Checkpoint**: MVP — the full workshop is readable end-to-end from a single file.

---

## Phase 4: User Story 2 - Practice with the hands-on exercises inside the ebook (Priority: P2)

**Goal**: Each chapter 01–10 embeds its exercise brief, with a reachable reference-solution appendix.

**Independent Test**: Build the ebook; confirm each chapter 01–10 has a "Hands-on exercise" subsection and (with solutions enabled) a "Solution" subsection reachable from the TOC.

### Implementation for User Story 2

- [X] T015 [US2] Extend chapter assembly in `scripts/ebook/build_ebook.py`: for chapters whose manifest `exercise` is non-null, append the exercise brief (`exercises/part-NN/README.md`) under a chapter-scoped "Hands-on exercise" subsection (FR-005, ST-4).
- [X] T016 [US2] Implement solution inclusion in `scripts/ebook/build_ebook.py`: when `include_solutions` is true and `--no-solutions` is not set, gather files from each chapter's `solution/` dir into a clearly labeled "Solution" subsection reachable via TOC; honor the `--no-solutions` toggle and state exclusion in the intro when off (FR-011, ST-5).
- [X] T017 [US2] Apply Marp-stripping/link-rewriting consistently to embedded exercise and solution content (e.g., rewrite intra-repo links, fenced code preserved) so no broken internal links remain (FR-007, ST-7).
- [X] T018 [US2] Run `scripts/build-ebook.sh` and verify ST-4, ST-5 and the `--no-solutions` path produce the expected sections.

**Checkpoint**: The ebook is a complete self-study resource with exercises and solutions.

---

## Phase 5: User Story 3 - Front matter, navigation, and supporting material (Priority: P3)

**Goal**: Polished front matter (intro + prerequisites/pre-work) and back matter (skills overview + certification/next-steps appendix).

**Independent Test**: Build the ebook; confirm it opens with a title page + "How to use this book" intro + prerequisites, and ends with a Skills Library appendix and a Certification & Next Steps appendix.

### Implementation for User Story 3

- [X] T019 [US3] Extend front matter in `scripts/ebook/build_ebook.py`: add a "How to use this book" introduction (stating whether solutions are included) and a prerequisites/pre-work section, sourced from `front_matter.source` (`README.md`) and the certification line (FR-002, ST-8).
- [X] T020 [P] [US3] Implement the Skills Library appendix in `scripts/ebook/build_ebook.py`: append `skills/README.md` (stripped + link-rewritten) as "Appendix A — Skills Library" (FR-006, ST-8).
- [X] T021 [P] [US3] Implement the Certification & Next Steps appendix in `scripts/ebook/build_ebook.py`: derive **certification logistics only** (pass thresholds, weighting, certificate issuance) from `manifest.back_matter.certification` (`README.md`) as "Appendix B". Do NOT re-emit the part-11 deck here — chapter 11 already covers Q&A/next-steps narrative (D1 boundary in [data-model.md](data-model.md)) (FR-006, ST-8).
- [X] T022 [US3] Ensure both appendices are linked from the table of contents (T012) and use unique chapter-scoped anchors.
- [X] T023 [US3] Run `scripts/build-ebook.sh` and verify ST-8 (front matter title page + intro; back matter skills + certification appendices present).

**Checkpoint**: All three stories functional; the ebook reads as a complete book.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation gate, integration, and docs.

- [X] T024 Create `scripts/check-ebook.sh` per [contracts/build-cli.md](contracts/build-cli.md): build to a temp path and assert ST-1..ST-9 from [contracts/ebook-structure.md](contracts/ebook-structure.md), printing PASS/FAIL per assertion; exit 0 only if all pass; `chmod +x`.
- [X] T025 Wire `scripts/check-ebook.sh` into [scripts/validate.sh](scripts/validate.sh) so release readiness enforces the ebook contract.
- [X] T026 [P] Run the full [quickstart.md](quickstart.md) flow end-to-end (`build-ebook.sh` → `check-ebook.sh`, plus `--no-solutions` and `--output` options) and confirm SC-001..SC-006 hold, including FR-010 (images/diagrams render) via T028.
- [X] T027 [P] Add a short "Workshop ebook" subsection to [README.md](README.md) (Build section) documenting `scripts/build-ebook.sh` / `scripts/check-ebook.sh` and the gitignored output path.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately.
- **Foundational (Phase 2)**: Depends on Setup. BLOCKS all user stories.
- **User Stories (Phase 3–5)**: All depend on Foundational. US1 is the MVP. US2 and US3 extend the same assembler; they are independently testable but, since they edit the same `build_ebook.py`, are best sequenced US1 → US2 → US3 to avoid merge churn.
- **Polish (Phase 6)**: Depends on the desired user stories being complete (the gate needs assertions for whatever is implemented).

### Within Each User Story

- US1: chapter assembly (T010) → front matter (T011) → TOC (T012) → writer (T013) → verify (T014).
- US2: exercise embed (T015) → solutions (T016) → link consistency (T017) → verify (T018).
- US3: front matter (T019) → appendices (T020/T021 parallel) → TOC links (T022) → verify (T023).

### Parallel Opportunities

- T002 and T003 (Setup) can run in parallel.
- T006, T007, and T028 (independent transformer functions) can run in parallel.
- T020 and T021 (separate appendix builders) can run in parallel.
- T026 and T027 (validation run vs. README docs) can run in parallel.
- Note: most US tasks touch the single file `scripts/ebook/build_ebook.py`, so they are sequential within and across stories despite different concerns.

---

## Parallel Example: Phase 2 Foundational

```bash
# Independent transformer primitives (different functions, no shared state):
Task T006: "Implement Marp-stripping in scripts/ebook/build_ebook.py"
Task T007: "Implement heading normalization + chapter-scoped anchors in scripts/ebook/build_ebook.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Phase 1: Setup (T001–T003).
2. Phase 2: Foundational (T004–T009) — CRITICAL, blocks all stories.
3. Phase 3: User Story 1 (T010–T014).
4. **STOP and VALIDATE**: build the ebook and confirm it reads end-to-end with a working TOC and no Marp markup. This alone is a shippable MVP.

### Incremental Delivery

- Add **US2** (T015–T018) to make it a hands-on self-study resource.
- Add **US3** (T019–T023) for polished front/back matter.
- Finish with **Polish** (T024–T027): the validation gate, `validate.sh` integration, quickstart verification, and README docs.

---

## Task Summary

- **Total tasks**: 28
- **Setup (Phase 1)**: 3 (T001–T003)
- **Foundational (Phase 2)**: 7 (T004–T009, T028)
- **User Story 1 (P1, MVP)**: 5 (T010–T014)
- **User Story 2 (P2)**: 4 (T015–T018)
- **User Story 3 (P3)**: 5 (T019–T023)
- **Polish (Phase 6)**: 4 (T024–T027)
- **Parallel opportunities**: T002/T003, T006/T007/T028, T020/T021, T026/T027
- **Suggested MVP scope**: Phases 1–3 (User Story 1) → a single readable ebook of all 11 parts.
