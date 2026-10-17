# 4.5.2 measurement — progress record

**Purpose:** resumable state for the impeccable 4.5.2 re-run pbakaus asked for
on pbakaus/impeccable#744 (2026-10-15). If the session resets, continue from
here: `pwsh tools/run-arms.ps1` skips every chunk already recorded with exit 0.

## Pins

| | |
| --- | --- |
| Skill under test | `impeccable` 4.5.2, marketplace pinned to tag `skill-v4.5.2` = `d631a8827f99414d2b6daba4ef08b7f8701751d7`, isolated `CLAUDE_CONFIG_DIR`, vendored verbatim to `skills/impeccable/` |
| Baseline arm | `impeccable` 4.2.2, the vendored copy from git `HEAD` before this run (`77222c5`), exported to `D:\pb-452\skill-4.2.2` — re-measured under the same instrument |
| Suite | `suites/impeccable.suite.yaml` v1, `sha256:c820aafc...` — byte-identical, DO NOT EDIT. 12 cases, not 20 |
| Model | `claude-haiku-4-5-20251001` |
| Runner | `npx @ktlsr/assay@0.5.0` (contextHash, hashing at load time, attempt isolation on) |
| Host | Claude Code `2.1.302` (from the record's `environment.version`) |
| Host context | `TEMP`/`TMP` = `D:\pb-452\tmp`; record says `host memory none loaded` |
| Engines | 0.1.14 (4.5.2) primed by hand, sha256 `38e09451...` matches the release sidecar; 0.1.3 (4.2.2) already cached |
| Modes | `acceptEdits`, `bypassPermissions` |
| Attempts | 120 per arm per mode, 10 chunks of 12 (`--repeat 1`), interleaved across the four arm×mode cells, orphans cleared between chunks |

## Why a 4.2.2 re-baseline

Between the 09-08 measurement and now, three things changed besides the skill:
runner 0.2.0 → 0.5.0, Claude Code host → 2.1.302 (which now ships built-in
`design` and `run` skills — new activation competitors), and the
`~/.claude/CLAUDE.md` leak is gone. Measuring only 4.5.2 would put those into
the delta. The 4.2.1 and old 4.2.2 numbers stay as history.

## Phase 0 findings (verification)

- `SKILL.md` Setup step 1 is **byte-identical to 4.2.2**: it already named the
  skill folder ("not a plugin root two levels above it") since #750. Steps 2–3
  unchanged. On Windows it still says to call the quoted
  `"${CLAUDE_SKILL_DIR}/scripts/impeccable.cmd"` with no `&` call operator.
- The #756 change is the "Launcher unavailable" paragraph only: now a fixed
  message ("Context loading did not run; I'll read the existing project context
  directly.") sent **before the next tool call**, and explicitly covering
  planning as well as editing.
- Other diffs: engine 0.1.3 → 0.1.14, new `generate` command and references
  (`generate.md`, `component-review.md`, `mode-*.md`, `region-map.md`), new
  "loaded symbols" rule, launcher `.cmd` rewritten (probe handshake).
- The record's `skillSource` is copied from the suite's `target.source`
  (the 4.2.1 commit `831cabee`) and does not identify the build; `skillHash`
  does.

Smoke (store `.assay-smoke`, NOT part of the measurement): 12 attempts
acceptEdits, 0 unknown, 2/5 positives fired, 0/7 FP, 2/2 launcher calls refused,
2/2 resolved the skill dir, 2/2 told the user. Record
`run-2026-10-17T08-01-38-496Z-ffad1069`. New refusal text:
"Command contains malformed syntax that cannot be parsed: pwsh exited with code
1: The command line is too long."

## Chunk ledger

<!--LEDGER-->
<!--/LEDGER-->
