#!/usr/bin/env bash
# Validate the generated workshop ebook against the structural contract
# (specs/006-workshop-ebook/contracts/ebook-structure.md, assertions ST-1..ST-11).
#
# Builds the ebook to a temporary file and asserts the contract holds. Prints
# PASS/FAIL per assertion and exits 0 only if every assertion passes.
#
# Usage: scripts/check-ebook.sh [--keep]
#   --keep   Leave the temporary build artifact on disk and print its path.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

KEEP=0
[[ "${1:-}" == "--keep" ]] && KEEP=1

TMP="$(mktemp -t claude-ebook.XXXXXX).md"
cleanup() { [[ "$KEEP" -eq 0 ]] && rm -f "$TMP"; }
trap cleanup EXIT

# Build with solutions included (default manifest setting) for full validation.
"$SCRIPT_DIR/build-ebook.sh" --output "$TMP" >/dev/null

python3 - "$TMP" <<'PY'
import re
import sys

path = sys.argv[1]
lines = open(path, encoding="utf-8").read().splitlines()

_slug_strip = re.compile(r"[^\w\- ]+")


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = _slug_strip.sub("", text)
    return text.replace(" ", "-")


# Classify lines as inside/outside fenced code blocks.
in_fence = False
fence_token = ""
content = []  # (lineno, text, in_fence)
for i, line in enumerate(lines, 1):
    stripped = line.lstrip()
    m = re.match(r"^(```+|~~~+)", stripped)
    if m:
        tok = m.group(1)[0] * 3
        if not in_fence:
            in_fence = True
            fence_token = tok
        elif stripped.startswith(fence_token):
            in_fence = False
            fence_token = ""
        content.append((i, line, True))
        continue
    content.append((i, line, in_fence))

prose = [(i, t) for (i, t, f) in content if not f]

results = []  # (id, ok, detail)


def check(cid, ok, detail=""):
    results.append((cid, ok, detail))


# ST-1: exactly one H1 outside fences.
h1 = [t for _, t in prose if re.match(r"^# \S", t)]
check("ST-1", len(h1) == 1, f"found {len(h1)} H1 line(s)")

# ST-2: chapters 01..11 in ascending order.
chap_nums = [int(m.group(1)) for _, t in prose
             if (m := re.match(r"^## (\d{2})\. ", t))]
check("ST-2", chap_nums == list(range(1, 12)),
      f"chapter sequence {chap_nums}")

# Collect heading anchors (outside fences) for ST-3/ST-7.
anchors = set()
for _, t in prose:
    hm = re.match(r"^#{1,6} (.+?)\s*$", t)
    if hm:
        anchors.add(slugify(hm.group(1)))

# ST-3: a Table of contents section exists.
has_toc = any(re.search(r"table of contents", t, re.I) for _, t in prose)
check("ST-3", has_toc, "Table of contents heading present")

# ST-4: chapters 01-10 each have a Hands-on exercise subsection.
ex_modules = {m.group(1) for _, t in prose
              if (m := re.match(r"^### Hands-on exercise — Module (\d{2})", t))}
missing_ex = [f"{n:02d}" for n in range(1, 11) if f"{n:02d}" not in ex_modules]
check("ST-4", not missing_ex, f"missing exercise modules {missing_ex}")

# ST-5: chapters 01-10 each have a Solution subsection (solutions included).
sol_modules = {m.group(1) for _, t in prose
               if (m := re.match(r"^### Solution — Module (\d{2})", t))}
missing_sol = [f"{n:02d}" for n in range(1, 11) if f"{n:02d}" not in sol_modules]
check("ST-5", not missing_sol, f"missing solution modules {missing_sol}")

# ST-6: no leaked Marp chrome outside fences.
leak_re = re.compile(r"<!--|class=|^marp:|^paginate:|<span|<img")
bare_sep_re = re.compile(r"^---\s*$")
leaks = [(i, t) for i, t in prose if leak_re.search(t) or bare_sep_re.match(t)]
check("ST-6", not leaks,
      f"{len(leaks)} leaked line(s)" + (f" e.g. L{leaks[0][0]}" if leaks else ""))

# ST-7: every in-document link resolves to a heading anchor.
link_re = re.compile(r"\]\(#([^)]+)\)")
broken = []
for i, t in prose:
    for m in link_re.finditer(t):
        if m.group(1) not in anchors:
            broken.append((i, m.group(1)))
check("ST-7", not broken,
      f"{len(broken)} broken link(s)" + (f" e.g. #{broken[0][1]}" if broken else ""))

# ST-8: front/back matter landmarks present.
text = "\n".join(t for _, t in prose)
fm_intro = bool(re.search(r"^## How to use this book", text, re.M))
appendix_a = bool(re.search(r"^## Appendix A — Skills Library", text, re.M))
check("ST-8", fm_intro and appendix_a,
      f"intro={fm_intro} appendixA={appendix_a}")

# ST-9: content images are Markdown; no raw decorative HTML chrome outside fences.
raw_html = [(i, t) for i, t in prose
            if re.search(r"<(span|div|img|section|header|footer)\b", t)]
check("ST-9", not raw_html,
      f"{len(raw_html)} raw HTML chrome line(s)")

# ST-10: Packt / certification / exam branding fully redacted (outside fences).
brand_re = re.compile(r"Packt|certif|\bexam\b", re.I)
brand = [(i, t) for i, t in prose if brand_re.search(t)]
check("ST-10", not brand,
      f"{len(brand)} branding line(s)" + (f" e.g. L{brand[0][0]}" if brand else ""))

# ST-11: self-contained — no external relative file references; images inlined
# as data URIs (the ebook must render detached from the repository).
ext_ref_re = re.compile(r"\]\(\.\.?/")
ext_refs = [(i, t) for (i, t, _f) in content if ext_ref_re.search(t)]
check("ST-11", not ext_refs,
      f"{len(ext_refs)} external relative ref(s)"
      + (f" e.g. L{ext_refs[0][0]}" if ext_refs else ""))

# Report.
all_ok = all(ok for _, ok, _ in results)
for cid, ok, detail in results:
    status = "PASS" if ok else "FAIL"
    suffix = f" — {detail}" if (detail and not ok) else ""
    print(f"  {status}  {cid}{suffix}")

print()
if all_ok:
    print("check-ebook: PASS (all structural assertions hold)")
    sys.exit(0)
print("check-ebook: FAIL (one or more assertions failed)")
sys.exit(1)
PY
