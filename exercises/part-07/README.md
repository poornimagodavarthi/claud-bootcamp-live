# Module 7 — Multimodal: Screenshot to UI

## Goal

Hand Claude a wireframe image, generate a working single-page Dashboard, and iterate one round of visual diff.

## Scenario

A designer hands you a wireframe at the standup. By lunch you have a runnable UI that matches it. The lift is in *not* translating the image to words — Claude reads it.

## Starter instructions

1. Choose your wireframe (both PNGs are committed in this folder, ready to attach):
   - `wireframe.png` — canonical, generated from `wireframe.mmd` (Mermaid).
   - `wireframe-sketch.png` — rough hand sketch, generated from `wireframe-sketch.svg` (Excalidraw export).
2. Choose framework: Flask + Jinja **or** Streamlit (Python only this module).
3. Create `module-07/`.

> **The `.png` files ship in this folder — just attach one to your prompt.** The
> `.mmd` and `.svg` files are the editable sources of truth; the `.png` files are
> their renders. You only need to re-render if you *edit* a source:
>
> ```bash
> ./render-wireframes.sh
> # or manually:
> npx -y @mermaid-js/mermaid-cli -i wireframe.mmd -o wireframe.png -w 1280 -H 720
> rsvg-convert -w 1280 -h 720 wireframe-sketch.svg -o wireframe-sketch.png
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

> **Give Claude a `.png` it can actually see.** Claude Code can read a `.png` from
> the working folder on its own (you'll see it run `Read wireframe.png`), or you can
> drag the image straight into the prompt — either works. What does **not** work is
> pointing it at the **`.svg`/`.mmd`** sources: those are text, not a raster image,
> so Claude can't view them as a picture and you'll get *"I don't see a wireframe
> image attached."* Both `.png` files are committed in this folder for exactly this
> reason.

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
| Claude can't see the image | Make sure a `.png` is in the folder (or drag it into the prompt). Claude Code reads `.png` from disk; it cannot view `.svg`/`.mmd`. |
| "I don't see a wireframe image attached" | You only have the `.svg`/`.mmd` source, not a viewable image. Use `wireframe.png` (or `wireframe-sketch.png`) — both are committed here. |
| Render uses Tailwind | Re-prompt with the "plain CSS" constraint reinforced. |
| Layout is "close" but not right | Run the visual-diff loop; cap at 3 iterations. |
| Streamlit sidebar collapses oddly | Use `st.sidebar` explicitly; layout is constrained — that's expected. |
