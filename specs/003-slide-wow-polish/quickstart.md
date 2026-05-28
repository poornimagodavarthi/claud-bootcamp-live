# Quickstart — Applying the `wow-beginner` Design System

**Feature**: Slide Decks That Shine
**Branch**: `003-slide-wow-polish`
**Audience**: a contributor adding a new beginner deck (or restyling an existing one) after this feature ships.
**Time to first polished slide**: ≤ 10 minutes.

This is the verification path for SC-010 ("a new contributor can read this once and produce a compliant ninth-module deck without further guidance").

---

## Prerequisites

- The repo cloned, on a branch off `main`.
- Node.js installed (any version supported by Marp CLI).
- Read access to: [slides/themes/wow-beginner.css](../../slides/themes/wow-beginner.css), [slides/themes/README.md](../../slides/themes/README.md), [contracts/slide-template-contracts.md](contracts/slide-template-contracts.md).

No package install needed — `slides/deploy-pptx.sh` self-bootstraps Marp via `npx`.

---

## Step 1 — Create the deck file (1 min)

Create `slides/beginner/part-09-your-module.md` with this exact front-matter:

```yaml
---
marp: true
theme: wow-beginner
paginate: true
size: 16:9
title: "Module 09 — Your Module Title"
description: "One-line description of what the learner will do."
---

<!-- duration: 20 min -->
```

The `theme: wow-beginner` line is the only line that wires you into the design system. Everything else (fonts, palette, slide templates) is inherited from `slides/themes/wow-beginner.css`.

---

## Step 2 — Add the Cover slide (1 min)

```markdown
<!-- _class: tpl-cover -->

# Module 09 — Your Module Title

Claude Code 101 · Beginner Workshop · Module 9 of 9

<img src="../themes/icons/lightbulb.svg" alt="" class="hero-icon" />

---
```

Required slots filled: module-number ("Module 09"), title (the `<h1>`), course-name (the subtitle line), hero-visual (the icon). See [Cover contract](contracts/slide-template-contracts.md#template-1--cover-tpl-cover).

---

## Step 3 — Add What You'll Learn (1 min)

```markdown
<!-- _class: tpl-objectives -->

## What you'll learn

1. First objective (verbatim from your spec source).
2. Second objective.
3. Third objective.

---
```

If you have a duration badge to surface, add `<span class="badge">20 min</span>` next to the heading.

---

## Step 4 — Add a Show Me slide with a teaching visual (3 min)

```markdown
<!-- _class: tpl-show -->

## Show me

```text
$ your --command
expected output line one
expected output line two
```

> Notice the prompt `$` is bold — that's the line you type. The rest is what your terminal prints back.

![](assets/09-your-visual.svg)

---
```

Authoring the SVG (`slides/beginner/assets/09-your-visual.svg`) is the only piece that takes real design time. Keep it to:

- Background-free (`<svg>` background is the slide's `--bg`).
- Strokes in `--ink` (`#1B1B1F`) at 2 px.
- Fills in `--accent-soft` (`#FCE6DA`) or `--bg`.
- One `--accent` (`#D9531E`) highlight per visual, never more.
- Include a `<title>` element so screen readers announce the visual.
- Validate against [TeachingVisual contract](data-model.md#entity-teachingvisual): the visual MUST teach the slide's main idea even with the body text hidden.

---

## Step 5 — Add Try It Yourself, Reflect, Closing (2 min)

Three slides, one each, copy-paste-and-edit from the existing decks. Verbatim text from your spec source goes in steps and checklist items.

```markdown
<!-- _class: tpl-try -->

## Try it yourself

1. Step one (verbatim).
2. Step two.
3. Step three.

> You're done when your terminal shows `<expected output>`.

---

<!-- _class: tpl-done -->

## Definition of done

- [ ] Item one.
- [ ] Item two.
- [ ] Item three.

> What's the one thing you'll do differently next time you sit down with Claude Code?

---

<!-- _class: tpl-next -->

## You finished Claude Code 101

You shipped a real artifact and you know the loop. Go build something small for yourself this week.
```

---

## Step 6 — Build (1 min)

```bash
./slides/deploy-pptx.sh --html
open slides/dist/html/beginner/part-09-your-module.html
```

You should see:

- The cream background, near-black ink, single coral accent.
- Inter for body, JetBrains Mono for code.
- Footer with course name + module number + page number.

If you instead see Marp's default white-and-blue, the `theme: wow-beginner` line is wrong — re-check Step 1.

---

## Step 7 — Verify (1 min)

Run the overflow check:

```bash
./scripts/check-slide-overflow.sh slides/dist/html/beginner/part-09-your-module.html
# expected: PASS — 0 slides overflow
```

Manually scan the rendered HTML once:

- [ ] No silent text overflow.
- [ ] All `$` prompts in Show Me slides are bold.
- [ ] The teaching visual reads correctly with body text mentally blanked out.
- [ ] No color carries meaning alone (success and danger always paired with check / shield icons).
- [ ] Verbatim blocks (objectives, commands, steps, checklist) match your source spec.

---

## Reviewer Set R1 (referenced by SC-001 / SC-004)

If your change is the polish pass itself (not a new module), recruit:

- **SC-001 panel (n=5)**: 5 people who have never seen the deck. Mix of technical / non-technical. Show them only the cover + first 3 content slides of Module 01 rendered as PNG. Ask: *"Describe what you're looking at in three adjectives."* Pass: ≥ 4 of 5 say a positive aesthetic adjective; 0 of 5 say "plain", "default", "amateur".
- **SC-004 panel (n=8)**: 8 technically literate people. For each of the 8 modules, show their chosen teaching-visual slide with body text blanked out (only title + visual visible). Ask: *"What is this slide teaching?"* Pass: ≥ 6 of 8 give a correct answer in their own words.

Record answers in `specs/003-slide-wow-polish/reviewer-panel-results.md` (added during implementation).

---

## Done

You now have:

- A polished, on-brand deck that inherits the design system automatically.
- A teaching visual that earns its place on the slide.
- Verifiable conformance with the spec's success criteria.

If you got here in ≤ 10 minutes, this quickstart is doing its job.
