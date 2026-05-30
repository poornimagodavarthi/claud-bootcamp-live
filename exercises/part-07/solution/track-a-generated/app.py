#!/usr/bin/env python3
"""Dashboard web application."""

from flask import Flask, render_template

app = Flask(__name__)

TASKS = [
    {"id": 1, "title": "Design homepage",      "status": "Done",        "assignee": "Alice", "due": "2026-05-15"},
    {"id": 2, "title": "Write API docs",        "status": "In Progress", "assignee": "Bob",   "due": "2026-05-20"},
    {"id": 3, "title": "Fix login bug",         "status": "Done",        "assignee": "Carol", "due": "2026-05-18"},
    {"id": 4, "title": "Add dark mode",         "status": "Todo",        "assignee": "Dave",  "due": "2026-06-01"},
    {"id": 5, "title": "Performance audit",     "status": "In Progress", "assignee": "Eve",   "due": "2026-05-25"},
    {"id": 6, "title": "Update dependencies",   "status": "Todo",        "assignee": "Alice", "due": "2026-06-05"},
    {"id": 7, "title": "Write unit tests",      "status": "In Progress", "assignee": "Bob",   "due": "2026-05-28"},
    {"id": 8, "title": "Deploy to staging",     "status": "Done",        "assignee": "Carol", "due": "2026-05-10"},
]

KPIS = [
    {"label": "Total Tasks",  "value": len(TASKS)},
    {"label": "Completed",    "value": sum(1 for t in TASKS if t["status"] == "Done")},
    {"label": "In Progress",  "value": sum(1 for t in TASKS if t["status"] == "In Progress")},
]

NAV_ITEMS = ["Overview", "Notes", "Tasks", "Reports", "Settings"]


@app.route("/")
def index():
    return render_template("index.html", tasks=TASKS, kpis=KPIS, nav_items=NAV_ITEMS)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
