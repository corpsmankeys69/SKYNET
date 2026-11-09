---
title: Quick Start Guide Conversion Rules
aliases: [QSG conversion, rebuild old guides on template]
tags: [template, process, documentation]
created: 2026-10-06
updated: 2026-11-09
sources: [sources/2026-10-06-amb-clinician-rooming-a-patient-nurse-v3-old.pdf, sources/2026-11-09-amb-bcma-faq-v8-old.docx, sources/2026-10-06-epic-training-quick-start-guide-template.md]
---

# Quick Start Guide Conversion Rules

Rules the user set for rebuilding old PDF guides on the [[Epic Training Quick Start Guide Template]]. Every guide must follow the template. The user adds screenshots and icons by hand. (pasted by user, 2026-10-06 conversation)

## Decisions
- Output is a .docx built from the template XML, so header, footer bar, styles, TOC field, and callout boxes carry over exactly.
- Strip all template sample text and the "Call Out Boxes" reference section.
- Drop old cover pages. Page 1 is the TOC.
- Header: fill the guide title, then "Application | Audience" from the old guide. The footer is left for the user to update (version, date, initials, org line).
- Heading mapping: Heading 1 is the guide title, Heading 2 is a workflow (main topic, starts a new page), Heading 3 is a subtopic. A fourth level in an old guide becomes Heading 3.
- Steps are numbered lists, each list restarting at 1. Bullets sit at level 2 of the list.
- Bold UI terms as the old guide did.
- Old "Hint:" lines become callout boxes. Time-savers and shortcuts are Efficiency Tip boxes. Troubleshooting or key-step reinforcement are Important Note boxes. Each hint is placed right after its step.
- Screenshots and icons become highlighted placeholders: `[Screenshot: ...]` on its own line after the step, `[icon]` inline. The user replaces them.
- The word "Epic" must not appear anywhere inside a finished guide (visible text, document properties, leftover links). Each spot becomes a purple-shaded blank placeholder `[      ]` (fill C3A6F0; Word has no purple highlight). User instruction, 2026-10-12. In the first guide: header brand line and one callout box. File names still contain "Epic" per the naming rule; not asked to change.
- Edits: fix grammar and typos only. Never merge or drop steps. Report duplicates and oddities to the user.
- Page references: not used in the first guide. Rule unanswered; ask when one appears.

## FAQ-style sources (first seen 2026-11-09, AMB BCMA FAQ)
- "update this as before" means: apply every rule on this page to the new file. The source can be a .docx as well as a PDF.
- Header line 2 uses the source's own title. For an FAQ the template's "Quick Start Guide" suffix is dropped (it would read "FAQ Quick Start Guide"). Header line 3 comes from the source header ("Ambulatory | Clinician").
- Structure: Heading 1 is the source title, one Heading 2 groups the questions ("Frequently Asked Questions"), and each question is a Heading 3 so the TOC lists every question. Putting each question at Heading 2 would force a new page per question.
- The "Q:" and "A:" labels are dropped; the heading style and the plain answer paragraph carry that meaning. Answers stay in Normal style.
- Hyperlinks (email, policy links) are kept as live links. Source text color (grey) is not kept.
- Standalone bullets use the template's bullet level with a 0.5 in indent.
- Screenshots in the middle of an answer become `[Screenshot: ...]` lines at that position. A screenshot the source placed before its text, where the text says "below", goes after the text.
- The footer is not touched: "v1.0 09.28.2026 INITIALS" and "UW Medicine | Fred Hutch" stay for the user to edit, even though the source footer said "v.8 2024.1231 EYL" and "FHCC".

## How a guide is built
- tools/run_guide.sh <config.py> <out.docx> builds from the template stored in sources/, renders with LibreOffice, fills TOC page numbers until stable, and validates. A guide's text lives in a config file: tools/guides/rooming.py and tools/guides/bcma_faq.py. tools/build_guide.py documents the content kinds and inline markup (bold, yellow hand-added markers, purple blank, links).
- It clones the template's own callout tables and icons, restarts numbering per list, sets the header, shades the header brand word as the purple blank, and removes the template name and old links from the file internals. Word's F9 refreshes the TOC.
- Regression check: rebuilding the Rooming guide from its config gives text identical to the delivered file.

## Open items
- Page reference and alternate-guide boxes: no rule yet. The BCMA FAQ says "refer to the BCMA tip sheet" in one answer; it was left as plain text.
- eLearning reference boxes: none in the first guide.
