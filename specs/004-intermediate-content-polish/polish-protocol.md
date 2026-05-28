# Intermediate content polish protocol (T027–T036)

**Status**: protocol authored; per-deck polish passes **deferred to human editor**.

## Why this is deferred

The Phase 4 user story (US2 — Content polish) calls for tightening the five **editable** sections of each intermediate deck:

| Section anchor | Treatment |
|---|---|
| `## Why this matters` | tighten prose |
| `## Concepts` | tighten prose (SVG embed exempt — `![w:760](...)` lines are filtered from word counts) |
| `## Common mistakes` | tighten prose (per clarification Q5: no verbatim carve-out) |
| `## Instructor notes` | tighten prose |
| `## Transition` | tighten prose |

The remaining nine section anchors are **protected** (verbatim) and may not be touched:

- `## Promise`, `## Suggested Claude Code prompts`, `## Deliverable checklist`, `## Definition of done`, `## Step-by-step lab` (5 categories under FR-010)
- Plus all cover/Title slides and the `## Live demo flow`, `## Mini project`, `## Review checkpoint` slides (untouched at the H2 anchor; only their slide-class markers were added in Phase 3).

**Tightening is a value judgement** — what to cut, what to keep, where the rhythm wants a comma — and is inherently outside the scope of mechanical scripting. The infrastructure work (theme, audit, gates, SVGs) is complete in this feature; the prose polish itself is staged for the next editorial pass.

## How to run the polish pass

For each module 1–10:

1. Read the five editable sections side-by-side with the audience-deck (`slides/beginner/part-NN-*.md`) when applicable.
2. Apply **tighten-only** edits — kill hedges (`really`, `just`, `actually`), collapse redundant clauses, replace nominalisations with verbs.
3. After each section save, run:

   ```sh
   scripts/check-verbatim-blocks.sh
   ```

   - Word-count delta for that section must be **≤ 0** (else exit 2).
   - Protected blocks must remain byte-identical (else exit 1).
   - Beginner decks must be byte-identical to baseline (else exit 4).

4. Append a one-line entry to the polish-log comment at EOF of the deck:

   ```markdown
   <!-- polish-log
   (intermediate-content-polish feature 004) — populated during US2 polish pass.

   YYYY-MM-DD  Why -8w / Concepts -12w / Mistakes -5w / Instructor -7w / Transition -4w
   -->
   ```

5. After all 10 decks are polished, re-run the full audit + build:

   ```sh
   scripts/check-verbatim-blocks.sh
   slides/deploy-pptx.sh --all
   scripts/check-slide-overflow.sh --budget 22 slides/dist/intermediate/html
   ```

## Acceptance for marking T027–T036 complete

A task `T0NN Polish Module M` is complete when **all** of:

- [ ] `scripts/check-verbatim-blocks.sh` returns exit 0 with that deck's row showing **≥ 1 negative delta** (positive deltas remain forbidden).
- [ ] Polish-log entry added to the deck EOF with date + per-section word delta.
- [ ] Module-M PPTX builds without overflow.
- [ ] Beginner decks remain byte-identical to baseline (`PASS [FR-012]`).

## What this feature delivers without the polish pass

Even without per-deck tightening:

- All 10 intermediate decks already use the new `wow-intermediate` theme.
- All 10 teaching SVGs are authored and embedded on the Concepts slide.
- The audit script is green (all deltas = 0, all protected blocks unchanged, beginner decks untouched).
- The build emits to the FR-018 audience-first layout (`slides/dist/intermediate/{pptx,pdf,html}/`).
- The polish-log scaffold sits at the EOF of every deck, ready for the editor.
