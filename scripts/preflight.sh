#!/usr/bin/env bash
# scripts/preflight.sh — pre-cohort audit for the Claude Code Bootcamp.
#
# Composes 15 gates (14 block + 1 warn) against the repository.
# Returns:
#   0 = all block gates passed (warn gates may still have emitted warnings)
#   1 = one or more block gates failed
#   2 = tooling / setup error
#  64 = invalid invocation
#
# See specs/005-may-2026-bootcamp-refresh/contracts/preflight-audit.contract.md
# for the wire contract.

set -u
LC_ALL=C
export LC_ALL

REPO_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )" || { echo "preflight: cannot resolve repo root" >&2; exit 2; }
cd "$REPO_ROOT" || { echo "preflight: cannot cd into repo root" >&2; exit 2; }

# ---------------------------------------------------------------------------
# Flag parsing
# ---------------------------------------------------------------------------
QUICK=0
VERBOSE=0
ONLY_GATE=""

usage() {
  cat <<EOF
Usage: scripts/preflight.sh [--quick] [--verbose] [--gate <audit.name>]

  --quick           Skip slow gates (audit.slide-overflow)
  --verbose         Print per-gate trace
  --gate <name>     Run a single gate by name (e.g., audit.cross-links)

Exit codes:
  0   all block gates passed
  1   one or more block gates failed
  2   tooling / setup error
  64  invalid invocation
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --quick)   QUICK=1 ;;
    --verbose) VERBOSE=1 ;;
    --gate)    shift; ONLY_GATE="${1:-}"; [ -z "$ONLY_GATE" ] && { usage >&2; exit 64; } ;;
    -h|--help) usage; exit 0 ;;
    *) echo "preflight: unknown flag '$1'" >&2; usage >&2; exit 64 ;;
  esac
  shift
done

# ---------------------------------------------------------------------------
# Report header
# ---------------------------------------------------------------------------
BOOTCAMP_NAME="$( basename "$REPO_ROOT" )"
FEATURE="005"
NOW="$( date -u +%Y-%m-%dT%H:%M:%SZ )"
printf 'preflight  bootcamp=%s  feature=%s  %s\n\n' "$BOOTCAMP_NAME" "$FEATURE" "$NOW"

# Counters
FAIL_COUNT=0
WARN_COUNT=0
PASS_COUNT=0

# Indent helper for offender lines
indent() { sed 's/^/       /'; }

# Trace helper
trace() { [ "$VERBOSE" -eq 1 ] && printf '       (trace) %s\n' "$*"; }

# Generic gate runner: $1=name $2=severity(block|warn) $3=function
run_gate() {
  local name="$1" sev="$2" fn="$3"
  if [ -n "$ONLY_GATE" ] && [ "$ONLY_GATE" != "$name" ]; then
    return 0
  fi
  local out rc
  out="$( "$fn" 2>&1 )"
  rc=$?
  if [ "$rc" -eq 0 ]; then
    # Function printed its own PASS / WARN line + details (if any)
    printf '%s\n' "$out"
    if printf '%s' "$out" | grep -q '^\[WARN\]'; then
      WARN_COUNT=$(( WARN_COUNT + 1 ))
    else
      PASS_COUNT=$(( PASS_COUNT + 1 ))
    fi
  else
    printf '%s\n' "$out"
    if [ "$sev" = "warn" ]; then
      WARN_COUNT=$(( WARN_COUNT + 1 ))
    else
      FAIL_COUNT=$(( FAIL_COUNT + 1 ))
    fi
  fi
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# List the part-NN-*.md decks (01..10 by default; pass --all to include part-11)
list_decks() {
  local mode="${1:-core}"  # core|all
  local f
  if [ "$mode" = "all" ]; then
    for f in slides/part-*.md; do [ -f "$f" ] && echo "$f"; done
  else
    for n in 01 02 03 04 05 06 07 08 09 10; do
      local g
      for g in slides/part-"$n"-*.md; do [ -f "$g" ] && echo "$g"; done
    done
  fi
}

# 13 canonical H2 sections for a deck (the H1 title is mandatory but not an H2).
DECK_SECTIONS="Promise|Why this matters|Concepts|Live demo flow|Mini project|Step-by-step lab|Suggested Claude Code prompts|Deliverable checklist|Definition of done|Review checkpoint|Common mistakes|Instructor notes|Transition"

# 9 canonical H2 sections for an exercise.
EXERCISE_SECTIONS="Goal|Scenario|Starter instructions|Claude Code prompt to use|Manual validation steps|Expected deliverable|Definition of done|Stretch challenge|Troubleshooting"

# 6 canonical SKILL.md H2 sections.
SKILL_SECTIONS="Purpose|When to use|Body|Inputs|Outputs|Worked example"

# Has H2 (case-insensitive substring match against the deck heading text)?
deck_has_section() {
  local file="$1" section="$2"
  # Match "## <section>" tolerating trailing extras (icons, modifiers)
  grep -Ei "^## .*${section}" "$file" >/dev/null 2>&1
}

# Get all markdown files in scope for cross-link / clarifications gates
scope_files() {
  # Excludes .git, node_modules, build artefacts, archive (allowed to point inward),
  # and specs/ (maintainer-only Spec Kit docs containing template placeholders).
  find . -type f -name '*.md' \
    -not -path './.git/*' \
    -not -path './node_modules/*' \
    -not -path './slides/dist/*' \
    -not -path './archive/*' \
    -not -path './specs/*' \
    2>/dev/null
}

# ---------------------------------------------------------------------------
# GATE 1: audit.module-bundle   (block)
# ---------------------------------------------------------------------------
gate_module_bundle() {
  local missing="" n deck readme sol
  for n in 01 02 03 04 05 06 07 08 09 10; do
    deck=$( ls slides/part-"$n"-*.md 2>/dev/null | head -n1 )
    readme="exercises/part-$n/README.md"
    sol="exercises/part-$n/solution"
    [ -z "$deck" ] && missing="${missing}module-$n: missing slide deck slides/part-$n-*.md\n"
    [ -f "$readme" ] || missing="${missing}module-$n: missing $readme\n"
    [ -d "$sol" ] || missing="${missing}module-$n: missing $sol/\n"
  done
  # Part 11 deck-only check
  [ -f "$( ls slides/part-11-*.md 2>/dev/null | head -n1 )" ] 2>/dev/null || \
    missing="${missing}module-11: missing slide deck slides/part-11-*.md\n"

  if [ -z "$missing" ]; then
    echo "[PASS] audit.module-bundle         (10 modules + Part 11 closing block all bundled)"
    return 0
  else
    echo "[FAIL] audit.module-bundle"
    printf '%b' "$missing" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 2: audit.slide-anatomy   (block)
# ---------------------------------------------------------------------------
gate_slide_anatomy() {
  local fails="" deck section
  while IFS='|' read -r section; do :; done < /dev/null  # noop to prove pipe support
  for deck in $( list_decks all ); do
    local IFS='|'
    for section in $DECK_SECTIONS; do
      if ! deck_has_section "$deck" "$section"; then
        fails="${fails}${deck}: missing section \"${section}\"\n"
      fi
    done
    unset IFS
  done
  if [ -z "$fails" ]; then
    local count
    count=$( list_decks all | wc -l | tr -d ' ' )
    echo "[PASS] audit.slide-anatomy         ($count decks \u00d7 13 required H2 sections present (+ H1 title))"
    return 0
  else
    echo "[FAIL] audit.slide-anatomy"
    printf '%b' "$fails" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 3: audit.slide-theme   (block)
# ---------------------------------------------------------------------------
gate_slide_theme() {
  local fails="" deck
  for deck in $( list_decks all ); do
    if ! awk '/^---$/{c++;next} c==1 && /^theme:[[:space:]]*wow-beginner[[:space:]]*$/ {found=1} END{exit !found}' "$deck"; then
      fails="${fails}${deck}: frontmatter does not set 'theme: wow-beginner'\n"
    fi
  done
  if [ -z "$fails" ]; then
    echo "[PASS] audit.slide-theme           (theme=wow-beginner on every deck)"
    return 0
  else
    echo "[FAIL] audit.slide-theme"
    printf '%b' "$fails" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 4: audit.slide-overflow   (block, slow)
# ---------------------------------------------------------------------------
gate_slide_overflow() {
  if [ "$QUICK" -eq 1 ]; then
    echo "[PASS] audit.slide-overflow        (skipped by --quick)"
    return 0
  fi
  if [ ! -x scripts/check-slide-overflow.sh ]; then
    echo "[FAIL] audit.slide-overflow"
    echo "       scripts/check-slide-overflow.sh missing or not executable" | indent
    return 1
  fi
  if [ ! -d slides/dist/html ]; then
    echo "[WARN] audit.slide-overflow        slides/dist/html not built; run slides/deploy-pptx.sh --all first"
    return 0
  fi
  local out rc
  out=$( bash scripts/check-slide-overflow.sh --budget 22 slides/dist/html 2>&1 )
  rc=$?
  if [ $rc -eq 0 ]; then
    echo "[PASS] audit.slide-overflow        (budget=22 lines/slide; all decks within limit)"
    return 0
  else
    echo "[FAIL] audit.slide-overflow"
    printf '%s\n' "$out" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 5: audit.duration-sum   (block, threshold 240 +/- 5)
# ---------------------------------------------------------------------------
gate_duration_sum() {
  local sum=0 deck n missing=""
  for n in 01 02 03 04 05 06 07 08 09 10; do
    deck=$( ls slides/part-"$n"-*.md 2>/dev/null | head -n1 )
    if [ -z "$deck" ]; then
      missing="${missing}module-$n: deck not found\n"; continue
    fi
    local m
    m=$( grep -Eo '<!--[[:space:]]*duration:[[:space:]]*[0-9]+[[:space:]]*min[[:space:]]*-->' "$deck" | head -n1 | grep -Eo '[0-9]+' | head -n1 )
    if [ -z "$m" ]; then
      missing="${missing}${deck}: no '<!-- duration: NN min -->' marker\n"; continue
    fi
    sum=$(( sum + m ))
  done
  if [ -n "$missing" ]; then
    echo "[FAIL] audit.duration-sum          sum=incomplete"
    printf '%b' "$missing" | indent
    return 1
  fi
  if [ "$sum" -ge 235 ] && [ "$sum" -le 245 ]; then
    echo "[PASS] audit.duration-sum          sum=${sum} min (target 240 \u00b1 5)"
    return 0
  else
    echo "[FAIL] audit.duration-sum          sum=${sum} expected 240 \u00b1 5"
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 6: audit.exercise-anatomy   (block)
# ---------------------------------------------------------------------------
gate_exercise_anatomy() {
  local fails="" n readme section
  for n in 01 02 03 04 05 06 07 08 09 10; do
    readme="exercises/part-$n/README.md"
    [ -f "$readme" ] || { fails="${fails}${readme}: missing\n"; continue; }
    local IFS='|'
    for section in $EXERCISE_SECTIONS; do
      if ! grep -Ei "^## .*${section}" "$readme" >/dev/null 2>&1; then
        fails="${fails}${readme}: missing section \"${section}\"\n"
      fi
    done
    unset IFS
  done
  if [ -z "$fails" ]; then
    echo "[PASS] audit.exercise-anatomy      (10 exercises \u00d7 9 required sections present)"
    return 0
  else
    echo "[FAIL] audit.exercise-anatomy"
    printf '%b' "$fails" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 7: audit.solution-presence   (block)
# ---------------------------------------------------------------------------
gate_solution_presence() {
  local fails="" n sol
  for n in 01 02 03 04 05 06 07 08 09 10; do
    sol="exercises/part-$n/solution"
    if [ ! -d "$sol" ]; then
      fails="${fails}${sol}: directory missing\n"; continue
    fi
    if ! ls "$sol"/README.md "$sol"/run.sh "$sol"/solution.* 2>/dev/null | head -n1 | grep -q .; then
      fails="${fails}${sol}: empty or missing entry point (README.md / run.sh / solution.*)\n"
    fi
  done
  if [ -z "$fails" ]; then
    echo "[PASS] audit.solution-presence     (10 solutions have entry points)"
    return 0
  else
    echo "[FAIL] audit.solution-presence"
    printf '%b' "$fails" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 8: audit.skill-contract   (block)
# ---------------------------------------------------------------------------
EXPECTED_SKILLS="best-of-n claude-md-template code-review documentation-generation git-workflow production-readiness-review refactor release-notes security-checklist test-generation release-readiness mcp-context-brief"

gate_skill_contract() {
  local OLD_IFS="$IFS"
  IFS=$' \t\n'
  local fails="" slug skill_file section
  # 1. Expected slugs present
  for slug in $EXPECTED_SKILLS; do
    skill_file="skills/$slug/SKILL.md"
    if [ ! -f "$skill_file" ]; then
      fails="${fails}skills/${slug}: missing SKILL.md\n"
    fi
  done
  # 2. No unexpected skill dirs (skip non-dirs like LICENSE/README.md)
  local entry name found
  for entry in skills/*/; do
    [ -d "$entry" ] || continue
    name=$( basename "$entry" )
    found=0
    for slug in $EXPECTED_SKILLS; do
      [ "$slug" = "$name" ] && { found=1; break; }
    done
    [ "$found" -eq 0 ] && fails="${fails}skills/${name}: unexpected skill directory (not in catalogue)\n"
  done
  # 3. Per-file checks: frontmatter name/description, 6 H2 sections, no module-NN paths
  for slug in $EXPECTED_SKILLS; do
    skill_file="skills/$slug/SKILL.md"
    [ -f "$skill_file" ] || continue
    grep -Eq "^name:[[:space:]]*${slug}[[:space:]]*$" "$skill_file" || \
      fails="${fails}${skill_file}: frontmatter 'name' missing or != '${slug}'\n"
    grep -Eq "^description:[[:space:]]*\S" "$skill_file" || \
      fails="${fails}${skill_file}: frontmatter 'description' missing or empty\n"
    local IFS='|'
    for section in $SKILL_SECTIONS; do
      if ! grep -Eq "^## .*${section}" "$skill_file"; then
        fails="${fails}${skill_file}: missing section \"${section}\"\n"
      fi
    done
    unset IFS
    if grep -Eq 'module-[0-9][0-9]/|exercises/part-[0-9][0-9]|slides/part-[0-9][0-9]' "$skill_file"; then
      fails="${fails}${skill_file}: contains module-specific paths (skill must be project-agnostic)\n"
    fi
  done
  if [ -z "$fails" ]; then
    IFS="$OLD_IFS"
    echo "[PASS] audit.skill-contract        (12 skills present, contract honoured)"
    return 0
  else
    IFS="$OLD_IFS"
    echo "[FAIL] audit.skill-contract"
    printf '%b' "$fails" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 9: audit.assessment-coverage   (block)
# ---------------------------------------------------------------------------
gate_assessment_coverage() {
  local OLD_IFS="$IFS"
  IFS=$' \t\n'
  local fails="" f
  for f in knowledge-quiz practical-task code-review-reflection rubric answer-key; do
    [ -f "assessments/${f}.md" ] || fails="${fails}assessments/${f}.md: missing\n"
  done
  if [ -f assessments/rubric.md ]; then
    local n
    for n in 01 02 03 04 05 06 07 08 09 10; do
      # Accept either "part-NN", "module NN", "Module NN", or "Part NN"
      if ! grep -Eiq "(part-${n}|module[[:space:]]+${n#0}|module[[:space:]]+${n}|part[[:space:]]+${n#0}|part[[:space:]]+${n})" assessments/rubric.md; then
        fails="${fails}assessments/rubric.md: no reference to module ${n}\n"
      fi
    done
  fi
  local topic file_scan
  file_scan="assessments/knowledge-quiz.md assessments/practical-task.md assessments/rubric.md assessments/code-review-reflection.md"
  for topic in "skill" "MCP" "hook" "GitHub Action" "multi-agent"; do
    if ! grep -Eiq "$topic" $file_scan 2>/dev/null; then
      fails="${fails}assessments/: no item mentions '${topic}'\n"
    fi
  done
  if [ -z "$fails" ]; then
    echo "[PASS] audit.assessment-coverage   (5 files; rubric maps 01–10; May-2026 topics covered)"
    IFS="$OLD_IFS"
    return 0
  else
    echo "[FAIL] audit.assessment-coverage"
    printf '%b' "$fails" | indent
    IFS="$OLD_IFS"
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 10: audit.cross-links   (block)
# ---------------------------------------------------------------------------
gate_cross_links() {
  local file
  : > /tmp/preflight.cross-links.$$
  scope_files | while IFS= read -r file; do
    [ -f "$file" ] || continue
    awk -v f="$file" '
      {
        line = $0
        lno = NR
        while (1) {
          p = index(line, "](")
          if (p == 0) break
          tail = substr(line, p + 2)
          q = index(tail, ")")
          if (q == 0) break
          link = substr(tail, 1, q - 1)
          sub(/#.*/, "", link)
          if (link != "" \
              && link !~ /^https?:\/\// \
              && link !~ /^mailto:/ \
              && link !~ /^[a-zA-Z][a-zA-Z0-9+.-]*:/ ) {
            print lno "|" link
          }
          line = substr(tail, q + 1)
        }
      }
    ' "$file" 2>/dev/null | while IFS='|' read -r lineno link; do
      local dir target
      dir=$( dirname "$file" )
      case "$link" in
        /*) target=".$link" ;;
        *)  target="$dir/$link" ;;
      esac
      target="${target%/}"
      if [ ! -e "$target" ] && [ ! -e "${target}/" ]; then
        printf '%s:%s -> %s  (unresolved)\n' "$file" "$lineno" "$link" >> /tmp/preflight.cross-links.$$
      fi
    done
  done
  if [ ! -s /tmp/preflight.cross-links.$$ ]; then
    rm -f /tmp/preflight.cross-links.$$
    echo "[PASS] audit.cross-links           (all intra-repo markdown links resolve)"
    return 0
  else
    echo "[FAIL] audit.cross-links"
    indent < /tmp/preflight.cross-links.$$
    rm -f /tmp/preflight.cross-links.$$
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 11: audit.bundle-coverage   (block)
# ---------------------------------------------------------------------------
gate_bundle_coverage() {
  local fails="" topic re
  for topic in "skill" "MCP" "hook" "GitHub Action" "multi-agent"; do
    re=$( printf '%s' "$topic" | sed 's/[][\\/.*^$]/\\&/g' )
    if ! grep -RIliE "$re" slides/part-*.md >/dev/null 2>&1; then
      fails="${fails}${topic}: no occurrence in slides/part-*.md\n"
    fi
    if ! grep -RIliE "$re" exercises/part-*/README.md >/dev/null 2>&1; then
      fails="${fails}${topic}: no occurrence in exercises/part-*/README.md\n"
    fi
  done
  if [ -z "$fails" ]; then
    echo "[PASS] audit.bundle-coverage       (Skills \u00b7 MCP \u00b7 Hooks \u00b7 GitHub Actions \u00b7 Multi-agent all in slides AND exercises)"
    return 0
  else
    echo "[FAIL] audit.bundle-coverage"
    printf '%b' "$fails" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 12: audit.no-clarifications-in-published   (block)
# ---------------------------------------------------------------------------
gate_no_clarifications() {
  local fails="" hits
  # Real Spec-Kit clarification markers have the form '[NEEDS CLARIFICATION: ...]'.
  # The colon distinguishes a real marker from documentation that just says '[NEEDS CLARIFICATION]'.
  # Scope: student-facing published surfaces only. The instructor-guide is the
  # audit's meta-documentation and is expected to mention the marker literally.
  hits=$( grep -rEn '\[NEEDS CLARIFICATION:|^TODO\b' \
            README.md student-guide.md \
            slides/part-*.md exercises/part-*/README.md skills/*/SKILL.md 2>/dev/null )
  if [ -z "$hits" ]; then
    echo "[PASS] audit.no-clarifications-in-published  (no NEEDS CLARIFICATION / leading TODO in published surfaces)"
    return 0
  else
    echo "[FAIL] audit.no-clarifications-in-published"
    printf '%s\n' "$hits" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 13: audit.archive-isolation   (block)
# ---------------------------------------------------------------------------
gate_archive_isolation() {
  [ -d archive ] || { echo "[PASS] audit.archive-isolation     (no archive/ directory)"; return 0; }
  local hits f line link allowed_heading allowed_block fails=""
  allowed_heading="## Optional pre-bootcamp warm-up (archived)"

  for f in README.md student-guide.md instructor-guide.md slides/part-*.md exercises/part-*/README.md skills/*/SKILL.md; do
    [ -f "$f" ] || continue
    # Find any markdown link whose target hits archive/
    while IFS=: read -r line content; do
      [ -z "$line" ] && continue
      # Only allow if file == README.md AND the line is inside the allowed section
      if [ "$f" = "README.md" ]; then
        # Determine the most recent H2 heading at or above $line
        nearest=$( awk -v target="$line" 'NR<=target && /^## / {h=$0} END{print h}' "$f" )
        if [ "$nearest" = "$allowed_heading" ]; then
          continue
        fi
      fi
      fails="${fails}${f}:${line}: links into archive/  ('${content#*]}')\n"
    done < <( grep -nE '\]\(\.?\.?/?archive/' "$f" 2>/dev/null )
  done
  if [ -z "$fails" ]; then
    echo "[PASS] audit.archive-isolation     (only README's 'Optional pre-bootcamp warm-up (archived)' links into archive/)"
    return 0
  else
    echo "[FAIL] audit.archive-isolation"
    printf '%b' "$fails" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# GATE 14: audit.dist-freshness   (warn)
# ---------------------------------------------------------------------------
gate_dist_freshness() {
  [ -d slides/dist/pdf ] || { echo "[WARN] audit.dist-freshness        slides/dist/pdf missing; run slides/deploy-pptx.sh --all"; return 0; }
  local stale="" deck pdf base
  for deck in slides/part-*.md; do
    [ -f "$deck" ] || continue
    base=$( basename "$deck" .md )
    pdf="slides/dist/pdf/${base}.pdf"
    if [ ! -f "$pdf" ]; then
      stale="${stale}${pdf}: missing PDF\n"
      continue
    fi
    # Source newer than PDF?
    if [ "$deck" -nt "$pdf" ]; then
      stale="${stale}${deck}: source newer than $pdf  (rebuild before delivery)\n"
    fi
  done
  if [ -z "$stale" ]; then
    echo "[PASS] audit.dist-freshness        (all PDFs up-to-date with sources)"
    return 0
  else
    echo "[WARN] audit.dist-freshness"
    printf '%b' "$stale" | indent
    return 0
  fi
}

# ---------------------------------------------------------------------------
# GATE 15: audit.contrast   (block)
# ---------------------------------------------------------------------------
gate_contrast() {
  if [ ! -x scripts/check-contrast.sh ]; then
    echo "[WARN] audit.contrast              scripts/check-contrast.sh not executable"
    return 0
  fi
  local out rc
  out=$( bash scripts/check-contrast.sh 2>&1 )
  rc=$?
  if [ $rc -eq 0 ]; then
    echo "[PASS] audit.contrast              (WCAG-AA contrast checks passed)"
    return 0
  else
    echo "[FAIL] audit.contrast"
    printf '%s\n' "$out" | indent
    return 1
  fi
}

# ---------------------------------------------------------------------------
# Gate registry & dispatch
# ---------------------------------------------------------------------------
# name|severity|function
GATES="
audit.module-bundle|block|gate_module_bundle
audit.slide-anatomy|block|gate_slide_anatomy
audit.slide-theme|block|gate_slide_theme
audit.slide-overflow|block|gate_slide_overflow
audit.duration-sum|block|gate_duration_sum
audit.exercise-anatomy|block|gate_exercise_anatomy
audit.solution-presence|block|gate_solution_presence
audit.skill-contract|block|gate_skill_contract
audit.assessment-coverage|block|gate_assessment_coverage
audit.cross-links|block|gate_cross_links
audit.bundle-coverage|block|gate_bundle_coverage
audit.no-clarifications-in-published|block|gate_no_clarifications
audit.archive-isolation|block|gate_archive_isolation
audit.dist-freshness|warn|gate_dist_freshness
audit.contrast|block|gate_contrast
"

# Validate --gate exists if specified
if [ -n "$ONLY_GATE" ]; then
  if ! printf '%s\n' "$GATES" | awk -F'|' -v g="$ONLY_GATE" '$1==g {found=1} END{exit !found}'; then
    echo "preflight: unknown gate '$ONLY_GATE'" >&2
    exit 64
  fi
fi

# Iterate without a pipe so counters in run_gate survive.
SAVED_IFS="$IFS"
IFS='
'
for line in $GATES; do
  IFS='|' read -r name sev fn <<EOF
$line
EOF
  [ -n "$name" ] || continue
  run_gate "$name" "$sev" "$fn"
done
IFS="$SAVED_IFS"

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
printf '\nResult: %d PASS, %d FAIL, %d WARN.\n' "$PASS_COUNT" "$FAIL_COUNT" "$WARN_COUNT"
if [ "$FAIL_COUNT" -gt 0 ]; then
  printf 'RC=1 (block gates failed)\n'
  exit 1
fi
printf 'RC=0 (safe to deliver)\n'
exit 0
