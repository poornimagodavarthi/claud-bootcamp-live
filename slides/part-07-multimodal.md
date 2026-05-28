---
marp: true
theme: wow-beginner
header: 'Claude Code Bootcamp · Day 1 · Module 07'
paginate: true
size: 16:9
title: "Module 7 — Multimodal: Screenshot to UI"
description: "Hand Claude a wireframe image and produce a working single-page Dashboard UI. Match the wireframe pixel-for-pixel-ish."
---

<!-- duration: 30 min -->
<!-- _class: tpl-cover -->
<!-- _paginate: false -->
<!-- _header: "" -->

<span class="module-chip">Module 07 · 30 min</span>

# Multimodal: Screenshot to UI

**Claude can read a picture. Hand it a wireframe; get a working UI back.**

<img class="hero-icon" src="themes/icons/eye.svg" alt="" />

<!--
SPEAKER NOTES — slide 1 (hook, 60 sec)
- One line: "Today the prompt includes an image. We turn a wireframe into a running dashboard."
-->

---

<!-- _class: tpl-objectives -->

## Theory · Layout-first prompting (4 min)

> Let Claude **read the layout** from the image; you describe what it **can't** see.

- The image carries: structure, regions, relative sizes.
- You must state: framework, data source, interactivity — Claude can't infer these.
- **Visual-diff loop**: render → screenshot → ask Claude "what's missing?" → patch. **Cap at 3 rounds.**
- **Scope discipline**: ship the layout. Theming and animation are stretch goals.

Two wireframes ship with the exercise: `wireframe.png` (canonical) and `wireframe-sketch.png` (rough).

<!--
SPEAKER NOTES — slide 2 (theory, 4 min)
- Forgetting to attach the image is the #1 fail — Claude can't read what isn't attached.
-->

---

<!-- _class: tpl-show -->

## From wireframe to running UI

![Screenshot-to-UI: layout-first prompt, build, screenshot-diff loop](intermediate/assets/07-screenshot-to-ui.svg)

Layout-first prompt → build → **screenshot-diff loop** (cap at 3 rounds).

<!--
SPEAKER NOTES — slide 3 (diagram, 1 min)
- The diff loop is the engine; the cap stops infinite pixel-chasing.
-->

---

<!-- _class: tpl-show -->

## Reference · markitdown — any file → Markdown

For **non-image** sources (PDF, DOCX, PPTX, XLSX, audio, video, HTML, ZIP, YouTube), convert to Markdown first — it's cheap and LLM-native:

```bash
pip install 'markitdown[all]'
markitdown report.pdf > report.md
```

Then drop into the prompt: *"Attached is the converted Markdown of `report.pdf`."* Claude consumes tables and headings without burning vision tokens.

<!--
SPEAKER NOTES — slide 3 (reference, 1 min)
- markitdown is the bridge for documents; image attachment is the bridge for visuals.
-->

---

<!-- _class: tpl-show -->

## Reference · Common mistakes

- "Looks close enough" — the whole point is precision; diff again.
- Pulling in Tailwind / shadcn (the constraint exists for a reason).
- Forgetting to attach the image.
- Iterating five rounds (cap at three).

<!--
SPEAKER NOTES — slide 4 (common mistakes, 30 sec)
Instructor cues:
- Project the wireframe and the render side-by-side throughout.
-->

---

<!-- _class: tpl-show -->

## Live demo · Wireframe → running UI (6 min)

1. Open `exercises/part-07/wireframe-sketch.png` in Claude Code.
2. Paste the prompt **with the framework constraint**:

```text
Build this wireframe as a Flask + Jinja app (no other deps): one route, one
template. Match the layout — header, sidebar, main, footer. Run on localhost:5000.
```

3. Save and run; screenshot it next to the wireframe, ask *"What's missing?"*
4. Apply one round of fixes; end on a side-by-side comparison.

**Success signal**: the app runs with one command and the layout clearly matches the wireframe.

<!--
SPEAKER NOTES — slide 5 (demo, 6 min)
-->

---

<!-- _class: tpl-try -->

## Your turn · Dashboard from wireframe (13 min)

**Exercise**: [`exercises/part-07/README.md`](../exercises/part-07/README.md)

Build a single-page dashboard matching the wireframe (static data OK):

```text
Header (title + primary action) · Sidebar (3–5 nav links)
Main (3 KPI cards + table of 5 rows) · Footer (version string)
```

Run the **visual-diff loop** at least once; record patches in `diff-notes.md`.

**Deliverables**: runnable app in `module-07/` · `render-final.png` at 1280×720 · `diff-notes.md`.

**Success signal**: render at 1280×720 unmistakably matches the wireframe.

<!--
SPEAKER NOTES — slide 6 (hands-on, 13 min)
- Catch students who skip the diff loop. "Looks close" isn't done. 3-min warning.
-->

---

<!-- _class: tpl-done -->

## Done & next (1 min)

**Definition of done**

- [ ] Runnable app; header, sidebar, 3 KPI cards, 5-row table, footer all present.
- [ ] `render-final.png` at 1280×720.
- [ ] `diff-notes.md` records ≥ 1 visual-diff round.

**Next** — we take messy code and make it clean *under constraints*, then document it.
**Module 8 — Refactoring & Documentation at Scale.**

<!--
SPEAKER NOTES — slide 7 (wrap, 1 min)
-->

<!-- polish-log
2026-05-28 · lean instructor-pacing shape (matches Module 1 pilot).
cover -> theory (layout-first) -> reference (markitdown · mistakes) -> live demo -> your turn -> done.
-->
