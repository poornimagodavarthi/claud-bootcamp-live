# Contract — Capstone Grader (`scripts/check-beginner-capstone.sh`)

**Feature**: `002-claude-beginner-course`  
**Applies to**: `scripts/check-beginner-capstone.sh`  
**Spec**: FR-045, FR-046, Clarifications Q4  
**Pairs with**: `contracts/capstone-cli.md`

---

## Invocation

```text
scripts/check-beginner-capstone.sh <path-to-notes.py>
```

| Arg | Required | Meaning |
|---|---|---|
| `$1` | yes | Path to the learner's `notes.py` (absolute or relative). Must be a readable file. |

If `$1` is missing or unreadable:

```text
usage: scripts/check-beginner-capstone.sh <path-to-notes.py>
```

Exit code: `2`.

## Behavior

The script MUST perform exactly these steps, in order:

1. Resolve `$1` to an absolute path; abort with usage if missing or unreadable.
2. Create a temp directory with `mktemp -d`; install a trap to `rm -rf` it on EXIT/INT/TERM.
3. Copy the input `notes.py` into the temp dir (so `notes.json` is created inside the temp dir, not next to the learner's file).
4. `cd` into the temp dir.
5. Run `python3 notes.py add "hello"` and capture stdout, stderr, and exit code.
    - Assert exit code `0` and stdout exactly equals `added: 1\n`. Otherwise FAIL.
6. Run `python3 notes.py list` and capture as above.
    - Assert exit code `0` and stdout exactly equals `1\thello\n`. Otherwise FAIL.
7. Run `python3 notes.py delete 1` and capture.
    - Assert exit code `0` and stdout exactly equals `deleted: 1\n`. Otherwise FAIL.
8. Run `python3 notes.py list` and capture.
    - Assert exit code `0` and stdout exactly equals `` (empty). Otherwise FAIL.
9. Concatenate the four captured stdouts into one string `ALL`.
10. Compute `TOKEN=$(printf '%s' "$ALL" | shasum -a 256 | awk '{print $1}' | cut -c1-8)`.
11. Print exactly: `PASS <TOKEN>` (one line, no trailing whitespace). Exit `0`.

## Failure output

On any failed assertion, the script MUST print exactly one line to stderr:

```text
FAIL: <step-name>: expected <expected>, got <actual>
```

Examples:

- `FAIL: add: expected 'added: 1', got 'added: 23'`
- `FAIL: add: expected exit 0, got exit 1 (stderr: 'NameError: …')`
- `FAIL: list-after-delete: expected empty output, got '1\thello'`

Exit code on any failure: `1` (distinct from usage error `2`).

## Portability constraints

- Bash 3.2+ (no associative arrays, no `mapfile`, no `[[ -v var ]]`).
- POSIX utilities only: `mktemp`, `cp`, `cd`, `printf`, `shasum`, `awk`, `cut`. No `jq`, no `python` (only `python3` is invoked, and only against `notes.py`).
- MUST work without internet access.
- MUST work when called from any cwd.

## Required script header

```bash
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
```

## Verification token semantics

- 8 hex characters, derived deterministically from `sha256(concatenated_stdouts)`.
- Two different correct `notes.py` files MAY produce the same token (because the captured stdouts are identical when behavior is identical). This is intentional: the token attests correctness, not authorship.
- The token is meant to be pasted into the certificate's `{{VERIFICATION_TOKEN}}` field by the learner. It is NOT a credential and is NOT meant to resist tampering.

## Self-test

A maintainer can verify the grader against the reference solution:

```text
$ scripts/check-beginner-capstone.sh exercises/beginner/part-08/solution/notes.py
PASS d4e3c2b1
```

The exact token will be stable across runs of the reference solution and will change only if the contract or solution output changes.

## Validator integration

`scripts/validate.sh` MAY (but is NOT required to) invoke the grader against the reference solution as a final smoke check, gated by `[[ -x scripts/check-beginner-capstone.sh ]]`. If it does, a failure is reported as `fail: scripts/check-beginner-capstone.sh: <grader output>`.
