#!/usr/bin/env python3
"""
AI Influencer Accelerator — PDF Generator v2
=============================================
Generates branded PDFs matching the original Canva design:
  - Dusty rose/mauve gradient content pages
  - Dark cover & TOC pages with statue imagery
  - Semi-transparent dark content panels with rounded corners
  - Italic two-tone section headers
  - Statue and dollar-sign decorative overlays

Uses WeasyPrint (HTML/CSS → PDF) for professional layout.

Usage:
    python generate_pdf.py                          # generates the template example
    python generate_pdf.py --config my_content.json # generates from a JSON content file
"""

import base64
import json
import os
import sys
from io import BytesIO
from pathlib import Path

from jinja2 import Template
from PIL import Image, ImageDraw, ImageFilter
from weasyprint import HTML

# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_DIR = BASE_DIR / "output"

# ---------------------------------------------------------------------------
# DESIGN CONSTANTS
# ---------------------------------------------------------------------------
PAGE_W = 1440
PAGE_H = 810

# Colors (from original Canva PDFs)
COVER_BG = "#1a1b1f"
COVER_BG_GRADIENT = "radial-gradient(ellipse at 30% 50%, #3d3036 0%, #1a1b1f 50%, #141519 100%)"
TOC_BG_GRADIENT = "linear-gradient(180deg, #5f4657 0%, #1a1b1f 40%, #141519 100%)"

# Content page rose/mauve palette
CONTENT_BG_BASE = "#c7a5b2"
CONTENT_BG_LIGHT = "#d4b6be"
CONTENT_BG_GRADIENT = "radial-gradient(ellipse at 50% 50%, #d4b6be 0%, #c7a5b2 40%, #a07d83 100%)"

# Content box (semi-transparent dark rose)
BOX_BG = "rgba(111, 76, 83, 0.82)"
BOX_BG_SOLID = "#6f4c53"

# Text colors
TEXT_WHITE = "#ffffff"
TEXT_LIGHT = "#e8d5dc"
TEXT_DARK = "#2a1a1f"
TEXT_MUTED_DARK = "#4a3038"
TEXT_MUTED_LIGHT = "#999999"
HEADER_FADE = "#c49a85"  # The faded last-word color in headers

FOOTER_TEXT = "All materials are strictly protected under AI Influencer Method\u00AE rights"
BRAND_NAME = "AI Influencer Method"


# ---------------------------------------------------------------------------
# ASSET HELPERS
# ---------------------------------------------------------------------------

def img_to_data_uri(path):
    """Convert image file to data URI for embedding in HTML."""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = Path(path).suffix.lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext.lstrip("."), "image/png")
    return f"data:{mime};base64,{data}"


def pil_to_data_uri(img, fmt="PNG"):
    """Convert PIL Image to data URI."""
    buf = BytesIO()
    img.save(buf, format=fmt)
    data = base64.b64encode(buf.getvalue()).decode()
    mime = "image/png" if fmt == "PNG" else "image/jpeg"
    return f"data:{mime};base64,{data}"


def generate_content_bg():
    """Generate dusty rose gradient background image."""
    w, h = PAGE_W, PAGE_H
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)

    # Radial gradient: center is lighter, edges are darker rose
    cx, cy = w // 2, h // 2
    max_r = ((w/2)**2 + (h/2)**2) ** 0.5

    # Base colors
    center = (212, 182, 190)  # #d4b6be
    edge = (160, 125, 131)    # #a07d83
    mid = (199, 165, 178)     # #c7a5b2

    for y_pos in range(h):
        for x_pos in range(w):
            dist = ((x_pos - cx)**2 + (y_pos - cy)**2) ** 0.5
            t = min(dist / max_r, 1.0)
            if t < 0.5:
                t2 = t / 0.5
                r = int(center[0] + (mid[0] - center[0]) * t2)
                g = int(center[1] + (mid[1] - center[1]) * t2)
                b = int(center[2] + (mid[2] - center[2]) * t2)
            else:
                t2 = (t - 0.5) / 0.5
                r = int(mid[0] + (edge[0] - mid[0]) * t2)
                g = int(mid[1] + (edge[1] - mid[1]) * t2)
                b = int(mid[2] + (edge[2] - mid[2]) * t2)
            draw.point((x_pos, y_pos), fill=(r, g, b))

    return img


def get_content_bg_uri():
    """Get or create content background as data URI."""
    cache_path = ASSETS_DIR / "content_bg_generated.png"
    if not cache_path.exists():
        img = generate_content_bg()
        img.save(str(cache_path))
    return img_to_data_uri(str(cache_path))


def get_asset_uri(name):
    """Get asset as data URI, return empty string if missing."""
    path = ASSETS_DIR / name
    if path.exists():
        return img_to_data_uri(str(path))
    return ""


# ---------------------------------------------------------------------------
# HTML/CSS TEMPLATES
# ---------------------------------------------------------------------------

CSS_BASE = """
@page {
    size: 1440px 810px;
    margin: 0;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
}

.page {
    width: 1440px;
    position: relative;
    page-break-after: always;
}

.page:last-child {
    page-break-after: auto;
}

/* Summary page always starts on a new page */
.page-summary {
    page-break-before: always;
}

/* ---- COVER PAGE ---- */
.page-cover {
    background: #0f1013;
    position: relative;
    overflow: hidden;
    height: 810px;
}

/* Atmospheric gradient overlay on cover */
.cover-gradient-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background:
        radial-gradient(ellipse at 25% 50%, rgba(90, 50, 65, 0.5) 0%, transparent 60%),
        radial-gradient(ellipse at 75% 40%, rgba(60, 35, 50, 0.4) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 100%, rgba(40, 25, 35, 0.6) 0%, transparent 50%),
        linear-gradient(180deg, #1a1b1f 0%, #0f1013 100%);
    z-index: 0;
}

/* Subtle decorative line accents on cover */
.cover-accent-line {
    position: absolute;
    left: 60px;
    top: 100px;
    width: 3px;
    height: 200px;
    background: linear-gradient(180deg, #c49a85 0%, transparent 100%);
    z-index: 3;
    border-radius: 2px;
}

.cover-accent-line-bottom {
    position: absolute;
    left: 80px;
    bottom: 80px;
    width: 120px;
    height: 1px;
    background: linear-gradient(90deg, rgba(196,154,133,0.6) 0%, transparent 100%);
    z-index: 3;
}

.cover-left {
    position: absolute;
    left: 0;
    top: 0;
    width: 50%;
    height: 100%;
    padding: 120px 40px 80px 85px;
    z-index: 4;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.cover-logo-wrap {
    position: absolute;
    right: -20px;
    top: 0;
    width: 55%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
}

.cover-logo-img {
    height: 92%;
    width: auto;
    max-width: 95%;
    object-fit: contain;
    opacity: 0.85;
    filter: drop-shadow(0 0 60px rgba(90, 50, 65, 0.4));
}

/* Glow behind statue */
.cover-glow {
    position: absolute;
    right: 100px;
    top: 50%;
    transform: translateY(-50%);
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(196,154,133,0.12) 0%, transparent 70%);
    z-index: 1;
    border-radius: 50%;
}

/* Subtle geometric design behind the logo */
.cover-logo-design {
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    width: 520px;
    height: 520px;
    z-index: 1;
}

.cover-logo-ring {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(196,154,133,0.08);
}

.cover-logo-ring-1 {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 500px;
}

.cover-logo-ring-2 {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 380px;
    height: 380px;
    border-color: rgba(196,154,133,0.06);
}

.cover-logo-ring-3 {
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 260px;
    height: 260px;
    border-color: rgba(196,154,133,0.04);
}

/* Decorative arc lines */
.cover-logo-arc {
    position: absolute;
    border-radius: 50%;
    border: 1px solid transparent;
}

.cover-logo-arc-1 {
    top: 10%;
    right: 5%;
    width: 200px;
    height: 200px;
    border-top-color: rgba(196,154,133,0.1);
    border-right-color: rgba(196,154,133,0.06);
    transform: rotate(-30deg);
}

.cover-logo-arc-2 {
    bottom: 15%;
    left: 10%;
    width: 160px;
    height: 160px;
    border-bottom-color: rgba(196,154,133,0.08);
    border-left-color: rgba(196,154,133,0.04);
    transform: rotate(20deg);
}

/* Small decorative dots */
.cover-logo-dot {
    position: absolute;
    width: 4px;
    height: 4px;
    border-radius: 50%;
    background: rgba(196,154,133,0.15);
}

.cover-logo-dot-1 { top: 20%; right: 15%; }
.cover-logo-dot-2 { bottom: 25%; left: 20%; }
.cover-logo-dot-3 { top: 60%; right: 8%; width: 3px; height: 3px; background: rgba(196,154,133,0.1); }

.cover-tag {
    font-size: 11px;
    font-weight: 600;
    color: #c49a85;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 8px;
}

.cover-module-label {
    font-size: 13px;
    font-weight: 500;
    color: rgba(196,154,133,0.5);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    margin-bottom: 4px;
}

.cover-lesson-label {
    font-size: 13px;
    font-weight: 500;
    color: rgba(196,154,133,0.5);
    text-transform: uppercase;
    letter-spacing: 2.5px;
    margin-bottom: 10px;
}

.cover-title {
    font-size: 48px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
    margin-bottom: 16px;
    letter-spacing: -0.5px;
}

.cover-subtitle {
    font-size: 16px;
    font-weight: 300;
    color: rgba(255,255,255,0.5);
    margin-bottom: 40px;
    letter-spacing: 0.5px;
    line-height: 1.5;
}

.cover-brand-row {
    display: flex;
    align-items: center;
    gap: 0;
}

.cover-brand {
    display: inline-block;
    border: 1px solid rgba(196,154,133,0.4);
    border-radius: 30px;
    padding: 11px 28px;
    color: #c49a85;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    background: rgba(196,154,133,0.06);
}

.cover-brand-sep {
    width: 1px;
    height: 28px;
    background: rgba(196,154,133,0.3);
    margin: 0 16px;
}

.cover-discord {
    display: inline-block;
    border: 1px solid rgba(140,160,196,0.4);
    border-radius: 30px;
    padding: 11px 28px;
    color: #8ca0c4;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    background: rgba(140,160,196,0.06);
    text-decoration: none;
}

.cover-divider {
    width: 50px;
    height: 2px;
    background: linear-gradient(90deg, #c49a85, transparent);
    margin-bottom: 18px;
    border-radius: 1px;
}

/* ---- TOC PAGE ---- */
.page-toc {
    background: linear-gradient(160deg, #2d2230 0%, #1a1b1f 40%, #0f1013 100%);
    padding: 55px 80px;
    position: relative;
    overflow: hidden;
    height: 810px;
}

/* Decorative gradient orbs on TOC */
.toc-orb {
    position: absolute;
    border-radius: 50%;
    z-index: 0;
}

.toc-orb-1 {
    top: -80px;
    left: -80px;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(95,70,87,0.4) 0%, transparent 70%);
}

.toc-orb-2 {
    bottom: -60px;
    right: 200px;
    width: 250px;
    height: 250px;
    background: radial-gradient(circle, rgba(80,55,65,0.3) 0%, transparent 70%);
}

.toc-statue {
    position: absolute;
    right: 20px;
    bottom: 20px;
    height: 82%;
    width: auto;
    opacity: 0.35;
    object-fit: contain;
    object-position: right bottom;
    z-index: 1;
    filter: drop-shadow(0 0 40px rgba(90,50,65,0.3));
}

.toc-tag {
    font-size: 10px;
    font-weight: 600;
    color: #c49a85;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 8px;
    position: relative;
    z-index: 2;
}

.toc-header {
    font-size: 38px;
    font-weight: 700;
    color: #ffffff;
    font-style: italic;
    margin-bottom: 8px;
    position: relative;
    z-index: 2;
}

.toc-header-line {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, #c49a85, transparent);
    margin-bottom: 30px;
    position: relative;
    z-index: 2;
}

.toc-grid {
    display: flex;
    gap: 24px;
    position: relative;
    z-index: 2;
}

.toc-column {
    flex: 1;
}

.toc-item {
    background: rgba(80, 55, 65, 0.45);
    border: 1px solid rgba(196,154,133,0.12);
    border-radius: 10px;
    padding: 12px 20px;
    margin-bottom: 8px;
    color: #e0ccd2;
    font-size: 14px;
    font-weight: 400;
    transition: all 0.2s;
}

.toc-item .toc-num {
    color: #c49a85;
    margin-right: 14px;
    font-weight: 600;
    font-size: 13px;
}

.toc-footer {
    position: absolute;
    bottom: 18px;
    left: 0;
    right: 0;
    text-align: center;
    color: rgba(255,255,255,0.25);
    font-size: 10px;
    z-index: 2;
    letter-spacing: 0.5px;
}

/* ---- CONTENT PAGE ---- */
.page-content {
    position: relative;
    padding: 10px 0 0 0;
    page: content-page;
    color: #e0ccd2;
}

.content-inner {
    position: relative;
    z-index: 3;
    width: 100%;
}

.section-header {
    font-size: 32px;
    font-weight: 700;
    font-style: italic;
    color: #ffffff;
    margin-bottom: 18px;
    margin-top: 0;
    text-transform: uppercase;
    letter-spacing: 1px;
    line-height: 1.2;
    position: relative;
    padding-left: 16px;
    padding-top: 5px;
    page-break-before: always;
    page-break-after: avoid;
}

/* First section header should not force a page break */
.content-inner .section-header:first-child {
    page-break-before: auto;
}

/* Accent bar before section headers */
.section-header::before {
    content: "";
    position: absolute;
    left: 0;
    top: 4px;
    width: 4px;
    height: 32px;
    background: linear-gradient(180deg, #c49a85, rgba(196,154,133,0.2));
    border-radius: 2px;
}

.section-header .fade {
    color: #c49a85;
}

/* ---- TWO-COLUMN LAYOUT ---- */
.content-columns {
    display: flex;
    gap: 40px;
    width: 100%;
    margin-bottom: 6px;
    page-break-inside: avoid;
}

.content-col {
    flex: 1;
    min-width: 0;
}

/* ---- CONTENT BLOCKS (no background boxes) ---- */
.content-box,
.content-box-full {
    margin-bottom: 14px;
    color: #e0ccd2;
}

.content-box p,
.content-box-full p {
    font-size: 13.5px;
    line-height: 1.65;
    margin-bottom: 10px;
    text-align: justify;
    color: #d4bcc4;
}

.content-box p:last-child,
.content-box-full p:last-child {
    margin-bottom: 0;
}

.content-box .sub-header,
.content-box-full .sub-header {
    font-size: 15px;
    font-weight: 700;
    color: #c49a85;
    margin-bottom: 8px;
    margin-top: 18px;
    letter-spacing: 0.3px;
    page-break-after: avoid;
}

.content-box .sub-header:first-child,
.content-box-full .sub-header:first-child {
    margin-top: 0;
}

.content-box ul,
.content-box-full ul {
    margin: 6px 0 10px 18px;
    padding: 0;
}

.content-box ul li,
.content-box-full ul li {
    font-size: 13.5px;
    line-height: 1.6;
    color: #d4bcc4;
    margin-bottom: 3px;
}

/* ---- EXAMPLES ---- */
.content-box .example-good,
.content-box-full .example-good {
    border-left: 3px solid #7dba6d;
    background: rgba(125,186,109,0.06);
    padding: 8px 12px;
    margin: 10px 0;
    font-style: italic;
    color: #c8e6c0;
    font-size: 13px;
    line-height: 1.55;
    border-radius: 0 6px 6px 0;
    page-break-inside: avoid;
}

.content-box .example-bad,
.content-box-full .example-bad {
    border-left: 3px solid #c9665a;
    background: rgba(201,102,90,0.06);
    padding: 8px 12px;
    margin: 10px 0;
    font-style: italic;
    color: #eaaca5;
    font-size: 13px;
    line-height: 1.55;
    border-radius: 0 6px 6px 0;
    page-break-inside: avoid;
}

.content-box .example-label,
.content-box-full .example-label {
    font-weight: 700;
    font-style: normal;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
}

/* ---- PANELS ---- */
.content-box .panel-box,
.content-box-full .panel-box {
    border-left: 3px solid rgba(196,154,133,0.6);
    padding: 14px 18px;
    margin: 12px 0 6px 0;
    page-break-inside: avoid;
}

.content-box .panel-title,
.content-box-full .panel-title {
    font-size: 12px;
    font-weight: 700;
    color: #c49a85;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.content-box .panel-body,
.content-box-full .panel-body {
    font-size: 13px;
    line-height: 1.55;
    color: #d4bcc4;
}

.content-footer {
    position: absolute;
    bottom: 18px;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 10px;
    color: rgba(255,255,255,0.25);
    z-index: 2;
    letter-spacing: 0.5px;
}

/* ---- SUMMARY PAGE ---- */
.summary-box ul li {
    margin-bottom: 6px;
}

.summary-brand-box {
    text-align: center;
    padding: 30px 24px;
}

.summary-brand-name {
    font-size: 22px;
    font-weight: 700;
    color: #c49a85;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.summary-brand-line {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #c49a85, transparent);
    margin: 0 auto 14px auto;
}

.summary-brand-text {
    font-size: 12px;
    color: rgba(255,255,255,0.4);
    letter-spacing: 0.5px;
}

/* ---- PAGE NUMBERS ---- */
.page-number {
    position: absolute;
    bottom: 18px;
    right: 60px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 1px;
    z-index: 10;
}

.page-number-dark {
    color: rgba(255,255,255,0.3);
}

/* ---- SMALL TOP-RIGHT LOGO ON CONTENT PAGES ---- */
.content-logo-small {
    position: absolute;
    top: 18px;
    right: 30px;
    height: 55px;
    width: auto;
    opacity: 0.35;
    object-fit: contain;
    z-index: 4;
}
"""


def split_header_two_tone(header_text):
    """Split header so last word gets fade color."""
    words = header_text.strip().split()
    if len(words) <= 1:
        return header_text, ""
    main = " ".join(words[:-1])
    fade = words[-1]
    return main, fade


def group_blocks_into_chunks(blocks):
    """Group blocks into logical chunks, splitting at each subheader.

    A chunk starts at a subheader (or from the beginning) and includes
    everything up to the next subheader.  This keeps each chunk small
    enough to fit on a single page, avoiding the monolithic-column
    problem with WeasyPrint floats.
    """
    chunks = []
    current_chunk = []
    for block in blocks:
        if block.get("type") == "subheader" and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
        current_chunk.append(block)
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def render_blocks_html(blocks):
    """Render a list of content blocks into HTML."""
    html = ""
    for block in blocks:
        btype = block.get("type", "text")

        if btype == "text":
            html += f'<p>{block["content"]}</p>\n'

        elif btype == "subheader":
            html += f'<div class="sub-header">{block["content"]}</div>\n'

        elif btype == "bullets":
            bullet = block.get("bullet", "")
            html += "<ul>\n"
            for item in block["items"]:
                prefix = f"{bullet} " if bullet and bullet != "•" else ""
                html += f"  <li>{prefix}{item}</li>\n"
            html += "</ul>\n"

        elif btype == "good_example":
            lines = block["content"].replace("\n", "<br>")
            html += f'<div class="example-good"><div class="example-label">Good example:</div>{lines}</div>\n'

        elif btype == "bad_example":
            lines = block["content"].replace("\n", "<br>")
            html += f'<div class="example-bad"><div class="example-label">Bad example:</div>{lines}</div>\n'

        elif btype == "panel":
            title = block.get("title", "")
            content = block.get("content", "").replace("\n", "<br>")
            html += '<div class="panel-box">\n'
            if title:
                html += f'  <div class="panel-title">{title}</div>\n'
            html += f'  <div class="panel-body">{content}</div>\n'
            html += '</div>\n'

        elif btype == "page_break":
            html += '<div style="page-break-before: always;"></div>\n'

    return html


# ---------------------------------------------------------------------------
# PAGE BUILDERS (HTML)
# ---------------------------------------------------------------------------

def build_cover_html(title, subtitle, logo_uri="", page_num=1, total_pages=1, module_label="", lesson_label=""):
    """Build cover page HTML."""
    title_html = title.replace("\n", "<br>")

    return f'''
    <div class="page page-cover">
        <div class="cover-gradient-overlay"></div>
        <div class="cover-glow"></div>
        <div class="cover-accent-line"></div>
        <div class="cover-accent-line-bottom"></div>
        <div class="cover-logo-design">
            <div class="cover-logo-ring cover-logo-ring-1"></div>
            <div class="cover-logo-ring cover-logo-ring-2"></div>
            <div class="cover-logo-ring cover-logo-ring-3"></div>
            <div class="cover-logo-arc cover-logo-arc-1"></div>
            <div class="cover-logo-arc cover-logo-arc-2"></div>
            <div class="cover-logo-dot cover-logo-dot-1"></div>
            <div class="cover-logo-dot cover-logo-dot-2"></div>
            <div class="cover-logo-dot cover-logo-dot-3"></div>
        </div>
        <div class="cover-left">
            <div class="cover-tag">Premium Course Material</div>
            <div class="cover-divider"></div>
            {"<div class='cover-module-label'>" + module_label + "</div>" if module_label else ""}
            {"<div class='cover-lesson-label'>" + lesson_label + "</div>" if lesson_label else ""}
            <div class="cover-title">{title_html}</div>
            <div class="cover-subtitle">{subtitle}</div>
            <div class="cover-brand-row">
                <div class="cover-brand">{BRAND_NAME}</div>
                <div class="cover-brand-sep"></div>
                <a class="cover-discord" href="https://discord.com/invite/ai-influencer-method" target="_blank">Our Discord</a>
            </div>
        </div>
        <div class="cover-logo-wrap">
            {"<img class='cover-logo-img' src='" + logo_uri + "' />" if logo_uri else ""}
        </div>
    </div>
    '''


def build_toc_html(sections, logo_uri="", page_num=2, total_pages=1):
    """Build table of contents page HTML."""
    mid = len(sections) // 2 + len(sections) % 2
    left_items = sections[:mid]
    right_items = sections[mid:]

    left_html = ""
    for pn, title in left_items:
        left_html += f'<div class="toc-item"><span class="toc-num">{pn:02d}</span>{title}</div>\n'

    right_html = ""
    for pn, title in right_items:
        right_html += f'<div class="toc-item"><span class="toc-num">{pn:02d}</span>{title}</div>\n'

    return f'''
    <div class="page page-toc">
        <div class="toc-orb toc-orb-1"></div>
        <div class="toc-orb toc-orb-2"></div>
        {"<img class='toc-statue' src='" + logo_uri + "' />" if logo_uri else ""}
        <div class="toc-tag">Course Outline</div>
        <div class="toc-header">Table Of Contents</div>
        <div class="toc-header-line"></div>
        <div class="toc-grid">
            <div class="toc-column">{left_html}</div>
            <div class="toc-column">{right_html}</div>
        </div>
        <div class="toc-footer">{FOOTER_TEXT}</div>
    </div>
    '''


def build_section_html(header, body_blocks):
    """Build HTML for a single section (header + content blocks).

    Returns flowing HTML that is NOT wrapped in a page div, so WeasyPrint
    can paginate it naturally across multiple slides.
    """
    main_part, fade_part = split_header_two_tone(header)

    header_html = main_part
    if fade_part:
        header_html += f' <span class="fade">{fade_part}</span>'

    content_html = ""

    # Group consecutive non-two-column blocks into a single content-box-full
    # so they flow together naturally instead of each being an isolated box.
    pending_blocks = []

    def flush_pending():
        nonlocal pending_blocks
        if not pending_blocks:
            return ""
        block_html = render_blocks_html(pending_blocks)
        pending_blocks = []
        return f'<div class="content-box-full">{block_html}</div>\n'

    for block in body_blocks:
        if block.get("type") == "two_column":
            content_html += flush_pending()
            # Split each column into small logical chunks (one per subheader
            # group) so each paired row is small enough for a single page.
            left_chunks = group_blocks_into_chunks(block["left"])
            right_chunks = group_blocks_into_chunks(block["right"])
            max_chunks = max(len(left_chunks), len(right_chunks))
            for i in range(max_chunks):
                left_html = render_blocks_html(left_chunks[i]) if i < len(left_chunks) else ""
                right_html = render_blocks_html(right_chunks[i]) if i < len(right_chunks) else ""
                left_box = f'<div class="content-box">{left_html}</div>' if left_html else ""
                right_box = f'<div class="content-box">{right_html}</div>' if right_html else ""
                content_html += f'''
                <div class="content-columns">
                    <div class="content-col">{left_box}</div>
                    <div class="content-col">{right_box}</div>
                </div>
                '''
        elif block.get("type") == "page_break":
            content_html += flush_pending()
            content_html += '<div style="page-break-before: always;"></div>\n'
        elif block.get("type") == "panel" and block.get("border"):
            # Bordered panels (rules, tips) are standalone — flush first
            content_html += flush_pending()
            block_html = render_blocks_html([block])
            content_html += f'<div class="content-box-full">{block_html}</div>\n'
        else:
            pending_blocks.append(block)

    content_html += flush_pending()

    return f'''
        <div class="section-header">{header_html}</div>
        {content_html}
    '''


def build_content_pages_html(sections, logo_uri=""):
    """Build all content sections as a single flowing content region.

    Instead of one .page div per section, all sections flow inside a single
    content container.  WeasyPrint paginates using the @page content-page
    rule, so content naturally fills each slide and overflows to the next
    without leaving whitespace gaps.
    """
    sections_html = ""
    for section in sections:
        sections_html += build_section_html(section["header"], section["blocks"])

    return f'''
    <div class="page-content">
        <div class="content-inner">
            {sections_html}
        </div>
    </div>
    '''


def build_summary_page_html(points, logo_uri="", page_num=1, total_pages=1):
    """Build summary page HTML."""
    bullets = ""
    for pt in points:
        bullets += f"<li>{pt}</li>\n"

    return f'''
    <div class="page page-content page-summary">
        <div class="content-inner">
            <div class="section-header">END <span class="fade">SUMMARY</span></div>
            <div class="content-columns">
                <div class="content-col">
                    <div class="content-box summary-box">
                        <ul>{bullets}</ul>
                    </div>
                </div>
                <div class="content-col">
                    <div class="content-box summary-brand-box">
                        <div class="summary-brand-name">{BRAND_NAME}</div>
                        <div class="summary-brand-line"></div>
                        <div class="summary-brand-text">All materials are strictly protected.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''


# ---------------------------------------------------------------------------
# MAIN GENERATION
# ---------------------------------------------------------------------------

def generate_pdf(config, output_path):
    """Generate a complete PDF from config dict."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load the main Course Logo (statue bust with dollar halo)
    logo_path = config.get("logo_path", "")
    if not logo_path:
        # Default to Course Logo.png
        default_logo = BASE_DIR / "PDF" / "Course_Logo.png"
        if default_logo.exists():
            logo_path = str(default_logo)
    logo_uri = img_to_data_uri(logo_path) if logo_path and os.path.exists(logo_path) else ""

    # Content pages now use CSS dark gradient background (no image needed)

    title = config["title"]
    subtitle = config.get("subtitle", "")
    module_label = config.get("module_label", "")
    lesson_label = config.get("lesson_label", "")
    sections = config["sections"]
    summary_points = config.get("summary_points", [])

    # Determine if TOC and summary should be included
    skip_toc = config.get("skip_toc", False)
    skip_summary = config.get("skip_summary", False)

    # Page count is dynamic now (WeasyPrint auto-paginates content)
    total_pages = 0  # placeholder, counter(pages) in CSS handles it

    # Build pages
    pages_html = ""

    # Cover — uses Course Logo as the main statue image
    pages_html += build_cover_html(title, subtitle, logo_uri, page_num=1, total_pages=total_pages, module_label=module_label, lesson_label=lesson_label)

    # TOC — uses Course Logo as background decoration
    if not skip_toc:
        toc_entries = [(i + 1, s["header"]) for i, s in enumerate(sections)]
        pages_html += build_toc_html(toc_entries, logo_uri, page_num=2, total_pages=total_pages)

    # Content — all sections flow continuously; WeasyPrint paginates
    pages_html += build_content_pages_html(sections, logo_uri=logo_uri)

    # Summary
    if summary_points and not skip_summary:
        pages_html += build_summary_page_html(
            summary_points,
            logo_uri=logo_uri,
        )

    # Build dynamic @page CSS for content pages (dark background + footer)
    footer_escaped = FOOTER_TEXT.replace('"', '\\"')
    dynamic_page_css = f"""
@page content-page {{
    margin: 45px 60px;
    padding: 0;
    background: #1a1b1f;
    @bottom-center {{
        content: "{footer_escaped}";
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 10px;
        color: rgba(255,255,255,0.25);
        letter-spacing: 0.5px;
    }}
    @bottom-right {{
        content: counter(page) " / " counter(pages);
        font-size: 11px;
        font-weight: 500;
        letter-spacing: 1px;
        color: rgba(255,255,255,0.3);
        margin-right: 0;
    }}
}}
"""

    # Full HTML document
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{CSS_BASE}
{dynamic_page_css}
</style>
</head>
<body>
{pages_html}
</body>
</html>"""

    # Generate PDF
    HTML(string=full_html, base_url=str(BASE_DIR)).write_pdf(output_path)
    print(f"Generated: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# JSON-DRIVEN GENERATION
# ---------------------------------------------------------------------------

def generate_from_json(config_path, output_path=None):
    """Generate a PDF from a JSON content file."""
    with open(config_path, "r") as f:
        config = json.load(f)

    if output_path is None:
        filename = config.get("output_filename", "output.pdf")
        output_path = str(OUTPUT_DIR / filename)

    # Try to find a platform logo
    logo_name = config.get("logo", "")
    if logo_name:
        config["logo_path"] = str(BASE_DIR / "PDF" / logo_name)
    elif not config.get("logo_path"):
        # Default: look for Course Logo
        default_logo = BASE_DIR / "PDF" / "Course_Logo.png"
        if default_logo.exists():
            config["logo_path"] = str(default_logo)

    return generate_pdf(config, output_path)


# ---------------------------------------------------------------------------
# TEMPLATE EXAMPLE
# ---------------------------------------------------------------------------

def generate_template_example():
    """Generate the template example PDF."""
    config = {
        "title": "AI Influencer Method\nFree Training",
        "subtitle": "The Complete Beginner's Blueprint to AI-Generated Influencer Income",
        "logo_path": str(BASE_DIR / "PDF" / "Course_Logo.png"),
        "sections": [
            {
                "header": "Intro: What Is the AI Influencer Method",
                "blocks": [
                    {"type": "text", "content": "The AI Influencer Method is a system for building and monetizing social media pages using AI-generated personas. These personas look, act, and engage like real influencers but are entirely created and managed through artificial intelligence tools."},
                    {"type": "text", "content": "This is not about catfishing or deception. This is a business model. The audience knows they are interacting with a curated persona. The value they receive is entertainment, attention, and content."},
                    {"type": "two_column", "left": [
                        {"type": "subheader", "content": "What You Will Learn"},
                        {"type": "bullets", "items": [
                            "How to create an AI influencer from scratch",
                            "Which platforms to use and why",
                            "How to grow from zero to monetization",
                            "The exact content pipeline that works",
                            "How to scale to multiple pages",
                        ]},
                    ], "right": [
                        {"type": "subheader", "content": "What This Is NOT"},
                        {"type": "bullets", "items": [
                            "A get-rich-quick scheme",
                            "A passive income fantasy",
                            "A one-click automation tool",
                            "Something that works without effort",
                        ]},
                    ]},
                ],
            },
            {
                "header": "Why AI Influencers Work",
                "blocks": [
                    {"type": "two_column", "left": [
                        {"type": "text", "content": "Traditional influencer marketing requires a real person. That person has limitations. AI influencers have none of these limitations. The persona is consistent. The content is controllable. The output is scalable."},
                        {"type": "text", "content": "The market for parasocial relationships is massive and growing. People pay for connection, attention, and fantasy."},
                    ], "right": [
                        {"type": "subheader", "content": "Key Advantages"},
                        {"type": "bullets", "items": [
                            "No physical limitations on content output",
                            "Consistent brand and persona",
                            "Scalable to multiple personas",
                            "Lower operating cost",
                            "Full creative control",
                        ]},
                        {"type": "panel", "title": "Industry Growth", "content": "The AI influencer market is projected to grow significantly year over year. Early movers have the strongest advantage."},
                    ]},
                ],
            },
            {
                "header": "The Business Model Overview",
                "blocks": [
                    {"type": "text", "content": "The business model is simple. Attention flows through a funnel. Free content creates interest. Interest creates followers. Followers convert to paying subscribers."},
                    {"type": "two_column", "left": [
                        {"type": "subheader", "content": "Revenue Sources"},
                        {"type": "bullets", "items": [
                            "Fanvue / subscription platform monthly fees",
                            "Pay-per-view (PPV) locked content",
                            "Custom content requests via chat",
                            "Tips and gifts from engaged fans",
                        ]},
                    ], "right": [
                        {"type": "subheader", "content": "Traffic Flow"},
                        {"type": "bullets", "items": [
                            "Instagram / TikTok \u2192 Link in Bio",
                            "Link in Bio \u2192 Free Telegram",
                            "Free Telegram \u2192 Fanvue subscription",
                            "Fanvue chat \u2192 Upsells and PPV",
                        ], "bullet": "\u2192"},
                    ]},
                ],
            },
            {
                "header": "Platform Selection: Where to Post",
                "blocks": [
                    {"type": "two_column", "left": [
                        {"type": "subheader", "content": "Primary Platforms"},
                        {"type": "bullets", "items": [
                            "Instagram \u2014 Main traffic and brand hub",
                            "Threads \u2014 Engagement and discovery",
                            "TikTok \u2014 Secondary reach",
                            "Fanvue \u2014 Monetization endpoint",
                        ]},
                    ], "right": [
                        {"type": "subheader", "content": "Support Platforms"},
                        {"type": "bullets", "items": [
                            "Telegram \u2014 Pre-sell funnel",
                            "Reddit \u2014 Niche viral exposure",
                            "Twitter/X \u2014 Brand presence",
                        ]},
                        {"type": "panel", "title": "Priority", "content": "1. Instagram (mandatory)\n2. Threads (mandatory)\n3. Fanvue (mandatory)\n4. Telegram (recommended)"},
                    ]},
                ],
            },
            {
                "header": "Content Creation Pipeline",
                "blocks": [
                    {"type": "text", "content": "Content is the fuel of this business. Without consistent, high-quality content, nothing else works."},
                    {"type": "two_column", "left": [
                        {"type": "subheader", "content": "Step-by-Step Pipeline"},
                        {"type": "bullets", "items": [
                            "Generate base images using AI tools",
                            "Edit and refine for consistency",
                            "Create variations for different platforms",
                            "Write captions that match platform tone",
                            "Schedule posts using a content calendar",
                        ], "bullet": "\u2192"},
                    ], "right": [
                        {"type": "subheader", "content": "Content Rules"},
                        {"type": "bullets", "items": [
                            "Same face across all images",
                            "Lighting and background vary naturally",
                            "Never same image on two platforms same day",
                            "Instagram gets best content first",
                        ]},
                    ]},
                ],
            },
            {
                "header": "Profile Setup: Identity & Trust",
                "blocks": [
                    {"type": "text", "content": "Your profile is the first thing anyone sees. It must look human, trustworthy, and interesting within 2 seconds."},
                    {"type": "two_column", "left": [
                        {"type": "subheader", "content": "Username Rules"},
                        {"type": "bullets", "items": [
                            "Human-sounding name",
                            "No random numbers",
                            "No sexual words",
                            "Easy to remember",
                        ]},
                    ], "right": [
                        {"type": "subheader", "content": "Bio Rules"},
                        {"type": "bullets", "items": [
                            "Short, casual, personality-driven",
                            "No links during warmup",
                            "No selling language early",
                            "Add link after 3 weeks",
                        ]},
                    ]},
                ],
            },
            {
                "header": "Growth Phase: First 30 Days",
                "blocks": [
                    {"type": "text", "content": "The first 30 days determine everything. Rush this phase and the account gets flagged or banned."},
                    {"type": "two_column", "left": [
                        {"type": "subheader", "content": "Week 1-2: Warmup"},
                        {"type": "bullets", "items": [
                            "No posting first 3 days",
                            "Scroll, like, and comment naturally",
                            "Follow 5-10 accounts per day max",
                            "First post on day 5-7",
                        ]},
                    ], "right": [
                        {"type": "subheader", "content": "Week 3-4: Activation"},
                        {"type": "bullets", "items": [
                            "Increase to 4-5 posts per week",
                            "Start using Stories daily",
                            "Begin Threads engagement",
                            "Add link in bio after week 3",
                        ]},
                        {"type": "panel", "title": "Critical Rule", "content": "If you rush the warmup, everything after breaks. There are no shortcuts."},
                    ]},
                ],
            },
            {
                "header": "Monetization: How Revenue Flows",
                "blocks": [
                    {"type": "two_column", "left": [
                        {"type": "subheader", "content": "Conversion Path"},
                        {"type": "bullets", "items": [
                            "Free content builds desire",
                            "Link in Bio captures interest",
                            "Telegram warms cold traffic",
                            "Fanvue captures the payment",
                            "Chat upsells increase revenue",
                        ], "bullet": "\u2192"},
                    ], "right": [
                        {"type": "subheader", "content": "Revenue Optimization"},
                        {"type": "bullets", "items": [
                            "Chat quality > follower count",
                            "Respond to new subs within 5 min",
                            "Use emotional framing, not hard selling",
                            "Prioritize whale management",
                        ]},
                    ]},
                ],
            },
            {
                "header": "Common Mistakes & How to Avoid Them",
                "blocks": [
                    {"type": "two_column", "left": [
                        {"type": "subheader", "content": "Mistakes That Kill Pages"},
                        {"type": "bullets", "items": [
                            "Posting before warmup is complete",
                            "Using inconsistent AI faces",
                            "Spamming links in captions",
                            "Posting explicit content on IG",
                        ]},
                    ], "right": [
                        {"type": "subheader", "content": "What Winners Do"},
                        {"type": "bullets", "items": [
                            "Follow the warmup timeline",
                            "One consistent AI model per page",
                            "Deploy links after trust is built",
                            "Keep Instagram safe and compliant",
                        ]},
                    ]},
                ],
            },
            {
                "header": "Scaling: From One Page to Many",
                "blocks": [
                    {"type": "text", "content": "Once the first page is profitable and stable, the system is ready to scale. Scaling means running multiple AI personas simultaneously."},
                    {"type": "two_column", "left": [
                        {"type": "subheader", "content": "When to Scale"},
                        {"type": "bullets", "items": [
                            "First page has consistent revenue",
                            "Content pipeline is systematized",
                            "Chat operations are delegated",
                        ]},
                    ], "right": [
                        {"type": "subheader", "content": "How to Scale"},
                        {"type": "bullets", "items": [
                            "New persona with different niche",
                            "Separate devices or browser profiles",
                            "Never link accounts to each other",
                            "Hire chatters for fan management",
                        ]},
                    ]},
                ],
            },
            {
                "header": "Tools & Resources",
                "blocks": [
                    {"type": "two_column", "left": [
                        {"type": "subheader", "content": "Content Generation"},
                        {"type": "bullets", "items": [
                            "AI image generation tools",
                            "Photo editing software",
                            "Face consistency tools",
                        ]},
                        {"type": "subheader", "content": "Platform Management"},
                        {"type": "bullets", "items": [
                            "Content scheduling tools",
                            "Analytics monitoring",
                            "Multi-account management",
                        ]},
                    ], "right": [
                        {"type": "subheader", "content": "Monetization"},
                        {"type": "bullets", "items": [
                            "Fanvue (primary platform)",
                            "Telegram (free funnel)",
                            "AllMyLinks / Linktree",
                        ]},
                        {"type": "subheader", "content": "Operations"},
                        {"type": "bullets", "items": [
                            "Chat management systems",
                            "Revenue tracking spreadsheets",
                            "Content calendar templates",
                        ]},
                    ]},
                ],
            },
        ],
        "summary_points": [
            "The AI Influencer Method is a real business that requires real effort",
            "Follow the warmup phase exactly \u2014 no shortcuts",
            "Instagram is the primary platform, everything else supports it",
            "Content consistency (same face) is non-negotiable",
            "Revenue comes from the funnel, not from posting",
            "Chat quality determines profit more than follower count",
            "Scale only after the first page is profitable and stable",
            "Patience in the first 30 days determines everything after",
        ],
    }

    output_path = str(OUTPUT_DIR / "AI-Influencer-Method-Free-Training.pdf")
    return generate_pdf(config, output_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--config":
        if len(sys.argv) < 3:
            print("Usage: python generate_pdf.py --config <path_to_json>")
            sys.exit(1)
        generate_from_json(sys.argv[2])
    else:
        generate_template_example()
