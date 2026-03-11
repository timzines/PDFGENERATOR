# PDF Template Rules — AI Influencer Accelerator

All PDFs produced under the AI Influencer Accelerator brand **must** follow
these rules exactly. No exceptions. The design is based on the original
Canva-designed PDFs.

---

## 1. Document Dimensions & Format

| Property       | Value                                      |
|----------------|--------------------------------------------|
| Page size      | **1440 × 810 px** (16:9 landscape)         |
| Orientation    | Landscape                                  |
| Color mode     | RGB                                        |
| Export format  | PDF (WeasyPrint HTML/CSS → PDF)            |
| Resolution     | 200 DPI for embedded raster elements       |

---

## 2. Color Palette

### Cover & TOC Pages (Dark Theme)
| Role               | Hex / Value                          | Usage                              |
|--------------------|--------------------------------------|------------------------------------|
| Cover Background   | `#1a1b1f`                            | Dark near-black base               |
| Cover Gradient     | Radial from `#3d3036` → `#1a1b1f`   | Subtle warm dark gradient          |
| TOC Gradient       | Linear `#5f4657` → `#1a1b1f`        | Dark mauve to black                |
| TOC Item BG        | `rgba(80, 55, 65, 0.6)`             | Semi-transparent pill backgrounds  |
| Cover Text         | `#ffffff`                            | Title text                         |
| Cover Muted        | `#999999`                            | Subtitle text                      |
| Cover Brand Border | `#555555`                            | Pill border around brand name      |

### Content Pages (Dark Theme — matches Cover/TOC)
| Role               | Hex / Value                          | Usage                              |
|--------------------|--------------------------------------|------------------------------------|
| BG Base            | `#1a1b1f`                            | Dark near-black base (same as cover) |
| BG Light           | `#242529`                            | Slightly lighter dark              |
| BG Gradient        | Radial from `#3d3036` → `#1a1b1f`   | Same warm dark gradient as cover   |
| Content Box BG     | `rgba(80, 55, 65, 0.6)`             | Semi-transparent dark panels       |
| Box Text           | `#e8d5dc`                            | Light warm body text               |
| Header Text        | `#ffffff`                            | Section header primary color       |
| Header Fade        | `#c49a85`                            | Section header last-word fade      |
| Sub-header         | `#ffffff`                            | Bold white within boxes            |
| Footer Text        | `#b0a0a5`                            | Muted light footer text            |
| Good Example       | `#7dba6d` border, `#c8e6c0` text    | Green-tinted examples              |
| Bad Example        | `#c9665a` border, `#eaaca5` text    | Red-tinted examples                |
| Panel BG           | `rgba(90, 60, 68, 0.5)`             | Inner highlight panels             |

> **IMPORTANT:** The old rose/mauve content page theme (`#d4b6be`, `#c7a5b2`, `#a07d83`) is
> **DEPRECATED and must NEVER be used**. ALL pages (cover, TOC, and content) use the same
> dark theme. Do not revert to the pink/rose palette under any circumstances.

---

## 3. Typography

| Element              | Font Family         | Weight    | Size (px) | Style       | Color         | Case       |
|----------------------|---------------------|-----------|-----------|-------------|---------------|------------|
| Cover Title          | Helvetica / Arial   | Bold 700  | 44        | Normal      | `#ffffff`     | Title Case |
| Cover Subtitle       | Helvetica / Arial   | Regular   | 16        | Normal      | `#999999`     | Sentence   |
| Section Header       | Helvetica / Arial   | Bold 700  | 32        | **Italic**  | `#ffffff`     | ALL CAPS   |
| Header Last Word     | Helvetica / Arial   | Bold 700  | 32        | **Italic**  | `#c49a85`     | ALL CAPS   |
| Sub-Header           | Helvetica / Arial   | Bold 700  | 14.5      | Normal      | `#ffffff`     | Title Case |
| Body Text            | Helvetica / Arial   | Regular   | 13.5      | Normal      | `#f0e0e6`     | Sentence   |
| Bullet Points        | Helvetica / Arial   | Regular   | 13.5      | Normal      | `#f0e0e6`     | Sentence   |
| Footer               | Helvetica / Arial   | Regular   | 10        | Normal      | `#b0a0a5`     | Sentence   |
| TOC Header           | Helvetica / Arial   | Bold 700  | 36        | **Italic**  | `#ffffff`     | Title Case |
| TOC Entry            | Helvetica / Arial   | Regular   | 14        | Normal      | `#e0ccd2`     | Title Case |
| Cover Brand          | Helvetica / Arial   | Regular   | 16        | Normal      | `#cccccc`     | Title Case |

**Fallback font stack:** Helvetica Neue → Helvetica → Arial → sans-serif

---

## 4. Visual Assets

### Statue Imagery
- **Cover statue:** Right half of cover page, extracted from original Canva design (`assets/cover_statue.png`)
- **Content statue:** Small, top-right corner of content pages, ~200px height, 35% opacity (`assets/content_statue.png`)
- **Content decor:** Bottom-right decoration, ~200px height, 18% opacity (`assets/content_decor.png`)
- **Background gradient:** Pre-rendered radial gradient in dark tones matching cover (`assets/content_bg_generated.png`)

### Course Logo
- `PDF/Course Logo.png` — used on cover page next to title (48×48px, rounded corners)

---

## 5. Page Structure (Mandatory Order)

Every PDF must contain these pages **in this exact order**:

### Page 1 — Cover
- Dark background (`#1a1b1f`) with subtle warm gradient
- 3D classical statue on right half (from assets)
- Left side: platform logo (optional) + title + subtitle
- "AI Influencer Accelerator" in rounded pill/badge below
- No footer on cover page

### Page 2 — Table of Contents
- Dark gradient background (mauve → dark)
- Header: "Table Of Contents" in italic bold white
- Two-column layout with pill-shaped items
- Semi-transparent item backgrounds
- Statue visible behind (lower opacity)
- Footer present

### Pages 3–N — Content Pages
- **Dark gradient background** (same as cover — `#1a1b1f` base with warm radial gradient)
- Small statue decoration top-right (subtle)
- Dollar sign decoration bottom-right (subtle)
- Section header: italic, bold, uppercase, two-tone coloring
- Content in semi-transparent dark rounded boxes (`border-radius: 14px`)
- Two-column box layout for dense content
- Single full-width box for simpler content (max 75% width)
- Footer on every page

### Final Page — Summary / End
- Same dark gradient background as content pages
- Two-column box layout with summary points
- Brand name panel
- Footer present

---

## 6. Layout Grid & Spacing

| Property                | Value                   |
|-------------------------|-------------------------|
| Page padding            | 50px top, 60px sides    |
| Bottom margin           | 45px (above footer)     |
| Column gap (2-col)      | 20–24px                 |
| Content box padding     | 22px 24px               |
| Content box radius      | 14px                    |
| Line height (body)      | 1.65                    |
| Paragraph spacing       | 10px                    |
| Section header to body  | 25px                    |
| Bullet indent           | 18px                    |
| Bullet symbol           | `•` (disc) or `→`      |

---

## 7. Content Panels & Cards

Content is displayed inside semi-transparent dark rounded boxes:
- Background: `rgba(80, 55, 65, 0.6)`
- Border-radius: `14px`
- Internal padding: `22px 24px`
- Text color: `#e8d5dc` (light warm text)
- Sub-headers within boxes: bold white `#ffffff`

### Good / Bad Example Blocks
| Type         | Border       | Text Color | Label Text       |
|--------------|-------------|------------|------------------|
| Good Example | 3px solid `#7dba6d` | `#c8e6c0`  | "GOOD EXAMPLE:"  |
| Bad Example  | 3px solid `#c9665a` | `#eaaca5`  | "BAD EXAMPLE:"   |

- Left-border accent style (not full border)
- Italic text for example content
- Always show both when comparing approaches

### Inner Highlight Panels
- Background: `rgba(90, 60, 68, 0.5)`
- Border: `1px solid rgba(255,255,255,0.15)`
- Border-radius: `8px`
- Used for key rules, warnings, and callouts

---

## 8. Footer

**Every page except the cover must have this footer:**

```
All materials are strictly protected under AI Influencer Accelerator® rights
```

- Font: 10px, muted light (`#b0a0a5`)
- Position: absolute bottom-center of page
- Consistent on every page

---

## 9. Section Header Two-Tone Rule

Section headers use a two-tone color effect:
- **Primary words:** White `#ffffff`
- **Last word:** Faded gold-rose `#c49a85`
- All uppercase, italic, bold
- Example: **INTRO: THE ROLE OF** <span style="color:#c49a85">**REDDIT**</span>

---

## 10. Content Writing Rules

1. **Direct tone** — no fluff, no filler, no motivational padding
2. **Short paragraphs** — max 3–4 lines per paragraph
3. **Imperative voice** — "Do X. Never do Y."
4. **Section = one concept** — each page covers one idea
5. **Bullet points > paragraphs** when listing steps or rules
6. **Bold key terms** on first use in a section
7. **No emojis in body text** — emojis only in quoted examples
8. **Examples are mandatory** — every rule must have a good/bad example where applicable
9. **Page count**: 12–18 pages per PDF (cover + TOC + content + summary)
10. **Text alignment**: Justified within content boxes

---

## 11. File Naming Convention

```
[Topic-Name-Hyphenated].pdf
```

Examples:
- `AI-Influencer-Method-Free-Training.pdf`
- `Reddit-SOP.pdf`
- `TikTok-SOP.pdf`
- `Instagram-Threads-Secret-Strategy.pdf`

---

## 12. JSON Content Schema

Each PDF is generated from a JSON config file in `content/`:

```json
{
  "title": "PDF Title",
  "subtitle": "Subtitle text",
  "output_filename": "My-PDF.pdf",
  "logo": "Course Logo.png",
  "sections": [
    {
      "header": "Section Title",
      "blocks": [
        {"type": "text", "content": "Paragraph text..."},
        {"type": "subheader", "content": "Sub-header text"},
        {"type": "bullets", "items": ["Item 1", "Item 2"], "bullet": "•"},
        {"type": "good_example", "content": "Good example text"},
        {"type": "bad_example", "content": "Bad example text"},
        {"type": "panel", "title": "Panel Title", "content": "Panel content"},
        {"type": "two_column", "left": [...blocks], "right": [...blocks]}
      ]
    }
  ],
  "summary_points": ["Point 1", "Point 2"]
}
```

---

## 13. Template Checklist (Before Export)

- [ ] Page size is 1440 × 810 landscape
- [ ] Cover page has statue, title, subtitle, brand badge
- [ ] Table of Contents is page 2 with pill-shaped items
- [ ] Content pages use dark gradient background (same as cover, NOT rose/pink)
- [ ] Section headers are italic, uppercase, two-tone colored
- [ ] Content boxes are semi-transparent dark rounded panels
- [ ] Body text is light warm `#e8d5dc` on dark boxes
- [ ] Footer appears on every page except cover
- [ ] Good/Bad examples use left-border accent style
- [ ] Statue decoration appears subtly on content pages
- [ ] File name follows hyphenated convention
- [ ] Total pages between 12–18
- [ ] No spelling errors
- [ ] All decorative assets are properly positioned
