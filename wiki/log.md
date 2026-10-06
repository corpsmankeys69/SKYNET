# Log

Append-only. Newest entry at the bottom. One entry per ingest / lint /
major edit. See `CLAUDE.md` §6 for the format contract.

## 2026-08-25 — Wiki initialized; first ingest (the LLM Wiki pattern itself)
- Source: sources/2026-08-25-llm-wiki-pattern.md (Karpathy's LLM Wiki gist)
- Created: [[LLM Wiki Pattern]], [[This Repository]]
- Updated: wiki/index.md (added Meta section)
- Notes: Bootstrapped the schema (`CLAUDE.md`), folder conventions
  (`sources/`, `wiki/topics/`), and ran the first ingest against the
  pattern's own source document as a worked example. No contradictions
  found (empty wiki).

## 2026-10-06 — Ingested Epic Training Quick Start Guide template (.dotx)
- Source: sources/2026-10-06-epic-training-quick-start-guide-template.md (extraction) and sources/2026-10-06-epic-training-quick-start-guide-template.dotx (original binary)
- Created: [[Epic Training Quick Start Guide Template]]
- Updated: wiki/index.md (new "Documents and templates" area)
- Notes: Extracted from the template XML: page setup, fonts, brand colors, header, footer gradient, callout box construction. No contradictions found (no related pages existed).

## 2026-10-06 — Converted first guide; recorded conversion rules; corrected body font
- Source: sources/2026-10-06-amb-clinician-rooming-a-patient-nurse-v3-old.pdf (Outpatient Clinician Rooming a Patient, v.3 02.01.2021)
- Created: [[Quick Start Guide Conversion Rules]]
- Updated: [[Epic Training Quick Start Guide Template]] (body font corrected from Calibri Light to Calibri 11 pt; link to conversion rules), wiki/index.md
- Notes: The earlier body-font claim was wrong. Added tools/build_guide.py so the build can be repeated in a fresh session. Built guide delivered as a .docx in chat, not stored in the repo. Old PDF footer said "UW Medicine | SCCA"; template says "Fred Hutch" and was kept.
