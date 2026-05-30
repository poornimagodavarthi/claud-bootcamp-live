"""Notes Dashboard — Flask + Jinja2, Track A. Run: python app.py"""
from flask import Flask, render_template_string

app = Flask(__name__)

KPIS = [
    {"key": "KPI 1", "label": "Total Notes", "value": "128"},
    {"key": "KPI 2", "label": "Active Tasks", "value": "42"},
    {"key": "KPI 3", "label": "Next Due",     "value": "7d"},
]

RECENT = [
    {"name": "Q2 Planning Notes",    "value": "2026-05-28"},
    {"name": "Sprint Retrospective", "value": "2026-05-27"},
    {"name": "Product Roadmap",      "value": "2026-05-25"},
    {"name": "Team OKRs",            "value": "2026-05-22"},
    {"name": "Bug Triage Log",       "value": "2026-05-20"},
]

NAV = ["Overview", "Notes", "Tasks", "Reports", "Settings"]

TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1280">
<title>Dashboard</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>

<header>
  <h1>Dashboard</h1>
  <button class="btn">+ New Note</button>
</header>

<div class="layout">
  <aside>
    <nav>
      {% for item in nav %}
      <a href="#">{{ item }}</a>
      {% endfor %}
    </nav>
  </aside>

  <main>
    <div class="kpi-row">
      {% for kpi in kpis %}
      <div class="kpi-card">
        <div class="kpi-key">{{ kpi.key }}</div>
        <div class="kpi-value">{{ kpi.value }}</div>
      </div>
      {% endfor %}
    </div>

    <div class="recent-panel">
      <h2>Recent items</h2>
      {% for row in recent %}
      <div class="recent-row">
        <span class="recent-name">{{ row.name }}</span>
        <span class="recent-dots"></span>
        <span class="recent-value">{{ row.value }}</span>
      </div>
      {% endfor %}
    </div>
  </main>
</div>

<footer>v1.0.0</footer>

</body>
</html>"""


@app.get("/")
def index():
    return render_template_string(TEMPLATE, kpis=KPIS, recent=RECENT, nav=NAV)


if __name__ == "__main__":
    app.run(debug=True)
