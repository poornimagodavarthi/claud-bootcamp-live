# Bootcamp Assessment — Poornima

## 1. AI-Introduced Bugs

### Bug A — `PATCH /notes/{id}` crash after concurrent delete
*Module 04 — `module-04/winner/app.py`*

- **Symptom:** A `PATCH` on a note deleted mid-handler returned a 500 error. The handler performed an early 404 guard but took no write lock. A concurrent `DELETE` caused the subsequent re-`SELECT` to return `None`, crashing `row_to_note(None)` with a `TypeError`.
- **Root cause:** Claude made an implicit boundary assumption—that the row exists after an initial check—without re-validating the data after the write operation.
- **Fix:** Check `cur.rowcount` after the `UPDATE` and return a clean 404 if it is 0.
- **Detection:** The **code-review skill** flagged the unguarded second `SELECT` and the potential `dict(None)` crash during the module-05 review.

### Bug B — Dashboard KPIs rendered in wrong layout
*Module 07 — `static/style.css`*

- **Symptom:** The wireframe specified a vertical KPI rail on the right, but Claude rendered them as a horizontal row across the top.
- **Root cause:** Claude defaulted to a standard dashboard pattern instead of following the specific spatial layout defined in the wireframe.
- **Fix:** Update `static/style.css` to use `flex-direction: row` on the main container and fix the KPI width to create a vertical sidebar.
- **Detection:** **Manual visual review** comparing `render-final.png` against the `wireframe.png`. Automated tests passed because the elements existed, but the layout was logically incorrect.

---

## 2. Rubric Analysis

Based on `code-review-rubric.md` and the Notes API project:

- **Item that earned its place:** **1. None / empty propagation**. This directly caught the High-Severity crash in Module 04 where a missing row after a concurrent delete wasn't handled. In Actimize policy management, null fields are the primary cause of rule failures; this check is essential.
- **Item to drop:** **6. Numeric and collection boundaries**. While mathematically sound, zero-division or negative offsets never surfaced as real issues in this CRUD-heavy project. It feels like lower-value overhead for this domain.
- **Item to add:** **Authentication & Authorization**. The Module 10 report identified the lack of auth as the biggest security risk. A rubric for AI code must verify that destructive operations (POST, PATCH, DELETE) are guarded by security checks.

---

## 3. Carry-over Skill

**Top Skill for Monday Morning: `best-of-n`**

In my day job as a Policy Rule expert, this replaces the subjective process of drafting variations of a business strategy. By generating three independent candidate implementations for an Actimize rule and scoring them against a rubric of Correctness, Simplicity, and Fit, I can provide business teams with a "winner" that is optimized for both accuracy and long-term auditability. This systematic approach ensures that the chosen rule logic is the most robust version possible before it enters production.

---

## 4. Constraint Discipline

The constraint discipline shifted how I approach rule optimization by forcing me to define "safety boundaries" upfront. In my day job, this means I will explicitly constrain Claude with rules like "do not alter core threshold values" and "preserve exact alert-reason outputs." This ensures the AI simplifies boolean logic without hallucinating changes to the underlying business strategy. This proactive bounding reduces the time spent on "correction loops" and increases the reliability of AI-generated policy modifications.
