#!/usr/bin/env python3
"""
Generate the 10 intermediate teaching SVGs (T038-T047).

Each SVG: viewBox 0 0 800 450 (16:9), palette tokens inline, Inter/JetBrains Mono
fonts, <title>+<desc> as first children, grayscale-recoverable (uses shape +
position differentiation, not colour alone).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "slides" / "intermediate" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

# Palette tokens (mirrored from wow-beginner.css :root).
BG, INK, MUTED, ACCENT, SOFT, SUCCESS = "#FAF7F2", "#1B1B1F", "#5A5A66", "#D9531E", "#FCE6DA", "#1F7A4D"

DEFS = f"""<defs>
    <style>
      .ink {{ fill: {INK}; }}
      .muted {{ fill: {MUTED}; }}
      .accent {{ fill: {ACCENT}; }}
      .soft {{ fill: {SOFT}; }}
      .bg {{ fill: {BG}; }}
      .success {{ fill: {SUCCESS}; }}
      .stroke-ink {{ fill: none; stroke: {INK}; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}
      .stroke-accent {{ fill: none; stroke: {ACCENT}; stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round; }}
      .stroke-muted {{ fill: none; stroke: {MUTED}; stroke-width: 1.5; stroke-dasharray: 4 4; }}
      text {{ font-family: 'Inter Variable', Inter, Helvetica, Arial, sans-serif; }}
      .h {{ font-weight: 700; font-size: 22px; fill: {INK}; }}
      .b {{ font-weight: 500; font-size: 16px; fill: {INK}; }}
      .s {{ font-weight: 600; font-size: 12px; fill: {MUTED}; letter-spacing: 0.1em; text-transform: uppercase; }}
      .mono {{ font-family: 'JetBrains Mono Variable', ui-monospace, monospace; font-weight: 600; font-size: 14px; fill: {INK}; }}
    </style>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{INK}"/>
    </marker>
  </defs>"""

def wrap(title, desc, body):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">{desc}</desc>
  {DEFS}
{body}
</svg>
'''

# --------------------------------------------------------------------- 01
def svg_01_tcc_loop():
    # Circular 5-node loop: Plan -> Implement -> Test -> Review -> Commit.
    import math
    cx, cy, r = 400, 230, 150
    labels = ["Plan", "Implement", "Test", "Review", "Commit"]
    nodes = []
    # 5 nodes evenly spaced, start at top.
    for i, lbl in enumerate(labels):
        ang = -math.pi/2 + i * 2*math.pi/5
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        nodes.append((x, y, lbl, i+1))
    parts = ['<g><text class="s" x="400" y="40" text-anchor="middle">The Claude Code loop · 5 steps · every module</text></g>']
    # Arcs between nodes (curved arrows along the circle).
    for i in range(5):
        x1, y1, _, _ = nodes[i]
        x2, y2, _, _ = nodes[(i+1) % 5]
        # Pull endpoints slightly inward so they don't overlap circles.
        dx, dy = x2-x1, y2-y1
        d = (dx*dx+dy*dy)**0.5
        x1a = x1 + dx/d*48; y1a = y1 + dy/d*48
        x2a = x2 - dx/d*52; y2a = y2 - dy/d*52
        # Curve outward from centre for clarity.
        mx, my = (x1a+x2a)/2, (y1a+y2a)/2
        # Outward perpendicular.
        nx, ny = (mx-cx), (my-cy)
        nlen = (nx*nx+ny*ny)**0.5 or 1
        cxp, cyp = mx + nx/nlen*22, my + ny/nlen*22
        parts.append(f'<path class="stroke-accent" d="M {x1a:.1f} {y1a:.1f} Q {cxp:.1f} {cyp:.1f} {x2a:.1f} {y2a:.1f}" marker-end="url(#ah)"/>')
    # Nodes.
    for x, y, lbl, n in nodes:
        parts.append(f'<g><circle class="soft" cx="{x:.1f}" cy="{y:.1f}" r="44"/><circle class="stroke-ink" cx="{x:.1f}" cy="{y:.1f}" r="44"/><text class="mono" x="{x:.1f}" y="{y-6:.1f}" text-anchor="middle">{n}</text><text class="b" x="{x:.1f}" y="{y+18:.1f}" text-anchor="middle">{lbl}</text></g>')
    return wrap(
        "The five-step Claude Code loop",
        "A circular diagram of five labelled nodes — Plan, Implement, Test, Review, Commit — connected by arrows that cycle clockwise.",
        "\n".join(parts),
    )

# --------------------------------------------------------------------- 02
def svg_02_prompt_anatomy():
    body = '''
  <text class="s" x="400" y="40" text-anchor="middle">Anatomy of a tech-lead prompt</text>
  <g transform="translate(60,70)">
    <rect class="bg" width="680" height="340" rx="14"/>
    <rect class="stroke-ink" width="680" height="340" rx="14"/>

    <g transform="translate(20,30)">
      <rect class="soft" width="120" height="34" rx="6"/>
      <rect class="stroke-accent" width="120" height="34" rx="6"/>
      <text class="b" x="60" y="23" text-anchor="middle">ROLE</text>
    </g>
    <text class="mono" x="160" y="92">You are a senior backend engineer.</text>

    <g transform="translate(20,116)">
      <rect class="soft" width="120" height="34" rx="6"/>
      <rect class="stroke-accent" width="120" height="34" rx="6"/>
      <text class="b" x="60" y="23" text-anchor="middle">GOAL</text>
    </g>
    <text class="mono" x="160" y="138">Add a /tasks endpoint that returns JSON.</text>

    <g transform="translate(20,162)">
      <rect class="soft" width="120" height="34" rx="6"/>
      <rect class="stroke-accent" width="120" height="34" rx="6"/>
      <text class="b" x="60" y="23" text-anchor="middle">CONSTRAINTS</text>
    </g>
    <text class="mono" x="160" y="184">Python 3.11. No new deps. ≤ 60 lines.</text>

    <g transform="translate(20,208)">
      <rect class="soft" width="120" height="34" rx="6"/>
      <rect class="stroke-accent" width="120" height="34" rx="6"/>
      <text class="b" x="60" y="23" text-anchor="middle">FORMAT</text>
    </g>
    <text class="mono" x="160" y="230">Return only the file contents in one fence.</text>

    <g transform="translate(20,254)">
      <rect class="soft" width="120" height="34" rx="6"/>
      <rect class="stroke-accent" width="120" height="34" rx="6"/>
      <text class="b" x="60" y="23" text-anchor="middle">CHECK</text>
    </g>
    <text class="mono" x="160" y="276">List the 3 invariants you will preserve.</text>

    <text class="s" x="340" y="320" text-anchor="middle">Five slots — every prompt fills them.</text>
  </g>
'''
    return wrap("Prompt anatomy: role, goal, constraints, format, check",
                "A bordered card listing five labelled prompt slots stacked vertically, each with its label in an accent pill on the left and a one-line example in monospace on the right.",
                body)

# --------------------------------------------------------------------- 03
def svg_03_claude_md_cheatsheet():
    body = '''
  <text class="s" x="400" y="40" text-anchor="middle">CLAUDE.md · what to put in it</text>
  <g transform="translate(140,70)">
    <rect class="bg" width="520" height="340" rx="10"/>
    <rect class="stroke-ink" width="520" height="340" rx="10"/>
    <rect class="soft" width="520" height="44" rx="10"/>
    <text class="mono" x="20" y="30">CLAUDE.md</text>
    <line class="stroke-muted" x1="0" y1="44" x2="520" y2="44"/>

    <text class="b" x="24" y="80">## Project shape</text>
    <text class="b" x="44" y="104" fill="''' + MUTED + '''">Stack, top-level dirs, how to run</text>

    <text class="b" x="24" y="136">## Conventions</text>
    <text class="b" x="44" y="160" fill="''' + MUTED + '''">Naming, lint, error handling style</text>

    <text class="b" x="24" y="192">## Tests</text>
    <text class="b" x="44" y="216" fill="''' + MUTED + '''">Where they live, how to run one</text>

    <text class="b" x="24" y="248">## Don't</text>
    <text class="b" x="44" y="272" fill="''' + MUTED + '''">Files/areas Claude must not touch</text>

    <text class="b" x="24" y="304">## Glossary</text>
    <text class="b" x="44" y="328" fill="''' + MUTED + '''">Project-specific terms in one line each</text>
  </g>
'''
    return wrap("CLAUDE.md cheat-sheet",
                "A file-card mock-up of CLAUDE.md showing five section headings — Project shape, Conventions, Tests, Don't, Glossary — each with a one-line description.",
                body)

# --------------------------------------------------------------------- 04
def svg_04_bon_scoring():
    rows = ["Correctness", "Readability", "Tests"]
    body_parts = ['<text class="s" x="400" y="40" text-anchor="middle">Best-of-N · score the candidates, pick the winner</text>']
    # 3 columns × 3 rows grid. Winner = column 2 (B).
    col_x = [220, 400, 580]
    headers = [("A", False), ("B", True), ("C", False)]
    for x, (h, win) in zip(col_x, headers):
        fill = "soft" if win else "bg"
        body_parts.append(f'<g><rect class="{fill}" x="{x-60}" y="80" width="120" height="280" rx="10"/><rect class="stroke-{"accent" if win else "ink"}" x="{x-60}" y="80" width="120" height="280" rx="10"/><text class="h" x="{x}" y="112" text-anchor="middle">{h}</text></g>')
    # Row labels.
    for i, r in enumerate(rows):
        y = 160 + i*60
        body_parts.append(f'<text class="b" x="60" y="{y+10}">{r}</text>')
        # Cells with score chips.
        scores = [["3", "5", "2"], ["4", "5", "3"], ["2", "5", "1"]][i]
        for x, s in zip(col_x, scores):
            body_parts.append(f'<g><rect class="bg" x="{x-26}" y="{y-22}" width="52" height="40" rx="6"/><rect class="stroke-ink" x="{x-26}" y="{y-22}" width="52" height="40" rx="6"/><text class="mono" x="{x}" y="{y+4}" text-anchor="middle">{s}</text></g>')
    # Totals + winner crown.
    totals = [9, 15, 6]
    for x, t in zip(col_x, totals):
        body_parts.append(f'<text class="h" x="{x}" y="350" text-anchor="middle">{t}</text>')
    body_parts.append(f'<text class="b" x="400" y="395" text-anchor="middle" fill="{ACCENT}">★ Winner: B</text>')
    return wrap("Best-of-N scoring grid",
                "A 3-by-3 grid scoring three candidate solutions A, B, C against three criteria. Column B is highlighted as the winner with the highest total.",
                "\n  ".join(body_parts))

# --------------------------------------------------------------------- 05
def svg_05_test_debug_loop():
    body = '''
  <text class="s" x="400" y="40" text-anchor="middle">Test → fail → fix → green</text>
  <g transform="translate(60,90)">
    <rect class="soft" width="160" height="100" rx="10"/>
    <rect class="stroke-ink" width="160" height="100" rx="10"/>
    <text class="b" x="80" y="44" text-anchor="middle">Write test</text>
    <text class="mono" x="80" y="74" text-anchor="middle">red</text>
  </g>
  <path class="stroke-accent" d="M 230 140 L 290 140" marker-end="url(#ah)"/>
  <g transform="translate(300,90)">
    <rect class="bg" width="160" height="100" rx="10"/>
    <rect class="stroke-ink" width="160" height="100" rx="10"/>
    <text class="b" x="80" y="44" text-anchor="middle">Run</text>
    <text class="mono" x="80" y="74" text-anchor="middle" fill="''' + ACCENT + '''">FAIL</text>
  </g>
  <path class="stroke-accent" d="M 470 140 L 530 140" marker-end="url(#ah)"/>
  <g transform="translate(540,90)">
    <rect class="bg" width="180" height="100" rx="10"/>
    <rect class="stroke-ink" width="180" height="100" rx="10"/>
    <text class="b" x="90" y="44" text-anchor="middle">Smallest fix</text>
    <text class="mono" x="90" y="74" text-anchor="middle">edit one file</text>
  </g>
  <path class="stroke-accent" d="M 630 200 Q 630 320 400 320 Q 170 320 140 240" marker-end="url(#ah)"/>
  <g transform="translate(320,290)">
    <rect class="success" width="160" height="80" rx="10" opacity="0.18"/>
    <rect class="stroke-ink" width="160" height="80" rx="10"/>
    <text class="b" x="80" y="34" text-anchor="middle" fill="''' + SUCCESS + '''">GREEN</text>
    <text class="mono" x="80" y="60" text-anchor="middle">commit</text>
  </g>
'''
    return wrap("Test, debug, ship — the red-green loop",
                "Four boxes arranged in a horseshoe: write a failing test, run it (red), make the smallest fix, then arrive at green and commit.",
                body)

# --------------------------------------------------------------------- 06
def svg_06_git_flow():
    body = f'''
  <text class="s" x="400" y="40" text-anchor="middle">main ← PR ← branch (your AI work)</text>
  <line class="stroke-ink" x1="80" y1="200" x2="720" y2="200"/>
  <text class="s" x="80" y="186">main</text>
  <line class="stroke-accent" x1="180" y1="200" x2="180" y2="280"/>
  <line class="stroke-accent" x1="180" y1="280" x2="600" y2="280"/>
  <line class="stroke-accent" x1="600" y1="280" x2="600" y2="200"/>
  <text class="s" x="180" y="306">branch: feature/x</text>

  <g><circle class="bg" cx="180" cy="200" r="10"/><circle class="stroke-ink" cx="180" cy="200" r="10"/></g>
  <g><circle class="bg" cx="260" cy="280" r="10"/><circle class="stroke-accent" cx="260" cy="280" r="10"/><text class="mono" x="260" y="316" text-anchor="middle">c1</text></g>
  <g><circle class="bg" cx="380" cy="280" r="10"/><circle class="stroke-accent" cx="380" cy="280" r="10"/><text class="mono" x="380" y="316" text-anchor="middle">c2</text></g>
  <g><circle class="bg" cx="500" cy="280" r="10"/><circle class="stroke-accent" cx="500" cy="280" r="10"/><text class="mono" x="500" y="316" text-anchor="middle">c3</text></g>
  <g><circle class="accent" cx="600" cy="200" r="10"/><text class="mono" x="600" y="186" text-anchor="middle">merge</text></g>

  <g transform="translate(440,90)">
    <rect class="soft" width="240" height="60" rx="10"/>
    <rect class="stroke-ink" width="240" height="60" rx="10"/>
    <text class="b" x="120" y="26" text-anchor="middle">Pull Request</text>
    <text class="mono" x="120" y="48" text-anchor="middle" fill="{MUTED}">Claude writes the description</text>
  </g>
  <line class="stroke-muted" x1="560" y1="150" x2="600" y2="190"/>
'''
    return wrap("Git workflow for safe AI development",
                "A horizontal main branch with a feature branch carrying three commits c1, c2, c3 below it, merged back into main via a Pull Request card.",
                body)

# --------------------------------------------------------------------- 07
def svg_07_screenshot_to_ui():
    body = f'''
  <text class="s" x="400" y="40" text-anchor="middle">Image → prompt → working UI</text>
  <g transform="translate(60,80)">
    <rect class="bg" width="280" height="300" rx="10"/>
    <rect class="stroke-ink" width="280" height="300" rx="10"/>
    <text class="s" x="20" y="32">Wireframe (paste)</text>
    <rect class="bg" x="20" y="50" width="240" height="40" rx="4"/>
    <rect class="stroke-muted" x="20" y="50" width="240" height="40" rx="4"/>
    <rect class="bg" x="20" y="106" width="100" height="160" rx="4"/>
    <rect class="stroke-muted" x="20" y="106" width="100" height="160" rx="4"/>
    <rect class="bg" x="140" y="106" width="120" height="74" rx="4"/>
    <rect class="stroke-muted" x="140" y="106" width="120" height="74" rx="4"/>
    <rect class="bg" x="140" y="196" width="120" height="70" rx="4"/>
    <rect class="stroke-muted" x="140" y="196" width="120" height="70" rx="4"/>
  </g>
  <path class="stroke-accent" d="M 350 230 L 430 230" marker-end="url(#ah)"/>
  <text class="s" x="390" y="216" text-anchor="middle">Claude</text>
  <g transform="translate(440,80)">
    <rect class="bg" width="300" height="300" rx="10"/>
    <rect class="stroke-ink" width="300" height="300" rx="10"/>
    <text class="s" x="20" y="32">Rendered UI</text>
    <rect class="accent" x="20" y="50" width="260" height="40" rx="4"/>
    <text class="b" x="36" y="76" fill="{BG}">Dashboard</text>
    <rect class="soft" x="20" y="106" width="120" height="160" rx="4"/>
    <text class="b" x="32" y="134">Sidebar</text>
    <rect class="bg" x="160" y="106" width="120" height="74" rx="4"/>
    <rect class="stroke-ink" x="160" y="106" width="120" height="74" rx="4"/>
    <text class="b" x="172" y="134">Card 1</text>
    <rect class="bg" x="160" y="196" width="120" height="70" rx="4"/>
    <rect class="stroke-ink" x="160" y="196" width="120" height="70" rx="4"/>
    <text class="b" x="172" y="224">Card 2</text>
  </g>
'''
    return wrap("From wireframe screenshot to working UI",
                "Two side-by-side panels: a hand-drawn wireframe on the left and a rendered dashboard UI on the right, connected by an arrow labelled Claude.",
                body)

# --------------------------------------------------------------------- 08
def svg_08_refactor_constraints():
    body = f'''
  <text class="s" x="400" y="40" text-anchor="middle">Refactor under written constraints</text>
  <g transform="translate(60,80)">
    <rect class="soft" width="190" height="40" rx="20"/>
    <text class="b" x="95" y="26" text-anchor="middle">≤ 60 lines / function</text>
  </g>
  <g transform="translate(280,80)">
    <rect class="soft" width="180" height="40" rx="20"/>
    <text class="b" x="90" y="26" text-anchor="middle">No new deps</text>
  </g>
  <g transform="translate(490,80)">
    <rect class="soft" width="250" height="40" rx="20"/>
    <text class="b" x="125" y="26" text-anchor="middle">Public API unchanged</text>
  </g>

  <g transform="translate(60,160)">
    <rect class="bg" width="320" height="240" rx="10"/>
    <rect class="stroke-ink" width="320" height="240" rx="10"/>
    <text class="s" x="20" y="32">Before</text>
    <text class="mono" x="20" y="64">def handle(x):</text>
    <text class="mono" x="20" y="86">  # 180 lines</text>
    <text class="mono" x="20" y="108">  # nested ifs</text>
    <text class="mono" x="20" y="130">  # 4 globals</text>
    <text class="mono" x="20" y="152">  ...</text>
    <text class="mono" x="20" y="200" fill="{ACCENT}">cyclomatic: 24</text>
  </g>
  <path class="stroke-accent" d="M 400 280 L 460 280" marker-end="url(#ah)"/>
  <g transform="translate(470,160)">
    <rect class="bg" width="270" height="240" rx="10"/>
    <rect class="stroke-ink" width="270" height="240" rx="10"/>
    <text class="s" x="20" y="32">After</text>
    <text class="mono" x="20" y="64">def handle(x):</text>
    <text class="mono" x="20" y="86">  v = validate(x)</text>
    <text class="mono" x="20" y="108">  d = build(v)</text>
    <text class="mono" x="20" y="130">  return send(d)</text>
    <text class="mono" x="20" y="200" fill="{SUCCESS}">cyclomatic: 4</text>
  </g>
'''
    return wrap("Refactor under written constraints",
                "Three constraint pills across the top — line cap, no new dependencies, public API unchanged — above a before/after comparison of a function with cyclomatic complexity dropping from 24 to 4.",
                body)

# --------------------------------------------------------------------- 09
def svg_09_skills_catalogue():
    body = f'''
  <text class="s" x="400" y="40" text-anchor="middle">skills/ · reusable instructions, project-agnostic</text>
  <line class="stroke-ink" x1="40" y1="380" x2="760" y2="380"/>
  <line class="stroke-ink" x1="40" y1="380" x2="60" y2="400"/>
  <line class="stroke-ink" x1="760" y1="380" x2="740" y2="400"/>
'''
    tiles = [
        ("test-generation", 70),
        ("code-review", 220),
        ("refactor", 370),
        ("documentation-generation", 520),
        ("release-notes", 670),
    ]
    parts = [body]
    for name, x in tiles:
        parts.append(f'''<g transform="translate({x},170)">
    <rect class="soft" width="110" height="170" rx="8"/>
    <rect class="stroke-ink" width="110" height="170" rx="8"/>
    <rect class="bg" x="14" y="14" width="82" height="120" rx="4"/>
    <rect class="stroke-muted" x="14" y="14" width="82" height="120" rx="4"/>
    <text class="mono" x="55" y="58" text-anchor="middle" fill="{MUTED}">SKILL</text>
    <text class="mono" x="55" y="80" text-anchor="middle" fill="{MUTED}">.md</text>
    <text class="b" x="55" y="158" text-anchor="middle" font-size="13">{name}</text>
  </g>''')
    return wrap("The skills/ catalogue",
                "Five labelled SKILL.md tiles sitting on a horizontal shelf, each representing a reusable, project-agnostic instruction set: test-generation, code-review, refactor, documentation-generation, release-notes.",
                "\n  ".join(parts))

# --------------------------------------------------------------------- 10
def svg_10_five_axes():
    # Pentagon radar over 5 axes.
    import math
    cx, cy, R = 400, 240, 150
    axes = ["Security", "Reliability", "Performance", "Observability", "Operability"]
    pts = []
    for i in range(5):
        ang = -math.pi/2 + i * 2*math.pi/5
        pts.append((cx + R*math.cos(ang), cy + R*math.sin(ang), axes[i]))
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in pts)
    # Inner radial gridlines.
    grid = "\n  ".join(
        f'<polygon points="{" ".join(f"{cx + R*frac*math.cos(-math.pi/2 + i*2*math.pi/5):.1f},{cy + R*frac*math.sin(-math.pi/2 + i*2*math.pi/5):.1f}" for i in range(5))}" class="stroke-muted" fill="none"/>'
        for frac in (0.33, 0.66, 1.0)
    )
    spokes = "\n  ".join(f'<line class="stroke-muted" x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>' for x, y, _ in pts)
    # Sample score polygon (varied).
    scores = [0.85, 0.6, 0.7, 0.5, 0.8]
    spts = []
    for i, s in enumerate(scores):
        ang = -math.pi/2 + i * 2*math.pi/5
        spts.append(f"{cx + R*s*math.cos(ang):.1f},{cy + R*s*math.sin(ang):.1f}")
    score_poly = " ".join(spts)
    # Axis labels positioned outside the pentagon.
    labels = []
    for x, y, lbl in pts:
        dx, dy = x - cx, y - cy
        d = (dx*dx + dy*dy)**0.5 or 1
        lx, ly = x + dx/d*32, y + dy/d*22
        anchor = "middle"
        if dx > 30: anchor = "start"
        elif dx < -30: anchor = "end"
        labels.append(f'<text class="b" x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}">{lbl}</text>')
    body = f'''
  <text class="s" x="400" y="40" text-anchor="middle">Production readiness · score across five axes</text>
  {grid}
  {spokes}
  <polygon points="{score_poly}" fill="{ACCENT}" opacity="0.18"/>
  <polygon points="{score_poly}" class="stroke-accent"/>
  {"".join(labels)}
'''
    return wrap("Production readiness across five axes",
                "A pentagon radar chart with five axes — Security, Reliability, Performance, Observability, Operability — overlaid with a sample score polygon showing strengths and gaps.",
                body)

SVGS = [
    ("01-tcc-loop.svg",            svg_01_tcc_loop),
    ("02-prompt-anatomy.svg",      svg_02_prompt_anatomy),
    ("03-claude-md-cheatsheet.svg",svg_03_claude_md_cheatsheet),
    ("04-bon-scoring.svg",         svg_04_bon_scoring),
    ("05-test-debug-loop.svg",     svg_05_test_debug_loop),
    ("06-git-flow.svg",            svg_06_git_flow),
    ("07-screenshot-to-ui.svg",    svg_07_screenshot_to_ui),
    ("08-refactor-constraints.svg",svg_08_refactor_constraints),
    ("09-skills-catalogue.svg",    svg_09_skills_catalogue),
    ("10-five-axes.svg",           svg_10_five_axes),
]

for name, fn in SVGS:
    (OUT / name).write_text(fn())
    print(f"OK   {name}")
