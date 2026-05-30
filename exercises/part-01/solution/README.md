# Reference solution — Module 1

> **Stop**: only open this after you have produced your own `module-01/` deliverable.

This module's deliverable is a **workspace** (not running code), so the reference solution is a worked example of what a strong submission contains. Compare your `module-01/` against the checklist below; do not copy.

## What a strong `module-01/` contains

```text
module-01/
├── environment.txt   # output of: python3 --version, node --version, git --version
└── loop-notes.md     # your one-paragraph explanation of the loop, in your own words
```

## The verification check

Confirm your toolchain, then read back your notes (paste one command at a time):

```bash
python3 --version
node --version
git --version
cat module-01/loop-notes.md
```

A strong `loop-notes.md` names all five steps in order — **Plan → Implement → Test → Review → Commit** — in your own words, and closes with why skipping **Review** is the most common failure mode. The reference paragraph looks like this (truncated):

```text
Working with Claude Code is like directing a junior engineer: you Plan the task as a
clear spec, let Claude Implement it, then Test that it runs, Review every line as if it
came from a stranger's PR, and only then Commit. Skipping Review is the #1 way
AI-generated bugs reach production.
```

## Definition of done (mirror of the exercise)

- [ ] `module-01/environment.txt` shows valid Python 3.11+, Node 20+, and Git versions.
- [ ] `module-01/loop-notes.md` names all 5 steps in order, in *your* words — not Claude's verbatim output.
- [ ] You can articulate the **plan → implement → test → review → commit** loop without notes.
