---
origin: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
added: 2026-08-25
added-by: user (korinstincts@gmail.com)
---

# LLM Wiki: Personal Knowledge Base Pattern (source gist, condensed)

## Core Concept

The LLM Wiki pattern describes a system where artificial intelligence
incrementally builds and maintains a persistent wiki — a structured
collection of markdown files — rather than repeatedly retrieving from raw
documents. As the document explains: "the wiki is a persistent, compounding
artifact. The cross-references are already there."

## Three-Layer Architecture

**Raw sources** remain immutable — articles, papers, and data files you
curate.

**The wiki** consists of LLM-generated markdown pages that the system owns
entirely, updating them as new information arrives.

**The schema** is a configuration document defining wiki structure,
conventions, and workflows — the rules that make the LLM a disciplined
maintainer.

## Key Operations

**Ingest**: When adding a source, the LLM reads it, extracts key
information, and integrates findings across 10-15 existing wiki pages
rather than simply indexing for later retrieval.

**Query**: Users ask questions against the wiki, with the LLM synthesizing
answers from relevant pages and optionally filing valuable discoveries back
as new wiki pages.

**Lint**: Periodic health checks identify contradictions, stale claims,
orphan pages, and missing cross-references.

## Why This Approach Works

The pattern addresses the core friction in knowledge management: "The
tedious part of maintaining a knowledge base is not the reading or the
thinking — it's the bookkeeping." LLMs excel at the maintenance burden
humans abandon — updating references, maintaining consistency, and noting
contradictions.

## Tools and Workflows

The document recommends Obsidian as the IDE for browsing results, with
optional enhancements like local search engines (qmd), the Dataview plugin
for dynamic queries, and Marp for presentations directly from wiki content.

Human responsibility centers on sourcing, exploration, and asking
productive questions. The LLM handles summarization, cross-referencing, and
consistency maintenance.
