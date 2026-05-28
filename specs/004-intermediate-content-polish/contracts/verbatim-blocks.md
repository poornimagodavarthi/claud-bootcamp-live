# Contract — Verbatim Blocks

**Feature**: 004 Intermediate Course Content Polish
**Consumers**: `scripts/check-verbatim-blocks.sh` (the audit script), human reviewers.

This contract is the machine-readable companion to FR-010 + Q2 + Q5. It defines, **for every intermediate deck**, the 5 protected-block categories (byte-identical to pre-polish) and the 5 editable-section categories (post-polish word count ≤ pre-polish).

The baseline reference is `git merge-base HEAD main` for branch `004-intermediate-content-polish`. All "pre-polish" extractions read from that ref.

---

## Per-deck extraction patterns

Each deck contains a stable set of H2 headings (Constitution Principle II). The audit script uses these awk anchors to extract each block's body:

| Section kind | Anchor regex (H2 header) | Body extraction rule |
|---|---|---|
| `Promise` | `^## (Promise|This module promises)` | Numbered list immediately following; ends at next H2. |
| `WhyThisMatters` | `^## Why this matters` | Body until next H2. |
| `Concepts` | `^## Concepts` | Body until next H2, EXCLUDING any image embed (`![…](…)`) and EXCLUDING any HTML comment. |
| `LiveDemoFlow` | `^## Live demo flow` | Numbered list/procedure until next H2. |
| `MiniProject` | `^## Mini project` | Body until next H2. |
| `StepByStepLab` | `^## Step-by-step lab` | Numbered steps until next H2. |
| `SuggestedClaudeCodePrompts` | `^## Suggested Claude Code prompts` | All ` ```text … ``` ` fences inside the section. |
| `DeliverableChecklist` | `^## Deliverable checklist` | All `- [ ]` lines. |
| `DefinitionOfDone` | `^## Definition of done` | All lines starting with `✅`. |
| `ReviewCheckpoint` | `^## Review checkpoint` | Body until next H2. |
| `CommonMistakes` | `^## Common mistakes` | Bullet list until next H2. |
| `InstructorNotes` | `^## Instructor notes` | Body until next H2. |
| `TransitionToNext` | `^## Transition to next module` | Body until end of file (excluding the `polish-log` HTML comment). |

---

## Protected (verbatim) categories — FR-010 a..e

For each deck, the audit MUST confirm post-polish `body` is byte-identical to pre-polish `body` (after a single trailing-newline normalisation):

| # | Section kind | FR-010 letter | Rationale |
|---|---|---|---|
| 1 | `Promise` (numbered list portion only) | a | Defines the testable learner capabilities; rubric anchors here. |
| 2 | `SuggestedClaudeCodePrompts` (every fence) | b | Students copy-paste these into Claude Code; one character change breaks the demo. |
| 3 | `DeliverableChecklist` (every `- [ ]` line) | c | Self-verification anchors (Constitution VI). |
| 4 | `DefinitionOfDone` (every ✅ line) | d | Same. |
| 5 | `StepByStepLab` (every numbered step) | e | Lab reproducibility. |

**Audit assertion**: for every `(deck, category)` pair, `sha256(body_post) == sha256(body_pre)`. On mismatch, the script prints a unified diff and exits non-zero.

---

## Editable (tighten-only) categories — Q2 + Q5

For each deck, the audit MUST confirm post-polish `wc -w(body)` ≤ pre-polish `wc -w(body)`:

| # | Section kind | Editable rule (FR-010 tighten-only) |
|---|---|---|
| 1 | `WhyThisMatters` | Shorten; no factual additions; no reordering. |
| 2 | `Concepts` (prose only; SVG embed exempt) | Tighten supporting one-liners; preserve bolded terms. |
| 3 | `CommonMistakes` | Shorten phrasing; preserve every failure-mode + corrective-action. |
| 4 | `InstructorNotes` | Drop hedging language; keep timing cues. |
| 5 | `TransitionToNext` | Single-sentence bridge preferred. |

**Audit assertion**: for every `(deck, editable_section)` pair, `delta_words = wc(post) − wc(pre)`; require `delta_words ≤ 0`. The script prints a 10×5 grid of deltas (10 decks × 5 sections). On any positive delta the script exits non-zero.

---

## Implicit-preservation categories

These section kinds are neither verbatim-listed in FR-010 nor in the editable list — they MUST remain unchanged by virtue of exclusion:

- `Title` (the H1 cover) — module title is part of the canonical 10-project list (Constitution IX).
- `MiniProject` — the GOAL paragraph and project framing.
- `LiveDemoFlow` — the demo procedure (numbered steps).
- `ReviewCheckpoint` — the checkpoint Qs.

If the audit detects any change to these, it prints a warning (not an error) so the author can confirm whether the edit was intentional. The warning becomes an error if the change adds or removes a slide entirely (`<!-- _class: -->` directives or H2 headings touched).

---

## Cross-deck invariants

| Invariant | SC | Audit step |
|---|---|---|
| Sum of declared durations across the 10 decks = 240 min | SC-009 | `grep -h '<!-- duration:' slides/part-*.md | awk -F'[: ]+' '{s+=$3} END{exit (s==240?0:1)}'` |
| Exactly 10 intermediate teaching SVGs exist | FR-004 | `ls slides/intermediate/assets/[0-1][0-9]-*.svg | wc -l` → expect 10 |
| Every deck declares `theme: wow-intermediate` | FR-002 | `grep -L '^theme: wow-intermediate' slides/part-*.md` → expect empty |
| Every deck has exactly one `tpl-demo` slide | FR-003 | `grep -c '<!-- _class: tpl-demo -->' slides/part-*.md` → expect 1 per file |
| Beginner decks untouched | FR-012 | `git diff --stat $(merge-base HEAD main) -- slides/beginner/` → expect empty |

---

## Script invocation contract

```bash
./scripts/check-verbatim-blocks.sh [--baseline <git-ref>] [--quiet]
```

| Flag | Default | Behaviour |
|---|---|---|
| `--baseline <ref>` | `$(git merge-base HEAD main)` | Git ref to extract pre-polish bodies from. |
| `--quiet` | off | Suppress the per-section delta grid; print only PASS/FAIL summary + non-zero exit. |

**Exit codes**:

- `0` — all 5 protected categories byte-identical across 10 decks AND all 5 editable categories delta ≤ 0 AND all cross-deck invariants pass.
- `1` — at least one protected-block mismatch (verbatim violation).
- `2` — at least one editable-section delta > 0 (tighten-only violation).
- `3` — at least one cross-deck invariant failed.
- `4` — beginner-deck diff non-empty (FR-012 violation).

The script is the single source of truth for SC-010.
