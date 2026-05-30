# Phase 0 Research: Workshop Markdown Ebook

All Technical Context items were resolvable from the existing repository; there were no open `NEEDS CLARIFICATION` markers in the spec. This document records the key decisions and the alternatives considered.

## Decision 1: Generate from source vs. hand-author the ebook

- **Decision**: Generate the ebook by transforming and concatenating existing source files (slides, exercises, README) via a repeatable script.
- **Rationale**: Constitution Principle IX (Cross-Artifact Consistency) and FR-009/SC-006 require the ebook to stay in sync with canonical content. Hand-authoring would immediately drift and double maintenance.
- **Alternatives considered**: (a) Manually write a standalone book — rejected: drift + duplicate effort. (b) Maintain the book as the source and back-port to slides — rejected: violates Principle III (Marp decks are the slide source of truth).

## Decision 2: Tooling — Bash + Python 3.11 stdlib

- **Decision**: A thin `scripts/build-ebook.sh` wrapper invoking `scripts/ebook/build_ebook.py` (Python standard library only).
- **Rationale**: Python 3.11 and Bash are already mandatory prerequisites (README pre-work). Text transformation (regex stripping of Marp syntax, heading re-leveling, link rewriting) is far cleaner in Python than pure Bash. Principle X forbids new runtime dependencies; stdlib-only respects this.
- **Alternatives considered**: (a) Pandoc — rejected: new heavy dependency, overkill for Markdown→Markdown. (b) Node/Marp — rejected: Marp is for slide rendering, not prose extraction; adds Chromium. (c) Pure Bash/sed — rejected: brittle for multi-line directive/speaker-note stripping.

## Decision 3: Marp artifact stripping rules

Slide decks contain presentation-only constructs that must not appear as prose. The transformer removes/normalizes:

- **YAML frontmatter** (`--- ... ---` at file start: `marp:`, `theme:`, `header:`, etc.) — removed.
- **HTML comment blocks** — two kinds: Marp directives (`<!-- _class: ... -->`, `<!-- duration: ... -->`, `<!-- _paginate: false -->`) and multi-line `SPEAKER NOTES` blocks. Both removed entirely.
- **Slide separators** (`---` on their own line) — converted to soft section breaks (blank line) rather than Markdown horizontal rules, so chapters read continuously.
- **HTML slide chrome** (`<span class="module-chip">`, `<img class="hero-icon">`, other class-bearing tags) — stripped or unwrapped to plain text/standard Markdown; decorative-only elements dropped.
- **Decision**: Implement as ordered regex passes with explicit, testable patterns; the validation gate asserts none of these constructs survive (SC-004).
- **Rationale**: Deterministic, inspectable, and matches the existing `scripts/check-verbatim-blocks.sh` style of content gating.

## Decision 4: Heading hierarchy and anchors

- **Decision**: Each part becomes a single `##` chapter under a top-level `#` book title; the deck's existing `#`/`##` headings are demoted one or more levels and prefixed/scoped per chapter so repeated titles (e.g., "Summary") remain unambiguous. The table of contents is generated from the final, de-duplicated heading set.
- **Rationale**: FR-003/FR-008/SC-002 require working TOC links and unambiguous navigation within one document. GitHub-style slug generation collides on duplicate headings; scoping by chapter avoids broken/duplicated anchors.
- **Alternatives considered**: Keeping raw deck heading levels — rejected: produces multiple `#` titles and colliding anchors in one file.

## Decision 5: Link rewriting for an ebook-only reader

- **Decision**: Relative links between source files (e.g., a slide linking to `exercises/part-03/README.md`, or README links like `student-guide.md#...`) are rewritten to in-document anchors when the target is included in the ebook, or converted to absolute repository URLs / plain text when the target is excluded.
- **Rationale**: FR-007/SC-005 require zero broken internal links for a reader who only has the ebook. A link map (built from the manifest) drives the rewrite.
- **Alternatives considered**: Leaving relative links untouched — rejected: every cross-file link breaks for an ebook-only reader.

## Decision 6: Exercise + solution placement

- **Decision**: For parts 01–10, append the exercise brief (`exercises/part-NN/README.md`) to that part's chapter under a clear "Hands-on exercise" subsection; reference solutions are collected into a labeled appendix section per chapter (or a back-matter appendix), reachable via TOC.
- **Rationale**: FR-005/FR-011/SC-003. Keeps reading flow (concepts → exercise) while keeping solutions discoverable but not spoiling the exercise inline.
- **Alternatives considered**: Excluding solutions — allowed by FR-011 only if stated in the intro; rejected as default because the spec assumption favors a complete self-study resource.

## Decision 7: Output location and gitignore

- **Decision**: Write to `book/dist/claude-code-bootcamp-ebook.md`; add `book/dist/` to `.gitignore`. Commit only the script, manifest, and validation gate.
- **Rationale**: Mirrors the established `slides/dist/` gitignored build-artifact pattern (Principle III) and keeps generated content out of version control.

## Decision 8: Validation gate

- **Decision**: `scripts/check-ebook.sh` builds the ebook to a temp/dist path and asserts: (1) all 11 parts present in order, (2) exercises for parts 01–10 present, (3) no surviving Marp frontmatter/directives/speaker-note markers, (4) no broken in-document anchors, (5) front matter + back matter present. Wire it into `scripts/validate.sh`.
- **Rationale**: Directly maps to SC-001..SC-006 and matches the repo's existing `check-*.sh` gate convention so release readiness can enforce it.
