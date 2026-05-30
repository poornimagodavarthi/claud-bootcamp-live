#!/usr/bin/env bash
# Validate the generated Leanpub (Markua) manuscript.
#
# Rebuilds the manuscript to a temporary directory and asserts the Markua/
# Leanpub contract holds: one chapter heading per file (fence-aware), section
# markers present, images resolve to real resource files, intra-chapter links
# resolve, and no data URIs / external refs / leaked chrome / branding survive.
#
# Usage: scripts/check-leanpub.sh [--keep]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

KEEP=0
[[ "${1:-}" == "--keep" ]] && KEEP=1

TMP="$(mktemp -d -t claude-leanpub.XXXXXX)"
cleanup() { [[ "$KEEP" -eq 0 ]] && rm -rf "$TMP"; }
trap cleanup EXIT

python3 "$SCRIPT_DIR/ebook/build_leanpub.py" --output "$TMP" >/dev/null

python3 - "$TMP/manuscript" <<'PY'
import re
import sys
from pathlib import Path

man = Path(sys.argv[1])
results = []  # (id, ok, detail)


def check(cid, ok, detail=""):
    results.append((cid, ok, detail))


def classify(text):
    """Yield (lineno, line, in_fence) honouring fenced code blocks."""
    in_fence, token = False, ""
    for i, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^\s*(```+|~~~+)", line)
        if m:
            tok = m.group(1)[0] * 3
            if not in_fence:
                in_fence, token = True, tok
            elif line.strip().startswith(token):
                in_fence, token = False, ""
            yield i, line, True
            continue
        yield i, line, in_fence


book = man / "Book.txt"
files = [l.strip() for l in book.read_text(encoding="utf-8").splitlines() if l.strip()]

# LP-1: every file listed in Book.txt exists.
missing = [f for f in files if not (man / f).is_file()]
check("LP-1", not missing, f"missing files {missing}")

# LP-2: chapter heading count is sane (fence-aware). Numbered chapters and the
# appendix have exactly one '#'; front matter may hold several front-matter
# chapters (>=1).
bad_h1 = []
for f in files:
    text = (man / f).read_text(encoding="utf-8")
    n = len([t for i, t, fence in classify(text)
             if not fence and re.match(r"^# \S", t)])
    expect_single = bool(re.match(r"^\d", f)) or f.startswith("appendix")
    ok = (n == 1) if expect_single else (n >= 1)
    if not ok:
        bad_h1.append(f"{f}={n}")
check("LP-2", not bad_h1, f"unexpected chapter-heading counts: {bad_h1}")

# LP-3: section markers present.
fm = (man / "frontmatter.md").read_text(encoding="utf-8")
appendix = next((man / f for f in files if f.startswith("appendix")), None)
bm = appendix.read_text(encoding="utf-8") if appendix else ""
check("LP-3",
      "{frontmatter}" in fm and "{mainmatter}" in fm and "{backmatter}" in bm,
      "expected {frontmatter}+{mainmatter} in frontmatter.md and {backmatter} in appendix")

# LP-4: every resources/ image reference resolves to a real file.
img_re = re.compile(r"!\[[^\]]*\]\((resources/[^)\s]+)\)")
broken_img = []
for f in files:
    for i, t, fence in classify((man / f).read_text(encoding="utf-8")):
        if fence:
            continue
        for m in img_re.finditer(t):
            if not (man / m.group(1)).is_file():
                broken_img.append(f"{f}:{m.group(1)}")
check("LP-4", not broken_img, f"missing image targets {broken_img[:3]}")

# LP-5: intra-file anchor links resolve to a {#id} in the same file.
link_re = re.compile(r"\]\(#([^)]+)\)")
id_re = re.compile(r"\{#([^}]+)\}")
broken_link = []
for f in files:
    text = (man / f).read_text(encoding="utf-8")
    ids = set(id_re.findall(text))
    for i, t, fence in classify(text):
        if fence:
            continue
        for m in link_re.finditer(t):
            if m.group(1) not in ids:
                broken_link.append(f"{f}:#{m.group(1)}")
check("LP-5", not broken_link, f"unresolved links {broken_link[:3]}")

# LP-6: self-contained resources — no data URIs, no external ../ refs.
ext = []
for f in files:
    for i, t, fence in classify((man / f).read_text(encoding="utf-8")):
        if "data:image" in t or re.search(r"\]\(\.\.?/", t):
            ext.append(f"{f}:{i}")
check("LP-6", not ext, f"data-uri/external refs {ext[:3]}")

# LP-7: no leaked Marp chrome / HTML, no Packt-certification branding (outside fences).
chrome_re = re.compile(r"<(span|div|img|section|header|footer)\b|<!--|class=", re.I)
brand_re = re.compile(r"Packt|certif|\bexam\b", re.I)
leaks = []
for f in files:
    for i, t, fence in classify((man / f).read_text(encoding="utf-8")):
        if fence:
            continue
        if chrome_re.search(t) or brand_re.search(t):
            leaks.append(f"{f}:{i}")
check("LP-7", not leaks, f"leaked chrome/branding {leaks[:3]}")

all_ok = all(ok for _, ok, _ in results)
for cid, ok, detail in results:
    status = "PASS" if ok else "FAIL"
    suffix = f" — {detail}" if (detail and not ok) else ""
    print(f"  {status}  {cid}{suffix}")
print()
if all_ok:
    print("check-leanpub: PASS (Markua manuscript contract holds)")
    sys.exit(0)
print("check-leanpub: FAIL (one or more assertions failed)")
sys.exit(1)
PY
