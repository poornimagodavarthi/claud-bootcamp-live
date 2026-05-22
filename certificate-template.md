# Certificate of Completion

<div align="center">

# {{WORKSHOP_TITLE}}

### Endorsed by **Packt Certification**

---

This certifies that

# {{STUDENT_NAME}}

has successfully completed

## Claude Code Bootcamp — Build 10 Real-World Projects with Claude Code in One Day

a five-hour, ten-module live workshop on AI-paired engineering with Claude Code,
covering: prompting, project context, Best-of-N, testing & self-review, Git workflows,
multimodal UI generation, refactoring, reusable skills, and production readiness.

The recipient has demonstrated mastery of the workshop's learning outcomes by:

- Passing the **Knowledge Quiz** (40% weight)
- Shipping the **Practical Task** to specification (40% weight)
- Submitting a graded **Code Review Reflection** (20% weight)

with a final weighted score of **≥ 70%** against the rubric at
`assessments/rubric.md`.

---

**Date of completion**: {{COMPLETION_DATE}}

**Instructor**: {{INSTRUCTOR_NAME}}

**Issued by**: LLM Engineering by Packt

---

*Endorsed by Packt Certification.*

</div>

---

## Placeholders

Replace the following before issuing:

| Placeholder | Default | Required |
|---|---|---|
| `{{STUDENT_NAME}}` | — | Yes |
| `{{COMPLETION_DATE}}` | The date the student passed (e.g., `30 May 2026`) | Yes |
| `{{INSTRUCTOR_NAME}}` | `Luca Berton` | Yes (default acceptable) |
| `{{WORKSHOP_TITLE}}` | `Claude Code Bootcamp — Build 10 Real-World Projects with Claude Code in One Day` | Yes (default acceptable) |

## Rendering

```bash
# 1. Replace placeholders inline (or use envsubst):
sed -e "s/{{STUDENT_NAME}}/Jane Doe/g" \
    -e "s/{{COMPLETION_DATE}}/30 May 2026/g" \
    -e "s/{{INSTRUCTOR_NAME}}/Luca Berton/g" \
    -e "s/{{WORKSHOP_TITLE}}/Claude Code Bootcamp/g" \
    certificate-template.md > /tmp/certificate.md

# 2. Render to PDF (any of):
pandoc /tmp/certificate.md -o /tmp/certificate.pdf
# or via Marp if you prefer the slide-style render:
npx --yes @marp-team/marp-cli@latest --pdf /tmp/certificate.md -o /tmp/certificate.pdf
```

## Issuance

Deliver the rendered PDF to the student through the Packt LMS message thread tied to the *Claude Code Bootcamp — 30 May 2026* assignment, alongside their final score breakdown.
