---
origin: pasted by user (korinstincts@gmail.com) — file Epic_Training_Quick_Start_Guide_Template_4.dotx; original binary saved beside this file as 2026-10-06-epic-training-quick-start-guide-template.dotx
added: 2026-10-06
added-by: user
---

# Epic Training Quick Start Guide Template (raw extraction from the .dotx XML)

Core properties: title "Epic Training Quick Start Guide"; creator "Iverson, Mary K"; created 2026-02-24; modified 2026-09-29.

## Page setup (word/document.xml sectPr)
Letter 12240x15840 twips; margins 1440 all sides (1 in); header distance 432; footer distance 277; one header, one footer, no columns.

## Theme (theme1.xml)
Fonts: major Calibri Light, minor Calibri. Color scheme is stock Office (accent1 4472C4, hlink 0563C1). Brand colors are NOT in the theme; they are hard-coded in styles, header, and footer.

## Styles (word/styles.xml)
- docDefaults: Calibri, en-US.
- Normal: 11 pt (sz 22).
- BasicParagraph ("[Basic Paragraph]"): based on Normal; line spacing 288 auto (1.2); color 000000; 12 pt (sz 24). Document body paragraphs use this with run overrides to Calibri Light, color 00000A, 11 pt.
- Heading1: bold, color 38296B, 16 pt (sz 32), space before 240, keepNext, keepLines.
- Heading2: not bold, color 38296B, 14 pt (sz 28), space before 40.
- Heading3: not bold, color 38296B, 12 pt (sz 24), space before 40.
- TOCHeading: based on Heading1; document overrides run to color 38296B, 14 pt; font majorHAnsi (Calibri Light).
- TOC1/2/3: spacing after 100; indent 0 / 220 / 440; right dot-leader tab at 9350.
- TipText (character): Calibri Light, color auto, character spacing 6, 11.5 pt (sz 23).
- Hyperlink: color 0563C1, underline.
- ListNumber2: 12 pt, indent left 1080 hanging 360, spacing after 160, contextualSpacing.
- contactinformation (header paragraphs): 9 pt (sz 18), right aligned by default (header overrides to left).
- CharacterStyle3: Calibri, bold, color 7B3870, spacing 2, 12 pt (header overrides color/size).

## Header (word/header1.xml)
Line 1: "Epic Training" — CharacterStyle3, bold, color 38296B, 16 pt (sz 32), spacing 1, left aligned.
Line 2: "[Title] Quick Start Guide" — CharacterStyle3 with bold off, color 00000A, 12 pt (style size, no override).
Line 3: "Application | Audience" — color 00000A, 7 pt (sz 14 found in the header paragraph properties).

## Footer (word/footer1.xml)
- Paragraph 1: centered PAGE field ("PAGE \* MERGEFORMAT") in Footer style, with an anchored rectangle shape (5955030 x 111125 EMU, about 6.5 in x 0.12 in) positioned 424511 EMU below the paragraph, left edge on the margin, decorative. Fill is a horizontal linear gradient (ang 0): stop 0% 32006E, stop 50% 261B65, stop 100% 1B365D; no outline.
- Paragraph 2 (Footer style, tabs center 4680 / right 9360): left "v1.0 09.28.2026 INITIALS" then two tabs then right-aligned "UW Medicine | Fred Hutch".
- Paragraph 3: empty, two tabs.
- Footer text uses default size (11 pt) and default color.

## Body content (verbatim text)
Table of Contents (TOC field \o "1-3" \h \z \u): Title of Quick Start Guide; Main Topic; Subtopic; Call Out Boxes; Efficiency Tip Box; Important Notes Box; eLearning Reference Box; Page / Alternate Guide Reference Box; Another main topic; Another subtopic.

Title of Quick Start Guide (Heading1)
Main Topic (Heading2): "Usually, each main topic is named after a workflow and includes steps for completing that workflow. If your guide includes many workflows, you may instead choose to use main topics to organize the guide, grouping the workflow tasks into subtopics. In these guides, the main topics themselves don't include any information or steps, which are instead found in the individual subtopics. For instructions on adding a new main topic, refer to the Add a Main Topic section in the Customize and Distribute Quick Start Guides handbook."
Subtopic (Heading3): "Use subtopics if you're not putting workflow steps in main topics but instead using them to group related workflows. For instructions on adding a subtopic, refer to the Add a Subtopic section in the Customize and Distribute Quick Start Guides handbook."
Call Out Boxes (Heading1)
Efficiency Tip Box (Heading2): "To write a quick tip to the user anywhere in the guide, copy the efficiency tip box:" Box text: "Enter a brief tip or trick here to help users save time, work more efficiently, or optimize their use of the system. Text inside this box should use the Tip Text style."
Important Notes Box (Heading2): "To reinforce crucial steps or provide troubleshooting advice, copy the important notes box:" Box text: "Enter a troubleshooting tip here to draw attention to a key step or help users avoid or resolve errors. Text inside this box should use the Tip Text style."
eLearning Reference Box (Heading2): "To refer users to related eLearning lessons, copy the eLearning reference box:" Box text: "Watch the [Name of Elearning Lesson] eLearning lesson to learn more about [topic]. Text inside this box should use the Tip Text style."
Page / Alternate Guide Reference Box (Heading2): "To refer to other pages/sections in the guide or to refer to alternate guides, copy the page reference box below. Note that in Epic-released guides, page number references are fields that you can update automatically. If you add your own page reference tip, enter the page numbers manually. Use meaningful links to link to alternate guides." Box texts: "Refer to [p. ##/section] for more information on [topic]. Text inside this box should use the Tip Text style." and "Refer to the [alternate guide] for more information on [topic]. Text inside this box should use the Tip Text style."
Another main topic (Heading2): "Each main topic should begin on a new page."
Another subtopic (Heading3): numbered steps "Do this." / "And this." / [efficiency tip box inline] / "Then this." / [see-also box: "See also Customize and Distribute Quick Start Guides" with hyperlink].

## Callout box construction (tables in document.xml)
Two-column, one-row table. tblInd 115; grid 596 / 8639 (about 0.41 in icon cell, 6 in text cell); row height 548 minimum; single 0.5 pt (sz 4) black borders on all edges and inside; no cell shading. Left cell holds a black round icon (white glyph) as a drawing: info "i" for efficiency tips, "!" for important notes, a video/play icon for eLearning, a pointing hand for page or alternate-guide references. Right cell is vertically centered, paragraph style ListNumber2 with indent left 0 and spacing 72 before/after, text run uses the TipText character style. Tables were rendered by LibreOffice in an Arial-like fallback for Calibri Light.

## Hyperlinks (document.xml.rels)
Four external links to galaxy.epic.com Redirect.aspx (DocumentID 100427482, 100428120, 100428023 with PrefDocID 194388), used for the handbook cross-references.
