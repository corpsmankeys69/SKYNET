---
title: LLM Wiki Pattern
aliases: [second brain pattern, LLM Wiki]
tags: [meta, knowledge-management, this-repo]
created: 2026-08-25
updated: 2026-08-25
sources: [sources/2026-08-25-llm-wiki-pattern.md]
---

# LLM Wiki Pattern

A pattern (Andrej Karpathy) for using an LLM agent to incrementally build
and maintain a personal knowledge base as a compounding set of markdown
pages, rather than treating documents as something to re-retrieve from on
every query. This repository is itself an implementation of the pattern —
see [[This Repository]] and the schema in `CLAUDE.md`. (sources/2026-08-25-llm-wiki-pattern.md)

## Three-layer architecture
- **Raw sources** — immutable originals (articles, papers, data). Curated
  by the human, never edited by the LLM once saved.
- **The wiki** — LLM-owned markdown pages, updated as new sources arrive.
  This is the actual knowledge base; it compounds over time because
  cross-references between pages accumulate rather than being rebuilt on
  every query.
- **The schema** — a configuration document (here, `CLAUDE.md`) defining
  structure, conventions, and workflow, so the LLM behaves as a
  disciplined, consistent maintainer rather than improvising each time.
(sources/2026-08-25-llm-wiki-pattern.md)

## Key operations
- **[[Ingest Operation|Ingest]]** — reading a new source and integrating
  its findings across the ~10-15 most relevant existing wiki pages, rather
  than simply filing it away for later retrieval.
- **[[Query Operation|Query]]** — answering a human question by
  synthesizing from wiki pages (not raw sources), optionally filing new
  discoveries back into the wiki.
- **[[Lint Operation|Lint]]** — periodic health checks for contradictions,
  stale claims, orphan pages, and missing cross-references.
(sources/2026-08-25-llm-wiki-pattern.md)

## Why it works
The bottleneck in personal knowledge management isn't reading or thinking,
it's bookkeeping — keeping references updated, staying internally
consistent, noticing contradictions. That's exactly the class of work LLMs
are good at and humans tend to abandon. (sources/2026-08-25-llm-wiki-pattern.md)

## Tooling
Designed to double as an Obsidian vault: plain markdown, YAML frontmatter,
`[[wikilinks]]`. Optional add-ons: a local search index (qmd), the
Dataview plugin for dynamic queries inside `index.md`, and Marp for
generating slide decks straight from wiki pages. None of this is required
for the pattern itself. (sources/2026-08-25-llm-wiki-pattern.md)

## Division of labor
Human: sources material, explores, asks productive questions, resolves
judgment calls (e.g. unresolved contradictions). LLM: reading, extraction,
cross-referencing, and consistency maintenance. (sources/2026-08-25-llm-wiki-pattern.md)
