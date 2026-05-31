# Visual Diff — wireframe vs. render-final

Comparing `wireframe.png` (target) against the rendered Flask dashboard. Gaps in
priority order; each with the smallest patch.

> Note: `render-final.png` has since been **updated to the corrected render**
> (gap #1 applied). The original pre-fix render — KPIs as a horizontal top row —
> is preserved in git history.

---

## 1. KPI panel orientation — HIGH (real layout gap) — FIXED

The wireframe puts the three KPIs in a **vertical rail down the right side** of
the main area (beside the content table); the render laid them as a **horizontal
row across the top**, with the list stacked underneath.

**Smallest patch** (`static/style.css`): flip the main axis and make the KPI group
a fixed right column.

```css
main          { flex-direction: row; }                  /* was: column */
.kpi-row      { flex-direction: column; flex: 0 0 200px; order: 2; }
.kpi-card     { flex: 0 0 auto; }                        /* don't stretch tall */
.recent-panel { order: 1; }                              /* content fills the left */
```

Status: **applied** — KPIs now render as a right-hand vertical rail.

---

## 2. Header action label — LOW (likely intentional)

Wireframe button reads **"Primary Action"**; render reads **"+ New Note"**.

**Smallest patch** (`app.py`, button text): `+ New Note` → `Primary Action`.

Recommendation: **keep "+ New Note"** — "Primary Action" is just the wireframe
placeholder, and the concrete label is the better real UI. Not applied.

---

## 3. List section heading — LOW (likely intentional)

Wireframe labels the list region **"Table"**; render labels it **"Recent items"**.

**Smallest patch** (`app.py`, `<h2>`): `Recent items` → `Table`.

Recommendation: **keep "Recent items"** — same placeholder-vs-real situation.
Not applied.

---

## 4. Footer text — LOW

Wireframe footer reads **"Footer · v1.0.0"**; render shows only **"v1.0.0"**.

**Smallest patch** (`app.py`, `<footer>`): `v1.0.0` → `Footer · v1.0.0`.

Recommendation: **render is arguably correct** — "Footer" is a wireframe region
label, not user-facing copy. Not applied.

---

## Deliberately NOT flagged as gaps

- **Sidebar position** — the wireframe diagram stacks "Sidebar" below "Main"
  (Mermaid flow layout), but the render's left vertical nav is the correct
  realization of a "Sidebar."
- **KPI labels** — both images show "KPI 1/2/3", so they match. (Separate code
  note, not a wireframe gap: `app.py` carries real labels — "Total Notes",
  "Active Tasks", "Next Due" — but the template renders `kpi.key` instead of
  `kpi.label`. Worth fixing for polish.)
