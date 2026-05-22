"""Module 7 reference UI — Flask + Jinja, plain CSS.

Run:
    python app.py
Open http://localhost:5000
"""
from __future__ import annotations

from flask import Flask, render_template

app = Flask(__name__)

KPIS = [
    {"label": "Total notes", "value": 128},
    {"label": "Open tasks", "value": 42},
    {"label": "Avg cycle", "value": "7d"},
]

ROWS = [
    {"id": 1, "title": "Spec drafted",       "owner": "lb", "status": "open"},
    {"id": 2, "title": "API skeleton",       "owner": "lb", "status": "open"},
    {"id": 3, "title": "Tests scaffolded",   "owner": "ay", "status": "done"},
    {"id": 4, "title": "PR description",     "owner": "lb", "status": "done"},
    {"id": 5, "title": "Readiness review",   "owner": "ay", "status": "open"},
]


@app.route("/")
def index() -> str:
    return render_template("index.html", kpis=KPIS, rows=ROWS, version="1.0.0")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
