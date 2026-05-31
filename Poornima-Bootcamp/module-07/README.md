# Module 07 — Dashboard (Track A: Flask)

Single-page dashboard matching the wireframe. No database, no auth, hardcoded sample data.

## Run

```bash
pip install flask
python app.py
```

Then open <http://127.0.0.1:5000> at 1280 × 720.

## Layout

```
┌─ Header: "Dashboard" ─────────────────── "+ New Note" ─┐
├─ Sidebar ──┬─ KPI 1 ──── KPI 2 ──── KPI 3 ────────────┤
│ Overview   │                                            │
│ Notes      ├─ Recent items ────────────────────────────┤
│ Tasks      │  Row 1 .............. value               │
│ Reports    │  Row 2 .............. value               │
│ Settings   │  ...                                       │
└────────────┴────────────────────────────────────────────┘
└─ Footer: v1.0.0 ───────────────────────────────────────┘
```
