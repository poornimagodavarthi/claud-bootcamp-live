# Quickstart — Authoring & Validating the Beginner Course

**Feature**: `002-claude-beginner-course`  
**Phase**: 1 (Design & Contracts)  
**Audience**: A maintainer who has cloned this repo and wants to (a) author a beginner module, (b) build the slides, (c) verify everything passes, or (d) grade a learner's capstone.

---

## Prerequisites

- macOS, Linux, or Windows + WSL2
- Node.js ≥ 20 (needed only by `npx` for Marp)
- Python 3.11+ (for the Module 08 capstone reference and grader)
- Bash 3.2+ (preinstalled on macOS; default everywhere else)
- A Chromium binary somewhere Puppeteer can find it (set `CHROME_PATH` if not in a standard location — see `slides/deploy-pptx.sh` header)
- Claude Code CLI installed: `npm i -g @anthropic-ai/claude-code` (only needed if you want to dry-run the prompts; not required to build or validate)

## Repo layout (beginner-relevant subset)

```text
Training-Claude-Code-Extended/
├── GLOSSARY.md
├── beginner-student-guide.md
├── beginner-instructor-guide.md
├── beginner-certificate-template.md
├── slides/
│   ├── deploy-pptx.sh            # builds intermediate AND beginner decks
│   └── beginner/part-NN-*.md
├── exercises/beginner/part-NN/{README.md,starter/,solution/}
├── assessments/beginner/{quiz.md,answer-key.md}
└── scripts/
    ├── validate.sh                       # extended for beginner
    └── check-beginner-capstone.sh        # new
```

Full layout: see `plan.md` § Project Structure.

---

## Workflow A — Author a new beginner module

Suppose you're adding **Module 04 — Reading code together**.

1. **Edit the glossary first** (single source of truth). Open `GLOSSARY.md` and add the new terms this module introduces, e.g.:

   ```markdown
   - **Code reading**: Asking Claude Code to explain a file before changing it.
   - **Follow-up**: A second prompt that builds on the answer to the first.
   ```

2. **Create the deck** at `slides/beginner/part-04-reading-code-together.md`. Copy the skeleton from `contracts/deck-10-section.md`. Make sure the `## Glossary card` section's lines are character-identical to the lines you just added to `GLOSSARY.md`.

3. **Create the exercise** at `exercises/beginner/part-04/`:

   ```text
   exercises/beginner/part-04/
   ├── README.md       # use the skeleton from contracts/exercise-7-section.md
   ├── starter/        # put any scaffolding files here (NEVER step 1 = create file)
   └── solution/       # a working reference (file, transcript, screenshot…)
   ```

4. **Add 2 quiz questions** to `assessments/beginner/quiz.md`, each preceded by `<!-- module: 04 -->`. Add matching entries to `assessments/beginner/answer-key.md` with the letter + source slide/step + a one-sentence rationale.

5. **Run the validator** (Workflow C). Fix everything red. Re-run until 0 fail.

6. **Build the deck to PPTX** (Workflow B) and eyeball the output for slide breaks and density.

7. Open a PR.

## Workflow B — Build all slides to PPTX

```text
cd slides
./deploy-pptx.sh                 # builds both intermediate and beginner decks
                                 # output: slides/dist/pptx/*.pptx
```

To build a single deck:

```text
cd slides
npx --yes @marp-team/marp-cli@latest \
  --allow-local-files --pptx \
  -o dist/pptx/beginner/part-04-reading-code-together.pptx \
  beginner/part-04-reading-code-together.md
```

Other formats: `--pdf`, `--html`. See `slides/deploy-pptx.sh --help`.

## Workflow C — Validate structural compliance

```text
scripts/validate.sh
```

Expected on a clean repo: `Result: N ok, 0 fail` (where N includes both the intermediate and beginner checks). Any `fail:` line names the file, line, and reason. Fix and re-run.

Tip: the validator runs in ≤ 5 seconds; bind it to your editor's save hook if useful.

## Workflow D — Grade a learner's capstone

The learner gives you their `notes.py`. From the repo root:

```text
scripts/check-beginner-capstone.sh /path/to/learner/notes.py
```

Outcomes:

| Output | Meaning |
|---|---|
| `PASS <8-hex-token>` (exit 0) | The four CLI calls behaved per `contracts/capstone-cli.md`. Issue the certificate; paste the token into `{{VERIFICATION_TOKEN}}`. |
| `FAIL: <step>: …` to stderr (exit 1) | The named step deviated. Tell the learner what failed; ask them to fix and resubmit. |
| `usage: …` (exit 2) | You forgot the path argument. |

The script runs in an isolated temp dir, so it never touches the learner's other files.

## Workflow E — Issue a certificate to a passing learner

After Workflow D returns `PASS <TOKEN>`, render the certificate:

```text
sed \
  -e 's/{{STUDENT_NAME}}/Jane Doe/g' \
  -e "s/{{COMPLETION_DATE}}/$(date +%Y-%m-%d)/g" \
  -e 's/{{INSTRUCTOR_NAME}}/Luca Berton/g' \
  -e 's/{{WORKSHOP_TITLE}}/Claude Code 101 — Beginner Workshop/g' \
  -e 's/{{VERIFICATION_TOKEN}}/d4e3c2b1/g' \
  beginner-certificate-template.md > /tmp/jane-cert.md
```

Convert to PDF/PNG via your preferred Markdown-to-PDF tool (e.g. `pandoc`, or open in VS Code and "Export PDF"). See `beginner-student-guide.md` for the canonical one-liner.

---

## Acceptance walk-through (matches `spec.md` user stories)

| User story | How to verify |
|---|---|
| **US1 — Absolute beginner, first lesson** | Walk a non-developer through `exercises/beginner/module-00-setup/README.md` + `exercises/beginner/part-01/README.md` cold. Stopwatch ≤ 30 min total. Deliverable: their `first-prompt.txt`. |
| **US2 — Self-paced learner, weekend completion** | Time one learner from `beginner-student-guide.md` to a rendered certificate. Target ≤ 5 hours. |
| **US3 — Workshop facilitator, 180 min live** | Read `beginner-instructor-guide.md` and run a dry-run. Hit the per-module minute budgets within ±10%. |
| **US4 — Intermediate-course learner uses this as remedial** | Cross-read: every Claude Code term used in `slides/part-01-setup-mindset.md` is defined in `GLOSSARY.md`. Run `grep -of <terms> slides/part-01-setup-mindset.md` against the glossary. |

---

## Failure-mode quick reference

| Symptom | First thing to check |
|---|---|
| `fail: …: glossary drift for term '…'` | Edit `GLOSSARY.md` first; then copy the canonical line into the deck. |
| `fail: …: deck H2 sequence mismatch` | Diff your deck against `contracts/deck-10-section.md` § Sample skeleton. |
| `fail: …: exercise H1 must match deck H1` | Update the exercise's `# Module NN — Title` to match the deck's H1. |
| `FAIL: list: expected '1\thello', got …` from grader | The learner's `list` command output is wrong; compare against `contracts/capstone-cli.md`. |
| Marp crashes with `require is not defined` | Your global `marp` binary is broken under Node 26. Use `npx --yes @marp-team/marp-cli@latest …` instead. |
| `PPTX export hangs` | Set `CHROME_PATH` to your Chromium binary; see `slides/deploy-pptx.sh` header. |

---

## Next step

Run `/speckit.tasks` to convert this plan into an ordered task list.
