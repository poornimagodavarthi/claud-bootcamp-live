# Research — Claude Code Beginner Course

**Feature**: `002-claude-beginner-course`  
**Phase**: 0 (Outline & Research)  
**Date**: 21 May 2026

This document resolves every NEEDS CLARIFICATION the spec and plan would otherwise carry into Phase 1. The five user-facing ambiguities were resolved in `spec.md` § Clarifications (Session 2026-05-21). The items below cover the remaining technical decisions inferred from the spec, the constitution, and the existing intermediate-course tooling.

---

## R1. Marp CLI invocation under Node v26

**Decision**: Invoke Marp exclusively via `npx --yes @marp-team/marp-cli@latest` from inside `slides/deploy-pptx.sh`. Do NOT rely on a globally installed `marp` binary.

**Rationale**: The currently installed global `marp` at `/opt/homebrew/bin/marp` is broken under Node v26 (yargs ESM/CJS `ReferenceError`). The intermediate course's PPTX build was completed only by bypassing the global binary with a direct `npx` invocation. Pinning the script to `npx --yes` makes the beginner build inherit the working path and removes the global-binary footgun for future contributors. `npx` is already permitted by Constitution Principle X (Marp CLI via npx fallback).

**Alternatives considered**:
- *Require contributors to uninstall the broken global*: brittle, depends on every machine being cleaned.
- *Downgrade to Node 20/22 LTS*: pushes a constraint into the contributor toolchain that the spec does not require.
- *Vendor a pinned Marp version in `package.json`*: introduces a new dependency surface (no `package.json` exists today); rejected for Minimal External Dependencies.

---

## R2. Deck discovery glob in `deploy-pptx.sh`

**Decision**: Change the deck discovery from a flat `slides/part-*.md` to a recursive `slides/**/part-*.md` (or equivalent `find slides -type f -name 'part-*.md'`), preserving the existing flat-glob output ordering for the intermediate decks and appending beginner decks in lexical order.

**Rationale**: FR-050 explicitly delegates the implementation choice to `/speckit.plan`. Recursive discovery is the lower-friction option: a new author drops a deck into `slides/beginner/part-NN-*.md` and the build picks it up automatically, with zero script edits. The alternative — a separate `--beginner` flag — doubles the surface area of the build script and creates a second place where deck lists can drift out of sync.

**Alternatives considered**:
- *Separate `slides/deploy-beginner-pptx.sh`*: violates the single-pipeline assumption in FR-050 and complicates instructor onboarding.
- *Explicit array of deck paths inside the script*: makes the script the single source of truth for "which decks exist," duplicating information that already lives on disk and in `slides/README.md` / `slides/beginner/README.md`.

---

## R3. Validator extension strategy

**Decision**: Extend `scripts/validate.sh` in place with a new section labeled `# --- Beginner course checks ---`, gated by `[[ -d slides/beginner ]]` so the intermediate-only test suite still passes if the beginner course is removed in isolation. Reuse the existing parallel-array bash-3.2 pattern (`BEG_DECK_SLUGS=(…)` + `BEG_DECK_MINS=(20 25 30 25 30 25 25 30)`), the existing forbidden-tokens regex (STRICT + LOOSE), and the existing HTML-comment stripping pre-pass.

**Rationale**: A single validator is what FR-051 requires and what Constitution Principle IX (Cross-Artifact Consistency) prefers. The gating `-d` check keeps the script safe when run from a partial checkout. Sharing the forbidden-tokens regex satisfies FR-055 by construction — there is exactly one regex, defined once.

**New checks added by this feature** (each emits `ok:` or `fail: <file>:<line>: <reason>`):

1. **Beginner deck 10-section check** — for each `slides/beginner/part-*.md`, assert exactly the 10 H2 headings of FR-011 appear in order. Heading texts: `What you'll learn`, `Why this matters`, `The one concept`, `Show me`, `Try it yourself`, `Common mistakes`, `Lesson reflection`, `What's next`, `Glossary card` (the title slide is the deck's H1, not an H2).
2. **Beginner deck duration marker** — assert each beginner deck contains `<!-- duration: NN min -->` with NN matching the canonical budget (20/25/30/25/30/25/25/30 by part number).
3. **Beginner deck content-slide cap** — assert each beginner deck has ≤ 12 content slides (count of `---` slide separators in the body, excluding title and glossary).
4. **Beginner exercise 7-section check** — for each `exercises/beginner/part-*/README.md`, assert exactly the 7 H2 headings of FR-021 appear in order: `What you'll build`, `Before you start`, `Step-by-step`, `The prompt to paste`, `How to know it worked`, `If something went wrong`, `You did it!`.
5. **Beginner exercise scaffolding check** — for each `exercises/beginner/part-NN/`, assert `starter/` exists and is non-empty (`find starter -type f` non-zero), and `solution/` exists and contains at least one non-empty file. Module 00 setup is exempt (no solution required; its deliverable is the learner's `first-prompt.txt`).
6. **Forbidden-tokens regex** — same STRICT+LOOSE patterns already in place; the glob now also covers `slides/beginner/**`, `exercises/beginner/**`, `assessments/beginner/**`, `GLOSSARY.md`, and the three top-level `beginner-*.md` files.
7. **Beginner duration sum** — sum the 8 beginner durations and assert `200 ≤ sum ≤ 240` (per SC-008).
8. **Glossary character-identity check** — for each beginner deck, extract every term shown on its "Glossary card" slide and look up the same term in `GLOSSARY.md`. The one-line definition MUST match byte-for-byte. Mismatch → fail with `file:line: glossary drift for term '<term>'`. Implementation: extract pairs as `term => definition` from both sources, diff them.
9. **Beginner quiz coverage** — assert `assessments/beginner/quiz.md` contains exactly 16 numbered questions and exactly 2 per module (matched by a `<!-- module: NN -->` tag adjacent to each question, per spec Key Entities).
10. **Cross-references** — assert `README.md` contains a link to `beginner-student-guide.md` and a link to `slides/beginner/README.md`; assert `beginner-student-guide.md` contains a link to `assessments/beginner/quiz.md` and to `beginner-certificate-template.md`.
11. **Optional skills check** — if `skills/beginner/` exists and contains any `SKILL.md`, apply the existing 6-section SKILL contract to each. If the directory is empty or missing, emit `ok: skills/beginner (optional)` and continue.

**Alternatives considered**:
- *Fork the validator into `scripts/validate-beginner.sh`*: duplicates the forbidden-tokens regex, the HTML-comment stripping, and the bash-3.2 utility helpers. Rejected.
- *Express the section contracts as JSON schemas and load them at validator runtime*: introduces a JSON parser dependency to bash, which violates Principle X.

---

## R4. Capstone grader (`scripts/check-beginner-capstone.sh`) shape

**Decision**: Pure bash 3.2 script taking `<path-to-notes.py>` as `$1`. Steps:

```text
1. Resolve the input path; abort with usage on missing arg or non-readable file.
2. mktemp -d a tmp working dir; trap-cleanup on exit.
3. cd into the tmp dir; copy notes.py into it (so notes.json is created in the tmp dir).
4. Run `python3 notes.py add "hello"`     → capture stdout/stderr/exit code.
5. Run `python3 notes.py list`            → assert stdout contains "hello".
6. Run `python3 notes.py delete 1`        → assert exit 0.
7. Run `python3 notes.py list`            → assert stdout no longer contains "hello".
8. On any failed assertion: print `FAIL: <reason>` and exit 1.
9. On success: compute `TOKEN=$(printf '%s' "$ALL_OUTPUTS" | shasum -a 256 | cut -c1-8)`
   and print `PASS <TOKEN>` on a single line; exit 0.
```

**Rationale**: This is the minimum viable contract that lets FR-044 / FR-046 be auditable. `shasum -a 256` is present by default on both macOS and Linux. The verification token is intentionally short (8 hex chars) so it fits on one certificate line and is easy to copy by hand. The token is deterministic given the same `notes.py` output, so two learners with identical correct solutions get the same token — that's acceptable for a "did it run?" check and is not meant as anti-cheat.

**Alternatives considered**:
- *Use Python for the grader*: works but doubles the language surface of the grading toolchain. Rejected; bash + `shasum` + `python3 notes.py` is sufficient.
- *Sign the token with an HMAC keyed off student name*: overkill for a self-paced beginner certificate; would require a key-distribution story.
- *Use `md5`*: not present by default on Linux as `md5` (it's `md5sum`); `shasum` is the portable choice.
- *Use only exit codes, no token*: makes the certificate unverifiable to a third party who didn't watch the script run — the explicit goal of Clarifications Q4.

---

## R5. `notes.py` reference solution architecture

**Decision**: Single-file `solution/notes.py`, ≤ 100 LOC including blank lines and comments. Uses only `sys`, `json`, `pathlib`. Stores state as a JSON list at `./notes.json`. Each note is `{"id": <int>, "text": <str>}`. `add` appends with `id = max(existing ids) + 1` (or 1 if empty); `list` prints `<id>\t<text>` lines; `delete <id>` removes the matching note (exit 1 with a one-line error if id missing). No third-party packages, no argparse (kept tiny: `sys.argv` dispatch). Unknown subcommand → print one-line usage on stderr, exit 2.

**Rationale**: This is the canonical solution the grader's expectations are pinned against. Keeping the dispatch hand-rolled (not argparse) makes the file fit comfortably under 100 LOC and is closer to what a beginner produces with Claude Code's help in 15 minutes. The `id` is integer (not UUID) so the grader's `delete 1` step is deterministic.

**Alternatives considered**:
- *SQLite persistence*: violates "no third-party deps" only nominally (sqlite3 is stdlib) but exceeds the beginner's expected mental model for module 08.
- *argparse*: more idiomatic at intermediate level but blows the LOC budget and introduces a concept (declarative arg parsing) not taught in any module.
- *Click/Typer*: third-party — forbidden by FR-033.

---

## R6. Marp deck conventions inherited from the intermediate course

**Decision**: Beginner decks use the same Marp frontmatter and the same `<!-- _class: lead -->` pattern for title slides as `slides/part-01-setup-mindset.md`. Glossary card slides use a fixed two-column layout (`<!-- _class: split -->` if such a class exists; otherwise plain bullets) so the validator can extract `**term**: definition` pairs with a single regex.

**Rationale**: Visual consistency between the two courses lowers cognitive load for any learner moving from beginner to intermediate (User Story 4). The fixed glossary-card layout makes the character-identity check (R3.8) a one-line extraction.

**Alternatives considered**:
- *Distinct beginner theme*: doubles the build surface and is not justified by the spec.

---

## R7. Mermaid cross-course path diagram in `README.md`

**Decision**: A small Mermaid `flowchart LR` with three nodes: `[Start here: Beginner course]` → `[Intermediate bootcamp]` → `[Certificate]`. Rendered inline via GitHub's native Mermaid support; no extra render step required. Fallback ASCII is provided in a `<details>` block in case the reader is on a Mermaid-less Markdown renderer.

**Rationale**: FR-054 mandates "a single ASCII or Mermaid diagram." Mermaid renders natively on GitHub (the canonical reading surface for the repo) and is editable as text. The ASCII fallback covers offline viewing without forcing every viewer to install a renderer.

---

## R8. Workshop title brand string

**Decision**: `"Claude Code 101 — Beginner Workshop"` (per spec Assumptions; no further clarification needed). Used in `beginner-instructor-guide.md`, `beginner-certificate-template.md` (as `{{WORKSHOP_TITLE}}` default), and `slides/beginner/README.md`.

**Rationale**: Mirrors the Anthropic Academy "Claude 101" reference shape and is consistent with the existing brand line "LLM Engineering by Packt".

---

## R9. Reading-level target enforcement

**Decision**: Not enforced by the validator in v1. The constitution and FR-004 set the bar at "US high-school senior," but no portable shell-only readability scorer exists with acceptable accuracy. Reviewers enforce this at PR time; a follow-up feature MAY add a `vale` or `textstat`-based check.

**Rationale**: Adding a Python NLP dependency for one check violates Principle X. Manual review at PR time is acceptable for a course that ships < 5,000 lines of prose total.

**Alternatives considered**:
- *Ship `textstat` Python helper in `scripts/`*: rejected for the dependency reason above.
- *Use a `vale` style file*: viable; deferred to a follow-up to avoid scope creep in v1.

---

## R10. Skills directory absence handling

**Decision**: The validator treats `skills/beginner/` as optional (per Clarifications Q5 and FR-060). When absent, emit `ok: skills/beginner (optional, none authored)`; when present, apply the existing 6-section SKILL contract to each `SKILL.md` and the MIT-license header check. No minimum count.

**Rationale**: Q5 chose Option B (allow opportunistically), so authors must NOT be blocked at validation time by the absence of skills.

---

## Summary of decisions

| ID | Decision | Source |
|----|----------|--------|
| R1 | Marp via `npx --yes`; no global binary | Constitution X, intermediate-course build experience |
| R2 | Recursive `slides/**/part-*.md` discovery in `deploy-pptx.sh` | FR-050 |
| R3 | Single `validate.sh` extended in place, gated by `-d slides/beginner` | FR-051, Principle IX |
| R4 | Bash 3.2 grader; `PASS <8-hex-token>` via `shasum -a 256` | Clarifications Q4, FR-045 |
| R5 | Single-file `notes.py`; stdlib-only; integer ids; JSON list | Clarifications Q3, FR-033 |
| R6 | Reuse intermediate Marp theme; fixed glossary-card layout | User Story 4, R3.8 |
| R7 | Mermaid path diagram in README with ASCII fallback | FR-054 |
| R8 | Workshop title `"Claude Code 101 — Beginner Workshop"` | Spec Assumptions |
| R9 | Reading-level check is manual at PR time in v1 | Principle X |
| R10 | `skills/beginner/` is optional; validator never fails on absence | Clarifications Q5, FR-060 |

All NEEDS CLARIFICATION markers from the Technical Context are now resolved.
