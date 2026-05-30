#!/usr/bin/env python3
"""Assemble the Claude Code Bootcamp workshop into a single Markdown ebook.

Reads a JSON manifest (scripts/ebook/manifest.json), transforms each Marp slide
deck into clean prose, embeds the hands-on exercises and reference solutions,
adds front matter (title page + intro + prerequisites + table of contents) and
back matter (skills library appendix), inlines images as base64 data URIs, and
writes one self-contained Markdown file.

Standard library only (Constitution Principle X): re, json, pathlib, argparse.

Exit codes:
    0  success
    2  missing / invalid manifest or source
    1  unexpected error
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from pathlib import Path

# Repo root is two levels up from this file: scripts/ebook/build_ebook.py
REPO_ROOT = Path(__file__).resolve().parents[2]

# Output lives at book/dist/, i.e. two directories below the repo root, so
# repo-root-relative resources must be reached with this prefix from the ebook.
OUTPUT_REL_PREFIX = "../../"


# --------------------------------------------------------------------------- #
# Manifest loading + validation
# --------------------------------------------------------------------------- #
def load_manifest(manifest_path: Path) -> dict:
    if not manifest_path.is_file():
        fail(f"manifest not found: {manifest_path}")
    try:
        return json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in manifest {manifest_path}: {exc}")


def validate_sources(manifest: dict) -> None:
    """Fail fast (exit 2) if any non-null source path is missing."""
    missing: list[str] = []

    def check(rel: str | None) -> None:
        if rel and not (REPO_ROOT / rel).exists():
            missing.append(rel)

    check(manifest.get("front_matter", {}).get("source"))
    for chapter in manifest.get("chapters", []):
        check(chapter.get("slide"))
        check(chapter.get("exercise"))
        check(chapter.get("solution"))
    back = manifest.get("back_matter", {})
    check(back.get("skills"))

    if missing:
        fail("missing source file(s):\n  - " + "\n  - ".join(missing))


# --------------------------------------------------------------------------- #
# Anchor helpers (GitHub-style slugs, chapter-scoped via unique heading text)
# --------------------------------------------------------------------------- #
_slug_strip = re.compile(r"[^\w\- ]+")


def slugify(text: str) -> str:
    """GitHub-compatible heading slug.

    Mirrors GitHub's algorithm: lowercase, drop characters that are not word
    chars / spaces / hyphens, then turn spaces into hyphens. Repeated hyphens
    are intentionally NOT collapsed (e.g. "A & B" -> "a--b") so generated TOC
    links match the anchors GitHub derives from the headings.
    """
    text = text.strip().lower()
    text = _slug_strip.sub("", text)
    return text.replace(" ", "-")


def chapter_anchor(chapter: dict) -> str:
    return slugify(f"{chapter['number']} {chapter['title']}")


def exercise_anchor(chapter: dict) -> str:
    return slugify(f"Hands-on exercise — Module {chapter['number']}")


def solution_anchor(chapter: dict) -> str:
    return slugify(f"Solution — Module {chapter['number']}")


# --------------------------------------------------------------------------- #
# Companion-repository references
# --------------------------------------------------------------------------- #
def companion_url(manifest: dict, repo_rel: str) -> str | None:
    """Absolute GitHub URL for a repo-relative path in the companion repo.

    Returns ``None`` when no ``companion_repo`` is configured so callers can
    skip emitting the reference.
    """
    meta = manifest.get("metadata", {})
    base = (meta.get("companion_repo") or "").rstrip("/")
    if not base:
        return None
    branch = meta.get("companion_branch", "main")
    return f"{base}/blob/{branch}/{repo_rel.lstrip('/')}"


def companion_callout(manifest: dict, chapter: dict,
                      include_solutions: bool) -> list[str]:
    """Blockquote linking a chapter's exercise (and solution) in the repo.

    Returns the lines to insert, or an empty list when the chapter has no
    exercise or no companion repo is configured.
    """
    exercise = chapter.get("exercise")
    if not exercise:
        return []
    ex_url = companion_url(manifest, exercise)
    if ex_url is None:
        return []

    lines = [
        f"> **Companion repository** — Work this exercise from the live files in "
        f"the [Claude Code Bootcamp repository]({manifest['metadata']['companion_repo']}): "
        f"[`{exercise}`]({ex_url}).",
    ]
    solution = chapter.get("solution")
    if include_solutions and solution:
        sol_url = companion_url(manifest, solution)
        if sol_url is not None:
            lines.append(
                f"> Reference solution: [`{solution}`]({sol_url})."
            )
    lines.append("")
    return lines


# --------------------------------------------------------------------------- #
# Source transformation (fence-aware)
# --------------------------------------------------------------------------- #
_frontmatter_re = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
_inline_comment_re = re.compile(r"<!--.*?-->", re.DOTALL)
_span_unwrap_re = re.compile(r"<span\b[^>]*>(.*?)</span>", re.DOTALL | re.IGNORECASE)
_img_tag_re = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
_stray_tag_re = re.compile(r"</?(?:div|br|hr|p|section)\b[^>]*>", re.IGNORECASE)
_heading_re = re.compile(r"^(#{1,6})(\s)")
_md_link_re = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")
_fence_re = re.compile(r"^\s*(```+|~~~+)")

# --------------------------------------------------------------------------- #
# Branding redaction (applied to imported content, outside code fences only).
# Removes Packt branding and certification/exam framing from the ebook without
# editing the slide/exercise source files (Constitution Principle III).
# --------------------------------------------------------------------------- #

# Heading text (after the leading #s) that triggers dropping the whole
# subsection up to the next heading.
_redact_section_re = re.compile(r"^Exam briefing\b", re.IGNORECASE)

# Whole prose lines to drop entirely when matched.
_redact_drop_res = [
    re.compile(r"\*\*Certificate\*\*:.*certificate", re.IGNORECASE),
    re.compile(r"Upload your submission zip", re.IGNORECASE),
    re.compile(r"^\s*-\s*\[\s*\]\s*Three assessment artefacts", re.IGNORECASE),
    re.compile(r"^\s*-\s*\[\s*\]\s*Weighted score", re.IGNORECASE),
]

# In-line substitutions to neutralise branding while keeping prose coherent.
_redact_subs = [
    (re.compile(r"\s*·\s*Endorsed by \*\*Packt Certification\*\*"), ""),
    (re.compile(r"\*\*Endorsed by Packt Certification\*\*[^\n]*"), ""),
    (re.compile(r"Q&A, Exam Briefing & Next Steps"), "Q&A & Next Steps"),
    (re.compile(r"the three frameworks you keep, the exam, and Monday"),
     "the three frameworks you keep and Monday"),
    (re.compile(r"Q&A, the exam briefing, and Monday"), "Q&A and Monday"),
    (re.compile(r"You're certified-ready"), "The whole bootcamp"),
]


def strip_frontmatter(text: str) -> tuple[str, str | None]:
    """Remove leading YAML frontmatter; return (body, title-if-found)."""
    title = None
    m = _frontmatter_re.match(text)
    if m:
        fm = m.group(0)
        tm = re.search(r'^title:\s*"?(.*?)"?\s*$', fm, re.MULTILINE)
        if tm:
            title = tm.group(1).strip()
        text = text[m.end():]
    return text, title


# Extensions to MIME types for images that are inlined as data URIs so the
# ebook is fully self-contained (no external asset references).
_IMAGE_MIME = {
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def embed_image(repo_rel: str) -> str | None:
    """Return a base64 data URI for a repo-relative image, or None.

    Inlining keeps the generated ebook self-contained: it renders even when
    detached from the repository (single-file deliverable).
    """
    path = REPO_ROOT / repo_rel
    mime = _IMAGE_MIME.get(path.suffix.lower())
    if mime is None or not path.is_file():
        return None
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def rewrite_links(line: str, source_dir: Path, link_map: dict[str, str],
                  img_handler=None) -> str:
    """Rewrite Markdown links/images for an ebook-only reader.

    - In-ebook source targets -> in-document anchor.
    - Images: by default inlined as base64 data URIs (self-contained build);
      when ``img_handler`` is given it is called with the repo-relative image
      path and must return a replacement target (e.g. ``resources/foo.png``).
    - External http(s)/anchor links -> unchanged.
    - Repo links with no ebook target -> de-linked to plain text (no broken link).
    """

    def repl(match: re.Match) -> str:
        bang, text, target, title = match.groups()
        title = title or ""

        # Leave external links and pure anchors untouched.
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        # Split optional in-target anchor (file.md#section).
        path_part, _, _frag = target.partition("#")
        resolved = (source_dir / path_part).resolve()
        try:
            repo_rel = resolved.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            repo_rel = None

        # Images: by default inline as a base64 data URI so the ebook is
        # self-contained; an ``img_handler`` can redirect to a resource file.
        if bang == "!":
            if img_handler and repo_rel:
                new_target = img_handler(repo_rel)
                if new_target:
                    return f"![{text}]({new_target}{title})"
            data_uri = embed_image(repo_rel) if repo_rel else None
            if data_uri:
                return f"![{text}]({data_uri})"
            rel = OUTPUT_REL_PREFIX + repo_rel if repo_rel else target
            return f"![{text}]({rel}{title})"

        # Non-image link whose target is included in the ebook.
        if repo_rel and repo_rel in link_map:
            return f"[{text}](#{link_map[repo_rel]})"

        # Repo file not in the ebook -> de-link to avoid a broken reference.
        if repo_rel is not None:
            return text or path_part

        return match.group(0)

    return _md_link_re.sub(repl, line)


def transform(text: str, source_rel: str, link_map: dict[str, str],
              heading_shift: int = 2, img_handler=None) -> str:
    """Convert one Marp/markdown source file into ebook prose.

    Fence-aware: content inside fenced code blocks is never altered (ST-6/A2).
    """
    text, _ = strip_frontmatter(text)
    source_dir = (REPO_ROOT / source_rel).resolve().parent

    out: list[str] = []
    in_fence = False
    fence_token = ""
    in_comment = False
    skip_section = False

    for raw in text.splitlines():
        # Fence toggling (only when not mid-comment).
        fence_m = _fence_re.match(raw)
        if fence_m and not in_comment:
            token = fence_m.group(1)
            if not in_fence:
                in_fence, fence_token = True, token[:3]
            elif raw.strip().startswith(fence_token):
                in_fence = False
            out.append(raw)
            continue

        if in_fence:
            out.append(raw)
            continue

        line = raw

        # Multi-line HTML comment handling.
        if in_comment:
            if "-->" in line:
                line = line.split("-->", 1)[1]
                in_comment = False
            else:
                continue  # still inside comment; drop line
        line = _inline_comment_re.sub("", line)
        if "<!--" in line:
            line = line.split("<!--", 1)[0]
            in_comment = True

        # Slide separator -> soft paragraph break.
        if line.strip() == "---":
            out.append("")
            continue

        # Strip / unwrap presentation-only HTML chrome.
        line = _span_unwrap_re.sub(r"\1", line)
        line = _img_tag_re.sub("", line)          # decorative slide icons
        line = _stray_tag_re.sub("", line)

        # Branding redaction (Packt / certification / exam framing).
        hsec = _heading_re.match(line)
        heading_text = line[hsec.end():].strip() if hsec else None
        if skip_section:
            if hsec and not _redact_section_re.match(heading_text or ""):
                skip_section = False  # a new (kept) section begins
            else:
                continue
        if hsec and _redact_section_re.match(heading_text or ""):
            skip_section = True
            continue
        if any(r.search(line) for r in _redact_drop_res):
            continue
        for _pat, _repl in _redact_subs:
            line = _pat.sub(_repl, line)
        line = line.rstrip()

        # Demote headings beneath the chapter heading.
        hm = _heading_re.match(line)
        if hm:
            level = min(len(hm.group(1)) + heading_shift, 6)
            line = "#" * level + hm.group(2) + line[hm.end():]

        # Rewrite links / images.
        line = rewrite_links(line, source_dir, link_map, img_handler)

        out.append(line)

    return collapse_blank_lines("\n".join(out)).strip()


def collapse_blank_lines(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text)


# --------------------------------------------------------------------------- #
# Assembly
# --------------------------------------------------------------------------- #
def build_link_map(manifest: dict) -> dict[str, str]:
    """Map repo-relative source paths -> in-document anchors."""
    link_map: dict[str, str] = {}
    for chapter in manifest["chapters"]:
        link_map[chapter["slide"]] = chapter_anchor(chapter)
        if chapter.get("exercise"):
            link_map[chapter["exercise"]] = exercise_anchor(chapter)
        if chapter.get("solution"):
            link_map[chapter["solution"]] = solution_anchor(chapter)
    return link_map


def read(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def build_front_matter(manifest: dict, include_solutions: bool,
                       link_map: dict) -> str:
    meta = manifest["metadata"]
    parts: list[str] = []

    # Title page (single H1 for the whole book -> ST-1).
    parts.append(f"# {meta['title']} — {meta['subtitle']}")
    parts.append("")
    parts.append(f"**Instructor:** {meta['instructor']}  ")
    parts.append(f"**Edition:** {meta['edition']}")
    parts.append("")

    # Introduction.
    parts.append("## How to use this book")
    parts.append("")
    parts.append(
        "This ebook is the complete Claude Code Bootcamp in a single document. "
        "It compiles the workshop's eleven parts into continuous prose, with the "
        "hands-on exercises embedded in each chapter so you can build as you read. "
        "You direct Claude Code; it implements; you review and merge. You are "
        "always the engineer of record."
    )
    parts.append("")
    repo = meta.get("companion_repo")
    if repo:
        parts.append(
            f"Every exercise and reference solution also lives in the companion "
            f"repository, the [Claude Code Bootcamp repository]({repo}). Clone it "
            f"and work each module from the live files; each chapter links directly "
            f"to its exercise there."
        )
        parts.append("")
    if include_solutions:
        parts.append(
            "Reference solutions are included as a labeled section at the end of "
            "each project chapter. Treat them as a checklist to compare against "
            "*after* you have produced your own deliverable — not as something to copy."
        )
    else:
        parts.append(
            "Reference solutions are **not** included in this edition of the ebook. "
            "Work each exercise to its Definition of Done on your own."
        )
    parts.append("")

    # Prerequisites / pre-work.
    parts.append("## Prerequisites and pre-work")
    parts.append("")
    parts.append("Complete this checklist before working through the chapters (~30 min):")
    parts.append("")
    parts.append("- Claude Code installed and signed in (any tier)")
    parts.append("- Python 3.11+ on `PATH` (primary track)")
    parts.append("- Node.js 20+ on `PATH` (secondary track for parts 2/4/5)")
    parts.append("- Git ≥ 2.30 on `PATH`")
    parts.append("- An IDE you can drive (VS Code recommended)")
    parts.append("- macOS / Linux / Windows-via-WSL2 — native PowerShell is not supported")
    parts.append("")

    # Table of contents (ST-3).
    parts.append("## Table of contents")
    parts.append("")
    for chapter in manifest["chapters"]:
        anchor = chapter_anchor(chapter)
        parts.append(f"{int(chapter['number'])}. [{chapter['number']}. {chapter['title']}](#{anchor})")
    parts.append("- [Appendix A — Skills Library](#appendix-a--skills-library)")
    parts.append("")

    return "\n".join(parts)


def build_chapter(chapter: dict, include_solutions: bool,
                  link_map: dict, manifest: dict) -> str:
    parts: list[str] = []
    parts.append(f"## {chapter['number']}. {chapter['title']}")
    parts.append("")

    body = transform(read(chapter["slide"]), chapter["slide"], link_map)
    parts.append(body)
    parts.append("")

    # US2: embedded exercise.
    if chapter.get("exercise"):
        parts.append(f"### Hands-on exercise — Module {chapter['number']}")
        parts.append("")
        parts.extend(companion_callout(manifest, chapter, include_solutions))
        parts.append(transform(read(chapter["exercise"]), chapter["exercise"], link_map))
        parts.append("")

    # US2: reference solution appendix.
    if include_solutions and chapter.get("solution"):
        parts.append(f"### Solution — Module {chapter['number']}")
        parts.append("")
        parts.append(transform(read(chapter["solution"]), chapter["solution"], link_map))
        parts.append("")

    return "\n".join(parts)


def build_back_matter(manifest: dict, link_map: dict) -> str:
    back = manifest.get("back_matter", {})
    parts: list[str] = []

    # Appendix A — Skills Library.
    parts.append("## Appendix A — Skills Library")
    parts.append("")
    if back.get("skills"):
        parts.append(transform(read(back["skills"]), back["skills"], link_map))
        parts.append("")

    parts.append(
        "Your proof of work is the portfolio you build across the chapters: one "
        "`module-NN/` deliverable per project, plus the reusable Skills Library in "
        "Appendix A. Keep practicing the Plan → Implement → Test → Review → Commit "
        "loop on your own projects."
    )
    parts.append("")

    return "\n".join(parts)


def assemble(manifest: dict, include_solutions: bool) -> str:
    link_map = build_link_map(manifest)
    sections = [build_front_matter(manifest, include_solutions, link_map)]
    for chapter in manifest["chapters"]:
        sections.append(build_chapter(chapter, include_solutions, link_map, manifest))
    sections.append(build_back_matter(manifest, link_map))
    return collapse_blank_lines("\n\n".join(sections)).strip() + "\n"


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def fail(message: str) -> None:
    print(f"build_ebook: error: {message}", file=sys.stderr)
    sys.exit(2)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the workshop Markdown ebook.")
    parser.add_argument("--manifest", default=str(Path(__file__).with_name("manifest.json")))
    parser.add_argument("--output", default=str(REPO_ROOT / "book" / "dist" / "claude-code-bootcamp-ebook.md"))
    parser.add_argument("--no-solutions", action="store_true",
                        help="Exclude reference-solution appendices.")
    args = parser.parse_args(argv)

    manifest = load_manifest(Path(args.manifest))
    validate_sources(manifest)

    include_solutions = manifest.get("metadata", {}).get("include_solutions", True)
    if args.no_solutions:
        include_solutions = False

    try:
        ebook = assemble(manifest, include_solutions)
    except Exception as exc:  # noqa: BLE001 - surface as exit 1 per contract
        print(f"build_ebook: unexpected error: {exc}", file=sys.stderr)
        return 1

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(ebook, encoding="utf-8")

    chapters = len(manifest["chapters"])
    size = out_path.stat().st_size
    print(f"build_ebook: assembled {chapters} chapters -> {out_path} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
