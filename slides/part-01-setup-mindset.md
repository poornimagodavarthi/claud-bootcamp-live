---
marp: true
theme: wow-beginner
header: 'Claude Code Bootcamp · Day 1 · Module 01'
paginate: true
size: 16:9
title: "Module 1 — Welcome, Setup & AI-First Mindset"
description: "Open the workshop. Meet the instructor, Anthropic, and the models. Name the 5-step AI coding loop. Confirm every laptop is ready."
---

<!-- duration: 20 min -->
<!-- _class: tpl-cover -->
<!-- _paginate: false -->
<!-- _header: "" -->

<span class="module-chip">Module 01 · 20 min</span>

# Setup & AI-First Mindset

**You + Claude Code = a junior engineer you direct, review, and merge.**

Instructor: **Luca Berton** · Endorsed by **Packt Certification**

<img class="hero-icon" src="themes/icons/terminal.svg" alt="" />

<!--
SPEAKER NOTES — slide 1 (60 sec hook)
- Welcome. Confirm everyone joined the LMS. Show today's schedule on your second screen.
- ONE sentence: "By the end of today you'll ship 10 small projects with Claude Code."
- DO NOT do live installs here. Pre-work is the entry condition.
-->

---

<!-- _class: tpl-objectives -->

## Welcome · What you'll build today

**10 small, real projects in 4 hours** — one per module, all with Claude Code.

- **Format**: short theory → live demo → you build it → quick review. Every module.
- **Proof of work**: each module drops a `module-NN/` folder into your final submission zip.
- **Certificate**: pass the quiz + practical + reflection (≥ 70%) → Packt-endorsed certificate.
- **The through-line**: one repeatable loop you take back to your day job on Monday.

You direct. Claude implements. You review and merge. **You are always the engineer of record.**

<!--
SPEAKER NOTES — slide 2 (course intro, 2 min)
- Point at the schedule in README.md on your second screen.
- Set expectations on breaks. Time is the scarce resource today — say it out loud.
-->

---

## Your instructor — Luca Berton

- **Automation engineer & educator.** 15+ years shipping infrastructure-as-code, Ansible, and developer tooling for global enterprises.
- **Author & speaker.** Books on Ansible and DevOps; regular conference speaker; runs a YouTube channel on automation.
- **AI-paired delivery practitioner.** Uses Claude Code daily to plan, refactor, document, and review production code.
- **Today's mission**: get you shipping with Claude Code the same way — safely, repeatably, with a loop you can take home.

🔗 [lucaberton.com](https://lucaberton.com/)

<!--
SPEAKER NOTES — slide 3 (instructor, 1 min)
- Keep it short and credible. The students are here to build, not to hear a résumé.
-->

---

<!-- _class: tpl-show -->

## Anthropic & the Claude models (May 2026)

**Anthropic** builds Claude — frontier models with a safety-first focus. **Claude Code** is their agentic coding tool.

| Model | Best for | Trade-off |
|---|---|---|
| **Claude Opus** | Hardest reasoning: architecture, gnarly refactors, multi-file plans | Slowest · highest cost |
| **Claude Sonnet** | The daily driver: most coding, reviews, tests | Balanced speed / cost / quality |
| **Claude Haiku** | Fast, cheap: quick edits, summaries, high-volume calls | Less depth on hard problems |

**Rule of thumb**: start on **Sonnet**. Escalate to **Opus** when stuck on design. Drop to **Haiku** for bulk/trivial work. Switch live with `/model`.

<!--
SPEAKER NOTES — slide 4 (models, 2 min)
- Don't quote exact prices — they move. Teach the SHAPE: Opus=think, Sonnet=do, Haiku=fast.
- Most of today runs fine on Sonnet. Mention you'll call out where Opus earns its cost.
-->

---

<!-- _class: tpl-objectives -->

## Theory · The AI coding loop (3 min)

**You stay the engineer of record. Claude proposes; you decide.**

Every module today repeats the same 5 steps:

> **Plan → Implement → Test → Review → Commit**

- **Plan** — write the prompt the way a Tech Lead writes a spec.
- **Implement** — let Claude generate; you read every line.
- **Test** — run it. If it doesn't run, you have nothing.
- **Review** — read it as if it came from a stranger's PR.
- **Commit** — atomic commits, written prose, no `Co-authored-by: Claude`.

**Skipping `Review` is the #1 way AI-generated bugs reach production.**

<!--
SPEAKER NOTES — slide 5 (theory, 3 min)
- Draw the loop on the whiteboard while talking through it.
- Anchor "engineer of record" — you sign the PR, not Claude.
-->

---

<!-- _class: tpl-show -->

## The loop you'll repeat all day

![The five-step Claude Code loop: Plan, Implement, Test, Review, Commit](intermediate/assets/01-tcc-loop.svg)

**Plan → Implement → Test → Review → Commit.** Skipping **Review** is how AI bugs ship.

<!--
SPEAKER NOTES — slide 6 (diagram, 1 min)
- Trace the arrows once with your cursor; the cycle is the whole course in one picture.
-->

---

<!-- _class: tpl-show -->

## Reference · Claude Code is everywhere (May 2026)

Claude Code ships on **four surfaces** with one shared context:

- **Terminal** — hands-on repo work, `claude -p` piping.
- **VS Code / JetBrains** — inline diffs, gutter actions.
- **Desktop app** — visual diff review, screenshots.
- **Web** — remote/cloud tasks, parallel work, shared sessions.

Today we work in **terminal + IDE**. Patterns transfer to the other surfaces unchanged.

<!--
SPEAKER NOTES — slide 6 (surfaces, 1 min)
- One sentence each. Students only need to know: pick terminal or IDE today.
-->

---

<!-- _class: tpl-show -->

## Reference · Slash commands cheat sheet

| Command | What it does |
|---|---|
| `/help` | List every available slash command |
| `/init` | Scaffold a `CLAUDE.md` for the current repo |
| `/clear` | Reset the conversation (forget context) |
| `/compact` | Compress history (keeps a summary, saves tokens) |
| `/model` | Switch model: Sonnet / Opus / Haiku |
| `/cost` | Show token spend and session cost |
| `/review` | Review the working-tree diff |
| `/agents` · `/mcp` · `/hooks` | Manage subagents · MCP servers · hooks |
| `/memory` | Open the memory editor |
| `/permissions` | Allow / deny tools per project |
| `/doctor` | Diagnose env, auth, and integrations |
| `/exit` | Leave the session (Ctrl-D works too) |

Forgot one? `/help` is one keystroke away.

<!--
SPEAKER NOTES — slide 7 (slash commands, 1 min)
- Don't read the table. Call out the 4 you'll use today: /init, /model, /review, /clear.
-->

---

<!-- _class: tpl-show -->

## Reference · Common mistakes

- Copying Claude's reply verbatim — the rubric penalises this.
- Treating Review as optional.
- Using PowerShell on Windows — move to WSL2 (see `student-guide.md`).

<!--
SPEAKER NOTES — slide 8 (common mistakes, 30 sec)
- Flag the "verbatim copy" trap now — it costs students points later.
Instructor cues:
- Hard-cap this block at 20 min. Mindset only — no live installs.
- Open from Claude Code on a known repo, not a slide.
- Broken environment? Pair the student. Move on.
-->

---

<!-- _class: tpl-show -->

## Live demo · "Read this repo" (5 min)

Watch. Don't type yet.

1. Open this repo in your IDE; run `git status` (clean) + `python3 --version` / `node --version` (green).
2. Paste the prompt verbatim:

```text
List the top-level files and tell me what kind of repository this is.
```

3. Claude reads the tree → narrates "workshop repo: slides + exercises + skills".
4. While it responds, narrate the **5-step loop** out loud.

**Success signal**: Claude names `slides/`, `exercises/`, and `skills/` without you opening them.

<!--
SPEAKER NOTES — slide 9 (demo, 5 min)
- Project this terminal full-screen, font ≥ 18pt.
- If Claude says something wrong, DO NOT correct it silently — narrate "see, this is why we review".
- Backup plan if Claude is slow: switch to /cost and show the token spend.
-->

---

<!-- _class: tpl-try -->

## Your turn · Verify + name the loop (8 min)

**Exercise**: [`exercises/part-01/README.md`](../exercises/part-01/README.md)

**Step 1** — capture your environment:

```bash
mkdir -p module-01
{ python3 --version; node --version; git --version; } > module-01/environment.txt
```

**Step 2** — paste into Claude Code, then **rewrite the reply in your own words** into `module-01/loop-notes.md`:

```text
In one short paragraph (≤ 6 sentences), explain the loop:
Plan → Implement → Test → Review → Commit.
End with one sentence on why skipping Review is the most common failure mode.
```

**Success signal**: `module-01/` contains both files; the notes name all 5 steps in order.

<!--
SPEAKER NOTES — slide 10 (hands-on, 8 min)
- Walk the room. Catch students copy-pasting Claude verbatim — that's the rubric trap.
- If pre-work was skipped, pair them with a neighbour; no live installs in this block.
- 2-min warning at the 6-min mark.
-->

---

<!-- _class: tpl-done -->

## Done & next (1 min)

**Definition of done**

- [ ] `module-01/environment.txt` — three version strings.
- [ ] `module-01/loop-notes.md` — names all 5 steps, **in your own words**.

**Next** — we apply step 1 (**Plan**) by writing prompts a Tech Lead would sign off on.
**Module 2 — Prompting Like a Tech Lead.**

<!--
SPEAKER NOTES — slide 11 (wrap, 1 min)
- Show the DoD on screen for a full 30 seconds.
- Bridge in one sentence — don't over-explain Module 2 yet.
-->

<!-- polish-log
2026-05-28 · feature 005 follow-up — instructor-pacing shape.
Flow: cover → welcome/course → instructor → Anthropic & models → theory loop
      → 3 reference slides (surfaces · slash commands · mistakes/cues)
      → live demo → hands-on → done & next.
Instructor notes in HTML comments (visible in PPTX presenter view).
-->
