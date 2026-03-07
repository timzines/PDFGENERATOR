#!/usr/bin/env python3
"""
Split module JSON configs into individual lesson PDFs in separate folders.

Output structure:
  output/
    Module 1 - The Basics/
      Lesson 1 - What Is the AI Influencer Method.pdf
      Lesson 2 - Why AI Influencers Work.pdf
      ...
    Module 2 - Base Model Creation/
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
    ("Module-09-Followers-To-Paying-Fans.json", "Module 9 - Followers to Paying Fans"),
    ("Module-10-Continued-On-Discord.json", "Module 10 - Continued on Discord"),
]


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


def generate_all_modules():
    """Split all modules into individual lesson PDFs."""
    content_dir = BASE_DIR / "content"

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

        for i, section in enumerate(sections):
            lesson_num = extract_lesson_number(section["header"]) or (i + 1)
            lesson_title = extract_lesson_title(section["header"])

            # Build individual lesson config
            lesson_config = {
                "title": f"Lesson {lesson_num}\n{lesson_title}",
                "subtitle": subtitle,
                "module_label": module_label,
                "skip_toc": True,
                "skip_summary": True,
                "sections": [section],
            }

            # Find logo
            default_logo = BASE_DIR / "PDF" / "Course_Logo.png"
            if default_logo.exists():
                lesson_config["logo_path"] = str(default_logo)

            # Output path
            safe_title = sanitize_filename(lesson_title)
            pdf_filename = f"Lesson {lesson_num} - {safe_title}.pdf"
            output_path = str(module_dir / pdf_filename)

            generate_pdf(lesson_config, output_path)

    print(f"\n{'='*60}")
    print(f"  All modules generated!")
    print(f"{'='*60}")


if __name__ == "__main__":
    generate_all_modules()
