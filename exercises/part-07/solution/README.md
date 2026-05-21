# Module 7 — Reference UI Solution (Flask + Jinja)

Single-page Dashboard rendered with Flask + plain CSS. Matches `wireframe.png`.

## Install

```bash
pip install flask
```

## Run

```bash
python app.py
```

Open http://localhost:5000 — render at 1280×720 should be unmistakably the wireframe (header, sidebar, 3 KPI cards, table of 5 rows, footer).

## Layout regions

- Header bar with title + primary action
- Left sidebar with 5 nav links
- Main: 3 KPI cards across the top, then a 5-row table
- Footer with version string
