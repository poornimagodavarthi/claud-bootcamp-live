# Reviewer-panel protocol — Feature 004 intermediate decks

**Modelled on**: `specs/003-slide-wow-polish/reviewer-panel-results.md`
**Status**: protocol authored; live panel run **deferred to human facilitation**.

## Why this is deferred

Tasks T059 (5-person dry-run reviewer panel) and T060 (instructor review) require live human reviewers projecting the decks, providing subjective feedback on visual rhythm, narrative flow, and instructional clarity. These are inherently human-judgement activities and are outside the scope of automated implementation.

## Panel composition

Recruit 5 reviewers spanning these archetypes:

1. **Returning learner** — completed feature 003 beginner decks; gauges continuity of the wow design language.
2. **First-time intermediate learner** — never saw the beginner course; gauges standalone clarity.
3. **Working developer (5+ yrs)** — gauges technical correctness of the live-demo flow and code snippets.
4. **Junior instructor** — gauges teach-ability of `## Instructor notes`, transition cues, and timing budget.
5. **Accessibility reviewer** — gauges colour contrast in live projection, font legibility from the back row, screen-reader rendering of SVG `<title>`/`<desc>`.

## What to measure

For each of the 10 intermediate modules:

| Axis | Question | Pass criterion |
|---|---|---|
| Visual rhythm | Does each slide feel composed, not crammed? | ≥ 4/5 reviewers say "yes" |
| Narrative flow | Do the 13 sections feel like one journey? | ≥ 4/5 say "yes" |
| SVG clarity | Does the Concepts SVG add insight vs noise? | ≥ 4/5 say "yes" |
| Timing | Does the declared duration feel honest? | ≤ 1 reviewer says "rushed" or "padded" |
| Instructor handoff | Could you teach this from the notes alone? | reviewer #4 says "yes" |

## How to capture results

After the panel:

1. Create `specs/004-intermediate-content-polish/reviewer-panel-results.md` with a row per module × axis × reviewer.
2. List action items in a follow-up section. Any actions must respect the verbatim-block rules (run `scripts/check-verbatim-blocks.sh` after each edit).
3. If actions span multiple modules, file them as a separate polish PR — do not bundle with the structural feature.

## Acceptance for marking T059/T060 complete

A task is complete when:

- [ ] `reviewer-panel-results.md` exists with all 5 reviewers × 10 modules × 5 axes filled.
- [ ] Each "fail" cell has a documented action item (or a documented decision to keep as-is).
- [ ] The audit script remains green after any action-item edits.

## What this feature delivers without the panel run

- Mechanical gates (verbatim audit, contrast, overflow, FR-018 build layout) all pass.
- All 10 decks rebuild cleanly to PPTX + PDF + HTML in the audience-first layout.
- All 10 teaching SVGs are present, structurally valid, and grayscale-recoverable.
- Beginner decks remain byte-identical to baseline (FR-012 PASS).
- The protocol above is ready to execute when reviewers are scheduled.
