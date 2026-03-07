# Plan: Break Down 10 Modules into Lesson PDFs

## Overview

Create 10 module JSON configs (one PDF per module), each containing 3-6 lesson sections. Content is sourced from existing SOP PDFs + the template example. Image placeholders will use `[IMAGE PLACEHOLDER: description]` text blocks where the user will add images later.

Each module = 1 PDF file with cover + TOC + lesson pages + summary.

---

## Module Breakdown (Lessons per Module)

### Module 1: The Basics (5 lessons)
**Source:** Template example (AI-Influencer-Method-Free-Training)
1. **What Is the AI Influencer Method** — Overview of the business model, what it is and isn't
2. **Why AI Influencers Work** — Market opportunity, key advantages over traditional influencers
3. **The Business Model & Revenue Sources** — Subscription fees, PPV, tips, chat upsells
4. **Platform Overview** — Primary vs support platforms, priority order
5. **Tools & Resources You'll Need** — Content generation tools, platform management, monetization tools

### Module 2: Base Model Creation (4 lessons)
**Source:** Referenced across SOPs (visual consistency sections) + new content
1. **Choosing Your Niche & Persona** — Picking a style, audience, and look for your AI model
2. **Generating Your Base Model** — AI image generation tools, creating the first consistent face
3. **Ensuring Face & Style Consistency** — Same face across all images, lighting variation, visual rules
4. **Building Your Content Library** — Batch generating images, organizing assets, image placeholder examples

### Module 3: SFW Image Creation (4 lessons)
**Source:** Content from visual consistency + content pipeline sections
1. **Reference Image Workflow** — How to use a reference image to generate new SFW content
2. **Prompt Engineering for SFW Images** — Writing prompts that produce natural, platform-safe results
3. **Editing & Refining AI Images** — Post-generation editing, removing artifacts, improving realism
4. **Platform-Specific Image Rules** — What's safe for IG vs TikTok vs Reddit, content tiers

### Module 4: SFW Video Creation (3 lessons)
**Source:** New content (Kling-specific)
1. **Introduction to AI Video with Kling** — What Kling is, motion control basics, when to use video
2. **Writing Video Prompts for Kling** — Prompt structure, motion descriptions, camera control
3. **Exporting & Using Videos on Social Media** — Format requirements, platform video specs, posting strategy

### Module 5: Phone Setup / Warmup Social Media (4 lessons)
**Source:** Instagram-Threads-Secret-Strategy (warmup phase), TikTok-SOP (warmup phase)
1. **Phone & Device Setup** — Separate devices, browser profiles, VPN/proxy, SIM cards
2. **Creating & Configuring Social Media Accounts** — Username rules, bio setup, profile photo, initial settings
3. **The Warmup Protocol** — Day-by-day warmup (scroll, like, comment, follow schedule), no posting early
4. **Warmup Mistakes That Get You Banned** — Common errors, what NOT to do during warmup

### Module 6: Growing Social Media (6 lessons)
**Source:** Instagram-Threads-Secret-Strategy, Reddit-SOP, TikTok-SOP, X-Twitter-Growth-Traffic-Manual
1. **Instagram Growth Strategy** — Reels launch process, content execution, stories & carousels
2. **Threads Growth Strategy** — How to post & reply, scaling & testing, engagement tactics
3. **Reddit Growth Strategy** — Profile setup, subreddit targeting, karma farming, niche infiltration
4. **TikTok Growth Strategy** — Account setup, carousel format, safe content, daily behavior
5. **Twitter/X Growth Strategy** — Reply-based growth, targeting audience pools, premium features
6. **Cross-Platform Coordination** — Posting schedule across platforms, content distribution rules

### Module 7: Scaling Social Media (4 lessons)
**Source:** Instagram-Threads (scaling phases), TikTok (scale strategy), template (scaling section)
1. **Content Posting Cadence & Scheduling** — Daily/weekly posting frequency per platform
2. **The Hook That Converts Viewers to Followers** — Content that stops the scroll, bio optimization, CTA placement
3. **Geo Targeting & Distribution Control** — USA priority, audience targeting, distribution settings
4. **Multi-Account Scaling** — Running multiple personas, separate devices, never linking accounts

### Module 8: Account Safety & Precautions (4 lessons)
**Source:** TikTok-SOP (multi-account safety), Instagram-Threads (failure recovery), X-Twitter (safety/shadowban)
1. **Understanding Platform Bans & Shadowbans** — How bans work, shadowban detection, warning signs
2. **Daily Safety Habits** — Trust signals, behavior patterns, what platforms monitor
3. **What to Do If You Get Banned** — Appeal process, account recovery, starting fresh safely
4. **Multi-Account Safety Rules** — Device separation, IP management, never cross-linking

### Module 9: Turning Followers into Paying Fans (6 lessons)
**Source:** AI-Funnelling-SOP, AI-Fanvue-Page-SOP, AI-OFM-Chatting-Systems
1. **Funnel Psychology & Overview** — How attention becomes revenue, traffic flow diagram
2. **Link in Bio & Funnel Architecture** — AllMyLinks/Linktree setup, Telegram funnel, IG highlights funnel
3. **Fanvue Page Setup** — Banner, bio, free posts, subscriber posts, PPV structure, pricing
4. **Chat Systems & Revenue Logic** — Fan psychology, message priority, new subscriber handling
5. **First Sale & Upsell Logic** — Chat flow structure, first sale timing, upsell strategy, whale management
6. **Hiring & Managing Chatters** — Where to find chatters, vetting, payment, performance tracking

### Module 10: Continued on Discord (1 lesson)
1. **What Comes Next: Advanced Training on Discord** — Brief overview that NSFW content, advanced strategies, and community support continue on Discord

---

## Technical Implementation

### File Creation
- 10 new JSON files: `content/Module-01-The-Basics.json` through `content/Module-10-Continued-On-Discord.json`
- Each follows the existing JSON schema with: title, subtitle, output_filename, sections, summary_points

### Image Placeholders
- Use a `panel` block with border color `#c49a85` and title `"IMAGE PLACEHOLDER"` containing a description of what image should go there
- Example: `{"type": "panel", "title": "IMAGE PLACEHOLDER", "content": "Screenshot of AI image generation tool interface showing base model creation"}`

### Block Types Used
- `text` — Explanatory paragraphs
- `subheader` — Lesson sub-sections
- `bullets` — Step lists, rules, tips
- `two_column` — Side-by-side comparisons (do's/don'ts, left/right info)
- `good_example` / `bad_example` — Correct vs incorrect approaches
- `panel` — Callouts, critical rules, image placeholders

### Generation
- Run `python generate_pdf.py --config content/Module-XX-Name.json` for each
- All 10 PDFs output to `output/` directory

### Content Sourcing Strategy
- Modules 1, 6, 7, 8, 9 → Heavy reuse from existing SOP JSONs (rewritten into lesson format)
- Modules 2, 3, 4 → Lighter existing content, more new material based on referenced concepts
- Module 5 → Warmup sections extracted from Instagram-Threads + TikTok SOPs
- Module 10 → Minimal, 1 lesson placeholder

---

## Execution Order
1. Create all 10 JSON config files
2. Generate all 10 PDFs
3. Verify output
4. Commit and push
