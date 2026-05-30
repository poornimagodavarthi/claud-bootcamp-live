#!/usr/bin/env bash
# Build the Leanpub (Markua) manuscript from the workshop sources.
#
# Usage: scripts/build-leanpub.sh [--no-solutions] [--output DIR]
#
# Output: book/leanpub/manuscript/ (Book.txt, Sample.txt, per-chapter files,
# resources/). Point a Leanpub book's GitHub/Dropbox sync at that folder.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec python3 "$SCRIPT_DIR/ebook/build_leanpub.py" "$@"
