# fullstack-agent install notes

This repo carries all four pieces of [jaredrhod/fullstack-agent](https://github.com/jaredrhod/fullstack-agent) — memory, voice, face, and hands — wired up per each piece's own wizard (`ai-memory-vault/ai-memory-vault.md`, `backtalk/backtalk.md`, `ai-visualizer/ai-visualizer.md`, `barehands/barehands.md`), run inside this session's conversation instead of a live terminal interview.

## What's here

- **`CLAUDE.md`** (repo root) — the boot config. Identity: renamed from the shipped Jarvis to **Bentley** (personality/rules otherwise unchanged: "sir/boss" address, welcome line "All systems online, sir. What are we working on today?"). Also carries the barehands board block (4b from `barehands.md`) at the bottom, so the agent knows to reach for the board when you ask to see something.
- **`vault/`** — the memory vault. `VAULT-INDEX.md` is filled in where this session had real answers (name: Bentley, vault location, folder structure) and left with `[FILL IN: ...]` markers everywhere the template's own design calls for a real interview (Background, How I Think, Beliefs, Preferences details, etc.) — those are opt-in by design, not an oversight.
- **`backtalk/backtalk.json`** — voice config: hands-free listening (`mic_mode: "open"`, home key still works as interrupt), built-in Kokoro voice (`bm_lewis`, British butler register), permissions set to ask-first (`permission_mode: "ask"`), `extra_dirs` pointed at `vault/`, `barehands_state_dir` pointed at `../barehands/state` so the voice drives the hands' ring too.
- **`ai-visualizer/ai-visualizer.json`** — face config: the board face, `bus_dir` pointed at `../backtalk` so it reads the voice's live state.
- **`barehands/barehands.json`** — hands config: a `Vault` notes orb pointed at `../vault` (this repo's own memory vault, not the sample notes), the default `Props` media orb.
- **`.claude/settings.json`** — `UserPromptSubmit`/`Stop` hooks that write `thinking`/`idle` into `barehands/state/state`, so barehands' ring mirrors real Claude Code sessions run from this repo's root (per barehands.md Phase 4a). Scoped to this repo only, not `~/.claude/settings.json`, so it never drives someone else's ring.
- **`fullstack-agent/`** — the installer/toolbox repo, vendored, so `update.sh` is one command away.
- **`ai-memory-vault/`, `backtalk/`, `ai-visualizer/`, `barehands/`** — each piece's own source, vendored (wizard file, README, templates/assets).

## What was skipped, and why

- **Obsidian:** not installed. This ran in a headless cloud container with no GUI, so the app-install step in `ai-memory-vault.md` (its "Part 1") couldn't run. The vault is plain markdown files and doesn't need Obsidian to be read or written by Claude Code — but `ai-memory-vault.md` treats Obsidian as required, not optional, for a person to actually *see and own* their memory day to day. Install it yourself and open `vault/` as a vault to get that.
- **Vault registration in `obsidian.json`:** skipped for the same reason — nothing to register against without Obsidian installed.
- **`~/.claude/projects/.../MEMORY.md` redirect:** skipped — that file lives outside any repo, in Claude Code's own per-project folder on whatever machine you run it from. See `ai-memory-vault/templates/MEMORY.md` for the pointer text if you want to wire that up locally.
- **backtalk's speech models and live voice:** attempted here, didn't finish. `./backtalk/install.sh` did succeed at the parts that don't need a mic or the open internet: `espeak-ng` and PortAudio installed, the `uv` venv built, the `backtalk` package installed into it. It stopped on two things this container genuinely can't do: (1) no microphone — confirmed directly, "NO WORKING MICROPHONE" from the audio backend; (2) this session's network policy blocks `huggingface.co`, where the speech-to-text and voice models are hosted, so the model download 403'd at the proxy. Both are container limits, not config problems — `.venv/` isn't committed (gitignored, and it's this machine's build anyway), so `./backtalk/install.sh` needs a full re-run on your own machine to actually get the models. The face piece has no such dependency: `ai-visualizer/server.py` was started headless here and confirmed serving the board face over HTTP with no errors.
- **barehands' server:** started headless here and confirmed working end to end that this container *can* do: `GET /config` returned the real orbs, `bin/board.sh` posted a card and got `204` back, `bin/board-state.sh` correctly reported "no tracker page has connected yet" (accurate — no webcam, no Chrome, no browser here). What's untestable in this container is the actual hand tracking, since that needs a real webcam and Chrome on your end.
- **Desktop shortcuts, the first-hello test drive, the marketing-skills offer:** all Phase 5/6 of the full fullstack-agent wizard — meaningless without a live desktop session, so not attempted here.

## Finishing this yourself

1. Clone this repo locally, `cd` into it.
2. `cd backtalk && ./install.sh` — sets up the Python env, `uv`, and downloads the two local models (~1 GB, one-time). Needs `espeak-ng` (the installer offers it).
3. From the repo root, `./fullstack-agent/start.sh voice` starts the voice line and opens the face together (or `./backtalk/run.sh` for voice only, `./ai-visualizer/run.sh` for face only). For hands: `cd barehands && python3 server.py`, then open `http://127.0.0.1:8794/stage.html` in Chrome and allow the camera.
4. Say "interview me and fill in my VAULT-INDEX" to complete the profile sections properly, in your own words, instead of the placeholders left here.
5. Install Obsidian and open `vault/` as a vault, if you want the app experience `ai-memory-vault.md` is built around.
6. Want ElevenLabs instead of the built-in voice? Tell your agent — it walks the account/key/audition flow per `backtalk/backtalk.md`. The key never goes in a tracked file.
