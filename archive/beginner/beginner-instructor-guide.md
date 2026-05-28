# Claude Code 101 — Beginner Instructor Guide

This guide is for the human leading a live or async cohort through the beginner workshop. It pairs with [beginner-student-guide.md](beginner-student-guide.md): students read theirs, you read this. Keep both open.

Target audience: any maintainer who can read Markdown, edit Bash, and read a Python file. You do not need to have written any of the materials.

## At a glance

| Item | Value |
|---|---|
| Total student time (modules + setup) | ~240 min |
| Recommended live-session length | 180 min (3 hours) |
| Cohort size | 6–12 ideal; up to 20 with a helper |
| Required tools on student machines | Node 18+, Git, terminal access, Claude Code |
| Required tools on instructor machine | All of the above + `npx`, `bash`, `python3` 3.11+ |
| Pass criteria per student | ≥ 12/16 on quiz AND `PASS <token>` from capstone grader |

## 180-minute live schedule

Use this when running a single 3-hour session. The 8 modules are compressed by reading the deck out loud as a group, then doing the exercise individually with a 90-second "share-out" round.

| Time   | Block                                       | Notes                                                                                       |
|--------|---------------------------------------------|---------------------------------------------------------------------------------------------|
| 0:00   | Welcome + setup check (module-00 quick gate)| Walk the room; everyone runs `claude --version`. Anyone failing pairs with a working laptop.|
| 0:10   | Module 01 — Meet Claude Code                | Deck 5 min, exercise 10 min, share-out 1 min.                                               |
| 0:26   | Module 02 — Your first real conversation    | Deck 5, exercise 12, share-out 1.                                                           |
| 0:44   | Module 03 — Asking for what you want        | Deck 6, exercise 14, share-out 1.                                                           |
| 1:05   | **Break (10 min)**                          |                                                                                             |
| 1:15   | Module 04 — Reading code together           | Deck 5, exercise 10, share-out 1.                                                           |
| 1:31   | Module 05 — Editing one file safely         | Deck 6, exercise 16, share-out 2. The git ceremony is the slowest step.                     |
| 1:55   | Module 06 — CLAUDE.md cheat sheet           | Deck 5, exercise 12, share-out 1.                                                           |
| 2:13   | Module 07 — Safer & smarter                 | Deck 6, exercise 10, share-out 2. Discuss real-world incidents.                             |
| 2:31   | Module 08 — Capstone                        | Deck 6, exercise 22, grader 2. Run the grader live, project the `PASS <token>` output.      |
| 3:01   | Quiz + certificates                         | 10 min quiz, 5 min grading, 5 min rendering, 5 min wrap.                                    |

The schedule overruns by 21 minutes — expected. Cut module-04 or module-06 to 10-minute share-outs if you're tight.

## How to grade

There are exactly two artifacts to grade per student:

1. **Quiz score**: open the student's submitted [assessments/beginner/quiz.md](assessments/beginner/quiz.md) and count matches against [assessments/beginner/answer-key.md](assessments/beginner/answer-key.md). 12/16 is pass. The answer key has a one-sentence rationale per question — use it when a student wants to learn from a wrong answer.

2. **Capstone token**: ask the student to send you their `notes.py`. Save it to a temp file and run:

   ```sh
   scripts/check-beginner-capstone.sh /tmp/student-notes.py
   ```

   - `PASS <8-hex-token>` on stdout, exit 0 → pass. Token goes on the certificate.
   - `FAIL: <step>: …` on stderr, exit 1 → fail. Read the step name, point the student at the matching "If something went wrong" row in [exercises/beginner/part-08/README.md](exercises/beginner/part-08/README.md), let them retry.

   Run the grader against your own copy of `exercises/beginner/part-08/solution/notes.py` before the session — that confirms your environment is correct and gives you a known-good token to demo with.

## Common student blockers — at least 8

| Blocker | Where it happens | Fast fix |
|---|---|---|
| `claude --version` exits 127 (command not found) | Module 00 setup | `npm install -g @anthropic-ai/claude-code` (or check PATH); see module-00 troubleshooting. |
| `npm install -g …` fails with EACCES | Module 00 on Linux | Configure a user prefix (`npm config set prefix ~/.npm-global`) or use a Node version manager. |
| WSL2 can't see Claude installed in Windows | Module 00 on Windows | Install Node and Claude **inside** WSL2; do not rely on the Windows install. |
| Student types prompt at `$` instead of `>` | Module 01 | Show that `$` is the shell, `>` is Claude. They must run `claude` first. |
| Student opens a new `claude` session per turn | Module 02 | Reinforce: one `claude` session for the whole conversation; `/exit` only at the end. |
| Vague prompt returns vague answer | Module 03 | Walk them through role + goal + constraint + format and have them rewrite. |
| Claude proposes extra edits the student missed | Module 05 | Reject; re-prompt with explicit "only X, nothing else"; reinforce reading every diff. |
| `git restore` fails because the repo was never committed | Module 05 | Re-do the `git init && git add . && git commit` step from the exercise README. |
| CLAUDE.md ignored | Module 06 | Confirm the student started `claude` from the directory containing CLAUDE.md. |
| Student pasted a real secret | Module 07 | Stop the session. Coach: rotate the secret, learn the lesson; redact going forward. |
| Capstone uses `len(notes) + 1` instead of monotonic ids | Module 08 | Grader catches it; point them at the "Next add reuses id 1" row of part-08 troubleshooting. |
| Grader prints `FAIL: list: expected …\t…, got … …` | Module 08 | Tabs vs spaces. Use a literal `\t` in the f-string. |

## Paper dry-run

Before your first cohort, do a paper dry-run alone:

1. Block out 180 minutes on a calendar with no interruptions.
2. Run through every exercise yourself, following only the student guide and the per-exercise README. Do **not** consult this instructor guide.
3. After each exercise, write down (a) the time it actually took and (b) any sentence in the deck or README that confused you. Send those to the maintainer.
4. At the end, render your own certificate. Confirm all five placeholders are substituted.

If the dry-run took more than 5 hours of wall-clock time, the course is too long for live delivery and you should split it across two sessions.

## Grading workflow checklist

For each student:

- [ ] Receive `~/three-turns.txt` (Module 02), `~/sharp-prompt.txt` (Module 03), and `notes.py` (Module 08).
- [ ] Score the submitted quiz; tally /16.
- [ ] Run `scripts/check-beginner-capstone.sh` against the submitted `notes.py`; record the `PASS <token>`.
- [ ] If both pass thresholds met, render the certificate (see student guide for the `sed` command).
- [ ] Send the rendered certificate to the student.
- [ ] Note any common stumbling blocks for the next cohort.

## What to skip when running short

Cut in this order:

1. The "Lesson reflection" slides during share-outs (read silently, do not discuss).
2. Module 04's follow-up question (one explanation is enough).
3. Module 06's "verify Claude is using CLAUDE.md" prompt (do it as a demo, not per-student).

Never cut: the capstone (Module 08), the quiz, or the safety lesson (Module 07).

## Pointers

- Glossary single source of truth: [GLOSSARY.md](GLOSSARY.md). If a slide and the glossary disagree, the glossary wins (and the validator will catch it).
- Structural validator: `scripts/validate.sh` — run before every cohort to confirm nothing has drifted.
- Capstone contract: [specs/002-claude-beginner-course/contracts/capstone-cli.md](specs/002-claude-beginner-course/contracts/capstone-cli.md).
- Student-facing companion: [beginner-student-guide.md](beginner-student-guide.md).

