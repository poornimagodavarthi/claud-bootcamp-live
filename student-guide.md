# Student Guide — Claude Code Bootcamp

> Companion to [`README.md`](README.md). Read this **before** the live session.
> Inaugural delivery: 30 May 2026, 09:00 AM EST · Live, Virtual & Practical.

## Prerequisites

You can attend if you have:

- Basic programming literacy in any language
- Git basics: `clone`, `branch`, `commit`, `push`
- A working **Claude Code** account (any tier)
- macOS, Linux, or **Windows-via-WSL2** (native PowerShell is not supported)
- ~30 minutes for the **mandatory pre-work** below
- A laptop, microphone, and a quiet room

## Environment setup

Install once, before the live session:

| Tool | Version | Why |
|---|---|---|
| Python | 3.11+ | Primary track for code-producing modules (2, 4, 5, 7, 8) |
| Node.js | 20+ | Slide build (Marp via npx) + secondary track for modules 2/4/5 |
| Git | any recent | Module 6 + submission |
| Claude Code | any current | All modules |

### macOS

```bash
brew install python@3.11 node git
```

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install -y python3.11 python3-pip nodejs npm git
```

### Windows (WSL2 only)

Native PowerShell is not supported. Set up WSL2 once:

1. Open PowerShell **as Administrator** and run `wsl --install` (Ubuntu by default).
2. Reboot. Open the Ubuntu terminal (Start → Ubuntu).
3. Inside WSL2, follow the Linux instructions above.
4. Run **all** workshop commands inside the WSL2 shell, never in PowerShell or `cmd.exe`.

Verify:

```bash
python3 --version    # → 3.11.x or higher
node --version       # → v20.x.x or higher
git --version
```

## Mandatory pre-work (~30 min)

> **Pre-work is an entry condition** for the live session. Without it you cannot keep up with the 4-hour instruction pace. Module 1's live time is mindset + a 5-minute verification check only — it does **not** include first-time install steps.

Complete in order:

### 1. Environment installed (10 min)

Follow the table above. Verify the three `--version` outputs.

### 2. Repository cloned (5 min)

```bash
git clone https://github.com/lberton/Training-Claude-Code-Extended.git
cd Training-Claude-Code-Extended
```

Confirm the layout matches [`README.md`](README.md#repository-layout).

### 3. Claude Code authenticated (5 min)

Log in via your usual Claude Code workflow (CLI, IDE plugin, or web). Confirm you can issue at least one prompt and receive a response.

### 4. Hello-Claude smoke test (10 min)

Open Claude Code in the cloned repo. Issue this prompt **verbatim**:

```text
You are running inside the Claude Code Bootcamp repository. In two short paragraphs:
1. List the top-level files and directories you can see.
2. Tell me whether Python 3.11+ and Node.js 20+ are available on this machine, and if so what the exact versions are.

End with a single line that says: "Pre-work smoke test passed."
```

**Save Claude's full reply** to:

```text
module-00-prework/hello-claude.txt
```

(Create this folder inside whatever working directory you'll use for submissions — it ships in your final zip.)

### Pre-work checklist

- [ ] Python 3.11+ installed and `python3 --version` works
- [ ] Node.js 20+ installed and `node --version` works
- [ ] Git installed and `git --version` works
- [ ] Repository cloned successfully
- [ ] Claude Code authenticated and responding
- [ ] Hello-Claude smoke test prompt submitted
- [ ] Reply saved to `module-00-prework/hello-claude.txt`
- [ ] Reply ends with the line `Pre-work smoke test passed.`

If any item is unchecked at session start, you will be paired with a neighbor in read-only mode for module 1 only.

## How to follow the modules

Each module has:

- A **slide deck** (live during the session): [`slides/part-NN-…md`](slides/)
- A **lab exercise** (you build): [`exercises/part-NN/README.md`](exercises/)
- An optional **Claude Skill** to invoke during the lab: [`skills/<skill>/SKILL.md`](skills/)

Inside each `exercises/part-NN/README.md` you'll find 9 sections in order: Goal · Scenario · Starter instructions · Claude Code prompt · Manual validation · Expected deliverable · Definition of done · Stretch challenge · Troubleshooting. Follow them top to bottom.

For code-producing modules (2, 4, 5, 7, 8) a **reference solution** lives at `exercises/part-NN/solution/`. **Do not open it before completing the lab** — it spoils the learning loop. After you finish, diff your code against it.

## Submission workflow

At the end of the session you upload **one zip** to the Packt LMS.

### Zip layout

```text
yourname-bootcamp.zip
├── module-00-prework/
│   └── hello-claude.txt
├── module-01/        # AI Coding Workspace artefacts
├── module-02/        # CLI Task Manager source
├── module-03/        # CLAUDE.md + screenshot of Claude using it
├── module-04/        # Notes API source
├── module-05/        # tests/ + bug fix notes + your code-review-rubric.md
├── module-06/        # branch + commit + PR text export
├── module-07/        # dashboard UI source + screenshot
├── module-08/        # refactored module + HANDOFF.md + ARCHITECTURE.md
├── module-09/
│   └── skill/
│       └── SKILL.md  # the skill you authored
├── module-10/        # production-readiness-report.md
└── assessments/
    ├── quiz-answers.md
    ├── practical/    # your practical-task deliverable
    └── reflection.md
```

12 top-level folders total. Stick to this layout — the instructor's grading workflow depends on it.

### Upload

1. Zip the folder: `zip -r yourname-bootcamp.zip yourname-bootcamp/`.
2. Log into the Packt LMS.
3. Find the *Claude Code Bootcamp — 30 May 2026* assignment.
4. Upload the zip.
5. Wait for grading. The instructor scores against [`assessments/rubric.md`](assessments/rubric.md) within 1 week and posts your score back to the LMS.

## Assessment & certificate path

Three components, weighted:

| Component | Weight | File |
|---|---:|---|
| Knowledge quiz | 40% | [`assessments/knowledge-quiz.md`](assessments/knowledge-quiz.md) |
| Practical task | 40% | [`assessments/practical-task.md`](assessments/practical-task.md) |
| Code review reflection | 20% | [`assessments/code-review-reflection.md`](assessments/code-review-reflection.md) |

**Pass = ≥ 70% weighted total.** Pass earns a Packt Certification Certificate of Completion issued from [`certificate-template.md`](certificate-template.md).

If you score < 70%, you may re-take using the same answer key + rubric pair within 30 days.

## Getting unstuck

- **Lab won't finish in time.** Ship the Definition of Done; skip the Stretch challenge.
- **Claude output is wrong.** Open `skills/code-review/SKILL.md` and ask Claude to review its own output.
- **Build fails.** Each exercise has a Troubleshooting section. Read it before asking the instructor.
- **Pair partner needed.** The instructor pairs students at break time on request.

---

**Welcome to the workshop. Build something real.** — Luca Berton
