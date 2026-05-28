#!/usr/bin/env bash
#
# check-verbatim-blocks.sh — Feature 004 verbatim & tighten-only audit.
#
# Enforces the FR-010 + Q2 + Q5 contract on the 10 intermediate decks:
#   * 5 protected categories per deck MUST be byte-identical to the baseline
#     (Promise list, Suggested CC prompt fences, Deliverable checklist,
#     Definition-of-done lines, Step-by-step lab steps).
#   * 5 editable sections per deck MUST have post-polish word count
#     <= pre-polish word count (tighten-only).
#   * Cross-deck invariants: theme decl, tpl-demo marker, SVG asset count,
#     duration sum = 240, beginner non-regression.
#
# Usage:
#   scripts/check-verbatim-blocks.sh [--baseline <git-ref>] [--quiet]
#
# Exit codes:
#   0  all pass
#   1  protected-block mismatch (verbatim violation)
#   2  editable-section delta > 0 (tighten-only violation)
#   3  cross-deck invariant failed
#   4  beginner-deck diff non-empty (FR-012)
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

BASELINE="$(cat specs/004-intermediate-content-polish/baseline-ref.txt 2>/dev/null || true)"
QUIET=0
while [ $# -gt 0 ]; do
  case "$1" in
    --baseline) BASELINE="$2"; shift 2 ;;
    --baseline=*) BASELINE="${1#--baseline=}"; shift ;;
    --quiet) QUIET=1; shift ;;
    -h|--help) sed -n '2,28p' "$0"; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 64 ;;
  esac
done
if [ -z "$BASELINE" ]; then
  BASELINE="$(git merge-base HEAD main 2>/dev/null || git rev-parse HEAD)"
fi

say() { [ "$QUIET" -eq 1 ] || echo "$@"; }

# 0. FR-012 beginner non-regression
beginner_diff="$(git diff --stat "$BASELINE" -- slides/beginner/ 2>/dev/null || true)"
if [ -n "$beginner_diff" ]; then
  echo "FAIL [FR-012]: beginner decks have diverged from baseline:" >&2
  echo "$beginner_diff" >&2
  exit 4
fi
say "PASS [FR-012] beginner decks byte-identical to baseline"

read_src() {
  case "$1" in
    GIT:*) git show "${1#GIT:}" 2>/dev/null || echo "" ;;
    *) cat "$1" ;;
  esac
}

extract_section() {
  read_src "$1" | awk -v anchor="$2" '
    BEGIN{ on=0 }
    /^## / {
      if (on) { exit }
      if ($0 ~ anchor) { on=1; next }
    }
    on { print }
  '
}

hash_block() {
  local src="$1" anchor="$2" filter="$3"
  extract_section "$src" "$anchor" | eval "$filter" | shasum -a 256 | awk '{print $1}'
}

wc_section() {
  # Word-count after stripping HTML comments and markdown image-embed lines.
  # Per Q4, the teaching-SVG embed (one per Concepts slide) is exempt from
  # the tighten-only word-count rule.
  extract_section "$1" "$2" \
    | perl -0777 -pe 's/<!--.*?-->//gs' \
    | grep -vE '^!\[' \
    | wc -w | tr -d ' '
}

PROTECTED_NAMES=("Promise" "Prompts" "Deliv" "DoD" "Steps")
PROTECTED_ANCHORS=("^## Promise" "^## Suggested Claude Code prompts" "^## Deliverable checklist" "^## Definition of done" "^## Step-by-step lab")
PROTECTED_FILTERS=(
  "cat"
  "awk 'BEGIN{f=0} /^\`\`\`text/{f=1;print;next} /^\`\`\`$/{if(f){print;f=0;next}} f{print}'"
  "grep -E '^- \\[ \\]' || true"
  "grep -E '^(- )?✅' || true"
  "grep -E '^[0-9]+\\.' || true"
)

EDITABLE_NAMES=("Why" "Concepts" "Mistakes" "Instr" "Trans")
EDITABLE_ANCHORS=("^## Why this matters" "^## Concepts" "^## Common mistakes" "^## Instructor notes" "^## Transition")

verbatim_violations=0
delta_violations=0

say ""
say "=== Per-deck verbatim audit (baseline=$BASELINE) ==="

say ""
say "Protected blocks (sha256 must match baseline):"
printf "%-40s | %-10s | %-10s | %-10s | %-10s | %-10s\n" "Deck" "${PROTECTED_NAMES[@]}"
for n in 01 02 03 04 05 06 07 08 09 10; do
  deck="$(ls slides/part-${n}-*.md 2>/dev/null | head -1)"
  [ -z "$deck" ] && continue
  row="$(basename "$deck")"
  cells=""
  for i in 0 1 2 3 4; do
    pre_hash="$(hash_block "GIT:${BASELINE}:${deck}" "${PROTECTED_ANCHORS[$i]}" "${PROTECTED_FILTERS[$i]}" 2>/dev/null || echo NA)"
    post_hash="$(hash_block "${deck}" "${PROTECTED_ANCHORS[$i]}" "${PROTECTED_FILTERS[$i]}" 2>/dev/null || echo NA)"
    if [ "$pre_hash" = "$post_hash" ]; then
      cells="${cells}OK         | "
    else
      cells="${cells}DIFF       | "
      verbatim_violations=$((verbatim_violations+1))
      [ "$QUIET" -eq 1 ] || echo "  [diff] ${row} ${PROTECTED_NAMES[$i]}: pre=$pre_hash post=$post_hash" >&2
    fi
  done
  printf "%-40s | %s\n" "$row" "$cells"
done

say ""
say "Editable sections (word-count delta must be <= 0):"
printf "%-40s | %6s | %6s | %6s | %6s | %6s\n" "Deck" "${EDITABLE_NAMES[@]}"
for n in 01 02 03 04 05 06 07 08 09 10; do
  deck="$(ls slides/part-${n}-*.md 2>/dev/null | head -1)"
  [ -z "$deck" ] && continue
  row="$(basename "$deck")"
  cells=""
  for i in 0 1 2 3 4; do
    pre_wc="$(wc_section "GIT:${BASELINE}:${deck}" "${EDITABLE_ANCHORS[$i]}" 2>/dev/null || echo 0)"
    post_wc="$(wc_section "${deck}" "${EDITABLE_ANCHORS[$i]}" 2>/dev/null || echo 0)"
    delta=$((post_wc - pre_wc))
    if [ "$delta" -gt 0 ]; then
      delta_violations=$((delta_violations+1))
      cells="$(printf "%s %+5d!" "$cells" "$delta")"
    else
      cells="$(printf "%s %+5d " "$cells" "$delta")"
    fi
  done
  printf "%-40s | %s\n" "$row" "$cells"
done

say ""
say "=== Cross-deck invariants ==="
set +e
inv_violations=0

missing_theme=$(grep -L '^theme: wow-beginner' slides/part-*.md 2>/dev/null || true)
if [ -n "$missing_theme" ]; then
  echo "FAIL [FR-002]: decks missing 'theme: wow-beginner':" >&2
  echo "$missing_theme" >&2
  inv_violations=$((inv_violations+1))
else
  say "PASS [FR-002] all 10 decks declare theme: wow-beginner"
fi

for n in 01 02 03 04 05 06 07 08 09 10; do
  deck="$(ls slides/part-${n}-*.md 2>/dev/null | head -1)"
  [ -z "$deck" ] && continue
  cnt=$(grep -c '<!-- _class: tpl-show -->' "$deck" 2>/dev/null || echo 0)
  if [ "$cnt" -lt 1 ]; then
    echo "FAIL [FR-003]: $(basename "$deck") has $cnt tpl-show markers (need >=1)" >&2
    inv_violations=$((inv_violations+1))
  fi
done

svg_count="$(ls slides/intermediate/assets/[0-1][0-9]-*.svg 2>/dev/null | wc -l | tr -d ' ')"
if [ "$svg_count" -ne 10 ]; then
  echo "WARN [FR-004]: expected 10 SVGs, found $svg_count" >&2
  inv_violations=$((inv_violations+1))
else
  say "PASS [FR-004] 10 teaching SVGs present"
fi

dur_sum="$(grep -h '<!-- duration:' slides/part-*.md 2>/dev/null | awk -F'[: ]+' '{s+=$3} END{print s+0}')"
if [ "$dur_sum" != "240" ]; then
  echo "FAIL [FR-011]: sum of declared durations = $dur_sum (need 240)" >&2
  inv_violations=$((inv_violations+1))
else
  say "PASS [FR-011] declared-duration sum = 240 min"
fi

say ""
say "=== Summary ==="
say "Verbatim mismatches: $verbatim_violations"
say "Word-count delta violations (positive): $delta_violations"
say "Cross-deck invariant violations: $inv_violations"

if [ "$verbatim_violations" -gt 0 ]; then exit 1; fi
if [ "$delta_violations" -gt 0 ]; then exit 2; fi

[ "$inv_violations" -gt 0 ] && exit 3
say "ALL GATES PASS"
exit 0
