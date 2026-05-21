# Code Review Reflection

> Worth **20%** of the final score. Length: 400–700 words. Submit as `assessments/reflection.md`.

## Prompt

Write a reflection essay covering all of the following:

### 1. Two AI-introduced bugs you encountered

Pick two bugs Claude generated for you during the workshop (in your own modules, not the seeded ones from `BUGS.md`). For each:

- **Symptom**: how did the bug manifest?
- **Root cause**: in one sentence, why did Claude produce it? (e.g., implicit boundary assumption, silent fallback, wrong default.)
- **Fix**: the smallest patch that resolved it.
- **Detection**: which of these caught it — your test suite, the `code-review` skill, manual review, runtime?

### 2. Your personal Code Review Rubric

You wrote one in Module 5 (`exercises/part-05/code-review-rubric.md`). Tell us:

- Which item on the rubric **earned its place** during the day — i.e., it caught a real issue?
- Which item are you considering **dropping**, and why?
- Which item is **missing** that you'd add tomorrow?

### 3. The carry-over question

Of the 10 skills shipped with this repo, name the **one** you will reach for first on Monday morning, and explain in 2–3 sentences which workflow in your day job it replaces.

### 4. A constraint that changed your mind

During Module 8 you wrote `constraints.md` *before* prompting Claude. In 2–3 sentences: did the constraint discipline change how you'll work day-to-day? Be specific — vague answers ("yes, very much") score zero.

## Format

- Markdown.
- 400–700 words total (the grader will count).
- Use H2 (`##`) for each of the four sections above.

## Definition of done

- [ ] Four H2 sections, in order: bugs · rubric · carry-over · constraint.
- [ ] Both bugs are real (graders will sanity-check against your `module-XX/` deliverables).
- [ ] The rubric reflection names specific items from your own `code-review-rubric.md`.
- [ ] The carry-over skill is named exactly (e.g., `code-review`, `best-of-n`).
- [ ] Word count: 400–700.

## Anti-patterns

- Recounting the day chronologically. This is reflection, not summary.
- Generic praise of AI tooling.
- "I learned a lot" with no specifics.
- Bugs that don't appear anywhere in your submission.
