<!--
SYNC IMPACT REPORT
==================
Version change: (uninitialized template) → 1.0.0
Bump rationale: Initial ratification of the project constitution. MAJOR 1.0.0
  per semver convention for the first formally adopted version.

Modified principles: N/A (initial adoption — all 10 principles new)
Added sections:
  - Core Principles (10 principles)
  - Quality Standards
  - Authoring & Delivery Workflow
  - Governance

Removed sections: None (template placeholders fully replaced)

Templates requiring updates:
  - ✅ .specify/templates/plan-template.md — reviewed; "Constitution Check"
       gate is generic and remains compatible. No edits required.
  - ✅ .specify/templates/spec-template.md — reviewed; aligns with
       deliverable/DoD-driven principles. No edits required.
  - ✅ .specify/templates/tasks-template.md — reviewed; user-story-based
       structure is compatible with module-based deliverables. No edits required.
  - ✅ .specify/templates/checklist-template.md — reviewed; compatible.
  - ✅ .github/prompts/speckit.*.prompt.md — generic, no agent-specific
       references requiring update.
  - ✅ README.md — already aligned with title, schedule, 10-project structure,
       and assessment policy referenced by this constitution. No edits required.
  - ⚠ slides/part-09-automation.md and slides/part-10-production.md —
       filenames diverge from the requested
       part-09-skills-workflows.md / part-10-production-readiness.md;
       tracked in feature spec FR-001 + Assumptions for renaming during
       implementation, NOT a constitution-level concern.

Follow-up TODOs:
  - RESOLVED(2026-05-21): Packt endorsement language confirmed via official
    Packt Certification promotional creative for the 30 May 2026 cohort.
    Canonical brand string: "Packt Certification" (parent line:
    "LLM Engineering by Packt"). Logo assets to be supplied by Packt as a
    binary drop into a future `assets/` directory and are not blocking
    spec/plan/tasks. Tracked in specs/001-bootcamp-course-materials/spec.md
    Assumptions.
-->

# Claude Code Extended Workshop Constitution

## Core Principles

### I. Practical, Project-Based Learning (NON-NEGOTIABLE)

Every module MUST produce a concrete, learner-built artifact (CLI tool, API,
test suite, branch, dashboard, refactor + docs, skill library, readiness
report). Slides without an associated mini-project are prohibited. Theory is
admitted only in service of the project a learner is about to build.

**Rationale**: The product's premium positioning is "live build workshop, not a
slide-only course." Learners must leave with a portfolio, not notes.

### II. Standardized Module Anatomy

Every module MUST contain, in this exact taxonomy: Promise, Topics, Mini
Project, Step-by-step Lab, Suggested Claude Code Prompts, Deliverable
Checklist, Definition of Done, Review Checkpoint. Slide decks MUST also
include Title, Why this matters, Concepts, Live demo flow, Common mistakes,
Instructor notes, and Transition to next module — for a total of 14 required
sections per deck. Exercises MUST contain 9 required sections (Goal,
Scenario, Starter instructions, Claude Code prompt to use, Manual validation
steps, Expected deliverable, Definition of done, Stretch challenge,
Troubleshooting).

**Rationale**: A predictable structure lets instructors teach any module
cold and lets students self-pace. Removing or renaming sections breaks
cross-module navigation, the rubric, and the review checkpoints.

### III. Marp-Flavored Markdown for All Slides

All slide decks MUST be authored in Marp-flavored Markdown under `slides/`
and MUST build via `slides/deploy-pptx.sh` (PPTX default; PDF/HTML via
flags). No proprietary slide formats (Keynote, .pptx sources, Google Slides
links) MAY be the source of truth. Build artifacts MUST land in
`slides/dist/` and MUST be gitignored.

**Rationale**: Markdown decks are diffable, reviewable in PRs, scriptable,
and let the same source produce PPTX, PDF, and HTML. Binary slide formats
break review workflows.

### IV. Beginner-to-Intermediate Accessibility

Materials MUST assume only basic programming literacy in any one language,
Git basics, and Claude Code access. Modules MUST NOT teach programming
fundamentals, advanced compiler theory, or framework-specific deep dives
beyond what the project requires. Where multiple languages are viable
(e.g., Node.js or Python), instructions MUST work for at least one common
choice and call out alternatives explicitly.

**Rationale**: The audience is professionals adopting AI-assisted
development, not CS students. Pitching too low wastes time; pitching too
high loses the room.

### V. Build, Review, Teach in Under 30 Minutes

The repository MUST be cloneable and buildable on a clean machine with
only Node.js installed; `slides/deploy-pptx.sh` MUST self-bootstrap Marp
via `npx`. A new instructor MUST be able to clone, build, and start
teaching module 1 in under 30 minutes (SC-001). Documentation
(`README.md`, `instructor-guide.md`, `student-guide.md`) MUST be
sufficient for solo onboarding.

**Rationale**: Friction at setup destroys instructor adoption and student
trust. The repository is a product; its time-to-first-value is a feature.

### VI. Concrete, Verifiable Deliverables

Every module's Definition of Done MUST be a pass/fail checklist a student
can self-verify without instructor judgment. Every exercise's Manual
validation steps MUST be deterministic (specific commands or observable
behaviors). Vague criteria ("works well", "looks good", "feels right")
are prohibited.

**Rationale**: Self-verification scales to large cohorts and self-paced
learners and produces a defensible 70% pass threshold for certification.

### VII. No Motivational Filler

Content MUST prioritize usable teaching assets over inspirational
language. Marketing-tone copy ("unleash your potential", "AI-powered
revolution") is prohibited inside teaching materials. Each slide and
each paragraph MUST advance a Promise, Topic, Lab step, Validation, or
Checkpoint. Removing a slide or paragraph MUST be considered the default
when its purpose is unclear.

**Rationale**: The premium tier competes on density and rigor, not
enthusiasm. Filler dilutes the value proposition and burns instruction
time.

### VIII. Assessment and Certification Are First-Class

Every release MUST ship with `assessments/knowledge-quiz.md`,
`assessments/practical-task.md`, `assessments/code-review-reflection.md`,
`assessments/rubric.md`, and `assessments/answer-key.md` consistent with
the published 40% / 40% / 20% weighting and 70% pass threshold.
`certificate-template.md` MUST be issuable as a Packt Publishing
endorsed Certificate of Completion. Assessment artifacts MUST stay in
sync with module deliverables; an assessment item that no module
prepares the student for is a defect.

**Rationale**: The certification is part of the product. Detached or
stale assessments degrade the credential and the brand endorsement.

### IX. Cross-Artifact Consistency

Module titles, project names, the canonical 10-project list, timing,
prerequisites, audience, and assessment weighting MUST match across
`README.md`, slide decks, exercises, skills, assessments, and guides.
Any change to a canonical name or weighting in one place is a defect
until propagated to all places. The maintainer MUST run a consistency
check (or equivalent review) before each release.

**Rationale**: Inconsistency between the README, the slides a student
sees, and the rubric they are graded against is the most common
trust-destroying failure mode of multi-artifact courses.

### X. Minimal External Dependencies

The repository MUST NOT introduce external runtime dependencies beyond
what individual project labs strictly require. Permitted core
dependencies: Marp CLI (slide build, via npx fallback), Chromium
(Marp's PPTX/PDF export), Git, and Claude Code (external SaaS, used by
learners). New dependencies MUST be justified in writing in the
relevant module's Topics or `instructor-guide.md`. SaaS lock-in beyond
Claude Code itself is prohibited.

**Rationale**: Every added dependency is friction at setup and a future
maintenance burden. A bootcamp that breaks because of an upstream tool
change cancels real revenue.

## Quality Standards

The following standards apply to all content shipped from this repository
and are enforced at review time:

- **Clear module learning outcomes**: Each module's Promise MUST be stated
  as testable learner capabilities (verbs: build, configure, review,
  refactor, etc.), not feelings or aspirations.
- **Instructor-friendly explanations**: Slides MUST include `Instructor
  notes` and `Common mistakes` sections sufficient for a qualified
  instructor (not the author) to teach the module without external
  preparation.
- **Student-friendly exercises**: Exercises MUST be runnable from the
  starter instructions alone, with all necessary scaffolding included or
  explicitly fetched in step 1.
- **Consistent formatting**: Markdown style (heading levels, code-fence
  language tags, list style, link style) MUST be uniform within and
  across modules. Lint-equivalent review is expected at PR time.
- **Buildable slide deck structure**: All decks MUST compile under
  `slides/deploy-pptx.sh` without manual fix-up; broken builds MUST
  block release.
- **Practical examples**: Every Concept MUST be paired with at least one
  worked example, code snippet, or transcript that learners can
  reproduce.
- **Review checkpoints**: Every module MUST end with a Review Checkpoint
  the instructor uses to verify the room is ready to advance.
- **Assessment-ready outputs**: Every learner deliverable MUST be
  inspectable by the rubric without translation (i.e., the rubric refers
  to the same artifact names the labs produce).

## Authoring & Delivery Workflow

- **Source of truth**: The `main` branch is the canonical, releasable
  state. Feature branches use the `NNN-short-name` Spec Kit convention
  (e.g., `001-bootcamp-course-materials`). Direct commits to `main`
  bypassing review are prohibited for content changes spanning more
  than one module.
- **Spec Kit alignment**: Major content additions follow the Spec Kit
  flow: `/speckit.specify` → `/speckit.clarify` (when needed) →
  `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`. Per-feature
  artifacts live under `specs/NNN-short-name/`.
- **Build before merge**: A PR that touches `slides/` MUST be merged
  only after a successful run of `slides/deploy-pptx.sh` (locally or in
  CI when CI is added).
- **Schedule integrity**: The sum of module instruction times MUST equal
  240 minutes (±5 minutes); the published 5-hour schedule accounts for
  the remaining 60 minutes as breaks and Q&A. Any change to a module's
  time budget MUST be balanced against the others in the same PR.
- **Release readiness**: Before tagging a release, the maintainer MUST
  verify (a) all 10 module decks build, (b) all 10 exercise directories
  have the 9 required sections, (c) all 10 skills have the 6 required
  attributes, (d) `assessments/rubric.md` references current deliverable
  names, and (e) cross-artifact terminology is consistent.

## Governance

This constitution supersedes informal practice. When ad-hoc decisions
conflict with a principle here, the constitution wins until amended.

- **Amendment procedure**: Amendments are proposed via a PR that edits
  this file, includes an updated Sync Impact Report at the top, and
  bumps the version per the policy below. Approval requires the
  repository owner's sign-off. Amendments touching Principles I–X MUST
  also propagate to dependent templates and guides in the same PR (or
  immediately following PR tracked as a follow-up).
- **Versioning policy** (semver for governance, not for course content):
  - **MAJOR**: Backward-incompatible changes to principles or governance
    (e.g., removing a principle, changing a non-negotiable rule,
    redefining the assessment weighting).
  - **MINOR**: Adding a new principle or materially expanding existing
    guidance.
  - **PATCH**: Clarifications, wording, typo fixes, non-semantic
    refinements.
- **Compliance review**: Every release readiness check (see Authoring &
  Delivery Workflow) constitutes a constitutional compliance review.
  PRs that introduce content violating a principle MUST either be
  revised, justified with a documented exception, or paired with an
  amendment.
- **Exceptions**: Time-boxed exceptions MAY be granted by the repository
  owner and MUST be recorded in the relevant PR description with a
  remediation date. Exceptions older than the next release without
  remediation are treated as defects.
- **Runtime guidance**: Day-to-day authoring guidance lives in
  `.github/copilot-instructions.md`, `instructor-guide.md`, and
  `student-guide.md`. Those documents elaborate on this constitution
  but MUST NOT contradict it.

**Version**: 1.0.0 | **Ratified**: 2026-05-21 | **Last Amended**: 2026-05-21
