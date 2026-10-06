---
title: Quick Start Guide Conversion Rules
aliases: [QSG conversion, rebuild old guides on template]
tags: [template, process, documentation]
created: 2026-10-06
updated: 2026-10-06
sources: [sources/2026-10-06-amb-clinician-rooming-a-patient-nurse-v3-old.pdf, sources/2026-10-06-epic-training-quick-start-guide-template.md]
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
- Edits: fix grammar and typos only. Never merge or drop steps. Report duplicates and oddities to the user.
- Page references: not used in the first guide. Rule unanswered; ask when one appears.

## How a guide was built
- Script: tools/build_guide.py. Unzip the template (sources/2026-10-06-epic-training-quick-start-guide-template.dotx), edit the CONTENT list, run `python3 -I tools/build_guide.py <unzipped template dir> <out.docx> [pages.json]`. It clones the template's own callout tables and icons, restarts numbering per list, sets the header, and fills TOC page numbers from a LibreOffice render. Word's F9 refreshes the TOC.

## Open items
- Page reference and alternate-guide boxes: no rule yet.
- eLearning reference boxes: none in the first guide.
