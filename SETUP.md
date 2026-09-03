# fullstack-agent install notes

This repo now carries the **memory** piece of [jaredrhod/fullstack-agent](https://github.com/jaredrhod/fullstack-agent): [ai-memory-vault](https://github.com/jaredrhod/ai-memory-vault), wired up per its own wizard (`ai-memory-vault/ai-memory-vault.md`), run inside this session's conversation instead of a live terminal interview.

## What's here

- **`CLAUDE.md`** (repo root) — the boot config. Identity: Jarvis, kept as shipped (unmodified personality, "sir/boss" address).
- **`vault/`** — the memory vault. `VAULT-INDEX.md` is filled in where this session had real answers (name: Bentley, vault location, folder structure) and left with `[FILL IN: ...]` markers everywhere the template's own design calls for a real interview (Background, How I Think, Beliefs, Preferences details, etc.) — those are opt-in by design, not an oversight.
- **`fullstack-agent/`** — the installer/toolbox repo, vendored, so `update.sh` and the other pieces (voice, face, hands) are one command away if you want them later.
- **`ai-memory-vault/`** — the memory piece's own source, vendored (its wizard, README, templates).

## What was skipped, and why

- **Voice (backtalk), face (ai-visualizer), hands (barehands):** not installed — you chose memory only when asked. Re-run the fullstack-agent installer any time to add them; it only installs what's missing.
- **Obsidian:** not installed. This ran in a headless cloud container with no GUI, so the app-install step in `ai-memory-vault.md` (its "Part 1") couldn't run. The vault is plain markdown files and doesn't need Obsidian to be read or written by Claude Code — but `ai-memory-vault.md` treats Obsidian as required, not optional, for a person to actually *see and own* their memory day to day. Install it yourself and open `vault/` as a vault to get that.
- **Vault registration in `obsidian.json`:** skipped for the same reason — nothing to register against without Obsidian installed.
- **`~/.claude/projects/.../MEMORY.md` redirect:** skipped — that file lives outside any repo, in Claude Code's own per-project folder on whatever machine you run it from. See `ai-memory-vault/templates/MEMORY.md` for the pointer text if you want to wire that up locally.
- **Desktop shortcuts, the first-hello test drive, the marketing-skills offer:** all Phase 5/6 of the full fullstack-agent wizard — meaningless without a live desktop session, so not attempted here.

## Finishing this yourself

1. Clone this repo locally, `cd` into it, and open Claude Code there — `CLAUDE.md` loads automatically.
2. Say "interview me and fill in my VAULT-INDEX" to complete the profile sections properly, in your own words, instead of the placeholders left here.
3. Install Obsidian and open `vault/` as a vault, if you want the app experience `ai-memory-vault.md` is built around.
4. To add voice/face/hands: `cd fullstack-agent && claude "set me up"` and pick the remaining pieces — it detects what's already here and only installs what's missing.
