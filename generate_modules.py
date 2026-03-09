#!/usr/bin/env python3
"""
Split module JSON configs into individual lesson PDFs in separate folders.

Output structure:
  output/
    Module 1 - The Basics/
      Overview.pdf
      Lesson 1 - The AI Influencer Method.pdf
      ...
    Module 2 - Base Model Creation/
      Overview.pdf
      Lesson 1 - Choosing Your Niche & Persona.pdf
      ...
"""

import json
import os
import re
import sys
from pathlib import Path
from generate_pdf import generate_pdf, BASE_DIR, OUTPUT_DIR


# Module metadata: maps JSON filename to clean module name
MODULE_ORDER = [
    ("Module-01-The-Basics.json", "Module 1 - The Basics"),
    ("Module-02-Base-Model-Creation.json", "Module 2 - Base Model Creation"),
    ("Module-03-SFW-Image-Creation.json", "Module 3 - SFW Image Creation"),
    ("Module-04-SFW-Video-Creation.json", "Module 4 - SFW Video Creation"),
    ("Module-05-Phone-Setup-Warmup.json", "Module 5 - Phone Setup & Warmup"),
    ("Module-06-Growing-Social-Media.json", "Module 6 - Growing Social Media"),
    ("Module-07-Scaling-Social-Media.json", "Module 7 - Scaling Social Media"),
    ("Module-08-Account-Safety.json", "Module 8 - Account Safety & Precautions"),
    ("Module-09-Followers-To-Paying-Fans.json", "Module 9 - Turning Followers into Paying Fans"),
    ("Module-10-Continued-On-Discord.json", "Module 10 - Continued on Discord"),
]

# Overview descriptions for each module
MODULE_OVERVIEWS = {
    1: {
        "description": "This module covers the complete foundation of the AI Influencer Method. You will understand what this business model is, why it works, how the revenue funnel operates, which platforms matter, and what tools you need before starting.",
        "outcomes": [
            "Understand the AI Influencer business model end to end",
            "Know the revenue funnel from free content to paying subscribers",
            "Identify which platforms are mandatory vs optional",
            "Have a clear picture of the tools and resources needed to start",
        ],
    },
    2: {
        "description": "In this module you will create your AI influencer from scratch. You will choose a niche, define a persona, generate your base model, lock in face and style consistency, and build a full content library ready for posting.",
        "outcomes": [
            "Choose a profitable niche and define your persona's identity",
            "Generate a realistic base model using AI image tools",
            "Ensure face and style consistency across all generated images",
            "Build a content library with enough material to start posting",
        ],
    },
    3: {
        "description": "This module teaches you how to produce high-quality SFW images for social media. You will master reference image workflows, prompt engineering, editing and refining AI outputs, and the specific image rules each platform enforces.",
        "outcomes": [
            "Use reference images to guide consistent AI generation",
            "Write precise prompts that produce the images you need",
            "Edit and refine AI images to look natural and polished",
            "Follow platform-specific image rules to avoid takedowns",
        ],
    },
    4: {
        "description": "This module covers AI video creation using Kling. You will learn motion control fundamentals, how to write effective video prompts, and how to export and optimize videos for each social media platform.",
        "outcomes": [
            "Understand how Kling generates AI video from images",
            "Write video prompts that produce natural, engaging motion",
            "Control motion intensity and camera movement effectively",
            "Export and format videos correctly for each platform",
        ],
    },
    5: {
        "description": "Before you post anything, your accounts need to be set up correctly and warmed up properly. This module walks you through device setup, account creation, the warmup protocol, and the mistakes that get new accounts banned immediately.",
        "outcomes": [
            "Set up a dedicated phone or device for your AI persona",
            "Create and configure accounts on all required platforms",
            "Follow the warmup protocol to build account trust",
            "Avoid the specific mistakes that trigger bans on new accounts",
        ],
    },
    6: {
        "description": "Now that your accounts are warmed up, it is time to grow. This module gives you the growth strategy for every platform: Instagram, Threads, Reddit, TikTok, Twitter/X, and how to coordinate across all of them.",
        "outcomes": [
            "Execute platform-specific growth strategies for Instagram, Threads, Reddit, TikTok, and Twitter/X",
            "Understand what type of content performs best on each platform",
            "Use cross-platform coordination to multiply your reach",
            "Build a consistent posting and engagement routine",
        ],
    },
    7: {
        "description": "Growth gets you followers. Scaling gets you results. This module covers posting cadence, the hook that converts viewers into followers, geo-targeting for maximum reach, and how to scale across multiple accounts safely.",
        "outcomes": [
            "Optimize your posting cadence and scheduling for maximum visibility",
            "Use proven hooks that convert passive viewers into followers",
            "Implement geo-targeting and distribution control for better reach",
            "Scale to multiple accounts without triggering platform flags",
        ],
    },
    8: {
        "description": "Accounts are your most valuable asset. This module teaches you how platform bans and shadowbans work, the daily safety habits that protect you, what to do if you get banned, and the rules for running multiple accounts safely.",
        "outcomes": [
            "Understand how bans and shadowbans work on each platform",
            "Build daily safety habits that keep your accounts protected",
            "Know exactly what to do if an account gets banned",
            "Follow multi-account safety rules to avoid linked bans",
        ],
    },
    9: {
        "description": "Followers are worth nothing if they do not convert. This module covers funnel psychology, link-in-bio architecture, Telegram strategy, content progression ladders, subscription pricing, and automated welcome messages that turn free attention into paid subscribers.",
        "outcomes": [
            "Understand the psychology behind why followers become paying fans",
            "Build a link-in-bio funnel that drives conversions",
            "Set up your subscription page and Telegram channel for maximum retention",
            "Implement a content progression ladder and pricing strategy that converts",
        ],
    },
    10: {
        "description": "The course continues on Discord where you will access NSFW content creation modules, advanced strategies, live support, and the private community. This lesson tells you exactly how to access everything.",
        "outcomes": [
            "Access the private Discord community",
            "Unlock NSFW content creation modules and advanced strategies",
            "Get live support and connect with other members",
        ],
    },
}


def extract_lesson_title(header):
    """Extract clean lesson title from section header.

    e.g. 'Lesson 1: What Is the AI Influencer Method' -> 'What Is the AI Influencer Method'
    """
    match = re.match(r"Lesson\s+\d+:\s*(.+)", header, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return header


def extract_lesson_number(header):
    """Extract lesson number from section header."""
    match = re.match(r"Lesson\s+(\d+)", header, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def sanitize_filename(name):
    """Make a string safe for use as a filename."""
    # Remove characters that are problematic in filenames
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip('. ')
    return name


def build_overview_config(module_num, module_label, subtitle, sections, logo_path,
                          merge_lessons=False):
    """Build a config dict for the module overview PDF.

    If merge_lessons is True, the lesson content sections are appended after the
    overview page so the module becomes a single PDF.
    """
    overview = MODULE_OVERVIEWS.get(module_num, {})
    description = overview.get("description", "")
    outcomes = overview.get("outcomes", [])

    # Build the overview content blocks
    blocks = []
    blocks.append({"type": "text", "content": description})

    if merge_lessons:
        # No lesson listing needed — the content follows directly
        blocks.append({
            "type": "two_column",
            "left": [
                {"type": "subheader", "content": "What You Will Learn"},
                {"type": "bullets", "items": outcomes},
            ],
            "right": [],
        })
    else:
        # Build lesson listing bullets
        lesson_bullets = []
        for i, section in enumerate(sections):
            num = extract_lesson_number(section["header"]) or (i + 1)
            title = extract_lesson_title(section["header"])
            lesson_bullets.append(f"Lesson {num}: {title}")

        blocks.append({
            "type": "two_column",
            "left": [
                {"type": "subheader", "content": "What You Will Learn"},
                {"type": "bullets", "items": outcomes},
            ],
            "right": [
                {"type": "subheader", "content": "Lessons in This Module"},
                {"type": "bullets", "items": lesson_bullets, "bullet": "→"},
            ],
        })

    all_sections = [{"header": "Module Overview", "blocks": blocks}]

    if merge_lessons:
        all_sections.extend(sections)

    config = {
        "title": "Overview",
        "subtitle": subtitle,
        "module_label": module_label,
        "lesson_label": "",
        "skip_toc": True,
        "skip_summary": True,
        "sections": all_sections,
    }

    if logo_path and os.path.exists(logo_path):
        config["logo_path"] = logo_path

    return config


def generate_all_modules():
    """Split all modules into individual lesson PDFs."""
    content_dir = BASE_DIR / "content"
    default_logo = BASE_DIR / "PDF" / "Course_Logo.png"
    logo_path = str(default_logo) if default_logo.exists() else ""

    for json_filename, module_folder_name in MODULE_ORDER:
        json_path = content_dir / json_filename
        if not json_path.exists():
            print(f"  SKIP: {json_filename} not found")
            continue

        with open(json_path, "r") as f:
            module_config = json.load(f)

        sections = module_config["sections"]
        subtitle = module_config.get("subtitle", "")

        # Extract module number for the label
        match = re.match(r"Module\s*(\d+)", module_folder_name)
        module_num = int(match.group(1)) if match else 0
        module_label = f"Module {module_num}"

        # Create module output folder
        module_dir = OUTPUT_DIR / module_folder_name
        os.makedirs(str(module_dir), exist_ok=True)

        print(f"\n{'='*60}")
        print(f"  {module_folder_name} ({len(sections)} lessons)")
        print(f"{'='*60}")

        # Modules with a single lesson merge overview + lesson into one PDF
        single_pdf_modules = {1, 10}

        if module_num in single_pdf_modules:
            # Merged: overview page + lesson content in one PDF
            overview_config = build_overview_config(
                module_num, module_label, subtitle, sections, logo_path,
                merge_lessons=True,
            )
            merged_title = extract_lesson_title(sections[0]["header"])
            safe_title = sanitize_filename(merged_title)
            merged_path = str(module_dir / f"{safe_title}.pdf")
            generate_pdf(overview_config, merged_path)
        else:
            # Generate Overview PDF first
            overview_config = build_overview_config(
                module_num, module_label, subtitle, sections, logo_path
            )
            overview_path = str(module_dir / "Overview.pdf")
            generate_pdf(overview_config, overview_path)

            # Generate individual lesson PDFs
            for i, section in enumerate(sections):
                lesson_num = extract_lesson_number(section["header"]) or (i + 1)
                lesson_title = extract_lesson_title(section["header"])

                # Use section-level subtitle override if provided
                lesson_subtitle = section.get("subtitle", subtitle)

                lesson_config = {
                    "title": lesson_title,
                    "subtitle": lesson_subtitle,
                    "module_label": module_label,
                    "lesson_label": f"Lesson {lesson_num}",
                    "skip_toc": True,
                    "skip_summary": True,
                    "sections": [section],
                }

                if logo_path:
                    lesson_config["logo_path"] = logo_path

                safe_title = sanitize_filename(lesson_title)
                pdf_filename = f"Lesson {lesson_num} - {safe_title}.pdf"
                output_path = str(module_dir / pdf_filename)

                generate_pdf(lesson_config, output_path)

    print(f"\n{'='*60}")
    print(f"  All modules generated!")
    print(f"{'='*60}")


if __name__ == "__main__":
    generate_all_modules()
