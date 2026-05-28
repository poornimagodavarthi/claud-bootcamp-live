#!/usr/bin/env bash
#
# check-slide-overflow.sh — guard against canvas overflow in built HTML decks.
#
# Marp renders every slide into a fixed 1280x720 (16:9) <section>. If a slide's
# content is taller than the canvas, Marp clips it silently. This script makes
# that failure loud.
#
# Strategy: render each deck to HTML, then for each <section> count the number
# of headings, paragraphs, list items, table rows, and image tags. Any single
# section that exceeds a content budget gets reported.
#
# This is a structural canary, not a pixel-perfect overflow detector — but it
# catches the most common slip (someone adding a 25th bullet to a tpl-objectives
# slide that was already at the limit).
#
# Usage:
#   scripts/check-slide-overflow.sh                      # default: beginner @ budget 18
#   scripts/check-slide-overflow.sh --budget 22 <html-dir>
#   scripts/check-slide-overflow.sh <html-dir>           # explicit directory; budget defaults to 18
#   scripts/check-slide-overflow.sh part-01              # legacy filter on default beginner dir
#
# Exit 0 = all decks within budget.
# Exit 1 = at least one slide over budget (details printed).
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Default to beginner layout for backwards compatibility (feature 003 contract).
DIST_DIR="$REPO_ROOT/slides/dist/html"
BUDGET=18
filter=""

while [ $# -gt 0 ]; do
  case "$1" in
    --budget)
      BUDGET="$2"
      shift 2
      ;;
    --budget=*)
      BUDGET="${1#--budget=}"
      shift
      ;;
    -*)
      echo "Unknown flag: $1" >&2
      exit 2
      ;;
    *)
      if [ -d "$1" ]; then
        DIST_DIR="$1"
      else
        filter="$1"
      fi
      shift
      ;;
  esac
done

if [ ! -d "$DIST_DIR" ]; then
  echo "ERROR: $DIST_DIR not found. Run ./slides/deploy-pptx.sh --html first." >&2
  exit 2
fi

echo "Scanning: $DIST_DIR (budget=$BUDGET)"

shopt -s nullglob
fails=0
checked=0
for html in "$DIST_DIR"/*.html; do
  base="$(basename "${html%.html}")"
  if [ -n "$filter" ] && [[ "$base" != *"$filter"* ]]; then
    continue
  fi
  checked=$((checked + 1))

  # Split into one record per <section>, count content elements per record.
  # awk records are sections; for each section, count opening tags of
  # h1/h2/h3/h4/p/li/tr/img/pre (block-level visual elements).
  awk -v deck="$base" -v budget="$BUDGET" '
    BEGIN { RS = "<section"; slide = 0 }
    NR == 1 { next }   # discard <head>…<body> preamble
    {
      slide++
      n = 0
      n += gsub(/<h[1-4][ >]/, "&")
      n += gsub(/<p[ >]/, "&")
      n += gsub(/<li[ >]/, "&")
      n += gsub(/<tr[ >]/, "&")
      n += gsub(/<img /, "&")
      n += gsub(/<pre[ >]/, "&")
      if (n > budget) {
        printf "OVER: %s slide %d has %d content elements (budget %d)\n", deck, slide, n, budget
        over++
      }
    }
    END { exit (over > 0) ? 1 : 0 }
  ' "$html" || fails=$((fails + 1))
done

if [ "$checked" -eq 0 ]; then
  echo "No decks matched filter '$filter'." >&2
  exit 2
fi

if [ "$fails" -gt 0 ]; then
  echo
  echo "FAIL: $fails deck(s) have slides over the $BUDGET-element budget."
  exit 1
fi

echo "OK: $checked deck(s) checked, all slides within $BUDGET-element budget."
