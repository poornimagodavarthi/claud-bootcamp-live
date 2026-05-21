# Module 5 — Python Reference Solution (Tests)

Pytest suite for the Module 4 Notes API (Python track).

## Install

```bash
pip install pytest fastapi httpx
```

## Run

```bash
pytest -q
```

Tests resolve the SUT at `../../part-04/solution/python/app.py` and use a per-test SQLite DB so they're isolated.
