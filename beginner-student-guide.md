# Claude Code 101 — Beginner Student Guide

Welcome to the Claude Code 101 beginner workshop. This guide is the one document you should keep open from start to finish. It tells you what to install, what to read in what order, how to know you finished, and how to render your certificate.

Total budget: **~210 minutes** of focused learning across 8 modules, plus ~30 minutes for setup. You can spread it over a single afternoon or four 1-hour sessions.

## Before you start

Complete the install exercise: [exercises/beginner/module-00-setup/](exercises/beginner/module-00-setup/). At the end you should have:

- `node --version` reporting 18 or newer
- `git --version` working
- `claude --version` printing a version number

If any of those fail, fix them before opening Module 01. The setup README has a troubleshooting table including macOS, Linux, and Windows (WSL2).

## The 8 modules — read in order

| #  | Module                              | Read this deck                                                                          | Do this exercise                                                                  | Minutes |
|----|-------------------------------------|-----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|---------|
| 01 | Meet Claude Code                    | [part-01-meet-claude-code.md](slides/beginner/part-01-meet-claude-code.md)              | [exercises/beginner/part-01/](exercises/beginner/part-01/)                        | 20      |
| 02 | Your first real conversation        | [part-02-first-conversation.md](slides/beginner/part-02-first-conversation.md)          | [exercises/beginner/part-02/](exercises/beginner/part-02/)                        | 25      |
| 03 | Asking for what you want            | [part-03-asking-for-what-you-want.md](slides/beginner/part-03-asking-for-what-you-want.md) | [exercises/beginner/part-03/](exercises/beginner/part-03/)                     | 30      |
| 04 | Reading code together               | [part-04-reading-code-together.md](slides/beginner/part-04-reading-code-together.md)    | [exercises/beginner/part-04/](exercises/beginner/part-04/)                        | 25      |
| 05 | Editing one file safely             | [part-05-editing-one-file-safely.md](slides/beginner/part-05-editing-one-file-safely.md) | [exercises/beginner/part-05/](exercises/beginner/part-05/)                       | 30      |
| 06 | CLAUDE.md cheat sheet               | [part-06-claude-md-cheat-sheet.md](slides/beginner/part-06-claude-md-cheat-sheet.md)    | [exercises/beginner/part-06/](exercises/beginner/part-06/)                        | 25      |
| 07 | Safer & smarter                     | [part-07-safer-and-smarter.md](slides/beginner/part-07-safer-and-smarter.md)                    | [exercises/beginner/part-07/](exercises/beginner/part-07/)                        | 25      |
| 08 | Putting it together (capstone)      | [part-08-putting-it-together.md](slides/beginner/part-08-putting-it-together.md)        | [exercises/beginner/part-08/](exercises/beginner/part-08/)                        | 30      |

The deck index lives at [slides/beginner/README.md](slides/beginner/README.md).

For every module: read the deck (5–10 minutes), then do the exercise (15–20 minutes). Take a 5-minute break between modules; you will learn more if you do not binge.

## The shared glossary

Every defined term is in [GLOSSARY.md](GLOSSARY.md). If a term on a slide is fuzzy, search the glossary first — the deck's "Glossary card" repeats the same definition byte-for-byte.

## Self-check: the quiz

After all 8 modules, take the 16-question multiple-choice quiz at [assessments/beginner/quiz.md](assessments/beginner/quiz.md). Passing threshold is **12 out of 16**. The answer key with citations is in [assessments/beginner/answer-key.md](assessments/beginner/answer-key.md) — try the quiz before peeking.

## The capstone token

Module 08's exercise produces a `notes.py` file. Run the grader from the repo root:

```sh
scripts/check-beginner-capstone.sh exercises/beginner/part-08/starter/notes.py
```

If your implementation is correct, the grader prints `PASS <8-hex-token>` on its first line. **Save that token.** It is how you prove on your certificate that you actually built and ran the capstone.

## Render your certificate

Once you have (a) at least 12 out of 16 on the quiz and (b) a `PASS <token>` from the grader, render your personal certificate from [beginner-certificate-template.md](beginner-certificate-template.md).

One-line rendering (replace each value with your own):

```sh
sed -e 's|{{STUDENT_NAME}}|Jane Doe|' \
    -e 's|{{COMPLETION_DATE}}|2025-05-21|' \
    -e 's|{{INSTRUCTOR_NAME}}|Ada Lovelace|' \
    -e 's|{{WORKSHOP_TITLE}}|Claude Code 101|' \
    -e 's|{{VERIFICATION_TOKEN}}|56043e66|' \
    beginner-certificate-template.md > my-certificate.md
```

Verify all five placeholders were replaced (none should remain):

```sh
grep -E '\{\{[A-Z_]+\}\}' my-certificate.md && echo "still has placeholders — fix" || echo "clean"
```

## When something goes wrong

Each exercise has its own troubleshooting table. Beyond that:

- **Claude cannot find a file**: you probably started `claude` from the wrong directory. `cd` into the project root.
- **`scripts/check-beginner-capstone.sh: command not found`**: invoke it with an explicit path; do not assume it is on `$PATH`.
- **The deck will not render to PPTX**: that is an instructor concern; see [beginner-instructor-guide.md](beginner-instructor-guide.md).

## What's next

If you finished, you have the foundation. The next course in this curriculum is the intermediate workshop in [specs/001-bootcamp-course-materials/](specs/001-bootcamp-course-materials/) — multi-file edits, automated testing, custom slash commands, and production workflows. Take a week's break first; let the basics stick.

