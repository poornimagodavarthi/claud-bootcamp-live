#!/usr/bin/env python3
"""
Restyle the 10 intermediate decks to use the wow-intermediate theme.
Idempotent: re-running on an already-restyled deck is a no-op.

This handles:
  * front-matter: theme=wow-intermediate; add header line
  * cover slide: tpl-cover marker, module-chip, H1, hero icon (Decision 2)
  * Module 2..10 cover: drop "Instructor:" credit line (Decision 7)
  * per-slide _class directives for each canonical section
  * tpl-next + is-finale on Module 10 Transition slide
  * polish-log HTML comment at EOF (initialised; T027-T036 will append entries)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SLIDES = ROOT / "slides"

# Decision 2: per-module hero icon and short title.
META = {
    "01": dict(icon="terminal", short="Setup & AI-First Mindset", duration="20 min"),
    "02": dict(icon="pencil",   short="Prompting Like a Tech Lead", duration="24 min"),
    "03": dict(icon="book",     short="Project Context with CLAUDE.md", duration="22 min"),
    "04": dict(icon="play",     short="Build Faster with Best-of-N", duration="30 min"),
    "05": dict(icon="shield",   short="Testing, Debugging & Self-Review", duration="28 min"),
    "06": dict(icon="folder",   short="Git Workflows for Safe AI Dev", duration="22 min"),
    "07": dict(icon="eye",      short="Multimodal: Screenshot to UI", duration="30 min"),
    "08": dict(icon="file",     short="Refactoring & Documentation at Scale", duration="24 min"),
    "09": dict(icon="lightbulb",short="Commands, Hooks & Reusable Workflows", duration="22 min"),
    "10": dict(icon="award",    short="Production Readiness", duration="18 min"),
}

# H2 anchor → slide-class marker. Editable sections get no class (defaults).
SECTION_CLASS = {
    "## Promise":                       "tpl-objectives",
    "## Live demo flow":                "tpl-demo",
    "## Mini project":                  "tpl-show",
    "## Step-by-step lab":              "tpl-try",
    "## Suggested Claude Code prompts": "tpl-show",
    "## Deliverable checklist":         "tpl-done",
    "## Definition of done":            "tpl-done",
    "## Review checkpoint":             "tpl-try",
    "## Transition to next module":     "tpl-next",
}

POLISH_LOG_HEADER = "<!-- polish-log\n(intermediate-content-polish feature 004) — populated during US2 polish pass.\n-->\n"

def restyle(path: Path) -> bool:
    text = path.read_text()
    mod = re.search(r"part-(\d{2})", path.name).group(1)
    meta = META[mod]
    short = meta["short"]
    icon = meta["icon"]
    duration = meta["duration"]
    mod_num = str(int(mod))  # "1".."10"

    # 1. Front-matter
    fm_match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm_match:
        print(f"{path.name}: no front-matter found", file=sys.stderr)
        return False
    fm = fm_match.group(1)
    fm_new = re.sub(r"^theme:.*$", "theme: wow-intermediate", fm, flags=re.M)
    if "header:" not in fm_new:
        # insert header after theme line
        fm_new = re.sub(
            r"(^theme: wow-intermediate$)",
            rf"\1\nheader: 'Claude Code Bootcamp · Day 1 · Module {mod}'",
            fm_new,
            count=1,
            flags=re.M,
        )
    text = text[:fm_match.start()] + f"---\n{fm_new}\n---\n" + text[fm_match.end():]

    # 2. Cover slide: replace from "<!-- duration: ..." up to first "---" separator.
    cover_re = re.compile(
        r"(<!-- duration: [^>]*-->\n)"           # 1: duration marker
        r"(?:<!--[^>]*-->\n)*"                   # any pre-existing slide markers (idempotent strip)
        r"(?:<span class=\"module-chip\">[^<]*</span>\n+)?"  # existing chip
        r"(?:#[^\n]*\n+)?"                       # existing H1 (idempotent) ...
        r"(?:## Module \d+ — [^\n]*\n+)?"         # ... or original H2 title
        r"([^\n]*\n)?"                            # course-name line
        r"(Instructor: [^\n]*\n)?"                # optional instructor credit
        r"\n*"
        r"(?=---\n)",                             # up to first slide separator
        re.M,
    )
    cover_re_simple = re.compile(
        r"(<!-- duration: [^>]*-->\n)"
        r"\n*"
        r"## Module \d+ — ([^\n]+)\n"
        r"\n"
        r"([^\n]*)\n"                              # course-name line (Claude Code Bootcamp · ...)
        r"(?:Instructor: [^\n]*\n)?"
        r"\n*"
        r"(?=---\n)",
        re.M,
    )

    def cover_replacement(course_line: str) -> str:
        chip = f'<span class="module-chip">Module {mod} · {duration}</span>'
        h1 = f"# {short}"
        instr = "\nInstructor: **Luca Berton** · Endorsed by **Packt Certification**\n" if mod == "01" else ""
        hero = f'\n<img class="hero-icon" src="themes/icons/{icon}.svg" alt="" />\n'
        return (
            f"<!-- duration: {duration} -->\n"
            f"<!-- _class: tpl-cover -->\n"
            f"<!-- _paginate: false -->\n"
            f"<!-- _header: \"\" -->\n\n"
            f"{chip}\n\n"
            f"{h1}\n\n"
            f"{course_line}\n"
            f"{instr}"
            f"{hero}\n"
        )

    m = cover_re_simple.search(text)
    if m:
        course_line = m.group(3).strip()
        text = text[:m.start()] + cover_replacement(course_line) + text[m.end():]
    else:
        # Idempotent path: already restyled. Detect by tpl-cover marker.
        if "<!-- _class: tpl-cover -->" not in text:
            print(f"{path.name}: cover slide pattern unrecognised", file=sys.stderr)
            return False

    # 3. Inject per-slide class directives before each canonical H2.
    for h2, cls in SECTION_CLASS.items():
        marker = f"<!-- _class: {cls} -->"
        # Idempotent: skip if marker already directly precedes the H2.
        pattern_present = re.compile(
            rf"{re.escape(marker)}\n\n{re.escape(h2)}\b", re.M
        )
        if pattern_present.search(text):
            continue
        # Insert: replace "---\n\n## Section" with marker block.
        pattern = re.compile(
            rf"^---\n\n{re.escape(h2)}\b", re.M
        )
        replacement = f"---\n\n{marker}\n\n{h2[3:]}"  # strip leading "## " then re-add via h2
        # Actually simpler: just rebuild
        replacement = f"---\n\n{marker}\n\n{h2}"
        text, n = pattern.subn(replacement, text, count=1)
        if n == 0:
            # H2 not present in this deck (some decks rename sections).
            pass

    # 4. Module 10 finale on Transition slide.
    if mod == "10":
        text = text.replace(
            "<!-- _class: tpl-next -->\n\n## Transition to next module",
            "<!-- _class: tpl-next is-finale -->\n\n## Transition to next module",
        )

    # 5. Polish-log header at EOF (only if absent).
    if "<!-- polish-log" not in text:
        if not text.endswith("\n"):
            text += "\n"
        text += "\n" + POLISH_LOG_HEADER

    path.write_text(text)
    return True

def main():
    targets = sorted(SLIDES.glob("part-*.md"))
    if not targets:
        print("No intermediate decks found", file=sys.stderr)
        sys.exit(1)
    failures = []
    for p in targets:
        ok = restyle(p)
        print(("OK   " if ok else "FAIL ") + p.name)
        if not ok:
            failures.append(p)
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
