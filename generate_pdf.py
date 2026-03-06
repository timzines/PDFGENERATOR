#!/usr/bin/env python3
"""
AI Influencer Accelerator — PDF Generator
==========================================
Generates branded PDFs following PDF_RULES.md exactly.

Usage:
    python generate_pdf.py                          # generates the template example
    python generate_pdf.py --config my_content.json # generates from a JSON content file

Content JSON format: see CONTENT_SCHEMA at bottom of file.
"""

import json
import os
import sys
import textwrap
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ---------------------------------------------------------------------------
# BRAND CONSTANTS (from PDF_RULES.md)
# ---------------------------------------------------------------------------
PAGE_W = 1440  # pts
PAGE_H = 810   # pts
PAGE_SIZE = (PAGE_W, PAGE_H)

# Colors
BG_COLOR        = HexColor("#0D0D0D")
ACCENT_GREEN    = HexColor("#39FF14")
ACCENT_LIGHT    = HexColor("#1AFF00")
TEXT_WHITE       = HexColor("#FFFFFF")
TEXT_MUTED       = HexColor("#AAAAAA")
PANEL_BG        = HexColor("#1A1A1A")
DANGER_RED      = HexColor("#FF3131")
BORDER_DARK     = HexColor("#333333")

# Margins
MARGIN_LEFT   = 70
MARGIN_RIGHT  = 70
MARGIN_TOP    = 55
MARGIN_BOTTOM = 45

CONTENT_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
COL_GAP   = 50
COL_W     = (CONTENT_W - COL_GAP) / 2

# Footer
FOOTER_TEXT = "All materials are strictly protected under AI Influencer Accelerator\u00AE rights"
FOOTER_FONT_SIZE = 9

# Font sizes
COVER_TITLE_SIZE   = 52
COVER_SUB_SIZE     = 24
SECTION_HDR_SIZE   = 36
SUB_HDR_SIZE       = 22
BODY_SIZE          = 15
BULLET_SIZE        = 15
TOC_SIZE           = 15
BRAND_SIZE         = 17
LINE_SPACING       = 1.5


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def hex_to_color(h):
    return HexColor(h)


def draw_bg(c):
    """Fill entire page with dark background."""
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)


def draw_footer(c):
    """Draw the standard footer on current page."""
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", FOOTER_FONT_SIZE)
    c.drawCentredString(PAGE_W / 2, 20, FOOTER_TEXT)


def draw_panel(c, x, y, w, h, border_color=None):
    """Draw a rounded dark panel."""
    c.setFillColor(PANEL_BG)
    if border_color:
        c.setStrokeColor(border_color)
        c.setLineWidth(1.5)
        c.roundRect(x, y, w, h, 10, fill=1, stroke=1)
    else:
        c.setStrokeColor(PANEL_BG)
        c.roundRect(x, y, w, h, 10, fill=1, stroke=0)


def wrap_text(text, font_name, font_size, max_width):
    """Wrap text to fit within max_width, returns list of lines."""
    # Rough char width estimate
    avg_char_w = font_size * 0.48
    chars_per_line = int(max_width / avg_char_w)
    if chars_per_line < 10:
        chars_per_line = 10
    lines = []
    for paragraph in text.split("\n"):
        if paragraph.strip() == "":
            lines.append("")
        else:
            wrapped = textwrap.wrap(paragraph, width=chars_per_line)
            lines.extend(wrapped if wrapped else [""])
    return lines


def draw_body_text(c, text, x, y, max_width, font_size=BODY_SIZE, color=TEXT_WHITE):
    """Draw wrapped body text. Returns new y position."""
    c.setFillColor(color)
    c.setFont("Helvetica", font_size)
    line_h = font_size * LINE_SPACING
    lines = wrap_text(text, "Helvetica", font_size, max_width)
    for line in lines:
        if y < MARGIN_BOTTOM + 30:
            break
        c.drawString(x, y, line)
        y -= line_h
    return y


def draw_bullets(c, items, x, y, max_width, font_size=BULLET_SIZE, color=TEXT_WHITE, bullet="•"):
    """Draw bullet list. Returns new y position."""
    c.setFillColor(color)
    c.setFont("Helvetica", font_size)
    line_h = font_size * LINE_SPACING
    indent = 20
    for item in items:
        if y < MARGIN_BOTTOM + 30:
            break
        lines = wrap_text(item, "Helvetica", font_size, max_width - indent)
        for i, line in enumerate(lines):
            if i == 0:
                c.drawString(x, y, bullet)
                c.drawString(x + indent, y, line)
            else:
                c.drawString(x + indent, y, line)
            y -= line_h
        y -= 4  # extra spacing between bullets
    return y


def draw_section_header(c, title, y=None):
    """Draw a green ALL CAPS section header."""
    if y is None:
        y = PAGE_H - MARGIN_TOP - SECTION_HDR_SIZE
    c.setFillColor(ACCENT_GREEN)
    c.setFont("Helvetica-Bold", SECTION_HDR_SIZE)
    c.drawString(MARGIN_LEFT, y, title.upper())
    # Green underline
    c.setStrokeColor(ACCENT_GREEN)
    c.setLineWidth(2)
    c.line(MARGIN_LEFT, y - 8, MARGIN_LEFT + CONTENT_W, y - 8)
    return y - 35


def draw_sub_header(c, title, x, y, color=TEXT_WHITE):
    """Draw a sub-header."""
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", SUB_HDR_SIZE)
    c.drawString(x, y, title)
    return y - SUB_HDR_SIZE * LINE_SPACING


# ---------------------------------------------------------------------------
# PAGE BUILDERS
# ---------------------------------------------------------------------------

def build_cover(c, title, subtitle, brand="AI Influencer Accelerator", logo_path=None):
    """Page 1 — Cover."""
    draw_bg(c)

    # Optional logo
    if logo_path and os.path.exists(logo_path):
        try:
            img = ImageReader(logo_path)
            iw, ih = img.getSize()
            scale = min(140 / iw, 140 / ih)
            draw_w, draw_h = iw * scale, ih * scale
            c.drawImage(logo_path, (PAGE_W - draw_w) / 2, PAGE_H - 60 - draw_h,
                        width=draw_w, height=draw_h, mask='auto')
        except Exception:
            pass

    # Title
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", COVER_TITLE_SIZE)
    # Wrap title if needed
    title_lines = wrap_text(title.upper(), "Helvetica-Bold", COVER_TITLE_SIZE, CONTENT_W)
    title_y = PAGE_H / 2 + (len(title_lines) - 1) * COVER_TITLE_SIZE * 0.6
    for line in title_lines:
        tw = c.stringWidth(line, "Helvetica-Bold", COVER_TITLE_SIZE)
        c.drawString((PAGE_W - tw) / 2, title_y, line)
        title_y -= COVER_TITLE_SIZE * 1.2

    # Subtitle
    sub_y = title_y - 20
    c.setFillColor(TEXT_MUTED)
    c.setFont("Helvetica", COVER_SUB_SIZE)
    tw = c.stringWidth(subtitle, "Helvetica", COVER_SUB_SIZE)
    c.drawString((PAGE_W - tw) / 2, sub_y, subtitle)

    # Brand
    brand_y = sub_y - 50
    c.setFillColor(ACCENT_GREEN)
    c.setFont("Helvetica-Bold", BRAND_SIZE)
    tw = c.stringWidth(brand, "Helvetica-Bold", BRAND_SIZE)
    c.drawString((PAGE_W - tw) / 2, brand_y, brand)

    # Decorative line
    c.setStrokeColor(ACCENT_GREEN)
    c.setLineWidth(2)
    line_w = 300
    c.line((PAGE_W - line_w) / 2, brand_y - 15, (PAGE_W + line_w) / 2, brand_y - 15)

    c.showPage()


def build_toc(c, sections):
    """Page 2 — Table of Contents."""
    draw_bg(c)

    # Header
    y = PAGE_H - MARGIN_TOP - 10
    c.setFillColor(TEXT_WHITE)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(MARGIN_LEFT, y, "Table Of Contents")
    y -= 50

    # Two columns
    mid = len(sections) // 2 + len(sections) % 2
    left_items = sections[:mid]
    right_items = sections[mid:]

    line_h = 32
    for i, (page_num, title) in enumerate(left_items):
        if y < MARGIN_BOTTOM + 40:
            break
        # Page number in green
        c.setFillColor(ACCENT_GREEN)
        c.setFont("Helvetica-Bold", TOC_SIZE)
        c.drawString(MARGIN_LEFT, y, f"{page_num:02d}")
        # Title in white
        c.setFillColor(TEXT_WHITE)
        c.setFont("Helvetica", TOC_SIZE)
        c.drawString(MARGIN_LEFT + 35, y, title)
        y -= line_h

    # Right column
    y2 = PAGE_H - MARGIN_TOP - 60
    x2 = MARGIN_LEFT + COL_W + COL_GAP
    for i, (page_num, title) in enumerate(right_items):
        if y2 < MARGIN_BOTTOM + 40:
            break
        c.setFillColor(ACCENT_GREEN)
        c.setFont("Helvetica-Bold", TOC_SIZE)
        c.drawString(x2, y2, f"{page_num:02d}")
        c.setFillColor(TEXT_WHITE)
        c.setFont("Helvetica", TOC_SIZE)
        c.drawString(x2 + 35, y2, title)
        y2 -= line_h

    draw_footer(c)
    c.showPage()


def build_content_page(c, header, body_blocks):
    """
    Generic content page.
    body_blocks is a list of dicts:
      {"type": "text", "content": "..."}
      {"type": "bullets", "items": [...]}
      {"type": "subheader", "content": "..."}
      {"type": "good_example", "content": "..."}
      {"type": "bad_example", "content": "..."}
      {"type": "two_column", "left": [...blocks], "right": [...blocks]}
      {"type": "panel", "title": "...", "content": "...", "border": "#39FF14"}
    """
    draw_bg(c)
    y = draw_section_header(c, header)

    def render_blocks(blocks, x, y, max_w):
        for block in blocks:
            if y < MARGIN_BOTTOM + 40:
                break
            btype = block.get("type", "text")

            if btype == "text":
                y = draw_body_text(c, block["content"], x, y, max_w)
                y -= 10

            elif btype == "bullets":
                bullet_char = block.get("bullet", "•")
                y = draw_bullets(c, block["items"], x, y, max_w, bullet=bullet_char)
                y -= 10

            elif btype == "subheader":
                y = draw_sub_header(c, block["content"], x, y)
                y -= 5

            elif btype == "good_example":
                panel_h = 14 * LINE_SPACING * (block["content"].count("\n") + 2) + 30
                draw_panel(c, x, y - panel_h, max_w, panel_h, border_color=ACCENT_GREEN)
                inner_y = y - 16
                c.setFillColor(ACCENT_GREEN)
                c.setFont("Helvetica-Bold", 13)
                c.drawString(x + 14, inner_y, "Good example:")
                inner_y -= 20
                inner_y = draw_body_text(c, block["content"], x + 14, inner_y, max_w - 28, font_size=13)
                y = y - panel_h - 12

            elif btype == "bad_example":
                panel_h = 14 * LINE_SPACING * (block["content"].count("\n") + 2) + 30
                draw_panel(c, x, y - panel_h, max_w, panel_h, border_color=DANGER_RED)
                inner_y = y - 16
                c.setFillColor(DANGER_RED)
                c.setFont("Helvetica-Bold", 13)
                c.drawString(x + 14, inner_y, "Bad example:")
                inner_y -= 20
                inner_y = draw_body_text(c, block["content"], x + 14, inner_y, max_w - 28, font_size=13)
                y = y - panel_h - 12

            elif btype == "panel":
                lines = wrap_text(block.get("content", ""), "Helvetica", 14, max_w - 28)
                panel_h = 14 * LINE_SPACING * len(lines) + 50
                border = HexColor(block["border"]) if block.get("border") else ACCENT_GREEN
                draw_panel(c, x, y - panel_h, max_w, panel_h, border_color=border)
                inner_y = y - 16
                if block.get("title"):
                    c.setFillColor(ACCENT_GREEN)
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(x + 14, inner_y, block["title"])
                    inner_y -= 24
                inner_y = draw_body_text(c, block.get("content", ""), x + 14, inner_y, max_w - 28, font_size=14)
                y = y - panel_h - 12

        return y

    # Check if there's a two_column block at top level
    has_two_col = any(b.get("type") == "two_column" for b in body_blocks)

    if has_two_col:
        for block in body_blocks:
            if block.get("type") == "two_column":
                left_y = render_blocks(block["left"], MARGIN_LEFT, y, COL_W)
                right_y = render_blocks(block["right"], MARGIN_LEFT + COL_W + COL_GAP, y, COL_W)
                y = min(left_y, right_y)
            else:
                y = render_blocks([block], MARGIN_LEFT, y, CONTENT_W)
    else:
        y = render_blocks(body_blocks, MARGIN_LEFT, y, CONTENT_W)

    draw_footer(c)
    c.showPage()


def build_summary_page(c, points, brand="AI Influencer Accelerator"):
    """Final page — Summary."""
    draw_bg(c)
    y = draw_section_header(c, "Summary")

    y = draw_body_text(c, "Key takeaways from this guide:", MARGIN_LEFT, y, CONTENT_W)
    y -= 15

    y = draw_bullets(c, points, MARGIN_LEFT, y, CONTENT_W, bullet="→")
    y -= 30

    # Brand
    c.setFillColor(ACCENT_GREEN)
    c.setFont("Helvetica-Bold", BRAND_SIZE)
    tw = c.stringWidth(brand, "Helvetica-Bold", BRAND_SIZE)
    c.drawString((PAGE_W - tw) / 2, MARGIN_BOTTOM + 80, brand)

    draw_footer(c)
    c.showPage()


# ---------------------------------------------------------------------------
# TEMPLATE: AI-Influencer-Method-Free-Training
# ---------------------------------------------------------------------------

def generate_template_example(output_path=None):
    """Generate the template example PDF: AI-Influencer-Method-Free-Training."""
    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(__file__), "output", "AI-Influencer-Method-Free-Training.pdf"
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    logo_path = os.path.join(os.path.dirname(__file__), "PDF", "Course Logo.png")

    c = canvas.Canvas(output_path, pagesize=PAGE_SIZE)
    c.setTitle("AI Influencer Method Free Training")
    c.setAuthor("AI Influencer Accelerator")
    c.setCreator("AI Influencer Accelerator PDF Generator")
    c.setProducer("AI Influencer Accelerator")

    # -----------------------------------------------------------------------
    # PAGE 1 — COVER
    # -----------------------------------------------------------------------
    build_cover(
        c,
        title="AI Influencer Method\nFree Training",
        subtitle="The Complete Beginner's Blueprint to AI-Generated Influencer Income",
        logo_path=logo_path,
    )

    # -----------------------------------------------------------------------
    # PAGE 2 — TABLE OF CONTENTS
    # -----------------------------------------------------------------------
    toc = [
        (3,  "Intro: What Is the AI Influencer Method"),
        (4,  "Why AI Influencers Work"),
        (5,  "The Business Model Overview"),
        (6,  "Platform Selection: Where to Post"),
        (7,  "Content Creation Pipeline"),
        (8,  "Profile Setup: Identity & Trust"),
        (9,  "Growth Phase: First 30 Days"),
        (10, "Monetization: How Revenue Flows"),
        (11, "Common Mistakes & How to Avoid Them"),
        (12, "Scaling: From One Page to Many"),
        (13, "Tools & Resources"),
        (14, "Summary"),
    ]
    build_toc(c, toc)

    # -----------------------------------------------------------------------
    # PAGE 3 — INTRO
    # -----------------------------------------------------------------------
    build_content_page(c, "Intro: What Is the AI Influencer Method", [
        {"type": "text", "content": (
            "The AI Influencer Method is a system for building and monetizing "
            "social media pages using AI-generated personas. These personas look, "
            "act, and engage like real influencers but are entirely created and "
            "managed through artificial intelligence tools."
        )},
        {"type": "text", "content": (
            "This is not about catfishing or deception. This is a business model. "
            "The audience knows they are interacting with a curated persona. "
            "The value they receive is entertainment, attention, and content."
        )},
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
                "A replacement for understanding marketing",
            ]},
        ]},
    ])

    # -----------------------------------------------------------------------
    # PAGE 4 — WHY AI INFLUENCERS WORK
    # -----------------------------------------------------------------------
    build_content_page(c, "Why AI Influencers Work", [
        {"type": "two_column", "left": [
            {"type": "text", "content": (
                "Traditional influencer marketing requires a real person. "
                "That person has limitations: they age, they get tired, "
                "they have bad days, they have opinions that alienate audiences."
            )},
            {"type": "text", "content": (
                "AI influencers have none of these limitations. "
                "The persona is consistent. The content is controllable. "
                "The output is scalable."
            )},
            {"type": "text", "content": (
                "The market for parasocial relationships is massive and growing. "
                "People pay for connection, attention, and fantasy. "
                "AI personas deliver exactly that at scale."
            )},
        ], "right": [
            {"type": "subheader", "content": "Key Advantages"},
            {"type": "bullets", "items": [
                "No physical limitations on content output",
                "Consistent brand and persona across all content",
                "Scalable to multiple personas simultaneously",
                "Lower operating cost than traditional models",
                "Full creative control over appearance and messaging",
                "24/7 availability through automated chat systems",
            ]},
            {"type": "panel", "title": "Industry Growth", "content": (
                "The AI influencer market is projected to grow significantly "
                "year over year. Early movers have the strongest advantage."
            ), "border": "#39FF14"},
        ]},
    ])

    # -----------------------------------------------------------------------
    # PAGE 5 — BUSINESS MODEL
    # -----------------------------------------------------------------------
    build_content_page(c, "The Business Model Overview", [
        {"type": "text", "content": (
            "The business model is simple. Attention flows through a funnel. "
            "Free content creates interest. Interest creates followers. "
            "Followers convert to paying subscribers."
        )},
        {"type": "two_column", "left": [
            {"type": "subheader", "content": "Revenue Sources"},
            {"type": "bullets", "items": [
                "Fanvue / subscription platform monthly fees",
                "Pay-per-view (PPV) locked content",
                "Custom content requests via chat",
                "Tips and gifts from engaged fans",
                "Upsells through Telegram funnels",
            ]},
        ], "right": [
            {"type": "subheader", "content": "Traffic Flow"},
            {"type": "bullets", "items": [
                "Instagram / TikTok → Link in Bio",
                "Link in Bio → Free Telegram",
                "Free Telegram → Fanvue subscription",
                "Fanvue chat → Upsells and PPV",
            ], "bullet": "→"},
            {"type": "panel", "title": "Core Principle", "content": (
                "Build desire on free platforms. Delay commitment. "
                "Force the purchase decision at Fanvue where you control the experience."
            ), "border": "#39FF14"},
        ]},
    ])

    # -----------------------------------------------------------------------
    # PAGE 6 — PLATFORM SELECTION
    # -----------------------------------------------------------------------
    build_content_page(c, "Platform Selection: Where to Post", [
        {"type": "text", "content": (
            "Not all platforms are equal. Each has a role in the ecosystem. "
            "Instagram is the primary platform. Everything else supports it."
        )},
        {"type": "two_column", "left": [
            {"type": "subheader", "content": "Primary Platforms"},
            {"type": "bullets", "items": [
                "Instagram — Main traffic and brand hub",
                "Threads — Engagement and discovery engine",
                "TikTok — Secondary reach and content recycling",
                "Fanvue — Monetization endpoint",
            ]},
            {"type": "subheader", "content": "Support Platforms"},
            {"type": "bullets", "items": [
                "Telegram — Pre-sell funnel and warming layer",
                "Reddit — Niche viral exposure (opportunistic)",
                "Twitter/X — Brand presence and link distribution",
            ]},
        ], "right": [
            {"type": "panel", "title": "Platform Priority", "content": (
                "1. Instagram (mandatory)\n"
                "2. Threads (mandatory)\n"
                "3. Fanvue (mandatory)\n"
                "4. Telegram (highly recommended)\n"
                "5. TikTok (recommended)\n"
                "6. Reddit (optional)\n"
                "7. Twitter/X (optional)"
            ), "border": "#39FF14"},
        ]},
    ])

    # -----------------------------------------------------------------------
    # PAGE 7 — CONTENT CREATION PIPELINE
    # -----------------------------------------------------------------------
    build_content_page(c, "Content Creation Pipeline", [
        {"type": "text", "content": (
            "Content is the fuel of this business. Without consistent, high-quality "
            "content, nothing else works. The pipeline must be systematic."
        )},
        {"type": "two_column", "left": [
            {"type": "subheader", "content": "Step-by-Step Pipeline"},
            {"type": "bullets", "items": [
                "Generate base images using AI tools",
                "Edit and refine for consistency",
                "Create variations for different platforms",
                "Write captions that match platform tone",
                "Schedule posts using a content calendar",
                "Recycle top-performing content across platforms",
            ], "bullet": "→"},
        ], "right": [
            {"type": "subheader", "content": "Content Rules"},
            {"type": "bullets", "items": [
                "Same face across all images (consistency is critical)",
                "Lighting and background should vary naturally",
                "Never use the same image on two platforms the same day",
                "Instagram gets the best content first",
                "TikTok and Threads get recycled or secondary content",
            ]},
            {"type": "good_example", "content": "Consistent face, varied outfits, natural settings, clear face visible"},
            {"type": "bad_example", "content": "Different faces per post, over-filtered, blurry, no face visible"},
        ]},
    ])

    # -----------------------------------------------------------------------
    # PAGE 8 — PROFILE SETUP
    # -----------------------------------------------------------------------
    build_content_page(c, "Profile Setup: Identity & Trust", [
        {"type": "text", "content": (
            "Your profile is the first thing anyone sees. It must look human, "
            "trustworthy, and interesting within 2 seconds."
        )},
        {"type": "two_column", "left": [
            {"type": "subheader", "content": "Username Rules"},
            {"type": "bullets", "items": [
                "Human-sounding (first name + modifier)",
                "No random numbers or underscores",
                "No sexual or suggestive words",
                "Easy to remember and search",
            ]},
            {"type": "good_example", "content": "sofia.mae / emmaraexo / lilyy.ann"},
            {"type": "bad_example", "content": "hotmodel_2024 / xxxsofia / user83742"},
        ], "right": [
            {"type": "subheader", "content": "Bio Rules"},
            {"type": "bullets", "items": [
                "Short, casual, personality-driven",
                "No links during warmup phase",
                "No selling language early on",
                "Add link in bio only after 3 weeks",
            ]},
            {"type": "good_example", "content": "just a chill girl who likes coffee and sunsets"},
            {"type": "bad_example", "content": "Model | Content Creator | Link below | DM for collabs"},
        ]},
    ])

    # -----------------------------------------------------------------------
    # PAGE 9 — GROWTH PHASE
    # -----------------------------------------------------------------------
    build_content_page(c, "Growth Phase: First 30 Days", [
        {"type": "text", "content": (
            "The first 30 days determine everything. Rush this phase and the "
            "account gets flagged, shadow-limited, or banned. Patience is mandatory."
        )},
        {"type": "two_column", "left": [
            {"type": "subheader", "content": "Week 1-2: Warmup"},
            {"type": "bullets", "items": [
                "No posting for the first 3 days",
                "Scroll, like, and comment naturally",
                "Follow 5-10 accounts per day maximum",
                "Add profile picture on day 3-5",
                "First post on day 5-7",
                "2-3 posts per week maximum",
            ]},
        ], "right": [
            {"type": "subheader", "content": "Week 3-4: Activation"},
            {"type": "bullets", "items": [
                "Increase to 4-5 posts per week",
                "Start using Stories daily",
                "Begin Threads engagement (Phase 1)",
                "Add link in bio after week 3",
                "Start Telegram funnel setup",
                "Monitor analytics for shadow limits",
            ]},
        ]},
        {"type": "panel", "title": "Critical Rule", "content": (
            "If you rush the warmup, everything after it breaks. "
            "There are no shortcuts. Follow the timeline exactly."
        ), "border": "#FF3131"},
    ])

    # -----------------------------------------------------------------------
    # PAGE 10 — MONETIZATION
    # -----------------------------------------------------------------------
    build_content_page(c, "Monetization: How Revenue Flows", [
        {"type": "text", "content": (
            "Revenue does not come from posting. Revenue comes from the funnel. "
            "The funnel converts free attention into paid subscriptions."
        )},
        {"type": "two_column", "left": [
            {"type": "subheader", "content": "Conversion Path"},
            {"type": "bullets", "items": [
                "Free content builds desire",
                "Link in Bio captures interest",
                "Telegram warms cold traffic",
                "Fanvue captures the payment",
                "Chat upsells increase revenue per fan",
            ], "bullet": "→"},
            {"type": "panel", "title": "Expected Timeline", "content": (
                "First revenue: Week 4-6\n"
                "Consistent revenue: Month 2-3\n"
                "Scalable revenue: Month 4+"
            ), "border": "#39FF14"},
        ], "right": [
            {"type": "subheader", "content": "Revenue Optimization"},
            {"type": "bullets", "items": [
                "Chat quality determines revenue more than follower count",
                "Respond to new subscribers within 5 minutes",
                "Use emotional framing, not hard selling",
                "Prioritize whale management (top spenders)",
                "PPV content should escalate gradually",
            ]},
        ]},
    ])

    # -----------------------------------------------------------------------
    # PAGE 11 — COMMON MISTAKES
    # -----------------------------------------------------------------------
    build_content_page(c, "Common Mistakes & How to Avoid Them", [
        {"type": "two_column", "left": [
            {"type": "subheader", "content": "Mistakes That Kill Pages"},
            {"type": "bullets", "items": [
                "Posting before warmup is complete",
                "Using inconsistent AI faces",
                "Spamming links in captions or comments",
                "Posting explicit content on Instagram",
                "Ignoring shadow limit warnings",
                "Copy-pasting the same captions",
            ]},
            {"type": "bad_example", "content": (
                "Day 1: Create account\n"
                "Day 1: Post 5 photos\n"
                "Day 1: Add link in bio\n"
                "Day 2: Wonder why reach is zero"
            )},
        ], "right": [
            {"type": "subheader", "content": "What Winners Do Instead"},
            {"type": "bullets", "items": [
                "Follow the warmup timeline exactly",
                "Use one consistent AI model per page",
                "Deploy links only after trust is established",
                "Keep Instagram content safe and compliant",
                "Monitor analytics daily for red flags",
                "Test and iterate captions and content angles",
            ]},
            {"type": "good_example", "content": (
                "Week 1-2: Warmup only\n"
                "Week 3: First careful posts\n"
                "Week 4: Link in bio activated\n"
                "Week 5: First subscribers arrive"
            )},
        ]},
    ])

    # -----------------------------------------------------------------------
    # PAGE 12 — SCALING
    # -----------------------------------------------------------------------
    build_content_page(c, "Scaling: From One Page to Many", [
        {"type": "text", "content": (
            "Once the first page is profitable and stable, the system is ready to scale. "
            "Scaling means running multiple AI personas simultaneously."
        )},
        {"type": "two_column", "left": [
            {"type": "subheader", "content": "When to Scale"},
            {"type": "bullets", "items": [
                "First page has consistent revenue for 30+ days",
                "Content pipeline is systematized",
                "Chat operations are handled or delegated",
                "You understand the platform algorithms",
            ]},
        ], "right": [
            {"type": "subheader", "content": "How to Scale"},
            {"type": "bullets", "items": [
                "Create a new persona with a different niche/look",
                "Use separate devices or browser profiles",
                "Never link accounts to each other",
                "Hire chatters for fan management",
                "Replicate the exact same funnel structure",
            ]},
        ]},
        {"type": "panel", "title": "Scaling Rule", "content": (
            "Never scale a broken system. Fix the first page completely before "
            "adding a second. A broken process multiplied by 5 is 5x the problems."
        ), "border": "#39FF14"},
    ])

    # -----------------------------------------------------------------------
    # PAGE 13 — TOOLS & RESOURCES
    # -----------------------------------------------------------------------
    build_content_page(c, "Tools & Resources", [
        {"type": "two_column", "left": [
            {"type": "subheader", "content": "Content Generation"},
            {"type": "bullets", "items": [
                "AI image generation tools",
                "Photo editing software",
                "Face consistency tools",
                "Background variation tools",
            ]},
            {"type": "subheader", "content": "Platform Management"},
            {"type": "bullets", "items": [
                "Content scheduling tools",
                "Analytics monitoring",
                "Multi-account management",
                "VPN and device separation",
            ]},
        ], "right": [
            {"type": "subheader", "content": "Monetization"},
            {"type": "bullets", "items": [
                "Fanvue (primary platform)",
                "Telegram (free funnel)",
                "AllMyLinks / Linktree (link in bio)",
            ]},
            {"type": "subheader", "content": "Operations"},
            {"type": "bullets", "items": [
                "Chat management systems",
                "Chatter hiring and training SOPs",
                "Revenue tracking spreadsheets",
                "Content calendar templates",
            ]},
        ]},
    ])

    # -----------------------------------------------------------------------
    # PAGE 14 — SUMMARY
    # -----------------------------------------------------------------------
    build_summary_page(c, [
        "The AI Influencer Method is a real business that requires real effort",
        "Follow the warmup phase exactly — no shortcuts",
        "Instagram is the primary platform, everything else supports it",
        "Content consistency (same face) is non-negotiable",
        "Revenue comes from the funnel, not from posting",
        "Chat quality determines profit more than follower count",
        "Scale only after the first page is profitable and stable",
        "Patience in the first 30 days determines everything after",
    ])

    c.save()
    print(f"Generated: {output_path}")
    return output_path


# ---------------------------------------------------------------------------
# JSON-DRIVEN GENERATION
# ---------------------------------------------------------------------------

def generate_from_json(config_path, output_path=None):
    """
    Generate a PDF from a JSON content file.

    JSON Schema:
    {
        "title": "PDF TITLE",
        "subtitle": "Subtitle text",
        "brand": "AI Influencer Accelerator",
        "output_filename": "My-PDF-Name.pdf",
        "sections": [
            {
                "header": "SECTION TITLE",
                "blocks": [
                    {"type": "text", "content": "..."},
                    {"type": "bullets", "items": ["...", "..."]},
                    {"type": "subheader", "content": "..."},
                    {"type": "good_example", "content": "..."},
                    {"type": "bad_example", "content": "..."},
                    {"type": "panel", "title": "...", "content": "...", "border": "#39FF14"},
                    {"type": "two_column", "left": [...blocks], "right": [...blocks]}
                ]
            }
        ],
        "summary_points": ["...", "..."]
    }
    """
    with open(config_path, "r") as f:
        config = json.load(f)

    title = config["title"]
    subtitle = config.get("subtitle", "")
    brand = config.get("brand", "AI Influencer Accelerator")
    sections = config["sections"]
    summary_points = config.get("summary_points", [])

    if output_path is None:
        filename = config.get("output_filename", title.replace(" ", "-") + ".pdf")
        output_path = os.path.join(os.path.dirname(__file__), "output", filename)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    logo_path = os.path.join(os.path.dirname(__file__), "PDF", "Course Logo.png")

    c = canvas.Canvas(output_path, pagesize=PAGE_SIZE)
    c.setTitle(title)
    c.setAuthor(brand)
    c.setCreator("AI Influencer Accelerator PDF Generator")
    c.setProducer(brand)

    # Cover
    build_cover(c, title=title, subtitle=subtitle, brand=brand, logo_path=logo_path)

    # TOC
    toc = [(i + 3, s["header"]) for i, s in enumerate(sections)]
    build_toc(c, toc)

    # Content pages
    for section in sections:
        build_content_page(c, section["header"], section["blocks"])

    # Summary
    if summary_points:
        build_summary_page(c, summary_points, brand=brand)

    c.save()
    print(f"Generated: {output_path}")
    return output_path


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
