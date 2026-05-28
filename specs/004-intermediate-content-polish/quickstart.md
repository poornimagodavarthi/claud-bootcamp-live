# Quickstart — Intermediate Course Content Polish

**Feature**: 004 Intermediate Course Content Polish
**Audience**: Workshop maintainer applying the wow design + content polish to the 10 intermediate decks, or a reviewer verifying the work.

---

## Prerequisites

- Repository cloned, on branch `004-intermediate-content-polish`.
- Feature 003 (`003-slide-wow-polish`) already merged to `main`; the wow design system shipped under `slides/themes/wow-beginner.css` + `slides/themes/fonts/` + `slides/themes/icons/`.
- Node.js ≥ 20, network access for the first `npx @marp-team/marp-cli@latest` fetch.
- ~10 minutes for a clean build; up to several hours for the content-polish pass across 10 decks.

```bash
# Confirm prerequisites
node --version            # expect v20+ (v26 known good)
git branch --show-current # expect 004-intermediate-content-polish
ls slides/themes/wow-beginner.css slides/themes/fonts slides/themes/icons
```

---

## Path 1 — End-to-end smoke build (5 min)

Use this to confirm the foundational pieces work before touching any module content.

```bash
# 1. Verify the new theme file exists and starts with the @import line
test -f slides/themes/wow-intermediate.css && head -1 slides/themes/wow-intermediate.css
# Expected first line: @import url('./wow-beginner.css');

# 2. Verify the intermediate assets directory exists
ls slides/intermediate/assets/ | head

# 3. Run a single-deck smoke build (Module 1, PPTX only)
rm -rf slides/dist
./slides/deploy-pptx.sh slides/part-01-setup-mindset.md --pptx
# Expected output: slides/dist/intermediate/pptx/part-01-setup-mindset.pptx
```

If the output lands under `slides/dist/intermediate/pptx/`, the FR-018 patch is in place.

---

## Path 2 — Apply the design to one module (US1 MVP)

This is the smallest independently-testable slice. Run this on Module 1 first; the same steps generalise to Modules 2–10.

```bash
# 1. Add front-matter
# Open slides/part-01-setup-mindset.md and ensure the YAML front-matter contains:
#   theme: wow-intermediate
#   header: 'Claude Code Bootcamp · Day 1 · Module 01'

# 2. Add per-slide class markers
# For each slide that fits a template, prepend Marp's per-slide class directive:
#   <!-- _class: tpl-cover -->
#   (then the slide H1 / H2 + content)
# Use this mapping for the 14 sections:
#   Title cover           → tpl-cover
#   Promise               → tpl-objectives
#   Why this matters      → (none; default body slide)
#   Concepts              → tpl-show       (this slide also embeds the SVG)
#   Live demo flow        → tpl-demo       (NEW class)
#   Mini project          → tpl-try
#   Step-by-step lab      → tpl-show       (code/transcript-heavy)
#   Suggested CC prompts  → tpl-try
#   Deliverable checklist → tpl-done
#   Definition of done    → tpl-done
#   Review checkpoint     → (none)
#   Common mistakes       → (none)
#   Instructor notes      → (none)
#   Transition to next    → tpl-next

# 3. Embed the teaching SVG on the Concepts slide
# Replace any pre-polish placeholder with:
#   ![Teaching visual: TCC loop](intermediate/assets/01-tcc-loop.svg)

# 4. Build PPTX + PDF for Module 1
./slides/deploy-pptx.sh slides/part-01-setup-mindset.md --pptx --pdf

# 5. Verify outputs
ls slides/dist/intermediate/{pptx,pdf}/part-01-setup-mindset.*
```

Open the PPTX in your viewer. The cover should show the bootcamp chip + the `terminal` hero icon; the Concepts slide should show the TCC-loop SVG; the Live-demo-flow slide should show the `tpl-demo` numbered-step treatment.

---

## Path 3 — Polish the editable prose (US2)

For each module, tighten the 5 editable sections under the **tighten-only** rule (FR-010 + Q2):

1. **Why this matters** — sharpen each sentence to name a concrete production risk or a measurable practice. Remove filler.
2. **Concepts** — keep the bold-headlined term list; tighten the supporting one-liner under each term.
3. **Common mistakes** — shorten phrasing; preserve every failure-mode + corrective-action pair (Edge Case rule).
4. **Instructor notes** — drop hedging language; keep timing cues.
5. **Transition to next** — single sentence: "Next module: <name>. <one-sentence bridge>."

**The hard constraint**: post-polish `wc -w` for each editable section MUST be ≤ pre-polish `wc -w`. No section may grow.

After polishing, append a `polish-log` HTML comment at the bottom of the deck:

```html
<!-- polish-log: 2026-05-29
  why-this-matters: -47 words
  concepts: -23 words
  common-mistakes: -12 words
  instructor-notes: -8 words
  transition-to-next: -3 words
-->
```

---

## Path 4 — Run the audit suite

The five automated gates that prove the feature is done.

```bash
# Gate 1 — Verbatim & word-count audit (US2)
./scripts/check-verbatim-blocks.sh
# Pass: exit 0; prints a 10-row table showing per-section word-count deltas (all ≤ 0).

# Gate 2 — Build pipeline (US4)
rm -rf slides/dist
time ./slides/deploy-pptx.sh --all > /tmp/post-polish-build.log 2>&1
# Pass: wall-clock ≤ 635.79 s (1.5 × the spec-003 baseline 423.86 s).

# Gate 3 — Overflow check (US4)
./scripts/check-slide-overflow.sh --budget 22 slides/dist/intermediate/html/
./scripts/check-slide-overflow.sh slides/dist/beginner/html/
# Pass: both report "OK" for every deck.

# Gate 4 — Contrast / WCAG AA (US5)
./scripts/check-contrast.sh slides/themes/wow-intermediate.css
# Pass: exit 0; every text/background pair ≥ AA threshold.

# Gate 5 — Beginner non-regression (US4)
git diff --stat $(git merge-base HEAD main) -- slides/beginner/
# Pass: empty output (no beginner deck modified).

# Bonus — Duration lock (SC-009)
grep -h '<!-- duration:' slides/part-*.md | awk -F'[: ]+' '{s+=$3} END{print s}'
# Pass: prints exactly 240
```

If all five gates pass, the automated half of the feature is complete.

---

## Path 5 — Deferred human reviewer panels (US1 + US3 + US5)

These three Success Criteria require human reviewers. The protocols are inherited from `specs/003-slide-wow-polish/reviewer-panel-results.md` — re-use them verbatim with the intermediate artefacts.

| SC | Panel | n | Artefacts shown | Pass threshold |
|---|---|---|---|---|
| SC-001 | First-impression | 5 | 10 cover slides as PNG thumbnails | ≥ 4/5 positive adjectives on ≥ 8/10 covers; 0/5 say "plain/default/amateur/busy" |
| SC-004 | Visual-only comprehension | 8 | 10 Concepts slides with body text blanked, only the SVG visible | ≥ 6/8 reviewers correctly name the lesson on ≥ 7/10 visuals |
| SC-008 | Colorblind audit | 1 reviewer + tooling | One slide per `tpl-*` class run through deuteranopia + protanopia simulators | Every color-coded element's meaning recoverable from icon + label |

Record results in `specs/004-intermediate-content-polish/reviewer-panel-results.md` (create when running panels).

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Theme 'wow-intermediate' not found` | `slides/themes/wow-intermediate.css` missing or `deploy-pptx.sh --theme-set` not applied | Confirm the file exists; confirm the feature-003 patch in `deploy-pptx.sh` adds `--theme-set slides/themes/`. |
| Build output still under `slides/dist/{pptx,pdf,html}/` (flat) | FR-018 patch not applied to `deploy-pptx.sh` | Verify the three Marp invocations write to `--output slides/dist/<audience>/<format>/<basename>.<format>`. |
| `check-verbatim-blocks.sh` reports a protected-block mismatch | An editable-section tighten accidentally crossed into a protected block | Compare with `git show HEAD:slides/part-NN-*.md` for the exact pre-polish text; restore the protected block byte-for-byte. |
| `check-verbatim-blocks.sh` reports a positive word-count delta | An editable section grew | Tighten further; the rule is one-way (≤ 0). |
| Build exceeds 635.79 s | Likely a Chromium re-fetch or an SVG with embedded raster | Confirm `~/.cache/marp-cli` is warm; verify all SVGs are pure vector (no `<image href=…>`). |
| `check-slide-overflow.sh` flags a slide | A polished section split or a teaching SVG is too tall | If the offender is the Concepts slide, lower the SVG's `viewBox` height proportionally; otherwise re-tighten the section's prose. |
| `git diff --stat … slides/beginner/` shows changes | Accidental beginner-deck edit | `git checkout main -- slides/beginner/<file>` to restore. |

---

## Definition of Done for this feature

- All 10 intermediate decks: `theme: wow-intermediate`, `header:` set, `tpl-*` markers applied, teaching SVG embedded, editable sections tightened, polish-log appended.
- `slides/themes/wow-intermediate.css` exists; starts with `@import url('./wow-beginner.css');`; adds only `.tpl-demo`.
- 10 SVGs under `slides/intermediate/assets/`.
- `scripts/check-verbatim-blocks.sh` exists; exits 0 on the full intermediate course.
- `slides/deploy-pptx.sh` writes to audience-first subtree; full build runs ≤ 635.79 s.
- `scripts/check-slide-overflow.sh` extended; reports 0 overflows.
- `scripts/check-contrast.sh` passes against the intermediate theme.
- `git diff --stat $(merge-base) -- slides/beginner/` empty.
- `grep '<!-- duration:' slides/part-*.md` sum = 240.
- Deferred: 3 human reviewer panels (SC-001, SC-004, SC-008) recorded under `reviewer-panel-results.md`.
