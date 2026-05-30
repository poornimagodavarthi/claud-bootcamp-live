# 07. Multimodal

Module 07 · 30 min

## Multimodal: Screenshot to UI

**Claude can read a picture. Hand it a wireframe; get a working UI back.**

### Theory · Layout-first prompting (4 min)

> Let Claude **read the layout** from the image; you describe what it **can't** see.

- The image carries: structure, regions, relative sizes.
- You must state: framework, data source, interactivity — Claude can't infer these.
- **Visual-diff loop**: render → screenshot → ask Claude "what's missing?" → patch. **Cap at 3 rounds.**
- **Scope discipline**: ship the layout. Theming and animation are stretch goals.

Two wireframes ship with the exercise: `wireframe.png` (canonical) and `wireframe-sketch.png` (rough).

### From wireframe to running UI

![Screenshot-to-UI: layout-first prompt, build, screenshot-diff loop](resources/07-screenshot-to-ui.png)

Layout-first prompt → build → **screenshot-diff loop** (cap at 3 rounds).

### Reference · markitdown — any file → Markdown

For **non-image** sources (PDF, DOCX, PPTX, XLSX, audio, video, HTML, ZIP, YouTube), convert to Markdown first — it's cheap and LLM-native:

```bash
pip install 'markitdown[all]'
markitdown report.pdf > report.md
```

Then drop into the prompt: *"Attached is the converted Markdown of `report.pdf`."* Claude consumes tables and headings without burning vision tokens.

### Reference · Common mistakes

- "Looks close enough" — the whole point is precision; diff again.
- Pulling in Tailwind / shadcn (the constraint exists for a reason).
- Forgetting to attach the image.
- Iterating five rounds (cap at three).

### Live demo · Wireframe → running UI (6 min)

1. Open `exercises/part-07/wireframe-sketch.png` in Claude Code.
2. Paste the prompt **with the framework constraint**:

```text
Build this wireframe as a Flask + Jinja app (no other deps): one route, one
template. Match the layout — header, sidebar, main, footer. Run on localhost:5000.
```

3. Save and run; screenshot it next to the wireframe, ask *"What's missing?"*
4. Apply one round of fixes; end on a side-by-side comparison.

**Success signal**: the app runs with one command and the layout clearly matches the wireframe.

### Your turn · Dashboard from wireframe (13 min)

**Exercise**: [`exercises/part-07/README.md`](#hands-on-exercise--module-07)

Build a single-page dashboard matching the wireframe (static data OK):

```text
Header (title + primary action) · Sidebar (3–5 nav links)
Main (3 KPI cards + table of 5 rows) · Footer (version string)
```

Run the **visual-diff loop** at least once; record patches in `diff-notes.md`.

**Deliverables**: runnable app in `module-07/` · `render-final.png` at 1280×720 · `diff-notes.md`.

**Success signal**: render at 1280×720 unmistakably matches the wireframe.

### Done & next (1 min)

**Definition of done**

- [ ] Runnable app; header, sidebar, 3 KPI cards, 5-row table, footer all present.
- [ ] `render-final.png` at 1280×720.
- [ ] `diff-notes.md` records ≥ 1 visual-diff round.

**Next** — we take messy code and make it clean *under constraints*, then document it.
**Module 8 — Refactoring & Documentation at Scale.**

## Hands-on exercise — Module 07 {#hands-on-exercise--module-07}

> **Companion repository** — Work this exercise from the live files in the [Claude Code Bootcamp repository](https://github.com/lucab85/Claude-Code-Bootcamp): [`exercises/part-07/README.md`](https://github.com/lucab85/Claude-Code-Bootcamp/blob/main/exercises/part-07/README.md).
> Reference solution: [`exercises/part-07/solution/README.md`](https://github.com/lucab85/Claude-Code-Bootcamp/blob/main/exercises/part-07/solution/README.md).

## Module 7 — Multimodal: Screenshot to UI

### Goal

Hand Claude a wireframe image, generate a working single-page Dashboard, and iterate one round of visual diff.

### Scenario

A designer hands you a wireframe at the standup. By lunch you have a runnable UI that matches it. The lift is in *not* translating the image to words — Claude reads it.

### Starter instructions

1. Choose your wireframe:
   - `wireframe.png` — canonical, generated from `wireframe.mmd` (Mermaid).
   - `wireframe-sketch.png` — rough hand sketch, generated from `wireframe-sketch.svg` (Excalidraw export).
2. Choose framework: Flask + Jinja **or** Streamlit (Python only this module).
3. Create `module-07/`.

> **Note on the wireframe sources**: the `.mmd` and `.svg` files in this folder are the source of truth. The `.png` files are renders. To re-render:
>
> ```bash
> npx -y @mermaid-js/mermaid-cli -i wireframe.mmd -o wireframe.png -w 1280 -H 720
> npx -y @resvg/resvg-js wireframe-sketch.svg wireframe-sketch.png
> ```

### Claude Code prompt to use

```text
INITIAL GENERATION
Below is a wireframe image. Build a working single-page web app matching the layout.

Constraints:
- Python 3.11. Track A: Flask + Jinja templates. Track B: Streamlit. Pick one and state the choice in the README.
- Static hardcoded sample data. No database. No auth.
- Single command to run: `python app.py` (Flask) or `streamlit run app.py`.
- Plain CSS, no Tailwind, no component libraries.
- Render at 1280x720 should look unmistakably like the wireframe.
```

```text
VISUAL DIFF
Image 1: the wireframe.
Image 2: my current render.

List the gaps in priority order. For each gap:
- One-sentence description.
- Smallest patch that closes it.

Stop after 5 items.
```

### Manual validation steps

```bash
cd module-07
python app.py        # or: streamlit run app.py
# Open the URL the framework prints
# Take a screenshot at 1280x720 → render-final.png
```

Side-by-side compare `wireframe.png` and `render-final.png`. Confirm header, sidebar, 3 KPI cards, table of 5 rows, footer.

### Expected deliverable

```text
module-07/
├── app.py                # plus templates/ if Flask
├── render-final.png      # 1280x720 screenshot
└── diff-notes.md         # the visual-diff list + which fixes you applied
```

### Definition of done

- [ ] App runs with one command.
- [ ] Render is unmistakably the wireframe.
- [ ] All 5 layout regions present: header, sidebar, 3 KPI cards, table (5 rows), footer.
- [ ] Visual-diff loop ran at least once.

### Stretch challenge

Theme the dashboard (light + dark) using only plain CSS variables. Document the prompt in `module-07/theme-notes.md`.

### Troubleshooting

| Symptom | Fix |
|---|---|
| Claude can't see the image | Confirm you attached it to the message. |
| Render uses Tailwind | Re-prompt with the "plain CSS" constraint reinforced. |
| Layout is "close" but not right | Run the visual-diff loop; cap at 3 iterations. |
| Streamlit sidebar collapses oddly | Use `st.sidebar` explicitly; layout is constrained — that's expected. |

## Solution — Module 07 {#solution--module-07}

## Module 7 — Reference UI Solution (Flask + Jinja)

Single-page Dashboard rendered with Flask + plain CSS. Matches `wireframe.png`.

### Install

```bash
pip install flask
```

### Run

```bash
python app.py
```

Open http://localhost:5000 — render at 1280×720 should be unmistakably the wireframe (header, sidebar, 3 KPI cards, table of 5 rows, footer).

### Layout regions

- Header bar with title + primary action
- Left sidebar with 5 nav links
- Main: 3 KPI cards across the top, then a 5-row table
- Footer with version string
