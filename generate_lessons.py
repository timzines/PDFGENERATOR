#!/usr/bin/env python3
"""
Generate individual lesson PDFs from module JSON configs.

Each section in a module JSON becomes its own lesson PDF, using the same
dark-themed styling as the module-level PDFs.
"""

import json
import os
import re
import sys
from pathlib import Path

from generate_pdf import generate_pdf, BASE_DIR, OUTPUT_DIR

CONTENT_DIR = BASE_DIR / "content"


def sanitize_filename(name):
    """Remove characters that are invalid in filenames."""
    return re.sub(r'[/\\:*?"<>|]', '', name)


def extract_lesson_name(header):
    """Extract clean lesson name from section header like 'Lesson 1: Choosing Your Niche & Persona'."""
    # Remove "Lesson N: " prefix for the title, keep for filename
    match = re.match(r'(Lesson \d+):\s*(.*)', header)
    if match:
        return match.group(1), sanitize_filename(match.group(2))
    return None, sanitize_filename(header)


def get_module_folder(config):
    """Get the module output folder from the config's output_filename."""
    output_filename = config.get("output_filename", "")
    if "/" in output_filename:
        return output_filename.split("/")[0]
    return None


def generate_overview_config(module_config, module_folder):
    """Generate an Overview PDF config from the module config."""
    title_lines = module_config["title"].split("\n")
    module_num_line = title_lines[0] if title_lines else "Module"
    module_name = title_lines[1] if len(title_lines) > 1 else ""

    # Overview has the TOC and a brief intro
    sections = []
    section_list = module_config.get("sections", [])

    # Build an overview section listing all lessons
    lesson_items = []
    for s in section_list:
        lesson_items.append(s["header"])

    overview_blocks = []

    if module_config.get("summary_points"):
        overview_blocks.append({"type": "subheader", "content": "Key Takeaways"})
        overview_blocks.append({"type": "bullets", "items": module_config["summary_points"]})

    # Append any extra blocks specified for the overview
    if module_config.get("overview_extra_blocks"):
        overview_blocks.extend(module_config["overview_extra_blocks"])

    sections.append({
        "header": f"{module_num_line}: {module_name} Overview",
        "blocks": overview_blocks,
    })

    return {
        "title": f"{module_num_line}\n{module_name}",
        "subtitle": "Module Overview",
        "module_label": module_num_line,
        "lesson_label": "Overview",
        "logo_path": module_config.get("logo_path", ""),
        "logo": module_config.get("logo", ""),
        "sections": sections,
        "skip_toc": True,
        "skip_summary": True,
        "output_filename": f"{module_folder}/Overview.pdf",
    }


def generate_lesson_configs(module_config):
    """Extract individual lesson configs from a module config."""
    module_folder = get_module_folder(module_config)
    if not module_folder:
        return []

    title_lines = module_config["title"].split("\n")
    module_num_line = title_lines[0] if title_lines else "Module"
    module_name = title_lines[1] if len(title_lines) > 1 else ""

    configs = []
    sections = module_config.get("sections", [])

    for section in sections:
        header = section["header"]
        lesson_num, lesson_title = extract_lesson_name(header)

        if lesson_num:
            filename = f"{lesson_num} - {lesson_title}.pdf"
            lesson_label = lesson_num
        else:
            filename = f"{sanitize_filename(header)}.pdf"
            lesson_label = ""

        # Create a single-section config for this lesson
        lesson_config = {
            "title": lesson_title,
            "subtitle": f"Learn the essentials of {lesson_title.lower()}",
            "module_label": module_num_line,
            "lesson_label": lesson_label,
            "logo_path": module_config.get("logo_path", ""),
            "logo": module_config.get("logo", ""),
            "sections": [section],
            "skip_toc": True,
            "skip_summary": False,
            "summary_points": module_config.get("summary_points", []),
            "output_filename": f"{module_folder}/{filename}",
        }

        configs.append(lesson_config)

    return configs


def main():
    # Find the default logo
    default_logo = BASE_DIR / "PDF" / "Course_Logo.png"
    default_logo_path = str(default_logo) if default_logo.exists() else ""

    # Process each module JSON
    module_files = sorted(CONTENT_DIR.glob("Module-*.json"))

    total_generated = 0

    for module_file in module_files:
        print(f"\n{'='*60}")
        print(f"Processing: {module_file.name}")
        print(f"{'='*60}")

        with open(module_file) as f:
            module_config = json.load(f)

        # Set logo path if not set
        if not module_config.get("logo_path") and not module_config.get("logo"):
            module_config["logo_path"] = default_logo_path
        elif module_config.get("logo") and not module_config.get("logo_path"):
            logo_candidate = BASE_DIR / "PDF" / module_config["logo"]
            if logo_candidate.exists():
                module_config["logo_path"] = str(logo_candidate)

        module_folder = get_module_folder(module_config)
        if not module_folder:
            print(f"  Skipping (no folder in output_filename)")
            continue

        # Generate individual lesson PDFs (skip modules with only 1 section — they're overviews)
        lesson_configs = generate_lesson_configs(module_config)
        if len(module_config.get("sections", [])) <= 1:
            print(f"  Skipping lesson generation (single-section overview module)")
            lesson_configs = []
        for lc in lesson_configs:
            output_path = str(OUTPUT_DIR / lc["output_filename"])
            print(f"  Generating: {lc['output_filename']}")
            try:
                generate_pdf(lc, output_path)
                total_generated += 1
            except Exception as e:
                print(f"    ERROR: {e}")

        # Generate Overview PDF (for modules with multiple sections)
        if len(module_config.get("sections", [])) > 1:
            overview_config = generate_overview_config(module_config, module_folder)
            # Set logo
            if not overview_config.get("logo_path"):
                overview_config["logo_path"] = default_logo_path
            elif overview_config.get("logo") and not overview_config.get("logo_path"):
                logo_candidate = BASE_DIR / "PDF" / overview_config["logo"]
                if logo_candidate.exists():
                    overview_config["logo_path"] = str(logo_candidate)

            output_path = str(OUTPUT_DIR / overview_config["output_filename"])
            print(f"  Generating: {overview_config['output_filename']}")
            try:
                generate_pdf(overview_config, output_path)
                total_generated += 1
            except Exception as e:
                print(f"    ERROR: {e}")

    print(f"\n{'='*60}")
    print(f"Done! Generated {total_generated} lesson PDFs.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
