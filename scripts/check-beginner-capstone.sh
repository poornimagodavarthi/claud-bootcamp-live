#!/usr/bin/env bash
#
# scripts/check-beginner-capstone.sh
#
# Smoke-check a learner's notes.py against the Module 08 capstone contract.
#
# Usage:
#   scripts/check-beginner-capstone.sh <path-to-notes.py>
#
# Exits:
#   0  PASS  (and prints "PASS <8-hex-token>" to stdout)
#   1  FAIL  (and prints "FAIL: …" to stderr)
#   2  usage error
#
# See specs/002-claude-beginner-course/contracts/capstone-grader.md
# Pairs with specs/002-claude-beginner-course/contracts/capstone-cli.md
#
set -eu
set -o pipefail

usage() {
  echo "usage: scripts/check-beginner-capstone.sh <path-to-notes.py>" >&2
  exit 2
}

if [ "$#" -lt 1 ]; then
  usage
fi

INPUT="$1"
if [ ! -r "$INPUT" ] || [ ! -f "$INPUT" ]; then
  usage
fi

# Resolve to absolute path (POSIX: cd + pwd).
INPUT_ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT INT TERM

cp "$INPUT_ABS" "$TMP/notes.py"
cd "$TMP"

# Helper that runs a step, captures stdout/stderr/exit, and asserts.
#   $1 = step name (for FAIL messages)
#   $2 = expected stdout (literal; printf is used so \n => newline)
#   $3 = expected exit code (numeric, usually 0)
#   $@ = command and args after shift 3
run_step() {
  step="$1"; expected_stdout="$2"; expected_exit="$3"
  shift 3
  set +e
  stderr_file="$(mktemp)"
  actual_stdout="$("$@" 2>"$stderr_file")"
  actual_exit=$?
  actual_stderr_capture="$(cat "$stderr_file")"
  rm -f "$stderr_file"
  set -e
  if [ "$actual_exit" -ne "$expected_exit" ]; then
    printf 'FAIL: %s: expected exit %d, got exit %d (stderr: %q)\n' \
      "$step" "$expected_exit" "$actual_exit" "$actual_stderr_capture" >&2
    exit 1
  fi
  # Compare stdout exactly (we generate expected via printf so newlines match).
  expected_rendered="$(printf '%b' "$expected_stdout")"
  if [ "$actual_stdout" != "$expected_rendered" ]; then
    printf 'FAIL: %s: expected %q, got %q\n' \
      "$step" "$expected_rendered" "$actual_stdout" >&2
    exit 1
  fi
  # Echo captured stdout (without trailing newline normalization) for token computation.
  printf '%s\n' "$actual_stdout"
}

ALL=""

OUT1="$(run_step add        'added: 1'   0 python3 notes.py add "hello")"
ALL="$ALL$OUT1"$'\n'

OUT2="$(run_step list       '1\thello'   0 python3 notes.py list)"
ALL="$ALL$OUT2"$'\n'

OUT3="$(run_step delete     'deleted: 1' 0 python3 notes.py delete 1)"
ALL="$ALL$OUT3"$'\n'

OUT4="$(run_step list-after-delete '' 0 python3 notes.py list)"
ALL="$ALL$OUT4"$'\n'

TOKEN="$(printf '%s' "$ALL" | shasum -a 256 | awk '{print $1}' | cut -c1-8)"
printf 'PASS %s\n' "$TOKEN"
exit 0
