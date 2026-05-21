# Module 7 — Multimodal: Screenshot to UI

## Goal

Hand Claude a wireframe image, generate a working single-page Dashboard, and iterate one round of visual diff.

## Scenario

A designer hands you a wireframe at the standup. By lunch you have a runnable UI that matches it. The lift is in *not* translating the image to words — Claude reads it.

## Starter instructions

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

## Claude Code prompt to use

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

## Manual validation steps

```bash
cd module-07
python app.py        # or: streamlit run app.py
# Open the URL the framework prints
# Take a screenshot at 1280x720 → render-final.png
```

Side-by-side compare `wireframe.png` and `render-final.png`. Confirm header, sidebar, 3 KPI cards, table of 5 rows, footer.

## Expected deliverable

```text
module-07/
├── app.py                # plus templates/ if Flask
├── render-final.png      # 1280x720 screenshot
└── diff-notes.md         # the visual-diff list + which fixes you applied
```

## Definition of done

- [ ] App runs with one command.
- [ ] Render is unmistakably the wireframe.
- [ ] All 5 layout regions present: header, sidebar, 3 KPI cards, table (5 rows), footer.
- [ ] Visual-diff loop ran at least once.

## Stretch challenge

Theme the dashboard (light + dark) using only plain CSS variables. Document the prompt in `module-07/theme-notes.md`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Claude can't see the image | Confirm you attached it to the message. |
| Render uses Tailwind | Re-prompt with the "plain CSS" constraint reinforced. |
| Layout is "close" but not right | Run the visual-diff loop; cap at 3 iterations. |
| Streamlit sidebar collapses oddly | Use `st.sidebar` explicitly; layout is constrained — that's expected. |
