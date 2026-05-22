# Knowledge Quiz — Answer Key

> Instructor-only. Do not distribute before grading.

## Answers

| # | Answer | Topic / Why |
|---|:---:|---|
| Q1 | **A** | Plan → Implement → Test → Review → Commit. The five-step loop named in Module 1. |
| Q2 | **B** | Skipping Review is the dominant failure mode for AI-paired code; this is the central thesis of Module 1. |
| Q3 | **A** | GCOE = Goal · Constraints · Output format · Examples (Module 2). |
| Q4 | **C** | Vague prompts lose specificity on the *constraints* axis first — language, deps, exit codes, output format. |
| Q5 | **B** | `CLAUDE.md` is a behavior file. Every line must change Claude's output on a future prompt (Module 3). |
| Q6 | **A** | Stack · Conventions · Commands · Do-not · Glossary — see `skills/claude-md-template/SKILL.md`. |
| Q7 | **A** | Independent candidates = separate chats with fresh context. Same chat = iteration, not BoN. |
| Q8 | **A** | Correctness · Simplicity · Fit. The 3-criterion rubric in `skills/best-of-n/SKILL.md`. |
| Q9 | **B** | "Stranger's PR" framing reduces sycophancy and gets actionable findings. From `skills/code-review/SKILL.md`. |
| Q10 | **B** | Student rubric lives at `exercises/part-05/code-review-rubric.md`. The instructor grading rubric (`assessments/rubric.md`) is a separate artifact. |
| Q11 | **B** | `<type>(<scope>): <summary>` — the Conventional Commits shape, ≤ 72 chars. |
| Q12 | **B** | The branch diff is the source of truth for a PR description. The prompt or commit list alone produces hand-wavy text. |
| Q13 | **B** | Run the visual-diff loop — wireframe + render side by side, smallest patch per gap. The lift in Module 7. |
| Q14 | **B** | The constraint forces students to learn layout primitives. Component libraries hide the lift Claude is providing on the wireframe. |
| Q15 | **B** | Without `constraints.md`, Claude reliably converts a refactor into a rewrite, breaking lock-ins like public signatures and dep counts. |
| Q16 | **B** | Combining the two passes makes the docs describe the prompt instead of the diff. Always two-pass. |
| Q17 | **A** | `name` and `description` are the required frontmatter fields. See the contract at `specs/001-bootcamp-course-materials/contracts/skill.contract.md`. |
| Q18 | **B** | Project-agnostic = the body has no repo-specific paths, filenames, or framework versions. The skill must drop into a fresh repo. |
| Q19 | **A** | Security · Observability · Deployment · Runbooks · Rollback. The five axes in `skills/production-readiness-review/SKILL.md`. |
| Q20 | **B** | The point of the report is the **decision**. Without a verdict, the rest is description without commitment. |

## Scoring

- 2 points per correct answer.
- Maximum: 40 points.
- Convert to percentage: `(raw / 40) × 100`.
- Quiz contributes to total: `quiz% × 0.40`.

## Common mis-answers (for instructor coaching)

- **Q5 → A**: students conflate `CLAUDE.md` with `README.md`. Reinforce: behavior, not documentation.
- **Q7 → D**: students think different prompts = independent. Wrong: same prompt, fresh context.
- **Q10 → A**: students confuse student rubric with grading rubric. The two-rubrics distinction is explicit in Module 5.
- **Q14 → A**: a plausible distractor. The real reason is pedagogical — see explanation above.
- **Q16 → A**: token cost is real but secondary; the real reason is doc quality.
