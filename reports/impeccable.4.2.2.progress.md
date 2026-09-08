# 4.2.2 measurement — progress record

**Purpose:** resumable state for the impeccable 4.2.2 run requested in
pbakaus/impeccable#744. If the session resets, continue from here; do not
restart from zero.

## Pins (must not change mid-run)

| | |
| --- | --- |
| Skill | `impeccable` 4.2.2, clean marketplace install |
| Marketplace commit | `2bc2879276c1f321a53c4ca99d3371e411329b52` |
| Install path | `claude plugin marketplace add pbakaus/impeccable` -> `claude plugin install impeccable@impeccable`, isolated `CLAUDE_CONFIG_DIR`, vendored verbatim to `skills/impeccable/` |
| Suite | `suites/impeccable.suite.yaml` v1, `sha256:c820aafc...` — byte-identical to the 4.2.1 runs, DO NOT EDIT |
| Model | `claude-haiku-4-5-20251001` |
| Runner | `npx @ktlsr/assay@0.2.0` — DO NOT CHANGE, the tool must stay constant |
| Modes | `acceptEdits` and `bypassPermissions` (the latter is an instrument, not a recommendation) |
| Attempts | 120 per mode, as 5 chunks of `--repeat 2` (24), orphans cleared between |
| Engine | `scripts/VERSION` 0.1.2 -> **0.1.3**; primed by hand before measuring (see below) |

## Phase 0 — install and diff (DONE)

4.2.2 differs from 4.2.1 in exactly five files:

| File | Change |
| --- | --- |
| `.claude-plugin/plugin.json` | version 4.2.1 -> 4.2.2 |
| `skills/impeccable/SKILL.md` | **the #750 change** — see below |
| `skills/impeccable/scripts/VERSION` | engine 0.1.2 -> 0.1.3 |
| `reference/live.md` | +1 para: no injection into deployed production sites |
| `reference/live-setup.md` | +1 para, same |
| (added) `.grok-plugin/plugin.json`, (dropped) root `LICENSE` | packaging |

`SKILL.md` carries three edits, and they map onto the open findings:

1. **`<skill-base-dir>` -> `${CLAUDE_SKILL_DIR}`**, with the ambiguity spelled
   out: "the directory that contains this SKILL.md (the skill folder, not a
   plugin root two levels above it)". Aimed at finding 4.
2. **Step 3 hardened**: "read craft-floor.md immediately before any UI edit,
   including small refinements". Aimed at finding 2.
3. **New "Launcher unavailable" paragraph**: message the user, then continue
   with permitted tools. Aimed at the acceptEdits refusal path.

Note the reference files still carry the old `<skill-base-dir>` placeholder;
SKILL.md now instructs the model to substitute it. Whether it does is
measurable and is folded into axis 2.

## Host priming (deliberate, matches the 4.2.1 condition)

Engine 0.1.3 is new, so this host was not primed for it. The 4.2.1 runs were
measured on a host already holding 0.1.2, so 0.1.3 was fetched and verified by
hand into `~/.impeccable/bin/0.1.3/` before measuring
(`sha256:50846da0...`, checked against the release sidecar). Without this the
run would be measuring a cold-cache engine bump rather than #750.

**Incidental host finding:** the launcher's own download path cannot self-heal
on this host. `C:\Windows\System32` is not on this shell's PATH, so the
launcher's `where curl.exe` probe fails and it goes straight to `:fail` with
exit 127. Host property, not a skill defect, but it is why priming was needed.

## Status

- [x] Phase 0 — install 4.2.2, record hashes, diff vs 4.2.1
- [x] Phase 1 — acceptEdits, 120 attempts (5 x 24) — DONE, 0 unknown, $8.19, 106.8 min
- [x] Phase 2 — bypassPermissions, 120/120 DONE (4x24 + 2x12), 0 unknown, $12.96, 179.0 min
- [x] Phase 3 — analysis DONE -> reports/impeccable.4.2.2.axes.txt, reports/impeccable.4.2.2.coverage.md
- [x] Phase 4 — DONE: reports/impeccable.4.2.2.md + issues/impeccable-744-4.2.2.comment.md

## Chunk ledger

Machine-readable ledgers: `reports/impeccable.4.2.2.<mode>.ledger.tsv`.
Driver: `tools/run-chunks.ps1 -Mode <mode>` — it is resumable and skips
chunks already recorded with exit 0.

Smoke (scratch store `.assay-smoke`, NOT part of the measurement): 12 attempts,
0 unknown, 3/5 positives fired, 0/7 false positives, 5/5 launcher calls refused
under acceptEdits but **5/5 resolved the base directory correctly**.
Record `run-2026-09-08T09-30-20-440Z-13fc9390`.

<!--LEDGER-->
| Mode | Chunk | Attempts | Record | State |
| --- | --- | --- | --- | --- |
| acceptEdits | acceptEdits-chunk1 | 24 | `run-2026-09-08T09-54-07-766Z-631543d1` | ok |
| acceptEdits | acceptEdits-chunk2 | 24 | `run-2026-09-08T10-15-55-401Z-c4c1faa3` | ok |
| acceptEdits | acceptEdits-chunk3 | 24 | `run-2026-09-08T10-40-28-846Z-06e91f2d` | ok |
| acceptEdits | acceptEdits-chunk4 | 24 | `run-2026-09-08T11-00-59-419Z-38eff4b3` | ok |
| acceptEdits | acceptEdits-chunk5 | 24 | `run-2026-09-08T11-22-26-246Z-a3590f30` | ok |
| **acceptEdits** | **total** | **120 / 120** | | COMPLETE |
| bypassPermissions | bypassPermissions-chunk1 | 24 | `run-2026-09-08T11-59-15-098Z-147c71ed` | ok |
| bypassPermissions | bypassPermissions-chunk2 | 24 | `run-2026-09-08T12-38-29-070Z-0c434e1e` | ok |
| bypassPermissions | bypassPermissions-chunk3 | 24 | `run-2026-09-08T13-17-11-967Z-2b58f036` | ok |
| bypassPermissions | bypassPermissions-chunk4 | 24 | `run-2026-09-08T13-56-09-772Z-bc105e7a` | ok |
| bypassPermissions | bypassPermissions-chunk5 | ? | `NONE` | FAILED exit -1 |
| bypassPermissions | bypassPermissions-chunk5 | ? | `NONE` | FAILED exit -1 |
| bypassPermissions | bypassPermissions-chunk5a | 12 | `run-2026-09-08T14-43-31-131Z-be061f24` | ok |
| bypassPermissions | bypassPermissions-chunk5b | 12 | `run-2026-09-08T15-01-42-733Z-c472c9b7` | ok |
| **bypassPermissions** | **total** | **120 / 120** | | COMPLETE |
<!--/LEDGER-->

## Open problems

1. **Bash / Git `sh` is broken on this host** — `bash.exe: *** fatal error -
   add_item ("\??\C:\Program Files\Git", "/", ...) failed, errno 1`. It bites
   the agent inside the sandbox too, and it bit `claude plugin marketplace add`
   once (succeeded on retry). Present in the 4.2.1 runs as well, so it is a
   constant across the comparison, not a new variable.
2. **`C:\Windows\System32` is not on this shell PATH**, so the launcher's
   `where curl.exe` self-download probe fails. Worked around by priming the
   engine by hand. Host property; recorded in Limitations.
3. **The runner needs credentials from `.env`.** A first smoke run scored
   12/12 `unknown` with "Not logged in · Please run /login". `tools/run-chunks.ps1`
   now loads `.env` and clears `CLAUDE_CONFIG_DIR` (the isolated install dir
   must not leak into the measurement). Do not run the runner without this.

## Instrument validation (done before any 4.2.2 attempt)

`tools/four_axes.py` was written for the four-way split the maintainer asked
for, and was checked against both stored 4.2.1 measurements first. It
reproduces every published figure exactly:

| | 4.2.1 acceptEdits | 4.2.1 bypassPermissions |
| --- | --- | --- |
| activations | 28 | 30 |
| precision / recall | 100% / 56% | 100% / 60% |
| launcher ran / path-fail / parser-fail / refused | 0 / 0 / 0 / 55 | 42 / 9 / 6 / 0 |
| reference files read | 0 | 7 (29 reads, same per-file counts) |
| craft-floor before UI edit | 0 / 28 | 6 / 29 |
| completion fired / DESIGN.md / document.md | 0 / 10 / 0 | 0 / 9 / 0 |

So a difference in the 4.2.2 numbers is a difference in the skill, not in the
instrument.
























