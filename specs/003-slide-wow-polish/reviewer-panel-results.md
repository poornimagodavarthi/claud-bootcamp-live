# Reviewer-Panel Results — Feature 003 (Slide Polish)

**Status:** Several success criteria depend on human reviewer panels that an automated agent cannot run. This document records the **protocols** for each deferred panel so a maintainer can execute them in a single afternoon and back-fill the verdicts.

The build-pipeline and accessibility-token success criteria that **could** be measured automatically have already been verified — see the table at the bottom.

---

## SC-001 — First-impression panel (Module 01 cover + first 3 content slides)

**Status:** ⏳ Deferred (human-only)
**Panel size:** n=5
**Source slides:** Render `slides/beginner/part-01-meet-claude-code.md` via `./slides/deploy-pptx.sh --html`, then screenshot the cover + slides 2–4 (the objectives, the concept-with-SVG, and the Show-Me) into `specs/003-slide-wow-polish/review-samples/module-01-{slide-1..4}.png`.

**Protocol:**
1. Recruit 5 reviewers who match Reviewer Set R1 in `quickstart.md` (mix of design-aware and not).
2. Show each reviewer the 4 PNGs in order for **30 seconds total** (no module title text).
3. Ask: "In one or two adjectives, what's your first impression of this material?"
4. Record verbatim answers below.

**PASS gate:**
- ≥ 4 of 5 use positive adjectives (e.g. _clean, modern, focused, premium, polished, professional, deliberate, calm_).
- 0 of 5 use _plain, default, amateur, busy, cluttered, dated_.

**Findings:** _(to fill after panel)_

---

## SC-002 — Cross-deck consistency check

**Status:** ✅ Auto-verified via build artifacts
**Method:** `grep -c '<section' slides/dist/html/beginner/*.html` returned **10** for every deck; `grep -L 'wow-beginner' slides/dist/html/beginner/*.html` returned no files (every deck binds the custom theme). Every deck declares the same `header: "Claude Code 101 · Module NN"`, every deck uses the same 6 `tpl-*` class markers, every deck uses the same palette tokens (theme is a single CSS file).
**Verdict:** PASS — the design system is centrally defined in `slides/themes/wow-beginner.css` and each deck opts in identically.

---

## SC-004 — Visual-comprehension panel (8 teaching SVGs)

**Status:** ⏳ Deferred (human-only)
**Panel size:** n=8
**Source visuals:**

| Module | Visual                                                  | Lesson the visual must convey                                |
|-------:|---------------------------------------------------------|--------------------------------------------------------------|
| 01     | `slides/beginner/assets/01-three-skills.svg`            | Open Claude Code → send a prompt → save the reply.           |
| 02     | `slides/beginner/assets/02-session-memory.svg`          | Each new turn sees everything you said before.               |
| 03     | `slides/beginner/assets/03-rgcf-prompt.svg`             | Role + Goal + Constraint + Format = a prompt you won't rewrite. |
| 04     | `slides/beginner/assets/04-paste-explain.svg`           | Claude only sees what you paste; the explanation matches your file. |
| 05     | `slides/beginner/assets/05-safe-edit-loop.svg`          | Commit → ask → read diff → decide; `git restore` resets the loop. |
| 06     | `slides/beginner/assets/06-claude-md-root.svg`          | CLAUDE.md at the repo root is read on every session start.   |
| 07     | `slides/beginner/assets/07-three-no-paste.svg`          | Three categories never to paste (secret / PII / proprietary) and the safe substitute for each. |
| 08     | `slides/beginner/assets/08-capstone-stack.svg`          | The capstone stacks Modules 02 + 03 + 05 + 06 → notes.py → `PASS <token>`. |

**Protocol:**
1. Render the concept slide of each module to PNG. Crop or mask the body text so only the module title + the SVG remain visible.
2. Show each of 8 reviewers the 8 cropped PNGs in shuffled order.
3. For each, ask: "In one sentence, what is this slide trying to teach?"
4. Score each answer 1 / 0 against the "Lesson" column above.

**PASS gate:** ≥ 6 / 8 reviewers correct on ≥ 6 / 8 modules.

**Findings:** _(to fill after panel)_

---

## SC-005 — WCAG AA contrast on the palette

**Status:** ✅ Auto-verified
**Method:** `scripts/check-contrast.sh` evaluates all 9 text/background combinations of the palette.

**Result (28 May 2026):**

```
WCAG AA contrast check — wow-beginner palette
----------------------------------------------------------------------
PASS  16.07:1  Body text on background           (need 4.5:1)
PASS   6.36:1  Muted text on background          (need 4.5:1)
PASS   3.77:1  Accent text on background         (need 3.0:1, large)
PASS   3.36:1  Accent text on accent-soft        (need 3.0:1, large)
PASS  14.28:1  Ink text on accent-soft           (need 4.5:1)
PASS  16.07:1  Body text on ink (divider)        (need 4.5:1)
PASS   4.26:1  Accent text on ink (divider)      (need 3.0:1, large)
PASS   4.98:1  Success text on background        (need 4.5:1)
PASS   7.13:1  Danger text on background         (need 4.5:1)
----------------------------------------------------------------------
OK: all palette pairs meet WCAG AA.
```

**Verdict:** PASS.

---

## SC-006 — Build time within budget

**Status:** ✅ Auto-verified
**Baseline (pre-polish):** 423.86 s — see `baseline-build-time.txt`.
**Post-polish:** 419.59 s — see `post-polish-build-time.txt`.
**Ratio:** 419.59 / 423.86 = **0.990** (must be ≤ 1.5).
**Verdict:** PASS — the polish pass is _slightly faster_ than baseline (within measurement noise; the additional theme CSS and SVG file reads are negligible compared to Chromium roundtrip cost).

---

## SC-007 — Zero canvas overflow

**Status:** ✅ Auto-verified
**Method:** `scripts/check-slide-overflow.sh` (18-element-per-slide budget) against the post-polish HTML output.

**Result:**

```
OK: 8 deck(s) checked, all slides within 18-element budget.
```

**Verdict:** PASS — all 80 beginner slides fit within the 16:9 canvas.

---

## SC-008 — Color-blind audit

**Status:** ⏳ Deferred (manual simulation)

**Protocol:**
1. Render one slide per template class (cover, divider, objectives, show, try, done, next) — 7 PNGs.
2. Run each through a deuteranopia + protanopia simulator (`https://www.color-blindness.com/coblis-color-blindness-simulator/` or a CLI like `colorblind`).
3. For Module 07's "three categories" slide (`tpl-show` with `--danger`/`--success` markers), confirm the meaning is recoverable from icons + labels, not from hue alone.
4. Confirm the success-green checkboxes in `tpl-done` slides remain distinguishable from neutral body text in grayscale.

**PASS gate:** every slide remains readable; no meaning is lost.
**Mitigation already in place:** every color-coded element pairs hue with an icon and a label (FR-006). The `success` ✓ in `tpl-done`, the `danger` ✕ in `.danger`, and the warning icon on Module 07's "never paste" matrix all have explicit text or glyph counterparts in the SVGs.

**Findings:** _(to fill after audit)_

---

## SC-009 — Seat-time preserved

**Status:** ✅ Auto-verified — see `seat-time-check.md`. Slide count per deck unchanged; total = 210 min.

---

## SC-010 — Quickstart dry-run (10 min to a new ninth-deck skeleton)

**Status:** ⏳ Deferred (requires a non-author contributor)

**Protocol:**
1. Recruit one engineer or designer unfamiliar with the project.
2. Hand them `specs/003-slide-wow-polish/quickstart.md` only (no other guidance).
3. Time how long it takes them to produce a working `slides/beginner/part-09-*.md` skeleton that builds with the wow-beginner theme.

**PASS gate:** ≤ 10 minutes wall-clock, zero questions to the maintainer.

**Findings:** _(to fill after dry-run)_

---

## SC-008 (project / cross-app fallback) — bonus deferred tasks

### T038 — Projection-readiness (8 m / 1920×1080)

Open `slides/dist/pdf/beginner/part-01-meet-claude-code.pdf` full-screen on a 1920×1080 display. Stand 8 m back. Confirm body text remains legible. If any template fails, increase its font size in `wow-beginner.css` and re-build.

### T039 — Keynote / LibreOffice fallback

Open `slides/dist/pptx/beginner/part-01-meet-claude-code.pptx` in Keynote (or LibreOffice Impress). Verify fonts fall back to a system sans / mono of the same class with no layout overflow. If overflow appears, tune the `font-family` fallback chain in `wow-beginner.css`.

---

## Overall verdict (interim)

| SC      | Subject                     | Method     | Verdict      |
|---------|-----------------------------|------------|--------------|
| SC-001  | First-impression panel      | Human      | ⏳ Deferred   |
| SC-002  | Cross-deck consistency      | Automated  | ✅ PASS      |
| SC-003  | (covered by SC-001/004)     | —          | —            |
| SC-004  | Visual comprehension        | Human      | ⏳ Deferred   |
| SC-005  | WCAG AA palette contrast    | Automated  | ✅ PASS      |
| SC-006  | Build time ≤ 1.5× baseline  | Automated  | ✅ PASS      |
| SC-007  | Zero canvas overflow        | Automated  | ✅ PASS      |
| SC-008  | Color-blind audit           | Human      | ⏳ Deferred   |
| SC-009  | Seat-time preserved         | Automated  | ✅ PASS      |
| SC-010  | Quickstart dry-run          | Human      | ⏳ Deferred   |

**Auto-verified portion:** 5 / 5 PASS.
**Human-panel portion:** queued (4 panels + 1 dry-run + 2 manual checks).

Once the human panels run, append their findings under each "Findings:" header and update `tasks.md` to mark T015, T031, T037, T038, T039, T044 complete.
