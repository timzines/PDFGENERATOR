#!/usr/bin/env python3
"""Generate enhanced luxury-themed PDFs from extracted SOP text files."""

import os
from weasyprint import HTML

OUTPUT_DIR = "output"
CHAPTERS_DIR = os.path.join(OUTPUT_DIR, "chapters")
os.makedirs(CHAPTERS_DIR, exist_ok=True)

# ── Theme CSS ──────────────────────────────────────────────────────────────
CSS = """
@page {
    size: A4;
    margin: 0;
}
@page :first {
    margin: 0;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    background: #0d0d0d;
    color: #e8e0d8;
    line-height: 1.7;
    font-size: 11pt;
}

/* ── Cover Page ── */
.cover {
    page-break-after: always;
    background: linear-gradient(160deg, #0d0d0d 0%, #1a1018 40%, #1f0f1a 70%, #0d0d0d 100%);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 60px 50px;
    position: relative;
    overflow: hidden;
}
.cover::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, transparent, #c9919b, #e8b4b8, #c9919b, transparent);
}
.cover::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, transparent, #c9919b, #e8b4b8, #c9919b, transparent);
}
.cover .brand {
    font-size: 11pt;
    letter-spacing: 6px;
    text-transform: uppercase;
    color: #c9919b;
    margin-bottom: 50px;
    font-weight: 300;
}
.cover h1 {
    font-size: 32pt;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 20px;
    line-height: 1.2;
}
.cover .subtitle {
    font-size: 12pt;
    color: #b8a0a6;
    letter-spacing: 2px;
    font-weight: 300;
    margin-bottom: 60px;
}
.cover .divider {
    width: 80px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #c9919b, transparent);
    margin: 0 auto 40px;
}
.cover .footer-text {
    font-size: 8pt;
    color: #5a4a50;
    letter-spacing: 2px;
    text-transform: uppercase;
    position: absolute;
    bottom: 40px;
}

/* ── Table of Contents ── */
.toc {
    page-break-after: always;
    background: #0d0d0d;
    padding: 60px 55px;
    min-height: 100vh;
}
.toc h2 {
    font-size: 18pt;
    color: #c9919b;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 40px;
    padding-bottom: 15px;
    border-bottom: 1px solid #2a1f24;
}
.toc-item {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 12px 0;
    border-bottom: 1px solid #1a1418;
}
.toc-num {
    color: #c9919b;
    font-weight: 700;
    font-size: 10pt;
    min-width: 30px;
}
.toc-title {
    flex: 1;
    color: #e8e0d8;
    font-size: 10.5pt;
    padding-left: 10px;
}

/* ── Content Pages ── */
.page {
    page-break-before: always;
    background: #0d0d0d;
    padding: 55px;
    min-height: 100vh;
    position: relative;
}
.page::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px;
    height: 100%;
    background: linear-gradient(180deg, #c9919b, transparent 70%);
}
.page h2 {
    font-size: 16pt;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 8px;
    padding-left: 15px;
    border-left: 3px solid #c9919b;
}
.page h3 {
    font-size: 12pt;
    color: #c9919b;
    letter-spacing: 1px;
    margin: 25px 0 12px;
    text-transform: uppercase;
}
.page p {
    margin-bottom: 14px;
    color: #d4ccc6;
    text-align: justify;
}
.page .highlight {
    background: linear-gradient(135deg, #1a1018, #1f1520);
    border-left: 3px solid #c9919b;
    padding: 16px 20px;
    margin: 18px 0;
    border-radius: 0 6px 6px 0;
    color: #e8d8dc;
    font-style: italic;
}
.page ul {
    list-style: none;
    margin: 12px 0 18px 0;
    padding: 0;
}
.page ul li {
    padding: 6px 0 6px 22px;
    position: relative;
    color: #d4ccc6;
}
.page ul li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 13px;
    width: 8px;
    height: 8px;
    background: #c9919b;
    border-radius: 50%;
}
.page .key-point {
    background: #151015;
    border: 1px solid #2a1f24;
    border-radius: 6px;
    padding: 18px 22px;
    margin: 16px 0;
}
.page .key-point strong {
    color: #c9919b;
}

/* ── Summary Page ── */
.summary-page {
    page-break-before: always;
    background: linear-gradient(160deg, #0d0d0d 0%, #1a1018 50%, #0d0d0d 100%);
    padding: 55px;
    min-height: 100vh;
}
.summary-page h2 {
    font-size: 18pt;
    color: #c9919b;
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-bottom: 30px;
    text-align: center;
}
.summary-page p {
    margin-bottom: 16px;
    color: #d4ccc6;
    text-align: justify;
    line-height: 1.8;
}
.summary-page .closing {
    text-align: center;
    margin-top: 40px;
    font-size: 13pt;
    color: #c9919b;
    font-style: italic;
    letter-spacing: 1px;
}

/* ── Rights Footer ── */
.rights {
    text-align: center;
    font-size: 7pt;
    color: #3a2a30;
    margin-top: 30px;
    letter-spacing: 1px;
}
"""

RIGHTS = "All materials are strictly protected under AI Influencer Accelerator\u00ae rights"


def clean_line(line):
    """Remove source markers and rights notices from a line."""
    line = line.replace("All materials are strictly protected under AI Influencer Accelerator\u00ae rights", "")
    return line.strip()


def build_cover(title, subtitle, brand="AI Influencer Accelerator"):
    return f"""
    <div class="cover">
        <div class="brand">{brand}</div>
        <div class="divider"></div>
        <h1>{title}</h1>
        <div class="subtitle">{subtitle}</div>
        <div class="divider"></div>
        <div class="footer-text">{RIGHTS}</div>
    </div>"""


def build_toc(chapters):
    items = ""
    for i, ch in enumerate(chapters, 1):
        items += f'<div class="toc-item"><span class="toc-num">{i:02d}</span><span class="toc-title">{ch}</span></div>\n'
    return f"""
    <div class="toc">
        <h2>Table of Contents</h2>
        {items}
    </div>"""


def build_section(title, content_html):
    return f"""
    <div class="page">
        <h2>{title}</h2>
        {content_html}
        <div class="rights">{RIGHTS}</div>
    </div>"""


def build_summary(content_html):
    return f"""
    <div class="summary-page">
        <h2>Summary</h2>
        {content_html}
    </div>"""


def text_to_html_content(text):
    """Convert plain text paragraph to styled HTML with bullet detection."""
    lines = text.strip().split('\n')
    html = ""
    in_list = False
    for line in lines:
        line = clean_line(line)
        if not line:
            if in_list:
                html += "</ul>"
                in_list = False
            continue
        # Detect bullet-like lines
        if line.startswith(('-', '\u2022')) or (len(line) < 100 and not line.endswith('.')):
            # Check if it looks like a list item
            cleaned = line.lstrip('-\u2022 ')
            if cleaned and len(cleaned) < 120:
                if not in_list:
                    html += "<ul>"
                    in_list = True
                html += f"<li>{cleaned}</li>"
                continue
        if in_list:
            html += "</ul>"
            in_list = False
        # Detect highlight/quote lines
        if line.startswith('"') or line.startswith('\u201c'):
            html += f'<div class="highlight">{line}</div>'
        else:
            html += f"<p>{line}</p>"
    if in_list:
        html += "</ul>"
    return html


def parse_pages(filepath):
    """Parse extracted text file into list of (page_num, lines) tuples."""
    pages = []
    current_page = []
    current_num = 0
    with open(filepath, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('=== PAGE '):
                if current_page:
                    pages.append((current_num, '\n'.join(current_page)))
                try:
                    current_num = int(line.split('PAGE ')[1].split(' ===')[0])
                except:
                    current_num += 1
                current_page = []
            elif line.startswith('SOURCE:'):
                continue
            else:
                current_page.append(line)
        if current_page:
            pages.append((current_num, '\n'.join(current_page)))
    return pages


def generate_pdf(html_content, output_path):
    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{html_content}</body></html>"""
    HTML(string=full_html).write_pdf(output_path)
    print(f"  Generated: {output_path}")


# ══════════════════════════════════════════════════════════════════════════════
# SOP Definitions - each defines title, subtitle, source file, and sections
# ══════════════════════════════════════════════════════════════════════════════

SOPS = [
    {
        "file": "extracted/AI_Funelling_SOP_2.txt",
        "output": "AI_Funelling_SOP.pdf",
        "title": "AI FUNELLING SOP",
        "subtitle": "Traffic Conversion & Monetization Framework",
        "sections": [
            ("Foreword: Funnel Psychology", [3]),
            ("Funnel Overview: Traffic Flow", [4]),
            ("Funnel Activation Timing", [5]),
            ("Link in Bio Architecture", [6, 7]),
            ("Free Telegram Funnel", [8]),
            ("Telegram Content Rules", [9]),
            ("Instagram Highlight Funnel", [10]),
            ("Funnel Aggression & Compliance", [11]),
            ("Funnel Mistakes & Visual Examples", [12]),
            ("Summary", [13]),
        ]
    },
    {
        "file": "extracted/AI_OFM_Chatting_Systems_1.txt",
        "output": "AI_OFM_Chatting_Systems.pdf",
        "title": "AI OFM CHATTING SYSTEM",
        "subtitle": "Chatting Structure & Revenue Logic",
        "sections": [
            ("Why Chatting Creates Revenue", [3]),
            ("Core Philosophy of Chat Systems", [4]),
            ("Fan Psychology and Motivation", [5]),
            ("Message Priority and Speed", [6]),
            ("New Subscriber Handling", [7]),
            ("Fan Profiling System", [8]),
            ("Nickname & Memory System", [9]),
            ("Timing & Context System", [10]),
            ("Chat Flow Structure", [11]),
            ("First Sale Logic", [12]),
            ("Upsell Logic", [13]),
            ("Objection Handling", [14]),
            ("Whale Management", [15]),
            ("Final Principles", [16]),
        ]
    },
    {
        "file": "extracted/Ai_Fanvue_Page_SOP_1.txt",
        "output": "AI_Fanvue_Page_SOP.pdf",
        "title": "AI FANVUE PAGE SOP",
        "subtitle": "Profile and Content Structure Manual",
        "sections": [
            ("Intro: The Role of the Fanvue Page", [3]),
            ("Banner: Visual First Impression", [4, 5]),
            ("Bio: Identity and Emotional Hook", [6, 7]),
            ("Posts for Free: Trust and Curiosity", [8, 9]),
            ("Posts for Subscribers: Intimacy & Value", [10, 11]),
            ("PPV: Fantasy and High Value", [12, 13]),
            ("Automated Free Follower Messages", [14]),
            ("Automated Subscriber Messages", [15]),
            ("Subscriber Pricing", [16]),
            ("Content Progression Model", [17]),
            ("Visual Consistency", [18]),
            ("Summary", [19]),
        ]
    },
    {
        "file": "extracted/Chatter_hiring_sop_4.txt",
        "output": "Chatter_Hiring_SOP.pdf",
        "title": "CHATTER HIRING SOP",
        "subtitle": "Recruitment and Vetting Manual",
        "sections": [
            ("Intro: Why Hiring Matters", [3]),
            ("Where to Find Chatters", [4]),
            ("First Screening", [5]),
            ("Interview Process", [6]),
            ("English and Skill Testing", [7]),
            ("Observation Period", [8]),
            ("Access Control", [9]),
            ("Payment Structure", [10]),
            ("Performance Tracking", [11]),
            ("Risk and Trust Management", [12]),
            ("Summary", [13]),
        ]
    },
    {
        "file": "extracted/INSTAGRAM_&_THREADS_SECRET_STRATEGY_1.txt",
        "output": "Instagram_Threads_Secret_Strategy.pdf",
        "title": "INSTAGRAM & THREADS\nSECRET STRATEGY",
        "subtitle": "Full Warmup, Growth & Monetization SOP",
        "sections": [
            ("Foreword: What This System Solves", [3]),
            ("Platform Roles & Traffic Logic", [4]),
            ("Warmup Phase: What To Do Day by Day", [5]),
            ("Threads Phase 1: Exact Execution", [6, 7]),
            ("Threads Phase 2: How to Scale", [8, 9, 10]),
            ("Instagram Reels: Step by Step", [11]),
            ("Instagram Content: Exact Rules", [12]),
            ("Geo Targeting & Distribution Control", [13, 14, 15, 16]),
            ("Failure Recovery & Rules", [17]),
            ("Conclusion", [18]),
        ]
    },
    {
        "file": "extracted/Reddit_SOP.txt",
        "output": "Reddit_SOP.pdf",
        "title": "REDDIT SOP",
        "subtitle": "Niche Traffic & Community Infiltration Manual",
        "sections": [
            ("Intro: The Role of Reddit", [3]),
            ("Profile: First Impression", [4]),
            ("Bio: Identity and Safety", [5]),
            ("Posts: Trust and Visibility", [6]),
            ("Comments: Relationship and Karma", [7]),
            ("Targeting: Subreddits and Niches", [8]),
            ("Warm Up: Trust and History", [9]),
            ("Posting Phase: After Warm Up", [10]),
            ("Content Progression Model", [11]),
            ("Visual Consistency", [12]),
            ("End Summary", [13]),
        ]
    },
    {
        "file": "extracted/TikTok_SOP.txt",
        "output": "TikTok_SOP.pdf",
        "title": "TIKTOK SOP",
        "subtitle": "Profile and Content Structure Manual",
        "sections": [
            ("Intro: The Role of TikTok", [3]),
            ("Platform Risk: TikTok vs Instagram", [4]),
            ("Account Setup: First Signals", [5]),
            ("Bio & Profile: Identity and Trust", [6]),
            ("Warm Up Phase: New Account Protocol", [7]),
            ("Posting Phase: After Warm Up", [8]),
            ("Daily Behavior: Trust Signals", [9]),
            ("Multi-Account Safety", [10]),
            ("Content Formats: Safe Reach & Carousels", [11]),
            ("Scale Strategy and Expectations", [12]),
            ("End Summary", [13]),
        ]
    },
    {
        "file": "extracted/X_Twitter_Growth_and_Traffic_Manual.txt",
        "output": "X_Twitter_Growth_Traffic_Manual.pdf",
        "title": "X (TWITTER) GROWTH &\nTRAFFIC MANUAL",
        "subtitle": "Discovery, Reputation & Audience Building",
        "sections": [
            ("Intro: The Role of X", [3]),
            ("Profile: Visual First Impression", [4, 5]),
            ("Bio: Identity and Emotional Hook", [6]),
            ("Posts: Visibility and Watch Time", [7, 8]),
            ("Replies: Reach and Relationship", [9]),
            ("Targeting: Audience and Pools", [10]),
            ("Warm Up: Trust and Reputation", [11]),
            ("Safety and Account Health", [12]),
            ("Premium and Visibility", [13]),
            ("Content Progression Model", [14]),
            ("Visual Consistency", [15]),
            ("Summary", [16]),
        ]
    },
]


def generate_sop_pdf(sop_def):
    """Generate a single SOP PDF."""
    pages = parse_pages(sop_def["file"])
    page_map = {num: text for num, text in pages}

    chapter_names = [s[0] for s in sop_def["sections"]]

    # Build HTML
    html = build_cover(sop_def["title"], sop_def["subtitle"])
    html += build_toc(chapter_names)

    for section_title, page_nums in sop_def["sections"]:
        combined_text = "\n".join(page_map.get(p, "") for p in page_nums)
        content_html = text_to_html_content(combined_text)

        if "summary" in section_title.lower() or "conclusion" in section_title.lower() or "final" in section_title.lower():
            html += build_summary(content_html)
        else:
            html += build_section(section_title, content_html)

    generate_pdf(html, os.path.join(OUTPUT_DIR, sop_def["output"]))
    return page_map


def generate_chatting_chapters(sop_def):
    """Generate individual chapter PDFs for AI OFM Chatting Systems."""
    pages = parse_pages(sop_def["file"])
    page_map = {num: text for num, text in pages}

    for section_title, page_nums in sop_def["sections"]:
        combined_text = "\n".join(page_map.get(p, "") for p in page_nums)
        content_html = text_to_html_content(combined_text)

        html = build_cover(section_title, "AI OFM Chatting Systems")

        if "summary" in section_title.lower() or "final" in section_title.lower():
            html += build_summary(content_html)
        else:
            html += build_section(section_title, content_html)

        safe_name = section_title.replace(":", "").replace("&", "and").replace(" ", "_")
        filename = f"Chatting_{safe_name}.pdf"
        generate_pdf(html, os.path.join(CHAPTERS_DIR, filename))


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating enhanced PDFs...")
    print()

    for sop in SOPS:
        print(f"[*] {sop['title'].replace(chr(10), ' ')}")
        generate_sop_pdf(sop)

    print()
    print("[*] Generating AI OFM Chatting Systems chapter splits...")
    generate_chatting_chapters(SOPS[1])

    print()
    print("Done! All PDFs generated in output/")
