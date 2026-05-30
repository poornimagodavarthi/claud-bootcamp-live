#!/usr/bin/env bash
# Build the Claude Code Bootcamp workshop into a single Markdown ebook.
#
# Usage:
#   scripts/build-ebook.sh [--output PATH] [--no-solutions] [--manifest PATH]
#
# Options:
#   --output PATH    Output Markdown file.
#                    Default: book/dist/claude-code-bootcamp-ebook.md
#   --no-solutions   Exclude reference-solution appendices.
#   --manifest PATH  Manifest file. Default: scripts/ebook/manifest.json
#   -h, --help       Print this help and exit.
#
# Requirements: Python 3.11+ (standard library only).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

MANIFEST="$SCRIPT_DIR/ebook/manifest.json"
OUTPUT="$REPO_ROOT/book/dist/claude-code-bootcamp-ebook.md"
NO_SOLUTIONS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output)
      OUTPUT="$2"; shift 2 ;;
    --manifest)
      MANIFEST="$2"; shift 2 ;;
    --no-solutions)
      NO_SOLUTIONS=(--no-solutions); shift ;;
    -h|--help)
      sed -n '2,16p' "$0"; exit 0 ;;
    *)
      echo "build-ebook: unknown argument: $1" >&2; exit 2 ;;
  esac
done

mkdir -p "$(dirname "$OUTPUT")"

python3 "$SCRIPT_DIR/ebook/build_ebook.py" \
  --manifest "$MANIFEST" \
  --output "$OUTPUT" \
  ${NO_SOLUTIONS[@]+"${NO_SOLUTIONS[@]}"}
