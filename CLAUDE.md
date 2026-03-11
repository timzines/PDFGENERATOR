# CLAUDE.md — Project Rules for AI Assistants

## Critical: PDF Theme Rules

**ALL PDFs use the DARK theme. There is NO pink/rose/mauve theme anymore.**

The old rose/mauve content page palette (`#d4b6be`, `#c7a5b2`, `#a07d83`, `rgba(111, 76, 83, 0.82)`)
is **PERMANENTLY DEPRECATED**. Never use these colors. Never revert to them.

The correct theme for ALL pages (cover, TOC, content, summary) is:
- Background base: `#1a1b1f` (dark near-black)
- Background gradient: radial from `#3d3036` → `#1a1b1f` → `#141519`
- Content box BG: `rgba(80, 55, 65, 0.6)` (semi-transparent dark)
- Text: `#e8d5dc` (light warm), headers `#ffffff`
- Header fade word: `#c49a85`

See `PDF_RULES.md` for the full specification. The `generate_pdf.py` constants are the
**single source of truth** for colors.

## Critical: Regeneration Rules

**When ANY template change is made (theme, layout, fonts, spacing, etc.), ALL PDFs must be regenerated.**

This means running BOTH:
1. `python generate_pdf.py` — regenerates top-level module PDFs in `output/`
2. `python generate_modules.py` — regenerates per-lesson PDFs in `output/Module X - .../`

**Never regenerate only one set.** Both scripts use the same `generate_pdf()` function from
`generate_pdf.py`, but they produce different output files. Forgetting to run `generate_modules.py`
after a template change will leave the per-lesson PDFs on the old design.

## Project Structure

- `generate_pdf.py` — Core PDF generator (HTML/CSS → PDF via WeasyPrint). Contains all design
  constants, colors, and the `generate_pdf()` function.
- `generate_modules.py` — Splits module JSON configs into individual per-lesson PDFs in subfolders.
  Imports `generate_pdf()` from `generate_pdf.py`.
- `content/` — JSON content files for each module.
- `output/` — Generated PDFs. Top-level are full-module PDFs. Subfolders contain per-lesson PDFs.
- `PDF_RULES.md` — Complete design specification. Must be kept in sync with `generate_pdf.py`.
- `assets/` — Images (statues, decorations, generated backgrounds).

## Common Pitfalls to Avoid

1. **Theme regression** — Do NOT reference old pink/rose colors from PDF_RULES.md history or git
   history. The dark theme is final.
2. **Partial regeneration** — Always run both `generate_pdf.py` AND `generate_modules.py` after
   any template change.
3. **PDF_RULES.md drift** — If you change colors/layout in `generate_pdf.py`, update `PDF_RULES.md`
   to match. The code is the source of truth but the docs must stay in sync.
4. **Stale per-lesson PDFs** — The per-lesson PDFs in module subfolders are generated separately
   from the top-level module PDFs. Check timestamps if something looks wrong.
