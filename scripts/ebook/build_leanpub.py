#!/usr/bin/env python3
"""Generate a Leanpub (Markua) manuscript from the workshop sources.

Reuses the transform/redaction pipeline from ``build_ebook.py`` but emits the
layout Leanpub expects for GitHub/Dropbox sync instead of one self-contained
file:

    book/leanpub/manuscript/
        Book.txt            ordered list of files Leanpub includes
        Sample.txt          files for the free sample (front matter + ch.1)
        resources/          images (SVG diagrams rasterised to PNG)
        frontmatter.md      {frontmatter} how-to + prerequisites, then {mainmatter}
        01-*.md ... 11-*.md  one chapter per file (Markua: '#' == chapter)
        appendix-a-*.md     {backmatter} skills library

Markua specifics applied here:
    * Chapter heading is a single top-level '#'; body headings shift down one.
    * No manual table of contents (Leanpub generates it).
    * Images live in ``resources/`` and are referenced as ``resources/NAME.png``.
    * Intra-chapter cross-links get explicit ``{#id}`` heading attributes.
    * ``{frontmatter}`` / ``{mainmatter}`` / ``{backmatter}`` mark the sections.

The Python here remains standard-library only (Constitution Principle X). SVG
rasterisation shells out to whichever system converter is available
(rsvg-convert, cairosvg, Inkscape, ImageMagick, or macOS qlmanage); this is a
build-time tool, not a Python dependency.

Exit codes:
    0  success
    2  missing manifest/source or no SVG converter available
    1  unexpected error
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Reuse the proven assembly pipeline from the single-file builder.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ebook as eb  # noqa: E402

REPO_ROOT = eb.REPO_ROOT
PNG_WIDTH = 1600  # crisp on retina/print without bloating the manuscript


# --------------------------------------------------------------------------- #
# SVG -> PNG rasterisation (best available system converter)
# --------------------------------------------------------------------------- #
def _run(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def rasterise_svg(src: Path, dst: Path) -> bool:
    """Render an SVG to PNG at PNG_WIDTH using the first available tool."""
    dst.parent.mkdir(parents=True, exist_ok=True)

    if shutil.which("rsvg-convert"):
        if _run(["rsvg-convert", "-w", str(PNG_WIDTH), "-o", str(dst), str(src)]):
            return True
    if shutil.which("cairosvg"):
        if _run(["cairosvg", str(src), "-o", str(dst),
                 "--output-width", str(PNG_WIDTH)]):
            return True
    if shutil.which("inkscape"):
        if _run(["inkscape", str(src), "--export-type=png",
                 f"--export-filename={dst}", f"--export-width={PNG_WIDTH}"]):
            return True
    for magick in ("magick", "convert"):
        if shutil.which(magick):
            base = [magick] if magick == "magick" else []
            if _run(base + ["-background", "none", "-density", "200",
                            str(src), "-resize", f"{PNG_WIDTH}x", str(dst)]):
                return True
    if shutil.which("qlmanage"):
        # qlmanage writes <name>.svg.png into the output dir; rename after.
        if _run(["qlmanage", "-t", "-s", str(PNG_WIDTH),
                 "-o", str(dst.parent), str(src)]):
            produced = dst.parent / (src.name + ".png")
            if produced.is_file():
                produced.replace(dst)
                return True
    return False


# --------------------------------------------------------------------------- #
# Image handler: copy raster images, rasterise SVGs, into resources/
# --------------------------------------------------------------------------- #
class ResourceCollector:
    """Maps repo-relative image paths to ``resources/NAME.png`` targets."""

    def __init__(self, resources_dir: Path) -> None:
        self.resources_dir = resources_dir
        self.cache: dict[str, str] = {}
        self.failures: list[str] = []

    def __call__(self, repo_rel: str) -> str | None:
        if repo_rel in self.cache:
            return self.cache[repo_rel]
        src = REPO_ROOT / repo_rel
        if not src.is_file():
            return None

        if src.suffix.lower() == ".svg":
            out_name = src.stem + ".png"
            dst = self.resources_dir / out_name
            if not rasterise_svg(src, dst):
                self.failures.append(repo_rel)
                return None
        else:
            out_name = src.name
            dst = self.resources_dir / out_name
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)

        target = f"resources/{out_name}"
        self.cache[repo_rel] = target
        return target


# --------------------------------------------------------------------------- #
# Manuscript assembly
# --------------------------------------------------------------------------- #
def chapter_filename(chapter: dict) -> str:
    slug = eb.slugify(chapter["title"])
    return f"{chapter['number']}-{slug}.md"


def front_matter_md(manifest: dict, include_solutions: bool) -> str:
    meta = manifest["metadata"]
    p: list[str] = ["{frontmatter}", ""]

    p.append("# How to use this book")
    p.append("")
    p.append(
        f"*{meta['title']} — {meta['subtitle']}*  ")
    p.append(f"Instructor: {meta['instructor']} · Edition: {meta['edition']}")
    p.append("")
    p.append(
        "This book is the complete Claude Code Bootcamp. It compiles the "
        "workshop's eleven parts into continuous prose, with the hands-on "
        "exercises embedded in each chapter so you can build as you read. You "
        "direct Claude Code; it implements; you review and merge. You are always "
        "the engineer of record."
    )
    p.append("")
    repo = meta.get("companion_repo")
    if repo:
        p.append(
            f"Every exercise and reference solution also lives in the companion "
            f"repository, the [Claude Code Bootcamp repository]({repo}). Clone it "
            f"and work each module from the live files; each chapter links directly "
            f"to its exercise there."
        )
        p.append("")
    if include_solutions:
        p.append(
            "Reference solutions are included at the end of each project chapter. "
            "Treat them as a checklist to compare against *after* you have produced "
            "your own deliverable — not as something to copy."
        )
    else:
        p.append(
            "Reference solutions are **not** included in this edition. Work each "
            "exercise to its Definition of Done on your own."
        )
    p.append("")

    p.append("# Prerequisites and pre-work")
    p.append("")
    p.append("Complete this checklist before working through the chapters (~30 min):")
    p.append("")
    p.append("- Claude Code installed and signed in (any tier)")
    p.append("- Python 3.11+ on `PATH` (primary track)")
    p.append("- Node.js 20+ on `PATH` (secondary track for parts 2/4/5)")
    p.append("- Git >= 2.30 on `PATH`")
    p.append("- An IDE you can drive (VS Code recommended)")
    p.append("- macOS / Linux / Windows-via-WSL2 — native PowerShell is not supported")
    p.append("")
    p.append("{mainmatter}")
    p.append("")
    return eb.collapse_blank_lines("\n".join(p)).strip() + "\n"


def chapter_md(chapter: dict, include_solutions: bool, link_map: dict,
               img_handler, manifest: dict) -> str:
    p: list[str] = [f"# {chapter['number']}. {chapter['title']}", ""]

    body = eb.transform(eb.read(chapter["slide"]), chapter["slide"],
                        link_map, heading_shift=1, img_handler=img_handler)
    p.append(body)
    p.append("")

    if chapter.get("exercise"):
        ex_id = eb.exercise_anchor(chapter)
        p.append(f"## Hands-on exercise — Module {chapter['number']} {{#{ex_id}}}")
        p.append("")
        p.extend(eb.companion_callout(manifest, chapter, include_solutions))
        p.append(eb.transform(eb.read(chapter["exercise"]), chapter["exercise"],
                              link_map, heading_shift=1, img_handler=img_handler))
        p.append("")

    if include_solutions and chapter.get("solution"):
        sol_id = eb.solution_anchor(chapter)
        p.append(f"## Solution — Module {chapter['number']} {{#{sol_id}}}")
        p.append("")
        p.append(eb.transform(eb.read(chapter["solution"]), chapter["solution"],
                              link_map, heading_shift=1, img_handler=img_handler))
        p.append("")

    return eb.collapse_blank_lines("\n".join(p)).strip() + "\n"


def back_matter_md(manifest: dict, link_map: dict, img_handler) -> str:
    back = manifest.get("back_matter", {})
    p: list[str] = ["{backmatter}", "", "# Appendix A — Skills Library", ""]
    if back.get("skills"):
        p.append(eb.transform(eb.read(back["skills"]), back["skills"],
                              link_map, heading_shift=1, img_handler=img_handler))
        p.append("")
    p.append(
        "Your proof of work is the portfolio you build across the chapters: one "
        "`module-NN/` deliverable per project, plus the reusable Skills Library "
        "above. Keep practicing the Plan → Implement → Test → Review → Commit "
        "loop on your own projects."
    )
    p.append("")
    return eb.collapse_blank_lines("\n".join(p)).strip() + "\n"


def build(manifest: dict, out_dir: Path, include_solutions: bool) -> None:
    manuscript = out_dir / "manuscript"
    resources = manuscript / "resources"
    # Start clean so removed assets don't linger.
    if manuscript.exists():
        shutil.rmtree(manuscript)
    resources.mkdir(parents=True, exist_ok=True)

    link_map = eb.build_link_map(manifest)
    collector = ResourceCollector(resources)

    files: list[str] = []

    # Front matter.
    (manuscript / "frontmatter.md").write_text(
        front_matter_md(manifest, include_solutions), encoding="utf-8")
    files.append("frontmatter.md")

    # Chapters.
    chapter_files: list[str] = []
    for chapter in manifest["chapters"]:
        name = chapter_filename(chapter)
        (manuscript / name).write_text(
            chapter_md(chapter, include_solutions, link_map, collector, manifest),
            encoding="utf-8")
        chapter_files.append(name)
        files.append(name)

    # Back matter.
    appendix_name = "appendix-a-skills-library.md"
    (manuscript / appendix_name).write_text(
        back_matter_md(manifest, link_map, collector), encoding="utf-8")
    files.append(appendix_name)

    # Book.txt (full book) and Sample.txt (front matter + first chapter).
    (manuscript / "Book.txt").write_text("\n".join(files) + "\n", encoding="utf-8")
    sample = ["frontmatter.md"]
    if chapter_files:
        sample.append(chapter_files[0])
    (manuscript / "Sample.txt").write_text("\n".join(sample) + "\n", encoding="utf-8")

    if collector.failures:
        eb.fail(
            "SVG rasterisation failed for:\n  - "
            + "\n  - ".join(collector.failures)
            + "\nInstall one of: rsvg-convert, cairosvg, inkscape, ImageMagick."
        )

    print(
        f"build_leanpub: wrote {len(files)} manuscript file(s) + "
        f"{len(collector.cache)} resource(s) -> {manuscript}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build a Leanpub (Markua) manuscript from the workshop sources.")
    parser.add_argument("--manifest",
                        default=str(Path(__file__).with_name("manifest.json")))
    parser.add_argument("--output",
                        default=str(REPO_ROOT / "book" / "leanpub"))
    parser.add_argument("--no-solutions", action="store_true",
                        help="Exclude reference-solution sections.")
    args = parser.parse_args(argv)

    manifest = eb.load_manifest(Path(args.manifest))
    eb.validate_sources(manifest)

    include_solutions = manifest.get("metadata", {}).get("include_solutions", True)
    if args.no_solutions:
        include_solutions = False

    build(manifest, Path(args.output), include_solutions)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
