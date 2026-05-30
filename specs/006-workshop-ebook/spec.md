# Feature Specification: Workshop Markdown Ebook

**Feature Branch**: `006-workshop-ebook`

**Created**: 29 May 2026

**Status**: Draft

**Input**: User description: "I want to create a markdown ebook of the workshop"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read the whole workshop as one self-contained ebook (Priority: P1)

A learner who cannot attend (or wants to revisit) the live bootcamp opens a single Markdown ebook and reads the entire course front to back — overview, all 11 parts, exercises, and closing material — without needing to jump between the slides, exercises, and guide files scattered across the repository.

**Why this priority**: This is the core value of the feature. A consolidated, ordered, readable ebook is the minimum that delivers a usable product. Everything else is enhancement.

**Independent Test**: Open the generated ebook file in any Markdown reader and confirm it contains, in correct order, a title page, table of contents, and every part (01–11) with coherent narrative flow. Reading start-to-finish requires no other file.

**Acceptance Scenarios**:

1. **Given** the workshop source content exists in the repository, **When** the ebook is produced, **Then** a single Markdown ebook is created containing a title page, a table of contents, and all 11 parts in sequential order.
2. **Given** the generated ebook, **When** a reader follows the table of contents links, **Then** each link resolves to the correct chapter within the same document.
3. **Given** a part contains slide content not meant for prose (e.g., presenter notes, slide directives), **When** that part is included in the ebook, **Then** the content reads as continuous prose rather than disconnected slide fragments.

---

### User Story 2 - Practice with the hands-on exercises inside the ebook (Priority: P2)

A self-paced reader wants to do the 10 hands-on projects while reading, so each chapter includes the matching exercise instructions (and optionally a reference solution) right where the project is introduced.

**Why this priority**: The bootcamp's value is hands-on. Including exercises makes the ebook a complete self-study resource, but the ebook is still useful for reading without them, so this ranks below P1.

**Independent Test**: Open the ebook, navigate to any part 01–10, and confirm the corresponding exercise brief appears in or adjacent to that chapter, with steps the reader can follow independently.

**Acceptance Scenarios**:

1. **Given** parts 01–10 each have an associated exercise, **When** the ebook is produced, **Then** each of those chapters includes the exercise instructions for that part.
2. **Given** a reader finishes an exercise, **When** they look for the reference solution, **Then** the solution is reachable from that chapter (inline appendix or clearly labeled section).

---

### User Story 3 - Front matter, navigation, and supporting material (Priority: P3)

A reader expects an ebook to feel complete: cover/title page with course metadata, an introduction explaining how to use the book, prerequisites/pre-work, and back matter such as the skills library overview and next-steps/certification info.

**Why this priority**: These elements raise polish and completeness but are not required for the ebook to deliver its primary reading value.

**Independent Test**: Open the ebook and confirm it opens with a title page and an introduction, and ends with back matter (skills overview, certification/next steps), distinct from the core part chapters.

**Acceptance Scenarios**:

1. **Given** course metadata exists (title, instructor, format, audience, prerequisites), **When** the ebook is produced, **Then** the title page and introduction reflect that metadata.
2. **Given** the workshop includes a skills library and closing/exam material, **When** the ebook is produced, **Then** that material appears as back matter after the part chapters.

---

### Edge Cases

- What happens when source files contain presentation-only syntax (slide separators, directives, speaker notes)? The ebook must present clean prose and must not leak raw presentation markup.
- What happens when a part references another file by relative path (e.g., a link to an exercise)? Such references must either resolve within the ebook or be rewritten so they do not become broken links for a reader who only has the ebook.
- What happens when images or diagrams are embedded? They must render in a standard Markdown reader or be represented in a way that does not break the reading flow.
- What happens when the underlying workshop content changes after the ebook is produced? There must be a clear, repeatable way to regenerate the ebook so it stays in sync.
- What happens with duplicated headings across parts (e.g., every part has "Summary")? Heading structure and any anchors must remain unambiguous within the single document.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The ebook MUST be a Markdown deliverable that consolidates the workshop content into a coherent reading experience covering all 11 parts in sequential order (01 → 11).
- **FR-002**: The ebook MUST include front matter consisting of a title page (course title, instructor, format, and edition/date) and an introduction describing the course and how to use the book.
- **FR-003**: The ebook MUST include a table of contents that lists all chapters and links to their locations within the document.
- **FR-004**: Each part chapter MUST present its content as readable prose, with presentation-only artifacts (slide separators, presenter notes, rendering directives) removed or converted so they do not appear as raw markup.
- **FR-005**: For parts that have an associated hands-on exercise (parts 01–10), the ebook MUST include the exercise instructions within or adjacent to the corresponding chapter.
- **FR-006**: The ebook MUST include back matter covering the skills library overview and the closing/certification/next-steps material.
- **FR-007**: Internal cross-references and links MUST resolve correctly for a reader who has only the ebook, or be rewritten so they do not appear as broken links.
- **FR-008**: The ebook MUST preserve a consistent and unambiguous heading hierarchy so that navigation and the table of contents work within a single document despite repeated section titles across parts.
- **FR-009**: The production process MUST be repeatable so the ebook can be regenerated when source workshop content changes, without manual re-authoring of the consolidated content.
- **FR-010**: The ebook MUST render correctly in a standard Markdown viewer, including any embedded images or diagrams, without exposing tool-specific syntax that breaks rendering.
- **FR-011**: Reference solutions for exercises MUST either be included as clearly labeled appendix/sections reachable from the relevant chapter, or be explicitly and intentionally excluded with that exclusion stated in the introduction.

### Key Entities *(include if feature involves data)*

- **Ebook**: The single consolidated Markdown reading deliverable, composed of front matter, ordered part chapters, and back matter.
- **Chapter**: A unit of the ebook corresponding to one workshop part (01–11), containing the instructional narrative and, where applicable, the matching exercise and solution references.
- **Front Matter**: Title page and introduction with course metadata and usage guidance.
- **Back Matter**: Supporting sections after the chapters — skills library overview and closing/certification/next-steps content.
- **Source Content**: The existing workshop materials (slide decks, exercise briefs, reference solutions, guides) that the ebook is assembled from.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reader can read the entire workshop end-to-end using only the ebook file, with zero need to open any other repository file to follow the core narrative.
- **SC-002**: 100% of the 11 parts appear in the ebook in correct sequential order, each reachable from the table of contents.
- **SC-003**: 100% of parts 01–10 include their associated exercise instructions within the ebook.
- **SC-004**: Zero raw presentation-only markup (slide separators, directives, presenter notes) appears as visible text when the ebook is viewed in a standard Markdown reader.
- **SC-005**: Zero broken internal links remain in the ebook for a reader who has only the ebook file.
- **SC-006**: Regenerating the ebook after a change to source workshop content reflects that change without manual rewriting of consolidated prose.

## Assumptions

- The ebook is assembled from the workshop's existing materials (slide decks for parts 01–11, exercise briefs, reference solutions, and the student/instructor guides) rather than newly authored from scratch.
- The primary output format is Markdown; converting to other formats (PDF, EPUB) is out of scope for this feature unless added later.
- The ebook is intended for self-paced reading and self-study, complementing — not replacing — the live bootcamp.
- A single consolidated ebook file is the primary deliverable; splitting into per-chapter files may be an internal/intermediate detail but the reader-facing experience is one continuous book.
- Reference solutions are included as back-of-chapter or appendix material so the ebook is a complete self-study resource; if any are excluded, that is stated in the introduction.
- Course metadata (title, instructor, format, audience, prerequisites) is taken from the existing repository README and guides.
