#!/usr/bin/env bash
# Build all workshop slide decks to PPTX (and optionally PDF/HTML) using Marp CLI.
#
# Usage:
#   ./deploy-pptx.sh              # PPTX only
#   ./deploy-pptx.sh --all        # PPTX + PDF + HTML
#   ./deploy-pptx.sh --pdf        # PPTX + PDF
#   ./deploy-pptx.sh --html       # PPTX + HTML
#   ./deploy-pptx.sh --clean      # remove dist/ before building
#
# Requirements:
#   - Node.js (for npx) OR a global install of @marp-team/marp-cli
#   - Chromium/Chrome available to Marp for PPTX/PDF export
#     (Marp will try to download one automatically on first run)
#
# Environment:
#   CHROME_PATH   Optional. Absolute path to a Chrome/Chromium binary, used by
#                 Marp when its bundled Chromium cannot be located. Example:
#                   export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
#                 then re-run `./deploy-pptx.sh --pdf`.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SLIDES_DIR="$SCRIPT_DIR"
DIST_DIR="$SCRIPT_DIR/dist"

BUILD_PDF=false
BUILD_HTML=false
CLEAN=false

for arg in "$@"; do
  case "$arg" in
    --all)   BUILD_PDF=true; BUILD_HTML=true ;;
    --pdf)   BUILD_PDF=true ;;
    --html)  BUILD_HTML=true ;;
    --clean) CLEAN=true ;;
    -h|--help)
      sed -n '2,21p' "$0"; exit 0 ;;
    *)
      echo "Unknown argument: $arg" >&2
      echo "Run '$0 --help' for usage." >&2
      exit 1 ;;
  esac
done

# Resolve a Marp CLI runner. The global 'marp' binary is known to break on
# Node 26 (require/ESM mismatch in bundled yargs), so we prefer 'npx' which
# pulls a self-consistent install. Set MARP_USE_GLOBAL=1 to force the global
# binary if you've verified it works in your environment.
if [[ "${MARP_USE_GLOBAL:-0}" == "1" ]] && command -v marp >/dev/null 2>&1; then
  MARP=(marp)
elif command -v npx >/dev/null 2>&1; then
  MARP=(npx --yes @marp-team/marp-cli@latest)
elif command -v marp >/dev/null 2>&1; then
  MARP=(marp)
else
  echo "Error: neither 'marp' nor 'npx' found in PATH." >&2
  echo "Install Node.js or run: npm i -g @marp-team/marp-cli" >&2
  exit 1
fi

if $CLEAN; then
  echo "Cleaning $DIST_DIR ..."
  rm -rf "$DIST_DIR"
fi

mkdir -p "$DIST_DIR/pptx"
$BUILD_PDF  && mkdir -p "$DIST_DIR/pdf"
$BUILD_HTML && mkdir -p "$DIST_DIR/html"

shopt -s nullglob

# Discover decks. Intermediate decks live flat in slides/; beginner decks live
# in slides/beginner/. List intermediate first (preserves existing build order),
# then append beginner decks in lexical order so beginner build artifacts land
# in dist/{pptx,pdf,html}/beginner/ subfolders and never collide with the
# intermediate set even if slugs were to coincide one day.
INTERMEDIATE_DECKS=("$SLIDES_DIR"/part-*.md)
BEGINNER_DECKS=()
if [ -d "$SLIDES_DIR/beginner" ]; then
  BEGINNER_DECKS=("$SLIDES_DIR"/beginner/part-*.md)
fi

DECKS=("${INTERMEDIATE_DECKS[@]}" ${BEGINNER_DECKS[@]+"${BEGINNER_DECKS[@]}"})
if [ ${#DECKS[@]} -eq 0 ]; then
  echo "No part-*.md decks found in $SLIDES_DIR (or $SLIDES_DIR/beginner/)" >&2
  exit 1
fi

# Optional list-only dry-run for tooling that needs to enumerate decks.
if [ "${LIST_DECKS:-0}" = "1" ]; then
  for deck in "${DECKS[@]}"; do echo "$deck"; done
  exit 0
fi

echo "Found ${#DECKS[@]} deck(s) (${#INTERMEDIATE_DECKS[@]} intermediate, ${#BEGINNER_DECKS[@]} beginner). Building ..."

# Map a deck path to its output subdirectory ("" for intermediate, "beginner" for beginner).
deck_subdir() {
  case "$1" in
    "$SLIDES_DIR"/beginner/*) echo "beginner" ;;
    *) echo "" ;;
  esac
}

for deck in "${DECKS[@]}"; do
  base="$(basename "${deck%.md}")"
  sub="$(deck_subdir "$deck")"
  out_pptx="$DIST_DIR/pptx${sub:+/$sub}"
  out_pdf="$DIST_DIR/pdf${sub:+/$sub}"
  out_html="$DIST_DIR/html${sub:+/$sub}"
  mkdir -p "$out_pptx"
  $BUILD_PDF  && mkdir -p "$out_pdf"
  $BUILD_HTML && mkdir -p "$out_html"

  echo
  echo "==> ${sub:+$sub/}$base"

  echo "    -> PPTX"
  "${MARP[@]}" --allow-local-files --pptx \
    -o "$out_pptx/${base}.pptx" "$deck"

  if $BUILD_PDF; then
    echo "    -> PDF"
    "${MARP[@]}" --allow-local-files --pdf \
      -o "$out_pdf/${base}.pdf" "$deck"
  fi

  if $BUILD_HTML; then
    echo "    -> HTML"
    "${MARP[@]}" --allow-local-files --html \
      -o "$out_html/${base}.html" "$deck"
  fi
done

echo
echo "Done. Output:"
echo "  PPTX:  $DIST_DIR/pptx/"
$BUILD_PDF  && echo "  PDF:   $DIST_DIR/pdf/"
$BUILD_HTML && echo "  HTML:  $DIST_DIR/html/"
