# Contract: Build Pipeline (`slides/deploy-pptx.sh`)

**Feature**: Slide Decks That Shine
**Branch**: `003-slide-wow-polish`
**Date**: 28 May 2026

What the build pipeline MUST keep guaranteeing after this feature lands. The script is modified, not replaced.

---

## Inputs (post-feature)

| Input | Source | Notes |
|---|---|---|
| Intermediate decks | `slides/part-*.md` | Unchanged. Declare `theme: default`. |
| Beginner decks | `slides/beginner/part-*.md` | Modified. Declare `theme: wow-beginner`. |
| Custom theme(s) | `slides/themes/*.css` | NEW input. Auto-discovered. |
| Bundled fonts | `slides/themes/fonts/*.woff2` | NEW. Referenced by theme via relative `@font-face`. |
| Bundled icons | `slides/themes/icons/*.svg` | NEW. Referenced by deck Markdown via relative `<img src="../themes/icons/...">` or by theme via `url(...)`. |
| Per-module SVG visuals | `slides/beginner/assets/*.svg` | NEW. Referenced by their owning deck via relative path. |

---

## Required script change (single, backward-compatible)

The CLI invocation MUST add `--theme-set` if `slides/themes/` exists and contains at least one `.css` file.

Pseudocode delta (review-only; exact patch is a task in `/speckit.tasks`):

```bash
THEME_DIR="$SLIDES_DIR/themes"
THEME_ARGS=()
if [ -d "$THEME_DIR" ] && compgen -G "$THEME_DIR/*.css" > /dev/null; then
  THEME_ARGS=(--theme-set "$THEME_DIR")
fi

# every "${MARP[@]}" invocation gains "${THEME_ARGS[@]}"
"${MARP[@]}" "${THEME_ARGS[@]}" --allow-local-files --pptx -o "$out_pptx/${base}.pptx" "$deck"
```

`--allow-local-files` was already present, so bundled fonts/icons/SVGs load without additional flags.

---

## Outputs (unchanged shape)

| Output | Path | Condition |
|---|---|---|
| PPTX | `slides/dist/pptx/[beginner/]<deck>.pptx` | Always |
| PDF | `slides/dist/pdf/[beginner/]<deck>.pdf` | `--pdf` or `--all` |
| HTML | `slides/dist/html/[beginner/]<deck>.html` | `--html` or `--all` |

The `dist/` tree shape, sub-folder split (`beginner/` vs. intermediate flat), and file naming are unchanged from pre-feature behavior.

---

## Guarantees (post-feature)

1. **Backward compatibility**: Running the script with no flags on the unchanged intermediate decks MUST produce byte-similar output to pre-feature (modulo Marp version drift). No intermediate deck need declare `theme: wow-beginner` or otherwise opt in.
2. **Exit code**: 0 on success; non-zero on any deck failing to render (existing behavior — `set -euo pipefail`).
3. **No new mandatory dependency**: The script MUST NOT require any tool not already required by the pre-feature script (Marp via npx or global, Chromium auto-fetched by Marp).
4. **No build-time network calls beyond Marp's existing Chromium fetch**: All fonts, icons, and SVG assets are bundled and referenced by relative paths.
5. **No new flags exposed to users**: `--help` text gains no new entry; `--theme-set` is internal-only.
6. **Idempotency**: Re-running the script produces the same output for the same inputs (modulo PPTX/PDF timestamp metadata — existing behavior).
7. **Performance**: Wall-clock time on a clean checkout MUST be ≤ 1.5 × pre-feature baseline (SC-006). Baseline recorded once in `specs/003-slide-wow-polish/baseline-build-time.txt`.

---

## Negative guarantees (what the script MUST NOT do)

- MUST NOT install npm packages globally as a side-effect.
- MUST NOT write outside `slides/dist/`.
- MUST NOT silently ignore a missing deck (one missing file is a build failure).
- MUST NOT fetch fonts from Google Fonts, Adobe Fonts, or any other remote source at build time.
- MUST NOT require `CHROME_PATH` to be set when Marp's bundled Chromium is available (existing behavior preserved).

---

## Out-of-script verification (companion contract)

The new helper `scripts/check-slide-overflow.sh` (added as a separate task) provides:

- **Input**: `slides/dist/html/` (built by `deploy-pptx.sh --html` or `--all`).
- **Output**: exit code 0 if 0 slides overflow; non-zero with a list of `<deck>:<slide-number>` pairs otherwise.
- **Used by**: maintainer pre-merge check; future CI; SC-007 verification.

The two scripts together form the build-and-verify contract for this feature.
