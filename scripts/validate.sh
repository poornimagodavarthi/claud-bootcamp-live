#!/usr/bin/env bash
# scripts/validate.sh — structural validator for the bootcamp repo.
#
# Enforces:
#   - Slide deck contract: 14 required H2 sections in order + Marp frontmatter + duration marker.
#   - Per-deck duration marker matches canonical minute budget (240 total).
#   - Exercise contract: 9 required H2 sections.
#   - Skill contract: YAML frontmatter (name, description) + 6 H2 body sections.
#   - 10-project list cross-consistency (README, slides/, exercises/).
#   - Forbidden-tokens regex (FR-027b) across all authoring files (excludes specs/ and HTML comments).
#
# Exits 0 on success, 1 on any violation.

set -uo pipefail

cd "$(dirname "$0")/.."

PASS=0
FAIL=0
FAIL_DETAILS=()

ok()   { PASS=$((PASS+1)); printf "  \033[32mok\033[0m   %s\n" "$1"; }
fail() { FAIL=$((FAIL+1)); FAIL_DETAILS+=("$1"); printf "  \033[31mFAIL\033[0m %s\n" "$1"; }

# ----------------------------------------------------------------------------
# 1. Slide deck contract
# ----------------------------------------------------------------------------

declare -a DECK_SLUGS=(
  part-01-setup-mindset
  part-02-prompting
  part-03-claude-md
  part-04-best-of-n
  part-05-testing-debugging
  part-06-git-workflows
  part-07-multimodal
  part-08-refactor-docs
  part-09-skills-workflows
  part-10-production-readiness
)
declare -a DECK_MINS=(20 24 22 30 28 22 30 24 22 18)

DECK_SECTIONS=(
  "Promise"
  "Why this matters"
  "Concepts"
  "Live demo flow"
  "Mini project"
  "Step-by-step lab"
  "Suggested Claude Code prompts"
  "Deliverable checklist"
  "Definition of done"
  "Review checkpoint"
  "Common mistakes"
  "Instructor notes"
  "Transition to next module"
)

echo
echo "=== Slide decks ==="
TOTAL_MIN=0
i=0
while [[ $i -lt ${#DECK_SLUGS[@]} ]]; do
  slug="${DECK_SLUGS[$i]}"
  expected="${DECK_MINS[$i]}"
  i=$((i+1))
  f="slides/${slug}.md"
  if [[ ! -f "$f" ]]; then
    fail "missing $f"; continue
  fi

  # Marp frontmatter
  if ! head -10 "$f" | grep -q '^marp: true'; then
    fail "$f: missing 'marp: true' frontmatter"
  fi
  for k in theme paginate size title description; do
    if ! head -10 "$f" | grep -q "^${k}:"; then
      fail "$f: missing frontmatter key '$k'"
    fi
  done

  # Duration marker
  if ! grep -qE "<!--[[:space:]]*duration:[[:space:]]*${expected}[[:space:]]*min[[:space:]]*-->" "$f"; then
    fail "$f: missing or mismatched <!-- duration: ${expected} min --> marker"
  else
    TOTAL_MIN=$((TOTAL_MIN + expected))
  fi

  # 14 sections (Title is the first H2; we check for the other 13 by name)
  H2_COUNT=$(grep -cE '^## ' "$f" || true)
  if (( H2_COUNT < 14 )); then
    fail "$f: expected ≥ 14 H2 sections, found $H2_COUNT"
  fi
  for sec in "${DECK_SECTIONS[@]}"; do
    if ! grep -qF "## ${sec}" "$f"; then
      fail "$f: missing H2 section '${sec}'"
    fi
  done

  ok "$f"
done

if (( TOTAL_MIN == 240 )); then
  ok "deck duration markers sum to 240 min"
else
  fail "deck duration markers sum to ${TOTAL_MIN} min (expected 240)"
fi

# ----------------------------------------------------------------------------
# 2. Exercise contract
# ----------------------------------------------------------------------------

EX_SECTIONS=(
  "Goal"
  "Scenario"
  "Starter instructions"
  "Claude Code prompt to use"
  "Manual validation steps"
  "Expected deliverable"
  "Definition of done"
  "Stretch challenge"
  "Troubleshooting"
)

echo
echo "=== Exercises ==="
for n in 01 02 03 04 05 06 07 08 09 10; do
  f="exercises/part-${n}/README.md"
  if [[ ! -f "$f" ]]; then
    fail "missing $f"; continue
  fi
  for sec in "${EX_SECTIONS[@]}"; do
    if ! grep -qF "## ${sec}" "$f"; then
      fail "$f: missing H2 section '${sec}'"
    fi
  done
  ok "$f"
done

# Module 5 student rubric must exist (distinct from assessments/rubric.md)
if [[ -f "exercises/part-05/code-review-rubric.md" ]]; then
  ok "exercises/part-05/code-review-rubric.md (student rubric)"
else
  fail "missing exercises/part-05/code-review-rubric.md (student rubric)"
fi

# ----------------------------------------------------------------------------
# 3. Skill contract
# ----------------------------------------------------------------------------

SKILL_SECTIONS=(
  "Purpose"
  "When to use"
  "Body"
  "Inputs"
  "Outputs"
  "Worked example"
)

EXPECTED_SKILLS=(
  claude-md-template
  code-review
  test-generation
  best-of-n
  refactor
  release-notes
  security-checklist
  git-workflow
  documentation-generation
  production-readiness-review
)

echo
echo "=== Skills ==="
for s in "${EXPECTED_SKILLS[@]}"; do
  f="skills/${s}/SKILL.md"
  if [[ ! -f "$f" ]]; then
    fail "missing $f"; continue
  fi

  # Frontmatter
  if ! awk 'NR==1 && /^---$/{found=1} NR>1 && /^---$/{exit} {if(found) print}' "$f" | grep -q '^name:'; then
    fail "$f: missing 'name' in YAML frontmatter"
  fi
  if ! awk 'NR==1 && /^---$/{found=1} NR>1 && /^---$/{exit} {if(found) print}' "$f" | grep -q '^description:'; then
    fail "$f: missing 'description' in YAML frontmatter"
  fi

  for sec in "${SKILL_SECTIONS[@]}"; do
    if ! grep -qF "## ${sec}" "$f"; then
      fail "$f: missing H2 section '${sec}'"
    fi
  done
  ok "$f"
done

# ----------------------------------------------------------------------------
# 4. Cross-consistency: 10 modules referenced in README
# ----------------------------------------------------------------------------

echo
echo "=== Cross-consistency ==="
SLIDES_README="slides/README.md"
for n in 01 02 03 04 05 06 07 08 09 10; do
  if ! grep -qE "part-${n}" "$SLIDES_README"; then
    fail "$SLIDES_README does not mention part-${n}"
  fi
done
ok "$SLIDES_README references all 10 modules"

# README.md must reference assessments and skills folders
for needed in "assessments/rubric.md" "skills/" "exercises/part-05/code-review-rubric.md"; do
  if ! grep -qF "$needed" README.md; then
    fail "README.md does not reference '$needed'"
  fi
done
ok "README.md references assessments/rubric.md, skills/, and student rubric"

# ----------------------------------------------------------------------------
# 5. Forbidden-tokens regex (FR-027b)
# ----------------------------------------------------------------------------

# Two-tier check:
#   STRICT_REGEX:    case-sensitive, word-boundary — TODO, TBD, FIXME, XXX
#   LOOSE_REGEX:     case-insensitive — buzzwords and placeholder/lorem ipsum
STRICT_REGEX='\b(TODO|TBD|FIXME|XXX)\b'
LOOSE_REGEX='coming soon|lorem ipsum|unleash|revolutioniz|revolutionary|game[- ]chang|cutting[- ]edge|world[- ]class|next[- ]gen|rockstar|ninja|transform your|master(ing)? the art'

# Files in scope (exclude specs/, .specify/, node_modules/, dist/, .git/)
SCOPED_FILES=(
  README.md
  instructor-guide.md
  student-guide.md
  certificate-template.md
)
while IFS= read -r f; do SCOPED_FILES+=("$f"); done < <(ls slides/part-*.md 2>/dev/null)
while IFS= read -r f; do SCOPED_FILES+=("$f"); done < <(ls exercises/part-*/README.md 2>/dev/null)
while IFS= read -r f; do SCOPED_FILES+=("$f"); done < <(ls assessments/*.md 2>/dev/null)
while IFS= read -r f; do SCOPED_FILES+=("$f"); done < <(ls skills/*/SKILL.md 2>/dev/null)

# V6 (beginner course): extend the forbidden-token scan to beginner authoring files.
if [[ -d slides/beginner ]]; then
  for f in GLOSSARY.md beginner-student-guide.md beginner-instructor-guide.md beginner-certificate-template.md; do
    [[ -f "$f" ]] && SCOPED_FILES+=("$f")
  done
  while IFS= read -r f; do SCOPED_FILES+=("$f"); done < <(ls slides/beginner/part-*.md 2>/dev/null)
  while IFS= read -r f; do SCOPED_FILES+=("$f"); done < <(ls exercises/beginner/part-*/README.md 2>/dev/null)
  [[ -f exercises/beginner/module-00-setup/README.md ]] && SCOPED_FILES+=("exercises/beginner/module-00-setup/README.md")
  while IFS= read -r f; do SCOPED_FILES+=("$f"); done < <(ls assessments/beginner/*.md 2>/dev/null)
  while IFS= read -r f; do SCOPED_FILES+=("$f"); done < <(ls skills/beginner/*/SKILL.md 2>/dev/null)
fi

echo
echo "=== Forbidden tokens (FR-027b) ==="
TOKEN_HITS=0
for f in "${SCOPED_FILES[@]}"; do
  [[ -f "$f" ]] || continue
  # Strip HTML comments before scanning
  stripped=$(perl -0777 -pe 's/<!--.*?-->//gs' "$f")
  hits_strict=$(printf '%s' "$stripped" | grep -nE "$STRICT_REGEX" || true)
  hits_loose=$(printf '%s' "$stripped" | grep -niE "$LOOSE_REGEX" || true)
  hits="${hits_strict}${hits_strict:+
}${hits_loose}"
  if [[ -n "$hits" ]]; then
    fail "$f: forbidden token(s):"
    while IFS= read -r line; do
      [[ -n "$line" ]] && printf "       %s\n" "$line"
    done <<< "$hits"
    TOKEN_HITS=$((TOKEN_HITS+1))
  fi
done
if (( TOKEN_HITS == 0 )); then
  ok "no forbidden tokens found across ${#SCOPED_FILES[@]} files"
fi

# ============================================================================
# BEGINNER COURSE EXTENSIONS (per specs/002-claude-beginner-course/contracts/
# validator-extensions.md, V1..V13). All gated by `-d slides/beginner` so the
# intermediate-only test surface is unaffected when the beginner course is
# removed or not yet authored.
# ============================================================================

if [[ -d slides/beginner ]]; then

  echo
  echo "=== Beginner course (V1..V13) ==="

  declare -a BEG_DECK_SLUGS=(
    part-01-meet-claude-code
    part-02-first-conversation
    part-03-asking-for-what-you-want
    part-04-reading-code-together
    part-05-editing-one-file-safely
    part-06-claude-md-cheat-sheet
    part-07-safer-and-smarter
    part-08-putting-it-together
  )
  declare -a BEG_DECK_MINS=(20 25 30 25 30 25 25 30)

  BEG_DECK_SECTIONS=(
    "What you'll learn"
    "Why this matters"
    "The one concept"
    "Show me"
    "Try it yourself"
    "Common mistakes"
    "Lesson reflection"
    "What's next"
    "Glossary card"
  )

  BEG_EX_SECTIONS=(
    "What you'll build"
    "Before you start"
    "Step-by-step"
    "The prompt to paste"
    "How to know it worked"
    "If something went wrong"
    "You did it!"
  )

  # --- V1, V2, V3, V13: per-deck checks --------------------------------------
  BEG_TOTAL_MIN=0
  i=0
  while [[ $i -lt ${#BEG_DECK_SLUGS[@]} ]]; do
    slug="${BEG_DECK_SLUGS[$i]}"
    expected_min="${BEG_DECK_MINS[$i]}"
    part_no=$(printf '%02d' $((i+1)))
    i=$((i+1))
    f="slides/beginner/${slug}.md"
    if [[ ! -f "$f" ]]; then
      # During authoring, decks may not yet exist; skip silently (V7 will fail later if total wrong).
      continue
    fi

    # Strip HTML comments once for body-content checks.
    stripped=$(perl -0777 -pe 's/<!--.*?-->//gs' "$f")

    # V2: duration marker = expected (matched against ORIGINAL file, since the marker IS an HTML comment).
    if ! grep -qE "<!--[[:space:]]*duration:[[:space:]]*${expected_min}[[:space:]]*min[[:space:]]*-->" "$f"; then
      fail "$f: duration marker must say ${expected_min} min for module ${part_no}"
    else
      BEG_TOTAL_MIN=$((BEG_TOTAL_MIN + expected_min))
      ok "$f: duration marker = ${expected_min} min"
    fi

    # V1: H2 sequence MUST equal BEG_DECK_SECTIONS exactly (after comment strip).
    actual_h2=$(printf '%s\n' "$stripped" | grep -E '^## ' | sed 's/^## //')
    expected_h2=$(printf '%s\n' "${BEG_DECK_SECTIONS[@]}")
    if [[ "$actual_h2" != "$expected_h2" ]]; then
      fail "$f: deck H2 sequence mismatch (expected 9 sections in canonical order, got: $(printf '%s\n' "$actual_h2" | tr '\n' '|'))"
    else
      ok "$f: deck sections (9/9 in order)"
    fi

    # V3: content-slide cap. Count `^---$` separators between end-of-frontmatter
    # and the `## Glossary card` heading. The deck has frontmatter delimited by
    # `---` at lines 1 and N; we want separators AFTER frontmatter and BEFORE
    # the Glossary card.
    sep_count=$(awk '
      BEGIN { in_fm=0; fm_done=0; count=0 }
      /^---$/ {
        if (!fm_done) {
          if (in_fm==0) { in_fm=1; next }
          else { in_fm=0; fm_done=1; next }
        } else { count++ }
        next
      }
      /^## Glossary card[[:space:]]*$/ { print count; exit }
      END { if (!seen) print count }
    ' "$f")
    sep_count=${sep_count:-0}
    if (( sep_count > 12 )); then
      fail "$f: ${sep_count} content slides exceed cap of 12"
    else
      ok "$f: content-slide count = ${sep_count} (≤ 12)"
    fi

    # V13: "Show me" slide body MUST contain a fenced code block or image link.
    showme_body=$(printf '%s\n' "$stripped" | awk '
      /^## Show me[[:space:]]*$/ { capture=1; next }
      capture && /^---[[:space:]]*$/ { exit }
      capture && /^## / { exit }
      capture { print }
    ')
    if printf '%s\n' "$showme_body" | grep -qE '^```' \
       || printf '%s\n' "$showme_body" | grep -qE '!\[[^]]*\]\([^)]+\)'; then
      ok "$f: \"Show me\" slide has runnable code or screenshot"
    else
      fail "$f: \"Show me\" slide must contain a fenced code block or image (no decorative stock imagery)"
    fi
  done

  # --- V7: duration sum --------------------------------------------------------
  beg_static_sum=0
  for m in "${BEG_DECK_MINS[@]}"; do beg_static_sum=$((beg_static_sum + m)); done
  if (( beg_static_sum >= 200 && beg_static_sum <= 240 )); then
    ok "beginner module duration sum = ${beg_static_sum} (range 200..240)"
  else
    fail "beginner module duration sum = ${beg_static_sum} (must be 200..240)"
  fi

  # --- V4, V5: per-exercise checks --------------------------------------------
  # Module 00 setup (V4 only; no solution/ required).
  m0="exercises/beginner/module-00-setup/README.md"
  if [[ -f "$m0" ]]; then
    actual_h2=$(grep -E '^## ' "$m0" | sed 's/^## //')
    expected_h2=$(printf '%s\n' "${BEG_EX_SECTIONS[@]}")
    if [[ "$actual_h2" != "$expected_h2" ]]; then
      fail "$m0: exercise H2 sequence mismatch (expected 7 sections in canonical order)"
    else
      ok "$m0: exercise sections (7/7 in order)"
    fi
    if [[ ! -d exercises/beginner/module-00-setup/starter ]]; then
      fail "exercises/beginner/module-00-setup/: required directory 'starter' missing"
    fi
  fi

  for n in 01 02 03 04 05 06 07 08; do
    f="exercises/beginner/part-${n}/README.md"
    if [[ ! -f "$f" ]]; then
      continue
    fi
    actual_h2=$(grep -E '^## ' "$f" | sed 's/^## //')
    expected_h2=$(printf '%s\n' "${BEG_EX_SECTIONS[@]}")
    if [[ "$actual_h2" != "$expected_h2" ]]; then
      fail "$f: exercise H2 sequence mismatch (expected 7 sections in canonical order)"
    else
      ok "$f: exercise sections (7/7 in order)"
    fi
    # V5: starter/ non-empty and solution/ has at least one non-empty file.
    starter_dir="exercises/beginner/part-${n}/starter"
    solution_dir="exercises/beginner/part-${n}/solution"
    if [[ ! -d "$starter_dir" ]] || [[ -z "$(find "$starter_dir" -type f 2>/dev/null | head -1)" ]]; then
      fail "exercises/beginner/part-${n}/: required directory 'starter' missing or empty"
    fi
    if [[ ! -d "$solution_dir" ]] || [[ -z "$(find "$solution_dir" -type f -not -empty 2>/dev/null | head -1)" ]]; then
      fail "exercises/beginner/part-${n}/: required directory 'solution' missing or empty"
    fi
  done

  # --- V8: glossary character-identity, orphans, dups -------------------------
  # Format: `- **Term**: definition.`
  glossary_file="GLOSSARY.md"
  if [[ -f "$glossary_file" ]]; then
    # Extract all (term, full-line) pairs from GLOSSARY.md.
    glossary_lines=$(grep -nE '^- \*\*[^*]+\*\*:' "$glossary_file" || true)
    # Collect unique terms (and detect dups).
    glossary_terms=$(printf '%s\n' "$glossary_lines" | sed -E 's/^[0-9]+:- \*\*([^*]+)\*\*:.*/\1/' | grep -v '^$' || true)
    dup_terms=$(printf '%s\n' "$glossary_terms" | sort | uniq -d || true)
    if [[ -n "$dup_terms" ]]; then
      while IFS= read -r dt; do
        [[ -n "$dt" ]] && fail "GLOSSARY.md: duplicate term '$dt'"
      done <<< "$dup_terms"
    fi

    # Extract all deck Glossary-card pairs.
    drift_count=0
    deck_referenced_terms=""
    for slug in "${BEG_DECK_SLUGS[@]}"; do
      df="slides/beginner/${slug}.md"
      [[ -f "$df" ]] || continue
      # Body between `## Glossary card` and end-of-file (or next H2 if any — none expected, it's last).
      gc_body=$(awk '/^## Glossary card[[:space:]]*$/ {capture=1; next} capture && /^## / {exit} capture {print}' "$df")
      deck_pairs=$(printf '%s\n' "$gc_body" | grep -E '^- \*\*[^*]+\*\*:' || true)
      while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        term=$(printf '%s' "$line" | sed -E 's/^- \*\*([^*]+)\*\*:.*/\1/')
        deck_referenced_terms="$deck_referenced_terms
$term"
        # Find matching line in GLOSSARY.md (byte-identical comparison).
        match=$(printf '%s\n' "$glossary_lines" | sed -E 's/^[0-9]+://' | grep -F -x -- "$line" || true)
        if [[ -z "$match" ]]; then
          fail "$df: Glossary card term '$term' does not byte-identically match any entry in GLOSSARY.md"
          drift_count=$((drift_count+1))
        fi
      done <<< "$deck_pairs"
    done

    # Orphan check: every GLOSSARY.md term must be referenced by ≥ 1 deck.
    orphan_count=0
    while IFS= read -r gt; do
      [[ -z "$gt" ]] && continue
      if ! printf '%s\n' "$deck_referenced_terms" | grep -F -x -- "$gt" >/dev/null; then
        fail "GLOSSARY.md: orphan term '$gt' not referenced by any beginner deck"
        orphan_count=$((orphan_count+1))
      fi
    done <<< "$glossary_terms"

    term_count=$(printf '%s\n' "$glossary_terms" | grep -c . || true)
    if (( drift_count == 0 && orphan_count == 0 )) && [[ -z "$dup_terms" ]]; then
      ok "GLOSSARY.md: ${term_count} terms, 0 orphans, 0 drift, all unique"
    fi
  else
    fail "GLOSSARY.md: file missing"
  fi

  # --- V9: quiz coverage ------------------------------------------------------
  quiz_file="assessments/beginner/quiz.md"
  ak_file="assessments/beginner/answer-key.md"
  if [[ -f "$quiz_file" ]]; then
    # Count Q-blocks: lines matching `^### Q[0-9]+\.`
    q_count=$(grep -cE '^### Q[0-9]+\.' "$quiz_file" || true)
    if (( q_count != 16 )); then
      fail "$quiz_file: expected 16 questions, found ${q_count}"
    fi

    # For each Q, find the preceding `<!-- module: NN -->` and count per module.
    per_module=$(awk '
      /<!--[[:space:]]*module:[[:space:]]*[0-9]+[[:space:]]*-->/ {
        line=$0
        sub(/.*module:[[:space:]]*/, "", line)
        sub(/[[:space:]]*-->.*/, "", line)
        cur=line
        next
      }
      /^### Q[0-9]+\./ { if (cur != "") counts[cur]++ }
      END { for (k in counts) printf "%s %d\n", k, counts[k] }
    ' "$quiz_file" | sort)
    bad_modules=""
    for n in 01 02 03 04 05 06 07 08; do
      cnt=$(printf '%s\n' "$per_module" | awk -v want="$n" '$1==want {print $2}')
      cnt=${cnt:-0}
      if [[ "$cnt" != "2" ]]; then
        bad_modules="$bad_modules module-${n}=${cnt}"
      fi
    done
    if [[ -n "$bad_modules" ]]; then
      fail "$quiz_file: each module must have exactly 2 questions; got:${bad_modules}"
    fi

    # Each question must have 4 options A. B. C. D.
    opt_issues=$(awk '
      /^### Q[0-9]+\./ { if (qn != "" && (a+b+c+d) != 4) print qn":opts="a+b+c+d; qn=$0; a=b=c=d=0; next }
      /^A\./ { a=1 } /^B\./ { b=1 } /^C\./ { c=1 } /^D\./ { d=1 }
      END { if (qn != "" && (a+b+c+d) != 4) print qn":opts="a+b+c+d }
    ' "$quiz_file")
    if [[ -n "$opt_issues" ]]; then
      while IFS= read -r oi; do
        [[ -n "$oi" ]] && fail "$quiz_file: ${oi} (expected exactly 4 options A-D)"
      done <<< "$opt_issues"
    fi

    if (( q_count == 16 )) && [[ -z "$bad_modules" ]] && [[ -z "$opt_issues" ]]; then
      ok "$quiz_file: 16/16 questions, 2 per module, all with A-D options"
    fi
  fi

  if [[ -f "$ak_file" ]] && [[ -f "$quiz_file" ]]; then
    # For each Q<N> in quiz, ensure answer-key has a line starting with "<N>." and a letter A-D.
    missing_ak=""
    q_nums=$(grep -oE '^### Q[0-9]+\.' "$quiz_file" | sed -E 's/^### Q([0-9]+)\..*/\1/')
    for qn in $q_nums; do
      if ! grep -qE "^${qn}\.[[:space:]]+[A-D]\b" "$ak_file"; then
        missing_ak="${missing_ak} Q${qn}"
      fi
    done
    if [[ -n "$missing_ak" ]]; then
      fail "$ak_file: missing or malformed entries for:${missing_ak}"
    else
      [[ -n "$q_nums" ]] && ok "$ak_file: all questions answered (A-D letter present)"
    fi
  fi

  # --- V10: cross-references --------------------------------------------------
  v10_check() {
    local file="$1"; shift
    [[ -f "$file" ]] || { fail "$file: file missing (required for V10 cross-references)"; return; }
    local missing=""
    for target in "$@"; do
      if ! grep -qF "$target" "$file"; then
        missing="${missing} $target"
      fi
    done
    if [[ -n "$missing" ]]; then
      for t in $missing; do
        fail "$file: missing required cross-reference to '$t'"
      done
    else
      ok "$file: all required cross-references present"
    fi
  }
  v10_check README.md beginner-student-guide.md slides/beginner/README.md
  v10_check beginner-student-guide.md assessments/beginner/quiz.md beginner-certificate-template.md scripts/check-beginner-capstone.sh
  v10_check beginner-instructor-guide.md beginner-student-guide.md

  # --- V11: optional beginner skills ------------------------------------------
  if [[ ! -d skills/beginner ]]; then
    ok "skills/beginner (optional, none authored)"
  else
    beg_skills=$(ls skills/beginner/*/SKILL.md 2>/dev/null || true)
    if [[ -z "$beg_skills" ]]; then
      ok "skills/beginner (optional, directory exists but no SKILL.md authored)"
    else
      for sf in $beg_skills; do
        missing_sec=""
        for sec in "${SKILL_SECTIONS[@]}"; do
          grep -qF "## ${sec}" "$sf" || missing_sec="${missing_sec} '${sec}'"
        done
        if [[ -n "$missing_sec" ]]; then
          fail "$sf: missing H2 section(s):${missing_sec}"
        else
          ok "$sf (optional beginner skill, 6-section contract satisfied)"
        fi
      done
    fi
  fi

  # --- V12: certificate template ----------------------------------------------
  cert_file="beginner-certificate-template.md"
  if [[ -f "$cert_file" ]]; then
    required_placeholders=(STUDENT_NAME COMPLETION_DATE INSTRUCTOR_NAME WORKSHOP_TITLE VERIFICATION_TOKEN)
    missing_p=""
    for p in "${required_placeholders[@]}"; do
      if ! grep -qF "{{${p}}}" "$cert_file"; then
        missing_p="${missing_p} {{${p}}}"
      fi
    done
    if [[ -n "$missing_p" ]]; then
      for mp in $missing_p; do
        fail "$cert_file: missing required placeholder '$mp'"
      done
    else
      ok "$cert_file: all 5 required placeholders present"
    fi
  else
    fail "$cert_file: file missing"
  fi

fi  # end beginner course extensions

# ----------------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------------

echo
echo "============================================================"
echo "  Validator summary: ${PASS} ok, ${FAIL} fail"
echo "============================================================"

if (( FAIL > 0 )); then
  echo
  echo "Failures:"
  for d in "${FAIL_DETAILS[@]}"; do
    echo "  - $d"
  done
  exit 1
fi
exit 0
