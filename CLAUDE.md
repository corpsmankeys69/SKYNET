# CLAUDE.md — LLM Wiki Schema

This repository is a personal second brain built on the **LLM Wiki** pattern
(Andrej Karpathy: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

This file is the **schema**: the durable configuration that tells any LLM
agent working in this repo how to behave as a disciplined wiki maintainer.
Read it in full before doing anything here. From now on, every interaction
in this repository follows this schema by default (see §9).

## 1. Three-layer architecture

1. **Raw sources** (`sources/`) — immutable. Original articles, transcripts,
   pasted notes, link dumps, quotes. Never edited or deleted once added,
   only appended to.
2. **The wiki** (`wiki/`) — mutable, LLM-owned. A compounding set of
   markdown pages that synthesize and cross-reference. This is the actual
   second brain. The agent owns this content; the human reads it, asks
   questions of it, and drives what gets ingested — but doesn't hand-edit it.
3. **The schema** (this file) — the rules. Only edited directly by the
   human, or by the agent when explicitly asked to change the schema itself.

> "The wiki is a persistent, compounding artifact. The cross-references are
> already there." — the tedious part of maintaining a knowledge base isn't
> the reading or thinking, it's the bookkeeping. That's the agent's job.

## 2. Directory layout

```
CLAUDE.md               schema — you are here
sources/                 raw, immutable inputs
  YYYY-MM-DD-slug.md      one file per ingested source
wiki/
  index.md                map of content — the front door
  log.md                  append-only ingest/change log
  topics/
    slug.md                one page per atomic concept, entity, or claim cluster
```

Rules:
- Never write into `wiki/topics/` without also updating `wiki/index.md`
  (if the map changed) and appending an entry to `wiki/log.md`.
- Never edit a file under `sources/` after creation. If a source needs
  correcting, add a new dated source and note the supersession in the
  wiki — don't rewrite history.
- Filenames: kebab-case, no spaces, `.md` extension.

## 3. Wiki page conventions (`wiki/topics/*.md`)

Every topic page starts with frontmatter:

```yaml
---
title: Human Readable Title
aliases: [alt name, acronym]
tags: [topic, area]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [sources/2026-08-25-slug.md]
---
```

Then:
- **One concept per page.** If a page is trying to be two things, split it
  and note the split in `log.md`.
- Use Obsidian-style `[[wikilinks]]` to cross-reference other topic pages
  by title. Prefer linking over repeating content.
- Write claims as short declarative sentences with a source pointer, e.g.
  `Ingest integrates a new source across the 10–15 most relevant existing
  pages rather than filing it away for later retrieval. (sources/2026-08-25-llm-wiki-pattern.md)`
- **Contradictions are surfaced, never silently overwritten.** If new
  information conflicts with an existing claim, flag it inline:
  `> ⚠️ Conflicts with [[Other Page]] as of 2026-08-25 — unresolved`
  and mention it to the human. Don't pick a winner on your own judgment.
- Mark stale/superseded claims rather than deleting them, unless the human
  confirms deletion.
- Keep pages short and dense. Split an unwieldy page rather than letting it
  sprawl.

## 4. Operations

### Ingest — triggered by a new source (link, paste, file, conversation)
1. Save the raw material verbatim to `sources/YYYY-MM-DD-slug.md`, with a
   one-line frontmatter noting origin (URL, "pasted by user", etc). Don't
   summarize at this stage — this copy is ground truth.
2. Read it fully; extract the claims, facts, and definitions worth keeping.
3. Search the existing wiki for the ~10–15 most relevant pages — topics it
   touches, entities it mentions, claims it extends or contradicts.
4. Integrate: update those pages in place (new claims, strengthened
   claims, flagged contradictions, new cross-links). Prefer editing over
   creating new pages.
5. Create a new topic page only for a genuinely new concept/entity nothing
   existing covers.
6. Update `wiki/index.md` if a page was created or a page's role in the
   map materially changed.
7. Append one entry to `wiki/log.md` (format in §6).
8. Report back: what was created, what was updated, what contradictions
   (if any) were flagged.

### Query — triggered by a question
1. Search the **wiki** first, not raw sources — the wiki is the
   compounding artifact; sources are the fallback for its gaps.
2. Synthesize an answer, citing the relevant topic pages.
3. If answering surfaces a gap, a stale claim, or a synthesis worth
   keeping, propose filing it back as a small ingest — ask before writing,
   unless the human has pre-authorized standing edits.

### Lint — triggered on request ("clean up", "check the wiki", periodically)
1. Scan for contradictions between pages that were flagged but never
   resolved.
2. Scan for orphan pages (no inbound `[[links]]` and not listed in
   `index.md`).
3. Scan for stale claims sourced only from something marked superseded.
4. Scan for missing cross-references between clearly related pages.
5. Report findings as a punch list. Auto-fix only the unambiguous cases
   (e.g. an obviously missing link); anything needing judgment goes to
   the human.

## 5. `wiki/index.md`

The front door. Hand-curated by the agent, grouped by area/theme, linking
to every topic page that deserves to be discoverable. Not auto-generated —
a page that hasn't earned a place in the map yet is itself a signal (it's
an orphan; lint should catch it).

## 6. `wiki/log.md`

Append-only, newest entry at the bottom. One entry per ingest/lint/major
edit:

```
## YYYY-MM-DD — <one-line action summary>
- Source: sources/....md (if applicable)
- Created: [[Page A]], [[Page B]]
- Updated: [[Page C]] (+contradiction flagged), [[Page D]]
- Notes: anything a human should know
```

Never edit past entries except to fix a factual error in the log itself.

## 7. Division of labor

- **Human**: sources material, asks questions, makes the judgment calls on
  unresolved contradictions, decides what's worth ingesting, edits this
  schema.
- **Agent**: does the reading, extraction, cross-referencing, bookkeeping,
  and consistency maintenance — the tedious part humans abandon.

## 8. Tooling notes

This repo is a plain markdown tree and works as an Obsidian vault as-is
(`[[wikilinks]]`, YAML frontmatter). Optional, non-required enhancements a
human may add later: Dataview queries inside `index.md`, Marp to turn
topic pages into slide decks, a local search index (e.g. qmd) for fast
recall over a large wiki.

## 9. Standing instruction

From this point forward, every interaction in this repository follows
this schema by default:
- A new source/link/paste → run **Ingest** (§4).
- A question → run **Query** (§4).
- "clean up" / "check the wiki" / "lint" → run **Lint** (§4).

If it's ambiguous which mode applies, ask rather than guess.
